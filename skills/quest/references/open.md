# Open

## `open`, `open current`, or `open current quest`

When the session is inside a canonically detected quest workspace, open the current quest. If the session is not inside a quest, ask for a slug.

After opening a quest, summarize its goals and `Current State`, then follow only the links needed to understand the active tasks and their exact next actions. If `Current State` is absent, incomplete, or stale, report the handoff gap and use the first relevant actionable unchecked task in section order as a fallback. An unchecked normal task remains pending. An unchecked `Approval:` item with a result or outcome link awaits user approval and must not cause the underlying work to be repeated; `Current State` must identify that approval explicitly. For quest material predating the `Approval:` convention, also preserve that behavior when `Current State` explicitly says the item awaits approval. Do not inspect a project worktree or modify the README merely because the quest was opened.

## `open <slug>`

Look for an exact slug directory in the quest root. If absent, look for clearly similar slugs among its immediate directories. Open one clear match and report the mapping. If several match, list them and ask the user to choose. If none match, say that no quest was found.
