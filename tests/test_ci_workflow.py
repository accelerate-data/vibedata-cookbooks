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
        "python scripts/build_catalog.py --validate",
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


def test_freshness_is_checked_only_on_the_way_to_main():
    steps = load_workflow()["jobs"]["contract"]["steps"]
    check = next(step for step in steps if step.get("run") == "python scripts/build_catalog.py --check")
    assert "github.base_ref == 'main'" in check["if"]
    assert "github.ref == 'refs/heads/main'" in check["if"]
    validate = next(step for step in steps if step.get("run") == "python scripts/build_catalog.py --validate")
    assert "if" not in validate


def test_catalog_is_regenerated_after_each_merge_to_pre_prod():
    workflow = yaml.safe_load((REPO_ROOT / ".github/workflows/catalog.yml").read_text(encoding="utf-8"))
    triggers = workflow.get("on", workflow.get(True))
    assert triggers == {"push": {"branches": ["pre-prod"]}}
    assert workflow["permissions"] == {"contents": "read"}
    assert workflow["concurrency"]["cancel-in-progress"] is False
    steps = workflow["jobs"]["regenerate"]["steps"]
    app_token = next(step for step in steps if step.get("uses", "").startswith("actions/create-github-app-token@"))
    assert app_token["with"]["permission-contents"] == "write"
    checkout = next(step for step in steps if step.get("uses", "").startswith("actions/checkout@"))
    assert checkout["with"]["token"] == "${{ steps.app-token.outputs.token }}"
    runs = "\n".join(step.get("run", "") for step in steps)
    assert "python scripts/build_catalog.py" in runs
    assert "git diff --quiet -- catalog.json" in runs
    assert "git push origin HEAD:pre-prod" in runs


def test_pr_policy_workflow_triggers():
    wf = yaml.safe_load((REPO_ROOT / ".github/workflows/pr-policy.yml").read_text(encoding="utf-8"))
    triggers = wf.get("on", wf.get(True))
    assert set(triggers["pull_request"]["types"]) == {"opened", "edited", "synchronize", "reopened"}
    assert "paths" not in triggers["pull_request"]
    assert {j["name"] for j in wf["jobs"].values()} == {"PR policy", "Secret scan"}
    assert wf["concurrency"]["cancel-in-progress"] is True


def test_gitleaks_is_pinned_and_verified():
    text = (REPO_ROOT / ".github/workflows/pr-policy.yml").read_text(encoding="utf-8")
    assert "gitleaks_8.30.1_linux_x64.tar.gz" in text
    assert "551f6fc83ea457d62a0d98237cbad105af8d557003051f41f3e7ca7b3f2470eb" in text
    assert "sha256sum -c" in text


def test_secret_scan_includes_merge_commit_content():
    text = (REPO_ROOT / ".github/workflows/pr-policy.yml").read_text(encoding="utf-8")
    assert '--log-opts="--diff-merges=first-parent $BASE_SHA..$HEAD_SHA"' in text


def test_pull_request_workflows_are_read_only():
    for path in (REPO_ROOT / ".github/workflows").glob("*.yml"):
        wf = yaml.safe_load(path.read_text(encoding="utf-8"))
        if "pull_request" not in wf.get("on", wf.get(True)):
            continue
        assert wf["permissions"] == {"contents": "read"}, path.name
        runs = "\n".join(s.get("run", "") for j in wf["jobs"].values() for s in j["steps"])
        assert "git push" not in runs and "git commit" not in runs, path.name
        for expression in (
            "github.event.pull_request.body",
            "github.event.pull_request.title",
            "github.event.pull_request.head.ref",
            "github.head_ref",
        ):
            assert expression not in runs, (path.name, expression)
