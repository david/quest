---
name: quest
description: Opens, creates, lists, and maintains context quests stored at a project-relative quest root. Uses each quest README as a living state record and index. Use when the user invokes the quest skill or asks to work with a quest.
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

Before starting substantive quest work, reuse a matching existing task or add one concise unchecked task to the relevant section; never duplicate it merely to record activity. Point `Current State` at that task and record the intended next action before advancing it. During the work, keep the task, handoff, and linked artifacts current. When the work finishes, add a short result or artifact link but leave the checkbox unchecked. Record the completed checkpoint and user approval as the next action. An unchecked task with a result or outcome link awaits user approval; an unchecked task without one remains pending. Only the user can authorize changing `- [ ]` to `- [x]`. Agents, delegated workers, implementers, reviewers, and supervisors must never infer that approval or check a task on their own.

`Current State`, the section checklists, and linked artifacts form the state record. Checked tasks show user-approved past work. Unchecked tasks with results show work awaiting approval. Unchecked tasks without results show present or future work.

Create all stable headings for new quests. For an existing quest, add missing headings during the next substantive quest-material update, not as a side effect of `open` or `list`. Do not invent content merely to populate an empty section. Preserve useful unrelated organization while converging the README on this structure.

## Session-Resettable State

Keep every active quest session-resettable at each turn boundary. The README and the focused artifacts it links must let an agent with no conversation or session history recover the current goal, active task, latest completed or attempted work, exact next action, blockers or required approvals, relevant files or worktrees, and validation state.

Before ending any turn that starts, advances, delegates, blocks, or fails substantive quest work, checkpoint the task, `Current State`, and relevant artifacts. Persist useful tool and worker results before the final response. Treat chat history, transient tool output, live process state, and session-local identifiers as non-durable context rather than the sole record of progress. Maintain the checkpoint during the work instead of deferring every update until the final response.

`open` and `list` may remain read-only because they do not advance quest work. When access limits or stronger instructions prevent a required checkpoint, stop at the last durable checkpoint and report that the quest was not advanced.

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

Before executing a command, read its dedicated reference. Do not load unrelated command references unless the request requires more than one command.

- `open`, `open current`, or `open current quest`: [Open](references/open.md)
- `new`: [New](references/new.md)
- `list`: [List](references/list.md)

When creating a quest, never replace an existing quest directory or file. Edit existing quest material narrowly under the update rules above.
