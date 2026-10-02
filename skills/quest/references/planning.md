# Planning And Task Breakdown

Use this guide to choose an approach, revise a plan, or break established work
into executable tasks. Scale detail to uncertainty and risk. A small, clear task
does not need separate planning or breakdown artifacts.

Read the goal, relevant evidence, accepted decisions, and constraints. Use
[goal clarification](goals.md) only when material outcome or scope questions remain.
A planning-only request does not authorize execution; a broader execution request
may continue into implementation once the work is ready.

## Choose An Approach

Keep the intended outcome, chosen approach, rationale, and success evidence clear.
Include material assumptions, dependencies, exclusions, risks, recovery needs,
and unresolved decisions. Omit empty categories and unnecessary detail.

Use specialist guidance for substantive design questions:

- `refactor-planning`: behavior-preserving changes to execution paths,
  responsibilities, or component and process boundaries.
- `event-modeling`: domain events, producing commands, and decision boundaries.
- `read-modeling`: consumer-facing outputs, sources, derivations, and freshness.
- [Acceptance integration](acceptance.md): concrete acceptance scenarios and proof.

Keep specialist contracts in the subject's existing plan rather than duplicating
them. Present current and proposed behavior in enough concrete detail for the user
to assess the tradeoffs. A representative user action, flow, or diagram can help;
avoid front-loading every algorithm or field.

Resolve choices that materially affect behavior, data integrity, authorization,
compatibility, or cross-task interfaces before dependent work starts. Leave local
implementation details to the implementer. Do not hide unresolved design in a task
called "finalize contracts." Independently specified work need not wait for an
unrelated decision.

Request approval only for user-reserved or policy-reserved decisions. Discussion
does not create an approval gate. Retain accepted choices and useful rejection
reasons with their subject, replacing obsolete guidance under the shared update
contract.

## Define Executable Tasks When Useful

Skip a separate breakdown when the work is already one clear task. Otherwise,
choose the smallest coherent set of independently verifiable tasks. Each needs:

- its outcome and scope;
- relevant inputs and governing contracts;
- prerequisites and dependencies; and
- completion evidence.

Make shared files, resources, evolving interfaces, and outputs needed by other
tasks explicit. Sequence coupled work; do not create more tasks merely to enable
parallelism. Use [implementation guidance](coding.md) when execution is authorized.

Keep a small checklist in Current State, or link a task record when detail warrants
it. Maintain one owning specification per task or shared interface. Link the plan
rather than copying it. Keep required remedies or follow-ups with their subject
and deferred tasks in Backlog or their existing owner.

A breakdown preserves the approach. If it exposes a material unresolved choice,
resolve that choice and mark dependent tasks blocked. Do not execute or mark tasks
complete merely because the breakdown is finished.

## Keep The Result Recoverable

Store brief plans in Current State and substantial plans in linked subject-focused
records. Keep rationale, assumptions, decisions, and success evidence with the plan;
keep live progress, blockers, and the next action in Current State. Update plans
when their approach changes, not merely because implementation advances.

Continue authorized work when ready. When a planning-only request is complete,
report the result and any useful next action without inventing follow-up work.
