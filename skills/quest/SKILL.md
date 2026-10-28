---
name: quest
description: >
  Maintain quests: one directory per task holding a QUEST.md memory record plus
  the documents and code checkouts that belong to that task. Use to set up a
  realm, or to create, open, list, sync, hand off, distill, or archive a quest,
  and to keep its records current while working inside one.
metadata:
  version: "6.1.0"
---

<!-- argument-hint: <realm init|new|open|list|sync|handoff|distill|archive> [path|slug] -->

# Quest

A quest is one directory for one task. It holds `QUEST.md`, the record that
lets an agent resume the task without the conversation that produced it, along
with the task's documents and code checkouts. This skill finds, creates,
maintains, and archives that directory; how the work is done is up to the user
and the instructions of the realm and its repository.

## Layout

```text
<realm>/
├── AGENTS.md                  # sets up quests and lists the lore
├── lore/                      # facts that outlive any single quest
├── quest-template/            # copied into each new quest; may be empty
├── <repository>/              # the realm's code, usually kept here
└── quests/                    # the quest root
    ├── <slug>/
    │   ├── QUEST.md           # the record; the only required file
    │   ├── research/          # findings and evidence, read on demand
    │   ├── local-data/        # private or non-reproducible local files
    │   └── worktrees/         # code checkouts, numbered from 1
    └── .archived/<slug>/      # archived quests
```

A realm, made by `realm init`, is never inside a repository, so its quests and
lore stay out of the code. Read [Lore](references/lore.md) whenever a task
touches `lore/`. A slug matches `^[a-z0-9]+(?:-[a-z0-9]+)*$`; reject paths and
other names. Create a file or directory only when there is something to put in
it, and keep a layout the realm or the quest already uses.

## Resolve The Quest

Resolve the quest root once per operation, from the session's working
directory (never the skill directory), and use its absolute path throughout:

1. If the working directory or an ancestor is a slug-named directory holding
   `QUEST.md` directly inside a directory named `quests`, that is the current
   quest, even from inside one of its checkouts, and its parent is the root.
2. Otherwise use the nearest `quests` directory: the working directory or an
   ancestor that is named `quests` or contains one, skipping any inside a Git
   repository.
3. Otherwise stop and report which directories you checked. Never create
   `quests` to make resolution succeed.

Without a slug, a command acts on the current quest, or else on the one the
session last created or opened; when neither applies, ask. Resolve relative
paths in a record from its quest's directory. Only `new` creates a quest, and
nothing replaces an existing quest directory or file.

## Quest Record

A new `QUEST.md` starts like this, with `quest_skill_version` set to this
skill's `metadata.version` and never changed afterwards:

```markdown
---
quest_skill_version: "<metadata.version>"
---

# Quest Title

## Current State

- Objective: The desired outcome and what would count as success.
- Constraints: What the user has and has not authorized, and other material limits.
- Workspace: Each checkout's path, branch, and purpose, with any ports or services allocated to the quest, or none.
- Active work: The active tasks, or none.
- Checkpoint: The latest durable result, what has been verified on which revision, and where to check it.
- Next actions: The exact resumption step for each active task, or that the work is complete or paused.
- Blockers: None, or the unresolved blockers and decisions waiting on the user.
```

`Current State` is the handoff: an agent with no session history must be able
to read it, follow only the links the next step needs, and continue correctly.
Keep it near the top and short, linking to detail. Larger quests can add
`Backlog` for deferred work and `References`, an index saying why each link
matters.

An unchecked checklist item is pending; check it once its outcome is recorded.
Prefix an item with `Approval:` when it needs the user's explicit decision,
check it only on their explicit authorization, and while it waits, name it
under Blockers and make asking for it the next action. Work already done
toward it waits on the user; do not repeat it.

## Update Rules

These apply to `QUEST.md` and every supporting file.

1. **Write what is true now.** The record describes the task, not the sessions
   that worked on it. Replace an old checkpoint, next action, plan, or
   decision instead of adding an entry beside it, and correct linked files the
   change makes misleading. A reader who finds two statements that disagree
   cannot tell which is current.
