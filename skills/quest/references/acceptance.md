# Acceptance Planning

Turn an intended capability into a durable, understandable acceptance contract.
Keep scenario titles clear to a product reader while retaining enough detail for
implementation and verification.

## Scope

Apply quest resolution and the shared update contract. Read the quest README
first, then only the requirements, plan,
decisions, interfaces, and implementation constraints needed to design or revise
acceptance scenarios.

Do not implement the capability, execute formal QA, access production, or mark
scenarios passed unless the user separately requests and authorizes that work.

Save the acceptance contract at the requested quest-relative location or a
subject-focused location consistent with existing quest conventions. Make it
discoverable from the README; do not leave the only copy in conversation history.
Apply `quest`'s retention and file-ownership rules: the requested contract is a durable output,
not a reason to create an additional planning report.

## Gather Context

Read only the material needed to establish the acceptance boundary:

1. Applicable repository instructions and domain vocabulary.
2. The current goal, requirement, issue, plan, decision, or implementation
   brief.
3. Existing product behavior and interfaces that the capability will use or
   replace.
4. Relevant contracts, persistence boundaries, asynchronous effects, and
   existing tests.
5. Explicit exclusions, deferred behavior, release gates, and compatibility
   constraints.

Distinguish these sources clearly:

- current production behavior;
- prototype, fixture, or mock behavior;
- approved intended behavior;
- unresolved product decisions; and
- deliberately deferred behavior.

Do not turn a prototype assumption into an acceptance requirement merely
because an interface already displays it.

## Resolve Material Ambiguity

Before drafting final scenarios, identify decisions that change user-visible
behavior, authorization, privacy, durable data, external effects, or release
risk. When approved context cannot establish the answer, default to one concise
question at a time; group independent questions when that makes answering easier.

Explain concrete consequences rather than internal jargon. If the requested
interface depends on missing backend capability, say so and distinguish a
truthful incremental boundary from a misleading hybrid.

Do not invent an endpoint, domain distinction, compatibility policy, or product
rule solely to make the checklist appear complete.

## Write Scenarios

Give every scenario a stable ID and a user-facing title.

Titles should describe an outcome a product reader can understand, such as:

- `The selected people receive the saved request`
- `An edited recipient keeps the intended Contact identity`
- `The user can correct an error without losing their work`

Avoid titles that expose implementation mechanisms, such as:

- `Transaction rollback boundaries`
- `Mutation idempotency`
- `Projection conflict handling`

Default to Given/When/Then assertions under each title; retain an existing format
when it expresses equivalent observable conditions, actions, and outcomes.
Assertions may name technical evidence when essential to prove the outcome.
Keep each scenario focused on one coherent risk or journey.

Use these dimensions to identify relevant risks, not as a mandatory checklist:

- primary successful journeys;
- authorization and opaque denial;
- privacy and sensitive-data boundaries;
- durable state and the agreed atomic or independent-save boundaries;
- retries, duplicate actions, idempotency, and concurrency;
- asynchronous work and external-effect boundaries;
- validation, error recovery, and preservation of user work;
- loading, empty, disabled, and unavailable states;
- accessibility and responsive interaction;
- explicit exclusions and truthful absence of unsupported controls; and
- regression evidence for reused foundations.

Do not force every dimension into every capability. Prefer the smallest complete
set that proves the actual acceptance boundary. Do not choose an arbitrary
scenario count.

## Order By Importance

Make the full useful outcome the primary acceptance scenario, not an intermediate
save or successful response. Derive it from the requested contract; denial or
recovery can itself be the main job. Default coverage, manual QA, and reporting to:

1. The core happy path: the full useful outcome, including authoritative data
   display and the business rules needed to make that outcome correct.
2. Applicable resilience and safeguards: data integrity, agreed save boundaries,
   authorization, privacy, security, cross-scope isolation, duplicate effects,
   concurrency, and durable asynchronous or external-effect guarantees.
3. Diagnostics, error recovery, preservation of user work, secondary interface
   states, explicit exclusions, and lower-risk polish.

Prioritize supporting checks by impact, likelihood, recoverability, and evidence
needs, not implementation convenience. Explain departures for concrete risks or
dependencies; speculative edge cases must not displace the useful outcome.
Authorization, safe setup, cleanup, and required security and data-integrity
checks remain mandatory prerequisites for safe execution regardless of priority.

Where the approved contract permits independent success, include mixed-validity
cases proving useful results for valid records. Do not infer this contract from
implementation behavior or assume atomic writes suppress read-only diagnostics.

Plan evidence to distinguish the core outcome from supporting checks and a scoped
error-path contract from overall feature acceptance. An application defect is not
a missing test-data prerequisite. Report defects by severity and risk, allowing
serious defects to lead without obscuring the core outcome's status.

Automation uses this priority for coverage and reporting, not execution order;
keep tests independent and able to run in parallel or any order.

If grouping obscures priority, add a priority-ordered index; reference stable IDs,
not document position.

## Plan Proportionate Evidence

Select checks for their ability to change the acceptance decision, accounting for
setup, execution, debugging, artifact review, time and token cost. A longer test
list is not inherently stronger evidence.

- Identify the minimum core proof and mandatory project or release checks.
  Add supporting scenarios for likely consequential failures or concrete
  material risks. Rare timing, response loss, concurrent actions and exhaustive
  permutations need a reason tied to the change or an explicit requirement;
  credible severe or irreversible harm can justify testing even when unlikely.
