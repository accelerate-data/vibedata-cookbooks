"""recipe.schema.json accepts the valid sample and rejects each wrong control."""

from __future__ import annotations

import copy
from typing import Any

import pytest
from jsonschema import Draft202012Validator

from samples import VALID_META, load_schema

SCHEMA = load_schema("recipe")
DELETE = object()


def mutated(path: tuple[str, ...], value: Any) -> dict[str, Any]:
    meta = copy.deepcopy(VALID_META)
    target = meta
    for key in path[:-1]:
        target = target[key]
    if value is DELETE:
        del target[path[-1]]
    else:
        target[path[-1]] = value
    return meta


def errors(instance: dict[str, Any]) -> list[Any]:
    return list(Draft202012Validator(SCHEMA).iter_errors(instance))


def test_schema_is_valid_draft_2020_12_with_version_1():
    Draft202012Validator.check_schema(SCHEMA)
    assert SCHEMA["version"] == 1


def test_valid_meta_passes():
    assert errors(VALID_META) == []


def test_optional_fields_pass():
    meta = {
        **VALID_META,
        "pitch": "Build a sample model and prove it in one pass.",
        "domain_objects": ["dbt_model"],
        "function": ["finance"],
        "qualifiers": ["Code only."],
        "related": ["other-recipe"],
        "works_with": {"platforms": ["duckdb_local", "redshift"], "tools": ["dbt"]},
        "evidence": {"features": ["generating-dbt-model"], "evals": []},
    }
    assert errors(meta) == []


def test_proven_with_evals_passes():
    meta = {**VALID_META, "readiness": "proven", "evidence": {"evals": ["journeys/sample"]}}
    assert errors(meta) == []


@pytest.mark.parametrize(
    ("path", "value"),
    [
        (("works_with",), DELETE),
        (("works_with",), {}),
        (("works_with",), {"platforms": []}),
        (("works_with",), {"platforms": ["duckdb"]}),
        (("works_with",), {"platforms": ["fabric"]}),
        (("works_with",), {"platforms": ["motherduck"], "engine": "x"}),
        (("readiness",), "proven"),
        (("id",), "Sample_Recipe"),
        (("title",), "x" * 121),
        (("title",), "   "),
        (("title",), "two\nlines"),
        (("trigger",), []),
        (("trigger",), ["x" * 201]),
        (("description",), "x" * 401),
        (("pitch",), "First sentence. Second sentence."),
        (("pitch",), "No terminal punctuation"),
        (("pitch",), "x" * 160 + "."),
        (("area",), "data quality"),
        (("job_category",), "migrate"),
        (("readiness",), "shipped"),
        (("prompt",), "Prompts live in the body now."),
        (("canonical_url",), "https://example.com"),
        (("revision",), "abc"),
        (("id",), "a" * 65),
        (("area",), "a" * 41),
        (("trigger",), [f"Trigger number {i}." for i in range(6)]),
        (("trigger",), ["Same trigger.", "Same trigger."]),
        (("function",), ["Not A Token"]),
        (("function",), ["a" * 65]),
        (("function",), ["finance", "finance"]),
        (("function",), [f"f{i}" for i in range(11)]),
        (("industry",), ["Not A Token"]),
        (("industry",), ["a" * 65]),
        (("industry",), ["retail", "retail"]),
        (("industry",), [f"i{i}" for i in range(11)]),
        (("domain_objects",), ["Not A Token"]),
        (("domain_objects",), ["a" * 65]),
        (("domain_objects",), ["dbt_model", "dbt_model"]),
        (("domain_objects",), [f"d{i}" for i in range(21)]),
        (("works_with",), {"platforms": ["motherduck", "motherduck"]}),
        (("works_with",), {"platforms": ["duckdb_local"], "tools": ["Not A Token"]}),
        (("works_with",), {"platforms": ["duckdb_local"], "tools": [f"t{i}" for i in range(11)]}),
        (("works_with",), {"platforms": ["duckdb_local"], "tools": ["dbt", "dbt"]}),
        (("qualifiers",), [f"Q{i}." for i in range(11)]),
        (("qualifiers",), ["Same qualifier.", "Same qualifier."]),
        (("qualifiers",), ["a" * 121]),
        (("qualifiers",), ["two\nlines"]),
        (("related",), [f"other-recipe-{i}" for i in range(11)]),
        (("related",), ["other-recipe", "other-recipe"]),
        (("related",), ["Not_An_Id"]),
        (("evidence",), {"features": ["Not A Token"]}),
        (("evidence",), {"features": [f"f{i}" for i in range(21)]}),
        (("evidence",), {"features": ["dup", "dup"]}),
        (("evidence",), {"evals": [f"eval-{i}" for i in range(21)]}),
        (("evidence",), {"evals": ["dup", "dup"]}),
        (("evidence",), {"evals": ["a" * 201]}),
    ],
    ids=[
        "works_with_missing",
        "platforms_missing",
        "platforms_empty",
        "legacy_duckdb",
        "generic_fabric",
        "works_with_extra_key",
        "proven_without_evals",
        "id_not_kebab",
        "title_over_cap",
        "title_blank",
        "title_multiline",
        "trigger_empty",
        "trigger_over_cap",
        "description_over_cap",
        "pitch_two_sentences",
        "pitch_unterminated",
        "pitch_over_cap",
        "area_not_kebab",
        "job_category_unknown",
        "readiness_unknown",
        "prompt_in_frontmatter",
        "canonical_url_in_frontmatter",
        "revision_in_frontmatter",
        "id_over_cap",
        "area_over_cap",
        "trigger_too_many_items",
        "trigger_duplicate_items",
        "function_invalid_token",
        "function_token_over_cap",
        "function_duplicate",
        "function_over_cap",
        "industry_invalid_token",
        "industry_token_over_cap",
        "industry_duplicate",
        "industry_over_cap",
        "domain_objects_invalid_token",
        "domain_objects_token_over_cap",
        "domain_objects_duplicate",
        "domain_objects_over_cap",
        "platforms_duplicate",
        "tools_invalid_token",
        "tools_over_cap",
        "tools_duplicate",
        "qualifiers_over_cap",
        "qualifiers_duplicate",
        "qualifiers_item_over_cap",
        "qualifiers_multiline",
        "related_over_cap",
        "related_duplicate",
        "related_invalid_id",
        "evidence_features_invalid_token",
        "evidence_features_over_cap",
        "evidence_features_duplicate",
        "evidence_evals_over_cap",
        "evidence_evals_duplicate",
        "evidence_evals_item_over_cap",
    ],
)
def test_rejects_wrong_control(path, value):
    assert errors(mutated(path, value))


def test_proven_with_empty_evals_is_rejected():
    meta = {**VALID_META, "readiness": "proven", "evidence": {"evals": []}}
    assert errors(meta)


def test_body_spec_lists_the_closed_heading_set_in_order():
    headings = [section["heading"] for section in SCHEMA["x-body"]["sections"]]
    assert headings == [
        "## Prompt",
        "## Verified by",
        "## Agent guidance",
        "### Instructions",
        "### Compose",
        "### Ask first",
        "### Guardrails",
    ]
