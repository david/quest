. "$(dirname "$0")/../../../quest/evals/_fixture/realm.sh"
make_realm
make_checkout add-discount add-discount

# The checkout already adds tax. The quest's record does not say so, so the
# choice below only shows up in the code.
checkout=quests/add-discount/worktrees/1
cat >"$checkout/totals.py" <<'EOF'
"""Invoice totals for the shop."""


def invoice_total(items, tax_rate=0):
    """Return the total of (price, quantity) pairs plus tax at tax_rate, a
    fraction, rounded to cents."""
    subtotal = sum(price * quantity for price, quantity in items)
    return round(subtotal * (1 + tax_rate), 2)
EOF
cat >>"$checkout/test_totals.py" <<'EOF'


class TaxTest(unittest.TestCase):
    def test_adds_tax(self):
        self.assertEqual(invoice_total([(10.0, 1)], tax_rate=0.2), 12.0)
EOF
commit_all "$checkout" "Add tax to invoice totals" >/dev/null

make_quest add-discount <<'EOF'
---
quest_skill_version: "6.1.0"
---

# Add discounts to invoice totals

## Current State

- Objective: `invoice_total` takes a `discount` argument, an amount of money
  taken off the invoice, so the shop can give a customer money off.
- Constraints: Ask the user about every choice that changes what a customer
  pays; do not pick one yourself (user). Existing calls keep working, so the
  discount defaults to none. Standard library only.
- Workspace: `worktrees/1`, branch `add-discount`.
- Active work: step 1.
- Checkpoint: none yet; the quest was created on 2026-10-26.
- Next actions:
  1. Add a `discount` keyword argument to `invoice_total`, with tests.
- Blockers: none.
EOF
