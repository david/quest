#!/usr/bin/env python3
"""Report what archiving a quest would remove, and what that would lose."""

import argparse
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
ROUTING = {
    "GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_COMMON_DIR", "GIT_NAMESPACE",
    "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_PREFIX",
}
LISTED = 20
FETCH_SECONDS = 120
# surrogateescape carries bytes that are not UTF-8, as in file names, through unchanged.
TEXT = {"encoding": "utf-8", "errors": "surrogateescape"}
# The trial rebase runs in a throwaway copy, without the user's Git configuration,
# which could sign commits, run hooks, or change how the rebase goes.
ISOLATED = {
    "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_AUTHOR_NAME": "archive check", "GIT_AUTHOR_EMAIL": "archive-check@example.invalid",
    "GIT_COMMITTER_NAME": "archive check", "GIT_COMMITTER_EMAIL": "archive-check@example.invalid",
}


class CheckError(Exception):
    pass


def git(directory: Path, *args: str, check: bool = True, stdin: str = "",
        env: dict[str, str] | None = None, timeout: int | None = None) -> str | None:
    # Never inherit a caller's alternate Git repository or index, never refresh
    # an index or start a file monitor while inspecting, and never wait at a
    # credential prompt.
    environment = {key: value for key, value in os.environ.items() if key not in ROUTING}
    environment |= {"GIT_OPTIONAL_LOCKS": "0", "GIT_TERMINAL_PROMPT": "0", **(env or {})}
    try:
        result = subprocess.run(
            ["git", "-C", str(directory), "-c", "core.fsmonitor=false", *args],
            env=environment, input=stdin, capture_output=True, timeout=timeout, **TEXT,
        )
    except subprocess.TimeoutExpired:
        raise CheckError(f"git {args[0]} in {directory}: no answer in {timeout} seconds") from None
    if result.returncode:
        if not check:
            return None
        detail = result.stderr.strip() or f"exit status {result.returncode}"
        raise CheckError(f"git {args[0]} in {directory}: {detail}")
    return result.stdout.rstrip("\n")


def lines(output: str | None) -> list[str]:
    # str.splitlines would also break at form feeds and other separators that a
    # commit subject or a branch name may contain.
    return output.split("\n") if output else []


class Report:
    def __init__(self, quest: Path):
        self.quest = quest
        self.findings = 0

    def name(self, path: Path) -> str:
        return str(path.relative_to(self.quest)) if path.is_relative_to(self.quest) else str(path)

    def note(self, text: str, details: list[str] | None = None,
             mark: str = " ", limit: int | None = LISTED) -> None:
        details = details or []
        print(f"  {mark} {text}")
        for detail in details[:limit]:
            print(f"        {detail}")
        if limit is not None and len(details) > limit:
            print(f"        and {len(details) - limit} more")

    def finding(self, text: str, details: list[str] | None = None) -> None:
        self.findings += 1
        self.note(text, details, mark="!")


def count(number: int, noun: str, plural: str = "") -> str:
    return f"{number} {noun if number == 1 else plural or noun + 's'}"


def natural(path: Path) -> tuple[int, int, str]:
    numbered = path.name.isascii() and path.name.isdigit()
    return (0, int(path.name), "") if numbered else (1, 0, path.name)


def registrations(checkout: Path) -> list[dict[str, str]]:
    """Every worktree of the checkout's repository; the main one comes first."""
    entries, entry = [], {}
    for line in [*lines(git(checkout, "worktree", "list", "--porcelain")), ""]:
        if line:
            key, _, value = line.partition(" ")
            entry[key] = value
        elif entry:
            entries.append(entry)
            entry = {}
    return entries


def common_directory(checkout: Path, check: bool = False) -> Path | None:
    """The repository a checkout belongs to, or None when it is not the top of one."""
    if not os.path.lexists(checkout / ".git"):
        return None
    found = git(
        checkout, "rev-parse", "--path-format=absolute", "--show-toplevel", "--git-common-dir",
        check=check)
    if found is None:
        return None
    top, common = lines(found)
    return Path(os.path.realpath(common)) if Path(os.path.realpath(top)) == checkout else None


