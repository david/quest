. "$(dirname "$0")/../_fixture/realm.sh"
make_realm
make_checkout fix-rounding fix-rounding

checkout=$REALM/quests/fix-rounding/worktrees/1
python3 - "$checkout/test_totals.py" <<'EOF'
import sys
path = sys.argv[1]
text = open(path).read()
test = '''
    def test_rounds_half_up(self):
        self.assertEqual(invoice_total([(0.125, 1)]), 0.13)
        self.assertEqual(invoice_total([(1.005, 1)]), 1.01)
'''
marker = '\n\nif __name__ == "__main__":'
open(path, "w").write(text.replace(marker, test + marker, 1))
EOF
sha=$(commit_all "$checkout" "Add failing test for half-cent rounding")

make_quest fix-rounding <<EOF
---
quest_skill_version: "6.0.0"
---

# Invoice totals round half-cents the wrong way

## Current State

- Objective: \`invoice_total\` rounds half a cent up, as customers expect:
  0.125 becomes 0.13 and 1.005 becomes 1.01. Done when the rounding test
  passes along with the existing tests.
- Constraints: Keep \`invoice_total(items)\`'s signature and keep returning a
  float (user's decision). Standard library only.
- Workspace: \`worktrees/1\`, branch \`fix-rounding\`.
- Active work: the fix.
- Checkpoint: \`test_rounds_half_up\` added in $sha. At that commit it fails
  (0.12 instead of 0.13) and the other tests pass. Cause: \`round()\` on floats
  rounds half to even and cannot see an exact half cent.
- Next actions: Compute the total with \`decimal.Decimal\` built from each
  price's string form, quantize to cents with \`ROUND_HALF_UP\`, return it as a
  float, then run the tests.
- Blockers: none.

## Decisions

- Use \`decimal\` rather than adding a small epsilon before rounding (user,
  2026-10-20): an epsilon fixes these values and breaks others.
- Rejected: integer cents throughout, because it changes the public API.
EOF
