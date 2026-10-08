# Open

## `open`

Opening requires the session's working directory to be inside the quest: the
quest directory itself, which holds `QUEST.md`, or anything below it, such as
one of its checkouts. Open that quest.

Read only `QUEST.md` and summarize its goals and `Current State`, including
recorded next actions, blockers, and approvals. If `QUEST.md` shows that the work
is complete or intentionally paused, say so. Report gaps apparent in `QUEST.md`
without following links or investigating them. Wait for the user's direction;
when the opening prompt also includes a question or request for work, load the
context needed for that request and proceed in the same turn.

An unchecked normal task remains pending. An unchecked `Approval:` item with a
result or outcome link awaits user approval and must not cause the underlying
work to be repeated; `Current State` must identify that approval explicitly. For
quest material predating the `Approval:` convention, also preserve that behavior
when `Current State` explicitly says the item awaits approval. Do not inspect a
checkout or modify `QUEST.md` merely because the quest was opened.

## Outside the quest

When no quest contains the working directory, or the user names a quest other
than the one that does, do not open it. Say so, and ask the user to change to
that quest's directory and start the session there. Give the absolute path: for
a named slug that exists in the quest root, `<quest-root>/<slug>`; for a name
that clearly matches other slugs, those paths; with no name, the output of
`list`.
