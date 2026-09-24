# Master

Use this reference when the user selects `quest master` or asks for delegated
investigation or subagent coordination within a quest. Apply quest resolution,
durable memory, and the shared update contract. Read other activity references
as needed for the user's task.
This reference governs subagent delegation and coordination while selected,
including work performed through those capabilities; it does not impose a
workflow or authorize additional tasks.

## Worker Coordination

Use the task's prerequisites, dependencies, and overlap constraints to decide
which authorized assignments can proceed independently. Prefer sequential work
when tasks overlap substantially or depend on an evolving shared contract. Do
not subdivide work merely to create more assignments or parallelism.

Give each worker a clear outcome, necessary context, authorized scope, and
completion evidence. Establish ownership of shared files and resources before
dispatching concurrent work. For implementation workers, read [Coding](coding.md) for
concrete branches, worktrees, and implementation-specific coordination.

Collect worker results and resolve conflicting findings or overlapping changes
before treating dependent work as ready. Check the returned evidence against the
assignment's completion criteria; an incomplete or blocked result remains open.
The main agent synthesizes outcomes and maintains durable quest context under
the `quest` shared update contract.

## Investigation Delegation

When the work needs code exploration, repository scouting, or web research,
dispatch a subagent for that investigation to preserve the main agent's context.
Examples include tracing behavior and dependencies, locating relevant tests or
documentation owners, investigating failures or conflicting claims, and checking
external capabilities or version-specific contracts. Routine bounded reads of
known files, quest records, and existing evidence stay with the main agent.

Give each investigator the factual question, necessary context, authorized scope,
and a stopping condition. Keep investigation read-only and request concise
findings with file/line references or authoritative URLs, relevant versions or
observation times, and unresolved uncertainty rather than raw search output.
Parallelize independent questions when useful; avoid duplicating the worker's
investigation in the main context. Inspect targeted source evidence when needed
to resolve uncertainty or support a consequential decision.

The main agent owns user discussion, synthesis, decisions, and durable quest
updates. Delegation does not expand the task's authorization or satisfy an
independent-review requirement by itself. Retain useful findings under the `quest`
shared update contract; do not create a record merely because a worker ran.
If subagents are unavailable, state that limitation and keep direct investigation
narrowly scoped.
