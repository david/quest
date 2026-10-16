# Knowledge Transfer

Use this guide for requested consolidation or retrospectives, or when material
quest findings need a maintained home in the realm. Ordinary documentation
corrections belong with the authorized work. PR creation, merge, and archival
do not by themselves require a separate consolidation exercise.

## Identify Useful Knowledge

Read relevant outcomes, decisions, findings, evidence, and maintained sources.
Inspect implementation when needed to establish accuracy. Do not assume the current
checkout contains every quest change or that every worktree belongs to the quest.
Distinguish intended, implemented, validated, merged, and released states; report
unavailable sources and coverage limits.

Preserve information that will improve future decisions, prevent costly
rediscovery, or explain current behavior. Useful destinations include the
realm's [lore](lore.md), user docs, architecture records, runbooks, contributor
guidance, and existing project work tracking. Prefer a targeted update to the existing owner over a per-quest
learnings document. Do not turn tentative findings or one-off workarounds into
standing rules.

Current records are the starting point. Inspect targeted quest-history diffs only
when there is reason to expect useful knowledge was removed during current-state
maintenance, or the user requests a retrospective that needs history. Validate
earlier findings against current evidence; history is not current authority.
Do not scan the entire history merely to complete a checkpoint.

## Apply Changes Within Authorization

Apply in-scope documentation and record updates under existing authorization.
Write current behavior, requirements, and rationale that stand on their own.
Keep uncertainty and evidence limits where material, and repair affected links.

Propose changes and wait for approval when they alter shared instructions or
policy, extend into another repository or otherwise exceed authorization, or
concern a user-reserved decision. Explain the destination, proposed substance,
evidence, and reason; include companion edits needed for coherence. A request for
consolidation does not authorize publication or an unrelated change to shared
guidance. Respect any explicitly requested inspect-and-propose-only mode.

Reread affected files before editing and preserve unrelated work. Verify accuracy,
links, and examples, and run proportionate checks plus required repository commands.
Follow the repository's own instructions for its changes and
commits. Include pre-merge documentation changes in the PR when applicable;
do not bypass delivery checks or publication permissions.

## Preserve Obligations And Report The Result

Distinguish required documentation or operational gaps from useful follow-up
knowledge transfer. Required gaps must be resolved or explicitly deferred where
permitted before the boundary that needs them. Useful follow-ups do not block
delivery or archival by default. Use existing work tracking, or the quest when
no authorized realm destination is available, without marking deferred work
complete.

Before checkout cleanup, verify transferred knowledge survives outside removable
checkouts. A backup preserves work but does not incorporate it into maintained
realm material. Follow [archive safety rules](archive.md) for cleanup.

Keep one concise result with links to maintained destinations and any outstanding
obligations. Identify inspected versions or history scope when needed to interpret
coverage; do not accumulate checkpoint logs. No updates is a valid result when
the inspected scope supports it. Keep live blockers and next actions in Current
State under the shared update contract.
