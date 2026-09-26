"""The breaking-change classifier and the version-bump check against a base commit."""

from __future__ import annotations

import copy
import json
import subprocess
from pathlib import Path
from typing import Any, Callable

import pytest

from check_schema_versions import FORMAT_RULE_FILES, SCHEMA_FILES, breaking_changes, check_versions, format_rule_regions
from samples import REPO_ROOT, load_schema

BASE: dict[str, Any] = {
    "version": 1,
    "title": "Sample",
    "type": "object",
    "additionalProperties": False,
    "required": ["id"],
    "$defs": {"token": {"type": "string"}},
    "properties": {
        "id": {"type": "string", "maxLength": 64},
        "kind": {"enum": ["a", "b"]},
        "tags": {"type": "array", "minItems": 0, "items": {"type": "string"}},
    },
}


def changed(mutate: Callable[[dict[str, Any]], None], base: dict[str, Any] = BASE) -> dict[str, Any]:
    head = copy.deepcopy(base)
    mutate(head)
    return head


NON_BREAKING = {
    "unchanged": lambda s: None,
    "add_optional_property": lambda s: s["properties"].update(note={"type": "string"}),
    "widen_enum": lambda s: s["properties"]["kind"]["enum"].append("c"),
    "raise_max_length": lambda s: s["properties"]["id"].update(maxLength=128),
    "drop_max_length": lambda s: s["properties"]["id"].pop("maxLength"),
    "drop_from_required": lambda s: s.update(required=[]),
    "edit_annotations": lambda s: s.update(title="Renamed", description="New words."),
    "add_def": lambda s: s["$defs"].update(extra={"type": "integer"}),
    "loosen_additional_properties": lambda s: s.update(additionalProperties=True),
}

BREAKING = {
    "remove_property": lambda s: s["properties"].pop("kind"),
    "rename_property": lambda s: s["properties"].update(kind_v2=s["properties"].pop("kind")),
    "remove_def": lambda s: s["$defs"].pop("token"),
    "newly_required": lambda s: s["required"].append("kind"),
    "narrow_enum": lambda s: s["properties"]["kind"]["enum"].remove("b"),
    "add_enum": lambda s: s["properties"]["tags"]["items"].update(enum=["x"]),
    "lower_max_length": lambda s: s["properties"]["id"].update(maxLength=32),
    "add_max_items": lambda s: s["properties"]["tags"].update(maxItems=3),
    "raise_min_items": lambda s: s["properties"]["tags"].update(minItems=1),
    "change_type": lambda s: s["properties"]["id"].update(type="integer"),
    "add_pattern": lambda s: s["properties"]["id"].update(pattern="^[a-z]+$"),
    "unique_items_on": lambda s: s["properties"]["tags"].update(uniqueItems=True),
}


@pytest.mark.parametrize("mutate", list(NON_BREAKING.values()), ids=list(NON_BREAKING))
def test_non_breaking_changes_are_classified_non_breaking(mutate):
    assert breaking_changes(BASE, changed(mutate)) == []


@pytest.mark.parametrize("mutate", list(BREAKING.values()), ids=list(BREAKING))
def test_breaking_changes_are_classified_breaking(mutate):
    assert breaking_changes(BASE, changed(mutate))


def test_tightening_additional_properties_is_breaking():
    base = changed(lambda s: s["properties"].update(meta={"type": "object"}))
    head = changed(lambda s: s["properties"]["meta"].update(additionalProperties=False), base)
    assert breaking_changes(base, head)


RECIPE = load_schema("recipe")


def body(mutate: Callable[[dict[str, Any]], None]) -> dict[str, Any]:
    head = copy.deepcopy(RECIPE)
    mutate(head["x-body"])
    return head


def test_raising_a_body_cap_is_non_breaking():
    assert breaking_changes(RECIPE, body(lambda b: b["sections"][0].update(max_chars=2000))) == []


def test_removing_a_denied_name_is_non_breaking():
    assert breaking_changes(RECIPE, body(lambda b: b["markup"]["denied_placeholder_names"].remove("user"))) == []


@pytest.mark.parametrize(
    "mutate",
    [
        lambda b: b["sections"][0].update(max_chars=1000),
        lambda b: b["sections"][1].update(min_items=2),
        lambda b: b["sections"][1].update(max_items=6),
        lambda b: b["sections"][0].update(forbid=["|", "#"]),
        lambda b: b["sections"].append({"heading": "### Notes", "kind": "paragraph", "field": "notes", "max_chars": 100}),
        lambda b: b["sections"][0].update(heading="## Task"),
        lambda b: b.update(max_bytes=8192),
        lambda b: b["markup"]["forbidden_substrings"].append("{{"),
        lambda b: b["markup"]["denied_placeholder_names"].append("model_name"),
        lambda b: b["markup"].update(placeholder_pattern="<[a-z]+>"),
    ],
    ids=[
        "lower_max_chars",
        "raise_min_items",
        "lower_max_items",
        "add_forbid",
        "add_section",
        "rename_heading",
        "lower_max_bytes",
        "add_forbidden_substring",
        "add_denied_name",
        "change_placeholder_pattern",
    ],
)
def test_body_tightening_is_breaking(mutate):
    assert breaking_changes(RECIPE, body(mutate))


def git(root: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=root, check=True, capture_output=True)


def write(root: Path, name: str, schema: dict[str, Any]) -> None:
    (root / "schema" / name).write_text(json.dumps(schema), encoding="utf-8")


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    git(tmp_path, "init", "-q")
    git(tmp_path, "config", "user.email", "test@example.com")
    git(tmp_path, "config", "user.name", "Test")
    git(tmp_path, "config", "commit.gpgsign", "false")
    (tmp_path / "schema").mkdir()
    for name in SCHEMA_FILES:
        write(tmp_path, name, BASE)
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-q", "-m", "base")
    return tmp_path


