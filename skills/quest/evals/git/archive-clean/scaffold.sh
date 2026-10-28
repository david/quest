. "$(dirname "$0")/../../_fixture/realm.sh"
make_realm
make_checkout readme-title readme-title

checkout=$REALM/quests/readme-title/worktrees/1
sed -i 's/^# Invoicing$/# Shop invoicing/' "$checkout/README.md"
sha=$(commit_all "$checkout" "Name the shop in the README title")
git -C "$checkout" push -q origin readme-title:main

make_quest readme-title <<EOF
---
quest_skill_version: "6.0.0"
---

# Name the shop in the README

## Current State

- Objective: The README's title names the shop.
- Constraints: none beyond the repository's.
- Workspace: \`worktrees/1\`, branch \`readme-title\`.
- Active work: none.
- Checkpoint: $sha is on origin/main.
- Next actions: none; the work is complete and merged.
- Blockers: none.
EOF
