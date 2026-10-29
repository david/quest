# Snapshots

```sh
python3 <quest-skill-directory>/bin/quest snapshot [--quest <directory>] [directory ...]
```

`quest snapshot` needs Python 3.9 or newer and Git, on Linux or macOS. From
each directory given, or else the current one, it resolves the quest root by
the skill's rules and snapshots every active quest directly under it, so a
session started in the realm covers the quest it edits. It skips archived
quests, and finding no root is not an error. `--quest <directory>`, which
can repeat, commits that quest's records too, even an archived one; with only
`--quest`, nothing else is resolved.

For each quest it creates `.git` on the first run, and writes the rules in
`assets/snapshot-exclude`, plus one for each nested repository, to
`.git/info/exclude`. It stops recording a file once an ignore rule covers it,
keeping the file and its earlier snapshots, and commits every other change
since the last snapshot. Defaults for every quest go in
`assets/snapshot-exclude`; one quest's own rules go in its `.gitignore`, which
the command never edits.

It uses the Git identity and signing already configured, runs no commit hooks,
never pushes, and locks each quest, so concurrent runs are safe. It prints one
line per commit. A problem goes to standard error with exit status 1, leaves
the records as they were, and is retried by the next run. It refuses, rather
than repairs, a quest root that is inside a repository or is one, a quest
`.git` that is not an ordinary directory, and a quest repository that tracks a
nested repository. Report a refusal to the user; do not untrack or move
records to get past it.

## Running It From A Hook

In Claude Code the skill directory is a plugin whose `hooks/hooks.json` does
this. Another harness needs its own hook that runs the command from the
session's working directory when a turn ends, whether or not it succeeded, and
when a prompt is submitted, which catches interrupted turns and edits made
outside the session. When the harness knows the directory the session started
in, pass it as a second directory, because the working directory can move or
be removed. Keep the output out of the model's context, map any nonzero exit
to a warning so that it never blocks a turn, and skip the hook when
`bin/quest` is missing.
