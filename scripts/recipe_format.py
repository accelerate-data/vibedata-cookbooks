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
