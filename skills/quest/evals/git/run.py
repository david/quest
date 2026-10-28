#!/usr/bin/env python3
"""Run the quest skill's eval cases that write Git state.

`claude plugin eval` makes every `.git` read-only, so a case that commits,
clones, or archives cannot run there. This runner gives each run a fresh
realm, starts `claude -p` in it with only the plugin under test (or nothing,
for the baseline), and grades the result with real Git commands.

Each child runs in Claude Code's own sandbox, which confines its writes to
the realm. The user's settings, skills, CLAUDE.md files, memory, and MCP
servers are left out, so both arms see the same environment apart from the
plugin.
"""

import argparse
import concurrent.futures
import fnmatch
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
from pathlib import Path

HERE = Path(__file__).resolve().parent
PLUGIN = HERE.parent.parent
TOOLS = ["Read", "Glob", "Grep", "Skill", "Bash", "Write", "Edit"]
SANDBOX = {
    "sandbox": {
        "enabled": True,
        "failIfUnavailable": True,
        "autoAllowBashIfSandboxed": True,
        "allowUnsandboxedCommands": False,
        "filesystem": {"allowGitConfig": True},
    }
}
ISOLATION_ENV = {
    "CLAUDE_CODE_DISABLE_CLAUDE_MDS": "1",
    "CLAUDE_CODE_DISABLE_AUTO_MEMORY": "1",
}
JUDGE_VOTES = 3


def main(cases_dir=HERE, plugins=None, tools=TOOLS, description=None):
    """Run the cases in cases_dir. plugins maps each arm to the plugin
    directories it loads; by default only the "with" arm loads this skill."""
    parser = argparse.ArgumentParser(description=description or __doc__.splitlines()[0])
    parser.add_argument("--case", default="*", help="glob over case names")
    parser.add_argument("--runs", type=int, help="runs per arm (default: the case's, else 3)")
    parser.add_argument("--arms", default="with,without", help="with, without, or both")
    parser.add_argument("--model", default="claude-opus-5-5")
    parser.add_argument("--judge-model", default="haiku")
    parser.add_argument("-j", "--concurrency", type=int, default=1)
    parser.add_argument("--max-cost-usd", type=float)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "quest-evals",
        help="where runs are made; it must support reflinks for the skill's default checkout",
    )
    parser.add_argument("--keep", action="store_true", help="keep each run's directory")
    parser.add_argument("--output", type=Path, help="write all results as JSON here")
    args = parser.parse_args()
    args.plugins = plugins or {"with": [PLUGIN], "without": []}
    args.tools = tools

    cases = [
        load_case(path.parent)
        for path in sorted(Path(cases_dir).glob("*/case.json"))
        if fnmatch.fnmatch(path.parent.name, args.case)
    ]
    if not cases:
        sys.exit(f"no case matches {args.case!r}")
    arms = [arm.strip() for arm in args.arms.split(",") if arm.strip()]
    args.root.mkdir(parents=True, exist_ok=True)

    jobs = [
        (case, arm, index)
        for case in cases
        for arm in arms
        for index in range(args.runs or case.get("runs", 3))
    ]
    spent = Spent(args.max_cost_usd)
    with concurrent.futures.ThreadPoolExecutor(args.concurrency) as pool:
        futures = [pool.submit(run_job, job, args, spent) for job in jobs]
        results = [future.result() for future in futures]
    results = [result for result in results if result is not None]

    report(cases, arms, results, spent.total)
    if args.output:
        args.output.write_text(json.dumps(results, indent=2))


def load_case(directory):
    case = json.loads((directory / "case.json").read_text())
    case["dir"] = directory
    return case


class Spent:
    def __init__(self, ceiling):
        self.ceiling = ceiling
        self.total = 0.0
        self.lock = threading.Lock()

    def add(self, cost):
        with self.lock:
            self.total += cost

    def exhausted(self):
        with self.lock:
            return self.ceiling is not None and self.total >= self.ceiling


def run_job(job, args, spent):
    case, arm, index = job
    if spent.exhausted():
        print(f"  {case['name']} [{arm}] run {index + 1}: skipped, cost ceiling reached")
        return None
    result = run_once(case, arm, args, spent)
    lines = [
        f"  {case['name']} [{arm}] run {index + 1}: score {result['score']:.2f}  "
        f"${result['cost']:.2f}  main context {result.get('main_context', 0):,}"
    ]
    if result.get("error"):
        lines.append(f"    ! {result['error']}")
    for grade in result["graders"]:
        mark = "✓" if grade["passed"] else "✗"
        note = "" if grade["scored"] else " [indicator]"
        lines.append(f"    {mark} {grade['name']}{note}: {grade['detail']}")
    if result.get("dir"):
        lines.append(f"    kept: {result['dir']}")
    print("\n".join(lines), flush=True)
    return result


