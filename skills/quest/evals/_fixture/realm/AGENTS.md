# Shop

Each quest lives in `quests/<slug>/`. Read its `QUEST.md` first and keep its
Current State up to date. `./app` is the shop's invoicing code. A quest's
checkout is a Git worktree of it at `worktrees/<slug>`, on a branch named after
the quest. Make it with `git -C app worktree add -b <slug> ../worktrees/<slug>
main`, and remove it with `git -C app worktree remove ../worktrees/<slug>`.
Follow the checkout's own instructions before working in it. Do not create
per-quest `AGENTS.md` files.

`upstream/app.git` is the shared remote, `origin` for `./app` and its clones.

## Lore

`lore/` holds facts about the project's environment that outlive any single
quest. Read the matching file when a task needs it.
