"""parse_body: the valid sample, the caps at their limit, and each wrong control."""

from __future__ import annotations

import re

import pytest

from recipe_format import CookbookError, parse_body
from samples import VALID_BODY, VALID_BODY_FIELDS, load_schema

SPEC = load_schema("recipe")["x-body"]
PROMPT = VALID_BODY_FIELDS["prompt"]
INSTRUCTIONS = VALID_BODY_FIELDS["agent_guidance"]["instructions"]


def test_valid_body_parses_to_fields():
    assert parse_body(VALID_BODY, SPEC) == VALID_BODY_FIELDS


def test_prompt_at_cap_passes():
    assert parse_body(VALID_BODY.replace(PROMPT, "x" * 1200), SPEC)["prompt"] == "x" * 1200


def test_twelve_verified_by_bullets_pass():
    body = VALID_BODY.replace("- The model builds in the sandbox.\n", "- Condition.\n" * 11)
    assert len(parse_body(body, SPEC)["verified_by"]) == 12


def test_instructions_at_cap_passes():
    body = VALID_BODY.replace(INSTRUCTIONS, "x" * 1500)
    assert parse_body(body, SPEC)["agent_guidance"]["instructions"] == "x" * 1500


SWAPPED = VALID_BODY.replace("## Prompt", "## TEMP").replace("## Verified by", "## Prompt").replace("## TEMP", "## Verified by")

REJECTIONS = {
    "missing_section": (VALID_BODY.replace("### Ask first\n\n- Ask for the grain only if it cannot be inferred.\n\n", ""), "headings"),
    "extra_heading": (VALID_BODY + "\n## Notes\n\nMore.\n", "headings"),
    "h1_title": ("# Title\n" + VALID_BODY, "headings"),
    "wrong_order": (SWAPPED, "headings"),
    "duplicate_heading": (VALID_BODY + "\n### Guardrails\n\n- Again.\n", "headings"),
    "heading_case": (VALID_BODY.replace("## Verified by", "## Verified By"), "headings"),
    "text_before_prompt": ("Intro.\n" + VALID_BODY, "before '## Prompt'"),
    "text_under_container": (VALID_BODY.replace("## Agent guidance\n", "## Agent guidance\n\nStray text.\n"), "subsections"),
    "prompt_two_lines": (VALID_BODY.replace(PROMPT, PROMPT + "\nSecond line."), "one paragraph on one line"),
    "prompt_two_paragraphs": (VALID_BODY.replace(PROMPT, PROMPT + "\n\nSecond paragraph."), "one paragraph on one line"),
    "prompt_pipe": (VALID_BODY.replace(PROMPT, "Build a | b."), "must not contain '|'"),
    "prompt_as_bullet": (VALID_BODY.replace(PROMPT, "- " + PROMPT), "not a list, quote or table"),
    "prompt_as_quote": (VALID_BODY.replace(PROMPT, "> " + PROMPT), "not a list, quote or table"),
    "star_bullet": (VALID_BODY.replace("- The model builds", "* The model builds"), "'- ' bullet"),
    "numbered_bullet": (VALID_BODY.replace("- The model builds", "1. The model builds"), "'- ' bullet"),
    "blank_between_bullets": (VALID_BODY.replace("sandbox.\n- The output", "sandbox.\n\n- The output"), "'- ' bullet"),
    "indented_bullet": (VALID_BODY.replace("- The output", "  - The output"), "whitespace"),
    "trailing_space": (VALID_BODY.replace("the sandbox.", "the sandbox. "), "whitespace"),
    "double_space_bullet": (VALID_BODY.replace("- The output", "-  The output"), "whitespace"),
    "empty_compose": (VALID_BODY.replace("- generating-dbt-model\n", ""), "between 1 and 12"),
    "prompt_over_cap": (VALID_BODY.replace(PROMPT, "x" * 1201), "1200-character cap"),
    "bullet_over_cap": (VALID_BODY.replace("Do not invent a key.", "x" * 301), "300-character cap"),
    "compose_over_cap": (VALID_BODY.replace("generating-dbt-model", "x" * 81), "80-character cap"),
    "too_many_bullets": (VALID_BODY.replace("- The model builds in the sandbox.\n", "- Condition.\n" * 12), "between 1 and 12"),
    "instructions_over_cap": (VALID_BODY.replace(INSTRUCTIONS, "x" * 1501), "1500-character cap"),
    "too_many_compose": (VALID_BODY.replace("- generating-dbt-model\n", "- Compose item.\n" * 13), "between 1 and 12"),
    "too_many_ask_first": (
        VALID_BODY.replace("- Ask for the grain only if it cannot be inferred.\n", "- Ask item.\n" * 9),
        "between 1 and 8",
    ),
    "too_many_guardrails": (VALID_BODY.replace("- Do not invent a key.\n", "- Guardrail item.\n" * 11), "between 1 and 10"),
    "empty_ask_first": (VALID_BODY.replace("- Ask for the grain only if it cannot be inferred.\n", ""), "between 1 and 8"),
    "empty_guardrails": (VALID_BODY.replace("- Do not invent a key.\n", ""), "between 1 and 10"),
}


@pytest.mark.parametrize(("body", "fragment"), list(REJECTIONS.values()), ids=list(REJECTIONS))
def test_rejects_wrong_control(body, fragment):
    with pytest.raises(CookbookError, match=re.escape(fragment)):
        parse_body(body, SPEC)
