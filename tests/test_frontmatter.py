"""split_frontmatter and load_frontmatter: the valid sample and each wrong control."""

from __future__ import annotations

import pytest

from recipe_format import CookbookError, load_frontmatter, split_frontmatter
from samples import VALID_BODY, VALID_FRONTMATTER, VALID_META, VALID_RECIPE


def test_split_returns_frontmatter_and_body():
    assert split_frontmatter(VALID_RECIPE) == (VALID_FRONTMATTER, VALID_BODY)


def test_valid_frontmatter_loads_to_the_sample_meta():
    assert load_frontmatter(VALID_FRONTMATTER) == VALID_META


@pytest.mark.parametrize(
    ("text", "fragment"),
    [
        (VALID_RECIPE[4:], "must start with"),
        ("\n" + VALID_RECIPE, "must start with"),
        ("---\n" + VALID_FRONTMATTER + VALID_BODY, "no closing"),
    ],
    ids=["no_opening_line", "blank_line_first", "no_closing_line"],
)
def test_split_rejects_wrong_control(text, fragment):
    with pytest.raises(CookbookError, match=fragment):
        split_frontmatter(text)


@pytest.mark.parametrize(
    ("yaml_text", "fragment"),
    [
        (VALID_FRONTMATTER + "id: again\n", "duplicate frontmatter key 'id'"),
        ("- a\n- b\n", "must be a YAML mapping"),
        ("", "must be a YAML mapping"),
        ("id: [unclosed\n", "not valid YAML"),
        (VALID_FRONTMATTER + "published: 2026-09-25\n", "quote it as a string"),
        ("1: numeric key\n", "must be a string"),
    ],
    ids=["duplicate_key", "list_not_mapping", "empty", "invalid_yaml", "unquoted_date", "numeric_key"],
)
def test_load_rejects_wrong_control(yaml_text, fragment):
    with pytest.raises(CookbookError, match=fragment):
        load_frontmatter(yaml_text)
