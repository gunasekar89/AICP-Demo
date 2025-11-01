"""Utility script to locate text within the repository without external tools."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Iterable


def iter_text_files(root: Path) -> Iterable[Path]:
    """Yield files under ``root`` that appear to be text files."""

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        # Heuristic: skip common binary directories
        if any(part.startswith(".") for part in path.parts[1:]):
            # still allow .env etc? maybe we skip hidden? maybe not? we skip .git though
            continue
        try:
            with path.open("r", encoding="utf-8") as handle:
                handle.read(1024)
        except (UnicodeDecodeError, OSError):
            continue
        yield path


def find_string(root: Path, needle: str, case_sensitive: bool) -> list[tuple[Path, int, str]]:
    """Return a list of matches as tuples of (path, line number, line text)."""

    matches: list[tuple[Path, int, str]] = []
    comparison = (lambda value: value) if case_sensitive else (lambda value: value.lower())
    search_term = comparison(needle)

    for path in iter_text_files(root):
        try:
            with path.open("r", encoding="utf-8") as handle:
                for index, line in enumerate(handle, start=1):
                    haystack = comparison(line)
                    if search_term in haystack:
                        matches.append((path, index, line.rstrip()))
        except UnicodeDecodeError:
            continue
    return matches


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Search for a string inside the repository without relying on ripgrep."
        )
    )
    parser.add_argument(
        "needle",
        help="Text to look for (for example: 'AI-SecOps Command Center').",
    )
    parser.add_argument(
        "--case-sensitive",
        action="store_true",
        help="Make the search case-sensitive (default ignores case).",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Root directory to search (defaults to the current working directory).",
    )

    args = parser.parse_args()
    matches = find_string(args.root.resolve(), args.needle, args.case_sensitive)

    if not matches:
        print(f"No matches found for '{args.needle}'.")
        return

    for path, line_number, line_text in matches:
        relative_path = os.path.relpath(path, args.root)
        print(f"{relative_path}:{line_number}: {line_text}")


if __name__ == "__main__":
    main()
