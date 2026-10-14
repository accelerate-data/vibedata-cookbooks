"""The PR policy check: evidence sections for Recipe changes, no catalog.json edits."""

from __future__ import annotations

import json
import re
import subprocess
from typing import Any

import check_pr_policy
from check_pr_policy import EVIDENCE_HEADINGS, check, main
from samples import REPO_ROOT

FULL_BODY = "".join(f"## {heading}\n\nFilled in.\n\n" for heading in EVIDENCE_HEADINGS)
RECIPE = ["recipes/foo/recipe.md"]


def event(body: str | None, base: str = "pre-prod", head: str = "feat/x", action: str = "opened") -> dict[str, Any]:
    return {
        "action": action,
        "pull_request": {"body": body, "base": {"ref": base, "sha": "b"}, "head": {"ref": head, "sha": "h"}},
    }


def section_replaced(body: str, heading: str, text: str) -> str:
    start = body.index(f"## {heading}\n") + len(f"## {heading}\n")
    end = body.find("\n## ", start)
    return body[:start] + "\n" + text + "\n" + (body[end:] if end != -1 else "")


def test_no_recipe_change_needs_no_evidence():
    assert check(event(""), ["README.md", "collections/x.json"]) == []


def test_full_body_passes():
    assert check(event(FULL_BODY), RECIPE) == []


def test_missing_heading_is_named():
    body = FULL_BODY.replace("## Platform compatibility", "## Platforms")
    errors = check(event(body), RECIPE)
    assert len(errors) == 1 and "'## Platform compatibility'" in errors[0]


def test_comment_only_section_is_empty():
    body = section_replaced(FULL_BODY, "Limitations and material risks", "<!-- todo\nstill todo -->")
    assert any("is empty" in e and "Limitations" in e for e in check(event(body), RECIPE))


def test_planned_not_applicable_passes():
    body = section_replaced(FULL_BODY, "Implementation example and execution evidence", "Not applicable: planned")
    assert check(event(body), RECIPE) == []


def test_edited_event_is_revalidated():
    assert check(event(FULL_BODY, action="edited"), RECIPE) == []
    assert check(event("", action="edited"), RECIPE)


def test_promotion_and_other_bases_are_out_of_scope():
    assert check(event("", base="main", head="pre-prod"), RECIPE + ["catalog.json"]) == []
    assert check(event("", base="main", head="feat/x"), RECIPE) == []


def test_catalog_edit_fails():
    errors = check(event(FULL_BODY), ["catalog.json"])
    assert len(errors) == 1 and "catalog.json" in errors[0]


def test_null_body_reports_every_heading():
    errors = check(event(None), RECIPE)
    assert len(errors) == len(EVIDENCE_HEADINGS)


def test_crlf_body_is_parsed():
    assert check(event(FULL_BODY.replace("\n", "\r\n")), RECIPE) == []


def test_heading_whitespace_and_fences():
    assert check(event(FULL_BODY.replace("## Summary\n", "## Summary   \n")), RECIPE) == []
    fenced = "```\n" + FULL_BODY + "```\n"
    assert len(check(event(fenced), RECIPE)) == len(EVIDENCE_HEADINGS)


def test_deleted_recipe_does_not_require_evidence():
    # main() passes --diff-filter=d, so a deletion never reaches check()
    assert check(event(""), []) == []


def test_main_prints_github_errors(tmp_path, capsys):
    ev = tmp_path / "event.json"
    ev.write_text(json.dumps(event("")))
    files = tmp_path / "files.txt"
    files.write_text("recipes/foo/recipe.md\n")
    assert main(["--event", str(ev), "--changed-files", str(files)]) == 1
    assert capsys.readouterr().out.count("::error::") == len(EVIDENCE_HEADINGS)


def test_main_out_of_scope_needs_no_git(tmp_path):
    ev = tmp_path / "event.json"
    ev.write_text(json.dumps(event("", base="main")))
    assert main(["--event", str(ev)]) == 0


def test_main_excludes_deleted_files_from_git_diff(tmp_path, monkeypatch):
    calls = []

    def fake_run(argv, **kwargs):
        calls.append(argv)
        return subprocess.CompletedProcess(argv, 0, stdout="", stderr="")

    monkeypatch.setattr(check_pr_policy.subprocess, "run", fake_run)
    ev = tmp_path / "event.json"
    ev.write_text(json.dumps(event("")))
    assert main(["--event", str(ev)]) == 0
    assert calls == [["git", "diff", "--name-only", "--diff-filter=d", "b...h"]]


def test_template_headings_match_policy():
    text = (REPO_ROOT / ".github/pull_request_template.md").read_text(encoding="utf-8")
    assert re.findall(r"^## (.+?)\s*$", text, re.M)[: len(EVIDENCE_HEADINGS)] == list(EVIDENCE_HEADINGS)
