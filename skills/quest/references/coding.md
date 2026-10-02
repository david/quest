# Implementation

Use this guide for authorized source-code or configuration changes within a quest.
Read the governing task, plan, decisions, and expected evidence. Planning and task
breakdown are not prerequisites for one clear bounded task.

For delegated work, the coordinator establishes scope, dependencies, ownership,
and completion evidence. Workers inspect applicable project instructions and
implementation context; the coordinator need not duplicate those reads.

Resolve ambiguities that materially change intended behavior or the approach
before deciding them in code. When `refactor-planning` supplies a preservation
contract, implement and migrate tests against the assigned entries. Report evidence
for the changed production boundary and relevant connections or variants. Old-path
or isolated-component passes do not prove integration preservation, and unverified
entries remain incomplete.

## Repository Preflight

Before choosing the execution layout:

1. Inspect repository status and current branch.
2. If the execution worktree has pre-existing tracked or untracked changes, stop
   before editing and report the dirty paths. Do not stash, clean, discard,
   commit, or move them, or create another worktree merely to bypass the blocker.
   Resume after the user or owning worker leaves the execution worktree clean.
3. Before implementation, rebase the execution branch onto the project's current
   primary branch unless it already contains that branch's tip. Identify the
   primary branch from project instructions or the authoritative remote's default
   branch, not an assumed `main`. Fetch that remote first. Resolve ambiguity or
   rebase failure before continuing, for any selected or newly created execution
   branch.
4. Identify shared files, generated outputs, dependency state, migrations, caches,
   ports, services, and other resources that can make concurrent work interfere.

The clean-state gate concerns changes present before this task begins. Changes
made by the authorized task belong to its execution and commit sequence.

## Worktree Layout And Coordination

Use the current compatible worktree by default for one bounded task. Use a separate
branch and worktree when it materially isolates independent parallel work,
interfering operations, or work requiring separate integration.

Prefer sequential execution when tasks share files or an evolving contract, or
one result must shape another. Separate directories do not make overlapping
changes independent. For parallel implementation, use
[parallel coordination](parallel-coordination.md) before dispatching workers.
Shared quest records remain coordinator-owned.

## Commits And Integration

Stage only task-owned files, never broad unrelated paths. Each coder must commit
all intentional task changes immediately after completion and successful
validation, before starting another task or handing work off. Report the commit
hash and validation result. Preserve an incomplete implementation in a separate
commit clearly labeled incomplete; do not create empty commits for unchanged work.

These rules concern implementation repositories. The snapshot plugin owns
quest-record snapshots. Workers report implementation commits and evidence;
the coordinator reconciles quest records.

Preserve task commits during integration. Do not squash, reset, or otherwise
rewrite them beyond the required primary-branch rebase unless the user explicitly
requests history cleanup. Resolve conflicts against the current contract and
rerun affected validation after integration. If requested review leads to fixes,
use dedicated follow-up commits rather than amending the reviewed implementation.

## Documentation And Delivery

Keep documentation needed for correctness or operation accurate as part of the
authorized change. Use [knowledge transfer](distill.md) for explicitly requested
consolidation or material findings that need a maintained home; PR creation and
merge alone do not require a separate distillation exercise or approval round.
Respect explicit project checkpoints and user-reserved approvals. This guide does
not authorize opening, pushing, or merging a PR beyond the existing request.

## Completion Evidence

Retain task outcomes, changed behavior, material deviations, validation limits,
and evidence needed to reproduce or interpret results. Link code, commits, and
check results instead of copying their history. Distinguish implementation
validation from integration, delivery, and acceptance; check tasks only when their
completion is evidenced.

For failed or unavailable checks, distinguish change-related failures from
unrelated or unavailable validation and preserve the exact recovery action.
Keep workspace and integration status, live blockers, and next actions in Current
State when needed for continuation. Do not create a report per commit or worker.
