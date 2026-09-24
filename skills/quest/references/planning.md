# Planning

Planning is an optional capability, not a gate every quest must pass. It
chooses an approach to achieve the goals and explains why it fits. Match the
plan's detail to the uncertainty and risk of the work.

## Scope

Apply quest resolution and the shared update contract. Read the quest README
first and follow only links needed to understand
the goal, current evidence, accepted decisions, and active constraints.

When the desired outcomes, beneficiaries, motivation, or scope are materially
unclear or disputed, read [Goals](goals.md) to establish shared understanding rather
than hiding those choices in a plan. Goal discovery is not a prerequisite when
the existing goals are already clear enough to plan against.

Do not conduct unrelated research, execute the plan, or approve decisions on the
user's behalf. Use a specialist planning skill when the domain calls for one;
index its result in the quest instead of duplicating it.

Choose the specialist by the design question:

- Use `event-modeling` for domain events, their producing commands, and decision
  boundaries, or an explicitly requested Event Modeling exercise.
- Use `read-modeling` for a consumer-facing output contract, its sources,
  derivations, and freshness.

Within quest planning, specialist results define the approach and contracts.
Execution task breakdown is a separate activity using
[Task Breakdown](partition.md).

## Establish The Plan

Always cover the intended outcome, chosen approach, and success evidence. Cover
the following where material to the plan, omitting empty categories:

- the intended outcome and explicit boundaries;
- current facts, assumptions, and unresolved decisions;
- the chosen approach and why it fits the constraints;
- expected artifacts, changed behavior, or other observable result;
- evidence that would demonstrate success;
- major dependencies that materially shape the approach; and
- material risks, recovery needs, exclusions, and blockers.

Do not partition the plan into execution tasks, assign ownership, or prescribe
a detailed task schedule. Include strategic sequencing constraints when they
shape the approach, such as migrating readers before removing an interface.
Recommend task breakdown after the outcome and approach are sufficiently stable
when the work needs more than one executable task. A small plan that is already
one clear task may proceed without partitioning.

Before recommending partitioning or implementation, distinguish resolved
contracts, ordinary implementation details, and material unresolved decisions.
Keep unresolved design work in the plan rather than deferring it through an
implementation task named "finalize contracts" or "close design." This does not
require exhaustive upfront design: local coding choices can remain with the
implementer. Choices that materially affect behavior, data integrity,
authorization, compatibility, or cross-task interfaces must be resolved before
the dependent work is ready. Independently specified work need not wait for
unrelated planning gaps.

## Present The Design

Present a compact, coherent view of the consequential structures and contracts
affected by the active scope so the user can assess their parts and relationships
together. Match the representation to the work: a user flow, interface, component
interaction, data model, document structure, or concise description of behavior.
Include concrete detail needed to evaluate the proposal, using a specialist
planning skill for domain-specific representations.

When work changes a system's architecture, explain the relevant current structure
and proposed changes in plain, concrete language. Describe what the affected
parts do, how they interact, what changes, and why. Ground the explanation in a
representative request or user action when useful. Explain consequential
tradeoffs and unresolved choices, introducing technical terms only when they
help and making their meaning clear. Use a diagram when it improves understanding.

Avoid front-loading algorithms or long field-by-field explanations. Let the user
choose where to challenge or explore the design in depth, connect each drill-down
to the overall approach, and integrate feedback into the whole proposal. Keep
the explanation current as the approach evolves, and communicate material
revisions to the user. Design discussion follows the decision and approval rules
below; it does not introduce a separate approval gate.

## Decisions And Approval

Presenting a technical detail for review does not by itself reserve that decision
to the user. Distinguish agreed behavioral and compatibility contracts from
implementation details that may be refined during execution.

Record current accepted choices and their rationale with the relevant subject, replacing
obsolete choices. Keep concise rejection reasons when they still inform current
work or prevent costly rediscovery, not superseded decision documents or planning
trails merely for history. Reconcile affected plans and tasks under the shared
update contract. Keep unresolved choices explicit and explain the consequence
of delaying them; do not invent a replacement decision.

Request formal review only when the user, applicable policy, or material risk
warrants it. Request user approval only when the user or applicable policy
reserves the decision. A reviewed plan is not approved on the user's behalf.
Use the quest `Approval:` convention for a real approval gate. When further work
is appropriate, recommend the remaining decision, partitioning, or executable
work according to readiness. If the planning request is complete, report that
without inventing follow-up work. Completing or reviewing a plan does not itself
authorize execution.

## Record The Result

Apply `quest`'s retention and file-ownership rules. Retain the approach and why it
fits in Current State for small work, or a linked subject-focused record when
detail warrants it. Keep rationale, assumptions, unresolved design choices, and
success criteria with the plan; reference existing accepted decisions instead of
duplicating them. Create files for independently useful aspects, not each session.

Keep readiness blockers and the selected next action in Current State. When work
breakdown is needed, recommend partitioning. Keep execution tracking and formal
assessment evidence distinguishable from the intended approach, linking their
owning records when separate. Update a plan when its approach or assumptions
change, not merely because implementation progresses.
