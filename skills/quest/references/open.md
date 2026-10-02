# Open

## `open`, `open current`, or `open current quest`

When the session is inside a canonically detected quest workspace, open the current quest. If the session is not inside a quest, ask for a slug.

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
project worktree or modify `QUEST.md` merely because the quest was opened.

## `open <slug>`

Look for an exact slug directory in the quest root. If absent, look for clearly similar slugs among its immediate directories. Open one clear match and report the mapping. If several match, list them and ask the user to choose. If none match, say that no quest was found.
