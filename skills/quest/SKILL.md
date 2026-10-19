---
name: quest
description: >
  Maintain quests: one directory per task holding a QUEST.md memory record plus
  the documents and code checkouts that belong to that task. Use to set up a
  realm, or to create, open, list, sync, hand off, distill, or archive a quest,
  and to keep its records current while working inside one.
metadata:
  version: "4.1.0"
---

<!-- argument-hint: <realm init|new|open|list|sync|handoff|distill|archive> [path|slug] -->

# Quest

A quest is one directory for one task. It gathers three things in a single
place: `QUEST.md`, the memory that lets an agent resume the task without the
conversation that produced it; the documents the task generates; and the code
checkouts the task works in.

This skill covers finding, creating, maintaining, and archiving that directory.
How the work itself is done is outside it: follow the user's direction and the
instructions of the realm and its repository.

## Layout

```text
<realm>/
├── AGENTS.md                  # declares the quest root and lists the lore
├── lore/                      # facts that outlive any single quest
├── quest-template/            # copied into each new quest; may be empty
├── <repository>/              # the realm's code, usually kept here
└── quests/                    # the quest root
    ├── <slug>/
    │   ├── QUEST.md           # the memory record; the only required file
    │   ├── research/          # findings and evidence, read on demand
    │   ├── local-data/        # private or non-reproducible local files
    │   └── worktrees/         # code checkouts, numbered from 1
    │       ├── 1/             # by default, a clone of the realm's repository
    │       └── <n>/           # by default, a worktree of that clone
    └── .archived/<slug>/      # archived quests, not active
```

A realm is a project set up for quests: the directory whose `AGENTS.md`
declares its quest root and lists its lore. `realm init` makes one. A realm is
never inside a repository, so its quests and lore stay out of the code, and its
repository is the one its quests clone.

Read [Lore](references/lore.md) whenever a task touches lore. It says what
belongs there and how the realm's `AGENTS.md` lists it.

A slug matches `^[a-z0-9]+(?:-[a-z0-9]+)*$`; reject paths and other names.
Create a file or directory only when there is something to put in it. Follow a
layout the realm's instructions configure, and any coherent structure a quest
already has, rather than rearranging it to match this one.

## Resolve The Quest

Resolve the quest root once per operation, starting from the session's current
working directory (never the skill directory), and use its absolute path for
every quest read, write, and search in that operation.

1. Look at the working directory and its ancestors for a directory that has a
   slug name, contains `QUEST.md`, and sits directly inside a directory named
   `quests`. That directory is the current quest and its parent is the root.
   This check comes first so that a session started inside a quest, including
   inside one of its checkouts, identifies it without any configuration.
2. Otherwise use a `Quest root: <path>` declaration from the instructions
   already in context, normally the realm's `AGENTS.md`. Resolve a relative
   path from the directory of the file that declares it; the most specific
   applicable declaration wins.
   It counts only when it resolves to an existing directory named `quests`.
   Work from the instructions already loaded rather than searching for more.
3. Otherwise use the working directory if it is named `quests`, or `./quests`
   if that directory exists.
4. Otherwise stop and report which candidates were checked. Creating a `quests`
   directory so that resolution succeeds, or guessing a root from repository
   depth, puts records where nobody will look for them.

`realm init` is the exception: it sets up a realm that may not have a root
yet.

A command acts on an explicit slug in the resolved root. Without one it acts on
the current quest or, in a session outside any quest, on the quest that session
last created or opened. When none of these applies, ask which quest is meant.
`archive` is stricter, as its guide says. A session does not have to run in the
quest directory, so resolve relative paths in a quest's records from that
quest's directory. Only `new` creates a quest, and nothing replaces an existing
quest directory or file.

## Quest Record

`QUEST.md` is the only required record and `Current State` its only required
section. A new record starts like this, with `quest_skill_version` set to this
skill's `metadata.version`:

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

`quest_skill_version` records the version a quest was created under, so leave it
unchanged afterwards. Records without it are valid.

