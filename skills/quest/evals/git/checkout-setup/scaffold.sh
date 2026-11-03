. "$(dirname "$0")/../../_fixture/realm.sh"
make_realm

# Upstream has a commit that ./app has not pulled, so a checkout made without
# updating main first lacks CHANGELOG.md.
changes=$(mktemp -d)
printf '# Changelog\n\n- Totals are rounded to cents.\n' >"$changes/CHANGELOG.md"
upstream_commit "$changes" "Start a changelog"
rm -rf "$changes"

make_quest add-currency <<'EOF'
---
quest_skill_version: "6.0.0"
---

# Currency on invoices

## Current State

- Objective: Each invoice records its currency, and totals refuse to mix
  currencies.
- Constraints: Standard library only.
- Workspace: none yet.
- Active work: none.
- Checkpoint: quest created.
- Next actions: Set up the checkout, then add a `currency` argument to
  `invoice_total`.
- Blockers: none.
EOF
