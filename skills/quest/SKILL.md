---
name: quest
description: >
  Open, create, list, archive, and maintain durable quest records for work that spans
  sessions or needs a recoverable handoff. Use for quest workspace discovery,
  current-state reconciliation, project installation, lifecycle commands, and routing work to an
  optional quest capability skill.
---

<!-- argument-hint: <install|open|new|list|archive> [path|slug] -->

# Quest

Use quests as lightweight shared context, not as a mandatory project process.
A quest may involve any kind of work, and its activities need not follow a
linear sequence. This skill is the durable memory layer: it does not select or
enforce a workflow. Users, individual capabilities, or an explicitly selected
orchestrator may direct the work independently.

Quest memory is a maintained representation of current understanding, not an
activity log or an archive of how that understanding evolved. Goals, research,
decisions, and plans must reflect the current contract. Preserve information
when losing it could cause a later agent to make a
materially worse decision, repeat costly investigation, overlook an unresolved
obligation, or resume incorrectly. Routine activity alone does not require a
durable record. Explicit deliverable, provenance, and audit requirements still
apply.

## Resolve The Quest

Resolve the quest root and any current quest context once per operation from
the session's current working directory, never from the skill directory:

Exception: `install` bootstraps a project that may not have a quest root yet.
Use its dedicated reference to select the installation target instead.

1. First inspect the current working directory and its ancestors for a
   canonical quest directory. A candidate must have a slug basename, contain
   `README.md`, and have a parent named `quests`. When a match exists, it is the
   current quest and its parent is the quest root. Run this check before
   considering any configured root so a quest opened directly remains
   self-identifying.
2. If the session is not inside a quest, inspect the applicable repository
   instructions already supplied in the session context for a declaration
   written as `Quest root: <path>`. Never search for instruction files. Resolve
   an absolute declaration directly and a relative declaration from the
   directory containing the declaring instruction file. The most specific
   applicable declaration wins. Use it only when it resolves to an existing
   directory named `quests`.
3. If no applicable declaration exists and the current directory itself is named
   `quests`, use it. Otherwise, if `./quests` is an existing directory, use it.
4. If no candidate succeeds, stop and report the current-quest, declared-root,
   and `./quests` candidates checked. Do not create a `quests` directory merely
   to make root detection succeed, infer one from repository depth, or fall
   back to a fixed path.

Canonicalize the selected quest root to an absolute path and use it for every
quest read, write, and search in that operation.

```text
<quest-root>/
├── <quest-slug>/
│   └── README.md
└── .archived/
    └── <archived-quest-slug>/
        └── README.md
```

A slug must match `^[a-z0-9]+(?:-[a-z0-9]+)*$`. Reject paths and non-slug names.

`.archived` is reserved storage, not an active quest. Archiving is explicit and
does not imply that every goal, provider validation, or release gate is complete.
Use the archive reference for its safety gates and cleanup; do not simply move a
directory containing registered worktrees.

## Quest Record

Every quest is a workspace whose only required file is `README.md`, with `Brief`
and `Current State` as its only required sections. Do not create empty directories,
per-session reports, or workflow metadata merely for consistency.

Always read `README.md` first. Follow only the links needed for the current
request, active work, and exact next action. Before changing shared quest
material, reread the affected content and preserve unrelated updates.

Create new records with this minimal structure:

```markdown
# Quest Title

## Brief

## Current State

- Active work: One or more active tasks or activities, or none.
- Checkpoint: The latest durable progress or result.
- Next actions: The exact recommended resumption step for each active task, or the recommended next overall step.
- Blockers: None, or the unresolved blockers and approvals.
```

- `Brief` captures the initial request, relevant background, source links, stated
  constraints, and suggested approaches as provisional input to discovery, not an
  agreed specification. Keep it concise and link substantial existing material.
- `Current State` is the single durable handoff. Link to detail instead of
  duplicating it.

Additional sections and their ordering belong to the selected workflow or
capability, not this memory layer. A standalone capability may add the sections
it needs when recording its results without invoking `quest-master` or creating
the rest of its layout. When explicitly selected, `quest-master` supplies the
default workflow layout. Respect user-defined and coherent existing structures.

