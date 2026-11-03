# Quest

An agent skill that gives each task its own directory: a quest. A quest holds
`QUEST.md`, a short record that lets an agent pick the task up again without
the conversation that started it, plus the task's documents and code checkouts.

The skill covers creating, opening, updating, and archiving quests. It does not
prescribe how the work itself is done.

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

**Security scanners.** `npx skills` may show medium-risk warnings for
`quest-master`. They come from two things. Its eval files load the repository's
own test runner and push to a throwaway local repository they create; see
`skills/quest-master/evals/`. And the skill reads subagent reports and can read
the web, which any such skill must trust to some degree. Read the skill and its
evals before installing if you want to check.

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
    │   └── research/       # findings, read on demand
    └── .archived/<slug>/
```

A realm is a project set up for quests. It sits outside the repository, so
quests and lore never end up in the code. Your agent's harness makes a
quest's code checkouts, such as OpenCode's worktrees, wherever it keeps them;
the quest records their paths.

## The `quest` command

`skills/quest/bin/quest` carries out the steps that a program does better than
an agent, and lists quests for other tools, such as a status bar widget:

- `quest world list`, `quest realm list`, and `quest list` print the worlds,
  the realms in them, and their quests, as described below.
- `quest realm show <realm>` and `quest show <realm> <slug>` print one realm
  or quest, with its directory.
- `quest where [<directory>]` prints the quest, quest root, and realm a
  directory is in, looking only upward from it. To look a quest up by slug,
  use `quest list` or `quest show`.
- `quest new <slug> --title <title>` creates a quest: it refuses an invalid
  slug or an existing quest, copies the realm's `quest-template/` in, and
  writes `QUEST.md`.
- `quest archive --check <quest> --checkout <path>` checks a quest's
  checkouts for work that removing them would lose. Once they are removed,
  `quest archive <quest>` moves the quest to `.archived/`.

Run it as `python3 skills/quest/bin/quest`, or link it into your `PATH`.

## OpenCode tools

`plugins/opencode/` is an OpenCode 2 plugin that offers the `quest` command
as tools in OpenCode and OpenChamber sessions: `quest_list`, `quest_open`,
`quest_new`, `quest_archive_check`, `quest_archive`, and `quest_link`. It
runs the installed quest skill's `bin/quest`, so install the skill first,
then the plugin:

```sh
opencode plugin add 'github:david/quest#main::path:plugins/opencode'
```

`quest_link` links a session and its directory, such as a worktree outside
the realm, to a quest. A session that later starts in that directory, or in a
quest's own directory, is told which quest it is on. The plugin needs
`python3` on the server's `PATH`.

`quest_archive` checks the permission action `quest_archive`, with the
quest's directory as the resource. OpenCode allows any action no rule
covers, so to be asked before a quest is archived, add this to your
`opencode.json`:

```json
{ "permissions": [{ "action": "quest_archive", "resource": "*", "effect": "ask" }] }
```

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

## Upgrading from 7.x

Version 8.0.0 drops snapshots: no hook commits quest records any more. A
quest's `.git` from earlier snapshots is left in place; delete it if you no
longer want that history. If you added snapshot hooks to
`~/.claude/settings.json` or another harness by hand, remove them.

## Requirements

- Git.
- Python 3.9 or newer, for `bin/quest`.

## Tests

```sh
cd skills
python3 -m unittest discover -s quest/tests
```

## License

[MIT](LICENSE)
