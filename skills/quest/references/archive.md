# Archive

## `archive`, `archive current`, or `archive <slug>`

Archive a quest only on explicit request. The request authorizes removing the
quest's checkouts, deleting the local branches they were on in a repository
that outlives the quest, and moving the records to
`<quest-root>/.archived/<slug>`. When the check below finds work that would be
lost, or the quest looks unfinished, the user decides first.

It does not authorize merging, rebasing, committing, stashing, deleting remote
branches, deploying, changing credentials, or stopping processes.

The quest's own `.git`, which holds its record snapshots, moves with it.
Snapshots skip archived quests, so later edits there are not committed.

### 1. Resolve the quest

Resolve the quest root by the skill's rules. With no slug, or `current`, the
session must be inside a quest; otherwise ask for a slug. A slug must name a
quest directory exactly: never guess at a near match for a command that
deletes. Read `QUEST.md` and the realm's instructions. If only
`.archived/<slug>` exists, report that the quest is already archived and change
nothing. When several quests are named, finish steps 2 to 4 for all of them
before removing anything.

### 2. Settle knowledge transfer

Check the record for documentation the quest still owes. Use
[knowledge transfer](distill.md) when findings need a maintained home. A
required gap needs to be closed, or deferred where the realm permits, with a
follow-up recorded somewhere that outlives the quest; other follow-ups can be
recorded without holding the archive up. Make sure what was transferred lives
where cleanup will not remove it, not only in a checkout.

The archive request covers such documentation edits in the quest's realm but
adds no permission to commit, integrate, or publish them. Make them before the
check, so that it sees them.

### 3. Run the check

```sh
python3 <quest-skill-directory>/bin/quest archive --check <quest-directory> \
  [--source <repository>] [--target <branch>]
```

The check needs Python 3.10 or newer and Git 2.38 or newer. It changes nothing
except to fetch the target branch into each repository. It exits 0 with no
findings, 1 with findings, and 2 when it could not finish. After a 2, remove
nothing: fix what it names, or ask the user, and run it again.

It reports, marking each finding with `!`:

- Every checkout in the quest's `worktrees/`, and every worktree that a clone
  there has anywhere else, with its uncommitted and untracked paths.
- Anything in `worktrees/` that is not a checkout.
- For a repository inside the quest, which is removed whole: every local
  branch and detached HEAD whose work is not on the target, and every stash
  entry.
- For a repository outside the quest: the same for what the quest has checked
  out, and the command that removes a worktree from it.
- Processes whose working directory is in a checkout, on systems with `/proc`.

To tell whether a branch's work is on the target, the check rebases a
throwaway copy of it onto the fetched target. A rebase drops commits whose
patch the target has, and commits that change nothing there, so rebased work
leaves nothing behind. Squashed work may not rebase commit by commit, so the
check also tries the branch squashed into one commit. Work is on the target
when either rebase leaves nothing. Otherwise it reports the commits left over,
or a conflict. A conflict can be a false alarm, but it still needs a look.

Pass `--source` when `worktrees/1` is a copy of the realm's repository. A copy
starts with that repository's branches and stashes, and the check leaves out
those that repository still keeps. Pass `--target <remote>/<branch>` when the
work was integrated somewhere other than `origin/main`. Take the target from
the realm's instructions or the pull request. It has to be a branch on a
remote, because anything local goes with the checkout.

The check does not report ignored files, look inside submodules, or search
reflogs. Anything Git ignores that is worth keeping, such as local settings or
QA evidence, belongs in `<quest>/local-data/`, which archiving keeps. Check by
hand any other checkout or branch that `QUEST.md` records as the quest's, and
servers, containers, or databases that use the quest's ports or paths.

### 4. Ask once

Read `Current State` too: active work, next actions, or blockers that are
still open mean the quest may not be finished. When the check has findings or
the record shows open work, put them all to the user in one message and ask
whether to archive anyway. Say that archiving removes the reported work for
good, and that it neither merges the work nor cancels automation on the
remote. With no findings and no open work, go on without asking.

- **Archive anyway** permits forcing the removal of the reported checkouts and
  deleting their unmerged local branches, nothing wider, and nothing on a
  remote. It does not cover a running process: ask the user to stop it.
- **Not yet** leaves everything as it is. If the user wants to keep something
  first, do it as they direct, then run the check again.

### 5. Remove and move

1. Record in `QUEST.md` what will be removed: checkout paths, branches, the
   target and the check's verdict, and what the user chose to lose.
2. Run the check again. Take any finding the user has not seen back to them.
3. Move the session's working directory out of the checkouts.
4. For each worktree of a repository outside the quest, run the removal
   command the check printed, with `--force` only if the user chose to lose
   its uncommitted work. Then delete the branch it was on with `git branch
   -d`. Use `-D` only when `-d` refuses a branch the check reported merged, or
   for one whose work the user chose to lose, and only while its commit is the
   one the check saw. Delete no other branch there, none that another worktree
   uses, and nothing on a remote. Do not run `git worktree prune` or `repair`.
5. For a repository inside the quest, delete the checkout directories the
   check listed, the clone last. Never delete a parent directory, another
   quest's checkout, or storage outside the quest. If a file resists removal,
   as dependencies created by a container can, fix permissions only inside
   that checkout. Remove `worktrees/` once it is empty.
6. Confirm that `.archived/<slug>` is still absent, create `.archived` if
   needed, and move the quest directory there.

If a step fails, stop, and report what was done and what remains. Do not
describe a partial archive as complete.

### 6. Reconcile the record

- Update `Current State` in the archived `QUEST.md`: that the quest is
  archived, what became of each checkout, the check's verdict, anything kept
  and where, any obligation still open, and how to resume. No next action is
  needed. Archiving does not complete an unchecked goal, so leave
  those as they are.
- Repair relative links inside the archive and known links into it. Where a
  source reference is still needed, pin it to a revision or give the
  repository path and revision; mark old absolute checkout paths as historical
  instead of rewriting what was validated there.
- Clear a current-quest pointer or a registered session path in the realm
  only when it selects this quest.
- Verify that the quest is gone from its old path, that the archive holds
  `QUEST.md`, its `.git`, and the retained documents, that the removed
  worktrees and branches are gone, that anything the user kept exists, and
  that nothing else was touched.
- Tell the user the archive path, what was removed, what was kept, and anything
  left incomplete.