def status(checkout: Path) -> list[str]:
    """Uncommitted paths, untracked ones included."""
    fields = iter(git(checkout, "status", "--porcelain=v1", "-z", "--untracked-files=all").split("\0"))
    changed = []
    for field in fields:
        if field:
            changed.append(field)
            if "R" in field[:2] or "C" in field[:2]:
                next(fields, None)  # The path it was renamed or copied from.
    return changed


def show_checkout(report: Report, path: Path, kind: str) -> None:
    head = git(path, "rev-parse", "--short", "--verify", "--quiet", "HEAD", check=False)
    branch = git(path, "symbolic-ref", "--quiet", "--short", "HEAD", check=False)
    print(f"{report.name(path)}: {kind}, {'on ' + branch if branch else 'detached'}"
          f" at {head or 'no commit'}")
    changed = status(path)
    if changed:
        report.finding(count(len(changed), "uncommitted path"), changed)


def find_target(report: Report, repository: Path, name: str) -> str | None:
    """The commit of a remote's branch, fetched first."""
    remote, _, branch = name.partition("/")
    if branch and remote in lines(git(repository, "remote")):
        try:
            git(repository, "fetch", "--quiet", "--no-tags", "--no-write-fetch-head", remote,
                f"+refs/heads/{branch}:refs/remotes/{name}", timeout=FETCH_SECONDS)
        except CheckError as error:
            report.finding(f"could not fetch {name}; merge status is as of the last fetch",
                           [lines(str(error))[-1]])
    # Nothing local can be the target: a local branch or tag of the same name
    # could hold the very work that is about to be removed.
    return git(
        repository, "rev-parse", "--verify", "--quiet", f"refs/remotes/{name}^{{commit}}", check=False)


def is_ancestor(repository: Path, tip: str, target: str) -> bool:
    return git(repository, "merge-base", "--is-ancestor", tip, target, check=False) is not None


def rebase(copy: Path, target: str) -> list[str] | None:
    """The subjects of the commits that rebasing HEAD onto the target keeps,
    or None when the rebase stops at a conflict."""
    try:
        git(copy, "rebase", "--quiet", target, env=ISOLATED)
    except CheckError:
        if not git(copy, "ls-files", "--unmerged"):
            raise
        git(copy, "rebase", "--abort", env=ISOLATED)
        return None
    kept = git(copy, "log", "--format=%H %s", f"{target}..HEAD")
    return [line.split(" ", 1)[1] for line in lines(kept)]


def unmerged(copy: Path, tip: str, target: str) -> list[str] | None:
    """What a rebase of the tip onto the target keeps: nothing when the target has
    the work, the subjects of the commits it lacks, or None for a conflict."""
    # A rebase leaves out commits whose patch the target has, and commits that
    # change nothing there, which covers rebased work.
    git(copy, "switch", "--quiet", "--detach", tip, env=ISOLATED)
    kept = rebase(copy, target)
    if kept == []:
        return kept
    # Work squashed into one commit on the target need not rebase commit by
    # commit, so squash it here too and try again. Work that cancels itself
    # out squashes to nothing, which says nothing about whether the target has it.
    base = git(copy, "merge-base", target, tip, check=False)
    git(copy, "switch", "--quiet", "--detach", tip, env=ISOLATED)
    if base and git(copy, "diff", "--quiet", base, tip, check=False) is None:
        git(copy, "reset", "--quiet", "--soft", base)
        git(copy, "commit", "--quiet", "--message", "Squashed", env=ISOLATED)
        if rebase(copy, target) == []:
            return []
    return kept


def commits(repository: Path, include: list[str], exclude: list[str], *options: str) -> list[str]:
    revisions = [*include, *(f"^{commit}" for commit in exclude)]
    return lines(git(repository, "rev-list", *options, "--stdin", stdin="\n".join(revisions) + "\n"))


