#!/usr/bin/env python3
"""Render one quest-local mise template without provisioning resources."""

import argparse
import os
from pathlib import Path
import re
import sys
import tomllib


def render(template: Path, destination: Path, slug: str, app_port: int) -> None:
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        raise ValueError("slug must be lowercase alphanumeric words separated by hyphens")
    if not 1 <= app_port <= 65535:
        raise ValueError("app port must be between 1 and 65535")

    text = template.read_text(encoding="utf-8")
    text = text.replace("<slug>", slug.replace("-", "_"))
    text = text.replace("<app-port>", str(app_port))
    if re.search(r"<[A-Za-z][A-Za-z0-9_-]*>", text):
        raise ValueError("template contains unresolved placeholders")
    tomllib.loads(text)

    # Exclusive creation also rejects dangling symlinks; never truncate user work.
    fd = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as output:
        output.write(text)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--template", required=True, type=Path)
    parser.add_argument("--destination", required=True, type=Path)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--app-port", required=True, type=int)
    args = parser.parse_args()
    try:
        render(args.template, args.destination, args.slug, args.app_port)
    except (OSError, ValueError) as error:
        # Do not echo TOML content or connection strings in diagnostics.
        if isinstance(error, tomllib.TOMLDecodeError):
            print("error: rendered template is not valid TOML", file=sys.stderr)
        else:
            print(f"error: {error}", file=sys.stderr)
        return 1
    print(f"Rendered {args.destination}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
