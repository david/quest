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
   its destination in the active application worktree, and the renderer invocation
   from [Template rendering](render-template.md). If this project does not use
   worktrees, explicitly establish the appropriate per-quest application directory
   rather than overwriting a shared application's local configuration.
4. Establish the app-port selection convention and any additional project-specific
   template values. Prefer the project's existing allocator or registry. Otherwise
   select an explicit available port, compare with recorded active quests, and
   record it in the quest README. An availability check is not a port reservation.
5. Explain that new quests read their README first, record active workspace paths
   there, and follow repository instructions in that workspace before repository
   work. Do not create per-quest `AGENTS.md` files by default or opt into
   `quest-master`. Keep provisioning, worktree creation, `mise trust`, dependency
   installation, and service startup as separate project-specific instructions
   subject to their own authorization.

The four baseline settings are the primary database URL, test database URL, app
port, and process-compose socket path. Include the matching process-compose log
path as well. Adapt unsupported settings to the actual project rather than
inventing services. Database names and socket paths must distinguish projects
and quests. Additional values such as Storybook ports are project-specific.

Do not overwrite an existing template. Compare it with the intended setup and
propose only needed changes. Never copy local secrets into a template. Flag any
needed ignore rules for generated local configuration under the project's policy.

Validate the resulting instructions and template together: render the template
into a temporary directory using a valid sample slug and explicit port, then
check the resulting values without provisioning resources. Report files changed,
unresolved setup choices, and any validation limits. The project is ready for
templated quest creation only when the destination and required values are clear.
