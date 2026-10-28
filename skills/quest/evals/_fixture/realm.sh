# Shared fixture for the quest skill's eval cases. A case's scaffold sources
# this file and calls make_realm, then adds the quests the case needs.
#
# The harness runs a scaffold with bash, in the run's working directory, with
# HOME set to the run's own home. The realm is built in the working directory
# itself, because that is where the agent's session starts.

set -euo pipefail

FIXTURE_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REALM=$PWD

# The harness puts an empty Git repository in the run's home, an ancestor of
# the working directory. The skill treats any quest root below a repository as
# misplaced, so remove it. Guard against running anywhere but a run's home.
drop_home_repo() {
  if [ "$(basename "$HOME")" = home ] && [ -f "$HOME/.git/commondir" ] &&
    [ "${REALM#"$HOME"/}" != "$REALM" ]; then
    rm -rf "$HOME/.git"
  fi
}

# The run's sandbox refuses to execute /usr/bin/git, and the cases need git
# the way a real session has it. Copy git and its helpers into the run's home
# and put them first on the PATH of the agent's shell, which reads ~/.bashrc.
# The user chose this on 2026-10-27. The cases in git/ run under their own
# runner, which needs none of it.
provide_git() {
  [ -z "${QUEST_EVAL_OWN_RUNNER:-}" ] || return 0
  mkdir -p "$HOME/.local/bin" "$HOME/.local/libexec"
  cp "$(command -v git)" "$HOME/.local/bin/git"
  cp -a "$(git --exec-path)" "$HOME/.local/libexec/git-core"
  cat >>"$HOME/.bashrc" <<'RC'
export PATH="$HOME/.local/bin:$PATH"
export GIT_EXEC_PATH="$HOME/.local/libexec/git-core"
RC
}

# The realm: AGENTS.md, an empty lore/, a quest template, quests/, the app's
# repository on main, and a bare upstream the repository tracks as origin.
make_realm() {
  drop_home_repo
  provide_git
  mkdir -p "$REALM/lore" "$REALM/quests" "$REALM/quest-template/research" \
    "$REALM/upstream"
  cp "$FIXTURE_DIR/realm/AGENTS.md" "$REALM/AGENTS.md"
  cp "$FIXTURE_DIR/realm/quest-template/research/README.md" \
    "$REALM/quest-template/research/README.md"

  # No hooks directory: the runner's sandbox refuses writes to one, so a
  # copy of a repository that has it would fail.
  git init -q -b main --template= "$REALM/app"
  cp -a "$FIXTURE_DIR/app/." "$REALM/app/"
  git -C "$REALM/app" add -A
  git -C "$REALM/app" commit -q -m "Initial invoice totals"
  git init -q --bare -b main --template= "$REALM/upstream/app.git"
  git -C "$REALM/app" remote add origin "$REALM/upstream/app.git"
  git -C "$REALM/app" push -q -u origin main
}

# A quest directory with QUEST.md read from standard input.
make_quest() {
  local slug=$1
  mkdir -p "$REALM/quests/$slug"
  cat >"$REALM/quests/$slug/QUEST.md"
}

# The quest's worktrees/1, made the way the skill makes it, on a new branch.
make_checkout() {
  local slug=$1 branch=$2 checkout="$REALM/quests/$1/worktrees/1"
  mkdir -p "$REALM/quests/$slug/worktrees"
  cp -a "$REALM/app" "$checkout"
  rm -rf "$checkout/.git/worktrees"
  git -C "$checkout" switch -q -c "$branch"
}

# Commit everything in a checkout and print the short hash.
commit_all() {
  local checkout=$1 message=$2
  git -C "$checkout" add -A
  git -C "$checkout" commit -q -m "$message"
  git -C "$checkout" rev-parse --short HEAD
}

# A commit on upstream's main that ./app has not pulled yet. Reads the
# commit's files from a directory given as the first argument.
upstream_commit() {
  local files=$1 message=$2 tmp
  tmp=$(mktemp -d)
  git clone -q "$REALM/upstream/app.git" "$tmp/app"
  cp -a "$files/." "$tmp/app/"
  git -C "$tmp/app" add -A
  git -C "$tmp/app" commit -q -m "$message"
  git -C "$tmp/app" push -q origin main
  rm -rf "$tmp"
}
