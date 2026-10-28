. "$(dirname "$0")/../_fixture/realm.sh"
make_realm
make_checkout add-tax add-tax

make_quest add-tax <<'EOF'
---
quest_skill_version: "6.0.0"
---

# Add tax to invoice totals

## Current State

- Objective: `invoice_total` can add sales tax, so an invoice shows what the
  customer pays. Done when both steps below are finished and tested.
- Constraints: Existing calls keep working, so tax defaults to none (user).
  Standard library only.
- Workspace: `worktrees/1`, branch `add-tax`.
- Active work: step 1.
- Checkpoint: none yet; the plan was agreed with the user on 2026-10-25.
- Next actions:
  1. Add a `tax_rate` keyword argument (a fraction, default 0) to
     `invoice_total`, applied to the subtotal before rounding, with tests.
  2. Add an example with tax to `README.md`.
- Blockers: none.
EOF
