---
name: quest
description: >
  Open, create, list, archive, and maintain durable quest records for work that spans
  sessions or needs a recoverable handoff. Use for quest workspace discovery,
  current-state reconciliation, project installation, lifecycle commands, task
  breakdown, and routing work to an optional quest capability skill.
---

<!-- argument-hint: <install|open|new|list|sync|archive> [path|slug] -->

# Quest

Use quests as lightweight shared context, not as a mandatory project process.
A quest may involve any kind of work, and its activities need not follow a
linear sequence. This skill is the durable memory layer: it does not select or
enforce a workflow.

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

Every quest is a workspace whose only required record is `README.md`, with
`Current State` as its only required section. Do not create empty directories,
per-session reports, or workflow metadata merely for consistency.

Always read `README.md` first. Follow only the links needed for the current
request, active work, and exact next action. Before changing shared quest
material, reread the affected content and preserve unrelated updates.

Create new records with this minimal structure:

```markdown
# Quest Title

## Current State

- Objective: The current desired outcome and what would count as success.
- Constraints: Material scope and authorization boundaries, or links to them.
- Active work: One or more active tasks or activities, or none.
- Checkpoint: The latest durable progress or result.
- Next actions: The exact recommended resumption step for each active task, or the recommended next overall step.
- Blockers: None, or the unresolved blockers and approvals.
```

The README is a resumption interface, not a workflow outline:

- `Current State` is the single durable handoff. Include the current objective,
  material constraints, and context needed to act correctly, not just recent
  progress. Link to detail instead of duplicating it. The fields above are a
  starting point; use concise prose or bullets suited to the work.
- Add `Backlog` when useful for pending or deferred work outside the immediate
  next actions. Preserve enough context to pick it up; link an existing task
  record rather than maintaining a second checklist.
- Add `References` when useful as an annotated index of supporting material and
  authoritative sources, including designs, decisions, research, acceptance
  contracts, evidence, and deliverables. State why each link matters.

Capabilities prescribe information to preserve, not README headings or directory
names. Organize detail around the subject matter. A small quest may fit entirely
in Current State; larger work may use linked records. Respect user-defined and
coherent existing structures; do not rearrange them merely to adopt this layout.

Keep each task in one owning location. An unchecked normal task remains pending.
Check it only after recording its outcome and appropriate evidence. Add a missing
Current State during the next substantive update, not merely because a quest was
opened or listed. Do not create empty headings for completeness.

At creation, capture supplied context and initialize Current State according to
[New](references/new.md). Distinguish clear user intent and explicit constraints
from proposed goals, approaches, or tasks. Suggestions are not accepted decisions
or an approved task list. Build on supplied answers without requiring repetition.
As understanding develops, replace provisional or obsolete context with current
goals and decisions rather than maintaining an immutable request transcript.

## File Ownership And Stability

Organize retained material by subject and purpose. Make supporting material
discoverable from the README, using References for an index when useful and
direct links from Current State for the active work.
Respect user-requested locations, specialist conventions, and coherent existing
layouts; do not relocate material solely to enforce a default.

Keep related context together: a design may include its problem, research,
alternatives, accepted choices, and rationale. Separate aspects when they are
independently useful or likely to change independently, not merely because they
arose during different workflow activities. Prefer updating the file that already
owns an aspect over creating a file for each activity, worker, session, or status change.

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

## Versioned Checkpoints

Each quest owns a Git repository rooted at its quest directory. Current files
describe the understanding an agent should act on; Git history preserves earlier
states for recovery and comparison. Normal resumption must not require reading
history. Keep rationale that still matters in the current records under the
shared retention test.

Quest storage must be outside existing Git repositories, including project
checkouts and worktrees; ignoring the storage in an enclosing repository does
not satisfy this requirement. Before creating a quest or initializing an existing
one, verify that its canonical parent location is outside any Git repository.
If it is inside one, report the conflict and request an external quest root;
do not create the quest or silently relocate existing records. Implementation
checkouts may live inside a quest under the configured workspace layout.

On creation, initialize the repository and commit the initial quest records after
setup. For an existing quest without its own repository, initialize and commit a
baseline of its existing records before the first substantive update. Opening or
listing a quest alone does not require initialization. Check the actual repository
root; Git discovering an ancestor repository does not establish quest ownership.

Maintain a quest-local `.gitignore` excluding `/work/`, `/local-data/`, other
implementation checkouts, caches, temporary output, and private configuration.
Track maintained quest records and suitable durable evidence. Inspect existing
files before the baseline; preserve them in place while excluding material that
does not belong in quest history. Do not add nested repositories as gitlinks.

After each coherent durable update, commit its affected records, including
additions and deletions. Reconcile supporting documents and Current State before
committing so one checkpoint captures a consistent result, rather than committing
each file write. Use a concise message describing the durable change; do not
create empty commits. These local quest-record commits are part of maintaining
the quest and do not authorize implementation commits or remote publication.