def held_by(source: Path, repository: Path) -> list[str]:
    """Commits in the repository that the source also keeps on a ref, reflog, or stash."""
    tips = git(source, "rev-list", "--no-walk", "--all", "--reflog").split()
    present = git(repository, "cat-file", "--batch-check", stdin="".join(f"{tip}\n" for tip in tips))
    return [line.split()[0] for line in lines(present) if " commit " in line]


def show_repository(report: Report, common: Path, main: Path, owned: bool,
                    checkouts: list[tuple[Path, dict[str, str]]],
                    args: argparse.Namespace, scratch: Path) -> None:
    via, target = checkouts[0][0], args.target
    if owned:
        print(f"Repository {report.name(common)}: the quest's own, removed with its checkouts")
    else:
        print(f"Repository {common}: outside the quest, and outlives it")
        report.note(f"remove a worktree with: git -C {main} worktree remove <path>")
    target_commit = find_target(report, via, target)
    held = held_by(args.source, via) if owned and args.source else []

    # A repository the quest owns is removed whole, so every local branch counts.
    # In any other, only what the quest has checked out is known to be its own.
    places: dict[str, list[str]] = {}
    tips: list[tuple[str, str]] = []
    for path, entry in checkouts:
        if "branch" in entry:
            places.setdefault(entry["branch"], []).append(report.name(path))
        elif entry.get("HEAD", "0").strip("0"):
            tips.append((f"detached HEAD of {report.name(path)}", entry["HEAD"]))
    for line in lines(git(via, "for-each-ref", "--format=%(objectname) %(refname)", "refs/heads")):
        commit, ref = line.split(" ", 1)
        if owned or ref in places:
            where = f" ({', '.join(places[ref])})" if ref in places else ""
            tips.append((ref.removeprefix("refs/heads/") + where, commit))

    copy = None
    for label, tip in tips:
        if target_commit is None:
            report.finding(f"{label}: there is no remote branch {target} to compare it with")
        elif is_ancestor(via, tip, target_commit):
            report.note(f"{label}: merged into {target}")
        elif not commits(via, [tip], [target_commit, *held]):
            report.note(f"{label}: not in {target}, but {args.source} keeps it")
        else:
            if copy is None:
                copy = Path(tempfile.mkdtemp(dir=scratch))
                git(copy, "clone", "--quiet", "--shared", "--no-checkout", str(common), ".", env=ISOLATED)
            kept = unmerged(copy, tip, target_commit)
            if kept is None:
                report.finding(f"{label}: conflicts when rebased onto {target}")
            elif kept:
                report.finding(f"{label}: {count(len(kept), 'commit')} not in {target}", kept)
            else:
                report.note(f"{label}: merged into {target}, as other commits")

    if owned:
        stashes = [
            line.split(" ", 1)[1] for line in lines(git(via, "stash", "list", "--format=%H %gd: %gs"))
            if line.split()[0] not in held]
        if stashes:
            report.finding(count(len(stashes), "stash entry", "stash entries"), stashes)


def processes(directories: list[Path]) -> list[str] | None:
    try:
        pids = sorted(int(name) for name in os.listdir("/proc") if name.isascii() and name.isdigit())
    except OSError:
        return None
    found = []
    for pid in pids:
        try:
            cwd = Path(os.readlink(f"/proc/{pid}/cwd"))
            name = Path(f"/proc/{pid}/comm").read_text(**TEXT).strip()
        except OSError:
            continue
        if pid != os.getpid() and any(cwd.is_relative_to(directory) for directory in directories):
            found.append(f"{pid} {name}{' (ran this check)' if pid == os.getppid() else ''}: {cwd}")
    return found


