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

After writing the initial `QUEST.md`, always move the current session to the absolute
`<quest-root>/<slug>` directory using OpenCode's `opencode.session_move` tool,
omitting `sessionID`. When tools are exposed through Code Mode, discover the tool
if necessary and invoke it through `execute`. Verify that the returned directory
matches the new quest and use its working-directory context and applicable
instructions for subsequent work. A shell `cd` does not move the session. Perform
this switch before further quest work or pausing, including when the user asks
only to create the record and pause. If switching is unavailable or fails,
preserve the created record, record the switching blocker and recovery action in
Current State, and report that creation succeeded but session switching did not.

After session switching and required setup, load
`quest-goals` and enter goal alignment in the same turn. Recap the understood
outcomes, scope, and success expectations; develop material gaps and tradeoffs
with the user, then seek confirmation of the resulting goal contract. Build on
supplied answers without requiring repetition. Do not stop at a creation notice
or merely recommend goal clarification for later.

While alignment is ongoing, keep confirmed intent, provisional interpretations,
and the next question recoverable from Current State. Record creation as complete
without implying that goal alignment is complete. Respect an explicit request to
create the record and pause. Keep workspace setup results and recovery actions
here.

Once goals are confirmed, continue any further work explicitly requested alongside
creation and retain useful results under the shared update contract. Otherwise,
summarize the agreed goals and recommend the next useful action without treating
alignment as authorization for planning or implementation.

Quest creation includes bounded workspace setup and conversational goal development.
Create the record and perform any required workspace setup, parent linkage, and
indexing from supplied or already-known context. Link authoritative existing
artifacts, reading only what goal alignment needs. Creation does not by itself
authorize codebase inventory, external research, implementation planning,
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
