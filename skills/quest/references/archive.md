# Archive

Archive a quest only on explicit request. The request authorizes removing the
quest's checkouts and moving the quest to `<quest-root>/.archived/<slug>`. It
does not authorize merging, rebasing, committing, stashing, deleting remote
branches, deploying, changing credentials, or stopping processes. When work would be lost, or the quest looks unfinished,
the user decides first.

## 1. Resolve the quest

With no slug, or `current`, the session must be inside a quest; otherwise ask
for a slug. A slug must name a quest directory exactly: never guess at a near
match for a command that deletes. If only `.archived/<slug>` exists, say the
quest is already archived and change nothing. Read `QUEST.md` and the realm's
instructions. For several quests, finish steps 2 to 4 for all of them before
removing anything.

## 2. Settle what only the quest holds

Nobody reads an archived quest, so anything left open in it is dropped.

- Write down results, decisions, questions, and plans from the session that
  are still only in chat.
- Move each open item, such as an unchecked Backlog item, deferred scope, a
  check still owed, or a follow-up, to a place still in use: another quest,
  lore, or the repository's docs. If documentation is owed,
  [distill](../SKILL.md#distill) it. Ask the user when no place fits or an
  item may no longer be wanted.
- Have an agent with no session history read only `QUEST.md` and report what
  it leaves out, what is stale, and what it says two ways; a record's author
  reads past its own gaps. Fix what it finds.

Make these edits before the check so that it sees them. The archive request
does not authorize committing or publishing them.

## 3. Run the check

```sh
python3 <quest-skill-directory>/bin/quest archive --check <quest-directory> \
  --checkout <path> ... [--source <repository>] [--target <remote>/<branch>]
```

Pass `--checkout` for each checkout `Current State` records on this computer.
The check needs Python 3.9 and Git 2.38 or newer, and changes nothing except
to fetch the target. It exits 0 with no findings, 1 with findings, each marked
`!`, and 2 when it could not finish. After a 2, remove nothing: fix what it
names, or ask the user, and run it again. It reports uncommitted and untracked
files in every checkout, other worktrees of a clone that removing it would
break, branches and detached heads whose work is not on the target, a clone's
stashes, and processes running in a checkout.

Pass `--source` when a checkout is a copy of another repository, so that what
it inherited from there is skipped. Pass `--target` when the work was
integrated somewhere other than `origin/main`, taking it from the realm's
instructions or the pull request; it must be a branch on a remote.

The check skips ignored files, submodules, and reflogs. Ignored files worth
keeping belong in `<quest>/local-data/`, which archiving keeps. Check by hand
a checkout on another computer, any branch `QUEST.md` records, and services
that use the quest's ports or paths.

## 4. Ask once

Read `Current State` too: open active work, next actions, or blockers mean the
quest may not be finished. When the check has findings or the record shows
open work, put them all to the user in one message and ask whether to archive
anyway. Say that archiving removes the reported work for good, and neither
merges it nor cancels automation on the remote. With no findings and no open
work, go on without asking.

- **Archive anyway** permits removing the reported checkouts with their
  work, nothing wider and nothing on a remote. A running process is the
  user's to stop.
- **Not yet** leaves everything as it is. If the user wants to keep something
  first, do it as they direct, then run the check again.

## 5. Remove and move

1. Record in `QUEST.md` what will be removed: checkout paths, the target and
   the check's verdict, and what the user chose to lose.
2. Move the session's working directory out of the checkouts.
3. Remove each checkout with the tool that made it, such as the harness's
   worktree command, as the realm's instructions say; when you cannot, ask the
   user to remove them, and wait. Checkouts a quest made before version 8.0.0
   are in `<quest>/worktrees/`: remove a worktree of another repository with
   `git worktree remove`, delete the rest, the clone last, then the empty
   `worktrees/`. Remove no checkout the record does not list, and nothing
   on a remote.
4. Move the quest:

   ```sh
   python3 <quest-skill-directory>/bin/quest archive <quest-directory> \
     --checkout <path> ...
   ```

   It refuses while a listed checkout or `<quest>/worktrees/` exists.
   Otherwise it moves the quest to `.archived/<slug>`. It exits 0 when done,
   and 2 when it stopped.

If a step fails, stop and report what was done and what remains. Do not call a
partial archive complete.

## 6. Reconcile the record

- Update `Current State` in the archived `QUEST.md`: that the quest is
  archived, what became of each checkout, the check's verdict, anything kept
  and where, where each open item went, and how to resume. Leave unchecked
  goals unchecked.
- Repair relative links inside the archive and known links into it. Pin a
  source reference still needed to a revision, and mark old checkout paths as
  historical. Clear a realm pointer that selects this quest.
- Verify that the old path is gone, that the archive holds `QUEST.md` and
  the kept documents, that the removed checkouts are gone, and that nothing
  else was touched.
- Tell the user the archive path, what was removed and kept, and anything left
  incomplete.
