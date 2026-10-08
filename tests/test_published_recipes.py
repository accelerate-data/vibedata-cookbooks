"""The catalog holds exactly the expected Recipes with their agreed platforms and readiness.

Each Recipe's agreed values live in their own file, tests/expected/<id>.json, so
pull requests that add different Recipes never edit the same lines. The catalog
is built in memory, because catalog.json is regenerated after each merge to
pre-prod and a pull request does not update it.
"""

from __future__ import annotations

import json

import pytest

from build_catalog import build_catalog
from samples import REPO_ROOT

EXPECTED_DIR = REPO_ROOT / "tests/expected"
EXPECTED = {
    path.stem: json.loads(path.read_text(encoding="utf-8"))
    for path in sorted(EXPECTED_DIR.glob("*.json"))
}


def catalog_entries() -> dict[str, dict]:
    catalog, _ = build_catalog(REPO_ROOT)
    return {entry["id"]: entry for entry in catalog["recipes"]}


def test_catalog_holds_exactly_the_expected_recipes():
    assert set(catalog_entries()) == set(EXPECTED)


@pytest.mark.parametrize("recipe_id", sorted(EXPECTED))
def test_recipe_has_its_agreed_platforms_and_readiness(recipe_id):
    entry = catalog_entries()[recipe_id]
    assert entry["readiness"] == EXPECTED[recipe_id]["readiness"]
    assert sorted(entry["works_with"]["platforms"]) == sorted(EXPECTED[recipe_id]["platforms"])
    assert entry["pitch"]
    assert entry["evidence"]["evals"] == []
