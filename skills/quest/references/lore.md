# Lore

Lore is what a realm knows that outlives any single quest: facts about the
project's environment, such as how its services run, what its data contains,
or a rule the user has set for all of its work. It lives in the realm's `lore/`
directory, outside every repository, so it never ends up in the code. The
realm's `AGENTS.md` lists it, so every session in the realm knows what lore
exists without reading it.

Read this guide whenever a task touches lore: creating `lore/`, adding,
changing, moving, or removing a lore file, or writing the Lore section.
Reading a lore file for its facts needs only the Lore section's description of
it.

## What Belongs In Lore

Put a fact in lore when a later quest would need it to act correctly, or would
otherwise have to find it out again. A finding that serves only the current
quest belongs in that quest's `research/`, and a tentative finding or a one-off
workaround stays there until it is settled. [Knowledge transfer](distill.md)
covers moving a quest's findings into lore.

Give each subject one file, named after it, and extend that file rather than
adding one per quest or session. Lore follows the
[shared update contract](../SKILL.md#shared-update-contract): it says what is
true now, keeps each fact in one place, records who made each decision, and
ties evidence to the revision or date it was observed. A quest record links to
the lore it relies on instead of copying it.

## The Lore Section

The realm's `AGENTS.md` has a Lore section. It names the lore directory and
lists every lore file as a Markdown link with what the file covers, so a reader
can pick a file from the list and open it from there:

```markdown
## Lore

`<lore-path>/` holds facts about the project's environment that outlive any
single quest. Read the matching file when a task needs it.

- <What the file covers>: [`<file>.md`](<lore-path>/<file>.md).
```

Name the directory by its absolute path or a path relative to `AGENTS.md`, and
use the same base for the links. Leave the list out while the directory is
empty.

Keep the list matching the directory. When a lore file is added, renamed, or
removed, change its entry in the same turn, and when what a file covers
changes, update its description. Describe each file clearly enough that an
agent can tell from the list alone whether to read it. When reconciling an
existing section, add the files it is missing and turn entries that name a file
without linking it into links. Preserve the rest of `AGENTS.md`.