def run_once(case, arm, args, spent):
    run = Path(tempfile.mkdtemp(prefix="run-", dir=args.root))
    home, template = run / "home", run / "git-template"
    cwd = home / "cwd"
    cwd.mkdir(parents=True)
    template.mkdir()
    (home / ".gitconfig").write_text(
        "[user]\n\tname = Plugin Eval\n\temail = eval@example.invalid\n"
    )
    scaffold_env = {
        "PATH": os.environ["PATH"],
        "HOME": str(home),
        "TMPDIR": str(run),
        "GIT_CONFIG_NOSYSTEM": "1",
        "QUEST_EVAL_OWN_RUNNER": "1",
    }
    result = {
        "case": case["name"], "arm": arm, "score": 0.0, "cost": 0.0, "main_context": 0, "graders": [],
    }
    try:
        scaffold = subprocess.run(
            ["bash", str(case["dir"] / "scaffold.sh")],
            cwd=cwd, env=scaffold_env, capture_output=True, text=True, timeout=120,
        )
        if scaffold.returncode != 0:
            result["error"] = f"scaffold failed: {scaffold.stderr.strip()[-500:]}"
            return result

        prompt = case["prompt"]
        if isinstance(prompt, dict):
            prompt = prompt[arm]
        command = [
            "claude", "-p", prompt,
            "--allowed-tools", *args.tools,
            "--setting-sources", "project,local",
            "--settings", json.dumps(SANDBOX),
            "--strict-mcp-config",
            "--permission-mode", "acceptEdits",
            "--output-format", "stream-json", "--verbose",
            "--max-turns", str(case.get("max_turns", 40)),
            "--model", args.model,
            "--no-session-persistence",
        ]
        for plugin in args.plugins.get(arm, []):
            command += ["--plugin-dir", str(plugin)]
        # Repositories made inside the run get no hooks, which the sandbox
        # would refuse to write.
        env = {**os.environ, **ISOLATION_ENV, "GIT_TEMPLATE_DIR": str(template)}
        try:
            agent = subprocess.run(
                command, cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                capture_output=True, text=True,
                timeout=case.get("timeout_seconds", 900),
            )
            stdout = agent.stdout
        except subprocess.TimeoutExpired as timeout:
            stdout = timeout.stdout or ""
            if isinstance(stdout, bytes):
                stdout = stdout.decode(errors="replace")
            result["error"] = "agent timed out"
        (run / "trace.jsonl").write_text(stdout)
        trace = parse_trace(stdout)
        result["cost"] = trace["cost"]
        result["main_context"] = trace["main_context"]
        spent.add(trace["cost"])

        context = {"cwd": cwd, "env": scaffold_env, "trace": trace, "args": args, "run": run}
        for grader in case["graders"]:
            # Whether the skill fired is an indicator for the skill's arm,
            # not part of the score, as in `claude plugin eval`.
            if grader["type"] == "skill" and arm != "with":
                continue
            if arm not in grader.get("arms", [arm]):
                continue
            grade = GRADERS[grader["type"]](grader, context)
            scored = grader["type"] != "skill" and not grader.get("indicator")
            result["graders"].append({"name": grader["name"], "scored": scored, **grade})
        scored = [grade for grade in result["graders"] if grade["scored"]]
        result["score"] = sum(grade["passed"] for grade in scored) / len(scored) if scored else 0.0
        result["last_message"] = trace["last_message"]
        return result
    finally:
        if args.keep:
            result["dir"] = str(run)
        else:
            shutil.rmtree(run, ignore_errors=True)


def parse_trace(stdout):
    """Tool calls, cost, the main agent's last message, and its peak context.
    A subagent's events carry the id of the Agent call that started it."""
    trace = {
        "last_message": "", "commands": [], "tools": [], "calls": [],
        "cost": 0.0, "main_context": 0,
    }
    for line in stdout.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "assistant":
            agent = "sub" if event.get("parent_tool_use_id") else "main"
            message = event.get("message", {})
            for block in message.get("content", []):
                if block.get("type") == "tool_use":
                    trace["tools"].append(block["name"])
                    trace["calls"].append(
                        {"agent": agent, "name": block["name"], "input": block.get("input", {})}
                    )
                    if block["name"] == "Bash":
                        trace["commands"].append(block["input"].get("command", ""))
                elif block.get("type") == "text" and agent == "main":
                    trace["last_message"] = block["text"]
            if agent == "main":
                usage = message.get("usage") or {}
                context = sum(
                    usage.get(key) or 0
                    for key in ("input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens")
                )
                trace["main_context"] = max(trace["main_context"], context)
        elif event.get("type") == "result":
            trace["cost"] = event.get("total_cost_usd") or 0.0
            if event.get("result"):
                trace["last_message"] = event["result"]
    return trace


