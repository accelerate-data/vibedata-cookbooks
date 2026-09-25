"""templates/recipe.md follows the body rules and names every frontmatter key a Recipe needs."""

from __future__ import annotations

from recipe_format import check_markup, load_frontmatter, parse_body, split_frontmatter
from samples import REPO_ROOT, load_schema

SCHEMA = load_schema("recipe")
TEMPLATE = REPO_ROOT / "templates/recipe.md"


def test_template_body_passes_the_body_and_markup_rules():
    _, body = split_frontmatter(TEMPLATE.read_text(encoding="utf-8"))
    check_markup(body, SCHEMA["x-body"]["markup"], "template body")
    parse_body(body, SCHEMA["x-body"])


def test_template_frontmatter_names_every_required_key_and_only_known_keys():
    frontmatter, _ = split_frontmatter(TEMPLATE.read_text(encoding="utf-8"))
    meta = load_frontmatter(frontmatter)
    assert set(SCHEMA["required"]) <= set(meta) <= set(SCHEMA["properties"])
    assert set(meta["works_with"]) == {"platforms", "tools"}
    assert set(meta["evidence"]) == {"features", "evals"}