`Current State` is the handoff. An agent with no session history should be able
to read it, follow only the links relevant to the next step, and continue
correctly. The template's fields say what that takes; they are a starting
point, so use the prose or bullets that suit the work. Keep this section near
the top and short enough to read in one pass, linking to detail instead of
including it.

Larger quests can add two sections: `Backlog` for pending or deferred work
outside the immediate next actions, and `References` as an annotated index of
supporting material that says why each link matters.

An unchecked checklist item is pending; check it once its outcome is recorded.
Prefix an item with `Approval:` when it needs an explicit decision from the
user, and check it only on their explicit authorization. While one is waiting,
say so under Blockers and make the next action the request for that decision.

## Shared Update Contract

These rules apply to `QUEST.md` and to every supporting file.

**Write what is true now.** The record is a maintained description of the task,
not a log of the sessions that worked on it. When something changes, replace the
old checkpoint, next action, plan, or decision instead of adding a new entry
beside it, and correct any linked file the change makes misleading. A reader who
finds two statements that disagree has to investigate which one is current, and
sparing them that investigation is what the record is for.

**Apply the retention test.** Keep an item when losing it could cause a worse
decision, a repeated investigation, a forgotten obligation, or a wrong
resumption, or when it is a requested deliverable or needed for audit. Remove
what fails the test rather than labelling it superseded. When an abandoned
approach would otherwise be rediscovered, keep one line: "Rejected A because X."
Ask before deleting material whose owner or purpose is unclear.

**Keep each fact in one place.** Link to the file or authoritative source that
owns a fact instead of copying it. Volatile state, such as active work, blockers,
and next actions, belongs in `Current State` so that supporting files stay
stable. Leave out state that Git or another tool reports live, such as whether
a commit is pushed or how far a branch is ahead or behind: it goes stale as
soon as someone acts, and the tool remains its owner. When such a step is the
quest's own pending work, record it as a next action.

**Record who made each decision.** Say whether the user or the agent made it. A
resuming agent may revisit an agent's choice when the facts change, but must
ask before changing the user's. Write an open question as open. If a change
invalidates a plan and its replacement is not yet decided, remove the stale
plan and state the gap instead of inventing one.

**Keep evidence tied to what it tested.** Name the revision or observation time
a result applies to, and do not let it stand for later work. Record a failed or
partial attempt as such, with what is needed to resume it or avoid repeating it.

**Update when durable context changes**, not after every action: a new
checkpoint, decision, blocker, or next action. Reread the affected content just
before editing so that concurrent updates survive, and edit narrowly. Chat
history, terminal output, running processes, and session IDs do not outlive the
session, so anything needed later has to be written into the record.

The record does not replace talking to the user. Tell them the outcome and the
recommended next step directly as well as recording it.

## Documents And Code

Supporting documents, such as research, designs, plans, evidence, and
deliverables, live in the quest directory, organized by subject. Extend the file
that already owns a subject rather than adding one per session, worker, or
activity. Start a separate file when the detail would obscure `QUEST.md` or when
the file is itself a deliverable, and link it from `QUEST.md`. Keep the layout
shallow.

`research/` keeps code exploration and source research available without loading
it by default. Put synthesized findings there, with their sources and the
revision or date observed when freshness matters, and keep in `QUEST.md` only
the conclusions needed to act. Read research files selectively, when a decision
needs their detail, and recheck a finding against the current code or live state
before acting on it. Anything an agent must know to act correctly belongs in the
plan or `Current State`, not only in background research.

Keep the evidence that substantiates a result rather than the output of every
run.

Code checkouts live under `worktrees/`, numbered from 1. Record each one in
`Current State`. Inside a checkout, that repository's own instructions govern
the work.

Do not `cd` into a checkout. A `cd` outlives the command that ran it, so every
later command, and the harness, would run inside the checkout. Point commands
at the checkout instead, for example `git -C <checkout>` or `make -C
<checkout>`.

