# Open

## `open`

Opening requires the session's working directory to be the quest directory
itself, the one that holds `QUEST.md`. Open that quest. A directory below it,
such as one of its checkouts, does not qualify.

Read `QUEST.md`, then the first checkout's instructions: `work/1/AGENTS.md`, or
`work/1/CLAUDE.md` when there is no `AGENTS.md`. Skip this when the quest has no
`work/1` or it holds neither file. Follow those instructions in the work that
comes after; they are not part of the summary. Read nothing else.

Summarize the goals and `Current State` in `QUEST.md`, including
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
checkout beyond that instruction file, or modify `QUEST.md`, merely because the
quest was opened.

## Outside the quest directory

When the working directory is not a quest directory, or the user names a quest
other than the one it is, do not open it. Say so, and ask the user to change to
that quest's directory and start the session there. Give the absolute path: for
a session below a quest directory, that directory; for a named slug that exists
in the quest root, `<quest-root>/<slug>`; for a name that clearly matches other
slugs, those paths; otherwise the output of `list`.
