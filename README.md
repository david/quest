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
ln -s "$PWD/quest/skills/quest-master" ~/.claude/skills/quest-master
```

Then set up a project with `/quest realm init`. This makes it a realm: it creates
the quest root, a directory named `quests` beside the project repository, and
a quest setup section in the project's `AGENTS.md`. It also creates a
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
| `distill` | Move findings into the realm's own documentation. |
| `archive` | Archive a quest after checking its checkouts for unmerged work. |

Commands can also be asked for in plain language.

## Quest master

`/quest-master` loads the quest skill and makes the session the master of a
quest: your one point of contact for it. The session keeps the quest's
records and lore, and hands all work in the quest's checkouts to subagents.
Subagents may read the quest's files but never write them; they report to
the master, which updates the record and brings their questions to you. This
lasts for the rest of the session. Pass a quest command to start with it, as
in `/quest-master open <slug>`.

## Layout

```text
<realm>/
├── AGENTS.md               # sets up quests and lists the lore
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
an agent, and lists quests for other tools, such as a status bar widget:

- `quest world list`, `quest realm list`, and `quest list` print the worlds,
  the realms in them, and their quests, as described below.
- `quest realm show <realm>` and `quest show <realm> <slug>` print one realm
  or quest, with its directory.
- `quest snapshot` commits each quest's records, as described below.
- `quest archive <quest>` checks a quest's checkouts for work that archiving
  would lose. When it finds none, it removes them and moves the quest to
  `.archived/`. With `--check` it only reports.

Run it as `python3 skills/quest/bin/quest`, or link it into your `PATH`.

## Worlds

A world is a directory of realms, on this computer or on another host. List
yours in `~/.config/quest/worlds.json`:

```json
[
  { "host": "devbox", "path": "/home/me/Projects" },
  { "path": "~/Projects" }
]
```

Leave out the host, or give this computer's name, for a world here; a
relative path starts at the home directory. Without the file, the one world is
`~/Projects` here. `--world [<host>:]<path>` lists another world instead.

Every directory in a world is a realm, except a hidden one. Its quests are in
its `quests` directory, if it has one. The listing commands print JSON and
include the worlds and realms that could not be listed. For a world on another host, `quest` runs itself
there over `ssh`, sending its own code, so that host needs only `python3` and
`ssh <host>` must work without a prompt.

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
- Python 3.9 or newer, for `bin/quest`.
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
