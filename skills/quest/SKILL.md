---
name: quest
description: Provides lightweight shared context for sessions working inside context quests and opens, creates, lists, and maintains quest records stored at a project-relative quest root. Use when a session needs to research, plan, implement, test, review, or update work within a quest.
---

<!-- argument-hint: <open|new|list> [slug] -->

# Quest

Resolve the quest root and any current quest context once per operation from the session's current working directory, never from the skill directory:

1. First inspect the current working directory and its ancestors for a canonical quest directory. A candidate must have a slug basename, contain `README.md`, and have a parent named `quests`. When a match exists, it is the current quest and its parent is the quest root. Run this check before considering any configured root so a quest opened directly remains self-identifying.
2. If the session is not inside a quest, inspect the applicable repository instructions already supplied in the session context for a declaration written as `Quest root: <path>`. Never search for instruction files. Resolve an absolute declaration directly and a relative declaration from the directory containing the declaring instruction file. The most specific applicable declaration wins. Use it only when it resolves to an existing directory named `quests`.
3. If no applicable declaration exists and `./quests` is an existing directory, use it.
4. If no candidate succeeds, stop and report the current-quest, declared-root, and `./quests` candidates checked. Do not create a `quests` directory merely to make root detection succeed, infer one from repository depth, or fall back to a fixed path.

Canonicalize the selected quest root to an absolute path and use it for every quest read, write, and search in that operation.

```text
<quest-root>/
└── <quest-slug>/
    └── README.md
```

Every quest is a free-form workspace. Its only required file is `README.md`. Beyond the stable README sections defined below, add files and directories only when the work calls for them; do not impose metadata, statuses, naming schemes, or an internal directory structure.

Always read `README.md` first. Use its links to select only the files relevant to the current request. Do not read every linked file by default; expand incrementally only when needed.

## Working in a Quest

A quest supplies shared context and a durable coordination record. It does not assign the session a fixed role or restrict the session to quest-material edits. Perform the requested research, planning, implementation, testing, review, or other project work directly. Explore and modify project files, run commands, and delegate to subagents when the task calls for them.

Read linked quest artifacts only when the current task, evidence, or next action requires them. Before changing shared quest material, reread the affected content and preserve unrelated updates. Record durable findings, results, blockers, and the exact next action under the update rules before finishing substantive work.

A slug must match `^[a-z0-9]+(?:-[a-z0-9]+)*$`. Reject paths and non-slug names.

## README.md

Treat the README as the quest's lean task record and artifact index. Use these stable sections in this order:

```markdown
# Quest Title

## Goals

- [ ] A desired outcome.

## Current State

- Active work: One or more tasks from the sections below, or none.
- Checkpoint: The latest durable progress or result.
- Next actions: The exact resumption step for each active task, or the next overall step.
- Blockers: None, or the unresolved blockers and approvals.

## Research

## Decisions

## Plan

## Implementation

## Review

## Backlog
```

- `Goals` is a checklist of desired outcomes. Use concise supporting text for scope boundaries when needed.
- `Current State` is the single durable handoff. It names the active checklist tasks or says that none are active, records the latest checkpoint, gives the exact next action for each active task, and identifies blockers or approvals. Link to relevant artifacts, affected worktrees, and validation evidence instead of duplicating their detail.
- `Research` indexes evidence, findings, uncertainties, open questions, and research tasks.
- `Decisions` indexes accepted choices, rationale, superseded choices, and unresolved decision tasks.
- `Plan` indexes implementation strategy, task decomposition, dependencies, parallelizable work streams, implementation validation, and detailed plan artifacts. Keep formal review tasks under `Review`. Submit a plan for formal review only after the user says it is ready, then obtain explicit user approval of the reviewed plan before implementation begins.
- `Implementation` indexes executable implementation tasks and their outcomes. Keep each task independently assignable and verifiable where practical, and identify dependencies when tasks cannot run in parallel.
- `Review` indexes formal independent verification of plans and implementations, along with its findings and tasks. Begin plan review only after the user says the plan is ready. Review completion does not approve the plan on the user's behalf. Begin implementation review only after the implementation tasks in its scope are complete and their validation evidence is recorded. Assign every review task to an independent agent that did not produce the work being reviewed; self-checks and automated tests are validation, not review.
- `Backlog` holds deferred or not-yet-classified work and stays last because it can grow large.

Keep each section concise and link to focused artifacts for detail. Use a direct checklist in the relevant section rather than adding `Tasks` subsections or duplicating tasks across sections. Move a task when its classification changes. Use `Backlog` only when a task is deferred or does not yet belong to another section.

Keep `Current State`, the section checklists, and linked artifacts consistent; together they form the state record. An unchecked task remains pending. An agent may check a normal task after completing it and recording its outcome and validation evidence. Prefix a checklist item with `Approval:` only when an explicit user decision is required. Require approval for a reviewed implementation plan and for choices or consequential actions that the user explicitly reserves; do not require it for research, implementation, validation, review, documentation, or administrative completion. For example: `- [ ] Approval: Accept [implementation plan](plan.md)`. Only explicit user authorization permits changing an `Approval:` item from `- [ ]` to `- [x]`. When an approval item has a result ready for decision, set `Current State`'s blockers to `Awaiting user approval` and make a next action request the user's acceptance or rejection; never rely on the result link alone to convey the gate. In existing quest material written before the `Approval:` convention, preserve an unchecked result as an approval gate only when `Current State` explicitly identifies it as awaiting approval, and add the prefix during the next substantive update.

Create all stable headings for new quests. For an existing quest, add missing headings during the next substantive quest-material update, not as a side effect of `open` or `list`. Do not invent content merely to populate an empty section. Preserve useful unrelated organization while converging the README on this structure.

## Recoverability Invariant

After every quest-material update, the README and the focused artifacts it links must let an agent with no conversation or session history recover the current goal, active tasks, latest completed or attempted work, exact next actions, blockers or required approvals, relevant files or worktrees, and validation state.

This invariant defines a valid quest record regardless of which workflow updates it. Treat chat history, transient tool output, live process state, and session-local identifiers as non-durable context rather than the sole record of progress.

### Reset-Readiness Audit

When the user asks whether a quest or session is ready for reset, handoff, compaction, or a new session, complete this audit before declaring readiness:

1. Reread `Current State`, the active tasks, and the focused artifacts linked for their checkpoint, next actions, blockers, decisions, plan, and validation evidence.
2. Reconcile every explicit user decision and useful worker or tool result produced since the last durable checkpoint.
3. Search the active artifacts for approval gates, open questions, blockers, residual risks, superseded requirements, and named contract terms affected by recent decisions. Remove or reclassify resolved items everywhere they appear.
4. Confirm that `Current State`, section checklists, decision artifacts, active plans, blocker records, and embedded acceptance or residual-risk summaries describe one consistent current contract.
5. Confirm that each next action names the first genuinely unresolved step for its task and that referenced worktree state, changed files, validation results, and in-flight work are accurate.

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

Perform substantive quest work in the current session. Use subagents when delegation adds value rather than as a requirement.

Before executing a quest record command, read its dedicated reference. Do not load unrelated command references unless the request requires more than one command.

- `open`, `open current`, or `open current quest`: [Open](references/open.md)
- `new`: [New](references/new.md)
- `list`: [List](references/list.md)

When creating a quest, never replace an existing quest directory or file. Edit existing quest material narrowly under the update rules above.