- Cover distinct behavior and boundaries, not every equivalent combination.
  Select representative variants and explain exceptions only where they matter.
- Map each assertion to the least costly layer that reliably proves it. Reuse
  existing applicable evidence, recording version and scope limits. Browser QA
  should address user interaction or integration gaps, not repeat every lower-layer
  assertion. A complete contract does not require a full browser rerun per change.
- Distinguish required acceptance checks from conditional investigation. Give
  conditional checks a concrete trigger, such as an observed failure, changed
  persistence boundary, or unresolved material uncertainty. Do not make optional
  edge coverage a release blocker by listing it in the plan.
- Establish a stopping condition: the core outcome and required changed-risk
  boundaries have sufficient evidence, with no unresolved blocking defect.
  Do not add successive testing rounds after that point without new evidence.

Scale the plan to the task; avoid a separate budget, matrix or report when a few
scenarios and evidence pointers suffice. Respect user scope and spending limits.
If they conflict with an approved requirement or mandatory check, identify that
specific conflict rather than silently weakening the contract. Record explicit
deferrals or waivers in the owning contract, never as passing evidence.

## Assign Responsibility

Separate technical verification from product acceptance.

Use neutral workflow labels by default:

- **Implementation worker** owns implementation, automated tests, test data,
  local database inspection, and technical evidence.
- **Implementation worker, then Product owner** means technical evidence comes
  first, followed by manual acceptance of visible behavior, wording, and product
  judgment.

Inspect project vocabulary before naming actors or responsibilities. Do not
reuse a domain term as a workflow role when that would be ambiguous. For
example, if `Operator`, `Reviewer`, or `Agent` names a product user, do not also
use that word for the implementation worker.

Choose automation based on applicable requirements, material risk, and project
capabilities, especially for authorization, privacy, transactions, migrations,
concurrency, and durable work. Product judgment cannot substitute for required
technical evidence or automation. If capabilities cannot provide required proof,
record the gap and next action rather than silently replacing it with manual
acceptance. Do not assign implementation or database work to the Product owner
merely because the user asked for acceptance tests.

## Artifact Structure

Use the smallest structure that keeps the acceptance contract recoverable. For
substantial work, prefer:

```markdown
# <Capability> Acceptance Tests

## Contract Boundary And Approval

## Purpose

## Test Rules

## Execution Order And Responsibility

## Scenarios

### AT-01: <User-facing outcome>

**Given** ...
**When** ...
**Then** ...

## Required Evidence

## Deferred Scope
```

The required-evidence section should map proof to the layers that own it, such
as shared contracts, frontend behavior, backend decisions, persistence,
asynchronous processors, browser review, and regression checks. Do not prescribe
repository-specific commands until they have been read from the repository's
current command documentation.

Keep this contract stable while tests are executed. Put execution and assessment
results in their implementation or review records, referencing scenario IDs and
the contract version; do not repeatedly edit the contract to track runs or live
progress. Current readiness, blockers, and the selected next action belong in
README `Current State`. Update the contract itself when requirements or its
accepted boundary change.

## Approval And Durable State

Inherit explicit signoff requirements from the user and applicable workflow.
Check the recorded contract and linked decisions for approval
or a scoped waiver before setting status. When the user has explicitly waived signoff for
the contract's scope, label it `Signoff waived` and reference the owning waiver
record. Do not label it awaiting approval, mark it approved, or leave an
approval blocker in Current State. Preserve separate implementation, delivery,
and validation requirements; a waiver is not evidence that scenarios passed.

When signoff is required and outstanding, label the artifact as awaiting the
required approver's signoff. Preserve explicit approval of the current boundary;
when signoff is not required, state that drafting is in progress or complete
without introducing an approval gate. Do not infer approval or a waiver
from discussion, scenario ordering, or a request to save the file. A waiver
applies only to its recorded scope; do not extend it to materially changed
requirements without explicit user direction.

On completion, or after explicit approval when required:

1. Record the contract boundary and, when explicitly approved, the approval date.
2. Update the quest task and `Current State` with the next action when work
   remains, or record completion or intentional pause without inventing follow-up.
3. Respect applicable implementation, delivery, and assessment gates without
   copying standing policy into the acceptance contract.
4. Do not mark implementation or execution scenarios passed before evidence
   exists.

When requirements change, update the owning scenarios and references that would
otherwise mislead and remove obsolete scenario guidance. Retain concise rationale
or earlier-contract evidence only when it meets the shared retention test or an
explicit retention requirement, clearly scoped and separate from the current
contract; a superseded label alone does not justify retention. Do not rewrite old
evidence or carry an earlier approval forward as approval of changed requirements.
Where signoff is required, seek renewed approval or an explicit scoped waiver for
materially changed requirements.

## Quality Check

Before finishing, verify that:

- titles are understandable without implementation knowledge;
- scenario assertions are observable or tied to explicit technical evidence;
- coverage and priority follow the useful outcome and risk rules above, preserving
  mandatory safety prerequisites;
- responsibilities do not conflict with domain vocabulary;
- mock behavior is not presented as production truth;
- primary journeys are covered; supporting recovery and edge cases have an
  explicit requirement or concrete risk justification;
- evidence reuse, layer choice and stopping conditions keep effort proportionate;
- manual review does not replace required automation;
- the contract's drafting status and any required signoff are explicit, and
  Current State identifies the next action or completed/paused state; and
- the linked quest record and acceptance artifact describe the same current
  contract.
