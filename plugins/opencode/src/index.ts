import { execFile } from "node:child_process"
import { existsSync, readFileSync, realpathSync, statSync } from "node:fs"
import { dirname, join, resolve as resolvePath } from "node:path"
import { Plugin } from "@opencode/plugin"

// Tools for quests. Each runs the installed quest skill's bin/quest, so the
// rules stay in one place: the skill and its command. The plugin adds only
// what a command cannot know: which session asks, and which quest it is on.

type Where = { quest: string | null; root: string | null; realm: string | null }
type Shown = { realm: string; slug: string; dir: string; title: string | null }

const ENTRY = "quest"

class QuestError extends Error {}

function run(bin: string, args: string[], cwd: string, signal?: AbortSignal) {
  return new Promise<{ code: number; stdout: string; stderr: string }>((resolve, reject) => {
    execFile("python3", [bin, ...args], { cwd, signal, maxBuffer: 16 * 1024 * 1024 }, (error, stdout, stderr) => {
      if (error && typeof error.code !== "number") return reject(error)
      resolve({ code: error ? (error.code as number) : 0, stdout, stderr })
    })
  })
}

async function json<T>(bin: string, args: string[], cwd: string, signal?: AbortSignal): Promise<T> {
  const result = await run(bin, args, cwd, signal)
  if (result.code !== 0) throw new QuestError(result.stderr.trim() || `quest ${args[0]} exited with ${result.code}`)
  return JSON.parse(result.stdout) as T
}