2. **Keep only what matters later**: what prevents a worse decision, a
   repeated investigation, a forgotten obligation, or a wrong resumption, plus
   deliverables. Remove the rest rather than marking it superseded; for an
   abandoned approach, keep one line: "Rejected A because X." Ask before
   deleting material whose owner or purpose is unclear.
3. **Keep each fact in one place**, linking to its owner. Active work,
   blockers, and next actions belong in `Current State`. Leave out what Git or
   another tool reports live, such as whether a commit is pushed.
4. **Record who decided**, the user or the agent. Revisit an agent's choice
   when facts change; ask before changing the user's. Write an open question
   as open, and replace a plan that stopped holding with the gap, not a guess.
5. **Tie evidence to the revision or time it tested.** Record a failed or
   partial attempt as such, with what resuming it needs.
6. **Update when durable context changes**: a new checkpoint, decision,
   blocker, or next action. Reread just before editing and edit narrowly.
   Chat, terminal output, and running processes die with the session.
7. **Tell the user too**: the outcome and the recommended next step.

Supporting documents live in the quest directory by subject: extend the file
that owns a subject rather than adding one per session, and link it from
`QUEST.md`. Put findings in `research/` with their sources and when they were
observed, keep in `QUEST.md` only the conclusions needed to act, and recheck a
finding before acting on it.

## Code Checkouts

