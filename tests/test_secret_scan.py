"""The pinned gitleaks binary flags a real-looking secret and ignores placeholders.
Skipped when no gitleaks binary is available; CI sets GITLEAKS_BIN."""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import pytest

GITLEAKS = os.environ.get("GITLEAKS_BIN") or shutil.which("gitleaks")
pytestmark = pytest.mark.skipif(not GITLEAKS, reason="gitleaks binary not available")


def scan(directory: Path) -> int:
    return subprocess.run([str(Path(GITLEAKS).resolve()), "dir", "--no-banner", str(directory)], capture_output=True).returncode


def test_synthetic_secret_is_caught(tmp_path):
    # Built from joined parts so the repo holds no literal token.
    (tmp_path / "config.txt").write_text("aws_key = " + "AKIA" + "Z7QX" + "J4LM" + "NOPQ" + "R2S3", encoding="utf-8")
    assert scan(tmp_path) == 1


def test_placeholder_is_not_flagged(tmp_path):
    (tmp_path / "config.txt").write_text("token: <api_token>\nkey = your-token-here\n", encoding="utf-8")
    assert scan(tmp_path) == 0
