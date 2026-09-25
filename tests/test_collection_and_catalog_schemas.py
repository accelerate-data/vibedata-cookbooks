"""collection.schema.json and catalog.schema.json: validity, mirroring, wrong controls."""

from __future__ import annotations

import copy
from typing import Any

import pytest
from jsonschema import Draft202012Validator

from samples import VALID_META, load_schema

RECIPE = load_schema("recipe")
COLLECTION = load_schema("collection")
CATALOG = load_schema("catalog")

RECIPE_ENTRY_EXTRA = {"path", "sha256"}
COLLECTION_ENTRY_EXTRA = {"resolved_members", "supported_or_proven_count", "website_publication_threshold", "website_visible"}

VALID_COLLECTION: dict[str, Any] = {
    "id": "sample",
    "title": "Sample",
    "kind": "curated",
    "description": "A sample collection.",
    "members": ["sample-recipe"],
}

VALID_CATALOG: dict[str, Any] = {
    "source": "https://github.com/accelerate-data/vibedata-cookbooks",
    "schema_versions": {"recipe": 1, "catalog": 1, "collection": 1},
    "recipes": [{**VALID_META, "path": "recipes/sample-recipe/recipe.md", "sha256": "0" * 64}],
    "collections": [
        {
            **VALID_COLLECTION,
            "resolved_members": ["sample-recipe"],
            "supported_or_proven_count": 1,
            "website_publication_threshold": 1,
            "website_visible": True,
        }
    ],
}


def errors(schema: dict[str, Any], instance: Any) -> list[Any]:
    return list(Draft202012Validator(schema).iter_errors(instance))


@pytest.mark.parametrize("schema", [COLLECTION, CATALOG], ids=["collection", "catalog"])
def test_schema_is_valid_with_version_1(schema):
    Draft202012Validator.check_schema(schema)
    assert schema["version"] == 1


def test_shared_defs_are_identical_across_schemas():
    for name, definition in RECIPE["$defs"].items():
        assert COLLECTION["$defs"][name] == definition
        assert CATALOG["$defs"][name] == definition


def test_recipe_entry_mirrors_recipe_schema_exactly():
    entry = CATALOG["$defs"]["recipe_entry"]
    assert {k: v for k, v in entry["properties"].items() if k not in RECIPE_ENTRY_EXTRA} == RECIPE["properties"]
    assert entry["required"] == RECIPE["required"] + ["path", "sha256"]
    assert entry["allOf"] == RECIPE["allOf"]
    assert entry["additionalProperties"] is False


def test_collection_entry_mirrors_collection_schema_exactly():
    entry = CATALOG["$defs"]["collection_entry"]
    assert {k: v for k, v in entry["properties"].items() if k not in COLLECTION_ENTRY_EXTRA} == COLLECTION["properties"]
    assert entry["required"] == COLLECTION["required"] + [
        "resolved_members",
        "supported_or_proven_count",
        "website_publication_threshold",
        "website_visible",
    ]
    assert entry["anyOf"] == COLLECTION["anyOf"]
    assert entry["additionalProperties"] is False


def test_valid_collection_passes():
    assert errors(COLLECTION, VALID_COLLECTION) == []
    selector_collection = {**{k: v for k, v in VALID_COLLECTION.items() if k != "members"}, "selector": {"platforms_any": ["duckdb_local"]}}
    assert errors(COLLECTION, selector_collection) == []


@pytest.mark.parametrize(
    "collection",
    [
        {k: v for k, v in VALID_COLLECTION.items() if k != "members"},
        {**VALID_COLLECTION, "selector": {"platforms_any": ["duckdb"]}},
        {**VALID_COLLECTION, "selector": {"platforms_any": []}},
        {**VALID_COLLECTION, "subfilters": [{"id": "local", "title": "Local", "platforms_any": ["duckdb"]}]},
        {**VALID_COLLECTION, "kind": "persona"},
        {**VALID_COLLECTION, "members": ["Not An Id"]},
        {**VALID_COLLECTION, "owner": "someone"},
    ],
    ids=["no_members_or_selector", "legacy_duckdb_selector", "empty_selector_list", "legacy_duckdb_subfilter", "unknown_kind", "bad_member_id", "extra_key"],
)
def test_collection_rejects_wrong_control(collection):
    assert errors(COLLECTION, collection)


def test_valid_catalog_passes():
    assert errors(CATALOG, VALID_CATALOG) == []


def catalog_with(mutate) -> dict[str, Any]:
    catalog = copy.deepcopy(VALID_CATALOG)
    mutate(catalog)
    return catalog


@pytest.mark.parametrize(
    "mutate",
    [
        lambda c: c.pop("schema_versions"),
        lambda c: c["schema_versions"].pop("collection"),
        lambda c: c.update(revision="12f2bbf8e83ca0fb22e95d31efa463d320458758"),
        lambda c: c["recipes"][0].pop("path"),
        lambda c: c["recipes"][0].pop("sha256"),
        lambda c: c["recipes"][0].update(sha256="A" * 64),
        lambda c: c["recipes"][0].update(sha256="0" * 63),
        lambda c: c["recipes"][0].update(path="recipes/sample-recipe/recipe.json"),
        lambda c: c["recipes"][0].update(prompt="Do the thing."),
        lambda c: c["recipes"][0].update(verified_by=["It works."]),
        lambda c: c["recipes"][0].update(agent_guidance={"instructions": "Go."}),
        lambda c: c["recipes"][0].update(canonical_url="https://example.com"),
        lambda c: c["recipes"][0]["works_with"].update(platforms=["duckdb"]),
        lambda c: c["collections"][0].pop("website_visible"),
    ],
    ids=[
        "no_schema_versions",
        "partial_schema_versions",
        "hand_revision",
        "entry_without_path",
        "entry_without_sha256",
        "uppercase_sha256",
        "short_sha256",
        "json_path",
        "prompt_copy",
        "verified_by_copy",
        "agent_guidance_copy",
        "canonical_url",
        "legacy_duckdb",
        "collection_without_visibility",
    ],
)
def test_catalog_rejects_wrong_control(mutate):
    assert errors(CATALOG, catalog_with(mutate))
