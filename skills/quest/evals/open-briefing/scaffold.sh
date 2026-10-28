. "$(dirname "$0")/../_fixture/realm.sh"
make_realm
make_checkout export-speed export-speed

quest=$REALM/quests/export-speed
mkdir -p "$quest/research"
cat >"$quest/research/cause.md" <<'EOF'
# Why the yearly export times out

Profiled on 2026-10-21 against a synthetic 20,000-invoice account. The export
builds the whole CSV in memory before sending the first byte; 31 of the 38
seconds are spent there. The query itself takes 2 seconds.
EOF
cat >"$quest/research/timings.md" <<'EOF'
# Export timings

Synthetic 20,000-invoice account, local server, 2026-10-23.

| Version | Time to last byte | Peak memory |
| --- | --- | --- |
| Before (main) | 38 s | 1.9 GB |
| Streaming (a3f9c21) | 4.1 s | 140 MB |
EOF

make_quest export-speed <<'EOF'
---
quest_skill_version: "6.0.0"
---

# Yearly invoice export times out for large accounts

## Current State

- Objective: Customers with many invoices can download their yearly export
  without the request timing out. Done when an export of the largest account
  (about 180,000 invoices) finishes in under 30 seconds.
- Constraints: No schema changes (user). Production data only with the user's
  explicit approval.
- Workspace: `worktrees/1`, branch `export-speed`. Local server on port 8412.
- Active work: validating the streaming export.
- Checkpoint: Streaming export implemented in a3f9c21; unit tests pass at that
  commit. On a synthetic 20,000-invoice account it takes 4.1 s, down from
  38 s ([timings](research/timings.md)). Not yet tried at production size.
- Next actions: Ask the user to approve the full-size trial below. Once
  approved, load an anonymized copy of the largest account and time the
  export.
- Blockers: the approval below.

- [x] Find why the export times out ([cause](research/cause.md)): it builds
  the whole file in memory before sending.
- [x] Stream rows as they are read.
- [ ] Approval: use an anonymized copy of production data for the full-size
  trial.
- [ ] Full-size trial.

## Backlog

- A progress indicator for long exports (deferred by the user).
- The CSV header repeats the `currency` column; a separate issue.

## Decisions

- Stream with a generator rather than paginating the query (agent,
  2026-10-22): fewer round trips. Revisit if memory spikes at full size.
- CSV stays the only export format (user).

## References

- [research/cause.md](research/cause.md): the profiling that found the
  in-memory build.
- [research/timings.md](research/timings.md): timings before and after.
EOF
