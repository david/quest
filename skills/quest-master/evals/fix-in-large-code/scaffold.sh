. "$(dirname "$0")/../../../quest/evals/_fixture/realm.sh"
make_realm

# The app is the quest command, about 2,000 lines with its tests, so doing the
# work costs real context. It finds nested repositories only two levels deep,
# so a clone at research/vendor/pdfkit breaks snapshots. The existing tests
# nest only two levels, so they still pass.
skill="$FIXTURE_DIR/../.."
git -C app rm -q -r .
mkdir -p app/bin app/assets app/tests
cp "$skill/bin/quest" app/bin/quest
cp "$skill/assets/snapshot-exclude" app/assets/
cp "$skill"/tests/test_*.py app/tests/
python3 - app/bin/quest <<'EOF'
import sys
path = sys.argv[1]
text = open(path).read()
old = "        else:\n            found.extend(nested_repositories(quest, relative))\n"
new = "        elif not prefix:\n            found.extend(nested_repositories(quest, relative))\n"
assert text.count(old) == 1, "the planted bug no longer applies"
open(path, "w").write(text.replace(old, new))
EOF
cat >app/CLAUDE.md <<'EOF'
# quest

`bin/quest` lists quests, snapshots their records, and archives them. Run the
tests with `python3 -m unittest discover -s tests` from the repository root.
Leave changes uncommitted: the user reviews and commits them.
EOF
cat >app/README.md <<'EOF'
# quest

A command that lists worlds, realms, and quests, commits each quest's records
to the quest's own Git repository (`quest snapshot`), and archives a quest
once a check finds nothing to lose (`quest archive`).
EOF
git -C app add -A
git -C app commit -q -m "Replace the invoicing code with the quest command"
git -C app push -q origin main

sed -i 's/`worktrees\/1` is a clone of `.\/app`, the shop'"'"'s invoicing code./`worktrees\/1` is a clone of `.\/app`, the quest command./' AGENTS.md
grep -q 'the quest command' AGENTS.md
make_checkout nested-clone-snapshot nested-clone-snapshot

make_quest nested-clone-snapshot <<'EOF'
---
quest_skill_version: "6.1.0"
---

# Snapshots fail on quests that keep a clone

## Current State

- Objective: `quest snapshot` works on a quest that keeps a Git clone
  anywhere inside it. A user's quest keeps a library's clone at
  `research/vendor/pdfkit`, and every snapshot of it fails with "a nested
  repository appeared while staging; refusing to record it".
- Constraints: Standard library only. Keep the existing tests passing (user).
- Workspace: `worktrees/1`, branch `nested-clone-snapshot`.
- Active work: step 1.
- Checkpoint: none yet; the quest was created on 2026-10-27.
- Next actions:
  1. Find the cause and fix it, with a test that fails without the fix.
- Blockers: none.
EOF
