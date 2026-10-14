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


def test_secret_added_in_a_merge_commit_is_caught(tmp_path):
    def git(*args: str) -> str:
        return subprocess.run(
            ["git", "-c", "user.name=t", "-c", "user.email=t@example.com", *args],
            cwd=tmp_path, capture_output=True, text=True, check=True,
        ).stdout.strip()

    git("init", "-q", "-b", "main")
    (tmp_path / "a.txt").write_text("a", encoding="utf-8")
    git("add", "a.txt")
    git("commit", "-qm", "base")
    base = git("rev-parse", "HEAD")
    git("checkout", "-qb", "side")
    (tmp_path / "s.txt").write_text("s", encoding="utf-8")
    git("add", "s.txt")
    git("commit", "-qm", "side")
    git("checkout", "-q", "main")
    (tmp_path / "m.txt").write_text("m", encoding="utf-8")
    git("add", "m.txt")
    git("commit", "-qm", "main")
    git("merge", "-q", "--no-ff", "--no-commit", "side")
    # The secret exists only in the merge commit's own diff.
    (tmp_path / "config.txt").write_text("aws_key = " + "AKIA" + "Z7QX" + "J4LM" + "NOPQ" + "R2S3", encoding="utf-8")
    git("add", "config.txt")
    git("commit", "-qm", "merge")
    head = git("rev-parse", "HEAD")

    def scan_log(log_opts: str) -> int:
        return subprocess.run(
            [str(Path(GITLEAKS).resolve()), "git", "--no-banner", "--redact", f"--log-opts={log_opts}", str(tmp_path)],
            capture_output=True,
        ).returncode

    assert scan_log(f"{base}..{head}") == 0  # the default log skips merge diffs
    assert scan_log(f"--diff-merges=first-parent {base}..{head}") == 1