// The first checkout the record's Workspace bullet names: the first absolute
// path in it that is the top of a Git checkout.
function firstCheckout(record: string): string | undefined {
  const state = record.split(/^## Current State$/m)[1]?.split(/^## /m)[0] ?? ""
  const workspace = state.match(/^- Workspace:([\s\S]*?)(?=^- |\n*$)/m)?.[1] ?? ""
  for (const [path] of workspace.matchAll(/\/[^\s`'",;)]+/g)) {
    const clean = path.replace(/[.:]+$/, "")
    if (existsSync(join(clean, ".git"))) return clean
  }
}

function instructions(checkout: string): { file: string; text: string } | undefined {
  for (const name of ["AGENTS.md", "CLAUDE.md"]) {
    const file = join(checkout, name)
    if (existsSync(file)) return { file, text: readFileSync(file, "utf8") }
  }
}

function isDirectory(path: string) {
  try {
    return statSync(path).isDirectory()
  } catch {
    return false
  }
}

export default Plugin.define({
  id: "quest",
  async setup(ctx) {
    // bin/quest of the installed quest skill, or the path in the plugin's options.
    async function questBin(): Promise<string> {
      const configured = ctx.options.bin
      if (typeof configured === "string") return configured
      const skills = await ctx.skill.list()
      const skill = skills.data.find((info) => info.id === "quest" || info.name === "quest")
      if (!skill) throw new QuestError("the quest skill is not installed, so bin/quest cannot be found")
      return join(dirname(skill.path), "bin", "quest")
    }

    async function sessionDirectory(sessionID: string): Promise<string> {
      return (await ctx.session.get({ sessionID })).location.directory
    }

    async function linked(key: string): Promise<string | undefined> {
      const value = await ctx.storage.get(key)
      return typeof value === "string" && existsSync(join(value, "QUEST.md")) ? value : undefined
    }

    // A quest by slug, else the one linked to the session or its directory,
    // else the one the directory is in. Nothing found is an error that says
    // how to look further, since `where` looks only upward.
    async function resolve(
      input: { path?: string; slug?: string; realm?: string },
      sessionID: string,
      signal?: AbortSignal,
    ): Promise<string> {
      const bin = await questBin()
      const directory = await sessionDirectory(sessionID)
      if (input.path) {
        const given = resolvePath(directory, input.path)
        const quest = existsSync(given) ? realpathSync(given) : given
        if (!existsSync(join(quest, "QUEST.md"))) {
          throw new QuestError(`${quest} is not a quest: it holds no QUEST.md, or does not exist`)
        }
        return quest
      }
      if (input.slug) {
        if (input.realm) {
          return (await json<Shown>(bin, ["show", input.realm, input.slug], directory, signal)).dir
        }
        const listing = await json<{ quests: Shown[] }>(bin, ["list"], directory, signal)
        const matches = listing.quests.filter((quest) => quest.slug === input.slug)
        if (matches.length === 1) return matches[0].dir
        if (matches.length > 1) {
          throw new QuestError(
            `quest ${input.slug} is in more than one realm; pass realm: ` +
              matches.map((quest) => quest.realm).join(", "),
          )
        }
        throw new QuestError(`no active quest ${input.slug}; quest_list shows the quests`)
      }
      const known = (await linked(`session/${sessionID}`)) ?? (await linked(`directory/${directory}`))
      if (known) return known
      const result = await run(bin, ["where", directory], directory, signal)
      const found = result.code === 0 ? (JSON.parse(result.stdout) as Where) : undefined
      if (found?.quest) return found.quest
      throw new QuestError(
        `${directory} is in no quest and this session is linked to none; ` +
          "pass a slug, or find the quest with quest_list",
      )
    }

    async function announce(sessionID: string, quest: string) {
      await ctx.session.instructions.entry.put({
        sessionID,
        key: ENTRY,
        value:
          `This session works on the quest at ${quest}. Before working on it, open it with ` +
          `quest_open (or the quest skill's open), and keep ${join(quest, "QUEST.md")} current.`,
      })
    }

    const text = (content: string) => ({ content })

    await ctx.tool.transform((editor) => {
      editor.namespace({
        name: "quest",
        description:
          "Quests: one directory per task, with a QUEST.md record. These tools run the quest skill's bin/quest; " +
          "the skill says how to write the record.",
      })

      editor.add({
        name: "list",
        description:
          "List the quests in every realm of every world, as JSON with each quest's realm, slug, title, and dir.",
        input: {
          type: "object",
          properties: {
            realm: { type: "string", description: "Only this realm's quests" },
            archived: { type: "boolean", description: "Include archived quests" },
          },
          additionalProperties: false,
        },
        options: { namespace: "quest", codemode: false },
        execute: async (raw, context) => {
          const input = raw as { realm?: string; archived?: boolean }
          const args = ["list", ...(input.realm ? ["--realm", input.realm] : []), ...(input.archived ? ["--archived"] : [])]
          const result = await run(await questBin(), args, await sessionDirectory(context.sessionID), context.signal)
          if (result.code !== 0) throw new QuestError(result.stderr.trim())
          return text(result.stdout)
        },
      })

      editor.add({
        name: "open",
        description:
          "Open a quest: return its QUEST.md and the instructions (AGENTS.md, else CLAUDE.md) of the first checkout " +
          "its Workspace names. Without a slug, opens the quest linked to this session or its directory, or the " +
          "quest the session's directory is in. Changes nothing.",
        input: {
          type: "object",
          properties: {
            path: { type: "string", description: "The quest's directory, instead of a slug" },
          slug: { type: "string", description: "The quest's slug" },
            realm: { type: "string", description: "The realm, when the slug is in more than one" },
          },
          additionalProperties: false,
        },
        options: { namespace: "quest", codemode: false },
        execute: async (raw, context) => {
          const input = raw as { path?: string; slug?: string; realm?: string }
          const quest = await resolve(input, context.sessionID, context.signal)
          const record = readFileSync(join(quest, "QUEST.md"), "utf8")
          const checkout = firstCheckout(record)
          const found = checkout ? instructions(checkout) : undefined
          const parts = [`Quest: ${quest}`, `--- ${join(quest, "QUEST.md")} ---`, record]
          if (found) parts.push(`--- ${found.file} (the first checkout's instructions) ---`, found.text)
          else parts.push(checkout ? `The first checkout, ${checkout}, has no AGENTS.md or CLAUDE.md.` : "The record names no checkout.")
          return text(parts.join("\n\n"))
        },
      })

      editor.add({
        name: "new",
        description:
          "Create a quest with quest new: refuses an invalid slug or an existing quest, copies the realm's " +
          "quest-template, and writes QUEST.md. Then fill in the record as the quest skill's New says.",
        input: {
          type: "object",
          properties: {
            slug: { type: "string", description: "The quest's slug: lowercase words joined by hyphens" },
            title: { type: "string", description: "The quest's title, one line" },
            root: { type: "string", description: "The quest root (default: the one the session's directory is in)" },
            noTemplate: { type: "boolean", description: "Do not copy the realm's quest-template" },
          },
          required: ["slug", "title"],
          additionalProperties: false,
        },
        options: { namespace: "quest", codemode: false },
        execute: async (raw, context) => {
          const input = raw as { slug: string; title: string; root?: string; noTemplate?: boolean }
          const args = [
            "new", "--title", input.title,
            ...(input.root ? ["--root", input.root] : []),
            ...(input.noTemplate ? ["--no-template"] : []),
            "--", input.slug,
          ]
          const result = await run(await questBin(), args, await sessionDirectory(context.sessionID), context.signal)
          if (result.code !== 0) throw new QuestError(result.stderr.trim())
          return text(result.stdout)
        },
      })

      const archiveInput = {
        type: "object",
        properties: {
          path: { type: "string", description: "The quest's directory, instead of a slug" },
          slug: { type: "string", description: "The quest's slug" },
          realm: { type: "string", description: "The realm, when the slug is in more than one" },
          checkouts: {
            type: "array",
            items: { type: "string" },
            description: "Every checkout the quest's record lists, by absolute path",
          },
        },
        required: ["checkouts"],
        additionalProperties: false,
      } as const

      editor.add({
        name: "archive_check",
        description:
          "Report what removing a quest's checkouts would lose, with quest archive --check. Read the quest skill's " +
          "references/archive.md first. Changes nothing but fetched refs.",
        input: {
          ...archiveInput,
          properties: {
            ...archiveInput.properties,
            target: { type: "string", description: "The remote branch work is merged into (default: origin/main)" },
          },
        },
        options: { namespace: "quest", codemode: false },
        execute: async (raw, context) => {
          const input = raw as { path?: string; slug?: string; realm?: string; checkouts: string[]; target?: string }
          const quest = await resolve(input, context.sessionID, context.signal)
          const args = [
            "archive", "--check", quest,
            ...input.checkouts.flatMap((path) => ["--checkout", path]),
            ...(input.target ? ["--target", input.target] : []),
          ]
          const result = await run(await questBin(), args, dirname(quest), context.signal)
          // 0: no findings; 1: findings, listed in the report; anything else: stopped.
          if (result.code > 1) throw new QuestError(`${result.stdout}\n${result.stderr}`.trim())
          return text(`${result.stdout}${result.stderr}`)
        },
      })

      editor.add({
        name: "archive",
        description:
          "Move a quest to .archived/ with quest archive, once its checkouts are removed. Only on the user's " +
          "explicit request, after the steps in the quest skill's references/archive.md.",
        input: archiveInput,
        options: { namespace: "quest", codemode: false },
        execute: async (raw, context) => {
          const input = raw as { path?: string; slug?: string; realm?: string; checkouts: string[] }
          const quest = await resolve(input, context.sessionID, context.signal)
          await ctx.permission.assert({
            sessionID: context.sessionID,
            agent: context.agent,
            source: { type: "tool", messageID: context.messageID, id: context.id },
            action: "quest_archive",
            resources: [quest],
          })
          const args = ["archive", quest, ...input.checkouts.flatMap((path) => ["--checkout", path])]
          const result = await run(await questBin(), args, dirname(quest), context.signal)
          if (result.code !== 0) throw new QuestError(`${result.stdout}\n${result.stderr}`.trim())
          return text(result.stdout)
        },
      })

      editor.add({
        name: "link",
        description:
          "Link this session and its directory to a quest, so that this session and any later one in the same " +
          "directory, such as a worktree outside the realm, finds the quest. Returns the session ID and directory; " +
          "write them into the record's Workspace yourself. Without a slug, links the quest quest_open would open.",
        input: {
          type: "object",
          properties: {
            path: { type: "string", description: "The quest's directory, instead of a slug" },
          slug: { type: "string", description: "The quest's slug" },
            realm: { type: "string", description: "The realm, when the slug is in more than one" },
          },
          additionalProperties: false,
        },
        options: { namespace: "quest", codemode: false },
        execute: async (raw, context) => {
          const input = raw as { path?: string; slug?: string; realm?: string }
          const quest = await resolve(input, context.sessionID, context.signal)
          const directory = await sessionDirectory(context.sessionID)
          await ctx.storage.set(`session/${context.sessionID}`, quest)
          await ctx.storage.set(`directory/${directory}`, quest)
          await announce(context.sessionID, quest)
          return text(JSON.stringify({ quest, sessionID: context.sessionID, directory }, null, 2))
        },
      })
    })

    // A session that starts in, or moves to, a linked directory or a quest's
    // own directory is told which quest it is on.
    const controller = new AbortController()
    void (async () => {
      const events = ctx.event.subscribe({ types: ["session.created", "session.moved"], signal: controller.signal })
      for await (const event of events) {
        try {
          const sessionID = event.data.sessionID
          const directory = await sessionDirectory(sessionID)
          let quest = (await linked(`session/${sessionID}`)) ?? (await linked(`directory/${directory}`))
          if (!quest && isDirectory(directory)) {
            const result = await run(await questBin(), ["where", directory], directory)
            if (result.code === 0) quest = (JSON.parse(result.stdout) as Where).quest ?? undefined
          }
          if (quest) {
            await ctx.storage.set(`session/${sessionID}`, quest)
            await announce(sessionID, quest)
          } else if (event.type === "session.moved") {
            await ctx.session.instructions.entry.remove({ sessionID, key: ENTRY }).catch(() => {})
          }
        } catch (error) {
          console.error("quest plugin:", error)
        }
      }
    })().catch((error) => {
      if (!controller.signal.aborted) console.error("quest plugin: event stream ended:", error)
    })
    return () => controller.abort()
  },
})
