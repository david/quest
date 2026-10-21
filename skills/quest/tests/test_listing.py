import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import unittest


QUEST = Path(__file__).resolve().parents[1] / "bin" / "quest"

# Stands in for ssh. For the host "remote" it runs the command in another home
# directory, as ssh would on that host; any other host cannot be reached.
FAKE_SSH = """#!/bin/sh
while [ "$1" != -- ]; do shift; done
shift
[ "$1" = remote ] || { printf 'ssh: Could not resolve hostname %s\\r\\n' "$1" >&2; exit 255; }
cd "$REMOTE_HOME" && HOME=$REMOTE_HOME exec sh -c "$2"
"""


class ListingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.home = self.base / "home"
        self.remote_home = self.base / "remote"
        bin = self.base / "bin"
        bin.mkdir()
        (bin / "ssh").write_text(FAKE_SSH)
        (bin / "ssh").chmod(0o755)
        (bin / "python3").symlink_to(sys.executable)
        self.env = {
            **os.environ, "HOME": str(self.home), "REMOTE_HOME": str(self.remote_home),
            "XDG_CONFIG_HOME": str(self.base / "config"), "PATH": f"{bin}:{os.environ['PATH']}",
        }
        # A space and a colon in every path: either can break a command line.
        self.world = self.home / "Pro jects:x"
        self.realm = self.add_realm(self.world, "app")

    def add_realm(self, world, name, declaration="Quest root: ./quests\n"):
        realm = world / name
        (realm / "quests").mkdir(parents=True)
        (realm / "AGENTS.md").write_text(f"# {name}\n\n{declaration}")
        return realm

    def add_quest(self, root, slug, text=None):
        quest = root / slug
        quest.mkdir(parents=True)
        (quest / "QUEST.md").write_text(f"# {slug} title\n" if text is None else text)
        return quest

    def set_worlds(self, worlds):
        config = self.base / "config" / "quest"
        config.mkdir(parents=True, exist_ok=True)
        (config / "worlds.json").write_text(json.dumps(worlds))

    def run_quest(self, *args):
        return subprocess.run(
            [sys.executable, str(QUEST), *args],
            cwd=self.base, env=self.env, capture_output=True, text=True,
        )

    def output(self, *args):
        result = self.run_quest(*args)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        return json.loads(result.stdout)

    def failure(self, *args):
        result = self.run_quest(*args)
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertEqual(result.stdout, "")
        return result.stderr

    def test_worlds_default_to_projects_in_the_home_directory(self):
        self.assertEqual(self.output("world", "list"),
                         [{"world": "~/Projects", "host": None, "path": "~/Projects"}])
        self.add_realm(self.home / "Projects", "here")
        self.assertEqual(self.output("realm", "list")["realms"], [{
            "world": "~/Projects", "host": None, "realm": "here",
            "dir": str(self.home / "Projects" / "here"),
            "root": str(self.home / "Projects" / "here" / "quests")}])

    def test_worlds_file(self):
        this = socket.gethostname()
        self.set_worlds([
            {"host": "remote", "path": "/srv/p"}, {"path": "~/p"},
            {"host": this.upper(), "path": "/a"}, {"host": "localhost", "path": "b"}, {"host": None, "path": "c"},
        ])
        self.assertEqual(self.output("world", "list"), [
            {"world": "remote:/srv/p", "host": "remote", "path": "/srv/p"},
            {"world": "~/p", "host": None, "path": "~/p"},
            {"world": f"{this.upper()}:/a", "host": None, "path": "/a"},
            {"world": "localhost:b", "host": None, "path": "b"},
            {"world": "c", "host": None, "path": "c"},
        ])

        for worlds, error in (
            ("[", "Expecting value"),
            ('{"path": "/a"}', "expected a list"),
            ('[{"host": "remote"}]', "expected a list"),
            ('[{"host": "-oProxyCommand", "path": "/a"}]', "not a host name: -oProxyCommand"),
            ('[{"path": "/a\\nb"}]', "not a path"),
        ):
            (self.base / "config" / "quest" / "worlds.json").write_text(worlds)
            with self.subTest(worlds=worlds):
                stderr = self.failure("realm", "list")
                self.assertTrue(stderr.startswith("quest realm list: "), stderr)
                self.assertIn("worlds.json", stderr)
                self.assertIn(error, stderr)
        self.assertIn("not a host name", self.failure("list", "--world=-v:/a"))

    def test_every_directory_in_a_world_is_a_realm(self):
        self.add_realm(self.world, "ticked", "Quest root: `./quests`\n")
        (self.world / "undeclared" / "quests").mkdir(parents=True)
        (self.world / "no-quests").mkdir()
        (self.world / "file-only").mkdir()
        (self.world / "file-only" / "quests").write_text("")
        shared = self.world / "shared" / "quests"
        shared.mkdir(parents=True)
        claude = self.world / "elsewhere"
        claude.mkdir()
        (claude / "CLAUDE.md").write_text("Quest root: ../shared/quests\n")
        self.add_realm(self.world, "broken", "Quest root: ./missing\n")
        (self.world / "file").write_text("")
        (self.world / ".hidden" / "quests").mkdir(parents=True)

        listing = self.output("realm", "list", "--world", str(self.world))
        realms = {realm["realm"]: realm["root"] for realm in listing["realms"]}
        self.assertEqual(realms, {
            "app": str(self.realm / "quests"),
            "ticked": str(self.world / "ticked" / "quests"),
            "elsewhere": str(shared),
            "shared": str(shared),
            "undeclared": str(self.world / "undeclared" / "quests"),
            "no-quests": None,
            "file-only": None,
            "broken": None,
        })
        self.assertEqual(listing["failed"], [{
            "world": str(self.world), "host": None, "realm": "broken",
            "error": f"invalid Quest root declaration in {self.world / 'broken' / 'AGENTS.md'}"}])

    def test_quests_titles_invalid_and_archived(self):
        root = self.realm / "quests"
        self.add_quest(root, "plain")
        self.add_quest(root, "front", '---\nquest_skill_version: "5.0.0"\n# a comment\n---\n\n# The title\n')
        self.add_quest(root, "untitled", "No heading\n")
        (root / "no-record").mkdir()
        (root / "Not_a_slug").mkdir()
        self.add_quest(root / ".archived", "done")
        other = self.add_realm(self.world, "other")
        self.add_quest(other / "quests", "elsewhere")

        world = ["--world", str(self.world)]
        listing = self.output("list", *world, "--realm", "app")
        quests = {quest["slug"]: quest for quest in listing["quests"]}
        self.assertEqual(sorted(quests), ["front", "plain", "untitled"])
        self.assertEqual(quests["plain"], {
            "world": str(self.world), "host": None, "realm": "app", "slug": "plain",
            "title": "plain title", "dir": str(root / "plain"), "archived": False})
        self.assertEqual(quests["front"]["title"], "The title")
        self.assertIsNone(quests["untitled"]["title"])
        self.assertEqual(sorted(entry["dir"] for entry in listing["invalid"]),
                         [str(root / "Not_a_slug"), str(root / "no-record")])
        self.assertEqual(listing["failed"], [])

        everything = self.output("list", *world, "--archived")["quests"]
        self.assertEqual(
            sorted((quest["realm"], quest["slug"], quest["archived"]) for quest in everything),
            [("app", "done", True), ("app", "front", False), ("app", "plain", False),
             ("app", "untitled", False), ("other", "elsewhere", False)])

    def test_remote_worlds_run_this_command_there(self):
        remote_world = self.remote_home / "Remote:Projects"
        realm = self.add_realm(remote_world, "far")
        self.add_quest(realm / "quests", "away")
        self.add_quest(self.realm / "quests", "near")
        self.set_worlds([
            {"host": "remote", "path": "Remote:Projects"},
            {"path": str(self.world)},
            {"host": "unreachable", "path": "/srv"},
            {"host": "remote", "path": "/nonexistent"},
        ])

        realms = self.output("realm", "list")
        self.assertEqual(
            sorted((realm["world"], realm["host"], realm["realm"], realm["dir"]) for realm in realms["realms"]),
            [(str(self.world), None, "app", str(self.realm)),
             ("remote:Remote:Projects", "remote", "far", str(realm))])
        self.assertEqual(realms["failed"], [
            {"world": "unreachable:/srv", "host": "unreachable",
             "error": "ssh: Could not resolve hostname unreachable"},
            {"world": "remote:/nonexistent", "host": "remote",
             "error": "/nonexistent: No such file or directory"},
        ])

        quests = self.output("list", "--world", "remote:Remote:Projects", "--realm", "far")
        self.assertEqual(quests, {
            "quests": [{"world": "remote:Remote:Projects", "host": "remote", "realm": "far",
                        "slug": "away", "title": "away title", "dir": str(realm / "quests" / "away"),
                        "archived": False}],
            "invalid": [], "failed": []})

    def test_show(self):
        self.add_quest(self.realm / "quests", "one")
        twin = self.base / "twin"
        self.add_quest(self.add_realm(twin, "app") / "quests", "one")
        self.set_worlds([{"path": str(self.world)}, {"host": "unreachable", "path": "/srv"}])

        result = self.run_quest("show", "app", "one")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["dir"], str(self.realm / "quests" / "one"))
        self.assertEqual(result.stderr, "quest show: could not search unreachable:/srv: "
                                        "ssh: Could not resolve hostname unreachable\n")
        self.assertEqual(self.output("realm", "show", "--world", str(self.world), "app"), {
            "world": str(self.world), "host": None, "realm": "app",
            "dir": str(self.realm), "root": str(self.realm / "quests")})

        both = ["--world", str(self.world), "--world", str(twin)]
        self.assertEqual(
            self.failure("show", *both, "app", "one"),
            f"quest show: quest one in app is in more than one world, so choose one with --world: "
            f"{self.world}, {twin}\n")
        self.assertIn("more than one world", self.failure("realm", "show", *both, "app"))
        self.assertEqual(self.failure("show", *both, "app", "two"), "quest show: no quest two in app\n")
        self.assertEqual(self.failure("realm", "show", *both, "none"), "quest realm show: no realm none\n")


if __name__ == "__main__":
    unittest.main()
