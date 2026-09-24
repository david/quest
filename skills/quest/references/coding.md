# Coding

Use this capability to implement coding tasks while preserving the quest's
durable contract and the repository's existing work. Coding may follow planning
and partitioning, but neither is a mandatory ceremony for one clear bounded task.

## Scope

Apply quest resolution and the shared update contract. Read the quest README
first. Read the active implementation task,
accepted plan, and decisions when those records are present, then only the
project files needed for the change.

Confirm the task's outcome, scope, dependencies, ownership, authorization, and
expected validation evidence. If implementation exposes an ambiguity that
materially changes the intended behavior or approach, seek the necessary
clarification or revise the affected plan before proceeding rather than silently
deciding it in code. A separate planning phase is not required for a clear,
bounded task.

Use implementation workers when useful within the authorized task scope, following
the ownership and coordination requirements below. Do not perform formal
independent review of your own implementation; author checks and automated tests
are implementation validation.

## Inspect Repository State

At task preflight, before choosing an execution layout:

1. Inspect repository status and current branch.
2. If the execution worktree contains any pre-existing tracked or untracked
   changes, stop before editing and report the dirty paths. Do not stash, clean,
   discard, commit, or move those changes, and do not create another worktree merely to
   bypass the blocker. Resume only after the user or owning worker leaves the
   execution worktree clean.
3. Before implementation, rebase the execution branch onto the project's current
   primary branch unless it already contains that branch's tip. Identify the
   primary branch from project instructions or the authoritative remote's default
   branch rather than assuming `main`; fetch that remote before rebasing. Resolve
   any ambiguity or rebase failure before continuing. Apply this requirement to
   any execution branch selected or created for the task.
4. Confirm whether tasks touch shared files, generated outputs, dependency state,
   migrations, build caches, ports, services, or other resources that can make
   concurrent work interfere.

This clean-state gate concerns changes present before the task begins. Changes
made by the authorized task after a clean preflight belong to its execution and
commit sequence.

## Choose A Worktree Layout

Use the current worktree by default for one bounded task when its state is
compatible with the work.

Recommend or create a separate branch and worktree when it provides material
isolation, such as when:

- explicitly authorized tasks can be developed and validated independently in
  parallel;
- dependency operations, generated files, migrations, or validation commands
  could interfere with another task; or
- the task needs an independent branch for later review or integration.

Do not create extra worktrees merely because multiple tasks exist. Prefer
sequential work when tasks modify the same files, share an evolving contract,
or one result must shape another. Separate worktrees reduce state interference;
they do not make conceptually overlapping changes independent or remove merge
risk.

For parallel implementation work, use
[parallel coordination](parallel-coordination.md) to establish
ownership, serialize shared operations, and assign integration responsibility
before workers begin. Shared quest records remain coordinator-owned; workers
return outcomes and evidence to the coordinator.

## Commit And Integrate

Never stage broad unrelated paths. Stage only files owned by the task.

Each coder must commit all intentional task changes immediately after the task
is complete and its validation has passed, before starting another task or
handing work off. Report the commit hash and validation result. If a coder ends
with an incomplete implementation that must be preserved, commit it separately
and label its incomplete status clearly. A coder that produced no changes
reports that fact instead of creating an empty commit.

These commit rules concern implementation repositories. The snapshot plugin owns
quest-record snapshots under `quest`'s Versioned Checkpoints rules. In parallel
work, workers report evidence and implementation commit hashes; the coordinator
reconciles shared quest records.

Address review findings in dedicated follow-up commits after the original
implementation commit. Never amend an implementation commit to incorporate
review fixes. Preserve implementation and review-fix commits during integration;
do not squash, reset, or otherwise rewrite them beyond the required
primary-branch rebase unless the user explicitly requests history cleanup after
review. Resolve integration conflicts against the current
contract and rerun affected validation after integration.

## PR Checkpoints

Before opening a PR, read [Distill](distill.md) to incorporate relevant project
documentation and durable learnings into the proposed change. Before merging,
use it again to reconcile changes and findings since the previous consolidation.
Include any resulting edits in the PR and complete applicable validation and
review before merging. A prior result may satisfy the checkpoint when verified
to cover the current proposed state. These checks do not authorize opening,
pushing, or merging a PR beyond the user's existing authorization.

## Record The Result

Apply `quest`'s retention and file-ownership rules. Update the owning task
with its outcome and evidence reference; keep current
workspace, integration status, blockers, and next action in `Current State` only
when needed for continuation. Check the task only after completion is evidenced.

Use a linked subject-focused record only when useful detail needs it, not for
each commit or worker. Preserve changed behavior, material deviations, validation
limits, and identifiers or commands needed to interpret or reproduce the result.
For failed or unavailable checks, preserve the evidence needed to resume and
distinguish change-related failures from unrelated or unavailable validation.
Link existing code, commits, or check results instead of copying their history.
Do not rewrite stable implementation evidence on each push or status change.

Distinguish author validation, independent assessment, and delivery evidence
without requiring separate files for each activity. Keep new findings and
decisions with the relevant subject and reference them rather than duplicating
them or building an activity log.
