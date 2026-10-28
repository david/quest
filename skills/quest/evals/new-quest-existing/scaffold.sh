. "$(dirname "$0")/../_fixture/realm.sh"
make_realm
make_quest fix-rounding <<'QUEST'
---
quest_skill_version: "6.0.0"
---

# Invoice totals round half-cents the wrong way

## Current State

- Objective: `invoice_total` rounds half a cent up.
- Constraints: Keep `invoice_total(items)`'s signature (user).
- Workspace: none yet.
- Active work: none.
- Checkpoint: cause found: float `round()` rounds half to even.
- Next actions: Make a checkout and write a failing test for 0.125.
- Blockers: none.
QUEST
