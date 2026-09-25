# VD-6115 Cookbook Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish one versioned Recipe contract from `vibedata-cookbooks`: Markdown Recipes with schema-validated frontmatter, a generated metadata-only catalog validated by its own schema, versioned schemas guarded by CI, and three new Recipes in the new format.

**Architecture:** Each Recipe becomes `recipes/<id>/recipe.md` (YAML frontmatter plus a closed set of Markdown sections). `schema/recipe.schema.json` validates the frontmatter and, under its `x-body` key, publishes the body and markup rules as data, so the build script and Studio's refresh gate read the same rules. `scripts/build_catalog.py` validates every Recipe and Collection and writes a sorted, byte-stable `catalog.json` holding metadata plus each file's `path` and `sha256`. `scripts/check_schema_versions.py` compares each schema against the merge base and fails a breaking change that does not raise the schema's top-level `version`.

**Tech Stack:** Python 3.12 (3.10 minimum), PyYAML 6.0.2, jsonschema 4.23.0 (JSON Schema draft 2020-12), pytest 8.3.4, GitHub Actions.

**Spec:** Linear VD-6115 (acceptance criteria) and the agreed decisions recorded in the Contract section below, which is the binding copy for this repository. Downstream plans (Studio VD-6112/VD-6116 and the plugin VD-6114) consume the Contract section verbatim.

> **Review gate:** the product owner reviews this Contract section and the three new Recipes' full text (Tasks 10, 11 and 12) before any task starts. Do not begin Task 1 until that review is recorded, and apply any change it asks for to this plan first.

## Contract

Two downstream plans read these exact values. Any change to them during implementation must be reported back before it lands.

### Recipe file

- Path: `recipes/<id>/recipe.md`. The directory name equals `id`. The directory contains `recipe.md` and nothing else (dotfiles are ignored). `recipe.json` and the generated per-Recipe `README.md` no longer exist.
- Encoding: UTF-8, LF line endings, no BOM, at most **16384 bytes**, ending with exactly one `\n`.
- Layout: the first line is `---`, then YAML frontmatter, then a line `---`, then the body.

### Frontmatter keys (validated by `schema/recipe.schema.json`, `additionalProperties: false`)

| Key | Type | Required | Rule and cap |
| --- | --- | --- | --- |
| `id` | string | yes | `^[a-z0-9]+(?:-[a-z0-9]+)*$`, at most 64 characters |
| `title` | string | yes | one line, at most 120 characters; a literal deliverable title |
| `trigger` | list of strings | yes | 1 to 5 unique items, each one line of at most 200 characters |
| `description` | string | yes | one line, at most 400 characters |
| `pitch` | string | no | one sentence for hero cards: one line, at most 160 characters, ends with `.`, `!` or `?`, and has no `.`, `!` or `?` followed by whitespace before the end |
| `job_category` | enum | yes | `get-running`, `re-engineer`, `build`, `prove`, `explain`, `cross-platform` |
| `area` | string | yes | `^[a-z0-9]+(?:-[a-z0-9]+)*$`, at most 40 characters |
| `readiness` | enum | yes | `proven`, `supported`, `planned` |
| `function` | list of strings | no | at most 10 unique tokens |
| `industry` | list of strings | no | at most 10 unique tokens |
| `domain_objects` | list of strings | no | at most 20 unique tokens |
| `works_with` | object | yes | `additionalProperties: false`; `platforms` required |
| `works_with.platforms` | list of enums | yes | at least 1 unique platform value |
| `works_with.tools` | list of strings | no | at most 10 unique tokens |
| `qualifiers` | list of strings | no | at most 10 unique items, each one line of at most 120 characters |
| `related` | list of strings | no | at most 10 unique Recipe ids; each must name an existing Recipe |
| `evidence` | object | no | `additionalProperties: false`; keys `features`, `evals` |
| `evidence.features` | list of strings | no | at most 20 unique tokens |
| `evidence.evals` | list of strings | no | at most 20 unique items, each one line of at most 200 characters |

- A token is `^[a-z0-9]+(?:[_-][a-z0-9]+)*$`, at most 64 characters.
- `readiness: proven` requires `evidence.evals` with at least one item (schema `allOf` / `if` / `then`).
- Every frontmatter string is a single line. The build script rejects any `\n` or `\r` in a frontmatter string, because Python's `$` also matches before a trailing newline and would otherwise let one through the schema's line pattern.
- YAML is parsed with a safe loader that rejects duplicate keys, non-string keys, and non-JSON values (an unquoted date, for example). `canonical_url` is not a frontmatter key: the catalog's `source` plus `path` locate the file.
- `compose` is an advisory hint: the cookbook applies only the length caps to it, holds no plugin skill list, and never checks that a name exists.

### Platform enum

`duckdb_local`, `motherduck`, `fabric_lakehouse`, `fabric_warehouse`, `redshift`. These are Studio's own values; there is no mapping anywhere. `duckdb` and a generic `fabric` are rejected everywhere, including Collection selectors and subfilters.

### Body

The body holds exactly these headings, each exactly once, in this order, and no other line may start with `#`:

1. `## Prompt`: one paragraph on one line, at most **1200** characters, containing no `|`. It lands verbatim in a Markdown table cell.
2. `## Verified by`: 1 to **12** bullets, each at most **300** characters; one acceptance condition per bullet.
3. `## Agent guidance`: holds only its four subsections; no text of its own.
4. `### Instructions`: one paragraph on one line, at most **1500** characters.
5. `### Compose`: 1 to **12** bullets, each at most **80** characters.
6. `### Ask first`: 1 to **8** bullets, each at most **300** characters.
7. `### Guardrails`: 1 to **10** bullets, each at most **300** characters.

Body rules:

- Every section must be non-empty. Blank lines may surround section content but may not appear inside a bullet list.
- A bullet is a line starting with `- ` followed by non-empty text with no leading or trailing whitespace. No other list marker (`*`, `+`, `1.`), no nesting, no indentation.
- A paragraph is exactly one non-blank line that does not start with a list marker, `>` or `|`.
- No line in the body may have leading or trailing whitespace. Nothing but blank lines may precede `## Prompt`.
- Character counts are Unicode code points.

Markup rules, applied to the whole body and to every frontmatter and Collection string:

- Forbidden substrings: `</`, `<!`, `<?`, `]]>`, three backticks, `~~~`, and the tool-call namespace prefix `antml:`.
- Forbidden characters: U+0000 to U+0009, U+000B to U+001F, U+007F, U+200B to U+200F, U+202A to U+202E, U+2066 to U+2069, U+FEFF.
- Forbidden HTML entities: `&name;`, `&#123;`, `&#x7B;`.
- Every `<` must open a placeholder matching `<[a-z][a-z0-9_]*>` whose name is not an HTML element name or a tool-call or chat-role word (the list is `x-body.markup.denied_placeholder_names`). So `<model_name>` passes, while `<div>`, `<DIV>`, `<br/>`, `<system-reminder>`, `<function_calls>` and `a < b` are rejected.

The rules above are published as data in `recipe.schema.json` under `x-body` (`max_bytes`, `sections[]` with `heading`, `kind`, `field`, `max_chars`, `min_items`, `max_items`, `forbid`, and `markup` with `forbidden_substrings`, `forbidden_chars_pattern`, `entity_pattern`, `placeholder_pattern`, `denied_placeholder_names`). The parsed body maps to `prompt`, `verified_by`, and `agent_guidance.{instructions, compose, ask_first, guardrails}`, the same names the JSON Recipe used.

### Schemas

| File | `version` | Validates |
| --- | --- | --- |
| `schema/recipe.schema.json` | `1` | Recipe frontmatter; `x-body` holds the body rules |
| `schema/catalog.schema.json` | `1` | `catalog.json` |
| `schema/collection.schema.json` | `1` | `collections/<id>.json` |

`version` is a top-level integer on each schema document (a sibling of `$schema`). It is raised by exactly 1, and only for a breaking change. A change is breaking when it removes or renames a property or `$defs` entry, makes a key newly required, removes an enum value or adds an enum, lowers an upper bound or adds one (`maxLength`, `maxItems`, `maximum`, `maxProperties`), raises a lower bound or adds one (`minLength`, `minItems`, `minimum`, `minProperties`), sets `uniqueItems` to true, tightens `additionalProperties`, changes any other validation keyword (`type`, `pattern`, `const`, `$ref`, `$id`, and so on), or tightens `x-body` (a changed heading list, kind or field; a lowered `max_bytes`, `max_chars` or `max_items`; a raised `min_items`; an added `forbid`, forbidden substring or denied name; a changed pattern). Changing any of the prose file and line rules that are not expressed as `x-body` data is also breaking and raises `recipe.schema.json`'s `version`: UTF-8, LF, no BOM and exactly one trailing newline; the bullet line rule; the paragraph rule; no leading or trailing whitespace on body lines; and nothing but blank lines before `## Prompt`. `scripts/check_schema_versions.py` treats any edit inside a `# format-rules: begin` / `# format-rules: end` region of `scripts/recipe_format.py` or `scripts/build_catalog.py` as such a change. Adding an optional property, widening an enum, raising a cap, dropping a key from `required`, loosening `additionalProperties`, and editing `title`, `description`, `$comment` or `examples` are not breaking. Any change the classifier cannot prove is loosening is treated as breaking. Raising `version` without a breaking change also fails.

### Catalog (`catalog.json`, generated)

Top-level keys, all required, `additionalProperties: false`:

- `source`: `"https://github.com/accelerate-data/vibedata-cookbooks"`.
- `schema_versions`: `{"catalog": 1, "collection": 1, "recipe": 1}`, read from the schema files at build time.
- `recipes`: list of Recipe entries sorted by `id`.
- `collections`: list of Collection entries sorted by `id`.

Recipe entry: exactly the Recipe's frontmatter as published (optional keys absent from the frontmatter are absent from the entry), plus:

- `path`: `"recipes/<id>/recipe.md"` (POSIX, relative to the repository root; pattern `^recipes/[a-z0-9]+(?:-[a-z0-9]+)*/recipe\.md$`).
- `sha256`: lowercase hex SHA-256 of the raw bytes of that `recipe.md` (pattern `^[0-9a-f]{64}$`).

An entry never holds `prompt`, `verified_by`, `agent_guidance`, `canonical_url` or `revision`. `evidence` stays. The catalog holds no `revision` at any level: the served identity is the Git commit a reader fetched.

Collection entry: the Collection source object as published, plus `resolved_members` (sorted unique Recipe ids), `supported_or_proven_count` (integer at least 0), `website_publication_threshold` (3 for `kind: function`, otherwise 1), and `website_visible` (boolean, count at least threshold).

Serialization: `json.dumps(catalog, indent=2, ensure_ascii=False, sort_keys=True) + "\n"`, written as UTF-8 bytes. Regenerating from the same sources is byte-identical. List values inside an entry keep their authored order.

### Collection source (`collections/<id>.json`)

Keys: `id` (Recipe-id pattern, equals the filename stem), `title` (one line, at most 120), `kind` (`function`, `industry`, `platform`, `curated`, `problem-area`), `description` (one line, at most 400), and at least one of `members` (at most 500 unique existing Recipe ids) or `selector` (`function`, `industry`: token lists; `platforms_any`: platform enum list; `job_category`: job-category enum list; each list non-empty and unique). Optional `subfilters`: at most 20 objects of `id` (Recipe-id pattern), `title` (one line, at most 60) and optional `platforms_any`. `additionalProperties: false` at every level.

## Global Constraints

- Repository: `accelerate-data/vibedata-cookbooks`, worktree `/Users/ukakkad/vibeData/worktrees/feature/vd-6115-cookbook-contract-markdown-recipes-a-metadata-only-catalog`, branch `feature/vd-6115-cookbook-contract-markdown-recipes-a-metadata-only-catalog`. Do not push.
- Dependencies are pinned exactly in `requirements.txt`: `PyYAML==6.0.2`, `jsonschema==4.23.0`, `pytest==8.3.4`. CI installs from that file; nothing else is installed.
- Local environment: `python3 -m venv .venv && .venv/bin/python -m pip install -r requirements.txt`. Every local command below uses `.venv/bin/python`.
- The existing Recipe `dbt-full-refresh-to-incremental` keeps byte-identical `prompt`, `verified_by` and `agent_guidance` text.
- New Recipes: `api-to-bronze-incremental-contract` (all five platforms, `supported`), `fabric-data-pipeline-as-code` (`fabric_lakehouse`, `fabric_warehouse`, `supported`), `motherduck-flight-scheduling` (`motherduck` only, `supported`). Each has a literal deliverable title, separate triggers, a paste-and-adapt prompt with `<placeholders>`, and guidance hidden from the invocation surface. No plugin evals are built for them, so `evidence.evals` is `[]`.
- Out of scope: signed releases, release tags, branch protection, CODEOWNERS, Studio's reader, the plugin's adoption guide.
- Markdown prose: each paragraph is one long line with no hard wraps. No emojis.
- One concern per commit; stage files by name (`git add <file>`); end every commit message with `Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>`.
- Each commit leaves `.venv/bin/python -m pytest -q` green, except where a step says a named test is expected to fail before its implementation step.

## File Structure

| Path | Responsibility |
| --- | --- |
| `requirements.txt` | Pinned Python dependencies for local runs and CI |
| `pytest.ini` | Points pytest at `tests/` |
| `.gitignore`, `.gitattributes` | Ignore the venv and caches; force LF so `sha256` is stable on every checkout |
| `schema/recipe.schema.json` | Frontmatter contract plus `x-body` body and markup rules, `version: 1` |
| `schema/collection.schema.json` | Collection contract, `version: 1` |
| `schema/catalog.schema.json` | Catalog contract, `version: 1`; copies the Recipe and Collection properties exactly |
| `scripts/recipe_format.py` | `CookbookError`, frontmatter split, strict YAML load, body parse, markup check |
| `scripts/build_catalog.py` | Loads schemas, validates Recipes and Collections, writes or checks `catalog.json` |
| `scripts/check_schema_versions.py` | Breaking-change classifier and version-bump check against a base commit |
| `recipes/<id>/recipe.md` | One file per Recipe |
| `catalog.json` | Generated |
| `templates/recipe.md` | Contributor starting point |
| `CONTRIBUTING.md`, `README.md` | Contributor guide and repository overview |
| `docs/adr/0001-cookbook-recipe-contract.md` | The contract decision |
| `.github/workflows/ci.yml` | Runs tests, `--check`, and the version-bump check |
| `tests/samples.py` | Shared valid samples and tree helpers |
| `tests/conftest.py` | Puts `scripts/` on `sys.path`; the `cookbook` fixture |
| `tests/test_*.py` | One test module per unit |
| `tests/fixtures/legacy-dbt-full-refresh-to-incremental.json` | Frozen copy of the pre-conversion `recipe.json` for the round-trip test |