Inspect status and the staged diff, stage explicit paths, and preserve unrelated
or unfinished edits. With concurrent agents, the coordinating agent owns commits;
workers report their changes for a coherent checkpoint. Do not include another
writer's unfinished work. If a commit is blocked, preserve the files and report
the missing checkpoint and required recovery action; do not claim it succeeded.
Use existing Git identity and signing settings rather than inventing or changing
them to bypass a failure.

Archive the quest with its `.git` directory intact. The quest-record repository
is retained memory, not an implementation checkout subject to removal or merge
verification.

## Shared Update Contract

Before writing, identify what changed in the durable context needed to continue.
If nothing material changed, no quest update is necessary. Otherwise update its
owning record and only those indexes, tasks, links, or current instructions that
would become misleading. Update Current State when the active work, checkpoint,
next action, or blocker changes; do not repeat the outcome across artifacts to
demonstrate reconciliation. This preserves stable context for selective loading
and cache reuse.

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

Retain commands, identifiers, and operational details when needed for reproduction, interpretation,
or recovery, not as proof that routine work occurred. Reference standing policy
rather than repeatedly copying it; preserve quest-specific decisions or exceptions
when they materially constrain continuation.

Treat chat history, transient output, live processes, and session-local IDs as
non-durable. Replace obsolete checkpoints and next actions rather than stacking
new status snapshots above them. When understanding changes, replace obsolete
goals, choices, and plans, correct misleading guidance, and remove resolved
questions or invalidated research. Apply this to affected supporting files,
tasks, and indexes as well as the README; a current summary does not compensate
for stale linked guidance. Remove content and files that fail the shared retention
test, repairing affected links; labeling them superseded or archiving them is not
a retention purpose.

Keep the useful conclusion of a discarded approach, not its investigation and
planning trail. When it still prevents costly rediscovery or constrains current
choices, record a concise rejection and reason, for example: "Rejected A because
X; B because Y." Apply the shared retention test to supporting detail.

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

At a handoff, blocker, or material change in direction, make the next useful action
explicit to the user when work remains, including during capability-specific
conversations. Briefly explain why it follows from the current state; do not leave
the recommendation only in the quest record. During ongoing work, a focused
question or announced action is sufficient; avoid repeating an already-clear next
step. Continue authorized work rather than stopping at a recommendation; request
a decision only when one is needed. When the agreed work is complete or
intentionally paused, say so without inventing a follow-up.

`Current State` and its linked records or authoritative sources must let an agent
without session history recover the current goal and active tasks, meaningful
checkpoint, next actions, blockers and approvals, relevant files or workspaces,
and the validation or evidence state and where to verify it. Individual artifacts
need not repeat this context.

When opening a quest, reporting progress, completing substantive work, or
encountering a blocker, preserve one concrete recommended next action for each
active task, or the next overall action if work remains. If the agreed work is
complete or intentionally paused, record that without inventing a next task.
Derive next actions from the user's direction, the active capability, or an
explicitly selected workflow, not from the order of README sections.
If work remains but no next action is established,
recommend the smallest useful action supported by the current goal and evidence;
do not infer a lifecycle or expand authorization. Keep `Current State` aligned
with the recommendation and make unresolved decisions and blockers explicit.

## Optional Capabilities

Load only the capability needed for the current request. These are not required
stages and may be used in any order or more than once:

- `quest-goal` for clarifying desired outcomes, motivation, priorities, and scope;
- `quest-planning` for choosing an approach to achieve the goals and why it fits;
- `quest-acceptance-planning` for creating a durable acceptance contract;
- `quest-coding` for implementing coding tasks with proportionate repository,
  validation, commit, and worktree discipline;
- `quest-review` for risk-based independent assessment;
- `quest-distill` for incorporating durable outcomes into maintained project
  documentation and guidance before PR creation, merge, or archival as needed; and
- `quest-handoff` for reconciliation before reset, compaction, or transfer.

Specialized skills may be used instead of or alongside these capabilities. Do
not duplicate a specialist workflow inside the quest record.

For a request to turn an established plan into executable tasks, use
[Task Breakdown](references/partition.md). A breakdown request alone does not
authorize task execution.

## Commands

Before running a command, read only its dedicated reference:

- `open`, `open current`, or `open current quest`: [Open](references/open.md)
- `new`: [New](references/new.md)
- `list`: [List](references/list.md)
- `sync quest`, or `sync` when the context clearly refers to quest state: [Sync](references/sync.md)
- `archive`, `archive current`, or `archive <slug>`: [Archive](references/archive.md)
- `install`: [Install](references/install.md)

When creating a quest, never replace an existing quest directory or file. Edit
existing quest material narrowly under the shared update contract.
