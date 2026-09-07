# Archive

## `archive`, `archive current`, or `archive <slug>`

Archive a quest only on explicit request. With no unresolved findings, this
command authorizes removing clean worktrees and merged local topic branches,
then moving retained records to `<quest-root>/.archived/<slug>`. Dirty worktrees,
unmerged branches, and unmerged commits are **user decision points, not automatic
refusals**. Always ask how to handle each before proceeding. The initial archive
request alone does not authorize discarding work, merging, rebasing, committing,
stashing, remote branch deletion, deployments, credential changes, or stopping
unrelated processes. Additional explicit instructions can authorize scoped local
preservation or discard as described below.

### Resolve and inventory

1. Resolve the quest root using the skill's normal rules. For an omitted slug or
   `current`, require a detected current quest; otherwise ask for a slug. An
   explicit slug must be valid and identify an immediate child of the root with
   a `README.md`. Do not fuzzy-match a destructive command.
2. Read the README first and applicable project/worktree instructions. If only
   the archived destination exists, report already archived without deleting or
   moving anything. If source and destination both exist, stop. Reject symlink
   sources or archive destinations and paths escaping the resolved root. Do not
   overwrite or merge directories.
3. Inventory **all** quest worktrees, not only `work/1`, including registrations
   and any known external worktrees owned by this quest. Resolve each worktree's
   own Git common directory and enumerate its registration; different quest
   worktrees may belong to different repositories. Do not assume one repository
   can remove another's worktree. If ownership, missing registrations, or broken
   Git pointers prevent a complete inventory, stop before deletion.
4. Record each worktree's path, branch, HEAD, repository, intended integration
   target, and a surviving worktree from which to perform Git cleanup. Also
   inventory explicitly quest-owned local topic branches without checkouts.
   Do not infer ownership just from a similar branch name. Preserve default,
   integration, backup/recovery, and shared branches unless separately requested.
   Detached worktrees require merge verification too; include unmerged detached
   commits in the user's preservation/discard decision.
5. Check for active workers, servers, or sessions using these paths. Stop for
   coordination if removal could disrupt ongoing work. Before removal, move the
   executing shell/session outside the target; never strand the current working
   directory inside a deleted checkout. Follow project environment wrappers and
   explicit `git -C <worktree>` rules for every Git command.

### Mandatory read-only preflight

Complete this inspection for **every** target before moving records, preserving
local files, removing any worktree, or deleting any branch. Fetching the target
branch is allowed for verification. For an explicit batch, preflight the entire
batch before starting destructive work.

- **Dirty worktrees:** inspect `git status --porcelain=v1 --untracked-files=all`,
  including staged/unstaged changes, untracked files, and dirty submodules.
  Report affected paths and ask what to preserve or discard. Do not automatically
  stash, commit, clean, reset, skip files, or force removal. Locks and active
  merge/rebase/cherry-pick/revert operations also require a coordination decision;
  never silently unlock or abort them.
- **Merged branches/HEADs:** determine the intended target from explicit project
  or PR evidence (often `origin/main`), not the topic branch's own upstream.
  Fetch that exact target without altering a checkout. If fetching or identifying
  the target fails, report merge status as unknown and ask how to proceed; never
  treat unknown as merged. First try
  `git merge-base --is-ancestor <topic-head> <fetched-target>`.
- **Rebase/squash histories:** lack of ancestry is not proof of unmerged work,
  but a PR marked merged alone is not proof that the current local tip is safe
  to delete. Accept only evidence covering the entire current tip: for example,
  all unique commits patch-equivalent to the fetched target with no omitted
  merge-only changes; or exact tree equality with a verified merged result that
  is reachable from the fetched target. Check merge-only resolutions explicitly
  when using patch equivalence (`git cherry` alone omits them). Extra local
  commits, unmatched patches, uncertain squash equivalence, or a closed-but-not-
  merged PR require the confirmation below. Cover commits not reachable from a
  named branch as well. Never merge or rewrite history just to make archival pass.
  An unavailable repository requires asking for access/recovery or another
  explicit handling plan, not inferring that its contents are disposable.
- **Ignored files:** inspect ignored paths separately; clean Git status does
  not mean all remaining files are disposable. Classify generated dependencies,
  caches, and builds versus local configuration, uploads, logs, or QA evidence.
  Plan to preserve non-reproducible material privately outside the checkout,
  normally under `<quest>/local-data/<worktree-label>/`. If ownership or safe
  treatment is unclear, stop and ask. Never print secret contents. Do not move
  whole directories containing tracked fixtures without separating those tracked
  files first.

No-worktree quests can be archived without Git checks only when inventory also
finds no quest-owned branches requiring verification. An inability to inspect
known Git state is not the same as having no Git work.

### Ask about dirty or unmerged work

