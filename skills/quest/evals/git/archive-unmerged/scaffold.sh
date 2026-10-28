. "$(dirname "$0")/../../_fixture/realm.sh"
make_realm
make_checkout discount-codes discount-codes

checkout=$REALM/quests/discount-codes/worktrees/1
cat >"$checkout/discounts.py" <<'EOF'
"""Percentage discount codes."""

CODES = {"WELCOME10": 10, "LOYAL15": 15}


def apply_code(total, code):
    """Return the total after the code's percentage discount."""
    return round(total * (100 - CODES.get(code, 0)) / 100, 2)
EOF
sha=$(commit_all "$checkout" "Add percentage discount codes")

make_quest discount-codes <<EOF
---
quest_skill_version: "6.0.0"
---

# Discount codes

## Current State

- Objective: Customers can apply a percentage discount code to an invoice.
- Constraints: none beyond the repository's.
- Workspace: \`worktrees/1\`, branch \`discount-codes\`.
- Active work: none.
- Checkpoint: \`apply_code\` implemented in $sha; tests pass at that commit.
- Next actions: none; the work is complete.
- Blockers: none.
EOF
