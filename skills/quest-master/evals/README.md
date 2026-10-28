# Evals

Cases that check what quest-master adds to the quest skill: the master keeps
the record, and its subagents do the work in the checkouts. Each case runs
with the quest and quest-master plugins, and with the quest plugin alone.

## Running

```sh
python3 <checkout>/skills/quest-master/evals/run.py --max-cost-usd 40
```

The runner is the quest skill's own, in `../../quest/evals/git/run.py`, and
takes the same options; see [its README](../../quest/evals/README.md). Runs
cost more than the quest skill's, because each one starts subagents.

Besides the scores, the runner reports the main agent's peak context for
each case and arm, which is what quest-master is meant to keep small.

## Layout

- Each case is a directory with `scaffold.sh`, which builds the quest skill's
  fixture realm and adds the case's quest, and `case.json`. A case's prompt
  is given per arm, because only the "with" arm has `/quest-master`.
- `tool_calls` graders tell the main agent's calls from its subagents'.
  `master-stays-out-of-worktrees` allows the main agent to read a checkout's
  `CLAUDE.md`, `AGENTS.md`, and `README.md`, and nothing else in it.
