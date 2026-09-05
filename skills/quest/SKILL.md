---
name: quest
description: >
  Open, create, list, and maintain durable quest records for work that spans
  sessions or needs a recoverable handoff. Use for quest workspace discovery,
  current-state reconciliation, lifecycle commands, and routing work to an
  optional quest capability skill.
---

<!-- argument-hint: <open|new|list> [slug] -->

# Quest

Use quests as lightweight shared context, not as a mandatory project process.
A quest may involve any kind of work, and its activities need not follow a
linear sequence. This skill is the durable memory layer: it does not select or
enforce a workflow. Users, individual capabilities, or an explicitly selected
orchestrator may direct the work independently.

## Resolve The Quest

Resolve the quest root and any current quest context once per operation from
the session's current working directory, never from the skill directory:

1. First inspect the current working directory and its ancestors for a
   canonical quest directory. A candidate must have a slug basename, contain
   `README.md`, and have a parent named `quests`. When a match exists, it is the
   current quest and its parent is the quest root. Run this check before
   considering any configured root so a quest opened directly remains
   self-identifying.
2. If the session is not inside a quest, inspect the applicable repository
   instructions already supplied in the session context for a declaration
   written as `Quest root: <path>`. Never search for instruction files. Resolve
   an absolute declaration directly and a relative declaration from the
   directory containing the declaring instruction file. The most specific
   applicable declaration wins. Use it only when it resolves to an existing
   directory named `quests`.
3. If no applicable declaration exists and `./quests` is an existing directory,
   use it.
4. If no candidate succeeds, stop and report the current-quest, declared-root,
   and `./quests` candidates checked. Do not create a `quests` directory merely
   to make root detection succeed, infer one from repository depth, or fall
   back to a fixed path.

Canonicalize the selected quest root to an absolute path and use it for every
quest read, write, and search in that operation.

```text
<quest-root>/
└── <quest-slug>/
    └── README.md
```

A slug must match `^[a-z0-9]+(?:-[a-z0-9]+)*$`. Reject paths and non-slug names.

## Quest Record

Every quest is a free-form workspace. Its only required file is `README.md`.
Do not impose metadata, statuses, naming schemes, or an internal directory
structure beyond the stable README sections below.

Always read `README.md` first. Follow only the links needed for the current
request, active work, and exact next action. Before changing shared quest
material, reread the affected content and preserve unrelated updates.

Use these stable sections in order:

```markdown
# Quest Title

## Goals

- [ ] A desired outcome.

## Current State

- Active work: One or more tasks from the sections below, or none.
- Checkpoint: The latest durable progress or result.
- Next actions: The exact recommended resumption step for each active task, or the recommended next overall step.
- Blockers: None, or the unresolved blockers and approvals.

## Research

## Decisions

## Plan

## Implementation

## Review

## Backlog
```

- `Goals` is a checklist of desired outcomes and concise scope boundaries.
- `Current State` is the single durable handoff. Link to detail instead of
  duplicating it.
- `Research` and `Decisions` index evidence and accepted choices.
- `Plan` indexes the intended strategy, boundaries, risks, and plan artifacts.
- `Implementation` holds executable task checklists and their outcomes.
- `Review` indexes assessment tasks, evidence, findings, and resolutions.
- `Backlog` holds deferred or not-yet-classified work and stays last.

Keep sections concise. Put each checklist item in the section that currently
owns it; do not duplicate tasks or add `Tasks` subsections. An unchecked normal
task remains pending. Check it only after recording its outcome and appropriate
evidence. Add missing stable headings during the next substantive quest update,
not merely because a quest was opened or listed. Do not invent content to
populate an empty section.

## Shared Update Contract

When work changes or attempts to change a quest's goals, findings, decisions,
plans, implementation, review evidence, backlog, or linked artifacts, reconcile
the affected section, checklist item, links, and `Current State` before
finishing.

Before substantive work, confirm the active task's intended outcome, boundaries,
authorization, dependencies, and expected evidence. Follow applicable project,
environment, safety, and domain instructions; preserve unrelated work; and use
the simplest approach that satisfies the current contract. Validate the result
proportionately. A failed or incomplete attempt is still a result: preserve
useful observations, state what remains, and do not present attempted work as
complete.

After every quest-material update, the README and focused artifacts it links
must let an agent with no session history recover:

- the current goal and active tasks;
- the latest completed or attempted work;
- exact recommended next actions;
- blockers and required approvals;
- relevant files or workspaces; and
- the validation or evidence state.

Treat chat history, transient output, live processes, and session-local IDs as
non-durable. Correct false or obsolete guidance, label useful historical or
superseded material clearly, preserve evidence that may prevent repeated work,
and remove resolved or irrelevant open questions. Never leave current and
superseded guidance contradictory or unlabeled. Prefer targeted edits; rewrite
a document only when targeted changes would leave it incoherent.

Prefix a checklist item with `Approval:` only when an explicit user decision is
actually required by the user, applicable policy, or a consequential reserved
choice. Only explicit user authorization may check that item. When a result is
ready for approval, set `Blockers` to `Awaiting user approval` and make the next
action request acceptance or rejection. For older records without the prefix,
treat an unchecked result as an approval gate only when `Current State`
explicitly says it awaits approval, then add `Approval:` during the next
substantive update.

## Actionable Handoff

When opening a quest, reporting progress, completing substantive work, or
encountering a blocker, preserve one concrete recommended next action for each
active task, or the next overall action if work remains. If the agreed work is
complete or intentionally paused, record that without inventing a next task.
Derive next actions from the user's direction, the active capability, or an
explicitly selected workflow,
not from the order of README sections. If no next action is established,
recommend the smallest useful action supported by the current goal and evidence;
do not infer a lifecycle or expand authorization. Keep `Current State` aligned
with the recommendation and make unresolved decisions and blockers explicit.

## Optional Capabilities

Load only the capability needed for the current request. These are not required
stages and may be used in any order or more than once:

- `quest-goal` for clarifying desired outcomes, motivation, priorities, and scope;
- `quest-research` for evidence, investigation, and open questions;
- `quest-planning` for choosing an approach to achieve the goals and why it fits;
- `quest-partitioning` for turning a stable plan into executable tasks;
- `quest-acceptance-planning` for creating a durable acceptance contract;
- `quest-coding` for implementing coding tasks with proportionate repository,
  validation, commit, and worktree discipline;
- `quest-review` for risk-based independent assessment; and
- `quest-handoff` for reconciliation before reset, compaction, or transfer.

Specialized skills may be used instead of or alongside these capabilities. Do
not duplicate a specialist workflow inside the quest record.

`quest-master` is an opt-in guide for a default discovery-to-delivery
workflow. Do not load it merely because a quest is opened or updated; using
quest memory or an individual capability does not opt into orchestration.

## Commands

Before running a command, read only its dedicated reference:

- `open`, `open current`, or `open current quest`: [Open](references/open.md)
- `new`: [New](references/new.md)
- `list`: [List](references/list.md)

When creating a quest, never replace an existing quest directory or file. Edit
existing quest material narrowly under the shared update contract.
