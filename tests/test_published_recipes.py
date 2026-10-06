"""The published catalog holds exactly the expected Recipes with their agreed platforms and readiness."""

from __future__ import annotations

import json

import pytest

from samples import REPO_ROOT

ALL_PLATFORMS = ["duckdb_local", "motherduck", "fabric_lakehouse", "fabric_warehouse", "redshift"]

EXPECTED = {
    "dbt-snapshot-history": {"readiness": "supported", "platforms": ["duckdb_local"]},
    "business-event-fact": {"readiness": "supported", "platforms": ALL_PLATFORMS},
    "event-resource-attribution": {"readiness": "supported", "platforms": ALL_PLATFORMS},
    "effective-dated-business-rules": {"readiness": "supported", "platforms": ALL_PLATFORMS},
    "dbt-full-refresh-to-incremental": {
        "readiness": "supported",
        "platforms": ["duckdb_local", "motherduck", "fabric_lakehouse", "fabric_warehouse"],
    },
    "api-to-bronze-incremental-contract": {"readiness": "supported", "platforms": ALL_PLATFORMS},
    "fabric-data-pipeline-as-code": {"readiness": "supported", "platforms": ["fabric_lakehouse", "fabric_warehouse"]},
    "motherduck-flight-scheduling": {"readiness": "supported", "platforms": ["motherduck"]},
    "logistics-fleet-utilization": {"readiness": "supported", "platforms": ALL_PLATFORMS},
    "metric-population-and-rollups": {"readiness": "supported", "platforms": ALL_PLATFORMS},
    "operational-state-duration": {"readiness": "supported", "platforms": ALL_PLATFORMS},
    "prove-dbt-change-safe": {"readiness": "supported", "platforms": ALL_PLATFORMS},
    "revops-quota-commission": {"readiness": "supported", "platforms": ["duckdb_local"]},
    "shift-unit-economics": {"readiness": "supported", "platforms": ALL_PLATFORMS},
    "revops-pipeline-snapshots": {"readiness": "supported", "platforms": ["duckdb_local"]},
    "service-ticket-sla": {"readiness": "supported", "platforms": ["duckdb_local"]},
    "identity-standardize-names-addresses": {"readiness": "supported", "platforms": ["duckdb_local"]},
    "identity-golden-record-crosswalk": {"readiness": "supported", "platforms": ["duckdb_local"]},
    "master-b2b-account-hierarchy": {"readiness": "supported", "platforms": ["duckdb_local"]},
}


def catalog_entries() -> dict[str, dict]:
    catalog = json.loads((REPO_ROOT / "catalog.json").read_text(encoding="utf-8"))
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
