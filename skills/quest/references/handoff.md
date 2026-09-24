# Handoff

Handoff is an optional reconciliation capability. Use it when context may be
lost or responsibility is changing, regardless of what kind of work the quest
contains or which activities happened most recently.

## Scope

Apply quest resolution and the shared update contract. A record that exists but
is stale, contradictory, or missing recent
decisions is not ready for handoff.

Do not perform unrelated research, planning, execution, or review merely to make
the record look complete. Surface genuinely unresolved work instead.

## Recoverability Audit

1. Read the README first, including Current State, any relevant Backlog items,
   and References; follow active checklist items and focused artifacts
   linked for checkpoints, decisions, evidence, blockers, and next actions.
2. Reconcile decisions and results since the last durable checkpoint under
   `quest`'s Shared Update Contract and file-ownership rules.
3. Search active material for approval gates, open questions, blockers, residual
   risks, superseded requirements, and contract terms affected by recent work.
4. Check that linked documents and references do not mislead or contradict the
   current contract; consult external authoritative state when needed.
5. Verify referenced files or workspaces and distinguish completed, attempted,
   in-flight, and unstarted work.
6. Confirm that the goal, checkpoint, blockers, approvals, and evidence state are
   recoverable without session history. Ensure each active task has one exact
   recommended resumption step selected from its first genuinely unresolved
   action, or record that the agreed work is complete or intentionally paused,
   including any agreed resume condition, without inventing a next task.

## Handoff Result

Apply the quest shared update contract, then report whether the quest is ready.
If it is ready, summarize the durable checkpoint, blockers, and recommended next
action or completed/paused state and any agreed resume condition without relying
on chat history. If it is not ready, identify the precise
record gap and the first action needed to close it. Do not declare readiness
while relevant state remains only in transient output or conversation context.

The handoff is the reconciled README and its references, not a new handoff file.
Do not manufacture an audit report or rewrite unaffected aspect files merely
because a session is ending.
