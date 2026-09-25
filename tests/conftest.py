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
