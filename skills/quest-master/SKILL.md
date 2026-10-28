---
name: quest-master
description: >
  Run a quest as its master: the session keeps the quest's records, talks to
  the user, and hands all work in the quest's code checkouts to subagents.
  Use only when the user invokes quest-master.
disable-model-invocation: true
metadata:
  version: "1.0.0"
---

<!-- argument-hint: [quest command] [slug] -->

# Quest Master

Quest master makes this session the user's one point of contact for a quest.
The session keeps the quest's records and sends the work in the quest's code
checkouts to subagents, which report back to it. These rules hold for the
rest of the session, and they come before the `quest` skill's wherever the
two differ.

## Start

Invoke the `quest` skill before anything else, passing on any arguments, and
follow it. Then work on the quest that it opens, creates, or resolves; when
none applies, ask which quest, or whether to create one.

## What You Do Yourself

Your context is for decisions. Work on code fills a context fast, so it goes
to subagents; what you need in order to decide well, you read yourself.

Use tools only for these:

- Read and write the current quest's files, except under `worktrees/`.
- Read and write the realm's `lore/`.
- Read the realm's `AGENTS.md` and the web.
- Read the project's documents, in a checkout or the realm's repository: its
  instructions (`CLAUDE.md`, `AGENTS.md`), as `open` describes, and others
  that say how the project works, such as a README or design notes, when a
  decision needs them.
- Use skills, including `quest` commands such as `new` to create another
  quest.
- Start and direct subagents.

Everything else goes to a subagent: reading code, searching, running
commands, and writing anywhere in a checkout or the realm's repository. This
includes making checkouts and the checkout check before `archive`. When a
decision needs something from the code, ask a subagent for the answer, not
for the code. To find documents beyond those you know of, have a subagent
list the relevant ones with a line on what each covers, and read only the
ones you need.

## Subagents

Brief each subagent with the quest's path, the checkout to work in, the task,
and what the user has authorized. It may read the quest's files for context.
Tell it:

- Never create, change, or delete the quest's files outside `worktrees/`, or
  files in `lore/`, even when the `quest` skill or a checkout's instructions
  say to update the record. Report instead.
- Ask the user nothing. When the work needs a decision or an approval, stop
  and report what is needed and the options.
- End with a short report: what changed, on which branch and revision; what
  was verified and how; what failed or is unfinished, with what resuming it
  needs; and findings the record should keep, with their sources. Leave out
  how it got there.

Pass on only authorizations the user gave, in the user's words. When a
subagent asks for a decision, ask the user, record the answer, and pass it on.

## Records

Only this session writes the quest's records. After each report, update them
under the `quest` skill's update rules, recording the result of the work, not
the report. Keep what the report claimed apart from what was verified, and
when a claim matters to the next step, have a subagent check it.

## The User

The user talks only to this session. Tell them the outcome of each piece of
work and the recommended next step in their terms, not as the subagent's
report, and bring every decision a subagent raised to them.
