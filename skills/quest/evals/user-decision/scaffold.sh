. "$(dirname "$0")/../_fixture/realm.sh"
make_realm
make_checkout persist-invoices persist-invoices

make_quest persist-invoices <<'EOF'
---
quest_skill_version: "6.0.0"
---

# Save invoices

## Current State

- Objective: Invoices are saved so the reporting team can query them. Done
  when `save_invoice` and `load_invoice` work against the database, with
  tests.
- Constraints: Standard library plus the database driver.
- Workspace: `worktrees/1`, branch `persist-invoices`.
- Active work: the storage module.
- Checkpoint: none yet.
- Next actions: Write `storage.py` with `save_invoice(invoice)` and
  `load_invoice(invoice_id)` on PostgreSQL using `psycopg`, with tests.
- Blockers: none.

## Decisions

- Store invoices in PostgreSQL, the reporting team's shared database (user,
  2026-10-24): reporting queries it directly.
EOF