Keep sections concise. Put each checklist item in the section that currently
owns it; do not duplicate tasks or add `Tasks` subsections. An unchecked normal
task remains pending. Check it only after recording its outcome and appropriate
evidence. Add missing required headings during the next substantive quest update,
not merely because a quest was opened or listed. Do not invent content to populate
an empty section or remove or rearrange existing sections merely because they are
not required by this skill.

At creation, capture supplied context in `Brief` and initialize `Current State`
according to the new reference; do not add workflow sections during creation alone.
Suggestions in the brief are not accepted decisions or an approved task list.
Explicit user constraints and authorization boundaries still apply. Use discovery
and subsequent activities to establish content in its owning section, without
requiring the user to repeat clear answers already supplied in the brief.
Established goals and decisions govern ongoing work; the brief must not revive
rejected approaches or override later user direction. Apply the shared retention
test to it, removing misleading duplication or linking to the owning section as
understanding develops rather than maintaining an immutable request transcript.
Do not move established content in existing quests back into the brief merely to
adopt this structure.

## File Ownership And Stability

Organize retained material by purpose, following the selected capability's or
workflow's conventions. Index supporting files in their owning README section.
Respect user-requested locations, specialist conventions, and coherent existing
layouts; do not relocate material solely to enforce a default.

Separate distinct aspects that are independently useful or likely to change
independently. Prefer updating the file that already owns an
aspect over creating a file for each activity, worker, session, or status
change. An activity does not require a file merely because work occurred in it.

Keep volatile coordination state in README `Current State`. Supporting files
should be self-contained for their purpose through concise context and
references, not repeated goals, workspace details, live blockers, or next
actions. Keep a fact in one owning location; indexes and other files should
link rather than copy it. A required follow-up intrinsic to a finding belongs
with that finding, while the choice of what to do next belongs in Current State.

Create a supporting file when useful detail would obscure the README or when
the file is itself a requested deliverable. Prefer a reference to an existing
authoritative source over copying it. Retain local rationale, evidence, or
uncertainty when that source does not capture it or may not remain available.
Identify a version or observation time when needed to interpret evidence;
refresh live external state before relying on it for action.

Preserve stable context for selective loading and cache reuse. A routine
progress update should touch only records whose meaning changed. Do not embed
volatile status in otherwise stable knowledge or rewrite unrelated material
to make every file reflect the latest activity.

## Shared Update Contract

Before writing, identify what changed in the durable context needed to continue.
If nothing material changed, no quest update is necessary. Otherwise update its
owning record and only those indexes, tasks, links, or current instructions that
would become misleading. Update Current State when the active work, checkpoint,
next action, or blocker changes; do not repeat the outcome across artifacts to
demonstrate reconciliation.

Before substantive work, confirm the active task's intended outcome, boundaries,
authorization, dependencies, and expected evidence. Follow applicable project,
environment, safety, and domain instructions; preserve unrelated work; and use
the simplest approach that satisfies the current contract. Validate the result
proportionately. A failed or incomplete attempt may contain important evidence:
preserve observations needed to resume or avoid repeating the mistake, not an
exhaustive execution trace. Do not present attempted work as complete.

Keep the user oriented in the conversation as the work develops. At the outset
of substantive work, briefly state your current understanding, the next useful
step and why, and any consequential uncertainty. As evidence emerges, explain
material changes in understanding or direction and how they affect the work.
Scale updates to their significance and build on what the user already knows.
Make clear how you will check the result, refining that approach as needed.
Durable quest updates do not substitute for user-facing communication. These
updates do not introduce approval gates.

The record as a whole, including referenced authoritative sources, must let an
agent with no session history recover the context needed to continue:

- the current goal and active tasks;
- the meaningful checkpoint, not a history of every action;
- exact recommended next actions;
- blockers and required approvals;
- relevant files or workspaces; and
- the validation or evidence state and where to verify it.

