"""Parse and check the Recipe file format: frontmatter, body sections and markup.

The rules themselves are data in schema/recipe.schema.json (x-body); this module
applies them. Every violation raises CookbookError with a message naming the rule.
"""

from __future__ import annotations

from typing import Any

import re
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
