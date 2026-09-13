#!/usr/bin/env python3
"""Validate canonical Cookbook JSON and generate Recipe pages + catalog.json.

No third-party dependencies are required. JSON Schema files document the public
contract; this script enforces the invariants needed to keep generated surfaces
and discovery data consistent.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RECIPES_DIR = ROOT / "recipes"
COLLECTIONS_DIR = ROOT / "collections"
CATALOG_PATH = ROOT / "catalog.json"
REPO_URL = "https://github.com/accelerate-data/vibedata-cookbooks"

JOB_CATEGORIES = {
    "get-running",
    "re-engineer",
    "build",
    "prove",
    "explain",
    "cross-platform",
}
READINESS = {"proven", "supported", "planned"}
PLATFORMS = {"fabric_lakehouse", "fabric_warehouse", "motherduck", "duckdb"}
COLLECTION_KINDS = {"function", "industry", "platform", "curated", "problem-area"}
REQUIRED_RECIPE_FIELDS = {
    "id",
    "title",
    "trigger",
    "description",
    "job_category",
    "area",
    "readiness",
    "prompt",
    "verified_by",
    "agent_guidance",
}


def fail(message: str) -> None:
    raise SystemExit(f"cookbook validation error: {message}")


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"{path.relative_to(ROOT)}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path.relative_to(ROOT)} must contain one JSON object")
    return value


def require_non_empty_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        fail(f"{label} must be a non-empty string")
    return value


def require_string_list(value: Any, label: str, *, non_empty: bool = False) -> list[str]:
    if not isinstance(value, list) or (non_empty and not value):
        requirement = "a non-empty list" if non_empty else "a list"
        fail(f"{label} must be {requirement} of strings")
    for index, item in enumerate(value):
        require_non_empty_string(item, f"{label}[{index}]")
    if len(value) != len(set(value)):
        fail(f"{label} must not contain duplicates")
    return value


def validate_recipe(path: Path, recipe: dict[str, Any]) -> None:
    missing = sorted(REQUIRED_RECIPE_FIELDS - recipe.keys())
    if missing:
        fail(f"{path.relative_to(ROOT)} missing required fields: {', '.join(missing)}")

    recipe_id = require_non_empty_string(recipe["id"], f"{path}: id")
    if path.parent.name != recipe_id:
        fail(f"{path.relative_to(ROOT)} id must match directory name {path.parent.name!r}")

    require_non_empty_string(recipe["title"], f"{recipe_id}: title")
    require_string_list(recipe["trigger"], f"{recipe_id}: trigger", non_empty=True)
    require_non_empty_string(recipe["description"], f"{recipe_id}: description")
    require_non_empty_string(recipe["area"], f"{recipe_id}: area")
    require_non_empty_string(recipe["prompt"], f"{recipe_id}: prompt")
    require_string_list(recipe["verified_by"], f"{recipe_id}: verified_by", non_empty=True)

    if recipe["job_category"] not in JOB_CATEGORIES:
        fail(f"{recipe_id}: unknown job_category {recipe['job_category']!r}")
    if recipe["readiness"] not in READINESS:
        fail(f"{recipe_id}: unknown readiness {recipe['readiness']!r}")

    for key in ("function", "industry", "domain_objects", "qualifiers", "related"):
        if key in recipe:
            require_string_list(recipe[key], f"{recipe_id}: {key}")

    works_with = recipe.get("works_with")
    if works_with is not None:
        if not isinstance(works_with, dict):
            fail(f"{recipe_id}: works_with must be an object")
        platforms = works_with.get("platforms", [])
        require_string_list(platforms, f"{recipe_id}: works_with.platforms")
        unknown = sorted(set(platforms) - PLATFORMS)
        if unknown:
            fail(f"{recipe_id}: unsupported platform values: {', '.join(unknown)}")
        if "fabric" in platforms:
            fail(f"{recipe_id}: generic 'fabric' is not an execution target")
        if "tools" in works_with:
            require_string_list(works_with["tools"], f"{recipe_id}: works_with.tools")

    guidance = recipe["agent_guidance"]
    if not isinstance(guidance, dict):
        fail(f"{recipe_id}: agent_guidance must be an object")
    require_non_empty_string(guidance.get("instructions"), f"{recipe_id}: agent_guidance.instructions")
    for key in ("compose", "ask_first", "guardrails"):
        if key in guidance:
            require_string_list(guidance[key], f"{recipe_id}: agent_guidance.{key}")

    evidence = recipe.get("evidence")
    if evidence is not None:
        if not isinstance(evidence, dict):
            fail(f"{recipe_id}: evidence must be an object")
        for key in ("features", "evals"):
            if key in evidence:
                require_string_list(evidence[key], f"{recipe_id}: evidence.{key}")


def recipe_matches_selector(recipe: dict[str, Any], selector: dict[str, Any]) -> bool:
    if not selector:
        return True

    if "function" in selector:
        held = set(recipe.get("function", []))
        if not held.intersection(selector["function"]):
            return False
    if "industry" in selector:
        held = set(recipe.get("industry", []))
        if not held.intersection(selector["industry"]):
            return False
    if "platforms_any" in selector:
        held = set(recipe.get("works_with", {}).get("platforms", []))
        if not held.intersection(selector["platforms_any"]):
            return False
    if "job_category" in selector:
        if recipe["job_category"] not in selector["job_category"]:
            return False
    return True


def validate_collection(path: Path, collection: dict[str, Any], recipe_ids: set[str]) -> None:
    for key in ("id", "title", "kind", "description"):
        if key not in collection:
            fail(f"{path.relative_to(ROOT)} missing required field {key}")
    collection_id = require_non_empty_string(collection["id"], f"{path}: id")
    if path.stem != collection_id:
        fail(f"{path.relative_to(ROOT)} id must match filename {path.stem!r}")
    require_non_empty_string(collection["title"], f"{collection_id}: title")
    require_non_empty_string(collection["description"], f"{collection_id}: description")
    if collection["kind"] not in COLLECTION_KINDS:
        fail(f"{collection_id}: unknown kind {collection['kind']!r}")
    if "members" not in collection and "selector" not in collection:
        fail(f"{collection_id}: define members or selector")
    if "members" in collection:
        members = require_string_list(collection["members"], f"{collection_id}: members")
        missing = sorted(set(members) - recipe_ids)
        if missing:
            fail(f"{collection_id}: unknown Recipe members: {', '.join(missing)}")
    selector = collection.get("selector")
    if selector is not None:
        if not isinstance(selector, dict):
            fail(f"{collection_id}: selector must be an object")
        for key in ("function", "industry", "platforms_any", "job_category"):
            if key in selector:
                require_string_list(selector[key], f"{collection_id}: selector.{key}")
        if "platforms_any" in selector:
            unknown = sorted(set(selector["platforms_any"]) - PLATFORMS)
            if unknown:
                fail(f"{collection_id}: unknown platform selector values: {', '.join(unknown)}")
        if "job_category" in selector:
            unknown = sorted(set(selector["job_category"]) - JOB_CATEGORIES)
            if unknown:
                fail(f"{collection_id}: unknown job categories: {', '.join(unknown)}")


def resolve_collection_members(
    collection: dict[str, Any], recipes_by_id: dict[str, dict[str, Any]]
) -> list[str]:
    members = set(collection.get("members", []))
    selector = collection.get("selector")
    if selector:
        members.update(
            recipe_id
            for recipe_id, recipe in recipes_by_id.items()
            if recipe_matches_selector(recipe, selector)
        )
    return sorted(members)


def render_recipe(recipe: dict[str, Any]) -> str:
    def bullets(items: list[str]) -> str:
        return "\n".join(f"- {item}" for item in items)

    lines = [
        f"# {recipe['title']}",
        "",
        f"**Recipe ID:** `{recipe['id']}`  ",
        f"**Job:** `{recipe['job_category']}`  ",
        f"**Area:** `{recipe['area']}`  ",
        f"**Readiness:** `{recipe['readiness']}`",
        "",
        recipe["description"],
        "",
        "## When to use this Recipe",
        "",
        bullets(recipe["trigger"]),
        "",
    ]

    function = recipe.get("function", [])
    industry = recipe.get("industry", [])
    domain_objects = recipe.get("domain_objects", [])
    platforms = recipe.get("works_with", {}).get("platforms", [])
    tools = recipe.get("works_with", {}).get("tools", [])
    if function or industry or domain_objects or platforms or tools:
        lines.extend(["## Compatibility and context", ""])
        if function:
            lines.append(f"- **Function:** {', '.join(function)}")
        if industry:
            lines.append(f"- **Industry:** {', '.join(industry)}")
        if domain_objects:
            lines.append(f"- **Objects:** {', '.join(f'`{x}`' for x in domain_objects)}")
        if platforms:
            lines.append(f"- **Platforms:** {', '.join(f'`{x}`' for x in platforms)}")
        if tools:
            lines.append(f"- **Tools:** {', '.join(f'`{x}`' for x in tools)}")
        lines.append("")

    lines.extend(
        [
            "## Recipe prompt",
            "",
            "> This is the canonical task specification the agent reads after the Recipe is selected. It is not the website copy/paste invocation pointer.",
            "",
            recipe["prompt"],
            "",
            "## Verified by",
            "",
            bullets(recipe["verified_by"]),
            "",
            "## Agent guidance",
            "",
            recipe["agent_guidance"]["instructions"],
            "",
        ]
    )

    guidance = recipe["agent_guidance"]
    if guidance.get("compose"):
        lines.extend(["### Compose", "", bullets([f"`{x}`" for x in guidance["compose"]]), ""])
    if guidance.get("ask_first"):
        lines.extend(["### Ask first", "", bullets(guidance["ask_first"]), ""])
    if guidance.get("guardrails"):
        lines.extend(["### Guardrails", "", bullets(guidance["guardrails"]), ""])

    lines.extend(
        [
            "## Invocation",
            "",
            "The Recipe executes in the current Intent context. A website or discovery surface should invoke it by ID/canonical URL rather than copying this entire page into a prompt.",
            "",
            "Canonical path:",
            "",
            f"`{REPO_URL}/tree/main/recipes/{recipe['id']}`",
            "",
            "<!-- Generated by scripts/build_catalog.py from recipe.json. Do not edit this README by hand. -->",
            "",
        ]
    )
    return "\n".join(lines)


def build_outputs() -> tuple[dict[Path, str], dict[str, Any]]:
    recipes: list[dict[str, Any]] = []
    outputs: dict[Path, str] = {}

    for path in sorted(RECIPES_DIR.glob("*/recipe.json")):
        recipe = load_json(path)
        validate_recipe(path, recipe)
        recipes.append(recipe)
        outputs[path.parent / "README.md"] = render_recipe(recipe)

    recipe_ids = [recipe["id"] for recipe in recipes]
    if len(recipe_ids) != len(set(recipe_ids)):
        fail("Recipe IDs must be unique")
    recipes_by_id = {recipe["id"]: recipe for recipe in recipes}

    collections: list[dict[str, Any]] = []
    for path in sorted(COLLECTIONS_DIR.glob("*.json")):
        collection = load_json(path)
        validate_collection(path, collection, set(recipe_ids))
        member_ids = resolve_collection_members(collection, recipes_by_id)
        supported_count = sum(
            1
            for recipe_id in member_ids
            if recipes_by_id[recipe_id]["readiness"] in {"supported", "proven"}
        )
        threshold = 3 if collection["kind"] == "function" else 1
        collections.append(
            {
                **collection,
                "resolved_members": member_ids,
                "supported_or_proven_count": supported_count,
                "website_publication_threshold": threshold,
                "website_visible": supported_count >= threshold,
            }
        )

    catalog_recipes = []
    for recipe in sorted(recipes, key=lambda item: item["id"]):
        catalog_recipes.append(
            {
                **recipe,
                "canonical_url": f"{REPO_URL}/tree/main/recipes/{recipe['id']}",
            }
        )

    catalog = {
        "source": REPO_URL,
        "recipes": catalog_recipes,
        "collections": sorted(collections, key=lambda item: item["id"]),
    }
    outputs[CATALOG_PATH] = json.dumps(catalog, indent=2, ensure_ascii=False) + "\n"
    return outputs, catalog


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate sources and fail if generated output differs from disk",
    )
    args = parser.parse_args()

    outputs, catalog = build_outputs()
    stale: list[str] = []
    for path, content in outputs.items():
        if args.check:
            current = path.read_text(encoding="utf-8") if path.exists() else None
            if current != content:
                stale.append(str(path.relative_to(ROOT)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

    if stale:
        fail("generated files are stale: " + ", ".join(stale))

    visible = sum(1 for collection in catalog["collections"] if collection["website_visible"])
    print(
        f"validated {len(catalog['recipes'])} recipe(s), "
        f"{len(catalog['collections'])} collection(s); {visible} collection(s) website-visible"
    )


if __name__ == "__main__":
    main()
