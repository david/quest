# Lore

Lore is what a realm knows that outlives any single quest: facts about the
project's environment, such as how its services run, what its data contains,
or a rule the user has set for all of its work. It lives in the realm's
`lore/`, outside every repository, and the realm's `AGENTS.md` lists it. Read
this guide when creating `lore/`, when adding, changing, moving, or removing a
lore file, or when writing the Lore section. Reading a lore file for its facts
needs only its entry in that section.

## What Belongs In Lore

A fact belongs in lore when a later quest would need it to act correctly or
would otherwise have to find it out again. A finding that serves only one
quest, or one that is tentative or a one-off workaround, stays in that quest's
`research/`. [Distill](../SKILL.md#distill) covers moving findings into lore.

Give each subject one file, named after it, and extend that file rather than
adding one per quest or session. Lore follows the skill's
[update rules](../SKILL.md#update-rules), and a quest record links to the lore
it relies on instead of copying it.

## The Lore Section

The realm's `AGENTS.md` has a Lore section that names the lore directory and
links every lore file with what it covers:

```markdown
## Lore

`<lore-path>/` holds facts about the project's environment that outlive any
single quest. Read the matching file when a task needs it.

- <What the file covers>: [`<file>.md`](<lore-path>/<file>.md).
```

Name the directory by its absolute path or a path relative to `AGENTS.md`, and
use the same base for the links. Leave the list out while the directory is
empty. When a lore file is added, renamed, or removed, or what it covers
changes, update its entry in the same turn, and describe each file well enough
that an agent can tell from the list alone whether to read it. When
reconciling an existing section, add the files it is missing, turn unlinked
names into links, and keep the rest of `AGENTS.md`.