---

### Task 1: Test tooling and the Recipe schema

**Files:**
- Create: `requirements.txt`, `pytest.ini`, `.gitignore`, `.gitattributes`, `tests/conftest.py`, `tests/samples.py`, `tests/test_recipe_schema.py`
- Modify: `schema/recipe.schema.json` (full rewrite)

**Interfaces:**
- Produces: `samples.REPO_ROOT: Path`, `samples.load_schema(name: str) -> dict`, `samples.VALID_META: dict`, `samples.VALID_FRONTMATTER: str`, `samples.VALID_BODY: str`, `samples.VALID_BODY_FIELDS: dict`, `samples.VALID_RECIPE: str`, `samples.write_recipe(root: Path, recipe_id: str, text: str) -> Path`, `samples.make_cookbook(root: Path) -> Path`; `schema/recipe.schema.json` with `version: 1` and `x-body`.

- [ ] **Step 1: Create the tooling files**

`requirements.txt`:

```text
PyYAML==6.0.2
jsonschema==4.23.0
pytest==8.3.4
```

`pytest.ini`:

```ini
[pytest]
testpaths = tests
```

`.gitignore`:

```text
.venv/
__pycache__/
.pytest_cache/
.DS_Store
```

`.gitattributes`:

```text
* text=auto eol=lf
```

`tests/conftest.py`:

```python
"""Shared pytest setup: make scripts/ importable and provide a cookbook tree."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from samples import make_cookbook  # noqa: E402


@pytest.fixture
def cookbook(tmp_path: Path) -> Path:
    """A minimal valid cookbook: the real schemas, one Recipe, no Collections."""
    return make_cookbook(tmp_path)
```

`tests/samples.py`:

```python
"""Valid sample Recipe content and helpers for building cookbook trees in tests."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]


def load_schema(name: str) -> dict[str, Any]:
    return json.loads((REPO_ROOT / "schema" / f"{name}.schema.json").read_text(encoding="utf-8"))


VALID_META: dict[str, Any] = {
    "id": "sample-recipe",
    "title": "Build a sample model and prove its output",
    "trigger": ["A sample situation calls for this Recipe."],
    "description": "Build a sample model from its upstream model and prove its output against an agreed slice.",
    "job_category": "build",
    "area": "transformation",
    "readiness": "supported",
    "works_with": {"platforms": ["duckdb_local"]},
}

VALID_FRONTMATTER = """id: sample-recipe
title: Build a sample model and prove its output
trigger:
  - A sample situation calls for this Recipe.
description: Build a sample model from its upstream model and prove its output against an agreed slice.
job_category: build
area: transformation
readiness: supported
works_with:
  platforms:
    - duckdb_local
"""

VALID_BODY = """
## Prompt

Build <model_name> from <upstream_model> and prove its output.

## Verified by

- The model builds in the sandbox.
- The output matches the agreed slice.

## Agent guidance

### Instructions

Inspect the upstream model before writing SQL.

### Compose

- generating-dbt-model

### Ask first

- Ask for the grain only if it cannot be inferred.

### Guardrails

- Do not invent a key.
"""

VALID_BODY_FIELDS: dict[str, Any] = {
    "prompt": "Build <model_name> from <upstream_model> and prove its output.",
    "verified_by": ["The model builds in the sandbox.", "The output matches the agreed slice."],
    "agent_guidance": {
        "instructions": "Inspect the upstream model before writing SQL.",
        "compose": ["generating-dbt-model"],
        "ask_first": ["Ask for the grain only if it cannot be inferred."],
        "guardrails": ["Do not invent a key."],
    },
}

VALID_RECIPE = "---\n" + VALID_FRONTMATTER + "---\n" + VALID_BODY


def write_recipe(root: Path, recipe_id: str, text: str) -> Path:
    directory = root / "recipes" / recipe_id
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "recipe.md"
    path.write_bytes(text.encode("utf-8"))
    return path


def make_cookbook(root: Path) -> Path:
    shutil.copytree(REPO_ROOT / "schema", root / "schema")
    (root / "collections").mkdir()
    write_recipe(root, "sample-recipe", VALID_RECIPE)
    return root
```

- [ ] **Step 2: Write the failing schema tests**

`tests/test_recipe_schema.py`:

```python
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
```

- [ ] **Step 3: Create the venv and run the tests to verify they fail**

Run: `python3 -m venv .venv && .venv/bin/python -m pip install -q -r requirements.txt && .venv/bin/python -m pytest tests/test_recipe_schema.py -q`
Expected: FAIL. `test_schema_is_valid_draft_2020_12_with_version_1` fails with `KeyError: 'version'`, `test_valid_meta_passes` fails because the old schema requires `prompt`, and `test_body_spec_lists_the_closed_heading_set_in_order` fails with `KeyError: 'x-body'`.

- [ ] **Step 4: Rewrite `schema/recipe.schema.json`**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/accelerate-data/vibedata-cookbooks/schema/recipe.schema.json",
  "version": 1,
  "title": "VibeData Recipe frontmatter",
  "description": "The YAML frontmatter of recipes/<id>/recipe.md. x-body publishes the body and markup rules that scripts/build_catalog.py enforces.",
  "type": "object",
  "additionalProperties": false,
  "required": ["id", "title", "trigger", "description", "job_category", "area", "readiness", "works_with"],
  "$defs": {
    "id": { "type": "string", "pattern": "^[a-z0-9]+(?:-[a-z0-9]+)*$", "maxLength": 64 },
    "line": { "type": "string", "pattern": "^[^\\r\\n]*\\S[^\\r\\n]*$" },
    "token": { "type": "string", "pattern": "^[a-z0-9]+(?:[_-][a-z0-9]+)*$", "maxLength": 64 },
    "platform": { "enum": ["duckdb_local", "motherduck", "fabric_lakehouse", "fabric_warehouse", "redshift"] }
  },
  "properties": {
    "id": { "$ref": "#/$defs/id" },
    "title": { "$ref": "#/$defs/line", "maxLength": 120 },
    "trigger": {
      "type": "array",
      "minItems": 1,
      "maxItems": 5,
      "uniqueItems": true,
      "items": { "$ref": "#/$defs/line", "maxLength": 200 }
    },
    "description": { "$ref": "#/$defs/line", "maxLength": 400 },
    "pitch": { "$ref": "#/$defs/line", "maxLength": 160, "pattern": "^(?!.*[.!?]\\s).*[.!?]$" },
    "job_category": { "enum": ["get-running", "re-engineer", "build", "prove", "explain", "cross-platform"] },
    "area": { "type": "string", "pattern": "^[a-z0-9]+(?:-[a-z0-9]+)*$", "maxLength": 40 },
    "readiness": { "enum": ["proven", "supported", "planned"] },
    "function": { "type": "array", "maxItems": 10, "uniqueItems": true, "items": { "$ref": "#/$defs/token" } },
    "industry": { "type": "array", "maxItems": 10, "uniqueItems": true, "items": { "$ref": "#/$defs/token" } },
    "domain_objects": { "type": "array", "maxItems": 20, "uniqueItems": true, "items": { "$ref": "#/$defs/token" } },
    "works_with": {
      "type": "object",
      "additionalProperties": false,
      "required": ["platforms"],
      "properties": {
        "platforms": { "type": "array", "minItems": 1, "uniqueItems": true, "items": { "$ref": "#/$defs/platform" } },
        "tools": { "type": "array", "maxItems": 10, "uniqueItems": true, "items": { "$ref": "#/$defs/token" } }
      }
    },
    "qualifiers": { "type": "array", "maxItems": 10, "uniqueItems": true, "items": { "$ref": "#/$defs/line", "maxLength": 120 } },
    "related": { "type": "array", "maxItems": 10, "uniqueItems": true, "items": { "$ref": "#/$defs/id" } },
    "evidence": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "features": { "type": "array", "maxItems": 20, "uniqueItems": true, "items": { "$ref": "#/$defs/token" } },
        "evals": { "type": "array", "maxItems": 20, "uniqueItems": true, "items": { "$ref": "#/$defs/line", "maxLength": 200 } }
      }
    }
  },
  "allOf": [
    {
      "if": { "required": ["readiness"], "properties": { "readiness": { "const": "proven" } } },
      "then": {
        "required": ["evidence"],
        "properties": { "evidence": { "required": ["evals"], "properties": { "evals": { "minItems": 1 } } } }
      }
    }
  ],
  "x-body": {
    "max_bytes": 16384,
    "sections": [
      { "heading": "## Prompt", "kind": "paragraph", "field": "prompt", "max_chars": 1200, "forbid": ["|"] },
      { "heading": "## Verified by", "kind": "bullets", "field": "verified_by", "min_items": 1, "max_items": 12, "max_chars": 300 },
      { "heading": "## Agent guidance", "kind": "container" },
      { "heading": "### Instructions", "kind": "paragraph", "field": "agent_guidance.instructions", "max_chars": 1500 },
      { "heading": "### Compose", "kind": "bullets", "field": "agent_guidance.compose", "min_items": 1, "max_items": 12, "max_chars": 80 },
      { "heading": "### Ask first", "kind": "bullets", "field": "agent_guidance.ask_first", "min_items": 1, "max_items": 8, "max_chars": 300 },
      { "heading": "### Guardrails", "kind": "bullets", "field": "agent_guidance.guardrails", "min_items": 1, "max_items": 10, "max_chars": 300 }
    ],
    "markup": {
      "forbidden_substrings": ["</", "<!", "<?", "]]>", "```", "~~~", "antml:"],
      "forbidden_chars_pattern": "[\\u0000-\\u0009\\u000B-\\u001F\\u007F\\u200B-\\u200F\\u202A-\\u202E\\u2066-\\u2069\\uFEFF]",
      "entity_pattern": "&(?:#[0-9]+|#[xX][0-9a-fA-F]+|[A-Za-z][A-Za-z0-9]*);",
      "placeholder_pattern": "<[a-z][a-z0-9_]*>",
      "denied_placeholder_names": [
        "a", "abbr", "address", "area", "article", "aside", "audio", "b", "base", "bdi", "bdo", "blockquote", "body", "br", "button",
        "canvas", "caption", "cite", "code", "col", "colgroup", "data", "datalist", "dd", "del", "details", "dfn", "dialog", "div", "dl", "dt",
        "em", "embed", "fieldset", "figcaption", "figure", "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6", "head", "header", "hgroup",
        "hr", "html", "i", "iframe", "img", "input", "ins", "kbd", "label", "legend", "li", "link", "main", "map", "mark", "math", "menu",
        "meta", "meter", "nav", "noscript", "object", "ol", "optgroup", "option", "output", "p", "param", "picture", "pre", "progress", "q",
        "rp", "rt", "ruby", "s", "samp", "script", "search", "section", "select", "slot", "small", "source", "span", "strong", "style", "sub",
        "summary", "sup", "svg", "table", "tbody", "td", "template", "textarea", "tfoot", "th", "thead", "time", "title", "tr", "track", "u",
        "ul", "var", "video", "wbr",
        "assistant", "function_calls", "function_results", "human", "invoke", "parameter", "system", "system_reminder", "thinking",
        "tool_call", "tool_result", "tool_use", "user"
      ]
    }
  }
}
```

- [ ] **Step 5: Run the tests to verify they pass**

Run: `.venv/bin/python -m pytest tests/test_recipe_schema.py -q`
Expected: PASS (all tests).

- [ ] **Step 6: Commit**

```bash
git add requirements.txt pytest.ini .gitignore .gitattributes tests/conftest.py tests/samples.py tests/test_recipe_schema.py schema/recipe.schema.json
git commit -m "feat(schema): version 1 Recipe frontmatter schema with published body rules

Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>"
```

---

### Task 2: Collection schema and catalog schema

**Files:**
- Modify: `schema/collection.schema.json` (full rewrite)
- Create: `schema/catalog.schema.json`, `tests/test_collection_and_catalog_schemas.py`

**Interfaces:**
- Consumes: `samples.load_schema`, `samples.VALID_META`, `schema/recipe.schema.json` (`$defs`, `properties`, `required`, `allOf`).
- Produces: `schema/collection.schema.json` `version: 1`; `schema/catalog.schema.json` `version: 1` with `$defs.recipe_entry` and `$defs.collection_entry`.

- [ ] **Step 1: Write the failing tests**

`tests/test_collection_and_catalog_schemas.py`:

```python
"""collection.schema.json and catalog.schema.json: validity, mirroring, wrong controls."""

from __future__ import annotations

import copy
from typing import Any

import pytest
from jsonschema import Draft202012Validator

from samples import VALID_META, load_schema

RECIPE = load_schema("recipe")
COLLECTION = load_schema("collection")
CATALOG = load_schema("catalog")

RECIPE_ENTRY_EXTRA = {"path", "sha256"}
COLLECTION_ENTRY_EXTRA = {"resolved_members", "supported_or_proven_count", "website_publication_threshold", "website_visible"}

VALID_COLLECTION: dict[str, Any] = {
    "id": "sample",
    "title": "Sample",
    "kind": "curated",
    "description": "A sample collection.",
    "members": ["sample-recipe"],
}

VALID_CATALOG: dict[str, Any] = {
    "source": "https://github.com/accelerate-data/vibedata-cookbooks",
    "schema_versions": {"recipe": 1, "catalog": 1, "collection": 1},
    "recipes": [{**VALID_META, "path": "recipes/sample-recipe/recipe.md", "sha256": "0" * 64}],
    "collections": [
        {
            **VALID_COLLECTION,
            "resolved_members": ["sample-recipe"],
            "supported_or_proven_count": 1,
            "website_publication_threshold": 1,
            "website_visible": True,
        }
    ],
}


def errors(schema: dict[str, Any], instance: Any) -> list[Any]:
    return list(Draft202012Validator(schema).iter_errors(instance))


@pytest.mark.parametrize("schema", [COLLECTION, CATALOG], ids=["collection", "catalog"])
def test_schema_is_valid_with_version_1(schema):
    Draft202012Validator.check_schema(schema)
    assert schema["version"] == 1


def test_shared_defs_are_identical_across_schemas():
    for name, definition in RECIPE["$defs"].items():
        assert COLLECTION["$defs"][name] == definition
        assert CATALOG["$defs"][name] == definition


def test_recipe_entry_mirrors_recipe_schema_exactly():
    entry = CATALOG["$defs"]["recipe_entry"]
    assert {k: v for k, v in entry["properties"].items() if k not in RECIPE_ENTRY_EXTRA} == RECIPE["properties"]
    assert entry["required"] == RECIPE["required"] + ["path", "sha256"]
    assert entry["allOf"] == RECIPE["allOf"]
    assert entry["additionalProperties"] is False


