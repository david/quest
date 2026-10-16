# Archive

## `archive`, `archive current`, or `archive <slug>`

Archive a quest only on explicit request. When the check below has no findings,
the request authorizes removing the quest's checkouts, deleting the merged
local branches they were on in a repository that outlives the quest, and moving
the records to `<quest-root>/.archived/<slug>`.

It does not authorize discarding work, merging, rebasing, committing, stashing,
deleting remote branches, deploying, changing credentials, or stopping
processes that are not the quest's. Uncommitted and unmerged work is a decision
for the user, not a reason to refuse and not something to resolve on your own.

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
python3 <quest-skill-directory>/scripts/archive-check.py <quest-directory> \
  [--source <repository>] [--target <branch>]
```

The script needs Python 3.10 or newer and Git 2.38 or newer. It changes nothing
except to fetch the target branch into each repository. It exits 0 with no
findings, 1 with findings, and 2 when it could not finish. After a 2, remove
nothing: fix what it names, or ask the user, and run it again.

It reports, marking each finding with `!`:

- Every checkout in the quest's `worktrees/`, and every worktree that a clone
  there has anywhere else: its uncommitted paths, tracked files that Git was told not
  to watch for changes, submodules, any merge, rebase, or similar operation in
  progress, a lock, and its ignored files.
- For a repository inside the quest, which is removed whole: every local
  branch and detached HEAD not merged into the target, every stash entry, and
  commits that only reflogs or tags still hold.
- For a repository outside the quest: the same merge check for what the quest
  has checked out, commits that only the reflogs of those worktrees and
  branches hold, and the command that removes a worktree from it.
- Processes whose working directory is in a checkout, on systems with `/proc`.

It counts work as merged when the fetched target contains its commits, contains
commits with the same patches, or would not change if the work were merged into
it. That covers rebased and squashed work. It errs towards reporting: work that
cancels itself out, such as a commit and its revert, is reported, and so is
squashed work whose lines the target has since changed again. A merged pull
request is not evidence by itself: what counts is the check's verdict on the
tip as it is now.

Pass `--source` when `worktrees/1` is a copy of the realm's repository. A copy
starts with that repository's branches, stashes, and reflogs, and the script
leaves out whatever that repository still keeps. What it has dropped since is
reported, and is the user's to dismiss. Pass `--target <remote>/<branch>` when
the work was integrated somewhere other than `origin/main`. Take the target
from the realm's instructions or the pull request, not from a branch's
upstream. It has to be a branch on a remote, because anything local goes with
the checkout.

Three things remain yours:

- **Ignored files.** Decide for each listed path whether it can be regenerated,
  as dependencies, caches, and builds can, or cannot, as with local
  configuration, uploads, logs, and QA evidence. Copy what cannot into
  `<quest>/local-data/<checkout>/` before removal, restrict access to anything
  sensitive, and never print a secret. Ask when it is unclear.
- **What the script cannot see.** It looks only at `worktrees/` and at the
  worktrees of clones there, and not inside a submodule it reports. Inspect by hand any
  other checkout or branch that `QUEST.md` records as the quest's, servers,
  containers, and databases that use the quest's ports or paths, and anything
  the quest added to a clone's `.git`, such as hooks. Git state you cannot
  inspect is a finding, not an absence of work.
- **The quest's documents.** Apply the retention test to them too. Doubt about
  whether something is useful is not permission to delete it.

### 4. Ask about every finding

Put all the findings to the user in one message: paths, branches and commits,
the target, and anything uncertain. Say that archiving neither merges the work
nor cancels automation on the remote. Commits that only reflogs hold are
usually earlier versions of commits that were amended or rebased. Say so when
that is what they look like, and still ask. The user can choose differently for
each item:

- **Preserve it and archive** (recommended). Agree on the method first. In a
  repository that outlives the quest, keep the unmerged branch, and give
  detached commits a new named ref. From a clone that will be removed, the
  work has to leave the clone: a ref inside it preserves nothing. For
  uncommitted work, copy staged, unstaged, untracked, and relevant ignored
  files out of the checkout; a diff alone is not a backup. Commit or stash only
  if the user picks that method. Verify the result and record how to restore
  it.
- **Discard it and archive.** Get a confirmation that names the paths,
  branches, and commits to be lost, and say what is lost. It permits forcing
  the removal of those worktrees and deleting those unmerged local branches,
  nothing wider, and nothing on a remote.
- **Defer or cancel.** Leave everything as it is.

Wait for an explicit answer. "Archive anyway" does not say whether to preserve
or discard, so ask which. For a process, a lock, or an operation in progress,
agree with the user what happens to it; do not stop, unlock, or abort it
yourself.

### 5. Remove and move

1. Record in `QUEST.md` what will be removed and why that is safe: checkout
   paths, branches and their commits, the target and the check's verdict, where
   preserved work went and how to restore it, and any discard the user
   confirmed.
2. Carry out the agreed preservation without overwriting anything, and verify
   it.
3. Run the check again. Take anything that differs from what the user decided
   on, other than what the preservation changed, back to the user.
4. Move the session's working directory out of the checkouts.
5. For each worktree of a repository outside the quest, run the removal command
   the check printed, without `--force` unless the user approved losing or
   preserving that worktree's uncommitted work. Then delete the branch it was
   on with `git branch -d` if the check reported it merged. Use `-D` only when
   `-d` refuses such a branch, or for one whose discard the user confirmed, and
   only while its commit is the one the check saw. Delete no other branch
   there, none that another worktree uses, and nothing on a remote. Do not run
   `git worktree prune` or `repair`.
6. For a repository inside the quest, delete the checkout directories the check
   listed, the clone last. A clean, merged clone needs no backup first. Never
   delete a parent directory, another quest's checkout, or storage outside the
   quest. If a file resists removal, as dependencies created by a container
   can, fix permissions only inside that checkout. Remove `worktrees/` once it
   is empty. A clone the user wants kept moves with the quest as an inactive
   recovery checkout: take its other worktrees away with `git worktree remove`
   instead of deleting their directories.
7. Confirm that `.archived/<slug>` is still absent, create `.archived` if
   needed, and move the quest directory there.

If a step fails, stop, and report what was done and what remains. Do not
describe a partial archive as complete.

### 6. Reconcile the record

- Update `Current State` in the archived `QUEST.md`: that the quest is
  archived, what became of each checkout, the merge evidence, what was
  preserved and where, any obligation still open, and how to resume. No next
  action is needed. Archiving does not complete an unchecked goal, so leave
  those as they are.
- Repair relative links inside the archive and known links into it. Where a
  source reference is still needed, pin it to a revision or give the
  repository path and revision; mark old absolute checkout paths as historical
  instead of rewriting what was validated there.
- Clear a current-quest pointer or a registered session path in the realm
  only when it selects this quest.
- Verify that the quest is gone from its old path, that the archive holds
  `QUEST.md`, its `.git`, and the retained documents, that the removed
  worktrees and branches are gone, that every promised preservation exists, and
  that nothing else was touched.
- Tell the user the archive path, what was removed, what was kept, and anything
  left incomplete.