If **any worktree is dirty, any branch is unmerged, or any commit is unmerged**
(including local-only or detached commits), pause before archival changes and
ask the user. Also ask when verification is uncertain. Present one consolidated
inventory with paths, branches/HEADs, target, unmatched commits, PR state if known,
and uncertainty. A merged PR does not exempt extra local commits from this check.
Explain that archiving will not merge work or cancel remote automation.

Offer these choices, allowing different treatment for different items:

- **Preserve the work and archive** (recommended): agree on a recoverable local
  preservation method before removing anything. Retain unmerged branches and
  create non-overwriting named recovery refs for detached commits. For dirty
  work, preserve staged and unstaged changes, untracked files, relevant ignored
  files, and submodule changes outside the checkout. A diff alone is not a full
  backup. Verify the preservation and record restore instructions before removal.
  Do not commit or stash unless the user selects that method explicitly.
- **Discard specified work and archive**: request explicit confirmation naming
  the dirty paths/worktrees and unmerged branches/commit tips to be discarded.
  Explain the loss. This scoped authorization may permit forced worktree removal
  or deletion of an unmerged local branch; it is not permission for broad cleanup
  or deleting remote branches. Detached commits may become unreachable, which
  must be included in the confirmation.
- **Defer or cancel archival**: leave everything unchanged for the user to finish
  or handle separately.

Wait for an explicit decision; do not convert these findings into a terminal
refusal or assume that a generic "archive anyway" means discard. If the answer
does not distinguish preservation from loss, clarify. Record the selected scope.
Recheck immediately before cleanup and ask again if paths, status, or commit tips
have changed. A user's decision does not waive higher-priority project rules or
permit deletion of unrelated work.

### Cleanup and move

1. Once preflight is complete and all findings have explicit handling decisions,
   save a concise record: removed checkout paths, branch names/tips, merge
   evidence/target, preservation locations/restore instructions, and any explicit
   discard authorization. Establish and verify promised recovery refs/backups
   before removing any checkout; never rely on reflogs as the only recovery path.
   Archival is not acceptance of unchecked goals or release gates. Do not rewrite
   historical evidence to claim validation that did not occur.
2. Preserve the identified local files without overwriting any existing archive
   material. Restrict access to sensitive local-data directories. Recheck every
   worktree's HEAD/status and branch tips before deletion; stop on concurrent
   changes and ask the user. Do not treat changes caused by your preservation
   step as permission to force removal.
3. From a surviving worktree of the **same repository**, use
   `git worktree remove <exact-target-path>` without force by default. A scoped
   `--force` is allowed only for dirty work whose preservation/removal the user
   approved and whose backup was verified, or whose loss the user explicitly
   approved. Unapproved changes still require asking, not escalation to force.
   Remove worktrees
   **before moving the quest**, avoiding broken absolute or relative `.git`
   pointers. Do not run broad `worktree repair`, `prune`, recursive deletes, or
   unrelated cleanup. If no permitted surviving worktree exists, stop and obtain
   an agreed cleanup location rather than guessing.
4. Delete only inventoried local topic branches that are **verified-merged** or
   explicitly selected for discard, after their worktrees are removed. Keep every
   branch/ref the user chose to preserve, regardless of what `branch -d` would
   allow relative to its upstream. Prefer `git branch -d <branch>`. If it refuses because the surviving
   checkout/upstream differs from the verified integration target or because of
   verified rewritten history, `-D` is permitted **only** with the recorded
   complete merge proof and a rechecked unchanged branch tip. For an unmerged
   branch, `-D` instead requires the user's explicit discard authorization for
   that exact unchanged tip. Otherwise ask before proceeding.
   Never remove a branch still used by another worktree. Do not delete remote
   branches or recreate missing remotes.
5. Recheck that `.archived/<slug>` is absent; create `.archived` if needed, and
   move the quest directory there without replacement. Only remove leftover
   `work/` directories if empty. If a step fails, report what completed and what
   remains; do not continue blindly or describe a partial archive as complete.

### Reconcile and verify

- Update the archived README's Current State: archived, no active worktree,
  preserved branch/merge evidence, and any unresolved obligations. No next task
  is required while intentionally archived; explain how to resume if needed.
- Correct local instructions that still select a removed worktree. Repair
  affected relative links within the archive and known inbound links. Mark old
  absolute worktree paths as historical instead of rewriting validation history.
- Clear a project current-quest pointer only if it selects this quest; preserve
  unrelated selections. Update registered navigation/session paths when the
  project uses them, without changing unrelated entries.
- Verify source absence, destination README and retained artifacts, removal of
   targeted Git registrations/approved branches, existence of every promised
   recovery ref and backup, and repaired links. Keep all unrelated
  quests, worktrees, branches, and remote state untouched.
- Report the archive path, removed worktrees/branches, retained local material,
  and any incomplete steps. Do not claim provider, staging, or production
  validation merely because the quest was archived.
