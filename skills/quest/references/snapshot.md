# Snapshots

`quest snapshot` commits quest records into each quest's own Git repository.
`quest` is `bin/quest` in the loaded `quest` skill directory. It needs Python
3.10 or newer and Git, and runs on Linux and macOS.

```sh
python3 <quest-skill-directory>/bin/quest snapshot [directory ...]
```

With no argument it starts from the current directory. It resolves the quest
root by the skill's rules, reading `Quest root:` declarations from `AGENTS.md`
and `CLAUDE.md` in the directory's ancestors. It then snapshots every active
quest directly under that root, not only the current one, so a session started
in the realm covers the quest it edits. Archived quests are skipped,
and a directory with no quest root is not an error.

For each quest the command:

- creates the quest's `.git` on the first run;
- writes the default rules in `assets/snapshot-exclude`, and a rule for each
  nested repository it finds, to the quest's `.git/info/exclude`, replacing
  whatever is there;
- stops recording a file once an ignore rule covers it, keeping the file and
  the snapshots already taken of it;
- stages every other addition, change, and deletion, and commits when anything
  differs from the last snapshot, as in
  `Snapshot quest records: 2 paths (QUEST.md, plan.md)`.

To change what every quest leaves out, edit `assets/snapshot-exclude`. A quest's
own rules go in its `.gitignore`, which the command never edits and which can
override a default.

It uses the Git identity and signing configuration already in effect, runs no
commit hooks, and never pushes. Each quest is locked while it is snapshotted,
so concurrent runs are safe, and a run with nothing to record changes nothing.

The command prints one line per commit. A problem goes to standard error with
exit status 1, leaves the records as they were, and is retried by the next run.
The command refuses, rather than repairs, when:

- the quest root is inside a repository, or is one itself;
- a quest's `.git` is not an ordinary directory of its own;
- a quest's repository tracks a nested repository.

Report a refusal to the user. Do not untrack or move records to make a snapshot
succeed.

## Running It From A Hook

Claude Code needs no setup: the skill directory is a plugin, and
`hooks/hooks.json` holds these hooks. Another harness needs its own.

Have the harness run the command from the session's working directory at two
points: when a turn ends, whether it succeeded or failed, and when a prompt is
submitted. The second catches an interrupted turn and edits made outside the
session. When the harness also knows the directory the session started in, pass
it as a second directory, because the working directory can move or be removed.

Discard standard output where the harness would add it to the model's context.
Make sure a failure cannot block the turn: map any nonzero exit to the status
the harness treats as a warning, and skip the hook when `bin/quest` is missing.
