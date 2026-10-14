# Quest

An agent skill that gives each task its own directory: a quest. A quest holds
`QUEST.md`, a short record that lets an agent pick the task up again without
the conversation that started it, plus the task's documents and code checkouts.

The skill covers creating, opening, updating, handing off, and archiving
quests. It does not prescribe how the work itself is done.

## Install

With [skills](https://github.com/vercel-labs/skills):

```sh
npx skills add david/quest -g
```

Or clone this repository and link the skill into your agent's skills directory:

```sh
git clone https://github.com/david/quest.git
ln -s "$PWD/quest/skills/quest" ~/.claude/skills/quest
```

Then set up a project with `/quest install`. This picks a quest root, a
directory named `quests` that lies outside the project repository, and declares
it in the project's `AGENTS.md`.

## Use

| Command | What it does |
| --- | --- |
| `install` | Set up quest support in a project. |
| `new` | Create a quest and capture its goal. |
| `open` | Open a quest and summarize where it stands. |
| `list` | List quests. |
| `sync` | Bring the record up to date with the session. |
| `handoff` | Check that another agent could resume from the record. |
| `distill` | Move findings into the project's own documentation. |
| `archive` | Archive a quest after checking its checkouts for unmerged work. |

Commands can also be asked for in plain language.

## Layout

```text
quests/
├── <slug>/
│   ├── QUEST.md        # the record; the only required file
│   ├── research/       # findings, read on demand
│   └── worktrees/
│       ├── 1/          # a copy-on-write clone of the project repository
│       └── <n>/        # Git worktrees of that clone
└── .archived/<slug>/
```

Each quest's code lives inside the quest, so removing the quest leaves nothing
behind in the project repository.

## Snapshots

`scripts/snapshot.py` commits each quest's records to the quest's own Git
repository, so earlier states can be recovered. Code checkouts and private
files are left out. The script is meant to run from a harness hook, not by the
agent. For Claude Code, add this to `~/.claude/settings.json` under `hooks` for
the `UserPromptSubmit`, `Stop`, `StopFailure`, and `SessionEnd` events:

```json
{
  "hooks": [
    {
      "type": "command",
      "command": "s=\"$HOME/.claude/skills/quest/scripts/snapshot.py\"; [ -f \"$s\" ] || exit 0; python3 \"$s\" . \"$CLAUDE_PROJECT_DIR\" >/dev/null || exit 1",
      "timeout": 60
    }
  ]
}
```

Change the path if the skill is installed somewhere else. See
[Snapshots](skills/quest/references/snapshot.md) for details.

## Requirements

- Git.
- Python 3.10 or newer, for the scripts.
- A filesystem with reflink support (such as Btrfs, XFS, or APFS) for the
  copy-on-write clone. Without it, the first checkout falls back to a Git
  worktree of the project repository.

## Tests

```sh
cd skills
python3 -m unittest discover -s quest/tests
```

## License

[MIT](LICENSE)
