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
