# Evals

Cases that check behavior the skill's text is responsible for, so a change to
`SKILL.md` or its guides can be compared with the current version and with no
skill at all. Most run under `claude plugin eval`, built into Claude Code. The
cases in `git/` write Git state, which that harness forbids, so a small runner
of our own runs them.

## Running

```sh
claude plugin eval <checkout>/skills/quest \
  --scaffold --allow-tools Bash Write Edit \
  --model claude-opus-5-5 \
  --output-dir <a directory outside the plugin> \
  --max-cost-usd 40

python3 <checkout>/skills/quest/evals/git/run.py --max-cost-usd 20
```

`--scaffold` runs each case's `scaffold.sh`, which builds the case's realm.
`--allow-tools` lets the agent change files. Both commands run each case three
times with the skill and three times without it, and report both scores and
their difference. `--case <glob>` picks cases in both; `--runs 1` and
`--ablation none` (or `--arms with` for the runner) make a cheap smoke run. A
run costs roughly $0.20 to $0.60. `git/run.py --help` lists its options.

To compare two versions of the skill, run both suites against a checkout of
each and compare the scores with the skill case by case. A shorter skill is
safe where it scores as well as the current one. Cases where the current
skill scores no better than no skill test behavior the skill does not add.

## Layout

- `_fixture/realm.sh` builds a small realm in the run's working directory:
  `AGENTS.md`, `lore/`, `quest-template/`, `quests/`, and `app/`, a Git
  repository of invoicing code with a bare `upstream/app.git` as `origin`. It
  also has helpers that add quests and checkouts. The app's `CLAUDE.md` tells
  agents to leave changes uncommitted, so no `claude plugin eval` case needs
  to commit.
- Each case is a directory with the `scaffold.sh` that adds what the case
  needs to the realm, and `case.yaml`, or `case.json` under `git/`.
- `git/run.py` gives each run a fresh realm under `~/.cache/quest-evals`, runs
  `claude -p` there with only the plugin under test, and grades with shell
  commands (`sh`), the agent's Bash commands (`commands`), its tool calls,
  told apart from its subagents' (`tool_calls`), and a judge model (`llm`).
  The quest-master skill's evals run on it too.

## How `claude plugin eval` constrains the cases

- The agent's shell may not execute `/usr/bin/git`. `realm.sh` copies git and
  its helpers into the run's home and puts them first on the `PATH` through
  `~/.bashrc`.
- Every `.git` is read-only, so the agent cannot commit, clone, fetch, or move
  a repository. Those cases live in `git/`.
- The harness puts an empty Git repository in the run's home, above the
  working directory. The skill would take the realm to be inside a
  repository, so `realm.sh` removes it.
- A session always starts in the run's working directory, so finding the
  quest from inside a quest or a checkout cannot be tested.
- `file_exists` sees only files written during the run; check a file the
  scaffold made with a `regex` on its contents. `tool_used` needs `min: 0`
  for an absence check.
- The judge, haiku by default, gives no reasons and does badly with long
  criteria, so each `llm` grader checks one short claim.

## How the runner isolates a run

Each child `claude -p` loads settings only from the realm
(`--setting-sources project,local`), with CLAUDE.md files and auto memory
turned off and no MCP servers, so your own skills, plugins, and instructions
stay out of both arms. It runs in Claude Code's sandbox with writes confined
to the realm; `allowGitConfig` lets it write `.git/config`, and the fixture's
repositories have no hooks directory, which the sandbox would refuse to copy.
Repositories the agent makes get none either, through `GIT_TEMPLATE_DIR`.
The plugin's hooks run outside the sandbox, as they would in a real session.
