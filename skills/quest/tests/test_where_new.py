import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest


QUEST = Path(__file__).resolve().parents[1] / "bin" / "quest"
SKILL = Path(__file__).resolve().parents[1] / "SKILL.md"


class WhereNewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        # A space in the path: it can break a command line.
        self.realm = Path(self.temp.name).resolve() / "my realm"
        self.root = self.realm / "quests"
        self.root.mkdir(parents=True)

    def run_quest(self, *args, cwd=None):
        return subprocess.run(
            [sys.executable, str(QUEST), *args], cwd=cwd or self.realm,
            capture_output=True, text=True)

    def add_quest(self, slug):
        quest = self.root / slug
        quest.mkdir()
        (quest / "QUEST.md").write_text(f"# {slug}\n")
        return quest

    def found(self, directory):
        result = self.run_quest("where", str(directory))
        return result.returncode, json.loads(result.stdout)

    # quest where

    def test_finds_the_quest_from_inside_it(self):
        quest = self.add_quest("fix-it")
        (quest / "research" / "deep").mkdir(parents=True)
        self.assertEqual(self.found(quest / "research" / "deep"), (0, {
            "quest": str(quest), "root": str(self.root), "realm": str(self.realm)}))

    def test_finds_the_root_from_the_realm_and_from_the_root(self):
        expected = (0, {"quest": None, "root": str(self.root), "realm": str(self.realm)})
        self.assertEqual(self.found(self.realm), expected)
        self.assertEqual(self.found(self.root), expected)

    def test_defaults_to_the_working_directory(self):
        quest = self.add_quest("fix-it")
        result = self.run_quest("where", cwd=quest)
        self.assertEqual(json.loads(result.stdout)["quest"], str(quest))

    def test_finds_the_realm_root_from_its_repository(self):
        repository = self.realm / "app" / "src"
        repository.mkdir(parents=True)
        (self.realm / "app" / ".git").mkdir()
        self.assertEqual(self.found(repository)[1]["root"], str(self.root))

    def test_skips_a_quests_directory_inside_a_repository(self):
        app = self.realm / "app"
        (app / ".git").mkdir(parents=True)
        (app / "quests").mkdir()
        self.assertEqual(self.found(app)[1]["root"], str(self.root))

    def test_a_directory_without_a_record_is_not_a_quest(self):
        (self.root / "draft").mkdir()
        self.assertEqual(self.found(self.root / "draft")[1]["quest"], None)

    def test_a_directory_with_an_invalid_slug_is_not_a_quest(self):
        quest = self.add_quest("Fix_It")
        self.assertEqual(self.found(quest)[1]["quest"], None)

    def test_reports_nothing_found(self):
        elsewhere = Path(self.temp.name) / "elsewhere"
        elsewhere.mkdir()
        result = self.run_quest("where", str(elsewhere))
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout), {"quest": None, "root": None, "realm": None})
        self.assertIn("is in no quest or realm", result.stderr)
        self.assertIn("quest list", result.stderr)

    # quest new

    def version(self):
        return re.search(r'version: "([^"]+)"', SKILL.read_text()).group(1)

    def test_creates_a_quest(self):
        result = self.run_quest("new", "fix-it", "--title", "Fix it")
        self.assertEqual(result.returncode, 0, result.stderr)
        quest = self.root / "fix-it"
        self.assertEqual(json.loads(result.stdout),
                         {"dir": str(quest), "record": str(quest / "QUEST.md")})
        record = (quest / "QUEST.md").read_text()
        self.assertTrue(record.startswith(f'---\nquest_skill_version: "{self.version()}"\n---\n\n# Fix it\n'))
        self.assertIn("\n## Current State\n", record)
        self.assertIn("- Checkpoint: the quest was created.\n", record)

    def test_the_new_quest_is_found_and_listed(self):
        self.run_quest("new", "fix-it", "--title", "Fix it")
        self.assertEqual(self.found(self.root / "fix-it")[1]["quest"], str(self.root / "fix-it"))

    def test_finds_the_root_from_a_quest(self):
        quest = self.add_quest("first")
        result = self.run_quest("new", "second", "--title", "Second", cwd=quest)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.root / "second" / "QUEST.md").is_file())

    def test_takes_a_root(self):
        elsewhere = Path(self.temp.name) / "elsewhere"
        elsewhere.mkdir()
        result = self.run_quest("new", "fix-it", "--title", "Fix it", "--root", str(self.root), cwd=elsewhere)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.root / "fix-it" / "QUEST.md").is_file())

    def test_copies_the_template(self):
        template = self.realm / "quest-template"
        (template / "research").mkdir(parents=True)
        (template / "research" / "README.md").write_text("findings\n")
        (template / ".env").write_text("PORT=\n")
        self.run_quest("new", "fix-it", "--title", "Fix it")
        quest = self.root / "fix-it"
        self.assertEqual((quest / "research" / "README.md").read_text(), "findings\n")
        self.assertEqual((quest / ".env").read_text(), "PORT=\n")
        self.assertTrue((quest / "QUEST.md").is_file())

    def test_refuses_a_template_with_a_record(self):
        template = self.realm / "quest-template"
        template.mkdir()
        (template / "QUEST.md").write_text("# template\n")
        result = self.run_quest("new", "fix-it", "--title", "Fix it")
        self.assertEqual(result.returncode, 1)
        self.assertIn("nothing was created", result.stderr)
        self.assertFalse((self.root / "fix-it").exists())

    def test_refuses_an_existing_quest(self):
        quest = self.add_quest("fix-it")
        result = self.run_quest("new", "fix-it", "--title", "Fix it")
        self.assertEqual(result.returncode, 1)
        self.assertIn("exists already", result.stderr)
        self.assertEqual((quest / "QUEST.md").read_text(), "# fix-it\n")

    def test_refuses_an_existing_file(self):
        (self.root / "fix-it").write_text("not a quest\n")
        result = self.run_quest("new", "fix-it", "--title", "Fix it")
        self.assertEqual(result.returncode, 1)
        self.assertEqual((self.root / "fix-it").read_text(), "not a quest\n")

    def test_refuses_invalid_slugs(self):
        for slug in ("Fix-it", "fix_it", "fix--it", "-fix", "../fix", "fix/it", ".archived", ""):
            with self.subTest(slug=slug):
                result = self.run_quest("new", "--title", "Fix it", "--", slug)
                self.assertEqual(result.returncode, 1)
                self.assertIn("not a slug", result.stderr)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_refuses_a_title_that_is_not_one_line(self):
        for title in ("", "  ", "Fix\nit"):
            with self.subTest(title=title):
                result = self.run_quest("new", "fix-it", "--title", title)
                self.assertEqual(result.returncode, 1)
        self.assertFalse((self.root / "fix-it").exists())

    def test_refuses_without_a_root(self):
        elsewhere = Path(self.temp.name) / "elsewhere"
        elsewhere.mkdir()
        result = self.run_quest("new", "fix-it", "--title", "Fix it", cwd=elsewhere)
        self.assertEqual(result.returncode, 1)
        self.assertIn("pass --root", result.stderr)


if __name__ == "__main__":
    unittest.main()
