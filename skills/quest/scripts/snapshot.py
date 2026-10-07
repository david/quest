#!/usr/bin/env python3
"""Commit each active quest's records to that quest's own Git repository."""

import argparse
import contextlib
import fcntl
import os
from pathlib import Path
import re
import subprocess
import sys
import time


SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
DECLARATION = re.compile(r"^\s*Quest root:\s*([^\r\n]+)$", re.MULTILINE)
INSTRUCTIONS = ("AGENTS.md", "CLAUDE.md")
DEFAULT_RULES = Path(__file__).resolve().parents[1] / "assets" / "snapshot-exclude"
UNSCANNED = {".git", "work", "local-data", "node_modules", ".cache", "__pycache__"}
ROUTING = {
    "GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_COMMON_DIR",
    "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_PREFIX",
}
LOCK_WAIT_SECONDS = 30
# surrogateescape carries bytes that are not UTF-8, as in file names, through unchanged.
TEXT = {"encoding": "utf-8", "errors": "surrogateescape"}


class SnapshotError(Exception):
    pass


def git(directory: Path, *args: str, check: bool = True, stdin: str = "") -> str | None:
    # Never inherit a caller's alternate Git repository or index.
    env = {key: value for key, value in os.environ.items() if key not in ROUTING}
    result = subprocess.run(
        ["git", "-C", str(directory), *args],
        env=env, input=stdin, capture_output=True, **TEXT,
    )
    if result.returncode:
        if not check:
            return None
        detail = result.stderr.strip() or f"exit status {result.returncode}"
        raise SnapshotError(f"git {' '.join(args)}: {detail}")
    return result.stdout.rstrip("\n")


def is_quest(directory: Path) -> bool:
    parent = directory.parent
    return (
        SLUG.fullmatch(directory.name) is not None
        and (directory / "QUEST.md").exists()
        and (parent.name == "quests"
             or (parent.name == ".archived" and parent.parent.name == "quests"))
    )


def find_root(directory: Path) -> Path | None:
    directory = Path(os.path.realpath(directory))
    ancestors = [directory, *directory.parents]
    for ancestor in ancestors:
        if is_quest(ancestor):
            parent = ancestor.parent
            return parent.parent if parent.name == ".archived" else parent
    # Read known instruction paths; never search checkouts for more.
    for ancestor in ancestors:
        for name in INSTRUCTIONS:
            try:
                declared = DECLARATION.findall((ancestor / name).read_text(encoding="utf-8"))
            except (OSError, UnicodeDecodeError):
                continue
            if declared:
                value = re.sub(r"^`(.*)`$", r"\1", declared[-1].strip())
                root = Path(os.path.realpath(ancestor / value))
                if root.name != "quests" or not root.is_dir():
                    raise SnapshotError(f"invalid Quest root declaration in {ancestor / name}")
                return root
    for candidate in (directory, Path(os.path.realpath(directory / "quests"))):
        if candidate.name == "quests" and candidate.is_dir():
            return candidate
    return None


def active_quests(root: Path) -> list[Path]:
    with os.scandir(root) as entries:
        names = sorted(entry.name for entry in entries if entry.is_dir(follow_symlinks=False))
    return [root / name for name in names if is_quest(root / name)]


@contextlib.contextmanager
def locked(directory: Path):
    # A kernel lock on the directory itself: it needs no lock file and is
    # released when this process dies.
    descriptor = os.open(directory, os.O_RDONLY | os.O_DIRECTORY)
    try:
        deadline = time.monotonic() + LOCK_WAIT_SECONDS
        while True:
            try:
                fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                if time.monotonic() >= deadline:
                    raise SnapshotError(f"timed out waiting for the lock on {directory}") from None
                time.sleep(0.05)
        yield
    finally:
        os.close(descriptor)


def ignore_pattern(relative: str) -> str:
    escaped = re.sub(r"[\[\]*?! #]", r"\\\g<0>", relative.replace("\\", "\\\\"))
    return f"/{escaped}/"


def append_missing(file: Path, line: str) -> None:
    content = file.read_text(**TEXT) if file.exists() else ""
    if line not in content.splitlines():
        file.parent.mkdir(parents=True, exist_ok=True)
        separator = "\n" if content and not content.endswith("\n") else ""
        with file.open("a", **TEXT) as output:
            output.write(f"{separator}{line}\n")


def exclude_from_enclosing(root: Path) -> None:
    seen = set()
    for directory in (root, *root.parents):
        if not (directory / ".git").exists():
            continue
        top = Path(os.path.realpath(git(directory, "rev-parse", "--show-toplevel")))
        if top in seen:
            continue
        seen.add(top)
        if top == root:
            raise SnapshotError(f"quest storage must not itself be a repository: {root}")
        relative = str(root.relative_to(top))
        common = Path(os.path.realpath(top / git(top, "rev-parse", "--git-common-dir")))
        with locked(common):
            if git(top, "ls-files", "-z", "--", f":(literal){relative}"):
                raise SnapshotError(
                    f"{top} tracks quest storage {root}; automatic untracking is refused")
            append_missing(common / "info" / "exclude", ignore_pattern(relative))
            if git(top, "check-ignore", "-q", "--", f"{root}/", check=False) is None:
                raise SnapshotError(f"{top} does not ignore quest storage {root}")


