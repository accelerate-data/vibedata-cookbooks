"""build_catalog: metadata-only, sorted, byte-stable output; --check; each rejection rule."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from build_catalog import build_catalog, main
from recipe_format import CookbookError
from samples import REPO_ROOT, VALID_META, VALID_RECIPE, write_recipe

COLLECTION = {"id": "sample", "title": "Sample", "kind": "curated", "description": "A sample collection."}
RECIPE_REL = "recipes/sample-recipe/recipe.md"


def test_valid_cookbook_builds_a_metadata_only_catalog(cookbook):
    catalog, _ = build_catalog(cookbook)
    assert set(catalog) == {"source", "schema_versions", "recipes", "collections"}
    assert catalog["source"] == "https://github.com/accelerate-data/vibedata-cookbooks"
    assert catalog["schema_versions"] == {"recipe": 1, "catalog": 1, "collection": 1}
    (entry,) = catalog["recipes"]
    assert entry == {**VALID_META, "path": RECIPE_REL, "sha256": hashlib.sha256((cookbook / RECIPE_REL).read_bytes()).hexdigest()}


def test_catalog_is_sorted_and_byte_stable(cookbook):
    write_recipe(cookbook, "another-recipe", VALID_RECIPE.replace("id: sample-recipe", "id: another-recipe"))
    first = build_catalog(cookbook)[1]
    assert first == build_catalog(cookbook)[1]
    assert [entry["id"] for entry in json.loads(first)["recipes"]] == ["another-recipe", "sample-recipe"]
    assert first.endswith("}\n")


def test_selector_collection_resolves_by_platform(cookbook):
    selector = {**COLLECTION, "id": "local", "kind": "platform", "selector": {"platforms_any": ["duckdb_local"]}}
    (cookbook / "collections/local.json").write_text(json.dumps(selector), encoding="utf-8")
    catalog, _ = build_catalog(cookbook)
    (collection,) = catalog["collections"]
    assert collection["resolved_members"] == ["sample-recipe"]
    assert collection["supported_or_proven_count"] == 1
    assert collection["website_publication_threshold"] == 1
    assert collection["website_visible"] is True


def test_check_mode_detects_a_stale_catalog(cookbook, capsys):
    assert main(["--check"], root=cookbook) == 1
    assert main([], root=cookbook) == 0
    assert main(["--check"], root=cookbook) == 0
    path = cookbook / RECIPE_REL
    path.write_bytes(VALID_RECIPE.replace("prove its output.", "prove its output twice.").encode("utf-8"))
    assert main(["--check"], root=cookbook) == 1
    assert "stale" in capsys.readouterr().err


def test_dotfiles_are_ignored(cookbook):
    (cookbook / "recipes/.DS_Store").write_bytes(b"x")
    (cookbook / "recipes/sample-recipe/.DS_Store").write_bytes(b"x")
    assert build_catalog(cookbook)[0]["recipes"]


def test_repository_catalog_is_fresh():
    assert main(["--check"], root=REPO_ROOT) == 0


def replace_in_recipe(old: str, new: str):
    def mutate(root: Path) -> None:
        path = root / RECIPE_REL
        text = path.read_text(encoding="utf-8")
        assert old in text
        path.write_bytes(text.replace(old, new).encode("utf-8"))

    return mutate


def write_file(relpath: str, content: bytes | str):
    def mutate(root: Path) -> None:
        path = root / relpath
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content if isinstance(content, bytes) else content.encode("utf-8"))

    return mutate


def drop_schema_version(root: Path) -> None:
    path = root / "schema/recipe.schema.json"
    schema = json.loads(path.read_text(encoding="utf-8"))
    del schema["version"]
    path.write_text(json.dumps(schema), encoding="utf-8")


REJECTIONS = {
    "legacy_recipe_json": (write_file("recipes/sample-recipe/recipe.json", "{}"), "must contain only recipe.md"),
    "generated_readme": (write_file("recipes/sample-recipe/README.md", "# x\n"), "must contain only recipe.md"),
    "stray_file": (write_file("recipes/notes.txt", "x"), "only Recipe directories"),
    "id_mismatch": (replace_in_recipe("id: sample-recipe", "id: other-recipe"), "must match directory name"),
    "missing_platforms": (replace_in_recipe("works_with:\n  platforms:\n    - duckdb_local\n", "works_with: {}\n"), "'platforms' is a required property"),
    "legacy_platform": (replace_in_recipe("- duckdb_local", "- duckdb"), "'duckdb' is not one of"),
    "proven_without_evals": (replace_in_recipe("readiness: supported", "readiness: proven"), "'evidence' is a required property"),
    "prompt_in_frontmatter": (replace_in_recipe("readiness: supported\n", "readiness: supported\nprompt: Do the thing.\n"), "'prompt' was unexpected"),
    "markup_in_frontmatter": (replace_in_recipe("area: transformation\n", "area: transformation\npitch: Build a <div> fast.\n"), "HTML or tool-call tag"),
    "trailing_newline_in_frontmatter": (replace_in_recipe("title: Build a sample model and prove its output", 'title: "Build a sample model\\n"'), "must be a single line"),
    "markup_in_body": (replace_in_recipe("Do not invent a key.", "Do not invent a </key>."), "forbidden markup"),
    "body_rule": (replace_in_recipe("## Verified by", "## Verified By"), "headings"),
    "no_trailing_newline": (write_file(RECIPE_REL, VALID_RECIPE.rstrip("\n")), "exactly one newline"),
    "double_trailing_newline": (write_file(RECIPE_REL, VALID_RECIPE + "\n"), "exactly one newline"),
    "not_utf8": (write_file(RECIPE_REL, b"---\nid: \xff\n---\n"), "not UTF-8"),
    "over_byte_cap": (write_file(RECIPE_REL, VALID_RECIPE.replace("Do not invent a key.", "Do not invent a key." + " x" * 9000)), "byte cap"),
    "unknown_related": (replace_in_recipe("readiness: supported\n", "readiness: supported\nrelated:\n  - missing-recipe\n"), "related names unknown Recipes"),
    "unknown_member": (write_file("collections/sample.json", json.dumps({**COLLECTION, "members": ["missing-recipe"]})), "members name unknown Recipes"),
    "legacy_platform_selector": (write_file("collections/sample.json", json.dumps({**COLLECTION, "selector": {"platforms_any": ["duckdb"]}})), "'duckdb' is not one of"),
    "collection_id_mismatch": (write_file("collections/sample.json", json.dumps({**COLLECTION, "id": "other", "members": ["sample-recipe"]})), "must match filename"),
    "collection_markup": (write_file("collections/sample.json", json.dumps({**COLLECTION, "description": "A <script> view.", "members": ["sample-recipe"]})), "HTML or tool-call tag"),
    "collection_not_json": (write_file("collections/sample.json", "{"), "not valid JSON"),
    "unversioned_schema": (drop_schema_version, "top-level 'version'"),
    "crlf_in_frontmatter": (replace_in_recipe("id: sample-recipe\n", "id: sample-recipe\r\n"), "must use LF line endings"),
    "lone_cr_in_frontmatter": (replace_in_recipe("area: transformation\n", "area: transformation\r"), "must use LF line endings"),
    "byte_order_mark": (write_file(RECIPE_REL, "\ufeff" + VALID_RECIPE), "byte-order mark"),
}


@pytest.mark.parametrize(("mutate", "fragment"), list(REJECTIONS.values()), ids=list(REJECTIONS))
def test_rejects_wrong_control(cookbook, mutate, fragment):
    mutate(cookbook)
    with pytest.raises(CookbookError, match=fragment):
        build_catalog(cookbook)


def test_main_reports_a_violation_and_exits_1(cookbook, capsys):
    write_file("recipes/sample-recipe/recipe.json", "{}")(cookbook)
    assert main([], root=cookbook) == 1
    assert "cookbook validation error" in capsys.readouterr().err


def test_collections_are_sorted_by_id(cookbook):
    (cookbook / "collections/zeta.json").write_text(
        json.dumps({**COLLECTION, "id": "zeta", "members": ["sample-recipe"]}), encoding="utf-8"
    )
    (cookbook / "collections/alpha.json").write_text(
        json.dumps({**COLLECTION, "id": "alpha", "members": ["sample-recipe"]}), encoding="utf-8"
    )
    catalog, _ = build_catalog(cookbook)
    assert [collection["id"] for collection in catalog["collections"]] == ["alpha", "zeta"]


def test_function_collection_needs_three_supported_recipes(cookbook):
    (cookbook / "collections/sample.json").write_text(
        json.dumps({**COLLECTION, "kind": "function", "members": ["sample-recipe"]}), encoding="utf-8"
    )
    catalog, _ = build_catalog(cookbook)
    (collection,) = catalog["collections"]
    assert collection["website_publication_threshold"] == 3
    assert collection["supported_or_proven_count"] == 1
    assert collection["website_visible"] is False

    write_recipe(cookbook, "another-recipe", VALID_RECIPE.replace("id: sample-recipe", "id: another-recipe"))
    write_recipe(cookbook, "third-recipe", VALID_RECIPE.replace("id: sample-recipe", "id: third-recipe"))
    (cookbook / "collections/sample.json").write_text(
        json.dumps(
            {**COLLECTION, "kind": "function", "members": ["sample-recipe", "another-recipe", "third-recipe"]}
        ),
        encoding="utf-8",
    )
    catalog, _ = build_catalog(cookbook)
    (collection,) = catalog["collections"]
    assert collection["website_visible"] is True


def test_planned_recipes_do_not_count(cookbook):
    write_recipe(cookbook, "sample-recipe", VALID_RECIPE.replace("readiness: supported", "readiness: planned"))
    (cookbook / "collections/sample.json").write_text(
        json.dumps({**COLLECTION, "members": ["sample-recipe"]}), encoding="utf-8"
    )
    catalog, _ = build_catalog(cookbook)
    (collection,) = catalog["collections"]
    assert collection["supported_or_proven_count"] == 0
    assert collection["website_visible"] is False
