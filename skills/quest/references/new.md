# New

## `new <slug>`

Refuse an invalid slug or a slug that already exists in the quest root. Create `<quest-root>/<slug>/README.md` with the quest title and the stable `Goals`, `Current State`, `Research`, `Decisions`, `Implementation`, `Review`, and `Backlog` headings in that order. Populate the sections only from context supplied by the user; leave a section empty rather than inventing content. Add supplied goals and initial tasks as unchecked items. Point `Current State` at the initial active task when the user supplied one; otherwise record that no task has started and name choosing the next task as the next action.

For an issue-backed quest, preserve the leading issue number and keep the remainder concise. Prefer one to three hyphen-delimited words after the issue number; use four only when needed for clarity. Distill the issue title instead of copying it verbatim. If a proposed issue-prefixed slug exceeds four words after the issue number, shorten it before creating the quest and report the final slug.
