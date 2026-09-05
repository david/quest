# New

## `new <slug>`

Refuse an invalid slug or a slug that already exists in the quest root. Create `<quest-root>/<slug>/README.md` with the quest title and the stable `Goals`, `Current State`, `Research`, `Decisions`, `Plan`, `Implementation`, `Review`, and `Backlog` headings in that order. Populate the sections only from context supplied by the user; leave a section empty rather than inventing content. Add supplied goals and initial tasks as unchecked items. Point `Current State` at the initial active work when the user supplied any; otherwise record that no task has started and name choosing the next task as the next action.

Keep quest creation administrative and bounded. Create the record and perform any required workspace setup, parent linkage, and indexing from supplied or already-known context. Link authoritative existing artifacts instead of rereading or restating them. A request to include the information needed for later work does not by itself authorize codebase inventory, external research, implementation planning, architecture or decision changes, contract reconciliation, testing, or implementation. Perform those activities only when the user explicitly requests them separately.

For an issue-backed quest, preserve the leading issue number and keep the remainder concise. Prefer one to three hyphen-delimited words after the issue number; use four only when needed for clarity. Distill the issue title instead of copying it verbatim. If a proposed issue-prefixed slug exceeds four words after the issue number, shorten it before creating the quest and report the final slug.

When project instructions configure a quest template, follow their source and
destination rules. Use [Template rendering](render-template.md) for
`mise.local.toml` after the intended application workspace exists and an explicit
app port has been selected. Keep the directory slug hyphenated; the renderer
normalizes only substituted values. Record workspace paths, selected ports, and
setup results in the README without copying secrets. Do not assume the template
belongs at the quest root, overwrite existing configuration, or infer permission
to provision resources from the presence of a template. If required workspace
setup is blocked, preserve the quest record and the exact next setup action.
