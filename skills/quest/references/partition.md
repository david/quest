# Task Breakdown

Turn an established plan into the smallest coherent set of executable,
verifiable tasks. Use this reference for standalone breakdown requests or from
`quest-master`; it does not opt the user into orchestration or authorize execution.

Use `quest` to resolve the workspace and establish its shared update contract.
Read the README first, then the relevant plan, accepted decisions, constraints,
and expected evidence. Skip a separate breakdown when the work is already one
clear executable task.

Create the task checklist under `Implementation`. Each task should identify its
outcome, scope, relevant inputs, prerequisites, and completion evidence. Make
blockers and outputs needed by other tasks explicit.

Make ordering and safe concurrency explicit. Prefer sequential execution when
tasks overlap substantially or depend on an evolving shared contract. Do not
subdivide work merely to create more assignments or parallelism. Keep substantial
specifications in `implementation/`, with one owning specification per task or
shared interface, and link the plan rather than duplicating it. Update task
specifications when scope or dependencies change, not for routine status updates.
For parallel coding work, identify ownership and isolation constraints; let
`quest-coding` choose concrete branches and worktrees.

Partitioning preserves the established approach. Return material unresolved
decisions to planning and mark dependent tasks as blocked. Keep `Current State`
aligned with the first unblocked task or exact prerequisite, respecting any
applicable authorization and acceptance-signoff requirements. Do not execute or
mark the resulting tasks complete merely because the breakdown is finished.