Checkouts live under `worktrees/`, numbered from 1, and each is recorded in
`Current State`. Inside one, its repository's instructions govern the work;
read them as [Open](#open) describes before working there.

**Never `cd` into a checkout**, not even as `cd <checkout> && <command>`: the
shell stays there for every later command. Use the tool's directory option,
such as `git -C <checkout>` or `make -C <checkout>`, or absolute paths.

Unless the realm arranges checkouts another way, `worktrees/1` is a
copy-on-write clone of the realm's repository, taken from `main` once `main`
is up to date, and further checkouts are worktrees of that clone:

```sh
git -C <repository> pull --ff-only origin main
cp -a --reflink=always <repository> <quest>/worktrees/1
rm -rf <quest>/worktrees/1/.git/worktrees
git -C <quest>/worktrees/1 worktree add -b <branch> ../<n>
```

- The repository must have `main` checked out, with `.git` a directory. If it
  is on another branch, or `main` cannot fast-forward, stop and say so; do not
  switch branches or merge.
- The `rm` drops the source's worktree registrations. The copy also carries
  the source's uncommitted changes: discard those that are not the quest's.
- Without reflinks the copy fails, leaving empty directories. Remove them and
  run `git -C <repository> worktree add -b <branch> <quest>/worktrees/1 main`
  instead; say in `Current State` that the quest's branches then live in the
  realm's repository, and remove such checkouts with `git worktree remove`.

## Snapshots

A hook runs `quest snapshot` (the skill's `bin/quest`) around every turn. It
commits each active quest's records to the quest's own `.git`, leaving out
`worktrees/`, `local-data/`, and nested repositories. Never initialize or
commit to that `.git` by hand. Keep other private or generated files in those
excluded places, or add a `.gitignore` rule before creating them.
[Snapshots](references/snapshot.md) covers the command and other harnesses.

## Commands

Route by intent, whether a command or plain language. Before `realm init` or
`archive`, read [Realm init](references/realm-init.md) or
[Archive](references/archive.md). The other commands follow.

### New

`new <slug>` refuses an invalid or existing slug, then creates
`<root>/<slug>/QUEST.md` from the template above. Capture the objective,
background, and constraints the user supplied, linking substantial material.
Keep what the user stated apart from what was only suggested, and record a
missing objective as unresolved rather than inventing one. Current State
starts with no task begun and a checkpoint that the quest was created.

Copy the realm's `quest-template/` in unchanged, unless the realm's
instructions say otherwise, and do the setup they require, such as choosing a
port, recording paths and ports but never secrets:

```sh
cp -a <realm>/quest-template/. <root>/<slug>/
```

Make checkouts only when authorized, and no `git init`. Then summarize the
captured goal and ask the smallest useful question only if a gap could change
the work. Creating a quest starts no research, planning, or implementation
unless the same request asks for it. For an issue, a slug keeps the issue
number first; for a pull request, it is `pr-<number>-<description>`.

### Open

`open [slug]` opens the named quest, or the one resolution selects; with
neither, ask which and show the `list`. For a slug with no exact match, open a
single clearly similar one and say so, or list several and ask.

Read `QUEST.md`, then the first checkout's instructions:
`worktrees/1/CLAUDE.md` when you are Claude Code and `worktrees/1/AGENTS.md`
otherwise, falling back to the other file. A session started outside that
checkout does not load them on its own. Read nothing else, and change nothing.

When the prompt only opens the quest, brief the user and then wait: recorded
next actions say where the work stands, not that you should do them. When it
also asks for something, load what that needs and proceed in the same turn.

The user arrives cold, often from another task. Brief them as a colleague
would in half a minute, from `QUEST.md` alone, under three headings:

1. **The quest**: the slug and title as a first-level heading, then one or two
   sentences, in your own words, on the problem and the outcome wanted.
2. **Where we left off**: three to five sentences on what is now known or
   built, and where the work stopped and why: under way, waiting on the user,
   paused, or complete. The result, not its history.
3. **What to do next**: a numbered list of at most three one-sentence items the
   user can answer with a number. Decisions and approvals waiting on the user
   come first, as questions naming the options. Then the step you would take
   on their go-ahead: the recorded next action or, failing one, a suggestion
   marked as such.

Leave out constraints and authorizations, decisions already made, the
workspace and ports, revisions, dates, measurements, evidence, how a finding
was reached, and how things work inside, unless an item depends on one. Write
a dozen sentences at most, whatever the record's size: plain words, one idea
per sentence, keeping "because", "so", and "but". Describe a thing rather than
using the record's name for it, and say "probably" when unsure. For example:

```markdown
# slow-invoice-export: Invoice export times out for large accounts

Customers with many invoices cannot download their yearly export, because the request times out. You want the export to work for an account of any size.

## Where we left off

We found the cause. The export loads every invoice into memory before it writes the file, and that takes too long for the largest accounts. A version that writes the file as it reads is built and passes its tests, but it has not been tried on a large account. The work stopped there because that trial needs a copy of production data, which you have not approved.

## What to do next

1. May I use a copy of production data to try the new export on a large account?
2. Suggestion: if not, I build a large account locally and try it on that.
```

### List

`list` shows the root's quest directories, sorted by slug, marking one without
`QUEST.md` as invalid. Leave out `.archived` unless asked.

### Sync And Handoff

`sync` brings the quest's records up to date with the session under the
update rules; with nothing material to add, it changes nothing. It neither
pushes nor continues the work.

`handoff`, or preparing for a reset, transfer, or pause, is a thorough sync
that makes the record enough to resume from. Write down results and decisions
still only in chat, repair stale or contradictory records, and keep done,
attempted, in-flight, and unstarted work distinct. Then read Current State as
a fresh agent: the goal, constraints, checkpoint, evidence limits, blockers,
and exact next action of each active task must be clear without a
chronology. When you can, give an agent with no session history only
`QUEST.md` and ask what it leaves out or says two ways; a record's author
reads past its own gaps. Report whether the record is ready, or the exact gap.

### Distill

`distill` moves findings later work needs into the realm's maintained
documentation, such as [lore](references/lore.md), docs, or runbooks. Update
the file that owns a subject rather than writing a per-quest learnings file,
check findings against the current code, and keep tentative findings and
one-off workarounds out of standing rules. Make in-scope documentation edits;
propose, and wait for approval of, changes to shared instructions or policy,
another repository, or a decision the user reserved. Distilling authorizes no
commit or publication. Report what changed and any obligation still open;
nothing to transfer is a valid result.