def grade_sh(grader, context):
    check = subprocess.run(
        ["bash", "-c", grader["run"]], cwd=context["cwd"], env=context["env"],
        capture_output=True, text=True, timeout=60,
    )
    detail = "ok" if check.returncode == 0 else (check.stdout + check.stderr).strip()[-300:] or f"exit {check.returncode}"
    return {"passed": check.returncode == 0, "detail": detail}


def grade_commands(grader, context):
    pattern = re.compile(grader["pattern"])
    hits = [command for command in context["trace"]["commands"] if pattern.search(command)]
    if grader.get("match", "contains") == "not_contains":
        return {"passed": not hits, "detail": "none matched" if not hits else f"matched: {hits[0][:200]}"}
    return {"passed": bool(hits), "detail": f"{len(hits)} matched"}


def grade_tool_calls(grader, context):
    """Calls by the main agent or its subagents (agent), to the named tools,
    whose input fields (all of the input by default) match pattern."""
    pattern = re.compile(grader.get("pattern", ""))
    fields = grader.get("fields")
    hits = []
    for call in context["trace"]["calls"]:
        if grader.get("agent", call["agent"]) != call["agent"]:
            continue
        if call["name"] not in grader.get("tools", [call["name"]]):
            continue
        if fields:
            text = "\n".join(str(call["input"].get(field, "")) for field in fields)
        else:
            text = json.dumps(call["input"])
        if pattern.search(text):
            hits.append(f"{call['name']} {text[:200]}")
    if grader.get("match", "contains") == "not_contains":
        return {"passed": not hits, "detail": "none matched" if not hits else f"matched: {hits[0]}"}
    return {"passed": bool(hits), "detail": f"{len(hits)} matched"}


def grade_skill(grader, context):
    count = context["trace"]["tools"].count("Skill")
    return {"passed": count > 0, "detail": f"Skill called {count}x"}


def grade_llm(grader, context):
    focus = grader.get("focus", "last_message")
    if focus == "last_message":
        content = context["trace"]["last_message"]
    else:
        path = context["cwd"] / focus["file"]
        if not path.is_file():
            return {"passed": False, "detail": f"{focus['file']} does not exist"}
        content = path.read_text()
    prompt = (
        "You are grading one output of an AI agent against a criterion. Judge "
        "only what the content shows.\n\n"
        f"Criterion:\n{grader['criteria'].strip()}\n\n"
        f"Content:\n<<<\n{content}\n>>>\n\n"
        "Reply with PASS or FAIL on the first line, then one sentence saying why."
    )
    votes, reasons = [], []
    for _ in range(JUDGE_VOTES):
        judge = subprocess.run(
            [
                "claude", "-p", prompt,
                "--model", context["args"].judge_model,
                "--setting-sources", "project",
                "--strict-mcp-config",
                "--disable-slash-commands",
                "--tools", "",
                "--max-turns", "1",
                "--no-session-persistence",
            ],
            cwd=context["run"], env={**os.environ, **ISOLATION_ENV}, stdin=subprocess.DEVNULL,
            capture_output=True, text=True, timeout=180,
        )
        answer = judge.stdout.strip()
        votes.append(answer.upper().startswith("PASS"))
        reasons.append(" ".join(answer.splitlines()[1:])[:200])
    passed = sum(votes) * 2 > len(votes)
    tally = " ".join("PASS" if vote else "FAIL" for vote in votes)
    reason = next((r for v, r in zip(votes, reasons) if v == passed and r), "")
    return {"passed": passed, "detail": f"judge votes: {tally}. {reason}".strip()}


GRADERS = {
    "sh": grade_sh,
    "commands": grade_commands,
    "tool_calls": grade_tool_calls,
    "skill": grade_skill,
    "llm": grade_llm,
}


def report(cases, arms, results, total):
    print()
    header = f"{'CASE':<20}" + "".join(f"{arm.upper():>9}" for arm in arms)
    if set(arms) == {"with", "without"}:
        header += f"{'Δ':>9}"
    print(header)
    for case in cases:
        scores = {}
        for arm in arms:
            runs = [r["score"] for r in results if r["case"] == case["name"] and r["arm"] == arm]
            scores[arm] = sum(runs) / len(runs) if runs else None
        line = f"{case['name']:<20}" + "".join(
            f"{scores[arm]:>9.2f}" if scores[arm] is not None else f"{'-':>9}" for arm in arms
        )
        if set(arms) == {"with", "without"} and None not in scores.values():
            line += f"{scores['with'] - scores['without']:>+9.2f}"
        print(line)
    print(f"\n{'MAIN CONTEXT':<20}" + "".join(f"{arm.upper():>9}" for arm in arms))
    for case in cases:
        line = f"{case['name']:<20}"
        for arm in arms:
            runs = [r["main_context"] for r in results if r["case"] == case["name"] and r["arm"] == arm]
            line += f"{sum(runs) / len(runs) / 1000:>8.0f}k" if runs else f"{'-':>9}"
        print(line)
    print(f"\n{len(results)} run(s) · ${total:.2f}")


if __name__ == "__main__":
    main()
