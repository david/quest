# Shop

Each quest lives in `quests/<slug>/`. Read its `QUEST.md` first and keep its
Current State up to date. A quest's code lives in its `worktrees/` directory:
`worktrees/1` is a clone of `./app`, the shop's invoicing code. Follow the
checkout's own instructions before working in it. Do not create per-quest
`AGENTS.md` files.

`upstream/app.git` is the shared remote, `origin` for `./app` and its clones.

## Lore

`lore/` holds facts about the project's environment that outlive any single
quest. Read the matching file when a task needs it.
