# Open

## `open` or `open current`

When the session is inside a canonically detected quest workspace, open the current quest. If the session is not inside a quest, ask for a slug.

After opening a quest, summarize its goals and the first relevant unchecked task in section order. An unchecked task with a result or outcome link awaits user approval and must not be repeated; an unchecked task without one remains pending. Follow only the links needed to understand that task, and inspect the relevant worktree before continuing when applicable. Do not modify the README merely because it was opened.

## `open <slug>`

Look for an exact slug directory in the quest root. If absent, look for clearly similar slugs among its immediate directories. Open one clear match and report the mapping. If several match, list them and ask the user to choose. If none match, say that no quest was found.
