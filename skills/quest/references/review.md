# Review Integration

Use this guide when the user explicitly requests a quest assessment, including
review of a plan, task breakdown, partial output, or completed functionality.
Progress, PR creation, or test results do not automatically request review.
If policy requires review beyond the active request, surface it and ask for direction.

Read the requested artifact or outcome, governing requirements, and available
validation evidence. Read the shared
[review policy](../../code-review/references/review-policy.md) for independence,
priorities, gates, and follow-up behavior, reusing it when already in context.
Review stays read-only unless changes are separately authorized. Do not approve
user-reserved decisions or expand into implementation.

## Assess The Requested Scope

Establish intended outcomes, accepted requirements, exclusions, relevant risks,
and expected evidence. Cite the exact artifact, behavior, or contract involved.
Distinguish defects, material risks, improvements, and evidence gaps; do not invent
requirements or treat stylistic preferences as defects.

- For a plan, assess whether its approach is executable, dependencies and material
  decisions are clear, and validation covers the intended outcome and risks.
- For a breakdown, assess task boundaries, dependencies, and coverage of the plan.
- For code or configuration, load `code-review`. Supply the exact diff, commit,
  or PR target, relevant requirements and exclusions, existing evidence, and any
  required independence or integration boundary. Use its findings and coverage
  limits rather than conducting a duplicate generic review.
- For completed functionality, assess the whole accepted quest contract, including
  conformance, evidence quality, safety, and residual uncertainty.

Production code and passing tests are not prerequisites for assessing partial
work. State missing evidence without implying it passed. A code review with no
findings is not proof that the whole goal was delivered or accepted. Author checks
and failure investigation are not independent review.

## Retain Findings And Their Consequences

Keep the reviewed version, conclusion, actionable findings, material evidence
limits, and independence when relevant recoverable from the owning record and
`QUEST.md`. Use a separate report only when useful detail or a requested deliverable
needs one. Workers return evidence; the coordinator owns shared quest updates.

Keep remedies with their findings and live blockers or next actions in Current
State. Reconcile proposed gates against the actual contract and shared review
policy, distinguishing dependent-work, integration, and release boundaries.
Deferred findings need owners and tracking destinations.

When fixes are authorized, follow [implementation guidance](coding.md) and keep
dedicated follow-up commits. Follow-up review requires authorization; a fix does
not request another review by itself. Identify the corrected version and its
evidence without implying an earlier assessment covers newer work.
