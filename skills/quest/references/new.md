# New

## `new <slug>`

Refuse an invalid slug or a slug that already exists in the quest root. Create
`<quest-root>/<slug>/QUEST.md` from the skill's record template: frontmatter
with `quest_skill_version`, the quest title, and `Current State`. Add Backlog or
References only when the supplied context needs them.

Capture the objective, relevant background, and explicit constraints the user
supplied, linking substantial existing material instead of copying it and
reading only what capturing the goal requires. Keep what the user stated
distinct from goals, approaches, or tasks that were only suggested. If no
objective was supplied, record it as unresolved rather than inventing one. Start
Current State with no task begun, a checkpoint that the quest was created, and
any setup blockers.

Then summarize the captured objective and constraints for the user. If a gap in
the goal could change the work, ask the smallest useful question; clear intent
needs no confirmation round. Respect an explicit request to create the record
and pause.

Creating a quest covers the record and its workspace setup. It does not by
itself start research, planning, or implementation; continue into those only
when the same request asks for them and the goal is clear enough.

Do not initialize a Git repository in the quest directory. The next snapshot
does that under the skill's Versioned Checkpoints rules.

## Slugs

When generating an issue-backed quest slug, preserve the leading issue number
and use a concise, recognizable summary of the title. For PR-based quests, use
`pr-<number>-<description>`, for example `pr-3708-calendar-subscription-prototype`.
Concision is a default, not a word-count limit; preserve an explicitly supplied
valid user slug.

## Workspace setup

Perform the setup the project's instructions require for a new quest, from
supplied or already-known context. When they configure a quest template, follow
their source and destination rules and use [Template rendering](render-template.md)
for `mise.local.toml` once its destination directory exists, selecting an app
port only when the template uses one. Keep the directory slug hyphenated; the
renderer normalizes only substituted values.

The default destination is the individual quest directory alongside its
`QUEST.md`, not the shared quest root or a checkout. Checkouts, when
authorized, are made under the skill's Documents And Code rules; rendering the
quest config does not require one to exist. Preserve explicit project
alternatives. Do not overwrite existing configuration, and do not treat the
presence of a template as permission to provision resources.

Record the workspace paths and selected ports needed to use the workspace, plus
material setup exceptions, in Current State, without copying secrets or
narrating each successful setup command. If required setup is blocked, keep the
quest record and record the exact next setup action.

## Herdr workspace label

After creating the quest, when the session runs inside a Herdr-managed pane
(`HERDR_ENV=1`), label the calling pane's workspace with the quest slug:

```sh
herdr workspace rename "$HERDR_WORKSPACE_ID" <slug>
```

Skip this silently outside Herdr. A failed rename does not block creating the
quest; mention it briefly and continue.
