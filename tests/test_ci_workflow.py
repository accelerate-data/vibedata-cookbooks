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
