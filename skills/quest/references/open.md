# Open

## `open`, `open current`, or `open current quest`

When the session is inside a canonically detected quest workspace, open the current quest. If the session is not inside a quest, ask for a slug.

After opening a quest, summarize its goals and `Current State`, then follow only the links needed to understand the active task and its exact next action. Inspect the relevant worktree and validation state before continuing when applicable. If `Current State` is absent, incomplete, or stale, report the handoff gap and use the first relevant pending unchecked task in section order as a fallback. An unchecked task with a result or outcome link awaits user approval and must not be repeated; an unchecked task without one remains pending. Do not modify the README merely because it was opened.

## `open <slug>`

Look for an exact slug directory in the quest root. If absent, look for clearly similar slugs among its immediate directories. Open one clear match and report the mapping. If several match, list them and ask the user to choose. If none match, say that no quest was found.
