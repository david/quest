import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


QUEST = Path(__file__).resolve().parents[1] / "bin" / "quest"


class ArchiveCheckTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        config = self.base / "gitconfig"
        config.write_text(
            "[user]\n\tname = Archive Test\n\temail = test@example.invalid\n"
            "[init]\n\tdefaultBranch = main\n[commit]\n\tgpgsign = false\n"
        )
        # Isolated identity and configuration; the user's signing setup must not apply.
        self.env = {
            **{key: value for key, value in os.environ.items() if not key.startswith("GIT_")},
            "HOME": str(self.base), "GIT_CONFIG_GLOBAL": str(config), "GIT_CONFIG_NOSYSTEM": "1",
        }
        self.origin = self.base / "origin.git"
        self.git(self.base, "init", "--quiet", "--bare", str(self.origin))
        # A space and a colon in every path: either can break a list of paths.
        self.project = self.base / "pro ject:x"
        self.repository = self.project / "repo"
        self.git(self.base, "clone", "--quiet", str(self.origin), str(self.repository))
        (self.repository / ".gitignore").write_text("node_modules/\n*.log\n")
        self.git(self.repository, "add", ".gitignore")
        self.commit(self.repository, "app.txt", "one\ntwo\nthree\n", "Start the app")
        self.git(self.repository, "push", "--quiet", "origin", "main")
        self.quest = self.project / "quests" / "sample-quest"
        self.quest.mkdir(parents=True)
        (self.quest / "QUEST.md").write_text("# Sample\n")
        self.worktrees = self.quest / "worktrees"

    def git(self, directory, *args):
        result = subprocess.run(
            ["git", "-C", str(directory), *args], env=self.env, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.rstrip("\n")

    def commit(self, checkout, name, text, subject):
        (checkout / name).write_text(text)
        self.git(checkout, "add", "--", name)
        self.git(checkout, "commit", "--quiet", "-m", subject)
        return self.git(checkout, "rev-parse", "--short", "HEAD")

    def clone(self):
        """Copy the project repository as the skill does, without needing reflinks."""
        self.worktrees.mkdir(exist_ok=True)
        shutil.copytree(self.repository, self.worktrees / "1", symlinks=True)
        return self.worktrees / "1"

    def check(self, *options, quest=None):
        return subprocess.run(
            [sys.executable, str(QUEST), "archive", "--check", *options, str(quest or self.quest)],
            cwd=self.base, env=self.env, capture_output=True, text=True,
        )

    def findings(self, *options):
        result = self.check(*options)
        self.assertIn(result.returncode, (0, 1), result.stderr)
        self.assertEqual(result.stderr, "")
        found = [line[4:] for line in result.stdout.split("\n") if line.startswith("  ! ")]
        self.assertEqual(result.returncode, 1 if found else 0, result.stdout)
        return found, result.stdout

    def archive(self, *options):
        return subprocess.run(
            [sys.executable, str(QUEST), "archive", *options, str(self.quest)],
            cwd=self.base, env=self.env, capture_output=True, text=True,
        )

    def refusal(self, *options, quest=None):
        result = self.check(*options, quest=quest)
        self.assertEqual(result.returncode, 2, result.stdout)
        return result.stderr

    def test_clean_merged_clone_has_no_findings(self):
        self.clone()
        found, report = self.findings()
        self.assertEqual(found, [])
        self.assertIn("worktrees/1: clone, on main at ", report)
        self.assertIn("Repository worktrees/1/.git: the quest's own", report)
        self.assertIn("    main (worktrees/1): merged into origin/main\n", report)
        self.assertTrue(report.endswith("\nNo findings.\n"))

    def test_quest_without_checkouts(self):
        found, report = self.findings()
        self.assertEqual(found, [])
        self.assertIn("No checkouts in worktrees/.", report)

    def test_uncommitted_and_stray_files(self):
        checkout = self.clone()
        (checkout / "app.txt").write_text("changed\n")
        (checkout / "notes.txt").write_text("untracked\n")
        (checkout / "debug.log").write_text("ignored\n")
        for directory in ("node_modules", "web/node_modules"):
            (checkout / directory).mkdir(parents=True)
            (checkout / directory / "package.js").write_text("generated\n")
        (self.worktrees / "scratch").mkdir()
        (self.worktrees / "scratch" / "data.csv").write_text("1\n")
        (self.worktrees / "empty").mkdir()
        found, report = self.findings()
        self.assertEqual(found, [
            "2 uncommitted paths", "in worktrees/ but not a checkout, so removed with it:"])
        self.assertIn("         M app.txt\n        ?? notes.txt\n", report)
        self.assertIn("        worktrees/scratch\n", report)
        self.assertNotIn("worktrees/empty", report)
        # Ignored files are not reported: what is worth keeping belongs in local-data/.
        self.assertNotIn("debug.log", report)
        self.assertNotIn("node_modules", report)

    def test_unmerged_branch_until_it_is_pushed(self):
        checkout = self.clone()
        self.git(checkout, "switch", "--quiet", "-c", "topic")
        self.commit(checkout, "feature.txt", "feature\n", "Add the feature")
        found, report = self.findings()
        self.assertEqual(found, ["topic (worktrees/1): 1 commit not in origin/main"])
        self.assertIn("        Add the feature\n", report)
        self.assertIn("    main: merged into origin/main\n", report)

        # The remote moves without this clone hearing of it; the check fetches.
        # The remote takes the commit itself, because a push from the clone,
        # even one to the remote's path, can update the clone's origin/main.
        self.git(self.origin, "fetch", "--quiet", str(checkout), "topic:main")
        found, report = self.findings()
        self.assertEqual(found, [])
        self.assertIn("    topic (worktrees/1): merged into origin/main\n", report)

    def test_squashed_and_rebased_work_counts_as_merged(self):
        checkout = self.clone()
        self.git(checkout, "switch", "--quiet", "-c", "squashed")
        self.commit(checkout, "feature.txt", "first\n", "Start the feature")
        self.commit(checkout, "feature.txt", "first\nsecond\n", "Finish the feature")
        self.git(checkout, "switch", "--quiet", "-c", "rebased", "main")
        self.commit(checkout, "fix.txt", "fix\n", "Fix the app")
        # Upstream moves on, then takes one branch as a single commit and the other rebased.
        self.commit(self.repository, "other.txt", "other\n", "Unrelated work")
        self.commit(self.repository, "feature.txt", "first\nsecond\n", "Add the feature (#1)")
        self.commit(self.repository, "fix.txt", "fix\n", "Fix the app")
        self.commit(self.repository, "fix.txt", "fix\nmore\n", "Extend the fix")
        self.git(self.repository, "push", "--quiet", "origin", "main")
        found, report = self.findings()
        self.assertEqual(found, [])
        self.assertIn("    rebased (worktrees/1): merged into origin/main, as other commits\n", report)
        self.assertIn("    squashed: merged into origin/main, as other commits\n", report)

    def test_work_that_cancels_out_is_not_merged(self):
        checkout = self.clone()
        self.commit(checkout, "idea.txt", "idea\n", "Try an idea")
        self.git(checkout, "revert", "--no-edit", "HEAD")
        found, report = self.findings()
        self.assertEqual(found, ["main (worktrees/1): 2 commits not in origin/main"])
        self.assertIn(" Try an idea\n", report)

    def test_work_past_a_squash_merge_is_unmerged(self):
        checkout = self.clone()
        self.git(checkout, "switch", "--quiet", "-c", "topic")
        self.commit(checkout, "feature.txt", "first\n", "Start the feature")
        self.commit(self.repository, "feature.txt", "first\n", "Add the feature (#1)")
        self.git(self.repository, "push", "--quiet", "origin", "main")
        self.commit(checkout, "feature.txt", "first\nlater\n", "Extend the feature")
        found, report = self.findings()
        self.assertEqual(found, ["topic (worktrees/1): 1 commit not in origin/main"])
        self.assertIn("        Extend the feature\n", report)
        self.assertNotIn("Start the feature", report)

    def test_worktrees_of_the_clone(self):
        checkout = self.clone()
        self.git(checkout, "worktree", "add", "--quiet", "-b", "second", "../2")
        self.git(checkout, "worktree", "add", "--quiet", "--detach", "../10")
        self.commit(self.worktrees / "10", "loose.txt", "loose\n", "Try something")
        outside = self.base / "elsewhere"
        self.git(checkout, "worktree", "add", "--quiet", "-b", "outside", str(outside))
        found, report = self.findings()
        self.assertEqual(found, [
            "outside the quest's worktrees/; removing its repository breaks it",
            "detached HEAD of worktrees/10: 1 commit not in origin/main",
        ])
        self.assertIn("        Try something\n", report)
        # Numbered checkouts in order, then what lies outside worktrees/.
        lines = [line for line in report.splitlines() if line and not line.startswith(" ")]
        self.assertEqual([line.split(":")[0] for line in lines[2:6]],
                         ["worktrees/1", "worktrees/2", "worktrees/10", str(outside)])
        self.assertIn("worktrees/2: worktree of worktrees/1, on second at ", report)
        self.assertIn("worktrees/10: worktree of worktrees/1, detached at ", report)
        self.assertIn(f"    outside ({outside}): merged into origin/main\n", report)

    def test_worktree_of_a_repository_that_outlives_the_quest(self):
        self.worktrees.mkdir()
        self.git(self.repository, "worktree", "add", "--quiet", "-b", "quest/sample", str(self.worktrees / "1"))
        self.git(self.repository, "branch", "someone-elses", "main")
        self.git(self.repository, "switch", "--quiet", "someone-elses")
        self.commit(self.repository, "theirs.txt", "theirs\n", "Not the quest's")
        found, report = self.findings()
        self.assertEqual(found, [])
        self.assertIn(f"worktrees/1: worktree of {self.repository}, on quest/sample at ", report)
        self.assertIn(f"Repository {self.repository / '.git'}: outside the quest, and outlives it\n", report)
        self.assertIn(f"    remove a worktree with: git -C {self.repository} worktree remove <path>\n", report)
        self.assertIn("    quest/sample (worktrees/1): merged into origin/main\n", report)
        self.assertNotIn("someone-elses", report)

        self.commit(self.worktrees / "1", "feature.txt", "feature\n", "Add the feature")
        self.assertEqual(self.findings()[0], ["quest/sample (worktrees/1): 1 commit not in origin/main"])

    def test_source_leaves_out_what_the_copy_inherited(self):
        self.git(self.repository, "switch", "--quiet", "-c", "old-topic")
        self.commit(self.repository, "old.txt", "old\n", "Old unmerged work")
        (self.repository / "app.txt").write_text("stashed\n")
        self.git(self.repository, "stash", "push", "--quiet", "-m", "inherited stash")
        self.git(self.repository, "switch", "--quiet", "main")
        checkout = self.clone()
        found, _ = self.findings()
        self.assertEqual(found, ["old-topic: 1 commit not in origin/main", "1 stash entry"])
        found, report = self.findings("--source", str(self.repository))
        self.assertEqual(found, [])
        self.assertIn(f"    old-topic: not in origin/main, but {self.repository} keeps it\n", report)

        # What the quest adds to the copy is reported, with the branch it built on.
        (checkout / "app.txt").write_text("the quest's stash\n")
        self.git(checkout, "stash", "push", "--quiet", "-m", "quest stash")
        self.git(checkout, "switch", "--quiet", "old-topic")
        self.commit(checkout, "more.txt", "more\n", "More on the old topic")
        found, report = self.findings("--source", str(self.repository))
        self.assertEqual(found, ["old-topic (worktrees/1): 2 commits not in origin/main", "1 stash entry"])
        self.assertIn("        More on the old topic\n        Old unmerged work\n", report)
        self.assertIn("        stash@{0}: On main: quest stash\n", report)
        self.assertNotIn("inherited stash", report)

    def test_inherited_worktree_registrations_are_not_the_quests(self):
        other = self.project / "quests" / "other-quest" / "worktrees" / "1"
        other.parent.mkdir(parents=True)
        self.git(self.repository, "worktree", "add", "--quiet", "-b", "other", str(other))
        (other / "dirty.txt").write_text("another quest's work\n")
        gone = self.base / "gone"
        self.git(self.repository, "worktree", "add", "--quiet", "-b", "gone", str(gone))
        shutil.rmtree(gone)
        self.clone()
        found, report = self.findings("--source", str(self.repository))
        self.assertEqual(found, [])
        self.assertNotIn("other-quest", report)

    def test_unreachable_or_missing_target(self):
        checkout = self.clone()
        self.git(checkout, "remote", "set-url", "origin", str(self.base / "missing.git"))
        found, report = self.findings()
        self.assertEqual(found, ["could not fetch origin/main; merge status is as of the last fetch"])
        self.assertIn("    main (worktrees/1): merged into origin/main\n", report)
        self.assertEqual(
            self.findings("--target", "origin/release")[0],
            ["could not fetch origin/release; merge status is as of the last fetch",
             "main (worktrees/1): there is no remote branch origin/release to compare it with"])

    def test_nothing_local_stands_in_for_the_target(self):
        checkout = self.clone()
        self.git(checkout, "switch", "--quiet", "-c", "origin/main")
        self.commit(checkout, "feature.txt", "feature\n", "Add the feature")
        self.git(checkout, "tag", "origin/main")
        self.assertEqual(self.findings()[0], ["origin/main (worktrees/1): 1 commit not in origin/main"])
        self.assertEqual(self.findings("--target", "main")[0], [
            "main: there is no remote branch main to compare it with",
            "origin/main (worktrees/1): there is no remote branch main to compare it with"])

    def test_text_with_unusual_separators(self):
        checkout = self.clone()
        for message in ("part one\u2028part two", "notes\fpage two"):
            (checkout / "app.txt").write_text(message)
            self.git(checkout, "stash", "push", "--quiet", "-m", message)
        self.git(checkout, "switch", "--quiet", "-c", "topic\u2028odd")
        self.commit(checkout, "feature.txt", "feature\n", "Add\x0bthe feature")
        (self.worktrees / "\u00b2").mkdir()
        found, report = self.findings()
        self.assertEqual(found, ["topic\u2028odd (worktrees/1): 1 commit not in origin/main", "2 stash entries"])
        self.assertIn("        stash@{1}: On main: part one\u2028part two\n", report)

    def test_refuses_what_it_cannot_inventory(self):
        self.assertIn("is not an active quest directory", self.refusal(quest=self.quest.parent))
        self.assertIn("is not an active quest directory", self.refusal(quest=self.base / "absent"))
        link = self.quest.parent / "linked-quest"
        link.symlink_to(self.quest)
        self.assertIn("is a symbolic link", self.refusal(quest=link))
        self.assertIn("rev-parse", self.refusal("--source", str(self.base)))
        checkout = self.clone()
        self.assertIn("is inside the quest", self.refusal("--source", str(checkout)))
        shutil.rmtree(self.worktrees)

        archived = self.quest.parent / ".archived" / "sample-quest"
        archived.mkdir(parents=True)
        self.assertIn("exists already", self.refusal())
        archived.rmdir()

        checkout = self.clone()
        self.git(checkout, "worktree", "add", "--quiet", "-b", "second", "../2")
        shutil.rmtree(checkout / ".git" / "worktrees" / "2")
        error = self.refusal()
        self.assertIn("any report above is incomplete", error)
        # Git's own wording for a worktree whose registration is gone varies by version.
        self.assertIn(f"git rev-parse in {self.worktrees / '2'}: fatal: ", error)

    def test_changes_nothing_in_the_quest(self):
        checkout = self.clone()
        self.git(checkout, "switch", "--quiet", "-c", "topic")
        self.commit(checkout, "feature.txt", "feature\n", "Add the feature")
        (checkout / "app.txt").write_text("changed\n")
        # Upstream moves on, and the clone has fetched it already, so the check's
        # fetch has nothing to write, and the trial rebase has something to do.
        self.commit(self.repository, "other.txt", "other\n", "Unrelated work")
        self.git(self.repository, "push", "--quiet", "origin", "main")
        self.git(checkout, "fetch", "--quiet", "origin")

        # Even a fetch with nothing new touches the objects directory, so compare files only.
        def state():
            return sorted(
                (str(path), path.lstat().st_mtime_ns, path.lstat().st_size)
                for path in self.quest.rglob("*") if not path.is_dir())

        before = state()
        self.assertEqual(self.findings()[0], [
            "1 uncommitted path", "topic (worktrees/1): 1 commit not in origin/main"])
        self.assertEqual(state(), before)

    def test_conflicting_rebase(self):
        checkout = self.clone()
        self.git(checkout, "switch", "--quiet", "-c", "topic")
        self.commit(checkout, "app.txt", "one\nTWO\nthree\n", "Shout two")
        # Upstream changes the same line another way.
        self.commit(self.repository, "app.txt", "one\n2\nthree\n", "Write two as a digit")
        self.git(self.repository, "push", "--quiet", "origin", "main")
        self.assertEqual(
            self.findings()[0], ["topic (worktrees/1): conflicts when rebased onto origin/main"])

    def test_rebase_ignores_the_users_git_configuration(self):
        checkout = self.clone()
        self.git(checkout, "switch", "--quiet", "-c", "rebased")
        self.commit(checkout, "fix.txt", "fix\n", "Fix the app")
        self.git(checkout, "switch", "--quiet", "-c", "topic", "main")
        self.commit(checkout, "feature.txt", "feature\n", "Add the feature")
        self.commit(self.repository, "other.txt", "other\n", "Unrelated work")
        self.commit(self.repository, "fix.txt", "fix\n", "Fix the app")
        self.git(self.repository, "push", "--quiet", "origin", "main")
        # A hook that refuses every rebase, and signing that always fails.
        hooks = self.base / "hooks"
        hooks.mkdir()
        (hooks / "pre-rebase").write_text("#!/bin/sh\nexit 1\n")
        (hooks / "pre-rebase").chmod(0o755)
        with open(self.env["GIT_CONFIG_GLOBAL"], "a") as config:
            config.write(f"[core]\n\thooksPath = {hooks}\n[commit]\n\tgpgSign = true\n"
                         "[gpg]\n\tprogram = false\n")
        found, report = self.findings()
        self.assertEqual(found, ["topic (worktrees/1): 1 commit not in origin/main"])
        self.assertIn("    rebased: merged into origin/main, as other commits\n", report)

    @unittest.skipUnless(os.path.isdir("/proc/self"), "needs /proc")
    def test_process_working_in_a_checkout(self):
        checkout = self.clone()
        sleeper = subprocess.Popen(["sleep", "60"], cwd=checkout)
        self.addCleanup(sleeper.wait)
        self.addCleanup(sleeper.kill)
        found, report = self.findings()
        self.assertEqual(found, ["processes with a working directory in a checkout:"])
        self.assertIn(f"        {sleeper.pid} sleep: {checkout}\n", report)


    def test_archive_removes_the_quests_clone_and_moves_the_quest(self):
        checkout = self.clone()
        self.git(checkout, "worktree", "add", "--quiet", "-b", "second", "../2")
        (checkout / "debug.log").write_text("ignored\n")
        (self.worktrees / "empty").mkdir()
        (self.quest / "notes.md").write_text("notes\n")
        result = self.archive()
        self.assertEqual((result.returncode, result.stderr), (0, ""), result.stdout)
        self.assertIn(
            "  last snapshot: Initialize quest records: 2 paths (QUEST.md, notes.md)\n"
            "  deleted worktrees/2\n  deleted worktrees/1\n  deleted worktrees/\n", result.stdout)
        archived = self.project / "quests" / ".archived" / "sample-quest"
        self.assertFalse(self.quest.exists())
        self.assertEqual(sorted(path.name for path in archived.iterdir()), [".git", "QUEST.md", "notes.md"])
        self.assertEqual(self.git(archived, "ls-files"), "QUEST.md\nnotes.md")
        self.assertEqual(self.git(self.repository, "branch", "--format=%(refname:short)"), "main")

    def test_archive_with_findings_changes_nothing(self):
        checkout = self.clone()
        (checkout / "app.txt").write_text("changed\n")
        result = self.archive()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertTrue(result.stdout.endswith("\nNothing was archived.\n"), result.stdout)
        self.assertEqual((checkout / "app.txt").read_text(), "changed\n")
        self.assertFalse((self.quest / ".git").exists())
        self.assertFalse((self.project / "quests" / ".archived").exists())

    def test_archive_removes_worktrees_and_merged_branches_of_a_repository_that_outlives_it(self):
        self.worktrees.mkdir()
        self.git(self.repository, "worktree", "add", "--quiet", "-b", "quest/sample", str(self.worktrees / "1"))
        self.commit(self.worktrees / "1", "feature.txt", "feature\n", "Add the feature")
        self.git(self.repository, "branch", "someone-elses", "main")
        # Upstream takes the work as another commit, which git branch -d does not see as merged.
        self.commit(self.repository, "feature.txt", "feature\n", "Add the feature (#1)")
        self.git(self.repository, "push", "--quiet", "origin", "main")
        result = self.archive()
        self.assertEqual((result.returncode, result.stderr), (0, ""), result.stdout)
        self.assertIn("  removed the worktree worktrees/1\n", result.stdout)
        self.assertIn(f"  deleted the merged branch quest/sample in {self.repository}\n", result.stdout)
        self.assertEqual(
            self.git(self.repository, "branch", "--format=%(refname:short)"), "main\nsomeone-elses")
        self.assertEqual(self.git(self.repository, "worktree", "list", "--porcelain").count("worktree "), 1)
        self.assertTrue((self.project / "quests" / ".archived" / "sample-quest" / "QUEST.md").is_file())


if __name__ == "__main__":
    unittest.main()