def test_collection_entry_mirrors_collection_schema_exactly():
    entry = CATALOG["$defs"]["collection_entry"]
    assert {k: v for k, v in entry["properties"].items() if k not in COLLECTION_ENTRY_EXTRA} == COLLECTION["properties"]
    assert entry["required"] == COLLECTION["required"] + [
        "resolved_members",
        "supported_or_proven_count",
        "website_publication_threshold",
        "website_visible",
    ]
    assert entry["anyOf"] == COLLECTION["anyOf"]
    assert entry["additionalProperties"] is False


def test_valid_collection_passes():
    assert errors(COLLECTION, VALID_COLLECTION) == []
    selector_collection = {**{k: v for k, v in VALID_COLLECTION.items() if k != "members"}, "selector": {"platforms_any": ["duckdb_local"]}}
    assert errors(COLLECTION, selector_collection) == []


@pytest.mark.parametrize(
    "collection",
    [
        {k: v for k, v in VALID_COLLECTION.items() if k != "members"},
        {**VALID_COLLECTION, "selector": {"platforms_any": ["duckdb"]}},
        {**VALID_COLLECTION, "selector": {"platforms_any": []}},
        {**VALID_COLLECTION, "subfilters": [{"id": "local", "title": "Local", "platforms_any": ["duckdb"]}]},
        {**VALID_COLLECTION, "kind": "persona"},
        {**VALID_COLLECTION, "members": ["Not An Id"]},
        {**VALID_COLLECTION, "owner": "someone"},
    ],
    ids=["no_members_or_selector", "legacy_duckdb_selector", "empty_selector_list", "legacy_duckdb_subfilter", "unknown_kind", "bad_member_id", "extra_key"],
)
def test_collection_rejects_wrong_control(collection):
    assert errors(COLLECTION, collection)


def test_valid_catalog_passes():
    assert errors(CATALOG, VALID_CATALOG) == []


def catalog_with(mutate) -> dict[str, Any]:
    catalog = copy.deepcopy(VALID_CATALOG)
    mutate(catalog)
    return catalog


@pytest.mark.parametrize(
    "mutate",
    [
        lambda c: c.pop("schema_versions"),
        lambda c: c["schema_versions"].pop("collection"),
        lambda c: c.update(revision="12f2bbf8e83ca0fb22e95d31efa463d320458758"),
        lambda c: c["recipes"][0].pop("path"),
        lambda c: c["recipes"][0].pop("sha256"),
        lambda c: c["recipes"][0].update(sha256="A" * 64),
        lambda c: c["recipes"][0].update(sha256="0" * 63),
        lambda c: c["recipes"][0].update(path="recipes/sample-recipe/recipe.json"),
        lambda c: c["recipes"][0].update(prompt="Do the thing."),
        lambda c: c["recipes"][0].update(verified_by=["It works."]),
        lambda c: c["recipes"][0].update(agent_guidance={"instructions": "Go."}),
        lambda c: c["recipes"][0].update(canonical_url="https://example.com"),
        lambda c: c["recipes"][0]["works_with"].update(platforms=["duckdb"]),
        lambda c: c["collections"][0].pop("website_visible"),
    ],
    ids=[
        "no_schema_versions",
        "partial_schema_versions",
        "hand_revision",
        "entry_without_path",
        "entry_without_sha256",
        "uppercase_sha256",
        "short_sha256",
        "json_path",
        "prompt_copy",
        "verified_by_copy",
        "agent_guidance_copy",
        "canonical_url",
        "legacy_duckdb",
        "collection_without_visibility",
    ],
)
def test_catalog_rejects_wrong_control(mutate):
    assert errors(CATALOG, catalog_with(mutate))
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `.venv/bin/python -m pytest tests/test_collection_and_catalog_schemas.py -q`
Expected: FAIL at collection time with `FileNotFoundError` for `schema/catalog.schema.json`.

- [ ] **Step 3: Rewrite `schema/collection.schema.json`**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/accelerate-data/vibedata-cookbooks/schema/collection.schema.json",
  "version": 1,
  "title": "VibeData Cookbook Collection",
  "description": "collections/<id>.json: a non-executable discovery view over Recipes.",
  "type": "object",
  "additionalProperties": false,
  "required": ["id", "title", "kind", "description"],
  "$defs": {
    "id": { "type": "string", "pattern": "^[a-z0-9]+(?:-[a-z0-9]+)*$", "maxLength": 64 },
    "line": { "type": "string", "pattern": "^[^\\r\\n]*\\S[^\\r\\n]*$" },
    "token": { "type": "string", "pattern": "^[a-z0-9]+(?:[_-][a-z0-9]+)*$", "maxLength": 64 },
    "platform": { "enum": ["duckdb_local", "motherduck", "fabric_lakehouse", "fabric_warehouse", "redshift"] }
  },
  "properties": {
    "id": { "$ref": "#/$defs/id" },
    "title": { "$ref": "#/$defs/line", "maxLength": 120 },
    "description": { "$ref": "#/$defs/line", "maxLength": 400 },
    "kind": { "enum": ["function", "industry", "platform", "curated", "problem-area"] },
    "members": { "type": "array", "maxItems": 500, "uniqueItems": true, "items": { "$ref": "#/$defs/id" } },
    "selector": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "function": { "type": "array", "minItems": 1, "uniqueItems": true, "items": { "$ref": "#/$defs/token" } },
        "industry": { "type": "array", "minItems": 1, "uniqueItems": true, "items": { "$ref": "#/$defs/token" } },
        "platforms_any": { "type": "array", "minItems": 1, "uniqueItems": true, "items": { "$ref": "#/$defs/platform" } },
        "job_category": {
          "type": "array",
          "minItems": 1,
          "uniqueItems": true,
          "items": { "enum": ["get-running", "re-engineer", "build", "prove", "explain", "cross-platform"] }
        }
      }
    },
    "subfilters": {
      "type": "array",
      "maxItems": 20,
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["id", "title"],
        "properties": {
          "id": { "$ref": "#/$defs/id" },
          "title": { "$ref": "#/$defs/line", "maxLength": 60 },
          "platforms_any": { "type": "array", "minItems": 1, "uniqueItems": true, "items": { "$ref": "#/$defs/platform" } }
        }
      }
    }
  },
  "anyOf": [{ "required": ["members"] }, { "required": ["selector"] }]
}
```

- [ ] **Step 4: Generate `schema/catalog.schema.json` from the two source schemas**

This one-off composition guarantees the copies are exact; the mirror tests keep them exact afterwards.

```bash
.venv/bin/python - <<'EOF'
import json
from pathlib import Path

recipe = json.loads(Path("schema/recipe.schema.json").read_text(encoding="utf-8"))
collection = json.loads(Path("schema/collection.schema.json").read_text(encoding="utf-8"))
recipe_entry = {
    "type": "object",
    "additionalProperties": False,
    "required": recipe["required"] + ["path", "sha256"],
    "properties": {
        **recipe["properties"],
        "path": {"type": "string", "pattern": "^recipes/[a-z0-9]+(?:-[a-z0-9]+)*/recipe\\.md$"},
        "sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
    },
    "allOf": recipe["allOf"],
}
collection_entry = {
    "type": "object",
    "additionalProperties": False,
    "required": collection["required"] + ["resolved_members", "supported_or_proven_count", "website_publication_threshold", "website_visible"],
    "properties": {
        **collection["properties"],
        "resolved_members": {"type": "array", "uniqueItems": True, "items": {"$ref": "#/$defs/id"}},
        "supported_or_proven_count": {"type": "integer", "minimum": 0},
        "website_publication_threshold": {"type": "integer", "minimum": 1},
        "website_visible": {"type": "boolean"},
    },
    "anyOf": collection["anyOf"],
}
version = {"type": "integer", "minimum": 1}
catalog = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://github.com/accelerate-data/vibedata-cookbooks/schema/catalog.schema.json",
    "version": 1,
    "title": "VibeData Cookbook catalog",
    "description": "catalog.json, generated by scripts/build_catalog.py. Metadata only: no prompt, verified_by or agent_guidance. recipe_entry and collection_entry copy recipe.schema.json and collection.schema.json exactly.",
    "type": "object",
    "additionalProperties": False,
    "required": ["source", "schema_versions", "recipes", "collections"],
    "$defs": {**recipe["$defs"], "recipe_entry": recipe_entry, "collection_entry": collection_entry},
    "properties": {
        "source": {"type": "string", "pattern": "^https://"},
        "schema_versions": {
            "type": "object",
            "additionalProperties": False,
            "required": ["recipe", "catalog", "collection"],
            "properties": {"recipe": version, "catalog": version, "collection": version},
        },
        "recipes": {"type": "array", "items": {"$ref": "#/$defs/recipe_entry"}},
        "collections": {"type": "array", "items": {"$ref": "#/$defs/collection_entry"}},
    },
}
Path("schema/catalog.schema.json").write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
EOF
```

- [ ] **Step 5: Run the tests to verify they pass**

Run: `.venv/bin/python -m pytest -q`
Expected: PASS (both schema test modules).

- [ ] **Step 6: Commit**

```bash
git add schema/collection.schema.json schema/catalog.schema.json tests/test_collection_and_catalog_schemas.py
git commit -m "feat(schema): version 1 collection and catalog schemas with Studio platform values

Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>"
```

---

### Task 3: Frontmatter split and strict YAML load

**Files:**
- Create: `scripts/recipe_format.py`, `tests/test_frontmatter.py`

**Interfaces:**
- Consumes: `samples.VALID_RECIPE`, `samples.VALID_FRONTMATTER`, `samples.VALID_BODY`, `samples.VALID_META`.
- Produces: `recipe_format.CookbookError(Exception)`, `recipe_format.split_frontmatter(text: str) -> tuple[str, str]` (frontmatter YAML text, body text), `recipe_format.load_frontmatter(yaml_text: str) -> dict[str, Any]`.

- [ ] **Step 1: Write the failing tests**

`tests/test_frontmatter.py`:

```python
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
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `.venv/bin/python -m pytest tests/test_frontmatter.py -q`
Expected: FAIL with `ModuleNotFoundError: No module named 'recipe_format'`.

- [ ] **Step 3: Create `scripts/recipe_format.py`**

```python
"""Parse and check the Recipe file format: frontmatter, body sections and markup.

The rules themselves are data in schema/recipe.schema.json (x-body); this module
applies them. Every violation raises CookbookError with a message naming the rule.
"""

from __future__ import annotations

from typing import Any

import yaml


class CookbookError(Exception):
    """A cookbook contract violation."""


def split_frontmatter(text: str) -> tuple[str, str]:
    """Return (frontmatter YAML text, body text) for a recipe.md file."""
    if not text.startswith("---\n"):
        raise CookbookError("file must start with a '---' frontmatter line")
    end = text.find("\n---\n", 3)
    if end == -1:
        raise CookbookError("frontmatter has no closing '---' line")
    return text[4 : end + 1], text[end + 5 :]


class _StrictLoader(yaml.SafeLoader):
    """SafeLoader that rejects duplicate and non-string mapping keys."""


def _construct_mapping(loader: _StrictLoader, node: yaml.MappingNode) -> dict[str, Any]:
    mapping: dict[str, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=True)
        if not isinstance(key, str):
            raise CookbookError(f"frontmatter key {key!r} must be a string")
        if key in mapping:
            raise CookbookError(f"duplicate frontmatter key {key!r}")
        mapping[key] = loader.construct_object(value_node, deep=True)
    return mapping


_StrictLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping)

_JSON_SCALARS = (str, bool, int, float, type(None))


def _require_json_types(value: Any, label: str) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            _require_json_types(item, f"{label}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _require_json_types(item, f"{label}[{index}]")
    elif not isinstance(value, _JSON_SCALARS):
        raise CookbookError(f"frontmatter {label} is a {type(value).__name__}; quote it as a string")


def load_frontmatter(yaml_text: str) -> dict[str, Any]:
    """Load frontmatter YAML into plain JSON-compatible values."""
    try:
        value = yaml.load(yaml_text, Loader=_StrictLoader)  # noqa: S506 - _StrictLoader extends SafeLoader
    except yaml.YAMLError as exc:
        raise CookbookError(f"frontmatter is not valid YAML: {exc}") from exc
    if not isinstance(value, dict):
        raise CookbookError("frontmatter must be a YAML mapping")
    for key, item in value.items():
        _require_json_types(item, key)
    return value
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `.venv/bin/python -m pytest tests/test_frontmatter.py -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/recipe_format.py tests/test_frontmatter.py
git commit -m "feat(format): split recipe.md frontmatter and load it with a strict YAML loader

Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>"
```

---

### Task 4: Body parser with the closed heading set

**Files:**
- Modify: `scripts/recipe_format.py` (append)
- Create: `tests/test_body.py`

**Interfaces:**
- Consumes: `recipe.schema.json` `x-body` (`sections[]` with `heading`, `kind` in `paragraph` / `bullets` / `container`, `field`, `max_chars`, `min_items`, `max_items`, `forbid`).
- Produces: `recipe_format.parse_body(body: str, spec: dict[str, Any]) -> dict[str, Any]`, returning `{"prompt": str, "verified_by": [str], "agent_guidance": {"instructions": str, "compose": [str], "ask_first": [str], "guardrails": [str]}}`.

- [ ] **Step 1: Write the failing tests**

`tests/test_body.py`:

```python
"""parse_body: the valid sample, the caps at their limit, and each wrong control."""

from __future__ import annotations

import re

import pytest

from recipe_format import CookbookError, parse_body
from samples import VALID_BODY, VALID_BODY_FIELDS, load_schema

SPEC = load_schema("recipe")["x-body"]
PROMPT = VALID_BODY_FIELDS["prompt"]


def test_valid_body_parses_to_fields():
    assert parse_body(VALID_BODY, SPEC) == VALID_BODY_FIELDS


def test_prompt_at_cap_passes():
    assert parse_body(VALID_BODY.replace(PROMPT, "x" * 1200), SPEC)["prompt"] == "x" * 1200


def test_twelve_verified_by_bullets_pass():
    body = VALID_BODY.replace("- The model builds in the sandbox.\n", "- Condition.\n" * 11)
    assert len(parse_body(body, SPEC)["verified_by"]) == 12


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
}