Unless the realm's instructions arrange checkouts another way, `worktrees/1`
is a copy-on-write clone of the realm's repository and every further checkout
is a Git worktree of that clone. Always make the clone from the repository's local
`main`, after bringing `main` up to date with `origin`:

```sh
git -C <repository> pull --ff-only origin main
cp -a --reflink=always <repository> <quest>/worktrees/1
git -C <quest>/worktrees/1 worktree add -b <branch> ../<n>
```

The clone has its own `.git`, so the quest's branches and worktree
registrations stay inside `worktrees/`, and removing `worktrees/` leaves
nothing behind in the realm's repository. Removing it also discards any commit
that exists only there, which is why archiving checks for unmerged work first.

The copy is of a whole checkout, so:

- The repository must have `main` checked out, in a checkout whose `.git` is a
  directory, not a linked worktree. If it is on another branch, or `main`
  cannot fast-forward, stop and say so instead of switching branches or
  merging.
- Right after copying, delete the copy's `.git/worktrees/` if it exists. It
  holds the source's worktree registrations, which point outside the quest.
- The copy includes the source's uncommitted changes. Discard those that are
  not the quest's.
- On a filesystem without reflinks the copy fails and leaves empty directories.
  Remove them and make `worktrees/1` a worktree of the realm's repository
  instead: `git -C <repository> worktree add -b <branch> <quest>/worktrees/1
  main`. The quest's branches and registrations then live in that repository,
  so say so in `Current State` and remove those checkouts with
  `git worktree remove`.

## Versioned Checkpoints

`scripts/snapshot.py` makes each active quest directory its own Git repository
and commits the quest's records there, including partial state and other
writers' edits. A harness hook runs it around every turn, so snapshots need
nothing from the agent. [Snapshots](references/snapshot.md) describes the
script and the hook.

The script owns each quest's `.git`; do not initialize it or commit to it by
hand. It refuses a quest root that is inside a repository, and leaves
`worktrees/`, `local-data/`, and nested repositories out of
snapshots. Put other private or generated material in those excluded locations,
or add a rule to the quest's own `.gitignore` before creating it.

Snapshots are recovery points. The current files remain the only thing a
resuming agent should need to read. Check the quest's own `git log` before
counting on history to recover removed material.

Archiving keeps the quest's `.git` directory and ends its snapshots.

## Opening A Quest

Always read `QUEST.md` first, then the first checkout's instructions:
`worktrees/1/CLAUDE.md` when you are Claude Code and `worktrees/1/AGENTS.md`
otherwise, falling back to the other file when yours does not exist. They
govern the work in the checkout, and a session started outside that checkout
does not load them on its own. When the prompt only opens a quest, read nothing
else and brief the user as the [Open](references/open.md#the-summary) guide
describes: in plain language, what the quest is about, where the work left off,
and what to do next, not a retelling of the record. Then wait. Recorded next
actions describe where the work stands; they are not a request to carry them
out. When the same prompt also asks for something, load what that request
needs and proceed in the same turn.

After that, load context for the decision at hand, starting with the records
that govern the active task, rather than reading the whole quest.

## Commands

Route by intent, whether it arrives as a command or in plain language, and read
the matching guide before acting.

| Command | Use when | Guide |
| --- | --- | --- |
| `realm init` | Setting up a project for quests, making it a realm. | [Realm init](references/realm-init.md) |
| `new` | Creating a quest and capturing its goal. | [New](references/new.md) |
| `open` | Opening an existing quest. | [Open](references/open.md) |
| `list` | Listing quests. | [List](references/list.md) |
| `sync` | Bringing the record up to date with the session. | [Sync](references/sync.md) |
| `handoff` | Preparing for a reset, transfer, or pause, or checking that another agent could resume. | [Sync: recoverability check](references/sync.md#recoverability-check) |
| `distill` | Moving quest findings into the realm's maintained documentation. | [Knowledge transfer](references/distill.md) |
| `archive` | Archiving a quest and cleaning up its checkouts. | [Archive](references/archive.md) |