def test_unchanged_schemas_pass(repo):
    assert check_versions(repo, "HEAD") == []


def test_non_breaking_change_keeps_its_version(repo):
    write(repo, "recipe.schema.json", changed(NON_BREAKING["add_optional_property"]))
    assert check_versions(repo, "HEAD") == []


def test_breaking_change_without_bump_fails(repo):
    write(repo, "recipe.schema.json", changed(BREAKING["narrow_enum"]))
    (error,) = check_versions(repo, "HEAD")
    assert "breaking change without a version bump to 2" in error


def test_breaking_change_with_bump_passes(repo):
    write(repo, "recipe.schema.json", changed(lambda s: (BREAKING["narrow_enum"](s), s.update(version=2))))
    assert check_versions(repo, "HEAD") == []


def test_breaking_change_skipping_a_version_fails(repo):
    write(repo, "recipe.schema.json", changed(lambda s: (BREAKING["narrow_enum"](s), s.update(version=3))))
    assert check_versions(repo, "HEAD")


def test_bump_without_breaking_change_fails(repo):
    write(repo, "recipe.schema.json", changed(lambda s: s.update(version=2)))
    (error,) = check_versions(repo, "HEAD")
    assert "without a breaking change" in error


def test_non_integer_version_fails(repo):
    write(repo, "recipe.schema.json", changed(lambda s: s.update(version="1")))
    assert check_versions(repo, "HEAD")


def test_removed_schema_fails(repo):
    (repo / "schema" / "catalog.schema.json").unlink()
    (error,) = check_versions(repo, "HEAD")
    assert "removed" in error


def test_new_schema_starts_at_version_1(repo):
    git(repo, "rm", "-q", "schema/catalog.schema.json")
    git(repo, "commit", "-q", "-m", "drop catalog schema")
    write(repo, "catalog.schema.json", changed(lambda s: s.update(version=2)))
    assert check_versions(repo, "HEAD")
    write(repo, "catalog.schema.json", BASE)
    assert check_versions(repo, "HEAD") == []


def test_first_versioned_schema_is_version_1(repo):
    write(repo, "recipe.schema.json", changed(lambda s: s.pop("version")))
    git(repo, "commit", "-q", "-am", "unversioned base")
    write(repo, "recipe.schema.json", changed(BREAKING["narrow_enum"]))
    assert check_versions(repo, "HEAD") == []
    write(repo, "recipe.schema.json", changed(lambda s: s.update(version=2)))
    assert check_versions(repo, "HEAD")


def test_unknown_base_revision_fails(repo):
    (error,) = check_versions(repo, "no-such-rev")
    assert "not a commit" in error


MARKED = "def keep():\n    pass\n\n# format-rules: begin\ndef rule():\n    return 1\n# format-rules: end\n"


def write_script(root: Path, rel: str, text: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


@pytest.fixture
def marked_repo(repo: Path) -> Path:
    for rel in FORMAT_RULE_FILES:
        write_script(repo, rel, MARKED)
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "format-rule markers")
    return repo


def test_introducing_format_rule_markers_needs_no_bump(repo):
    write_script(repo, "scripts/recipe_format.py", MARKED)
    assert check_versions(repo, "HEAD") == []


def test_format_rule_edit_without_bump_fails(marked_repo):
    write_script(marked_repo, "scripts/recipe_format.py", MARKED.replace("return 1", "return 2"))
    (error,) = check_versions(marked_repo, "HEAD")
    assert error.startswith("schema/recipe.schema.json: breaking change without a version bump to 2")
    assert "scripts/recipe_format.py: format-rule region changed" in error


def test_format_rule_edit_with_bump_passes(marked_repo):
    write_script(marked_repo, "scripts/build_catalog.py", MARKED.replace("return 1", "return 2"))
    write(marked_repo, "recipe.schema.json", changed(lambda s: s.update(version=2)))
    assert check_versions(marked_repo, "HEAD") == []


def test_edit_outside_format_rules_needs_no_bump(marked_repo):
    write_script(marked_repo, "scripts/recipe_format.py", MARKED.replace("pass", "return None"))
    assert check_versions(marked_repo, "HEAD") == []


def test_removing_format_rule_markers_fails(marked_repo):
    write_script(marked_repo, "scripts/build_catalog.py", "def rule():\n    return 1\n")
    (error,) = check_versions(marked_repo, "HEAD")
    assert "scripts/build_catalog.py: format-rule regions removed" in error


def test_unbalanced_format_rule_markers_fail(marked_repo):
    write_script(marked_repo, "scripts/recipe_format.py", MARKED.replace("# format-rules: end\n", ""))
    (error,) = check_versions(marked_repo, "HEAD")
    assert "scripts/recipe_format.py: unbalanced" in error


def test_repository_marks_the_code_that_enforces_the_format_rules():
    regions = {rel: "\n".join(format_rule_regions((REPO_ROOT / rel).read_text(encoding="utf-8")) or []) for rel in FORMAT_RULE_FILES}
    for fragment in ("def split_frontmatter", "_NOT_A_PARAGRAPH = ", "def _section_value", "def parse_body"):
        assert fragment in regions["scripts/recipe_format.py"], fragment
    for fragment in (
        'raw.decode("utf-8")',
        'text.endswith("\\n\\n")',
        'b"\\r" in raw',
        '"\\r" in value',
        "parse_body(body_text, spec)",
    ):
        assert fragment in regions["scripts/build_catalog.py"], fragment
