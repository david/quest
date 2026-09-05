# Install

## `install [project-directory]`

Install quest memory and workspace-template conventions, not a workflow. Use the
explicit project directory, or the session's current working directory when
omitted. Canonicalize the target and confirm it is the intended project when
ambiguous. Do not require existing quest-root discovery or install into the skill
directory. Do not create a quest, worktree, database, or running service.

Inspect the target's existing `AGENTS.md`, quest setup, and relevant environment
configuration. Reuse a valid existing quest-root declaration and template setup;
do not create parallel roots or migrate existing quests. Ask before changing a
conflicting declaration, file layout, or setup rule. Rerunning installation must
preserve existing files and avoid duplicate instruction blocks.

For a fresh installation:

1. Create `quests/` and `quest-template/` under the project directory.
2. Create `quest-template/mise.local.toml` from the skill's
   `assets/mise.local.toml`. Choose the project's database connection format and
   variable names from its actual configuration. The bundled PostgreSQL format
   is a fallback to confirm when the project supplies no database convention.
   Replace `<project>` with a stable project identifier normalized to lowercase
   words separated by underscores; confirm an ambiguous identifier. Retain
   `<slug>` and `<app-port>` for per-quest rendering. Do not embed credentials;
   preserve the project's established secret-loading mechanism.
3. Add or narrowly update a quest setup section in the project's `AGENTS.md`.
   Preserve all unrelated instructions. Declare `Quest root: ./quests` (or the
   reused root, relative to this instruction file). Describe the template source,
   its destination at `<quest-root>/<slug>/mise.local.toml` alongside the quest
   README, and the renderer invocation from
   [Template rendering](render-template.md). For projects using Git worktrees,
   establish `<quest-root>/<slug>/work/<n>/` as the application worktree location,
   where `<n>` is a positive integer. Allow multiple worktrees per quest; choose
   unused numbers and record each path, branch, and purpose in the README.
   Do not create worktrees during installation. Do not default to sibling
   worktrees outside the quest or put generated config inside an application
   checkout. Preserve an established alternative layout; ask before changing it.
   For projects without worktrees, establish the per-quest application location
   and how its commands load the quest configuration without overwriting shared
   application configuration.
4. Establish the app-port selection convention and any additional project-specific
   template values. Prefer the project's existing allocator or registry. Otherwise
   select an explicit available port, compare with recorded active quests, and
   record it in the quest README. An availability check is not a port reservation.
   Multiple worktrees in one quest inherit the same settings by default, not
   separate runtime allocations. Document one running instance per quest with
   those defaults, or establish explicit per-instance overrides for concurrent
   services (ports, sockets, logs, and databases when isolation is needed).
5. Explain that new quests read their README first, record active workspace paths
   there, and follow repository instructions in that workspace before repository
   work. Do not create per-quest `AGENTS.md` files by default or opt into
   `quest-master`. Keep provisioning, worktree creation, `mise trust`, dependency
   installation, and service startup as separate project-specific instructions
   subject to their own authorization.

The default layout after authorized quest and worktree creation is:

```text
<quest-root>/<slug>/
├── README.md
├── mise.local.toml
└── work/
    ├── 1/                 # Application Git worktree
    └── 2/                 # Optional additional worktree
```

Explain that mise loads the quest config through ancestor discovery when run
inside a nested worktree, alongside that worktree's own `mise.toml`. Once the
configs are trusted as authorized, use `mise run <task>` from the worktree or
`mise -C work/1 run <task>` from the quest directory. An outer `mise exec` wrapper
is not needed for this layout. For a reused alternative layout, document and
validate explicit config loading if ancestor discovery cannot reach the quest.

The four baseline settings are the primary database URL, test database URL, app
port, and process-compose socket path. Include the matching process-compose log
path as well. Adapt unsupported settings to the actual project rather than
inventing services. Database names and socket paths must distinguish projects
and quests. Additional values such as Storybook ports are project-specific.

Do not overwrite an existing template. Compare it with the intended setup and
propose only needed changes. Never copy local secrets into a template. Flag any
needed ignore rules for generated local configuration under the project's policy.
Do not add an application-repository ignore rule for a quest-level file outside
that repository; assess whether the quest storage itself is version-controlled.

Validate the resulting instructions and template together: render the template
into a temporary directory using a valid sample slug and explicit port, then
check the resulting values without provisioning resources. Verify that a harmless
command in a representative nested application directory receives the quest
environment; do not start services or persist trust changes for this check.
Report files changed,
unresolved setup choices, and any validation limits. The project is ready for
templated quest creation only when the destination and required values are clear.
