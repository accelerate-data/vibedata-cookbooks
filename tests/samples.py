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
