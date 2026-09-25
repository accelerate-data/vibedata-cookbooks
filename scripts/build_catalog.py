#!/usr/bin/env python3
"""Validate the cookbook and generate catalog.json from Recipe frontmatter.

Run `python3 scripts/build_catalog.py` to regenerate catalog.json, or pass
`--check` to fail when catalog.json differs from a fresh build. The contract
rules live in schema/*.json; this script applies them.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

from recipe_format import CookbookError, check_markup, load_frontmatter, parse_body, split_frontmatter

ROOT = Path(__file__).resolve().parents[1]
REPO_URL = "https://github.com/accelerate-data/vibedata-cookbooks"
SCHEMA_NAMES = ("recipe", "catalog", "collection")
RECIPE_FILE = "recipe.md"
COUNTED_READINESS = {"supported", "proven"}


@dataclass(frozen=True)
class Recipe:
    meta: dict[str, Any]
    body: dict[str, Any]
    path: str
    sha256: str


def load_schemas(root: Path) -> dict[str, dict[str, Any]]:
    schemas: dict[str, dict[str, Any]] = {}
    for name in SCHEMA_NAMES:
        rel = f"schema/{name}.schema.json"
        schema = json.loads((root / rel).read_text(encoding="utf-8"))
        version = schema.get("version")
        if type(version) is not int or version < 1:
            raise CookbookError(f"{rel}: top-level 'version' must be an integer >= 1")
        try:
            Draft202012Validator.check_schema(schema)
        except SchemaError as exc:
            raise CookbookError(f"{rel}: not a valid JSON Schema: {exc.message}") from exc
        schemas[name] = schema
    return schemas


def raise_first_schema_error(schema: dict[str, Any], instance: Any, label: str) -> None:
    errors = sorted(
        Draft202012Validator(schema).iter_errors(instance),
        key=lambda error: ([str(part) for part in error.absolute_path], error.message),
    )
    if errors:
        error = errors[0]
        where = "/".join(str(part) for part in error.absolute_path) or "(root)"
        raise CookbookError(f"{label}: {where}: {error.message}")


def walk_strings(value: Any, label: str) -> Iterator[tuple[str, str]]:
    if isinstance(value, str):
        yield label, value
    elif isinstance(value, dict):
        for key, item in value.items():
            yield from walk_strings(item, f"{label}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from walk_strings(item, f"{label}[{index}]")


def visible_entries(directory: Path) -> list[Path]:
    return sorted(path for path in directory.iterdir() if not path.name.startswith("."))


def load_recipe(root: Path, directory: Path, schema: dict[str, Any]) -> Recipe:
    rel_dir = directory.relative_to(root).as_posix()
    names = [path.name for path in visible_entries(directory)]
    if names != [RECIPE_FILE]:
        raise CookbookError(f"{rel_dir}: must contain only {RECIPE_FILE}; found {names}")
    path = directory / RECIPE_FILE
    rel = path.relative_to(root).as_posix()
    spec = schema["x-body"]
    # format-rules: begin
    raw = path.read_bytes()
    if len(raw) > spec["max_bytes"]:
        raise CookbookError(f"{rel}: {len(raw)} bytes exceeds the {spec['max_bytes']}-byte cap")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise CookbookError(f"{rel}: not UTF-8 ({exc.reason})") from exc
    if not text.endswith("\n") or text.endswith("\n\n"):
        raise CookbookError(f"{rel}: must end with exactly one newline")
    # format-rules: end
    try:
        frontmatter, body_text = split_frontmatter(text)
        meta = load_frontmatter(frontmatter)
        for label, value in walk_strings(meta, "frontmatter"):
            if "\n" in value or "\r" in value:
                raise CookbookError(f"{label}: must be a single line")
            check_markup(value, spec["markup"], label)
        raise_first_schema_error(schema, meta, "frontmatter")
        check_markup(body_text, spec["markup"], "body")
        body = parse_body(body_text, spec)
    except CookbookError as exc:
        raise CookbookError(f"{rel}: {exc}") from exc
    if meta["id"] != directory.name:
        raise CookbookError(f"{rel}: id {meta['id']!r} must match directory name {directory.name!r}")
    return Recipe(meta=meta, body=body, path=rel, sha256=hashlib.sha256(raw).hexdigest())


def load_recipes(root: Path, schema: dict[str, Any]) -> list[Recipe]:
    entries = visible_entries(root / "recipes")
    stray = [path.name for path in entries if not path.is_dir()]
    if stray:
        raise CookbookError(f"recipes/: only Recipe directories are allowed; found {stray}")
    recipes = [load_recipe(root, directory, schema) for directory in entries]
    ids = {recipe.meta["id"] for recipe in recipes}
    for recipe in recipes:
        unknown = sorted(set(recipe.meta.get("related", [])) - ids)
        if unknown:
            raise CookbookError(f"{recipe.path}: related names unknown Recipes: {', '.join(unknown)}")
    return recipes


def matches(meta: dict[str, Any], selector: dict[str, Any]) -> bool:
    for key in ("function", "industry"):
        if key in selector and not set(meta.get(key, [])) & set(selector[key]):
            return False
    if "platforms_any" in selector and not set(meta["works_with"]["platforms"]) & set(selector["platforms_any"]):
        return False
    if "job_category" in selector and meta["job_category"] not in selector["job_category"]:
        return False
    return True


def load_collections(
    root: Path, schema: dict[str, Any], markup: dict[str, Any], recipes: list[Recipe]
) -> list[dict[str, Any]]:
    by_id = {recipe.meta["id"]: recipe.meta for recipe in recipes}
    collections: list[dict[str, Any]] = []
    for path in sorted((root / "collections").glob("*.json")):
        rel = path.relative_to(root).as_posix()
        try:
            collection = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise CookbookError(f"{rel}: not valid JSON: {exc}") from exc
        raise_first_schema_error(schema, collection, rel)
        for label, value in walk_strings(collection, rel):
            check_markup(value, markup, label)
        if collection["id"] != path.stem:
            raise CookbookError(f"{rel}: id {collection['id']!r} must match filename {path.stem!r}")
        unknown = sorted(set(collection.get("members", [])) - by_id.keys())
        if unknown:
            raise CookbookError(f"{rel}: members name unknown Recipes: {', '.join(unknown)}")
        members = set(collection.get("members", []))
        if "selector" in collection:
            members |= {recipe_id for recipe_id, meta in by_id.items() if matches(meta, collection["selector"])}
        resolved = sorted(members)
        count = sum(1 for recipe_id in resolved if by_id[recipe_id]["readiness"] in COUNTED_READINESS)
        threshold = 3 if collection["kind"] == "function" else 1
        collections.append(
            {
                **collection,
                "resolved_members": resolved,
                "supported_or_proven_count": count,
                "website_publication_threshold": threshold,
                "website_visible": count >= threshold,
            }
        )
    return collections


def build_catalog(root: Path = ROOT) -> tuple[dict[str, Any], str]:
    schemas = load_schemas(root)
    recipes = load_recipes(root, schemas["recipe"])
    collections = load_collections(root, schemas["collection"], schemas["recipe"]["x-body"]["markup"], recipes)
    catalog = {
        "source": REPO_URL,
        "schema_versions": {name: schemas[name]["version"] for name in SCHEMA_NAMES},
        "recipes": [
            {**recipe.meta, "path": recipe.path, "sha256": recipe.sha256}
            for recipe in sorted(recipes, key=lambda recipe: recipe.meta["id"])
        ],
        "collections": sorted(collections, key=lambda collection: collection["id"]),
    }
    raise_first_schema_error(schemas["catalog"], catalog, "catalog.json")
    return catalog, json.dumps(catalog, indent=2, ensure_ascii=False, sort_keys=True) + "\n"


def main(argv: list[str] | None = None, root: Path = ROOT) -> int:
    parser = argparse.ArgumentParser(description="Validate the cookbook and generate catalog.json.")
    parser.add_argument("--check", action="store_true", help="fail if catalog.json differs from a fresh build")
    args = parser.parse_args(argv)
    try:
        catalog, text = build_catalog(root)
    except CookbookError as exc:
        print(f"cookbook validation error: {exc}", file=sys.stderr)
        return 1
    path = root / "catalog.json"
    if args.check:
        current = path.read_bytes().decode("utf-8") if path.exists() else None
        if current != text:
            print("cookbook validation error: catalog.json is stale; run python3 scripts/build_catalog.py", file=sys.stderr)
            return 1
    else:
        path.write_bytes(text.encode("utf-8"))
    visible = sum(1 for collection in catalog["collections"] if collection["website_visible"])
    print(
        f"validated {len(catalog['recipes'])} recipe(s), {len(catalog['collections'])} collection(s); "
        f"{visible} collection(s) website-visible"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
