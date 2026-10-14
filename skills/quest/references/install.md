# Install

## `install [project-directory]`

Install quest memory, with workspace-template conventions when applicable, not a
workflow. Use the explicit project directory, or the session's current working directory when
omitted. Canonicalize the target and confirm it is the intended project when
ambiguous. Do not require existing quest-root discovery or install into the skill
directory. Do not create a quest, checkout, database, or running service.

Inspect the target's existing `AGENTS.md`, quest setup, and relevant environment
configuration. Reuse a valid existing quest-root declaration and template setup;
do not create parallel roots or migrate existing quests. Ask before changing a
conflicting declaration, file layout, or setup rule. Rerunning installation must
preserve existing files and avoid duplicate instruction blocks.

For installation or reconciliation of an existing setup, the baseline is:

1. Reuse the configured quest root or default to `./quests` under the project
   directory. The root must be named `quests` and lie outside any repository,
   which the [snapshot script](snapshot.md) enforces; if the project directory
   is itself a repository, agree with the user where the root goes before
   creating anything. Create the storage directory. Where the script refuses
   an existing root, preserve its records and ask before moving them.
2. Add or narrowly update a quest setup section in the project's `AGENTS.md`.
   Preserve all unrelated instructions. Declare `Quest root: <path>` using the
   selected root's absolute path or a path relative to this instruction file.
3. Explain that new quests read their `QUEST.md` first, record active workspace paths
   there when applicable, and follow repository instructions in that workspace
   before repository work. Do not create per-quest `AGENTS.md` files by default.

Add only the workspace conventions applicable to the project:

1. For projects using mise-based per-quest environments, create `quest-template/`
   and adapt the skill's `assets/mise.local.toml` to
   `quest-template/mise.local.toml`. Include only settings the project uses.
   When a database is needed, choose its connection format and variable names
   from actual configuration; confirm any missing convention rather than assuming
   the bundled PostgreSQL format applies.
   Replace `<project>` with a stable project identifier normalized to lowercase
   words separated by underscores; confirm an ambiguous identifier. Retain
   `<slug>` and, when needed, `<app-port>` for per-quest rendering. Do not embed
   credentials; preserve the project's established secret-loading mechanism.
2. In the setup instructions, describe any configured template source,
   its destination at `<quest-root>/<slug>/mise.local.toml` alongside the quest
   `QUEST.md`, and the renderer invocation from
   [Template rendering](render-template.md). Do not put generated config
   inside a checkout.
3. For projects whose quests work on code, name the repository that a quest's
   `worktrees/1` is cloned from under the skill's Documents And Code rules, and
   add only what the project does differently, such as a default branch other
   than `main` or how branches are named.
   Preserve an established alternative, such as worktrees of the project
   repository or one shared checkout, and ask before changing it; for such a
   project, record where a quest's code lives and how its commands load quest
   configuration without overwriting shared configuration.
   Do not create checkouts during installation.
4. When services need ports, establish the app-port selection convention and any
   additional project-specific template values. Prefer the project's existing
   allocator or registry. Otherwise
   select an explicit available port, compare with recorded active quests, and
   record it in `QUEST.md`. An availability check is not a port reservation.
   Multiple checkouts in one quest inherit the same settings by default, not
   separate runtime allocations. Document one running instance per quest with
   those defaults, or establish explicit per-instance overrides for concurrent
   services (ports, sockets, logs, and databases when isolation is needed).
5. Keep provisioning, checkout creation, `mise trust`, dependency installation,
   and service startup as separate project-specific instructions subject to their
   own authorization.

For projects using mise, the default layout after authorized quest and
checkout creation is:

```text
<quest-root>/<slug>/
├── QUEST.md
├── mise.local.toml
└── worktrees/
    ├── 1/                 # The quest's clone of the repository
    └── 2/                 # Optional worktree of that clone
```

When mise is configured, explain that it loads the quest config through ancestor
discovery when run inside a nested checkout, alongside that checkout's own
`mise.toml`. Once the
configs are trusted as authorized, use `mise run <task>` from the checkout or
`mise -C worktrees/1 run <task>` from the quest directory. An outer
`mise exec` wrapper is not needed for this layout. For a reused alternative layout, document and
validate explicit config loading if ancestor discovery cannot reach the quest.

The bundled template offers primary and test database URLs, an app port, and
process-compose socket and log paths. Retain database settings only for projects
using databases, ports only for applicable services, and socket/log paths only
when using process-compose. Database names and socket paths, when used, must
distinguish projects and quests. Additional values such as Storybook ports are
project-specific.

Do not overwrite an existing template. Compare it with the intended setup and
propose only needed changes. Never copy local secrets into a template. Flag any
needed ignore rules for generated local configuration under the project's policy.
Keep quest-level private configuration excluded in the quest's own repository
under the skill's Versioned Checkpoints rules. Application-repository ignore
rules do not apply to files outside that repository.

Validate the quest-root declaration and resulting instructions. When a template
is configured, validate it with the instructions: render the template
into a temporary directory using a valid sample slug and explicit renderer port, then
check the resulting values without provisioning resources. Verify that a harmless
command in a representative application directory receives the configured quest
environment; do not start services or persist trust changes for this check.
Report files changed,
unresolved setup choices, and any validation limits. Basic quest setup does not
require a runtime template. When templated creation is configured, it is ready
only when the destination and required values are clear.
