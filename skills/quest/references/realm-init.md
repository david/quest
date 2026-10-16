# Realm Init

## `realm init [directory]`

Make a project a realm: set up quest memory in it, with a template for new
quests and workspace conventions when applicable, not a workflow. Use the explicit directory, or
the session's current working directory when omitted.
Canonicalize the target and confirm it is the intended realm when ambiguous.
Do not require existing quest-root discovery or set up the skill directory as a
realm. Do not create a quest, checkout, database, or running service.

Stop without changing anything when the target is a Git repository or
lies inside one, that is, when it or any parent holds a `.git` entry. The quest
root and `lore/` must stay out of every repository. Tell the user to run
`realm init` from a directory outside the repository, such as one that holds it.

Inspect the target's existing `AGENTS.md`, quest setup, and relevant environment
configuration. Reuse a valid existing quest-root declaration and template setup;
do not create parallel roots or migrate existing quests. Ask before changing a
conflicting declaration, file layout, or setup rule. Rerunning `realm init` must
preserve existing files and avoid duplicate instruction blocks.

For a new realm or reconciliation of an existing setup, the baseline is:

1. Reuse the configured quest root or default to `./quests` in the realm. The
   root must be named `quests` and lie outside any repository, which the
   [snapshot script](snapshot.md) enforces. Create the storage directory.
   Where the script refuses an existing root, preserve its records and ask
   before moving them.
2. Add or narrowly update a quest setup section in the realm's `AGENTS.md`.
   Preserve all unrelated instructions. Declare `Quest root: <path>` using the
   selected root's absolute path or a path relative to this instruction file.
3. Explain that new quests read their `QUEST.md` first, record active workspace paths
   there when applicable, and follow repository instructions in that workspace
   before repository work. Do not create per-quest `AGENTS.md` files by default.
4. Create `lore/` in the realm. It holds facts about the project's
   environment that outlive any single quest, as [Lore](lore.md) describes.
5. Add a Lore section to the same `AGENTS.md` in the format
   [Lore](lore.md#the-lore-section) gives. When reconciling, bring an existing
   Lore section to that format.
6. Create `quest-template/` in the realm. [New](new.md#workspace-setup) copies
   its contents into every new quest, so it holds what each quest starts with,
   such as agent or editor settings. It stays empty until the realm has
   something to put there.

Add only the workspace conventions applicable to the realm:

1. For realms whose quests work on code, name the repository that a quest's
   `worktrees/1` is cloned from under the skill's Documents And Code rules, and
   add only what the repository does differently, such as a default branch other
   than `main` or how branches are named.
   Preserve an established alternative, such as worktrees of the realm's
   repository or one shared checkout, and ask before changing it; for such a
   realm, record where a quest's code lives and how its commands load quest
   configuration without overwriting shared configuration.
   Do not create checkouts during `realm init`.
2. When a quest needs values of its own, such as a port, a database name, or a
   socket path, say in the setup section how a new quest chooses and records
   them. The skill copies the template unchanged and fills in nothing. For
   ports, prefer the realm's existing allocator or registry. Otherwise select
   an explicit available port, compare with recorded active quests, and record
   it in `QUEST.md`. An availability check is not a port reservation. Multiple
   checkouts in one quest share the quest's values by default; document one
   running instance per quest, or explicit per-instance overrides where
   services run concurrently.
3. Keep provisioning, checkout creation, trusting configuration, dependency
   installation, and service startup as separate realm-specific instructions
   subject to their own authorization.

Do not overwrite or empty an existing `quest-template/`; propose only needed
changes to it. Never put secrets in a template, since every quest gets a copy.
Files copied from the template are snapshotted with the quest's records unless
an ignore rule covers them, so a template can include the quest's `.gitignore`,
as the skill's Versioned Checkpoints rules describe. Application-repository
ignore rules do not apply to files outside that repository.

Validate the quest-root declaration and resulting instructions. Report files
changed, unresolved setup choices, and any validation limits.