@pytest.mark.parametrize(("body", "fragment"), list(REJECTIONS.values()), ids=list(REJECTIONS))
def test_rejects_wrong_control(body, fragment):
    with pytest.raises(CookbookError, match=re.escape(fragment)):
        parse_body(body, SPEC)
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `.venv/bin/python -m pytest tests/test_body.py -q`
Expected: FAIL with `ImportError: cannot import name 'parse_body'`.

- [ ] **Step 3: Append the parser to `scripts/recipe_format.py`**

Add `import re` to the imports at the top (after `from typing import Any`), then append:

```python
_NOT_A_PARAGRAPH = re.compile(r"^(?:[-*+]\s|\d+[.)]\s|>|\|)")


def _check_cap(heading: str, text: str, cap: int) -> None:
    if len(text) > cap:
        raise CookbookError(f"{heading}: {len(text)} characters exceeds the {cap}-character cap")


def _section_value(section: dict[str, Any], content: list[str]) -> Any:
    heading = section["heading"]
    kind = section["kind"]
    if kind == "container":
        if content:
            raise CookbookError(f"{heading}: must hold only its subsections")
        return None
    if kind == "paragraph":
        if len(content) != 1:
            raise CookbookError(f"{heading}: must be exactly one paragraph on one line")
        text = content[0]
        if _NOT_A_PARAGRAPH.match(text):
            raise CookbookError(f"{heading}: must be a paragraph, not a list, quote or table")
        for token in section.get("forbid", []):
            if token in text:
                raise CookbookError(f"{heading}: must not contain {token!r}")
        _check_cap(heading, text, section["max_chars"])
        return text
    if kind == "bullets":
        items: list[str] = []
        for line in content:
            if not line.startswith("- ") or len(line) < 3:
                raise CookbookError(f"{heading}: every line must be a '- ' bullet, with no blank lines between bullets")
            item = line[2:]
            if item != item.strip():
                raise CookbookError(f"{heading}: bullet text must have no leading or trailing whitespace")
            items.append(item)
        low, high = section["min_items"], section["max_items"]
        if not low <= len(items) <= high:
            raise CookbookError(f"{heading}: needs between {low} and {high} bullets; found {len(items)}")
        for item in items:
            _check_cap(heading, item, section["max_chars"])
        return items
    raise CookbookError(f"{heading}: unknown section kind {kind!r}")


def _assign(result: dict[str, Any], field: str, value: Any) -> None:
    *parents, leaf = field.split(".")
    target = result
    for parent in parents:
        target = target.setdefault(parent, {})
    target[leaf] = value


def parse_body(body: str, spec: dict[str, Any]) -> dict[str, Any]:
    """Parse a recipe.md body into its fields, enforcing the x-body section rules."""
    lines = body.split("\n")
    for number, line in enumerate(lines, start=1):
        if line != line.strip():
            raise CookbookError(f"body line {number}: no leading or trailing whitespace is allowed")
    sections = spec["sections"]
    expected = [section["heading"] for section in sections]
    positions = [index for index, line in enumerate(lines) if line.startswith("#")]
    found = [lines[index] for index in positions]
    if found != expected:
        raise CookbookError(f"body headings must be exactly {expected}, in order; found {found}")
    if any(lines[: positions[0]]):
        raise CookbookError(f"body has text before {expected[0]!r}")
    result: dict[str, Any] = {}
    ends = positions[1:] + [len(lines)]
    for section, start, end in zip(sections, positions, ends):
        content = lines[start + 1 : end]
        while content and content[0] == "":
            content.pop(0)
        while content and content[-1] == "":
            content.pop()
        value = _section_value(section, content)
        if "field" in section:
            _assign(result, section["field"], value)
    return result
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `.venv/bin/python -m pytest tests/test_body.py tests/test_frontmatter.py -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/recipe_format.py tests/test_body.py
git commit -m "feat(format): parse the Recipe body against the closed heading set

Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>"
```

---

### Task 5: Markup check

**Files:**
- Modify: `scripts/recipe_format.py` (append)
- Create: `tests/test_markup.py`

**Interfaces:**
- Consumes: `recipe.schema.json` `x-body.markup`.
- Produces: `recipe_format.check_markup(text: str, markup: dict[str, Any], label: str) -> None` (raises `CookbookError`).

- [ ] **Step 1: Write the failing tests**

`tests/test_markup.py`:

```python
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
        "zero​width",
        "bidi‮flip",
        "bell\x07",
        "carriage\rreturn",
        "﻿bom",
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
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `.venv/bin/python -m pytest tests/test_markup.py -q`
Expected: FAIL with `ImportError: cannot import name 'check_markup'`.

- [ ] **Step 3: Append `check_markup` to `scripts/recipe_format.py`**

```python
def check_markup(text: str, markup: dict[str, Any], label: str) -> None:
    """Reject markup that could escape its section; allow <lower_snake_case> placeholders."""
    if re.search(markup["forbidden_chars_pattern"], text):
        raise CookbookError(f"{label}: contains a control, zero-width, bidirectional or byte-order character")
    for token in markup["forbidden_substrings"]:
        if token in text:
            raise CookbookError(f"{label}: contains forbidden markup {token!r}")
    if re.search(markup["entity_pattern"], text):
        raise CookbookError(f"{label}: contains an HTML entity")
    placeholder = re.compile(markup["placeholder_pattern"])
    denied = set(markup["denied_placeholder_names"])
    for opening in re.finditer("<", text):
        match = placeholder.match(text, opening.start())
        if match is None:
            raise CookbookError(f"{label}: every '<' must open a lower_snake_case placeholder such as <model_name>")
        name = match.group(0)[1:-1]
        if name in denied:
            raise CookbookError(f"{label}: <{name}> is an HTML or tool-call tag, not a placeholder")
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `.venv/bin/python -m pytest -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/recipe_format.py tests/test_markup.py
git commit -m "feat(format): reject markup that could escape a Recipe section

Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>"
```

---

### Task 6: Convert `dbt-full-refresh-to-incremental` to `recipe.md`

The JSON file stays until Task 7 removes it with the old build script; the old build ignores `recipe.md`.

**Files:**
- Create: `recipes/dbt-full-refresh-to-incremental/recipe.md`, `tests/fixtures/legacy-dbt-full-refresh-to-incremental.json`, `tests/test_roundtrip.py`

**Interfaces:**
- Consumes: `split_frontmatter`, `load_frontmatter`, `parse_body`, `check_markup`, `samples.load_schema`, `samples.REPO_ROOT`.

- [ ] **Step 1: Freeze the legacy Recipe as a fixture**

Run: `mkdir -p tests/fixtures && cp recipes/dbt-full-refresh-to-incremental/recipe.json tests/fixtures/legacy-dbt-full-refresh-to-incremental.json`
Then: `git diff --no-index --stat tests/fixtures/legacy-dbt-full-refresh-to-incremental.json recipes/dbt-full-refresh-to-incremental/recipe.json`
Expected: no output (identical).

- [ ] **Step 2: Write the failing round-trip test**

`tests/test_roundtrip.py`:

```python
"""The converted Recipe keeps the published prompt, acceptance and guidance text exactly."""

from __future__ import annotations

import copy
import json

from jsonschema import Draft202012Validator

from recipe_format import check_markup, load_frontmatter, parse_body, split_frontmatter
from samples import REPO_ROOT, load_schema

SCHEMA = load_schema("recipe")
RECIPE = REPO_ROOT / "recipes/dbt-full-refresh-to-incremental/recipe.md"
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
```

- [ ] **Step 3: Run the test to verify it fails**

Run: `.venv/bin/python -m pytest tests/test_roundtrip.py -q`
Expected: FAIL with `FileNotFoundError` for `recipes/dbt-full-refresh-to-incremental/recipe.md`.

- [ ] **Step 4: Create `recipes/dbt-full-refresh-to-incremental/recipe.md`**

```markdown
---
id: dbt-full-refresh-to-incremental
title: Convert a full-refresh dbt model to incremental and show the runtime delta
trigger:
  - A dbt model is correct but a full refresh is too slow or too expensive to run routinely.
  - A full-refresh model needs to become incremental without changing its required consumer-visible output.
description: Convert an existing full-refresh dbt model to an incremental implementation while preserving its required semantics, handling agreed late-arriving data correctly, and recording the before-and-after runtime.
pitch: Make a slow full-refresh dbt model incremental and prove both the output parity and the runtime saving.
job_category: re-engineer
area: transformation
readiness: supported
domain_objects:
  - dbt_model
works_with:
  platforms:
    - duckdb_local
    - motherduck
    - fabric_lakehouse
    - fabric_warehouse
  tools:
    - dbt
evidence:
  features:
    - profiling-source-data
    - generating-dbt-model
    - running-dbt-in-sandbox
    - validating-against-baseline
    - dbt-unit-testing
  evals: []
---

## Prompt

Convert the existing full-refresh dbt model to an incremental model. Preserve the required consumer-visible output and downstream contract. Determine and implement the appropriate incremental strategy from the model and source evidence, verify the unique-key and late-arriving-data behaviour, and record the runtime change against the current full-refresh baseline.

## Verified by

- Incremental output matches the approved full-refresh baseline on the agreed comparison slice.
- A repeated incremental run produces no duplicate unique keys or unintended row changes.
- The agreed late-arriving-data case updates exactly the expected records.
- The before-and-after runtime is recorded from observed executions.

## Agent guidance

### Instructions

Inspect the existing model, dependencies, source behaviour, and current full-refresh result before changing materialization. Use evidence to choose the incremental strategy and key. Implement the smallest change that preserves the model's required semantics. Run the old and new paths in the appropriate isolated environment and collect actual comparison and runtime evidence before declaring the Recipe complete.

### Compose

- profiling-source-data
- generating-dbt-model
- running-dbt-in-sandbox
- validating-against-baseline
- dbt-unit-testing

### Ask first

- Ask for the intended late-arriving-data policy only if it cannot be inferred from approved project requirements or existing model behaviour.
- Ask for the intended business key only if no defensible unique key can be established from repository and data evidence.

### Guardrails

- Do not invent a unique key merely to make the incremental materialization compile.
- Do not change consumer-visible model semantics merely to make incremental processing easier.
- Do not treat predicted performance as evidence; record observed runtime from actual executions.
```

The file ends with a single `\n` after the last guardrail. The Compose bullets carry no backticks, because the legacy `compose` values have none.

- [ ] **Step 5: Run the tests to verify they pass**

Run: `.venv/bin/python -m pytest -q`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add recipes/dbt-full-refresh-to-incremental/recipe.md tests/fixtures/legacy-dbt-full-refresh-to-incremental.json tests/test_roundtrip.py
git commit -m "feat(recipes): convert dbt-full-refresh-to-incremental to recipe.md with a round-trip test

Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>"
```

---

### Task 7: Rewrite `build_catalog.py` for a metadata-only catalog

**Files:**
- Modify: `scripts/build_catalog.py` (full rewrite), `catalog.json` (regenerated)
- Delete: `recipes/dbt-full-refresh-to-incremental/recipe.json`, `recipes/dbt-full-refresh-to-incremental/README.md`
- Create: `tests/test_build_catalog.py`

**Interfaces:**
- Consumes: everything in `recipe_format`; the three schemas; `samples.make_cookbook`, `samples.write_recipe`, `samples.VALID_RECIPE`, `samples.VALID_META`; the `cookbook` fixture.
- Produces: `build_catalog.build_catalog(root: Path = ROOT) -> tuple[dict[str, Any], str]` (catalog object, serialized text); `build_catalog.main(argv: list[str] | None = None, root: Path = ROOT) -> int` (0 on success, 1 on any violation or a stale catalog in `--check`); `build_catalog.Recipe` dataclass (`meta`, `body`, `path`, `sha256`).

- [ ] **Step 1: Write the failing tests**

`tests/test_build_catalog.py`:

```python
"""build_catalog: metadata-only, sorted, byte-stable output; --check; each rejection rule."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from build_catalog import build_catalog, main
from recipe_format import CookbookError
from samples import REPO_ROOT, VALID_META, VALID_RECIPE, write_recipe

COLLECTION = {"id": "sample", "title": "Sample", "kind": "curated", "description": "A sample collection."}
RECIPE_REL = "recipes/sample-recipe/recipe.md"


def test_valid_cookbook_builds_a_metadata_only_catalog(cookbook):
    catalog, _ = build_catalog(cookbook)
    assert set(catalog) == {"source", "schema_versions", "recipes", "collections"}
    assert catalog["source"] == "https://github.com/accelerate-data/vibedata-cookbooks"
    assert catalog["schema_versions"] == {"recipe": 1, "catalog": 1, "collection": 1}
    (entry,) = catalog["recipes"]
    assert entry == {**VALID_META, "path": RECIPE_REL, "sha256": hashlib.sha256((cookbook / RECIPE_REL).read_bytes()).hexdigest()}


def test_catalog_is_sorted_and_byte_stable(cookbook):
    write_recipe(cookbook, "another-recipe", VALID_RECIPE.replace("id: sample-recipe", "id: another-recipe"))
    first = build_catalog(cookbook)[1]
    assert first == build_catalog(cookbook)[1]
    assert [entry["id"] for entry in json.loads(first)["recipes"]] == ["another-recipe", "sample-recipe"]
    assert first.endswith("}\n")


def test_selector_collection_resolves_by_platform(cookbook):
    selector = {**COLLECTION, "id": "local", "kind": "platform", "selector": {"platforms_any": ["duckdb_local"]}}
    (cookbook / "collections/local.json").write_text(json.dumps(selector), encoding="utf-8")
    catalog, _ = build_catalog(cookbook)
    (collection,) = catalog["collections"]
    assert collection["resolved_members"] == ["sample-recipe"]
    assert collection["supported_or_proven_count"] == 1
    assert collection["website_publication_threshold"] == 1
    assert collection["website_visible"] is True


def test_check_mode_detects_a_stale_catalog(cookbook, capsys):
    assert main(["--check"], root=cookbook) == 1
    assert main([], root=cookbook) == 0
    assert main(["--check"], root=cookbook) == 0
    path = cookbook / RECIPE_REL
    path.write_bytes(VALID_RECIPE.replace("prove its output.", "prove its output twice.").encode("utf-8"))
    assert main(["--check"], root=cookbook) == 1
    assert "stale" in capsys.readouterr().err


def test_dotfiles_are_ignored(cookbook):
    (cookbook / "recipes/.DS_Store").write_bytes(b"x")
    (cookbook / "recipes/sample-recipe/.DS_Store").write_bytes(b"x")
    assert build_catalog(cookbook)[0]["recipes"]


def test_repository_catalog_is_fresh():
    assert main(["--check"], root=REPO_ROOT) == 0


def replace_in_recipe(old: str, new: str):
    def mutate(root: Path) -> None:
        path = root / RECIPE_REL
        text = path.read_text(encoding="utf-8")
        assert old in text
        path.write_bytes(text.replace(old, new).encode("utf-8"))

    return mutate


def write_file(relpath: str, content: bytes | str):
    def mutate(root: Path) -> None:
        path = root / relpath
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content if isinstance(content, bytes) else content.encode("utf-8"))

    return mutate


def drop_schema_version(root: Path) -> None:
    path = root / "schema/recipe.schema.json"
    schema = json.loads(path.read_text(encoding="utf-8"))
    del schema["version"]
    path.write_text(json.dumps(schema), encoding="utf-8")


REJECTIONS = {
    "legacy_recipe_json": (write_file("recipes/sample-recipe/recipe.json", "{}"), "must contain only recipe.md"),
    "generated_readme": (write_file("recipes/sample-recipe/README.md", "# x\n"), "must contain only recipe.md"),
    "stray_file": (write_file("recipes/notes.txt", "x"), "only Recipe directories"),
    "id_mismatch": (replace_in_recipe("id: sample-recipe", "id: other-recipe"), "must match directory name"),
    "missing_platforms": (replace_in_recipe("works_with:\n  platforms:\n    - duckdb_local\n", "works_with: {}\n"), "'platforms' is a required property"),
    "legacy_platform": (replace_in_recipe("- duckdb_local", "- duckdb"), "'duckdb' is not one of"),
    "proven_without_evals": (replace_in_recipe("readiness: supported", "readiness: proven"), "'evidence' is a required property"),
    "prompt_in_frontmatter": (replace_in_recipe("readiness: supported\n", "readiness: supported\nprompt: Do the thing.\n"), "'prompt' was unexpected"),
    "markup_in_frontmatter": (replace_in_recipe("area: transformation\n", "area: transformation\npitch: Build a <div> fast.\n"), "HTML or tool-call tag"),
    "trailing_newline_in_frontmatter": (replace_in_recipe("title: Build a sample model and prove its output", 'title: "Build a sample model\\n"'), "must be a single line"),
    "markup_in_body": (replace_in_recipe("Do not invent a key.", "Do not invent a </key>."), "forbidden markup"),
    "body_rule": (replace_in_recipe("## Verified by", "## Verified By"), "headings"),
    "no_trailing_newline": (write_file(RECIPE_REL, VALID_RECIPE.rstrip("\n")), "exactly one newline"),
    "double_trailing_newline": (write_file(RECIPE_REL, VALID_RECIPE + "\n"), "exactly one newline"),
    "not_utf8": (write_file(RECIPE_REL, b"---\nid: \xff\n---\n"), "not UTF-8"),
    "over_byte_cap": (write_file(RECIPE_REL, VALID_RECIPE.replace("Do not invent a key.", "Do not invent a key." + " x" * 9000)), "byte cap"),
    "unknown_related": (replace_in_recipe("readiness: supported\n", "readiness: supported\nrelated:\n  - missing-recipe\n"), "related names unknown Recipes"),
    "unknown_member": (write_file("collections/sample.json", json.dumps({**COLLECTION, "members": ["missing-recipe"]})), "members name unknown Recipes"),
    "legacy_platform_selector": (write_file("collections/sample.json", json.dumps({**COLLECTION, "selector": {"platforms_any": ["duckdb"]}})), "'duckdb' is not one of"),
    "collection_id_mismatch": (write_file("collections/sample.json", json.dumps({**COLLECTION, "id": "other", "members": ["sample-recipe"]})), "must match filename"),
    "collection_markup": (write_file("collections/sample.json", json.dumps({**COLLECTION, "description": "A <script> view.", "members": ["sample-recipe"]})), "HTML or tool-call tag"),
    "collection_not_json": (write_file("collections/sample.json", "{"), "not valid JSON"),
    "unversioned_schema": (drop_schema_version, "top-level 'version'"),
}


@pytest.mark.parametrize(("mutate", "fragment"), list(REJECTIONS.values()), ids=list(REJECTIONS))
def test_rejects_wrong_control(cookbook, mutate, fragment):
    mutate(cookbook)
    with pytest.raises(CookbookError, match=fragment):
        build_catalog(cookbook)


def test_main_reports_a_violation_and_exits_1(cookbook, capsys):
    write_file("recipes/sample-recipe/recipe.json", "{}")(cookbook)
    assert main([], root=cookbook) == 1
    assert "cookbook validation error" in capsys.readouterr().err
```

`match=` is a regular expression; every fragment above is chosen to contain no regex metacharacters other than `'` and `.`, which match themselves or any character.

- [ ] **Step 2: Run the tests to verify they fail**

Run: `.venv/bin/python -m pytest tests/test_build_catalog.py -q`
Expected: FAIL with `ImportError: cannot import name 'build_catalog' from 'build_catalog'`.

- [ ] **Step 3: Rewrite `scripts/build_catalog.py`**

```python
#!/usr/bin/env python3
"""Validate the cookbook and generate catalog.json from Recipe frontmatter.

Run `python3 scripts/build_catalog.py` to regenerate catalog.json, or pass
`--check` to fail when catalog.json differs from a fresh build. The contract
rules live in schema/*.json; this script applies them.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

from recipe_format import CookbookError, check_markup, load_frontmatter, parse_body, split_frontmatter

ROOT = Path(__file__).resolve().parents[1]
REPO_URL = "https://github.com/accelerate-data/vibedata-cookbooks"
SCHEMA_NAMES = ("recipe", "catalog", "collection")
RECIPE_FILE = "recipe.md"
COUNTED_READINESS = {"supported", "proven"}


@dataclass(frozen=True)
class Recipe:
    meta: dict[str, Any]
    body: dict[str, Any]
    path: str
    sha256: str


def load_schemas(root: Path) -> dict[str, dict[str, Any]]:
    schemas: dict[str, dict[str, Any]] = {}
    for name in SCHEMA_NAMES:
        rel = f"schema/{name}.schema.json"
        schema = json.loads((root / rel).read_text(encoding="utf-8"))
        version = schema.get("version")
        if type(version) is not int or version < 1:
            raise CookbookError(f"{rel}: top-level 'version' must be an integer >= 1")
        try:
            Draft202012Validator.check_schema(schema)
        except SchemaError as exc:
            raise CookbookError(f"{rel}: not a valid JSON Schema: {exc.message}") from exc
        schemas[name] = schema
    return schemas


def raise_first_schema_error(schema: dict[str, Any], instance: Any, label: str) -> None:
    errors = sorted(
        Draft202012Validator(schema).iter_errors(instance),
        key=lambda error: ([str(part) for part in error.absolute_path], error.message),
    )
    if errors:
        error = errors[0]
        where = "/".join(str(part) for part in error.absolute_path) or "(root)"
        raise CookbookError(f"{label}: {where}: {error.message}")


def walk_strings(value: Any, label: str) -> Iterator[tuple[str, str]]:
    if isinstance(value, str):
        yield label, value
    elif isinstance(value, dict):
        for key, item in value.items():
            yield from walk_strings(item, f"{label}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from walk_strings(item, f"{label}[{index}]")


def visible_entries(directory: Path) -> list[Path]:
    return sorted(path for path in directory.iterdir() if not path.name.startswith("."))


def load_recipe(root: Path, directory: Path, schema: dict[str, Any]) -> Recipe:
    rel_dir = directory.relative_to(root).as_posix()
    names = [path.name for path in visible_entries(directory)]
    if names != [RECIPE_FILE]:
        raise CookbookError(f"{rel_dir}: must contain only {RECIPE_FILE}; found {names}")
    path = directory / RECIPE_FILE
    rel = path.relative_to(root).as_posix()
    spec = schema["x-body"]
    raw = path.read_bytes()
    if len(raw) > spec["max_bytes"]:
        raise CookbookError(f"{rel}: {len(raw)} bytes exceeds the {spec['max_bytes']}-byte cap")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise CookbookError(f"{rel}: not UTF-8 ({exc.reason})") from exc
    if not text.endswith("\n") or text.endswith("\n\n"):
        raise CookbookError(f"{rel}: must end with exactly one newline")
    try:
        frontmatter, body_text = split_frontmatter(text)
        meta = load_frontmatter(frontmatter)
        for label, value in walk_strings(meta, "frontmatter"):
            if "\n" in value or "\r" in value:
                raise CookbookError(f"{label}: must be a single line")
            check_markup(value, spec["markup"], label)
        raise_first_schema_error(schema, meta, "frontmatter")
        check_markup(body_text, spec["markup"], "body")
        body = parse_body(body_text, spec)
    except CookbookError as exc:
        raise CookbookError(f"{rel}: {exc}") from exc
    if meta["id"] != directory.name:
        raise CookbookError(f"{rel}: id {meta['id']!r} must match directory name {directory.name!r}")
    return Recipe(meta=meta, body=body, path=rel, sha256=hashlib.sha256(raw).hexdigest())


def load_recipes(root: Path, schema: dict[str, Any]) -> list[Recipe]:
    entries = visible_entries(root / "recipes")
    stray = [path.name for path in entries if not path.is_dir()]
    if stray:
        raise CookbookError(f"recipes/: only Recipe directories are allowed; found {stray}")
    recipes = [load_recipe(root, directory, schema) for directory in entries]
    ids = {recipe.meta["id"] for recipe in recipes}
    for recipe in recipes:
        unknown = sorted(set(recipe.meta.get("related", [])) - ids)
        if unknown:
            raise CookbookError(f"{recipe.path}: related names unknown Recipes: {', '.join(unknown)}")
    return recipes


def matches(meta: dict[str, Any], selector: dict[str, Any]) -> bool:
    for key in ("function", "industry"):
        if key in selector and not set(meta.get(key, [])) & set(selector[key]):
            return False
    if "platforms_any" in selector and not set(meta["works_with"]["platforms"]) & set(selector["platforms_any"]):
        return False
    if "job_category" in selector and meta["job_category"] not in selector["job_category"]:
        return False
    return True


def load_collections(
    root: Path, schema: dict[str, Any], markup: dict[str, Any], recipes: list[Recipe]
) -> list[dict[str, Any]]:
    by_id = {recipe.meta["id"]: recipe.meta for recipe in recipes}
    collections: list[dict[str, Any]] = []
    for path in sorted((root / "collections").glob("*.json")):
        rel = path.relative_to(root).as_posix()
        try:
            collection = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise CookbookError(f"{rel}: not valid JSON: {exc}") from exc
        raise_first_schema_error(schema, collection, rel)
        for label, value in walk_strings(collection, rel):
            check_markup(value, markup, label)
        if collection["id"] != path.stem:
            raise CookbookError(f"{rel}: id {collection['id']!r} must match filename {path.stem!r}")
        unknown = sorted(set(collection.get("members", [])) - by_id.keys())
        if unknown:
            raise CookbookError(f"{rel}: members name unknown Recipes: {', '.join(unknown)}")
        members = set(collection.get("members", []))
        if "selector" in collection:
            members |= {recipe_id for recipe_id, meta in by_id.items() if matches(meta, collection["selector"])}
        resolved = sorted(members)
        count = sum(1 for recipe_id in resolved if by_id[recipe_id]["readiness"] in COUNTED_READINESS)
        threshold = 3 if collection["kind"] == "function" else 1
        collections.append(
            {
                **collection,
                "resolved_members": resolved,
                "supported_or_proven_count": count,
                "website_publication_threshold": threshold,
                "website_visible": count >= threshold,
            }
        )
    return collections


def build_catalog(root: Path = ROOT) -> tuple[dict[str, Any], str]:
    schemas = load_schemas(root)
    recipes = load_recipes(root, schemas["recipe"])
    collections = load_collections(root, schemas["collection"], schemas["recipe"]["x-body"]["markup"], recipes)
    catalog = {
        "source": REPO_URL,
        "schema_versions": {name: schemas[name]["version"] for name in SCHEMA_NAMES},
        "recipes": [
            {**recipe.meta, "path": recipe.path, "sha256": recipe.sha256}
            for recipe in sorted(recipes, key=lambda recipe: recipe.meta["id"])
        ],
        "collections": sorted(collections, key=lambda collection: collection["id"]),
    }
    raise_first_schema_error(schemas["catalog"], catalog, "catalog.json")
    return catalog, json.dumps(catalog, indent=2, ensure_ascii=False, sort_keys=True) + "\n"


def main(argv: list[str] | None = None, root: Path = ROOT) -> int:
    parser = argparse.ArgumentParser(description="Validate the cookbook and generate catalog.json.")
    parser.add_argument("--check", action="store_true", help="fail if catalog.json differs from a fresh build")
    args = parser.parse_args(argv)
    try:
        catalog, text = build_catalog(root)
    except CookbookError as exc:
        print(f"cookbook validation error: {exc}", file=sys.stderr)
        return 1
    path = root / "catalog.json"
    if args.check:
        current = path.read_bytes().decode("utf-8") if path.exists() else None
        if current != text:
            print("cookbook validation error: catalog.json is stale; run python3 scripts/build_catalog.py", file=sys.stderr)
            return 1
    else:
        path.write_bytes(text.encode("utf-8"))
    visible = sum(1 for collection in catalog["collections"] if collection["website_visible"])
    print(
        f"validated {len(catalog['recipes'])} recipe(s), {len(catalog['collections'])} collection(s); "
        f"{visible} collection(s) website-visible"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run the unit tests to verify they pass, except the repository check**

Run: `.venv/bin/python -m pytest tests/test_build_catalog.py -q`
Expected: every test passes except `test_repository_catalog_is_fresh`, which fails because `recipe.json` and `README.md` are still in the Recipe directory.

- [ ] **Step 5: Remove the legacy files and regenerate the catalog**

Run: `git rm -q recipes/dbt-full-refresh-to-incremental/recipe.json recipes/dbt-full-refresh-to-incremental/README.md && .venv/bin/python scripts/build_catalog.py`
Expected: `validated 1 recipe(s), 3 collection(s); 2 collection(s) website-visible`.

Then inspect: `git diff catalog.json`
Expected: `revision`, `prompt`, `verified_by`, `agent_guidance` and `canonical_url` are gone; `schema_versions`, `path`, `sha256` and `pitch` are present; `duckdb` reads `duckdb_local`.

- [ ] **Step 6: Run the full suite and the check**

Run: `.venv/bin/python -m pytest -q && .venv/bin/python scripts/build_catalog.py --check`
Expected: all tests PASS; the check prints the `validated ...` line and exits 0.

- [ ] **Step 7: Commit**

```bash
git add scripts/build_catalog.py tests/test_build_catalog.py catalog.json
git commit -m "feat(build): generate a metadata-only catalog with path and sha256 from recipe.md