def nested_repositories(quest: Path, prefix: str = "") -> list[str]:
    found = []
    with os.scandir(quest / prefix) as entries:
        names = [entry.name for entry in entries
                 if entry.is_dir(follow_symlinks=False) and entry.name not in UNSCANNED]
    for name in names:
        relative = os.path.join(prefix, name)
        directory = quest / relative
        bare = all((directory / part).exists() for part in ("HEAD", "objects", "refs"))
        if os.path.lexists(directory / ".git") or bare:
            found.append(relative)
        else:
            found.extend(nested_repositories(quest, relative))
    return found


def snapshot(quest: Path, default_rules: str) -> str | None:
    """Commit the quest's records; return the subject, or None if nothing changed."""
    with locked(quest):
        dotgit = quest / ".git"
        if not os.path.lexists(dotgit):
            git(quest, "init", "--quiet")
        if dotgit.is_symlink() or not dotgit.is_dir():
            raise SnapshotError("the quest does not own its repository")

        def run(*args: str, check: bool = True, stdin: str = "") -> str | None:
            # Pinned, so a broken .git never sends a command to an enclosing repository.
            return git(quest, "--git-dir=.git", "--work-tree=.", *args, check=check, stdin=stdin)

        def has_gitlink() -> bool:
            return any(line.startswith("160000 ") for line in run("ls-files", "--stage").splitlines())

        if not run("--no-optional-locks", "status", "--porcelain"):
            return None

        # The script owns this file and replaces it whenever it differs, so a
        # change to the defaults reaches every quest. A quest's own rules live
        # in its .gitignore, which Git reads with higher precedence.
        rules = default_rules + "".join(
            f"{ignore_pattern(path)}\n" for path in sorted(nested_repositories(quest)))
        exclude = dotgit / "info" / "exclude"
        if not exclude.is_file() or exclude.read_text(**TEXT) != rules:
            exclude.parent.mkdir(exist_ok=True)
            exclude.write_text(rules, **TEXT)
        if has_gitlink():
            raise SnapshotError(
                "the quest tracks a nested repository; automatic untracking is refused")
        # A rule added after a file was recorded takes it out of later snapshots.
        # Earlier snapshots and the file itself are kept.
        ignored = run("ls-files", "-z", "-ci", "--exclude-standard")
        if ignored:
            run("update-index", "--force-remove", "-z", "--stdin", stdin=ignored)
        # Includes deletions and other writers' partial edits by design.
        run("add", "-A", "--", ".")
        if has_gitlink():
            raise SnapshotError("a nested repository appeared while staging; refusing to record it")

        tree = run("write-tree")
        parent = run("rev-parse", "--verify", "--quiet", "HEAD", check=False)
        base = parent or run("hash-object", "-t", "tree", "/dev/null")
        if tree == run("rev-parse", f"{base}^{{tree}}"):
            return None
        changed = [path for path in run(
            "diff-tree", "--no-commit-id", "--name-only", "-r", "-z", base, tree).split("\0") if path]
        subject = "{} quest records: {} path{} ({})".format(
            "Snapshot" if parent else "Initialize", len(changed),
            "" if len(changed) == 1 else "s", ", ".join(changed[:2]))
        subject = re.sub(r"[\x00-\x1f\x7f\udc80-\udcff]", "?", subject)[:100]

        # Commit exactly the tree summarized above. update-ref is compare-and-swap,
        # so a writer outside this lock cannot be overwritten.
        signing = run("config", "--bool", "--get", "commit.gpgsign", check=False) == "true"
        commit = run(
            "commit-tree", tree, *(["-p", parent] if parent else []),
            *(["-S"] if signing else []), "-m", subject)
        run("update-ref", "-m", subject, "HEAD", commit, parent or "0" * len(commit))
        return subject


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "directory", nargs="*", type=Path,
        help="resolve the quest root from here (default: the current directory)")
    args = parser.parse_args()

    failed = False

    def report(subject: Path, error: Exception) -> None:
        nonlocal failed
        failed = True
        print(f"quest snapshot: {subject}: {error}", file=sys.stderr)

    roots = []
    for directory in args.directory or [Path(".")]:
        try:
            root = find_root(directory)
        except FileNotFoundError:
            # A session can outlive its directory, as when its quest is archived.
            continue
        except (OSError, SnapshotError) as error:
            report(directory, error)
            continue
        if root and root not in roots:
            roots.append(root)

    if not roots:
        return 1 if failed else 0
    try:
        default_rules = DEFAULT_RULES.read_text(**TEXT)
    except OSError as error:
        report(DEFAULT_RULES, error)
        return 1
    if not default_rules.endswith("\n"):
        default_rules += "\n"

    for root in roots:
        try:
            exclude_from_enclosing(root)
            quests = active_quests(root)
        except (OSError, SnapshotError) as error:
            report(root, error)
            continue
        for quest in quests:
            try:
                subject = snapshot(quest, default_rules)
            except (OSError, SnapshotError) as error:
                report(quest, error)
            else:
                if subject:
                    print(f"{quest.name}: {subject}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
