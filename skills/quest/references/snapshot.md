# Snapshots

`scripts/snapshot.py` commits quest records into each quest's own Git
repository. It needs Python 3.10 or newer and Git, and runs on Linux and macOS.
Resolve it from the loaded `quest` skill directory.

```sh
python3 <quest-skill-directory>/scripts/snapshot.py [directory ...]
```

With no argument it starts from the current directory. It resolves the quest
root by the skill's rules, reading `Quest root:` declarations from `AGENTS.md`
and `CLAUDE.md` in the directory's ancestors. It then snapshots every active
quest directly under that root, not only the current one, so a session started
in the project directory covers the quest it edits. Archived quests are skipped,
and a directory with no quest root is not an error.

For each quest the script:

- creates the quest's `.git` on the first run;
- keeps the required exclusions as the last lines of the quest's `.gitignore`,
  after any rules already there, and adds each nested repository it finds;
- stops recording a file once an ignore rule covers it, keeping the file and
  the snapshots already taken of it;
- stages every other addition, change, and deletion, and commits when anything
  differs from the last snapshot, as in
  `Snapshot quest records: 2 paths (QUEST.md, plan.md)`.

It uses the Git identity and signing configuration already in effect, runs no
commit hooks, and never pushes. Each quest is locked while it is snapshotted,
so concurrent runs are safe, and a run with nothing to record changes nothing.

The script prints one line per commit. A problem goes to standard error with
exit status 1, leaves the records as they were, and is retried by the next run.
The script refuses, rather than repairs, when:

- an enclosing repository tracks files under the quest root, or the quest root
  is itself a repository;
- a quest's `.git` is not an ordinary directory of its own;
- a quest's repository tracks a nested repository.

Report a refusal to the user. Do not untrack or move records to make a snapshot
succeed.

## Running It From A Hook

Have the harness run the script from the session's working directory at two
points: when a turn ends, whether it succeeded or failed, and when a prompt is
submitted. The second catches an interrupted turn and edits made outside the
session. When the harness also knows the directory the session started in, pass
it as a second directory, because the working directory can move or be removed.

Discard standard output where the harness would add it to the model's context.
Make sure a failure cannot block the turn: map any nonzero exit to the status
the harness treats as a warning, and skip the hook when the script is missing.