Removes recipe.json and the generated per-Recipe README, and the hand-written revision.

Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>"
```

`git rm` in Step 5 already staged the two deletions.

---

### Task 8: Schema version-bump check

**Files:**
- Create: `scripts/check_schema_versions.py`, `tests/test_schema_versions.py`

**Interfaces:**
- Consumes: `samples.load_schema`.
- Produces: `check_schema_versions.breaking_changes(base: Any, head: Any, path: str = "#") -> list[str]`, `check_schema_versions.check_versions(root: Path, base_rev: str) -> list[str]` (error messages; empty means pass), `check_schema_versions.main(argv: list[str] | None = None, root: Path = ROOT) -> int`, `check_schema_versions.SCHEMA_FILES: tuple[str, ...]`.

- [ ] **Step 1: Write the failing tests**

`tests/test_schema_versions.py`:

```python
"""The breaking-change classifier and the version-bump check against a base commit."""

from __future__ import annotations

import copy
import json
import subprocess
from pathlib import Path
from typing import Any, Callable

import pytest

from check_schema_versions import SCHEMA_FILES, breaking_changes, check_versions
from samples import load_schema

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
```

The fixture disables commit signing locally so a global `commit.gpgsign` setting cannot break the temporary repository.

- [ ] **Step 2: Run the tests to verify they fail**

Run: `.venv/bin/python -m pytest tests/test_schema_versions.py -q`
Expected: FAIL with `ModuleNotFoundError: No module named 'check_schema_versions'`.

- [ ] **Step 3: Create `scripts/check_schema_versions.py`**

```python
#!/usr/bin/env python3
"""Fail when a schema changes incompatibly without raising its top-level version.

Usage: python3 scripts/check_schema_versions.py --base <git-rev>

Each schema/*.schema.json in the working tree is compared with the same file at
<git-rev> (CI passes the merge base). A breaking change needs version + 1; a
non-breaking change keeps the version. Any change this classifier cannot prove
is loosening counts as breaking.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_FILES = ("recipe.schema.json", "catalog.schema.json", "collection.schema.json")
MISSING = object()
ANNOTATIONS = {"title", "description", "$comment", "examples", "version"}
UPPER_BOUNDS = {"maxLength", "maxItems", "maximum", "maxProperties"}
LOWER_BOUNDS = {"minLength", "minItems", "minimum", "minProperties"}
SUBSCHEMA_MAPS = {"properties", "$defs"}
SUBSCHEMAS = {"items", "not", "if", "then", "else", "contains"}
SUBSCHEMA_LISTS = {"allOf", "anyOf", "oneOf", "prefixItems"}
BODY_UPPER = ("max_chars", "max_items")
MARKUP_LISTS = ("forbidden_substrings", "denied_placeholder_names")


def _markup_changes(old: dict[str, Any], new: dict[str, Any], where: str) -> list[str]:
    changes = []
    for key in MARKUP_LISTS:
        added = sorted(set(new.get(key, [])) - set(old.get(key, [])))
        if added:
            changes.append(f"{where}/{key}: added {added}")
    for key in sorted((set(old) | set(new)) - set(MARKUP_LISTS)):
        if old.get(key) != new.get(key):
            changes.append(f"{where}/{key}: changed")
    return changes


def body_changes(old: Any, new: Any, where: str) -> list[str]:
    if not isinstance(old, dict) or not isinstance(new, dict):
        return [f"{where}: added or removed"]
    changes: list[str] = []
    for key in sorted((set(old) | set(new)) - {"max_bytes", "sections", "markup"}):
        if old.get(key) != new.get(key):
            changes.append(f"{where}/{key}: changed")
    if new.get("max_bytes", 0) < old.get("max_bytes", 0):
        changes.append(f"{where}/max_bytes: lowered to {new.get('max_bytes')}")
    old_sections, new_sections = old.get("sections", []), new.get("sections", [])
    shape = lambda sections: [(s.get("heading"), s.get("kind"), s.get("field")) for s in sections]  # noqa: E731
    if shape(old_sections) != shape(new_sections):
        changes.append(f"{where}/sections: heading set, order, kind or field changed")
    else:
        for o, n in zip(old_sections, new_sections):
            label = f"{where}/sections/{o['heading']}"
            for key in BODY_UPPER:
                if key in n and (key not in o or n[key] < o[key]):
                    changes.append(f"{label}/{key}: lowered to {n[key]}")
            if "min_items" in n and ("min_items" not in o or n["min_items"] > o["min_items"]):
                changes.append(f"{label}/min_items: raised to {n['min_items']}")
            added = sorted(set(n.get("forbid", [])) - set(o.get("forbid", [])))
            if added:
                changes.append(f"{label}/forbid: added {added}")
            other = (set(o) | set(n)) - {"heading", "kind", "field", "min_items", "forbid", *BODY_UPPER}
            for key in sorted(other):
                if o.get(key) != n.get(key):
                    changes.append(f"{label}/{key}: changed")
    changes += _markup_changes(old.get("markup", {}), new.get("markup", {}), f"{where}/markup")
    return changes


def breaking_changes(base: Any, head: Any, path: str = "#") -> list[str]:
    """List the breaking differences from base to head; empty means compatible."""
    if not isinstance(base, dict) or not isinstance(head, dict):
        return [] if base == head else [f"{path}: changed"]
    changes: list[str] = []
    for key in sorted(set(base) | set(head)):
        where = f"{path}/{key}"
        old, new = base.get(key, MISSING), head.get(key, MISSING)
        if key in ANNOTATIONS or old == new:
            continue
        if key == "x-body":
            changes += body_changes(old, new, where)
        elif key in SUBSCHEMA_MAPS:
            old_map = {} if old is MISSING else old
            new_map = {} if new is MISSING else new
            for name in sorted(old_map):
                if name not in new_map:
                    changes.append(f"{where}/{name}: removed")
                else:
                    changes += breaking_changes(old_map[name], new_map[name], f"{where}/{name}")
        elif key == "required":
            added = sorted(set([] if new is MISSING else new) - set([] if old is MISSING else old))
            if added:
                changes.append(f"{where}: newly required {added}")
        elif key == "enum":
            if old is MISSING:
                changes.append(f"{where}: enum added")
            elif new is not MISSING:
                removed = [value for value in old if value not in new]
                if removed:
                    changes.append(f"{where}: values removed {removed}")
        elif key in UPPER_BOUNDS:
            if new is not MISSING and (old is MISSING or new < old):
                changes.append(f"{where}: lowered to {new}")
        elif key in LOWER_BOUNDS:
            if new is not MISSING and (old is MISSING or new > old):
                changes.append(f"{where}: raised to {new}")
        elif key == "additionalProperties":
            o = True if old is MISSING else old
            n = True if new is MISSING else new
            if n is True or o is False:
                continue
            if isinstance(o, dict) and isinstance(n, dict):
                changes += breaking_changes(o, n, where)
            else:
                changes.append(f"{where}: tightened")
        elif key == "uniqueItems":
            if new is True:
                changes.append(f"{where}: now true")
        elif key in SUBSCHEMAS and old is not MISSING and new is not MISSING:
            changes += breaking_changes(old, new, where)
        elif key in SUBSCHEMA_LISTS and isinstance(old, list) and isinstance(new, list) and len(old) == len(new):
            for index, (o, n) in enumerate(zip(old, new)):
                changes += breaking_changes(o, n, f"{where}/{index}")
        else:
            changes.append(f"{where}: changed")
    return changes


def _git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True)


def _is_version(value: Any) -> bool:
    return type(value) is int and value >= 1


def check_versions(root: Path, base_rev: str) -> list[str]:
    if _git(root, "rev-parse", "--verify", "--quiet", f"{base_rev}^{{commit}}").returncode != 0:
        return [f"base revision {base_rev!r} is not a commit"]
    errors: list[str] = []
    for name in SCHEMA_FILES:
        rel = f"schema/{name}"
        shown = _git(root, "show", f"{base_rev}:{rel}")
        base_text = shown.stdout if shown.returncode == 0 else None
        head_path = root / rel
        if not head_path.exists():
            if base_text is not None:
                errors.append(f"{rel}: removed; a published schema cannot be deleted")
            continue
        head = json.loads(head_path.read_text(encoding="utf-8"))
        head_version = head.get("version")
        if not _is_version(head_version):
            errors.append(f"{rel}: top-level 'version' must be an integer >= 1")
            continue
        if base_text is None:
            if head_version != 1:
                errors.append(f"{rel}: a new schema starts at version 1, not {head_version}")
            continue
        base = json.loads(base_text)
        base_version = base.get("version")
        if base_version is None:
            if head_version != 1:
                errors.append(f"{rel}: the first versioned schema is version 1, not {head_version}")
            continue
        breaking = breaking_changes(base, head)
        if breaking and head_version != base_version + 1:
            errors.append(
                f"{rel}: breaking change without a version bump to {base_version + 1} "
                f"(found {head_version}): " + "; ".join(breaking)
            )
        elif not breaking and head_version != base_version:
            errors.append(f"{rel}: version changed from {base_version} to {head_version} without a breaking change")
    return errors


def main(argv: list[str] | None = None, root: Path = ROOT) -> int:
    parser = argparse.ArgumentParser(description="Fail on a breaking schema change without a version bump.")
    parser.add_argument("--base", required=True, help="git revision to compare against, normally the merge base")
    args = parser.parse_args(argv)
    errors = check_versions(root, args.base)
    for error in errors:
        print(f"schema version error: {error}", file=sys.stderr)
    if not errors:
        print(f"schema versions consistent with {args.base}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `.venv/bin/python -m pytest tests/test_schema_versions.py -q`
Expected: PASS.

- [ ] **Step 5: Run the check against this branch's merge base**

Run: `.venv/bin/python scripts/check_schema_versions.py --base "$(git merge-base origin/main HEAD)"`
Expected: `schema versions consistent with <sha>` and exit 0. `origin/main`'s schemas carry no `version` and `catalog.schema.json` does not exist there, so each schema is accepted at version 1.

- [ ] **Step 6: Commit**

```bash
git add scripts/check_schema_versions.py tests/test_schema_versions.py
git commit -m "feat(ci): fail a breaking schema change that does not raise the schema version

Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>"
```

---

### Task 9: CI workflow

**Files:**
- Create: `.github/workflows/ci.yml`, `tests/test_ci_workflow.py`

**Interfaces:**
- Consumes: `requirements.txt`, `scripts/build_catalog.py --check`, `scripts/check_schema_versions.py --base`.

- [ ] **Step 1: Write the failing test**

`tests/test_ci_workflow.py`:

```python
"""The CI workflow runs every contract gate on pull requests and on pushes to main."""

from __future__ import annotations

import yaml

from samples import REPO_ROOT

WORKFLOW = REPO_ROOT / ".github/workflows/ci.yml"


def test_ci_runs_every_gate():
    workflow = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    triggers = workflow.get("on", workflow.get(True))  # YAML 1.1 reads a bare `on` key as True
    assert "pull_request" in triggers
    assert triggers["push"]["branches"] == ["main"]
    steps = workflow["jobs"]["contract"]["steps"]
    runs = "\n".join(step.get("run", "") for step in steps)
    for command in (
        "python -m pip install -r requirements.txt",
        "python -m pytest",
        "python scripts/build_catalog.py --check",
        "python scripts/check_schema_versions.py --base",
    ):
        assert command in runs
    checkout = next(step for step in steps if step.get("uses", "").startswith("actions/checkout@"))
    assert checkout["with"]["fetch-depth"] == 0
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `.venv/bin/python -m pytest tests/test_ci_workflow.py -q`
Expected: FAIL with `FileNotFoundError` for `.github/workflows/ci.yml`.

- [ ] **Step 3: Create `.github/workflows/ci.yml`**

```yaml
name: CI

on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  contract:
    name: Cookbook contract
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
      - name: Install pinned dependencies
        run: python -m pip install -r requirements.txt
      - name: Unit tests
        run: python -m pytest -q
      - name: Catalog is valid and fresh
        run: python scripts/build_catalog.py --check
      - name: Schema changes carry a version bump
        env:
          EVENT_NAME: ${{ github.event_name }}
          PR_BASE_SHA: ${{ github.event.pull_request.base.sha }}
          PUSH_BEFORE_SHA: ${{ github.event.before }}
        run: |
          if [ "$EVENT_NAME" = "pull_request" ]; then
            base="$(git merge-base "$PR_BASE_SHA" HEAD)"
          else
            base="$PUSH_BEFORE_SHA"
          fi
          if [ -z "$base" ] || [ "$base" = "0000000000000000000000000000000000000000" ]; then
            echo "No base commit to compare against; skipping the version-bump check."
            exit 0
          fi
          python scripts/check_schema_versions.py --base "$base"
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `.venv/bin/python -m pytest -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add .github/workflows/ci.yml tests/test_ci_workflow.py
git commit -m "ci: run tests, the catalog check and the schema version check

Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>"
```

---

### Task 10: Recipe `api-to-bronze-incremental-contract`

**Files:**
- Create: `recipes/api-to-bronze-incremental-contract/recipe.md`, `tests/test_published_recipes.py`
- Modify: `catalog.json` (regenerated)

**Interfaces:**
- Produces: `tests/test_published_recipes.py` with an `EXPECTED` dict keyed by Recipe id; Tasks 11 and 12 add entries.

- [ ] **Step 1: Write the failing test**

`tests/test_published_recipes.py`:

```python
"""The published catalog holds exactly the expected Recipes with their agreed platforms and readiness."""

from __future__ import annotations

import json

import pytest

from samples import REPO_ROOT

ALL_PLATFORMS = ["duckdb_local", "motherduck", "fabric_lakehouse", "fabric_warehouse", "redshift"]

EXPECTED = {
    "dbt-full-refresh-to-incremental": {
        "readiness": "supported",
        "platforms": ["duckdb_local", "motherduck", "fabric_lakehouse", "fabric_warehouse"],
    },
    "api-to-bronze-incremental-contract": {"readiness": "supported", "platforms": ALL_PLATFORMS},
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
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `.venv/bin/python -m pytest tests/test_published_recipes.py -q`
Expected: FAIL: `test_catalog_holds_exactly_the_expected_recipes` reports the missing `api-to-bronze-incremental-contract`, and its parametrized case raises `KeyError`.

- [ ] **Step 3: Create `recipes/api-to-bronze-incremental-contract/recipe.md`**

Adapted from the GTM seed entry "Land a SaaS or REST API into bronze with an incremental cursor and a schema contract": the seed's multi-line prompt becomes one paragraph, `on <platform>` is dropped because the Intent supplies the platform, the `<evolve | freeze | discard_row>` choice loses its pipes, and the seed's Verify line becomes separate, checkable acceptance conditions.

```markdown
---
id: api-to-bronze-incremental-contract
title: Land a SaaS or REST API into bronze with an incremental cursor and a schema contract
trigger:
  - An API source has to load into bronze incrementally instead of reloading everything on every run.
  - A pipeline breaks whenever the source API adds or changes a field.
description: Build a dlt pipeline that lands a SaaS or REST API into bronze with cursor-based incremental loading and a schema contract that decides how new or changed columns are handled, with pytest coverage of both and a sandbox load that proves the landed row counts.
pitch: Land an API into bronze incrementally, with a schema contract that decides what happens when a field changes.
job_category: build
area: ingestion
readiness: supported
domain_objects:
  - dlt_pipeline
  - dlt_resource
  - bronze_table
works_with:
  platforms:
    - duckdb_local
    - motherduck
    - fabric_lakehouse
    - fabric_warehouse
    - redshift
  tools:
    - dlt
evidence:
  features:
    - discovering-source-schema
    - generating-dlt-pipeline
    - running-dlt-in-sandbox
    - dlt-unit-testing
    - ingestion-data-testing
  evals: []
---

## Prompt

Build a dlt pipeline that lands <source_name> into bronze. Load <resource_list> incrementally on the <cursor_field> cursor, starting from <initial_value>. Handle new columns with the <new_column_policy> schema contract (evolve, freeze or discard_row), and freeze type changes. Add pytest coverage for the cursor and the contract, run the pipeline in the sandbox, and report the landed row count for each resource.

## Verified by

- A sandbox load lands every requested resource in bronze, and the landed row count of each resource is reported.
- A second run loads only rows newer than the persisted cursor value.
- A fixture that adds a column is handled exactly as the agreed new-column policy states.
- A fixture that changes a column's type fails the schema contract test.
- The pytest suite covers the cursor and both contract cases, and it passes.
- The connector and dlt versions are pinned in the pipeline's requirements.

## Agent guidance

### Instructions

Confirm the source connection resolves and discover its resources before writing pipeline code. Settle the cursor field, write disposition and primary key of each resource from the request and the source's evidence, and record each choice. Build the pipeline on the vendored connector, cover the cursor and both contract cases in pytest, then run it in the sandbox twice and collect the row counts and the second-run evidence before declaring the Recipe complete.

### Compose

- discovering-source-schema
- generating-dlt-pipeline
- running-dlt-in-sandbox
- dlt-unit-testing
- ingestion-data-testing

### Ask first

- Ask for the write disposition of a resource (append, replace or merge) only if neither the request nor the source's evidence settles it.
- Ask for the primary key of a merge resource only if the source exposes no defensible one.
- Ask whether child resources are needed only if the source exposes them and the request does not say.

### Guardrails

- Pin the connector and dlt versions in the pipeline's requirements.
- Do not fall back silently from MotherDuck to local DuckDB.
- Do not report the contract as tested until a fixture with a changed type has turned its test red.
- Do not reload rows the persisted cursor has already passed.
```

- [ ] **Step 4: Regenerate the catalog and run the tests**

Run: `.venv/bin/python scripts/build_catalog.py && .venv/bin/python -m pytest -q`
Expected: `validated 2 recipe(s), 3 collection(s); 2 collection(s) website-visible`, then all tests PASS. `microsoft-fabric` now resolves both Recipes.

- [ ] **Step 5: Commit**

```bash
git add recipes/api-to-bronze-incremental-contract/recipe.md tests/test_published_recipes.py catalog.json
git commit -m "feat(recipes): add api-to-bronze-incremental-contract

Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>"
```

---

### Task 11: Recipe `fabric-data-pipeline-as-code`

**Files:**
- Create: `recipes/fabric-data-pipeline-as-code/recipe.md`
- Modify: `tests/test_published_recipes.py`, `catalog.json` (regenerated)

- [ ] **Step 1: Add the expectation (failing)**

In `tests/test_published_recipes.py`, add this entry to `EXPECTED` after the `api-to-bronze-incremental-contract` line:

```python
    "fabric-data-pipeline-as-code": {"readiness": "supported", "platforms": ["fabric_lakehouse", "fabric_warehouse"]},
```

Run: `.venv/bin/python -m pytest tests/test_published_recipes.py -q`
Expected: FAIL on the missing `fabric-data-pipeline-as-code`.

- [ ] **Step 2: Create `recipes/fabric-data-pipeline-as-code/recipe.md`**

Adapted from the seed entry "Author a Fabric Data Pipeline that sequences ingestion, dbt, and downstream refresh as committed code"; compose names the plugin's orchestration skills.

```markdown
---
id: fabric-data-pipeline-as-code
title: Author a Fabric Data Pipeline that sequences ingestion, dbt, and downstream refresh as committed code
trigger:
  - A Fabric Data Pipeline was built by clicking and lives only in the workspace.
  - Ingestion, the dbt build and a downstream refresh have to run in order on a schedule in Fabric.
description: Author a Fabric Data Pipeline and its schedule as committed code that runs ingestion, the dbt job and a downstream step in order, validate its dependency graph statically, run it once on demand, and document its schedule and dependency order.
pitch: Turn a clicked-together Fabric pipeline into committed code that runs ingestion, dbt and the downstream refresh in order.
job_category: build
area: orchestration
readiness: supported
domain_objects:
  - fabric_data_pipeline
  - dbt_job
  - schedule
works_with:
  platforms:
    - fabric_lakehouse
    - fabric_warehouse
  tools:
    - dlt
    - dbt
evidence:
  features:
    - generating-orchestration
    - evaluating-orchestration
    - running-orchestration-in-sandbox
    - documenting-orchestration
  evals: []
---

## Prompt

Author a Fabric Data Pipeline named <pipeline_name> that runs <ingestion_pipeline>, then the dbt job, then <downstream_step>, on a <cadence> schedule with <retry_policy>. Commit the pipeline and its schedule as code, validate its dependency graph, run it once on demand in the sandbox, and document the schedule and the dependency order.

## Verified by

- The pipeline definition and its schedule are committed to the repository as code.
- Every artifact the pipeline invokes exists in the repository.
- Static validation of the pipeline's dependency graph passes with no findings.
- An on-demand sandbox run of the pipeline completes, and its run evidence is recorded.
- The schedule, the retry policy and the step order are documented.

## Agent guidance

### Instructions

Inventory the ingestion pipeline, the dbt job and the downstream step the pipeline will invoke, and confirm each exists in the repository before referencing it. Generate the pipeline and its schedule as code, validate the dependency graph statically, run the pipeline once on demand in the sandbox, and document its schedule and dependency order before declaring the Recipe complete.

### Compose

- generating-orchestration
- evaluating-orchestration
- running-orchestration-in-sandbox
- documenting-orchestration

### Ask first

- Ask for the failure notification target only if no approved requirement or project convention names one.
- Ask whether a step is optional only if the request does not say how its failure affects the steps after it.

### Guardrails

- Do not reference an artifact the repository does not contain.
- Do not edit the pipeline by hand in the workspace; the committed definition is the only source.
- Do not treat static validation as proof that the pipeline runs; record an on-demand run.
```

- [ ] **Step 3: Regenerate the catalog and run the tests**

Run: `.venv/bin/python scripts/build_catalog.py && .venv/bin/python -m pytest -q`
Expected: `validated 3 recipe(s), 3 collection(s); 2 collection(s) website-visible`, then all tests PASS.

- [ ] **Step 4: Commit**

```bash
git add recipes/fabric-data-pipeline-as-code/recipe.md tests/test_published_recipes.py catalog.json
git commit -m "feat(recipes): add fabric-data-pipeline-as-code

Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>"
```

---

### Task 12: Recipe `motherduck-flight-scheduling`

**Files:**
- Create: `recipes/motherduck-flight-scheduling/recipe.md`
- Modify: `tests/test_published_recipes.py`, `catalog.json` (regenerated)

- [ ] **Step 1: Add the expectation (failing)**

In `tests/test_published_recipes.py`, add this entry to `EXPECTED` after the `fabric-data-pipeline-as-code` line:

```python
    "motherduck-flight-scheduling": {"readiness": "supported", "platforms": ["motherduck"]},
```

Run: `.venv/bin/python -m pytest tests/test_published_recipes.py -q`
Expected: FAIL on the missing `motherduck-flight-scheduling`.

- [ ] **Step 2: Create `recipes/motherduck-flight-scheduling/recipe.md`**

Renamed from the seed's `motherduck-duckdb-scheduling` and narrowed to MotherDuck: local DuckDB has no scheduling capability, and GitHub Actions is dropped because the plugin authors Flights, not workflow files. The seed marked it roadmap; the plugin's `generating-orchestration` and `running-orchestration-in-sandbox` skills now author and run `orchestration/<Name>.Flight/`, so it is `supported`.

```markdown
---
id: motherduck-flight-scheduling
title: Schedule a dlt load and a dbt build on MotherDuck as a committed MotherDuck Flight
trigger:
  - The MotherDuck load and build run from a cron job on someone's laptop.
  - A dlt load and a dbt build on MotherDuck have to run in order on a schedule without standing up an orchestrator.
description: Author a MotherDuck Flight as committed code that runs a dlt load and then a dbt build in order on a schedule, with every credential declared as a secret, and prove one on-demand run succeeded on the workload's own result as well as the Flight's status.
pitch: Replace the laptop cron with a committed MotherDuck Flight that loads and builds on a schedule.
job_category: build
area: orchestration
readiness: supported
domain_objects:
  - motherduck_flight
  - schedule
works_with:
  platforms:
    - motherduck
  tools:
    - dlt
    - dbt
evidence:
  features:
    - generating-orchestration
    - evaluating-orchestration
    - running-orchestration-in-sandbox
    - documenting-orchestration
  evals: []
---

## Prompt

Schedule <dlt_pipeline> and then the dbt build of <dbt_selector> to run every <cadence> on MotherDuck as a MotherDuck Flight named <flight_name>. Commit the Flight as code with every credential it reads declared as a secret, run it once on demand in the sandbox, and report its run status, its exit code and the workload's own result.

## Verified by

- The Flight is committed to the repository with its schedule, and no Flight id or credential value appears in the repository.
- The Flight passes static Flight validation with no findings.
- An on-demand sandbox run reaches a succeeded status with exit code 0.
- The run's own dlt and dbt results show that the load and the build both succeeded.
- The Flight name, version, run number, status and exit code are recorded as run evidence.

## Agent guidance

### Instructions

Confirm the dlt pipeline and the dbt selection the Flight will run exist in the repository before authoring it. Author the Flight from the canonical template and adapt it only through its configuration, declaring every credential as a secret and committing the Flight's name, never its generated id. Validate it statically, run it once on demand in the sandbox, and judge success on the workload's own result as well as the Flight's status before declaring the Recipe complete.

### Compose

- generating-orchestration
- evaluating-orchestration
- running-orchestration-in-sandbox
- documenting-orchestration

### Ask first

- Ask for the schedule cadence only if neither the request nor the approved requirements state one.
- Ask whether the dbt build should run when the load lands no new rows only if the approved requirements do not say.

### Guardrails

- Do not create, apply or schedule the Flight directly on the platform; the committed item is the only deploy path.
- Do not treat a succeeded Flight status alone as proof; a failed dbt graph can still report success.
- Do not offer this Recipe for local DuckDB, which has no scheduling capability.
```

- [ ] **Step 3: Regenerate the catalog and run the tests**

Run: `.venv/bin/python scripts/build_catalog.py && .venv/bin/python -m pytest -q`
Expected: `validated 4 recipe(s), 3 collection(s); 2 collection(s) website-visible`, then all tests PASS.

- [ ] **Step 4: Commit**

```bash
git add recipes/motherduck-flight-scheduling/recipe.md tests/test_published_recipes.py catalog.json
git commit -m "feat(recipes): add motherduck-flight-scheduling

Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>"
```

---

### Task 13: Contributor guide, Recipe template and README

**Files:**
- Create: `templates/recipe.md`, `CONTRIBUTING.md`, `tests/test_template.py`
- Modify: `README.md` (full rewrite)

**Interfaces:**
- Consumes: `split_frontmatter`, `load_frontmatter`, `parse_body`, `check_markup`, `samples.load_schema`, `samples.REPO_ROOT`.

- [ ] **Step 1: Write the failing test**

`tests/test_template.py`:

```python
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
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `.venv/bin/python -m pytest tests/test_template.py -q`
Expected: FAIL with `FileNotFoundError` for `templates/recipe.md`.

- [ ] **Step 3: Create `templates/recipe.md`**

```markdown
---
# Copy to recipes/<recipe_id>/recipe.md and replace every value. CONTRIBUTING.md describes each key.
id: <recipe_id>
title: <literal_deliverable_title>
trigger:
  - <situation_that_calls_for_this_recipe>
description: <one_line_outcome_and_scope>
pitch: <one_sentence_for_the_hero_card>
job_category: build  # get-running, re-engineer, build, prove, explain or cross-platform
area: transformation  # kebab-case, for example ingestion, transformation, orchestration
readiness: supported  # proven, supported or planned; proven needs at least one evidence.evals entry
domain_objects:
  - <domain_object>
works_with:
  platforms:  # one or more of duckdb_local, motherduck, fabric_lakehouse, fabric_warehouse, redshift
    - duckdb_local
  tools:
    - dbt
evidence:
  features:
    - <skill_name>
  evals: []
---

## Prompt

Replace this line with the task as one paragraph on one line, and mark each value the engineer adapts as a placeholder such as <model_name>.

## Verified by

- Replace with one independently checkable acceptance condition.
- Add one bullet per further condition.

## Agent guidance

### Instructions

Replace with one paragraph on how the agent should approach the work and what evidence it must collect before declaring the Recipe complete.

### Compose

- <skill_name>

### Ask first

- Ask for <decision> only if it cannot be inferred from approved requirements or repository evidence.

### Guardrails

- Do not <unsafe_shortcut>.
```

- [ ] **Step 4: Create `CONTRIBUTING.md`**

```markdown
# Contributing a Recipe

A Recipe is one requirement-sized data-engineering outcome a data engineer adopts into a Studio Intent. This guide covers what belongs here, the Recipe file, and the checks every change must pass. The contract itself is recorded in [ADR 0001](docs/adr/0001-cookbook-recipe-contract.md).

## Feature or Recipe

A candidate is a **Feature**, not a Recipe, when one direct operation or one skill contract is the whole job: testing a source connection, registering a source, adding one test, running a change in isolation, comparing a relation against a baseline, enforcing a contract, or explaining one number. Features are reached by asking for them, and listing one as a Recipe would suggest it needs a Recipe to work.

A candidate is a **Recipe** when it is one recognizable engineering requirement that composes several capabilities or needs real design or modelling judgment, and has its own acceptance behaviour. Every Recipe proves itself: its tests, sandbox runs and comparisons belong in its own `Verified by` section, never in a second Recipe.

## The shape of a Recipe

- **Title:** the literal deliverable, the thing the engineer ends up with, not a slogan.
- **Trigger:** one or more situations, written separately from the title, in which an engineer would reach for the Recipe.
- **Description and pitch:** the bounded outcome in one line, and an optional one-sentence pitch for hero cards.
- **Prompt:** the paste-and-adapt task. Values the engineer adapts are `<lower_snake_case>` placeholders. Never ask for context Studio already knows, such as the platform, the repository or the Domain.
- **Agent guidance:** instructions, composed skills, genuinely open questions and guardrails. The agent reads it; the invocation surface does not show it as the prompt.

## Adding a Recipe

1. Copy `templates/recipe.md` to `recipes/<id>/recipe.md`, where `<id>` is the Recipe's kebab-case id. The directory holds that one file.
2. Fill in the frontmatter and every body section.
3. Run the checks below and commit `recipe.md` together with the regenerated `catalog.json`.

## Frontmatter

Required keys: `id`, `title`, `trigger`, `description`, `job_category`, `area`, `readiness`, `works_with.platforms`. Optional keys: `pitch`, `function`, `industry`, `domain_objects`, `works_with.tools`, `qualifiers`, `related`, `evidence.features`, `evidence.evals`. Every string is one line. `schema/recipe.schema.json` holds the exact rules and length caps.

`works_with.platforms` uses Studio's own values: `duckdb_local`, `motherduck`, `fabric_lakehouse`, `fabric_warehouse`, `redshift`. There is no generic `fabric` value; a Recipe for both Fabric targets lists both.

`readiness` is `proven` only when a dedicated Recipe-level eval or journey proves the exact Recipe shape; name it in `evidence.evals`. `supported` means current capabilities can execute it end to end without such an eval. `planned` means at least one capability is missing today.

## Body

The body holds exactly these headings, in this order, and nothing else that starts with `#`:

| Heading | Content | Cap |
| --- | --- | --- |
| `## Prompt` | one paragraph on one line, no `\|` | 1200 characters |
| `## Verified by` | one acceptance condition per `- ` bullet | 1 to 12 bullets, 300 characters each |
| `## Agent guidance` | only the four subsections below | none |
| `### Instructions` | one paragraph on one line | 1500 characters |
| `### Compose` | one skill or Feature name per bullet; an advisory hint the cookbook does not check | 1 to 12 bullets, 80 characters each |
| `### Ask first` | one genuinely open question per bullet | 1 to 8 bullets, 300 characters each |
| `### Guardrails` | one Recipe-specific guardrail per bullet | 1 to 10 bullets, 300 characters each |

Bullets use `- ` only, never nested or indented, with no blank line inside a list. No line has leading or trailing whitespace. The whole file stays under 16384 bytes.

Nothing may escape its section: no HTML tags or comments, no HTML entities, no code fences, no control, zero-width or bidirectional characters. A `<` is allowed only to open a placeholder such as `<model_name>`, and a placeholder may not be an HTML element name or a tool-call word.

## Collections

A Collection in `collections/<id>.json` is a discovery view over Recipes: a `members` list of existing Recipe ids, a `selector` over Recipe metadata, or both. `schema/collection.schema.json` holds the rules.

## Checks

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -q
.venv/bin/python scripts/build_catalog.py
.venv/bin/python scripts/check_schema_versions.py --base "$(git merge-base origin/main HEAD)"
```

`build_catalog.py` validates everything and rewrites `catalog.json`; CI runs it with `--check` and fails when the committed catalog is stale.

## Changing a schema

Each schema carries a top-level integer `version`. Raise it by exactly one for a breaking change: removing or renaming a field, making a field required, narrowing an enum, tightening a cap or pattern, or changing the body headings. Adding an optional field, widening an enum or raising a cap is not breaking and keeps the version. `check_schema_versions.py` enforces this in CI against the merge base, and treats any change it cannot prove is loosening as breaking. `catalog.schema.json` copies the Recipe and Collection properties exactly, so a change to either schema is made in `catalog.schema.json` too; a test fails when they drift.
```

- [ ] **Step 5: Rewrite `README.md`**

````markdown
# VibeData Cookbooks

Public, canonical definitions for **materialized VibeData Recipes and Collections**.

A Recipe is one requirement-sized data-engineering outcome that a data engineer can adopt into an Intent. It contains the task specification, an observable acceptance contract, and guidance the VibeData agent reads when the Recipe is invoked.

## Source ownership

- **Linear Cookbook project**: canonical backlog and lifecycle for Recipe candidates: <https://linear.app/acceleratedata/project/cookbook-fb2483d9868a/overview>
- **This repository**: canonical definition of Recipes and Collections once they are materialized.

The VibeData website and Studio consume the materialized catalog from this repository. They do not own separate Recipe registries. The served identity of a Recipe is the Git commit a reader fetched; the catalog carries no revision of its own.

## Execution model

A Recipe executes inside an existing Studio Intent.

```text
Recipe definition + current Intent context = execution
```

The Recipe does not require the engineer to restate environment, repository, Domain, platform, or source context that Studio already knows. `works_with.platforms` is used for discovery and compatibility; it is not a set of invocation arguments.

## Three prompt concepts

1. **Website invocation pointer**: small copyable text that names the Recipe and its path and tells the agent to read it in the current Intent context.
2. **The Recipe's `## Prompt`**: the canonical task specification; what outcome the agent must deliver.
3. **The Recipe's `## Agent guidance`**: how the agent should approach execution.

The website may display the prompt and guidance for evaluation, but they are not the copy-and-paste invocation payload.

## Repository layout

```text
recipes/<recipe-id>/recipe.md      canonical Recipe: YAML frontmatter + Markdown body
collections/<collection-id>.json   canonical Collection
schema/recipe.schema.json          Recipe frontmatter contract, with the body rules under x-body
schema/collection.schema.json      Collection contract
schema/catalog.schema.json         catalog.json contract
scripts/build_catalog.py           validation + catalog generator
scripts/check_schema_versions.py   schema version-bump check
catalog.json                       generated metadata-only discovery index
templates/recipe.md                starting point for a new Recipe
```

`recipe.md` and the Collection files are authoritative. `catalog.json` is generated and must not be edited by hand. It holds each Recipe's metadata plus its `path` and `sha256`, never the prompt, acceptance conditions or guidance; readers fetch `recipe.md` for those. `schema_versions` records the schema versions the catalog was built against.

## Checks

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -q
.venv/bin/python scripts/build_catalog.py --check
```

Run `scripts/build_catalog.py` without `--check` to regenerate `catalog.json`. CI (`.github/workflows/ci.yml`) runs the tests, the `--check` build and the schema version-bump check on every pull request and every push to `main`.

## Platforms

Exact execution-target values, shared with Studio: `duckdb_local`, `motherduck`, `fabric_lakehouse`, `fabric_warehouse`, `redshift`. There is no generic `fabric` value; the website may group the two Fabric targets under one Microsoft Fabric Collection with All, Lakehouse and Warehouse views.

## Readiness

- `proven`: a dedicated Recipe-level eval or journey proves the exact Recipe shape end to end, named in `evidence.evals`. The schema rejects `proven` without one.
- `supported`: current capabilities can execute the Recipe end to end, without a dedicated Recipe-level eval.
- `planned`: at least one required capability, integration or object type is unsupported today.

## Collections

Collections are non-executable discovery views over Recipes; they never copy Recipe definitions and may name only Recipes that exist. Website publication thresholds: a function Collection needs at least 3 `supported` or `proven` Recipes, any other Collection at least 1; `planned` Recipes do not count.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) and the Recipe template in [templates/recipe.md](templates/recipe.md). The contract is recorded in [ADR 0001](docs/adr/0001-cookbook-recipe-contract.md).

## Recipes

- [Convert a full-refresh dbt model to incremental and show the runtime delta](recipes/dbt-full-refresh-to-incremental/recipe.md)
- [Land a SaaS or REST API into bronze with an incremental cursor and a schema contract](recipes/api-to-bronze-incremental-contract/recipe.md)
- [Author a Fabric Data Pipeline that sequences ingestion, dbt, and downstream refresh as committed code](recipes/fabric-data-pipeline-as-code/recipe.md)
- [Schedule a dlt load and a dbt build on MotherDuck as a committed MotherDuck Flight](recipes/motherduck-flight-scheduling/recipe.md)
````

- [ ] **Step 6: Run the tests and the stale-reference sweep**

Run: `.venv/bin/python -m pytest -q && .venv/bin/python scripts/build_catalog.py --check && git grep -n -e 'recipe\.json' -e 'duckdb[^_]' -e 'revision' -- README.md CONTRIBUTING.md templates/`
Expected: tests PASS, the check exits 0, and the `git grep` prints only the README sentence "the catalog carries no revision of its own". Any other hit is a stale reference to fix.

- [ ] **Step 7: Commit**

```bash
git add templates/recipe.md CONTRIBUTING.md README.md tests/test_template.py
git commit -m "docs: contributor guide, Recipe template and README for the Markdown contract

Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>"
```

---

### Task 14: ADR 0001 and final verification

**Files:**
- Create: `docs/adr/0001-cookbook-recipe-contract.md`

- [ ] **Step 1: Create `docs/adr/0001-cookbook-recipe-contract.md`**

```markdown
# 1. Cookbook Recipe contract

- Status: Accepted
- Date: 2026-09-25
- Issue: VD-6115

## Context

Recipes were JSON even though most of each one is guidance written by people and read by agents. The catalog embedded a second full copy of every Recipe and had no schema, neither schema had a version, the hand-written catalog revision always named an earlier commit, platform names differed from Studio's, and a Recipe could omit its platforms. Consumers had to guess the contract, and Studio's Recipe discovery (VD-6112) returned nothing as a result.

## Decision

1. **Markdown Recipes with schema-validated frontmatter.** Each Recipe is `recipes/<id>/recipe.md`: YAML frontmatter validated by `schema/recipe.schema.json`, then a body with a closed, required set of headings (`## Prompt`, `## Verified by`, `## Agent guidance` with `### Instructions`, `### Compose`, `### Ask first`, `### Guardrails`). The prompt is one paragraph that fits a table cell, each acceptance condition is one bullet, every field has a length cap, and markup that could escape its section is rejected. The body and markup rules are published as data under `x-body` in the Recipe schema, so every validator applies the same rules.
2. **A generated, metadata-only catalog.** `scripts/build_catalog.py` generates `catalog.json` from frontmatter alone. Entries are sorted by id, regeneration is byte-stable, and each entry carries the Recipe file's `path` and `sha256`. The catalog holds no prompt, acceptance conditions or guidance; `evidence` stays because it backs the `proven` claim. `schema/catalog.schema.json` validates it, and Collections may name only existing Recipes.
3. **Versioned schemas published with the catalog.** Each schema carries a top-level integer `version`, raised by one only for a breaking change. The catalog records `schema_versions`. CI compares each schema with the merge base and fails a breaking change without a bump, or a bump without a breaking change.
4. **The Git commit is the served identity.** The hand-written `revision` is removed. A reader reports the commit it fetched; the schema version only says whether it can parse what it fetched.
5. **Studio's platform values.** `works_with.platforms` is required and uses `duckdb_local`, `motherduck`, `fabric_lakehouse`, `fabric_warehouse` and `redshift`, so no mapping exists anywhere. `compose` stays an advisory hint the cookbook does not validate.

## Consequences

- Readers fetch `recipe.md` at the catalog's commit for the body and can verify it against `sha256`.
- The catalog no longer carries `canonical_url`; a consumer derives a link from `source` and `path`.
- Adding an optional frontmatter field is not breaking, but it touches both `recipe.schema.json` and `catalog.schema.json`, whose copies a test keeps identical.
- The caps were set from the published Recipes with headroom; a legitimate Recipe that hits one raises the cap, which is not a breaking change.
- Signed releases, release tags and branch protection stay out of scope; readers keep following `main`.

## Alternatives considered

- **Keep JSON Recipes.** Rejected: guidance written as escaped JSON strings is hard to author and review, and the body is what people and agents read.
- **Embed Recipe bodies in the catalog.** Rejected: two copies drift, and the catalog is a discovery index, not a distribution format.
- **Keep a revision field in the catalog.** Rejected: a file cannot name the commit that contains it, so it always named an earlier one.
- **Semantic-version strings for schemas.** Rejected: readers only need to know whether they can parse a schema, which one integer says.
```

- [ ] **Step 2: Run the full verification**

Run: `.venv/bin/python -m pytest -q && .venv/bin/python scripts/build_catalog.py --check && .venv/bin/python scripts/check_schema_versions.py --base "$(git merge-base origin/main HEAD)" && git status --short`
Expected: tests PASS; `validated 4 recipe(s), 3 collection(s); 2 collection(s) website-visible`; `schema versions consistent with <sha>`; `git status --short` lists only `docs/adr/0001-cookbook-recipe-contract.md`.

- [ ] **Step 3: Commit**

```bash
git add docs/adr/0001-cookbook-recipe-contract.md
git commit -m "docs(adr): 0001 cookbook Recipe contract

Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>"
```

## Acceptance-criteria coverage

| VD-6115 criterion (cookbook side) | Task |
| --- | --- |
| Every Recipe is one Markdown file with optional `pitch` and the closed heading set; lists are bullets | 1, 4, 6, 10 to 12 |
| Outcome, acceptance and guidance text unchanged by the conversion | 6 |
| Schema validates metadata; body rules require every section, table-cell prompt, one condition per line | 1, 4, 7 |
| Every Recipe declares platforms with Studio's names | 1, 2, 6 |
| Length caps; markup that could escape a section is rejected | 1, 4, 5, 7 |
| `compose` advisory, no plugin skill list | 1 (caps only), 13 |
| Catalog generated from metadata, no copies, stable order, `evidence` kept | 7 |
| Each entry has its file and content hash | 7 |
| Catalog validated by its own schema | 2, 7 |
| Hand-written revision removed | 2, 7 |
| Collections reference only existing Recipes | 7 |
| Top-level integer `version`, `schema_versions` in the catalog | 1, 2, 7 |
| Publishing fails on a contract violation or an unbumped schema change | 7, 8, 9 |
| Three new Recipes with agreed platforms and readiness, checkable conditions, cookbook shape | 10, 11, 12 |
| Contributor guide with a Recipe template | 13 |
| ADR records the contract | 14 |