Each individual artifact or update need not repeat this context. Retain commands,
identifiers, and operational details when needed for reproduction, interpretation,
or recovery, not as proof that routine work occurred. Reference standing policy
rather than repeatedly copying it; preserve quest-specific decisions or exceptions
when they materially constrain continuation.

Treat chat history, transient output, live processes, and session-local IDs as
non-durable. Replace obsolete checkpoints and next actions rather than stacking
new status snapshots above them. Correct false or misleading guidance and remove
resolved open questions.

When understanding changes, replace obsolete goals, choices, and plans, and
remove invalidated or irrelevant research. Reconcile affected supporting files,
tasks, and indexes as well as the README; a current summary does not compensate
for stale guidance in linked material. Remove obsolete content and files that
no longer have a retention purpose, repairing affected links. Do not retain a
document merely by labeling it superseded or moving it to an archive.

Keep the useful conclusion of a discarded approach, not its investigation and
planning trail. When it still prevents costly rediscovery or constrains current
choices, record a concise rejection and reason, for example: "Rejected A because
X; B because Y." Retain supporting detail only when it meets the shared retention
test or an explicit deliverable, provenance, or audit requirement.

Earlier-version evidence may remain valid without describing the current state.
Keep it only when it supports current decisions, validation, recovery, or an
explicit retention requirement; identify its scope and separate it from current
guidance. Do not rewrite old evidence to imply validation of a newer contract.

If a change invalidates a plan or decision but selecting its replacement is
unresolved or outside the authorized scope, remove the obsolete guidance and
state the gap and required next action explicitly. Do not invent a replacement
or leave stale instructions pending reconciliation. Preserve unrelated work;
if ownership or retention requirements are unclear, ask before deleting it.
Prefer targeted edits; rewrite a document only when targeted changes would leave
it incoherent. Do not use routine updates as a reason for unrelated reorganization.

Prefix a checklist item with `Approval:` only when an explicit user decision is
actually required by the user, applicable policy, or a consequential reserved
choice. Only explicit user authorization may check that item. When a result is
ready for approval, set `Blockers` to `Awaiting user approval` and make the next
action request acceptance or rejection. For older records without the prefix,
treat an unchecked result as an approval gate only when `Current State`
explicitly says it awaits approval, then add `Approval:` during the next
substantive update.

## Actionable Handoff

When opening a quest, reporting progress, completing substantive work, or
encountering a blocker, preserve one concrete recommended next action for each
active task, or the next overall action if work remains. If the agreed work is
complete or intentionally paused, record that without inventing a next task.
Derive next actions from the user's direction, the active capability, or an
explicitly selected workflow,
not from the order of README sections. If no next action is established,
recommend the smallest useful action supported by the current goal and evidence;
do not infer a lifecycle or expand authorization. Keep `Current State` aligned
with the recommendation and make unresolved decisions and blockers explicit.

## Optional Capabilities

Load only the capability needed for the current request. These are not required
stages and may be used in any order or more than once:

- `quest-goal` for clarifying desired outcomes, motivation, priorities, and scope;
- `quest-planning` for choosing an approach to achieve the goals and why it fits;
- `quest-partitioning` for turning a stable plan into executable tasks;
- `quest-acceptance-planning` for creating a durable acceptance contract;
- `quest-coding` for implementing coding tasks with proportionate repository,
  validation, commit, and worktree discipline;
- `quest-review` for risk-based independent assessment; and
- `quest-handoff` for reconciliation before reset, compaction, or transfer.

Specialized skills may be used instead of or alongside these capabilities. Do
not duplicate a specialist workflow inside the quest record.

`quest-master` is an opt-in guide for a default discovery-to-delivery
workflow. Do not load it merely because a quest is opened or updated; using
quest memory or an individual capability does not opt into orchestration.

## Commands

Before running a command, read only its dedicated reference:

- `open`, `open current`, or `open current quest`: [Open](references/open.md)
- `new`: [New](references/new.md)
- `list`: [List](references/list.md)
- `archive`, `archive current`, or `archive <slug>`: [Archive](references/archive.md)
- `install`: [Install](references/install.md)

When creating a quest, never replace an existing quest directory or file. Edit
existing quest material narrowly under the shared update contract.
