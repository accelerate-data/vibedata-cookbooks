"""Check historical migration fidelity against frozen migrated output.

The Markdown fixture is recipes/dbt-full-refresh-to-incremental/recipe.md from
commit df876578aaf44ca21a33e38a2456649e414438a6, before B10 content evolution.
Live Recipes remain covered by published-Recipe, schema and catalog tests.
"""

from __future__ import annotations

import copy
import json

from jsonschema import Draft202012Validator

from recipe_format import check_markup, load_frontmatter, parse_body, split_frontmatter
from samples import REPO_ROOT, load_schema

SCHEMA = load_schema("recipe")
RECIPE = REPO_ROOT / "tests/fixtures/migrated-dbt-full-refresh-to-incremental.md"
LEGACY = json.loads((REPO_ROOT / "tests/fixtures/legacy-dbt-full-refresh-to-incremental.json").read_text(encoding="utf-8"))
BODY_KEYS = {"prompt", "verified_by", "agent_guidance"}


def parts():
    frontmatter, body = split_frontmatter(RECIPE.read_text(encoding="utf-8"))
    return load_frontmatter(frontmatter), body


def test_body_text_is_byte_identical_to_the_legacy_recipe():
    _, body = parts()
    parsed = parse_body(body, SCHEMA["x-body"])
    for key in BODY_KEYS:
        assert parsed[key] == LEGACY[key]


def test_metadata_carries_over_with_the_studio_platform_name():
    meta, _ = parts()
    expected = copy.deepcopy({k: v for k, v in LEGACY.items() if k not in BODY_KEYS})
    expected["works_with"]["platforms"] = ["duckdb_local" if p == "duckdb" else p for p in expected["works_with"]["platforms"]]
    expected["pitch"] = meta["pitch"]
    assert meta == expected


def test_converted_recipe_passes_schema_and_markup():
    meta, body = parts()
    assert list(Draft202012Validator(SCHEMA).iter_errors(meta)) == []
    check_markup(body, SCHEMA["x-body"]["markup"], "body")
