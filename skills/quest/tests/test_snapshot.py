import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


SKILL = Path(__file__).resolve().parents[1]
QUEST = SKILL / "bin" / "quest"
DEFAULT_RULES = (SKILL / "assets" / "snapshot-exclude").read_text()


class SnapshotTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.project = self.base / "project"
        self.root = self.project / "quests"
        self.quest = self.add_quest("sample-quest", "# Existing records\n")
        config = self.base / "gitconfig"
        config.write_text(
            "[user]\n\tname = Snapshot Test\n\temail = test@example.invalid\n"
            "[init]\n\tdefaultBranch = main\n"
        )
        # Isolated identity and configuration; the user's signing setup must not apply.
        self.env = {
            **{key: value for key, value in os.environ.items() if not key.startswith("GIT_")},
            "HOME": str(self.base), "GIT_CONFIG_GLOBAL": str(config), "GIT_CONFIG_NOSYSTEM": "1",
        }

    def add_quest(self, slug, text, root=None):
        quest = (root or self.root) / slug
        quest.mkdir(parents=True)
        (quest / "QUEST.md").write_text(text)
        return quest

    def snapshot(self, *directories, cwd=None):
        return subprocess.run(
            [sys.executable, str(QUEST), "snapshot", *map(str, directories)],
            cwd=cwd or self.quest, env=self.env, capture_output=True, text=True,
        )

    def snapshot_ok(self, *directories, cwd=None):
        result = self.snapshot(*directories, cwd=cwd)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        return result.stdout

    def git(self, directory, *args):
        result = subprocess.run(
            ["git", "-C", str(directory), *args], env=self.env, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.rstrip("\n")

    def commits(self, quest):
        return int(self.git(quest, "rev-list", "--count", "HEAD"))

    def rules(self, quest):
        return (quest / ".git" / "info" / "exclude").read_text()

    def test_baseline_changes_deletions_and_no_op(self):
        (self.quest / "research").mkdir()
        (self.quest / "research" / "notes.md").write_text("notes\n")
        self.assertEqual(
            self.snapshot_ok(),
            "sample-quest: Initialize quest records: 2 paths (QUEST.md, research/notes.md)\n")
        self.assertEqual(self.git(self.quest, "show", "HEAD:QUEST.md"), "# Existing records")
        self.assertEqual(self.rules(self.quest), DEFAULT_RULES)
        self.assertFalse((self.quest / ".gitignore").exists())

        (self.quest / "QUEST.md").write_text("# Changed\n")
        (self.quest / "plan.md").write_text("plan\n")
        (self.quest / "research" / "notes.md").unlink()
        self.assertEqual(
            self.snapshot_ok(),
            "sample-quest: Snapshot quest records: 3 paths (QUEST.md, plan.md)\n")
        self.assertEqual(self.git(self.quest, "ls-files"), "QUEST.md\nplan.md")

        (self.quest / "plan.md").write_text("one more\n")
        self.assertEqual(
            self.snapshot_ok(), "sample-quest: Snapshot quest records: 1 path (plan.md)\n")
        self.assertEqual(self.snapshot_ok(), "")
        self.assertEqual(self.commits(self.quest), 3)
        self.assertEqual(self.git(self.quest, "status", "--porcelain"), "")
        self.assertEqual(self.git(self.quest, "log", "-1", "--format=%an <%ae>"),
                         "Snapshot Test <test@example.invalid>")

    def test_private_and_generated_paths_stay_out(self):
        for path in ("worktrees/1/app.py", "local-data/dump.sql", "node_modules/x/index.js",
                     "research/.env"):
            (self.quest / path).parent.mkdir(parents=True, exist_ok=True)
            (self.quest / path).write_text("private\n")
        (self.quest / ".env.example").write_text("EXAMPLE=1\n")
        self.snapshot_ok()
        self.assertEqual(self.git(self.quest, "ls-files"), ".env.example\nQUEST.md")

    def test_quest_ignore_file_is_left_alone_and_nested_repositories_never_staged(self):
        (self.quest / ".gitignore").write_bytes(b"/qa/\n/caf\xe9/\n")
        (self.quest / "qa").mkdir()
        (self.quest / "qa" / "shot.png").write_text("image\n")
        nested = self.quest / "vendor" / "odd name"
        nested.mkdir(parents=True)
        self.git(nested, "init", "--quiet")
        (nested / "file.txt").write_text("nested\n")
        self.snapshot_ok()
        self.assertEqual(self.git(self.quest, "ls-files"), ".gitignore\nQUEST.md")
        self.assertEqual((self.quest / ".gitignore").read_bytes(), b"/qa/\n/caf\xe9/\n")
        self.assertEqual(self.rules(self.quest), DEFAULT_RULES + "/vendor/odd\\ name/\n")
        self.assertNotIn("160000", self.git(self.quest, "ls-files", "--stage"))
        self.assertEqual(self.snapshot_ok(), "")
        self.assertEqual(self.commits(self.quest), 1)

    def test_rules_file_is_owned_by_the_script(self):
        self.snapshot_ok()
        (self.quest / ".git" / "info" / "exclude").write_text("QUEST.md\n")
        (self.quest / "plan.md").write_text("plan\n")
        (self.quest / "local-data").mkdir()
        (self.quest / "local-data" / "dump.sql").write_text("private\n")
        self.snapshot_ok()
        self.assertEqual(self.rules(self.quest), DEFAULT_RULES)
        self.assertEqual(self.git(self.quest, "ls-files"), "QUEST.md\nplan.md")

    def test_quest_rule_can_override_a_default(self):
        (self.quest / ".gitignore").write_text("!/build/\n")
        (self.quest / "build").mkdir()
        (self.quest / "build" / "report.md").write_text("kept on purpose\n")
        (self.quest / "dist").mkdir()
        (self.quest / "dist" / "bundle.js").write_text("generated\n")
        self.snapshot_ok()
        self.assertEqual(
            self.git(self.quest, "ls-files"), ".gitignore\nQUEST.md\nbuild/report.md")

    def test_missing_default_rules_are_reported_once_and_nothing_is_created(self):
        self.add_quest("sibling-quest", "# Existing sibling\n")
        copy = self.base / "skill" / "bin"
        copy.mkdir(parents=True)
        shutil.copy(QUEST, copy)
        result = subprocess.run(
            [sys.executable, str(copy / "quest"), "snapshot"],
            cwd=self.quest, env=self.env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(len(result.stderr.splitlines()), 1)
        self.assertIn("snapshot-exclude", result.stderr)
        self.assertFalse((self.quest / ".git").exists())
        outside = self.base / "outside"
        outside.mkdir()
        result = subprocess.run(
            [sys.executable, str(copy / "quest"), "snapshot"],
            cwd=outside, env=self.env, capture_output=True, text=True)
        self.assertEqual((result.returncode, result.stderr), (0, ""))

    def test_entirely_ignored_quest_makes_no_empty_commit(self):
        (self.quest / ".gitignore").write_text("*\n")
        self.assertEqual(self.snapshot_ok(), "")
        self.assertEqual(self.snapshot_ok(), "")
        result = subprocess.run(
            ["git", "-C", str(self.quest), "rev-parse", "--verify", "--quiet", "HEAD"], env=self.env)
        self.assertNotEqual(result.returncode, 0)

    def test_containing_quest_wins_over_a_nearer_quests_directory(self):
        checkout = self.quest / "worktrees" / "1"
        elsewhere = self.add_quest("other-quest", "# Elsewhere\n", checkout / "quests")
        self.snapshot_ok(cwd=checkout)
        self.assertEqual(self.commits(self.quest), 1)
        self.assertFalse((elsewhere / ".git").exists())

    def test_repository_finds_its_realms_quests_not_its_own(self):
        repository = self.project / "repo"
        own = self.add_quest("own-quest", "# The repository's own\n", repository / "quests")
        (repository / "src").mkdir()
        self.git(repository, "init", "--quiet")
        self.assertEqual(
            self.snapshot_ok(cwd=repository / "src"),
            "sample-quest: Initialize quest records: 1 path (QUEST.md)\n")
        self.assertFalse((own / ".git").exists())

    def test_root_fallbacks_and_no_root(self):
        self.snapshot_ok(cwd=self.root)
        self.assertEqual(self.commits(self.quest), 1)
        (self.quest / "QUEST.md").write_text("# From the project directory\n")
        self.snapshot_ok(cwd=self.project)
        self.assertEqual(self.commits(self.quest), 2)

        outside = self.base / "outside"
        outside.mkdir()
        self.assertEqual(self.snapshot_ok(cwd=outside), "")
        self.assertEqual(sorted(path.name for path in outside.iterdir()), [])

    def test_several_directories_snapshot_each_root_once(self):
        other = self.add_quest("other-quest", "# Other\n", self.base / "second" / "quests")
        output = self.snapshot_ok(self.quest, self.project, other, self.base / "missing")
        self.assertEqual(output.count("Initialize quest records"), 2)
        self.assertEqual(self.commits(self.quest), 1)
        self.assertEqual(self.commits(other), 1)

    def test_removed_working_directory_is_skipped(self):
        gone = self.base / "gone"
        gone.mkdir()
        result = subprocess.run(
            ["sh", "-c", 'rmdir "$PWD" && exec "$0" "$1" snapshot . "$2"',
             sys.executable, str(QUEST), str(self.project)],
            cwd=gone, env=self.env, capture_output=True, text=True,
        )
        self.assertEqual((result.returncode, result.stderr), (0, ""))
        self.assertEqual(self.commits(self.quest), 1)

    def test_siblings_are_snapshotted_and_archived_quests_are_not(self):
        sibling = self.add_quest("sibling-quest", "# Existing sibling\n")
        symlinked = self.base / "linked-target"
        symlinked.mkdir()
        (symlinked / "QUEST.md").write_text("# Linked\n")
        (self.root / "linked-quest").symlink_to(symlinked)
        self.add_quest("Not_A_Slug", "# Ignored\n")
        self.snapshot_ok()
        self.assertEqual(self.git(sibling, "show", "HEAD:QUEST.md"), "# Existing sibling")
        self.assertFalse((symlinked / ".git").exists())
        self.assertFalse((self.root / "Not_A_Slug" / ".git").exists())

        archive = self.root / ".archived" / "sample-quest"
        archive.parent.mkdir()
        self.quest.rename(archive)
        (archive / "QUEST.md").write_text("# Archived edit\n")
        (sibling / "QUEST.md").write_text("# Sibling after archive\n")
        self.snapshot_ok(cwd=archive)
        self.assertEqual(self.commits(archive), 1)
        self.assertEqual(self.git(archive, "show", "HEAD:QUEST.md"), "# Existing records")
        self.assertEqual(self.git(sibling, "show", "HEAD:QUEST.md"), "# Sibling after archive")

    def test_root_inside_a_repository_is_refused(self):
        for repository in (self.root, self.project):
            self.git(repository, "init", "--quiet")
            result = self.snapshot()
            self.assertEqual(result.returncode, 1)
            self.assertIn(f"but {repository} is one", result.stderr)
            self.assertFalse((self.quest / ".git").exists())
            self.assertIn("??", self.git(repository, "status", "--porcelain"))
            shutil.rmtree(repository / ".git")

    def test_quest_that_does_not_own_its_repository_is_refused(self):
        other = self.base / "other-repo"
        other.mkdir()
        self.git(other, "init", "--quiet")
        (self.quest / ".git").write_text(f"gitdir: {other / '.git'}\n")
        result = self.snapshot()
        self.assertEqual(result.returncode, 1)
        self.assertIn("does not own its repository", result.stderr)
        self.assertEqual(self.git(other, "ls-files", "--stage"), "")

    def test_file_ignored_after_it_was_recorded_leaves_later_snapshots(self):
        (self.quest / "qa").mkdir()
        (self.quest / "qa" / "server.log").write_text("first run\n")
        (self.quest / "qa" / "caf\udce9 [1].log").write_text("odd name\n")
        (self.quest / "qa" / "journey.ts").write_text("steps\n")
        self.snapshot_ok()
        self.assertIn("qa/server.log", self.git(self.quest, "ls-files"))

        (self.quest / "qa" / ".gitignore").write_text("*.log\n")
        (self.quest / "qa" / "server.log").write_text("second run\n")
        (self.quest / "QUEST.md").write_text("# Changed\n")
        self.assertEqual(
            self.snapshot_ok(),
            "sample-quest: Snapshot quest records: 4 paths (QUEST.md, qa/.gitignore)\n")
        self.assertEqual(
            self.git(self.quest, "ls-files"), "QUEST.md\nqa/.gitignore\nqa/journey.ts")
        self.assertEqual((self.quest / "qa" / "server.log").read_text(), "second run\n")
        self.assertEqual(self.git(self.quest, "show", "HEAD^:qa/server.log"), "first run")
        self.assertEqual(self.snapshot_ok(), "")

    def test_forced_tracking_of_an_excluded_path_is_undone(self):
        self.snapshot_ok()
        (self.quest / "local-data").mkdir()
        (self.quest / "local-data" / "dump.sql").write_text("data\n")
        self.git(self.quest, "add", "-f", "local-data/dump.sql")
        self.assertEqual(self.snapshot_ok(), "")
        self.assertEqual(self.git(self.quest, "ls-files"), "QUEST.md")
        self.assertTrue((self.quest / "local-data" / "dump.sql").exists())
        self.assertEqual(self.commits(self.quest), 1)

    def test_tracked_nested_repository_is_refused(self):
        self.snapshot_ok()
        nested = self.quest / "vendor"
        nested.mkdir()
        self.git(nested, "init", "--quiet")
        (nested / "file.txt").write_text("nested\n")
        self.git(nested, "add", "file.txt")
        self.git(nested, "commit", "--quiet", "-m", "nested")
        self.git(self.quest, "add", "-f", "vendor")
        result = self.snapshot()
        self.assertEqual(result.returncode, 1)
        self.assertIn("tracks a nested repository", result.stderr)
        self.assertEqual(self.commits(self.quest), 1)

    def test_one_failing_quest_does_not_stop_the_others(self):
        sibling = self.add_quest("sibling-quest", "# Existing sibling\n")
        (self.quest / ".git").write_text("gitdir: /nonexistent\n")
        result = self.snapshot()
        self.assertEqual(result.returncode, 1)
        self.assertEqual(self.commits(sibling), 1)

    def test_parallel_processes_serialize(self):
        processes = [
            subprocess.Popen(
                [sys.executable, str(QUEST), "snapshot"], cwd=self.quest, env=self.env,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            for _ in range(6)
        ]
        results = [(process.communicate(), process.returncode) for process in processes]
        for (_, stderr), code in results:
            self.assertEqual((code, stderr), (0, ""))
        self.assertEqual(sum(bool(stdout) for (stdout, _), _ in results), 1)
        self.assertEqual(self.commits(self.quest), 1)

    def test_signing_failure_keeps_records_and_the_next_run_retries(self):
        self.snapshot_ok()
        self.git(self.quest, "config", "commit.gpgsign", "true")
        self.git(self.quest, "config", "gpg.program", "/does-not-exist")
        (self.quest / "QUEST.md").write_text("retain failed snapshot\n")
        head = self.git(self.quest, "rev-parse", "HEAD")
        result = self.snapshot()
        self.assertEqual(result.returncode, 1)
        self.assertIn(str(self.quest), result.stderr)
        self.assertEqual(self.git(self.quest, "rev-parse", "HEAD"), head)
        self.assertEqual((self.quest / "QUEST.md").read_text(), "retain failed snapshot\n")

        self.git(self.quest, "config", "commit.gpgsign", "false")
        self.snapshot_ok()
        self.assertEqual(self.git(self.quest, "show", "HEAD:QUEST.md"), "retain failed snapshot")

    def test_caller_git_routing_is_not_inherited(self):
        other = self.base / "other-repo"
        other.mkdir()
        self.git(other, "init", "--quiet")
        self.env.update(GIT_DIR=str(other / ".git"), GIT_WORK_TREE=str(other),
                        GIT_INDEX_FILE=str(other / ".git" / "index"))
        self.snapshot_ok()
        del self.env["GIT_DIR"], self.env["GIT_WORK_TREE"], self.env["GIT_INDEX_FILE"]
        self.assertEqual(self.commits(self.quest), 1)
        self.assertEqual(self.git(other, "status", "--porcelain"), "")


if __name__ == "__main__":
    unittest.main()
