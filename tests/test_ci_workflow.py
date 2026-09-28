"""The CI workflow runs every contract gate on pull requests and on pushes to pre-prod and main,
and admits only pre-prod into main."""

from __future__ import annotations

import yaml

from samples import REPO_ROOT

WORKFLOW = REPO_ROOT / ".github/workflows/ci.yml"


def load_workflow():
    return yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))


def test_ci_runs_every_gate():
    workflow = load_workflow()
    triggers = workflow.get("on", workflow.get(True))  # YAML 1.1 reads a bare `on` key as True
    assert "pull_request" in triggers
    assert triggers["push"]["branches"] == ["pre-prod", "main"]
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


def test_main_takes_only_pre_prod():
    job = load_workflow()["jobs"]["promotion-source"]
    assert job["name"] == "Promotion source"
    assert job["if"] == "github.event_name == 'pull_request' && github.base_ref == 'main'"
    step = job["steps"][0]
    assert step["env"]["HEAD_REF"] == "${{ github.head_ref }}"
    assert step["env"]["HEAD_REPO"] == "${{ github.event.pull_request.head.repo.full_name }}"
    assert '"$HEAD_REF" != "pre-prod"' in step["run"]
    assert '"$HEAD_REPO" != "$BASE_REPO"' in step["run"]
    assert "exit 1" in step["run"]
