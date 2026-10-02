# Sync

Bring the current quest's durable record up to date with the conversation and
available evidence. Accept `sync quest`, or `sync` when the context clearly
refers to quest state. Use the recoverability check below for `handoff`, reset,
transfer, pause, or an explicit audit of whether another agent can resume.

Resolve the quest using the skill's root-resolution rules and the active quest
context. Ask which quest to use only when the target is not clear. Read its
`QUEST.md` first, then apply the shared update contract to material changes,
including affected supporting records and `Current State`. If nothing material
changed, no edit is needed.

## Recoverability Check

Handoff is a thorough reconciliation, not a separate deliverable. Check the
active scope without performing unrelated work merely to make records look complete:

- Read Current State and relevant linked goals, decisions, tasks, and evidence.
  Reconcile material results and decisions still present only in conversation.
- Check active material for unresolved questions, approval gates, blockers, residual
  risks, and requirements affected by recent work. Repair stale or contradictory
  guidance under the shared update contract.
- Verify relevant linked files and workspaces. Consult live authoritative state
  only when needed. Distinguish completed, attempted, in-flight, and unstarted work.
- Confirm that an agent without session history can recover the goal, constraints,
  checkpoint, evidence limits, blockers, and exact resumption action for each active
  task. Record completion or intentional pause and any agreed resume condition
  without inventing another task.

Report the durable checkpoint and whether the records are ready for resumption.
If not, identify the precise gap and first action needed to close it. Do not claim
readiness while relevant state remains only in chat or transient output. The
handoff is `QUEST.md` and its references, not a new handoff file or routine audit
report. Leave unaffected supporting records alone.

The snapshot plugin preserves eligible changes under the skill's Versioned
Checkpoints rules. Sync maintains records; it does not imply remote synchronization
or continuing the quest's next task.
