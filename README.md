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

Then set up a project with `/quest realm init`. This makes it a realm: it picks
a quest root, a directory named `quests` that lies outside the project
repository, and declares it in the project's `AGENTS.md`. It also creates a
`lore/` directory for facts that outlive any single quest, adds a Lore
section to `AGENTS.md` that links to each of its files, and creates an empty
`quest-template/` directory whose contents are copied into each new quest. Run
it from a directory that holds the repository, not from inside the repository;
it refuses to run there.

## Use

| Command | What it does |
| --- | --- |
| `realm init` | Set up a project for quests, making it a realm. |
| `new` | Create a quest and capture its goal. |
| `open` | Open a quest and summarize where it stands. |
| `list` | List quests. |
| `sync` | Bring the record up to date with the session. |
| `handoff` | Check that another agent could resume from the record. |
| `distill` | Move findings into the realm's own documentation. |
| `archive` | Archive a quest after checking its checkouts for unmerged work. |

Commands can also be asked for in plain language.

## Layout

```text
<realm>/
├── AGENTS.md               # declares the quest root and lists the lore
├── lore/                   # facts that outlive any single quest
├── quest-template/         # copied into each new quest
├── <repository>/           # the realm's code
└── quests/
    ├── <slug>/
    │   ├── QUEST.md        # the record; the only required file
    │   ├── research/       # findings, read on demand
    │   └── worktrees/
    │       ├── 1/          # a copy-on-write clone of the realm's repository
    │       └── <n>/        # Git worktrees of that clone
    └── .archived/<slug>/
```

A realm is a project set up for quests. It sits outside the repository, so
quests and lore never end up in the code. Each quest's code lives inside the
quest, so removing the quest leaves nothing behind in the repository.

## The `quest` command

`skills/quest/bin/quest` carries out the steps that a program does better than
an agent. So far it has two commands:

- `quest snapshot` commits each quest's records, as described below.
- `quest archive <quest>` checks a quest's checkouts for work that archiving
  would lose. When it finds none, it removes them and moves the quest to
  `.archived/`. With `--check` it only reports.

Run it as `python3 skills/quest/bin/quest`, or link it into your `PATH`.

## Snapshots

`quest snapshot` commits each quest's records to the quest's own Git
repository, so earlier states can be recovered. Code checkouts and private
files are left out. It is meant to run from a harness hook, not by the agent.

For Claude Code, the skill directory is also a plugin. Claude Code loads it
from `~/.claude/skills/quest` as `quest@skills-dir` and runs the hooks in
[`hooks/hooks.json`](skills/quest/hooks/hooks.json) in every session, so there
are no settings to edit. If you added the snapshot hooks to
`~/.claude/settings.json` by hand, remove them.

Other agents need their own hook. See
[Snapshots](skills/quest/references/snapshot.md) for what it must do.

## Requirements

- Git.
- Python 3.10 or newer, for `bin/quest`.
- A filesystem with reflink support (such as Btrfs, XFS, or APFS) for the
  copy-on-write clone. Without it, the first checkout falls back to a Git
  worktree of the realm's repository.

## Tests

```sh
cd skills
python3 -m unittest discover -s quest/tests
```

## License

[MIT](LICENSE)
