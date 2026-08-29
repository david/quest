---
name: quest
description: Opens, creates, lists, and maintains context quest records stored at a project-relative quest root. Defines their README structure, state semantics, recoverability invariant, and update rules. Use for quest record operations; use quest-master to advance substantive quest work through delegated workers.
---

<!-- argument-hint: <open|new|list> [slug] -->

# Quest

Resolve the quest root and any current quest context once per operation from the session's current working directory, never from the skill directory:

1. First inspect the current working directory and its ancestors for a canonical quest directory. A candidate must have a slug basename, contain `README.md`, and have a parent named `quests`. When a match exists, it is the current quest and its parent is the quest root. Run this check before testing `./quests` so nested workspace content cannot be mistaken for the quest root.
2. If the session is not inside a quest and `./quests` is an existing directory, the current working directory is the project support directory; use `./quests`.
3. Otherwise, run `git rev-parse --show-toplevel` to locate the enclosing worktree root. From that root—not from the possibly nested current directory—resolve `../../quests` and use it only if it is an existing directory.
4. If no candidate succeeds, stop and report the candidates checked. Do not create a `quests` directory merely to make root detection succeed, and do not fall back to a fixed path.

Canonicalize the selected quest root to an absolute path and use it for every quest read, write, and search in that operation.

```text
<quest-root>/
└── <quest-slug>/
    └── README.md
```

Every quest is a free-form workspace. Its only required file is `README.md`. Beyond the stable README sections defined below, add files and directories only when the work calls for them; do not impose metadata, statuses, naming schemes, or an internal directory structure.

Always read `README.md` first. Use its links to select only the files relevant to the current request. Do not read every linked file by default; expand incrementally only when needed.

A slug must match `^[a-z0-9]+(?:-[a-z0-9]+)*$`. Reject paths and non-slug names.

## README.md

Treat the README as the quest's lean task record and artifact index. Use these stable sections in this order:

```markdown
# Quest Title

## Goals

- [ ] A desired outcome.

## Current State

- Active task: A task from a section below, or none.
- Checkpoint: The latest durable progress or result.
- Next action: The exact resumption step.
- Blockers: None, or the unresolved blockers and approvals.

## Research

## Decisions

## Implementation

## Review

## Backlog
```

- `Goals` is an unchecked checklist of desired outcomes. Use concise supporting text for scope boundaries when needed.
- `Current State` is the single durable handoff. It names the active checklist task or says that none is active, records the latest checkpoint, gives the exact next action, and identifies blockers or approvals. Link to relevant artifacts, affected worktrees, and validation evidence instead of duplicating their detail.
- `Research` indexes evidence, findings, uncertainties, open questions, and research tasks.
- `Decisions` indexes accepted choices, rationale, superseded choices, and unresolved decision tasks.
- `Implementation` indexes implementation plans, outcomes, and implementation tasks.
- `Review` indexes independent verification, findings, and review tasks.
- `Backlog` holds deferred or not-yet-classified work and stays last because it can grow large.

Keep each section concise and link to focused artifacts for detail. Use a direct checklist in the relevant section rather than adding `Tasks` subsections or duplicating tasks across sections. Move a task when its classification changes. Use `Backlog` only when a task is deferred or does not yet belong to another section.

Keep `Current State`, the section checklists, and linked artifacts consistent; together they form the state record. An unchecked task without a result remains pending. An unchecked task with a result or outcome link awaits user approval. A checked task records user-approved past work. Only the user can authorize changing `- [ ]` to `- [x]`; agents must never infer that approval or check a task on their own.

Create all stable headings for new quests. For an existing quest, add missing headings during the next substantive quest-material update, not as a side effect of `open` or `list`. Do not invent content merely to populate an empty section. Preserve useful unrelated organization while converging the README on this structure.

## Recoverability Invariant

After every quest-material update, the README and the focused artifacts it links must let an agent with no conversation or session history recover the current goal, active task, latest completed or attempted work, exact next action, blockers or required approvals, relevant files or worktrees, and validation state.

This invariant defines a valid quest record regardless of which workflow updates it. Treat chat history, transient tool output, live process state, and session-local identifiers as non-durable context rather than the sole record of progress.

### Reset-Readiness Audit

When the user asks whether a quest or session is ready for reset, handoff, compaction, or a new session, complete this audit before declaring readiness:

1. Reread `Current State`, the active task, and the focused artifacts linked for its checkpoint, next action, blockers, decisions, plan, and validation evidence.
2. Reconcile every explicit user decision and useful worker or tool result produced since the last durable checkpoint.
3. Search the active artifacts for approval gates, open questions, blockers, residual risks, superseded requirements, and named contract terms affected by recent decisions. Remove or reclassify resolved items everywhere they appear.
4. Confirm that `Current State`, section checklists, decision artifacts, active plans, blocker records, and embedded acceptance or residual-risk summaries describe one consistent current contract.
5. Confirm that `Next action` names the first genuinely unresolved step and that referenced worktree state, changed files, validation results, and in-flight work are accurate.

A record that is durable but stale, contradictory, or missing a recent decision is not reset-ready. Reconcile it before reporting readiness.

## Updating Quest Material

When an operation changes or attempts to change a quest's goals, findings, plans, implementation, review evidence, backlog, or linked artifacts, reconcile the relevant README sections, task item, and `Current State` before finishing.

Keep current guidance clear without discarding useful evidence. When findings or decisions change existing quest material, prefer a new focused artifact plus the smallest reconciliation edits needed in existing indexes, statuses, and summaries. Do not create a new file merely to avoid correcting a contradiction elsewhere.

Classify affected material before editing it:

- Correct or remove factually false statements and obsolete instructions.
- Replace superseded requirements with the current contract. Preserve the old requirement only when its rejection or evolution remains useful, and label it explicitly in past tense under a heading such as `Original concern`, `Investigated and rejected`, `Superseded requirement`, or `Historical evidence`.
- Preserve observations, test results, failed approaches, and decision rationale that may prevent repeated work.
- Mark resolved questions as resolved or remove them from open-question lists. Remove questions made irrelevant unless explaining why they became irrelevant has continuing value.
- Do not preserve untested speculation merely for historical completeness.

Never leave current and superseded guidance contradictory or unlabeled. When a decision resolves part of a challenge or risk, normally create or update the focused decision artifact, update the parent index status, and make a targeted status or wording change in the affected document while leaving unrelated investigation material intact.

Rewrite a whole document only when most of it is invalid, its structure obscures the current state, or targeted edits would leave it incoherent. Before rewriting, account for every useful fact, observation, result, rationale, and remaining question so the rewrite does not silently lose information.

## Commands

Use [Quest Master](../quest-master/SKILL.md) when a request advances substantive quest work through exploration, research, analysis, implementation, testing, or review.

Before executing a command, read its dedicated reference. Do not load unrelated command references unless the request requires more than one command.

- `open`, `open current`, or `open current quest`: [Open](references/open.md)
- `new`: [New](references/new.md)
- `list`: [List](references/list.md)

When creating a quest, never replace an existing quest directory or file. Edit existing quest material narrowly under the update rules above.
