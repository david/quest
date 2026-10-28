#!/usr/bin/env python3
"""Run the quest-master skill's eval cases.

Each case runs with the quest and quest-master plugins, and with the quest
plugin alone, so the difference is what quest-master adds. The runner is the
quest skill's, in `../../quest/evals/git/run.py`.
"""

import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILLS = HERE.parent.parent

spec = importlib.util.spec_from_file_location("quest_runner", SKILLS / "quest/evals/git/run.py")
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)

if __name__ == "__main__":
    runner.main(
        cases_dir=HERE,
        plugins={
            "with": [SKILLS / "quest", SKILLS / "quest-master"],
            "without": [SKILLS / "quest"],
        },
        tools=[*runner.TOOLS, "Agent"],
        description=__doc__.splitlines()[0],
    )
