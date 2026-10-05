# New

## `new <slug>`

Refuse an invalid slug or a slug that already exists in the quest root. Create
`<quest-root>/<slug>/QUEST.md` with the quest title and `Current State`.
Add Backlog or References only when supplied context needs them.

The snapshot plugin discovers the new quest at turn completion and preserves its
initial eligible records under the skill's Versioned Checkpoints rules.

Capture the supplied objective, relevant background, and explicit constraints in
Current State, linking substantial existing material. Distinguish confirmed intent
from suggested goals, approaches, or tasks; creation does not establish findings,
accept decisions, or approve a plan. If no objective was supplied, state that it
is unresolved rather than inventing one.

Initialize Current State with no substantive task started, a checkpoint that the
quest was created, and any setup blockers.

After required setup, summarize the captured objective and
material constraints. If goal gaps could change the work, use
[goal clarification](goals.md) and ask the smallest useful question. Clear supplied
intent does not require another confirmation round. Keep unresolved questions and
provisional interpretations recoverable without inventing an alignment blocker.

Continue further work explicitly requested alongside creation when the goal is
clear enough. Otherwise report creation and any unresolved goal or setup gap;
recommend a next action only when useful. Respect an explicit request to create
the record and pause. Keep workspace setup results and recovery actions in
Current State. Creation alone does not authorize planning or implementation.

Quest creation includes bounded workspace setup and necessary goal clarification.
Create the record and perform any required workspace setup, parent linkage, and
indexing from supplied or already-known context. Link authoritative existing
artifacts, reading only what capturing or clarifying the goal needs. Creation does
not by itself authorize codebase inventory, external research, implementation planning,
architecture or delivery decision changes, reconciliation of downstream contracts,
testing, or implementation. Perform those activities only when the user explicitly
requests them separately.

When generating an issue-backed quest slug, preserve the leading issue number
and use a concise, recognizable summary of the title. For PR-based quests, use
`pr-<number>-<description>`, for example `pr-3708-calendar-subscription-prototype`.
Concision is a default, not a word-count limit; preserve an explicitly supplied
valid user slug.

When project instructions configure a quest template, follow their source and
destination rules. Use [Template rendering](render-template.md) for
`mise.local.toml` after its destination directory exists, selecting an app port
only when the template uses one. Keep the directory slug hyphenated; the renderer
normalizes only substituted values. Record workspace paths, selected ports, and
setup results in `QUEST.md` without copying secrets. The default destination is
the individual quest directory alongside its `QUEST.md`, not the shared quest root
or an application worktree. Application worktrees, when authorized, use
`<quest-root>/<slug>/work/<n>/`; rendering the quest config does not require a
worktree to exist. Preserve explicit project alternatives. Do not overwrite
existing configuration or infer permission
to provision resources from the presence of a template. If required workspace
setup is blocked, preserve the quest record and the exact next setup action.
