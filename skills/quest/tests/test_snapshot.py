import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "snapshot.py"
EXCLUDED = (
    "/work/\n/local-data/\n/mise.local.toml\n.env\n.env.*\n!.env.example\n"
    "node_modules/\n.cache/\n__pycache__/\n*.pyc\n.DS_Store\n/tmp/\n/temp/\n"
    "/build/\n/dist/\n/coverage/\n"
)


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
            [sys.executable, str(SCRIPT), *map(str, directories)],
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

    def test_baseline_changes_deletions_and_no_op(self):
        (self.quest / "research").mkdir()
        (self.quest / "research" / "notes.md").write_text("notes\n")
        self.assertEqual(
            self.snapshot_ok(),
            "sample-quest: Initialize quest records: 3 paths (.gitignore, QUEST.md)\n")
        self.assertEqual(self.git(self.quest, "show", "HEAD:QUEST.md"), "# Existing records")

        (self.quest / "QUEST.md").write_text("# Changed\n")
        (self.quest / "plan.md").write_text("plan\n")
        (self.quest / "research" / "notes.md").unlink()
        self.assertEqual(
            self.snapshot_ok(),
            "sample-quest: Snapshot quest records: 3 paths (QUEST.md, plan.md)\n")
        self.assertEqual(self.git(self.quest, "ls-files"), ".gitignore\nQUEST.md\nplan.md")

        (self.quest / "plan.md").write_text("one more\n")
        self.assertEqual(
            self.snapshot_ok(), "sample-quest: Snapshot quest records: 1 path (plan.md)\n")
        self.assertEqual(self.snapshot_ok(), "")
        self.assertEqual(self.commits(self.quest), 3)
        self.assertEqual(self.git(self.quest, "status", "--porcelain"), "")
        self.assertEqual(self.git(self.quest, "log", "-1", "--format=%an <%ae>"),
                         "Snapshot Test <test@example.invalid>")

    def test_private_and_generated_paths_stay_out(self):
        for path in ("work/1/app.py", "local-data/dump.sql", "node_modules/x/index.js",
                     "research/.env", "mise.local.toml"):
            (self.quest / path).parent.mkdir(parents=True, exist_ok=True)
            (self.quest / path).write_text("private\n")
        (self.quest / ".env.example").write_text("EXAMPLE=1\n")
        self.snapshot_ok()
        self.assertEqual(self.git(self.quest, "ls-files"), ".env.example\n.gitignore\nQUEST.md")

    def test_existing_ignores_are_kept_and_nested_repositories_never_staged(self):
        (self.quest / ".gitignore").write_text("/qa/\n!/work/\n")
        (self.quest / "qa").mkdir()
        (self.quest / "qa" / "shot.png").write_text("image\n")
        (self.quest / "work").mkdir()
        (self.quest / "work" / "kept-out.txt").write_text("checkout\n")
        nested = self.quest / "vendor" / "odd name"
        nested.mkdir(parents=True)
        self.git(nested, "init", "--quiet")
        (nested / "file.txt").write_text("nested\n")
        self.snapshot_ok()
        self.assertEqual(self.git(self.quest, "ls-files"), ".gitignore\nQUEST.md")
        self.assertEqual(
            (self.quest / ".gitignore").read_text(),
            "/qa/\n!/work/\n" + EXCLUDED + "/vendor/odd\\ name/\n")
        self.assertNotIn("160000", self.git(self.quest, "ls-files", "--stage"))
        # The required block is already last, so a second run rewrites nothing.
        self.assertEqual(self.snapshot_ok(), "")
        self.assertEqual(self.commits(self.quest), 1)

        # A later negation cannot re-include an excluded path.
        with (self.quest / ".gitignore").open("a") as ignore:
            ignore.write("!/work/\n")
        self.snapshot_ok()
        self.assertEqual(self.git(self.quest, "ls-files"), ".gitignore\nQUEST.md")
        self.assertTrue((self.quest / ".gitignore").read_text().endswith(
            "!/work/\n" + EXCLUDED + "/vendor/odd\\ name/\n"))

    def test_ignore_file_that_is_not_utf8_is_extended_byte_for_byte(self):
        (self.quest / ".gitignore").write_bytes(b"/caf\xe9/\n")
        self.snapshot_ok()
        self.assertEqual(
            (self.quest / ".gitignore").read_bytes(), b"/caf\xe9/\n" + EXCLUDED.encode())

    def test_entirely_ignored_quest_makes_no_empty_commit(self):
        (self.quest / ".gitignore").write_text("*\n")
        self.assertEqual(self.snapshot_ok(), "")
        self.assertEqual(self.snapshot_ok(), "")
        result = subprocess.run(
            ["git", "-C", str(self.quest), "rev-parse", "--verify", "--quiet", "HEAD"], env=self.env)
        self.assertNotEqual(result.returncode, 0)

    def test_containing_quest_wins_over_a_declaration(self):
        elsewhere = self.add_quest("other-quest", "# Elsewhere\n", self.base / "declared" / "quests")
        (self.project / "AGENTS.md").write_text("Quest root: ../declared/quests\n")
        checkout = self.quest / "work" / "1" / "src"
        checkout.mkdir(parents=True)
        self.snapshot_ok(cwd=checkout)
        self.assertEqual(self.commits(self.quest), 1)
        self.assertFalse((elsewhere / ".git").exists())

    def test_declarations_resolve_beside_their_instruction_file(self):
        declared = self.base / "declared" / "quests"
        elsewhere = self.add_quest("other-quest", "# Elsewhere\n", declared)
        repo = self.project / "repo" / "src"
        repo.mkdir(parents=True)
        (self.project / "AGENTS.md").write_text(
            "# Quests\n\nQuest root: ./quests\n\nQuest root: `../declared/quests`\n")
        self.assertEqual(
            self.snapshot_ok(cwd=repo),
            "other-quest: Initialize quest records: 2 paths (.gitignore, QUEST.md)\n")
        self.assertFalse((self.quest / ".git").exists())

        # The nearest instruction file wins, and CLAUDE.md is read like AGENTS.md.
        (self.project / "repo" / "CLAUDE.md").write_text("Quest root: ../quests\n")
        self.snapshot_ok(cwd=repo)
        self.assertEqual(self.commits(self.quest), 1)
        self.assertEqual(self.commits(elsewhere), 1)

    def test_invalid_declaration_is_reported_and_creates_nothing(self):
        (self.project / "AGENTS.md").write_text("Quest root: ./records\n")
        (self.project / "records").mkdir()
        result = self.snapshot(cwd=self.project)
        self.assertEqual(result.returncode, 1)
        self.assertIn("invalid Quest root declaration", result.stderr)
        self.assertFalse((self.quest / ".git").exists())

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
            ["sh", "-c", 'rmdir "$PWD" && exec "$0" "$1" . "$2"',
             sys.executable, str(SCRIPT), str(self.project)],
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

    def test_enclosing_repository_excludes_all_quest_storage(self):
        self.git(self.project, "init", "--quiet")
        (self.project / "app.txt").write_text("app\n")
        self.git(self.project, "add", "app.txt")
        self.snapshot_ok()
        self.assertEqual(self.git(self.quest, "rev-parse", "--show-toplevel"), str(self.quest))
        self.git(self.project, "check-ignore", "-q", "quests/.archived/anything/QUEST.md")
        self.assertEqual(self.git(self.project, "status", "--porcelain"), "A  app.txt")
        self.snapshot_ok()
        self.assertEqual((self.project / ".git" / "info" / "exclude").read_text().count("/quests/"), 1)

    def test_enclosing_repository_that_tracks_quests_is_left_alone(self):
        self.git(self.project, "init", "--quiet")
        self.git(self.project, "add", "quests")
        result = self.snapshot()
        self.assertEqual(result.returncode, 1)
        self.assertIn("automatic untracking is refused", result.stderr)
        self.assertFalse((self.quest / ".git").exists())
        self.assertEqual(self.git(self.project, "ls-files"), "quests/sample-quest/QUEST.md")

    def test_quest_that_does_not_own_its_repository_is_refused(self):
        self.git(self.project, "init", "--quiet")
        (self.quest / ".git").write_text("gitdir: ../../.git\n")
        result = self.snapshot()
        self.assertEqual(result.returncode, 1)
        self.assertIn("does not own its repository", result.stderr)
        self.assertEqual(self.git(self.project, "ls-files", "--stage"), "")

    def test_tracked_excluded_content_is_refused_without_untracking(self):
        self.snapshot_ok()
        (self.quest / "local-data").mkdir()
        (self.quest / "local-data" / "dump.sql").write_text("data\n")
        self.git(self.quest, "add", "-f", "local-data/dump.sql")
        result = self.snapshot()
        self.assertEqual(result.returncode, 1)
        self.assertIn("automatic untracking is refused", result.stderr)
        self.assertEqual(self.commits(self.quest), 1)
        self.assertIn("local-data/dump.sql", self.git(self.quest, "ls-files"))

    def test_one_failing_quest_does_not_stop_the_others(self):
        sibling = self.add_quest("sibling-quest", "# Existing sibling\n")
        (self.quest / ".git").write_text("gitdir: /nonexistent\n")
        result = self.snapshot()
        self.assertEqual(result.returncode, 1)
        self.assertEqual(self.commits(sibling), 1)

    def test_parallel_processes_serialize(self):
        processes = [
            subprocess.Popen(
                [sys.executable, str(SCRIPT)], cwd=self.quest, env=self.env,
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
