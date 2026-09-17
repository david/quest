# Install

## `install [project-directory]`

Install quest memory, with workspace-template conventions when applicable, not a
workflow. Use the explicit project directory, or the session's current working directory when
omitted. Canonicalize the target and confirm it is the intended project when
ambiguous. Do not require existing quest-root discovery or install into the skill
directory. Do not create a quest, worktree, database, or running service.

Inspect the target's existing `AGENTS.md`, quest setup, and relevant environment
configuration. Reuse a valid existing quest-root declaration and template setup;
do not create parallel roots or migrate existing quests. Ask before changing a
conflicting declaration, file layout, or setup rule. Rerunning installation must
preserve existing files and avoid duplicate instruction blocks.

For a fresh installation, the baseline is:

1. Create `quests/` under the project directory.
2. Add or narrowly update a quest setup section in the project's `AGENTS.md`.
   Preserve all unrelated instructions. Declare `Quest root: ./quests` (or the
   reused root, relative to this instruction file).
3. Explain that new quests read their README first, record active workspace paths
   there when applicable, and follow repository instructions in that workspace
   before repository work. Do not create per-quest `AGENTS.md` files by default
   or opt into `quest-master`.

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
   README, and the renderer invocation from
   [Template rendering](render-template.md). For projects using Git worktrees,
   establish `<quest-root>/<slug>/work/<n>/` as the application worktree location,
   where `<n>` is a positive integer. Allow multiple worktrees per quest; choose
   unused numbers and record each path, branch, and purpose in the README.
   Do not create worktrees during installation. Do not default to sibling
   worktrees outside the quest or put generated config inside an application
   checkout. Preserve an established alternative layout; ask before changing it.
   For application projects without worktrees, establish the per-quest application
   location and how its commands load any quest configuration without overwriting
   shared application configuration.
3. When services need ports, establish the app-port selection convention and any
   additional project-specific template values. Prefer the project's existing
   allocator or registry. Otherwise
   select an explicit available port, compare with recorded active quests, and
   record it in the quest README. An availability check is not a port reservation.
   Multiple worktrees in one quest inherit the same settings by default, not
   separate runtime allocations. Document one running instance per quest with
   those defaults, or establish explicit per-instance overrides for concurrent
   services (ports, sockets, logs, and databases when isolation is needed).
4. Keep provisioning, worktree creation, `mise trust`, dependency installation,
   and service startup as separate project-specific instructions subject to their
   own authorization.

For projects using mise and Git worktrees, the default layout after authorized
quest and worktree creation is:

```text
<quest-root>/<slug>/
├── README.md
├── mise.local.toml
└── work/
    ├── 1/                 # Application Git worktree
    └── 2/                 # Optional additional worktree
```

When mise is configured, explain that it loads the quest config through ancestor
discovery when run inside a nested worktree, alongside that worktree's own
`mise.toml`. Once the
configs are trusted as authorized, use `mise run <task>` from the worktree or
`mise -C work/1 run <task>` from the quest directory. An outer `mise exec` wrapper
is not needed for this layout. For a reused alternative layout, document and
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
Do not add an application-repository ignore rule for a quest-level file outside
that repository; assess whether the quest storage itself is version-controlled.

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
