# Parallel Coordination

Use this reference when coordinating parallel implementation workers within the
authorized task scope. When delegated coordination is selected, load the
`quest-master` skill and follow its Investigation Delegation rule for read-only
investigation.
Worktree isolation does not expand task authorization or bypass the clean
execution-worktree preflight in [Coding](coding.md).

When workers share one worktree, require non-overlapping file ownership and
non-interfering commands. Serialize operations on the Git index, commits,
dependency state, generated outputs, and shared services. Coordinate clean
preflights and task boundaries so one worker's uncommitted changes do not block
another worker's start; use sequential execution or suitable isolation when
these requirements cannot be met.

When using separate worktrees, record each task's branch, worktree, ownership,
dependencies, and integration destination before work begins. Check for shared
resources outside the worktrees, including caches, ports, and services; separate
directories alone do not prevent interference.

Keep one coordinator responsible for reconciling shared quest material and
integrating parallel results. Workers return outcomes, validation evidence,
commit hashes, and remaining blockers rather than editing coordinator-owned
quest records concurrently. The coordinator maintains useful current records;
the snapshot plugin preserves eligible changes under `quest`'s Versioned
Checkpoints rules, including partial or concurrent-writer state.
Preserve implementation and review-fix commits and rerun affected validation as
required by Coding's commit and integration rules.
