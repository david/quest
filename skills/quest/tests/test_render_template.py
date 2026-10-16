from pathlib import Path
import subprocess
import sys
import tempfile
import tomllib
import unittest


SKILL = Path(__file__).resolve().parents[1]
SCRIPT = SKILL / "scripts" / "render-template.py"


class RenderTemplateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.template = self.root / "template.toml"
        self.destination = self.root / "work" / "mise.local.toml"
        self.destination.parent.mkdir()
        self.template.write_text(
            (SKILL / "assets" / "mise.local.toml").read_text().replace("<realm>", "demo")
        )

    def run_renderer(self, slug="123-add-login", port="5101"):
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--template", str(self.template),
             "--destination", str(self.destination), "--slug", slug,
             "--app-port", port],
            capture_output=True, text=True,
        )

    def test_renders_baseline_and_normalizes_slug(self):
        result = self.run_renderer()
        self.assertEqual(result.returncode, 0, result.stderr)
        env = tomllib.loads(self.destination.read_text())["env"]
        self.assertEqual(env["DATABASE_URL"], "postgres:///demo_123_add_login")
        self.assertEqual(env["TEST_DATABASE_URL"], "postgres:///demo_123_add_login_test")
        self.assertEqual(env["PORT"], "5101")
        self.assertEqual(env["PC_SOCKET_PATH"], "/tmp/demo-process-compose-123_add_login.sock")
        self.assertEqual(env["PC_LOG_FILE"], "/tmp/demo-process-compose-123_add_login.log")
        self.assertEqual(self.destination.stat().st_mode & 0o777, 0o600)

    def test_invalid_slugs_create_nothing(self):
        for slug in ("../escape", "Upper", "two_words", "a--b", "-a", "a-", ""):
            with self.subTest(slug=slug):
                self.assertNotEqual(self.run_renderer(slug=slug).returncode, 0)
                self.assertFalse(self.destination.exists())

    def test_invalid_ports_create_nothing(self):
        for port in ("0", "65536", "-1", "abc"):
            with self.subTest(port=port):
                self.assertNotEqual(self.run_renderer(port=port).returncode, 0)
                self.assertFalse(self.destination.exists())

    def test_unresolved_placeholder_creates_nothing(self):
        self.template.write_text('[env]\nVALUE = "<realm>_<slug>"\n')
        self.assertNotEqual(self.run_renderer().returncode, 0)
        self.assertFalse(self.destination.exists())

    def test_invalid_toml_creates_nothing_without_leaking_content(self):
        self.template.write_text('[env]\nVALUE = secret-value\n')
        result = self.run_renderer()
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("secret-value", result.stderr)
        self.assertFalse(self.destination.exists())

    def test_existing_file_is_preserved(self):
        self.destination.write_text("user work")
        self.assertNotEqual(self.run_renderer().returncode, 0)
        self.assertEqual(self.destination.read_text(), "user work")

    def test_dangling_symlink_is_preserved(self):
        target = self.root / "missing"
        self.destination.symlink_to(target)
        self.assertNotEqual(self.run_renderer().returncode, 0)
        self.assertTrue(self.destination.is_symlink())
        self.assertFalse(target.exists())

    def test_missing_parent_is_not_created(self):
        self.destination = self.root / "absent" / "mise.local.toml"
        self.assertNotEqual(self.run_renderer().returncode, 0)
        self.assertFalse(self.destination.parent.exists())

    def test_repeat_render_is_deterministic_and_preserves_template(self):
        original = self.template.read_bytes()
        self.assertEqual(self.run_renderer().returncode, 0)
        first = self.destination.read_bytes()
        self.destination = self.root / "second.toml"
        self.assertEqual(self.run_renderer().returncode, 0)
        self.assertEqual(first, self.destination.read_bytes())
        self.assertEqual(original, self.template.read_bytes())


if __name__ == "__main__":
    unittest.main()
