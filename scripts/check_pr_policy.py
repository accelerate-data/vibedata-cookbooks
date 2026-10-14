#!/usr/bin/env python3
"""Fail a pull request into pre-prod that breaks the publication policy.

Usage: python3 scripts/check_pr_policy.py --event "$GITHUB_EVENT_PATH" [--changed-files PATH]

Two rules apply to pull requests whose base is pre-prod (promotion pull
requests from pre-prod are out of scope):
- catalog.json is regenerated after merge, so a pull request must not edit it.
- A pull request that adds or edits recipes/*/recipe.md needs the six evidence
  sections in its description, each non-empty.

The description is read only from the event file. Without --changed-files, the
changed files come from git diff between the event's base and head SHAs;
deleted files are excluded.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from fnmatch import fnmatchcase
from pathlib import Path
from typing import Any

EVIDENCE_HEADINGS: tuple[str, ...] = (
    "Summary",
    "Distinct outcome and overlap",
    "Readiness and required capabilities",
    "Platform compatibility",
    "Implementation example and execution evidence",
    "Limitations and material risks",
)

HEADING = re.compile(r"^## (.+?)\s*$")
COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)


def sections(body: str | None) -> dict[str, str]:
    """Map each '## ' heading outside a code fence to its section text."""
    found: dict[str, list[str]] = {}
    current: list[str] | None = None
    fenced = False
    for line in (body or "").replace("\r\n", "\n").split("\n"):
        if line.startswith(("```", "~~~")):
            fenced = not fenced
        match = None if fenced else HEADING.match(line)
        if match:
            current = found.setdefault(match.group(1), [])
        elif current is not None:
            current.append(line)
    return {name: "\n".join(lines) for name, lines in found.items()}


def in_scope(pr: dict[str, Any]) -> bool:
    return pr.get("base", {}).get("ref") == "pre-prod" and pr.get("head", {}).get("ref") != "pre-prod"


def check(event: dict[str, Any], changed_files: list[str]) -> list[str]:
    """Return policy errors for a pull_request event; an empty list means pass."""
    pr = event.get("pull_request") or {}
    if not in_scope(pr):
        return []
    errors: list[str] = []
    if "catalog.json" in changed_files:
        errors.append(
            "catalog.json is regenerated after merge (docs/adr/0003-catalog-generated-after-merge.md); "
            "remove it from this pull request."
        )
    if any(fnmatchcase(path, "recipes/*/recipe.md") for path in changed_files):
        found = sections(pr.get("body"))
        for heading in EVIDENCE_HEADINGS:
            if heading not in found:
                errors.append(
                    f"PR description is missing the '## {heading}' section (see .github/pull_request_template.md)."
                )
            elif not COMMENT.sub("", found[heading]).strip():
                errors.append(
                    f"PR description section '## {heading}' is empty; for a planned Recipe write 'Not applicable: planned'."
                )
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--event", required=True, type=Path, help="path to the GitHub event JSON")
    parser.add_argument("--changed-files", type=Path, help="newline list of changed files (default: git diff)")
    args = parser.parse_args(argv)
    event = json.loads(args.event.read_text(encoding="utf-8"))
    pr = event.get("pull_request")
    if not pr or not in_scope(pr):
        return 0  # no pull request, or out of scope: git is not needed
    if args.changed_files:
        changed = args.changed_files.read_text(encoding="utf-8").splitlines()
    else:
        diff = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=d", f"{pr['base']['sha']}...{pr['head']['sha']}"],
            capture_output=True, text=True, check=True,
        )
        changed = diff.stdout.splitlines()
    errors = check(event, changed)
    for error in errors:
        print(f"::error::{error}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
