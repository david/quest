# Open

## `open` or `open <slug>`

Open the named quest, or without a slug the quest the skill's resolution rules
select. The session can be anywhere: in the quest directory, below it, such as
in one of its checkouts, or outside it, such as in the project directory. When
no slug is given and the rules select no quest, ask which one to open and give
the output of `list`.

For a slug with no exact match in the quest root, look for clearly similar
slugs among the root's immediate directories. Open a single clear match and say
which quest it is. If several match, list them and ask the user to choose. If
none does, say that no quest was found.

Read `QUEST.md`, then the first checkout's instructions: `work/1/CLAUDE.md`
when you are Claude Code and `work/1/AGENTS.md` otherwise, falling back to the
other file when yours does not exist. Skip this when the quest has no `work/1`,
when it holds neither file, or when the session started inside `work/1` and so
loaded them already. Follow those instructions in the work that comes after;
they are not part of the summary. Read nothing else.

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