def check(args: argparse.Namespace) -> int:
    if args.quest.is_symlink():
        raise CheckError(f"{args.quest} is a symbolic link")
    quest = Path(os.path.realpath(args.quest))
    root = quest.parent
    if not (SLUG.fullmatch(quest.name) and root.name == "quests" and (quest / "QUEST.md").is_file()):
        raise CheckError(f"{quest} is not an active quest directory")
    destination = root / ".archived" / quest.name
    if (root / ".archived").is_symlink() or os.path.lexists(destination):
        raise CheckError(f"{destination} exists already, or .archived is a symbolic link")
    worktrees = quest / "worktrees"
    if worktrees.is_symlink():
        raise CheckError(f"{worktrees} is a symbolic link")
    if args.source:
        kept = git(args.source, "rev-parse", "--path-format=absolute", "--git-common-dir")
        if Path(os.path.realpath(kept)).is_relative_to(quest):
            raise CheckError(f"{args.source} is inside the quest, so it keeps nothing once the quest is archived")

    # Every directory in worktrees/, then every other worktree of a repository the quest owns.
    repositories: dict[Path, list[Path]] = {}
    strays = []
    for entry in sorted(worktrees.iterdir(), key=natural) if worktrees.is_dir() else []:
        if entry.is_dir() and not entry.is_symlink() and os.path.lexists(entry / ".git"):
            common = common_directory(entry, check=True)
            if common is None:
                raise CheckError(f"{entry} is not the top of its checkout")
            repositories.setdefault(common, []).append(entry)
        elif entry.is_symlink() or not entry.is_dir() or any(entry.iterdir()):
            strays.append(entry)
    found: dict[Path, tuple[Path, dict[str, str]]] = {}
    mains: dict[Path, Path] = {}
    for common, paths in repositories.items():
        listed = registrations(paths[0])
        mains[common] = Path(os.path.realpath(listed[0]["worktree"]))
        for entry in listed:
            path = Path(os.path.realpath(entry["worktree"]))
            # A copied clone still lists the worktrees of the repository it was
            # copied from. Only one whose own .git leads back here belongs to it.
            if path in paths or (common.is_relative_to(quest) and common_directory(path) == common):
                found[path] = (common, entry)
        for path in paths:
            if path not in found:
                raise CheckError(f"{path} is not registered in {common}")

    report = Report(quest)
    print(f"Quest {quest}\nArchives to {destination}\n")
    for path in sorted(found, key=lambda path: (not path.is_relative_to(worktrees), natural(path))):
        main = mains[found[path][0]]
        show_checkout(report, path, "clone" if path == main else f"worktree of {report.name(main)}")
        if not path.is_relative_to(worktrees):
            report.finding("outside the quest's worktrees/; removing its repository breaks it")
    if not found:
        print("No checkouts in worktrees/.")
    if strays:
        report.finding("in worktrees/ but not a checkout, so removed with it:",
                       [report.name(entry) for entry in strays])

    with tempfile.TemporaryDirectory() as scratch:
        for common in repositories:
            print()
            show_repository(
                report, common, mains[common], common.is_relative_to(quest),
                [(path, entry) for path, (owner, entry) in found.items() if owner == common],
                args, Path(scratch))

    print()
    running = processes(list(found))
    if running is None:
        print("Processes: not checked, because this system has no /proc.")
    elif running:
        report.finding("processes with a working directory in a checkout:", running)
    else:
        print("Processes: none has a working directory in a checkout.")
    print(f"\n{count(report.findings, 'finding')}, marked \"!\"." if report.findings else "\nNo findings.")
    return report.findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("quest", type=Path, help="the quest directory")
    parser.add_argument(
        "--target", default="origin/main",
        help="the remote branch the quest's work is merged into (default: origin/main)")
    parser.add_argument(
        "--source", type=Path,
        help="the repository a clone was copied from; commits it keeps are not the quest's")
    args = parser.parse_args()
    sys.stdout.reconfigure(errors="backslashreplace")
    try:
        return 1 if check(args) else 0
    except Exception as error:
        # Any failure, a bug included, must not pass for the status that means findings.
        detail = str(error) if isinstance(error, (OSError, CheckError)) else repr(error)
        print(f"archive check: stopped, so any report above is incomplete: {detail}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
