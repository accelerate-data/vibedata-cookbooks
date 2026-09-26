#!/usr/bin/env python3
"""Fail when a schema changes incompatibly without raising its top-level version.

Usage: python3 scripts/check_schema_versions.py --base <git-rev>

Each schema/*.schema.json in the working tree is compared with the same file at
<git-rev> (CI passes the merge base). A breaking change needs version + 1; a
non-breaking change keeps the version. Any change this classifier cannot prove
is loosening counts as breaking. An edit inside a format-rule region of the
build scripts counts as a breaking change to recipe.schema.json.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_FILES = ("recipe.schema.json", "catalog.schema.json", "collection.schema.json")
MISSING = object()
ANNOTATIONS = {"title", "description", "$comment", "examples", "version"}
UPPER_BOUNDS = {"maxLength", "maxItems", "maximum", "maxProperties"}
LOWER_BOUNDS = {"minLength", "minItems", "minimum", "minProperties"}
SUBSCHEMA_MAPS = {"properties", "$defs"}
SUBSCHEMAS = {"items", "not", "if", "then", "else", "contains"}
SUBSCHEMA_LISTS = {"allOf", "anyOf", "oneOf", "prefixItems"}
BODY_UPPER = ("max_chars", "max_items")
MARKUP_LISTS = ("forbidden_substrings", "denied_placeholder_names")
FORMAT_RULE_FILES = ("scripts/recipe_format.py", "scripts/build_catalog.py")
FORMAT_BEGIN = "# format-rules: begin"
FORMAT_END = "# format-rules: end"


def _markup_changes(old: dict[str, Any], new: dict[str, Any], where: str) -> list[str]:
    changes = []
    for key in MARKUP_LISTS:
        added = sorted(set(new.get(key, [])) - set(old.get(key, [])))
        if added:
            changes.append(f"{where}/{key}: added {added}")
    for key in sorted((set(old) | set(new)) - set(MARKUP_LISTS)):
        if old.get(key) != new.get(key):
            changes.append(f"{where}/{key}: changed")
    return changes


def body_changes(old: Any, new: Any, where: str) -> list[str]:
    if not isinstance(old, dict) or not isinstance(new, dict):
        return [f"{where}: added or removed"]
    changes: list[str] = []
    for key in sorted((set(old) | set(new)) - {"max_bytes", "sections", "markup"}):
        if old.get(key) != new.get(key):
            changes.append(f"{where}/{key}: changed")
    if new.get("max_bytes", 0) < old.get("max_bytes", 0):
        changes.append(f"{where}/max_bytes: lowered to {new.get('max_bytes')}")
    old_sections, new_sections = old.get("sections", []), new.get("sections", [])
    shape = lambda sections: [(s.get("heading"), s.get("kind"), s.get("field")) for s in sections]  # noqa: E731
    if shape(old_sections) != shape(new_sections):
        changes.append(f"{where}/sections: heading set, order, kind or field changed")
    else:
        for o, n in zip(old_sections, new_sections):
            label = f"{where}/sections/{o['heading']}"
            for key in BODY_UPPER:
                if key in n and (key not in o or n[key] < o[key]):
                    changes.append(f"{label}/{key}: lowered to {n[key]}")
            if "min_items" in n and ("min_items" not in o or n["min_items"] > o["min_items"]):
                changes.append(f"{label}/min_items: raised to {n['min_items']}")
            added = sorted(set(n.get("forbid", [])) - set(o.get("forbid", [])))
            if added:
                changes.append(f"{label}/forbid: added {added}")
            other = (set(o) | set(n)) - {"heading", "kind", "field", "min_items", "forbid", *BODY_UPPER}
            for key in sorted(other):
                if o.get(key) != n.get(key):
                    changes.append(f"{label}/{key}: changed")
    changes += _markup_changes(old.get("markup", {}), new.get("markup", {}), f"{where}/markup")
    return changes


def breaking_changes(base: Any, head: Any, path: str = "#") -> list[str]:
    """List the breaking differences from base to head; empty means compatible."""
    if not isinstance(base, dict) or not isinstance(head, dict):
        return [] if base == head else [f"{path}: changed"]
    changes: list[str] = []
    for key in sorted(set(base) | set(head)):
        where = f"{path}/{key}"
        old, new = base.get(key, MISSING), head.get(key, MISSING)
        if key in ANNOTATIONS or old == new:
            continue
        if key == "x-body":
            changes += body_changes(old, new, where)
        elif key in SUBSCHEMA_MAPS:
            old_map = {} if old is MISSING else old
            new_map = {} if new is MISSING else new
            for name in sorted(old_map):
                if name not in new_map:
                    changes.append(f"{where}/{name}: removed")
                else:
                    changes += breaking_changes(old_map[name], new_map[name], f"{where}/{name}")
        elif key == "required":
            added = sorted(set([] if new is MISSING else new) - set([] if old is MISSING else old))
            if added:
                changes.append(f"{where}: newly required {added}")
        elif key == "enum":
            if old is MISSING:
                changes.append(f"{where}: enum added")
            elif new is not MISSING:
                removed = [value for value in old if value not in new]
                if removed:
                    changes.append(f"{where}: values removed {removed}")
        elif key in UPPER_BOUNDS:
            if new is not MISSING and (old is MISSING or new < old):
                changes.append(f"{where}: lowered to {new}")
        elif key in LOWER_BOUNDS:
            if new is not MISSING and (old is MISSING or new > old):
                changes.append(f"{where}: raised to {new}")
        elif key == "additionalProperties":
            o = True if old is MISSING else old
            n = True if new is MISSING else new
            if n is True or o is False:
                continue
            if isinstance(o, dict) and isinstance(n, dict):
                changes += breaking_changes(o, n, where)
            else:
                changes.append(f"{where}: tightened")
        elif key == "uniqueItems":
            if new is True:
                changes.append(f"{where}: now true")
        elif key in SUBSCHEMAS and old is not MISSING and new is not MISSING:
            changes += breaking_changes(old, new, where)
        elif key in SUBSCHEMA_LISTS and isinstance(old, list) and isinstance(new, list) and len(old) == len(new):
            for index, (o, n) in enumerate(zip(old, new)):
                changes += breaking_changes(o, n, f"{where}/{index}")
        else:
            changes.append(f"{where}: changed")
    return changes


def _git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True)


def _is_version(value: Any) -> bool:
    return type(value) is int and value >= 1


def format_rule_regions(text: str) -> list[str] | None:
    """Return the text of each marked format-rule region, or None when the markers are unbalanced."""
    regions: list[str] = []
    current: list[str] | None = None
    for line in text.split("\n"):
        marker = line.strip()
        if marker == FORMAT_BEGIN:
            if current is not None:
                return None
            current = []
        elif marker == FORMAT_END:
            if current is None:
                return None
            regions.append("\n".join(current))
            current = None
        elif current is not None:
            current.append(line)
    return None if current is not None else regions


def format_rule_changes(root: Path, base_rev: str) -> list[str]:
    """List edits, relative to base_rev, to the code that enforces the prose file and line rules.

    Those rules are not x-body data, so readers hard-code them; an edit is a breaking
    change to recipe.schema.json. A base without markers has nothing to compare.
    """
    changes: list[str] = []
    for rel in FORMAT_RULE_FILES:
        head_path = root / rel
        head = format_rule_regions(head_path.read_text(encoding="utf-8")) if head_path.exists() else []
        shown = _git(root, "show", f"{base_rev}:{rel}")
        base = format_rule_regions(shown.stdout) if shown.returncode == 0 else []
        if head is None:
            changes.append(f"{rel}: unbalanced '{FORMAT_BEGIN}' / '{FORMAT_END}' markers")
        elif not base:
            continue
        elif not head:
            changes.append(f"{rel}: format-rule regions removed")
        elif head != base:
            changes.append(f"{rel}: format-rule region changed")
    return changes


def check_versions(root: Path, base_rev: str) -> list[str]:
    if _git(root, "rev-parse", "--verify", "--quiet", f"{base_rev}^{{commit}}").returncode != 0:
        return [f"base revision {base_rev!r} is not a commit"]
    format_changes = format_rule_changes(root, base_rev)
    errors: list[str] = []
    for name in SCHEMA_FILES:
        rel = f"schema/{name}"
        shown = _git(root, "show", f"{base_rev}:{rel}")
        base_text = shown.stdout if shown.returncode == 0 else None
        head_path = root / rel
        if not head_path.exists():
            if base_text is not None:
                errors.append(f"{rel}: removed; a published schema cannot be deleted")
            continue
        head = json.loads(head_path.read_text(encoding="utf-8"))
        head_version = head.get("version")
        if not _is_version(head_version):
            errors.append(f"{rel}: top-level 'version' must be an integer >= 1")
            continue
        if base_text is None:
            if head_version != 1:
                errors.append(f"{rel}: a new schema starts at version 1, not {head_version}")
            continue
        base = json.loads(base_text)
        base_version = base.get("version")
        if base_version is None:
            if head_version != 1:
                errors.append(f"{rel}: the first versioned schema is version 1, not {head_version}")
            continue
        breaking = breaking_changes(base, head)
        if name == "recipe.schema.json":
            breaking += format_changes
        if breaking and head_version != base_version + 1:
            errors.append(
                f"{rel}: breaking change without a version bump to {base_version + 1} "
                f"(found {head_version}): " + "; ".join(breaking)
            )
        elif not breaking and head_version != base_version:
            errors.append(f"{rel}: version changed from {base_version} to {head_version} without a breaking change")
    return errors


def main(argv: list[str] | None = None, root: Path = ROOT) -> int:
    parser = argparse.ArgumentParser(description="Fail on a breaking schema change without a version bump.")
    parser.add_argument("--base", required=True, help="git revision to compare against, normally the merge base")
    args = parser.parse_args(argv)
    errors = check_versions(root, args.base)
    for error in errors:
        print(f"schema version error: {error}", file=sys.stderr)
    if not errors:
        print(f"schema versions consistent with {args.base}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
