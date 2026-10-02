# Template Rendering

Use the shared skill script rather than agent-written substitutions. Requires
Python 3.11 or newer. Resolve the script from the loaded `quest` skill directory,
not the project directory; do not copy the renderer into each project.

```sh
python3 <quest-skill-directory>/scripts/render-template.py \
  --template <project-directory>/quest-template/mise.local.toml \
  --destination <quest-root>/123-add-login/mise.local.toml \
  --slug 123-add-login \
  --app-port 5101
```

The default destination is the quest directory alongside its `QUEST.md`, not an
application worktree. Application worktrees live beneath it at `work/<n>/` and
inherit the configuration through mise's ancestor discovery. Follow an existing
project's explicitly configured alternative destination instead of migrating it.

Quote actual paths as needed. The destination parent must already exist. The
renderer handles only this explicitly selected TOML file, not recursive copying
or template hooks. It replaces `<slug>` with `123_add_login` and `<app-port>`
with `5101`. The quest directory remains `123-add-login`. Project-specific values
such as `<project>` must already be resolved during installation.

The script validates the slug, port range, unresolved `<name>` placeholders, and
rendered TOML before creating anything. It refuses existing destinations,
including symlinks, and creates configuration with owner-only permissions.
It never selects ports, creates databases, trusts mise files, or starts services.

The renderer requires `--app-port` even when a project template omits `<app-port>`;
in that case, supply a valid sample value without allocating a service port.
When the template uses it, choose the port separately using project conventions
and record it alongside the active workspace in `QUEST.md`. A hash of the slug does not guarantee a
unique port, and a free-port check does not reserve it. If the destination already
exists, inspect and reconcile it with the user rather than deleting it to rerun
the renderer. Record failed setup and its exact recovery action in `Current State`.
