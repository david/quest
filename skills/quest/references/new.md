# New

## `new <slug>`

Refuse an invalid slug or a slug that already exists in the quest root. Create
`<quest-root>/<slug>/README.md` with the quest title, then only `Brief` and
`Current State`. Workflow sections belong to the selected orchestrator or
capabilities and are not part of administrative creation.

Capture supplied context only in `Brief`: the initial request, relevant background,
source links, stated constraints, and suggested goals, approaches, or tasks. Treat
this as input to discovery, not established goals, findings, accepted decisions,
or an approved plan. Preserve explicit user constraints without inventing content.
Leave `Brief` empty if no useful context was supplied. If further work was
explicitly requested alongside creation, perform it separately after creating
the record; its results may then populate their owning sections, adding them as
needed.

Initialize `Current State` with no substantive task started, a checkpoint that the
quest was created and whether a brief was captured, and any setup blockers. When
the user has opted into `quest-master`, name goal discovery from the brief as the
next action. Otherwise use the user's selected next activity, or recommend the
smallest useful next action supported by the supplied context. Clarify intent only
when a material question remains unresolved; do not ask the user to repeat clear
outcomes. Creation alone does not invoke or opt into orchestration. If no further
work is requested, record creation as complete without inventing a task. Keep
workspace setup results and recovery actions here,
not in substantive sections as invented tasks or findings.

Keep quest creation administrative and bounded. Create the record and perform any required workspace setup, parent linkage, and indexing from supplied or already-known context. Link authoritative existing artifacts instead of rereading or restating them. A request to include the information needed for later work does not by itself authorize codebase inventory, external research, implementation planning, architecture or decision changes, contract reconciliation, testing, or implementation. Perform those activities only when the user explicitly requests them separately.

When generating an issue-backed quest slug, preserve the leading issue number
and use a concise, recognizable summary of the title. Concision is a default,
not a word-count limit; preserve an explicitly supplied valid user slug.

When project instructions configure a quest template, follow their source and
destination rules. Use [Template rendering](render-template.md) for
`mise.local.toml` after its destination directory exists, selecting an app port
only when the template uses one. Keep the directory slug hyphenated; the renderer
normalizes only substituted values. Record workspace paths, selected ports, and
setup results in the README without copying secrets. The default destination is
the individual quest directory alongside its README, not the shared quest root
or an application worktree. Application worktrees, when authorized, use
`<quest-root>/<slug>/work/<n>/`; rendering the quest config does not require a
worktree to exist. Preserve explicit project alternatives. Do not overwrite
existing configuration or infer permission
to provision resources from the presence of a template. If required workspace
setup is blocked, preserve the quest record and the exact next setup action.
