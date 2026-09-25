"""check_markup: placeholders pass; anything that could escape a section is rejected."""

from __future__ import annotations

import pytest

from recipe_format import CookbookError, check_markup
from samples import load_schema

MARKUP = load_schema("recipe")["x-body"]["markup"]

# Built by concatenation so this file never holds a literal chat or tool tag.
REMINDER_TAG = "<" + "system-reminder>"
TOOL_PREFIX = "antml" + ":invoke"


@pytest.mark.parametrize(
    "text",
    [
        "plain text",
        "<model_name>",
        "Load <resource_list> on <cursor_field> with chunk size <n>.",
        "a > b",
        "AT&T",
        "line one\nline two",
        "Use `dbt build --select <model_name>`.",
    ],
    ids=["plain", "placeholder", "several_placeholders", "greater_than", "bare_ampersand", "newline", "inline_code"],
)
def test_allows(text):
    check_markup(text, MARKUP, "field")


@pytest.mark.parametrize(
    "text",
    [
        "</p>",
        "<div>",
        "<DIV>",
        "<br/>",
        "<p>",
        REMINDER_TAG,
        "<system_reminder>",
        "<function_calls>",
        "<invoke>",
        "<!-- hidden -->",
        "<?xml version='1.0'?>",
        "<![CDATA[x]]>",
        "&lt;script&gt;",
        "&#60;",
        "&#x3C;",
        "```python",
        "~~~",
        "a < b",
        "<Model Name>",
        "zero\u200bwidth",
        "bidi\u202eflip",
        "bell\x07",
        "carriage\rreturn",
        "\ufeffbom",
        TOOL_PREFIX,
    ],
    ids=[
        "closing_tag",
        "html_tag",
        "uppercase_tag",
        "self_closing_tag",
        "single_letter_tag",
        "reminder_tag",
        "reminder_placeholder_form",
        "tool_call_tag",
        "invoke_tag",
        "html_comment",
        "processing_instruction",
        "cdata",
        "named_entity",
        "decimal_entity",
        "hex_entity",
        "backtick_fence",
        "tilde_fence",
        "bare_less_than",
        "placeholder_with_space",
        "zero_width_space",
        "bidi_override",
        "control_char",
        "carriage_return",
        "byte_order_mark",
        "tool_namespace",
    ],
)
def test_rejects_wrong_control(text):
    with pytest.raises(CookbookError):
        check_markup(text, MARKUP, "field")


def test_error_names_the_field():
    with pytest.raises(CookbookError, match="frontmatter.pitch"):
        check_markup("<div>", MARKUP, "frontmatter.pitch")
