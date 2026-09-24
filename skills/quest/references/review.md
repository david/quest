# Review

Review is an optional, risk-based capability. Routine author checks and direct
validation are useful evidence but are not independent review.

## Scope

Apply quest resolution and the shared update contract. Read the quest README
first, then the artifact or outcome under review,
its governing requirements, and its recorded validation evidence.

Begin formal review only when its scope and review target are sufficiently
stable. The reviewer must be independent of the producer when the review is
described as independent or when applicable policy requires separation. Do not
approve user-reserved decisions, rewrite the work under review, or expand into
unrequested implementation.

## Review Against The Contract

Establish the review basis before judging the work:

- intended outcome and explicit scope;
- accepted requirements and decisions;
- relevant risks and failure modes;
- expected evidence or validation; and
- known exclusions and residual uncertainty.

Prioritize findings by consequence and actionability. Distinguish blocking
defects, material risks, minor improvements, and questions caused by missing
evidence. Cite the exact artifact, behavior, or contract involved. Do not invent
requirements or treat stylistic preference as a defect.

For a plan, assess executability, dependencies, validation, unresolved decisions,
and risk coverage. For a work breakdown, assess task boundaries, dependencies,
ordering, validation evidence, and coverage of the plan. For completed work,
assess conformance, evidence quality, regressions, safety, and residual risk.
Use a specialist review or testing skill when it better matches the subject.

## Record The Result

Apply `quest`'s retention and file-ownership rules. Retain the assessment with
the relevant subject or in a linked focused record when detail warrants it or a
report is a requested deliverable. Review scope/version, independence when
relevant, conclusion, actionable findings, and material evidence limits must be
recoverable from the README and its links without duplication. Reference
existing evidence rather than repeating execution logs.

Keep required remedies with their findings and the selected next action in
`Current State`. Review completion does not approve a result on the user's behalf.
Apply the shared update contract as work advances: identify the reviewed version
without implying coverage of newer work, correct inaccurate findings, and link
relevant resolution evidence.
