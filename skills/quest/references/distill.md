# Distill

Ensure information established by a quest is maintained where future project
work will look for it. Inspect, propose, then apply only the changes the user
approves. Scale the work to the changes and findings; a small quest may need one
documentation correction or no updates.

## Scope

Apply quest resolution and the shared update contract.
Read the README first, then relevant outcomes, decisions, review findings,
validation evidence, proposed changes, and the project documents that own the
affected information. Respect repository instructions and existing authorization.
Inspection and proposals are read-only. This approval boundary also covers quest
record updates made by this capability; include them in the proposals when needed
by the shared update contract.
Consolidation does not authorize opening or merging a PR, publishing, or changing
another repository or shared guidance outside the agreed scope.

## Checkpoints

- **Before opening a PR:** consolidate relevant documentation and established
  learnings into the proposed change so they can be reviewed with the implementation.
- **Before merging a PR:** reconcile changes and findings since the previous
  consolidation, including review decisions and validation results.
- **Before archival:** check for outstanding knowledge-transfer obligations and
  later findings. Resolve required gaps and record useful follow-ups before
  cleanup, including for quests without PRs.

At each checkpoint, an existing result that still covers the final proposed or
delivered state and relevant quest history needs only confirmation. If its coverage
is unclear, inspect the relevant scope again.

This activity may also be used during work or at a milestone. These checkpoints do
not require a PR for quests whose delivery takes another form.

## Inspect Quest Records And Implementation

Identify the repositories, branches, and worktrees associated with the quest from
its records and Git worktree listings. Inspect relevant implementation, tests,
configuration, and documentation, including committed changes and uncommitted or
untracked work. Use the appropriate base for each branch; do not assume that the
current checkout contains all quest work or that every registered worktree belongs
to the quest. Preserve unrelated work and do not switch, clean, or remove worktrees
to perform the inspection.

Compare what the quest records say with what was actually implemented and with
existing maintained project knowledge. Look for missing behavior documentation,
consequential rationale and constraints, operational knowledge, established
conventions, and documentation made inaccurate or redundant by the work. Identify
conflicts and distinguish intended, implemented, validated, merged, and released
states. If a relevant worktree or other source is unavailable, state the coverage
gap rather than claiming a complete inspection.

After inspecting current records and implementation, use the quest's own Git
history to find useful knowledge removed during current-state maintenance. Inspect
relevant changes since the previously recorded history-coverage commit; on a first
pass or without a usable coverage reference, scan relevant history for candidates.
Use targeted diffs and earlier file versions to investigate removed findings,
rejected approaches, corrected assumptions, or resolved operational issues when
they could prevent rediscovery or explain current choices. Scale the search to the
quest and likely value; do not reconstruct every intermediate state. Treat history
as evidence of earlier understanding, not current authority: validate candidates
against current records, implementation, and maintained sources before proposing
changes under the approval rules below. If history is unavailable or incomplete,
state the limit and proceed with available evidence.

## Propose Durable Changes

1. Identify information that would materially improve future decisions, prevent
   costly rediscovery, or explain current behavior. Compare the quest's findings
   with the actual proposed or delivered state and existing maintained sources.
   Do not promote tentative observations or one-off workarounds into standing rules.
2. Identify the source that should own each aspect. Typical destinations include:
   - user documentation for behavior, configuration, and usage;
   - architecture documents or ADRs for consequential constraints and rationale;
   - runbooks and contributor documentation for operations and troubleshooting;
   - project instructions for established project-specific conventions;
   - existing skills or shared guidance for techniques with demonstrated broader
     applicability, within the authorized scope; and
   - existing project work tracking for unfinished obligations.
3. Prefer targeted updates to existing documents. Propose a new document only when
   the knowledge needs its own maintained home, not to produce a retrospective
   or per-quest learnings file. Write current behavior, requirements, and rationale
   that stand on their own; retain uncertainty and evidence scope when material.
   Distinguish proposed or implemented behavior from released behavior and checks
   that actually ran from validation still pending.
4. Present independently approvable proposals with stable IDs. For each, give:
   - the operation (edit, add, move, or delete) and exact repository/worktree and
     file path, including the destination for a move;
   - the knowledge to preserve or the inaccurate/redundant material to remove,
     with its evidence source and why the project needs the change;
   - the proposed wording or a focused diff, with enough detail to approve the
     substance; for deletion, explain where any useful knowledge is retained; and
   - dependencies such as link repairs or companion updates that must be approved
     together to keep the result coherent.
   Ask which proposals the user approves, rejects, or wants revised, then wait.
   Requesting distillation, reaching a checkpoint, or approving the implementation is
   not approval of these proposals. If no changes are warranted, report the
   inspected scope and conclusion without manufacturing proposals.

## Apply Approved Proposals

1. Apply only explicitly approved proposals. Accept approval of individual items
   or a clearly identified group; leave rejected or unanswered proposals unapplied.
   Reread affected files before editing and preserve unrelated changes. If new
   evidence or intervening edits require a material change to an approved proposal,
   present the revised proposal for approval before applying it. Include required
   companion edits in approval rather than silently expanding an approved item.
2. Include project-local updates in the same PR where appropriate. Identify a
   scoped update or durable follow-up for knowledge owned elsewhere. Distinguish
   documentation required for correctness, operation, or an explicit delivery
   obligation from useful follow-up knowledge transfer. If a required update
   cannot be completed, surface the exact gap and required next action; obtain
   an explicit deferral decision before proceeding past the checkpoint, subject
   to applicable requirements. Useful follow-ups may be recorded within existing
   authorization without blocking the checkpoint or requiring a deferral approval;
   writing those follow-ups still requires approval of the proposed file changes.
   Record outstanding work in the project's existing tracking location when
   available and authorized, otherwise in the quest, with appropriate links.
   Do not mark deferred work complete or expand scope to update another repository.
3. Verify accuracy against the implementation and evidence, check affected links
   and examples, and run proportionate checks plus required repository commands.
   Pre-merge file changes must be included in the PR and receive the applicable
   validation and review before merge. Follow [Coding](coding.md)'s commit rules
   when applicable; consolidation does not bypass delivery checks.
4. Before archival, verify that incorporated knowledge survives checkout cleanup.
   A recovery backup preserves work but does not incorporate it into maintained
   docs; updates only in a removable checkout remain unresolved under the
   required-gap versus useful-follow-up distinction above. Follow the
   [archive preservation and authorization rules](archive.md).

## Record The Result

Include any needed durable result in the proposals and write it only after
approval. Keep one concise result with the relevant subject in an existing record,
or in Current State when brief. Make supporting detail discoverable from the README.
Record implementation coverage using a PR, commit, or other concrete state
reference, and quest-history coverage using the inspected quest commit and relevant
scope. Use a commit that already exists when inspected, not the later commit that
records this result. Note unavailable history or coverage references rather than
implying full coverage. Include links to maintained destinations, validation limits,
and any deferred obligations. A documented
"Reviewed; no project updates needed" is valid when inspection supports it.
Update this result as coverage changes rather than accumulating checkpoint logs.

Apply `quest`'s shared update contract: keep live blockers and next actions in
Current State, and link authoritative knowledge rather than duplicating it.
Report what was incorporated, what remains unapproved or deferred, and whether
any coverage gaps remain. Do not claim the checkpoint is satisfied merely because
a result was recorded.
