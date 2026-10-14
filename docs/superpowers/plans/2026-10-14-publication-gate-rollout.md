# Cookbook Publication Gate Rollout Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Apply the approved Cookbook publication gate across `vibedata-cookbooks` (CI, template, docs, tests), `gtm-skills` (the `reviewing-recipe` skill), and `vibedata-gtm` (cookbook docs). Then apply the `pre-prod` ruleset and file the consumer follow-up after operator approval.

**Architecture:** Tracks A, B, and C are independent and run in parallel worktrees. Each track ends in one PR, and no PR merges automatically. Track D makes the external writes. It runs only at operator checkpoints, and D1 runs only after the Track A PR merges.

**Tech Stack:** Python 3.12, pytest 8.3.4, PyYAML 6.0.2, jsonschema 4.23.0 (cookbook `requirements.txt`). GitHub Actions. gitleaks CLI v8.30.1. `gh` CLI. Linear MCP. Markdown skills.

**Spec:** `/Users/shwetanksheel/scratch/99_working/vibedata-cookbooks/docs/superpowers/specs/2026-10-14-publication-gate-rollout-design.md`. It refers to the source spec `2026-10-14-publication-gate-source-spec.md` in the same folder. Read both. The design doc wins wherever the two differ.

## Global Constraints

- Cookbook work branches from `origin/pre-prod`, and its PR targets `pre-prod`. gtm-skills and vibedata-gtm branch from `origin/main` and target `main`.
- Never merge a PR. Never push to `pre-prod` or `main`.
- No `Co-Authored-By` or other AI attribution in commit messages. Commit author: Shwetank Sheel <github@shwetank.com>. Every PR body ends with: `_Drafted with Claude's help — content and judgment are mine; Claude helped implement and verify the changes._`
- Stage only named files. Never run `git add -A`.
- Never change files under `recipes/`, `collections/`, `schema/`, or `catalog.json` in the cookbook.
- Every PR workflow runs with `permissions: contents: read`. No workflow step pushes, commits, or edits source.
- The PR body is read only from `$GITHUB_EVENT_PATH`, by Python or `jq`. It is never placed in a `${{ }}` expression inside a `run:` block.
- gitleaks: version `8.30.1`, asset `gitleaks_8.30.1_linux_x64.tar.gz`, SHA-256 `551f6fc83ea457d62a0d98237cbad105af8d557003051f41f3e7ca7b3f2470eb`. The SHA-256 is hardcoded in the workflow and is not read from the release's checksum file.
- The evidence headings, exactly, in this order: `Summary`, `Distinct outcome and overlap`, `Readiness and required capabilities`, `Platform compatibility`, `Implementation example and execution evidence`, `Limitations and material risks`.
- Reader-facing verdicts, exactly: `PASS`, `PASS WITH WARNINGS`, `CHANGES REQUIRED`. Finding classes, exactly: Blocker, Warning, Suggestion.
- The skill name is `reviewing-recipe`, and it is invoked as `gtm-skills:reviewing-recipe`.
- In gtm-skills, change the Claude and Codex manifests together to `0.14.0`.
- Do not read, scan, or link Google Drive content in any check, skill step, or test.
- Times reported to the operator use the workstation's local timezone (`date +%Z`).

## Review Focus

1. **The PR body is `null`.** This happens when an author deletes the template. Expected: one `::error::` line for each heading, and the script does not crash. Test: `test_null_body_reports_every_heading` (Task A2).
2. **The body has CRLF line endings.** The GitHub web editor saves `\r\n`. Expected: the headings are still found. Test: `test_crlf_body_is_parsed` (Task A2).
3. **A heading has trailing spaces, or a heading line appears inside a fenced code block.** Expected: trailing spaces are ignored, and a heading inside a fence does not count. Test: `test_heading_whitespace_and_fences` (Task A2).
4. **A PR only deletes a `recipe.md`.** Expected: the evidence headings are not required, and the deletion still goes through human review. Test: `test_deleted_recipe_does_not_require_evidence` (Task A2). `changed_files` comes from `git diff --name-only --diff-filter=d`.
5. **An edited PR body contains a secret, and no new commit was pushed.** Expected: `Secret scan` re-runs on the `edited` event and fails. Covered by the workflow trigger assertion in `test_pr_policy_workflow_triggers` (Task A3), plus the manual check in Task A5 step 3.

---

## Track A — `vibedata-cookbooks`

Worktree: `git worktree add ../vibedata-cookbooks-gate -b feat/publication-gate origin/pre-prod`. Copy the spec, source spec, and this plan from the main checkout into the worktree under `docs/superpowers/`. The PR carries them.

### Task A1: Allow `proven` evals in the published-Recipe test

**Files:**
- Modify: `tests/test_published_recipes.py:51`

- [ ] **Step 1:** Replace `assert entry["evidence"]["evals"] == []` with:

```python
    if entry["readiness"] == "proven":
        assert entry["evidence"]["evals"], f"{recipe_id} is proven but names no eval"
```

- [ ] **Step 2:** Run `python -m pytest -q tests/test_published_recipes.py tests/test_recipe_schema.py`. Expected: PASS. Confirm that `test_recipe_schema.py` already has a case where `proven` without evals fails the schema. If it does not, add `test_proven_without_evals_is_rejected` to it, using the sample builders in `tests/samples.py`.
- [ ] **Step 3:** Commit: `test: allow proven Recipes to name their evals`.

### Task A2: PR policy script

**Files:**
- Create: `scripts/check_pr_policy.py`
- Create: `tests/test_pr_policy.py`

**Interfaces:**
- Produces:
  - `EVIDENCE_HEADINGS: tuple[str, ...]`, the six headings from Global Constraints.
  - `check(event: dict, changed_files: list[str]) -> list[str]`, which returns error messages. An empty list means pass.
  - `main(argv: list[str] | None = None) -> int`, with the arguments `--event PATH` (required) and `--changed-files PATH` (optional; a newline list). When `--changed-files` is missing, `main` runs `git diff --name-only --diff-filter=d <base.sha>...<head.sha>`, taking both SHAs from the event. It prints each error as `::error::<message>` and returns 1 if there is any error, otherwise 0.
- `check` rules:
  - Scope: when `event["pull_request"]["base"]["ref"] != "pre-prod"` or `head.ref == "pre-prod"`, return `[]`.
  - Catalog: if `"catalog.json"` is in `changed_files`, add the error `catalog.json is regenerated after merge (docs/adr/0003-catalog-generated-after-merge.md); remove it from this pull request.`
  - Evidence: if a changed file matches `recipes/*/recipe.md`, parse the body. A missing heading gives the error `PR description is missing the '## <heading>' section (see .github/pull_request_template.md).` A heading whose section text is empty after HTML comments are removed and whitespace is stripped gives the error `PR description section '## <heading>' is empty; for a planned Recipe write 'Not applicable: planned'.`
  - Parsing: normalize `\r\n` to `\n`. Treat a `None` body as `""`. A heading is a line that matches `^## (.+?)\s*$` and is outside a ``` fence. A section runs until the next `## ` heading line.

- [ ] **Step 1: Write the failing tests.** Use a helper `event(body, base="pre-prod", head="feat/x", action="opened")` that returns `{"action": action, "pull_request": {"body": body, "base": {"ref": base, "sha": "b"}, "head": {"ref": head, "sha": "h"}}}`, and a constant `FULL_BODY` with all six headings filled.

```python
RECIPE = ["recipes/foo/recipe.md"]

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
    ev = tmp_path / "event.json"; ev.write_text(json.dumps(event("")))
    files = tmp_path / "files.txt"; files.write_text("recipes/foo/recipe.md\n")
    assert main(["--event", str(ev), "--changed-files", str(files)]) == 1
    assert capsys.readouterr().out.count("::error::") == len(EVIDENCE_HEADINGS)
```

`section_replaced(body, heading, text)` is a test helper that replaces the text under one heading.

- [ ] **Step 2:** Run `python -m pytest -q tests/test_pr_policy.py`. Expected: FAIL with `ModuleNotFoundError: check_pr_policy`.
- [ ] **Step 3:** Implement `scripts/check_pr_policy.py` to the interface above. Use only the standard library. Start the file with a module docstring in the style of the other scripts.
- [ ] **Step 4:** Run `python -m pytest -q tests/test_pr_policy.py`. Expected: PASS.
- [ ] **Step 5:** Commit: `feat(ci): check PR evidence sections and catalog edits`.

### Task A3: PR policy workflow and secret scan

**Files:**
- Create: `.github/workflows/pr-policy.yml`
- Create: `.gitleaksignore`, containing only a comment header that describes the fingerprint-and-reason format
- Modify: `tests/test_ci_workflow.py`
- Create: `tests/test_secret_scan.py`

**Interfaces:**
- Consumes: `python scripts/check_pr_policy.py --event "$GITHUB_EVENT_PATH"` (Task A2).
- Produces: the status check names `PR policy` and `Secret scan`. Task D1 depends on these exact names.

Workflow shape:
- `on: pull_request: types: [opened, edited, synchronize, reopened]`, with no `paths` filter.
- `permissions: contents: read`.
- Job `policy`, named `PR policy`: checkout with `fetch-depth: 0`, setup-python 3.12, then run `python scripts/check_pr_policy.py --event "$GITHUB_EVENT_PATH"`. No dependency install is needed.
- Job `secrets`, named `Secret scan`:
  1. Checkout with `fetch-depth: 0`.
  2. Download the pinned tarball with `curl -fsSL`. Verify it with `echo "<sha>  <file>" | sha256sum -c -`. Extract `gitleaks`.
  3. Run `./gitleaks git --redact --no-banner --log-opts="$BASE_SHA..$HEAD_SHA" .`. `BASE_SHA` and `HEAD_SHA` come from `env:` set to `${{ github.event.pull_request.base.sha }}` and `${{ github.event.pull_request.head.sha }}`. SHAs are safe in `env:`.
  4. Run `jq -r '.pull_request.body // ""' "$GITHUB_EVENT_PATH" > "$RUNNER_TEMP/pr-body.md"`, then `./gitleaks dir --redact --no-banner "$RUNNER_TEMP/pr-body.md"`.
  5. Install `requirements.txt` and run `python -m pytest -q tests/test_secret_scan.py` with `GITLEAKS_BIN=./gitleaks`, so that the synthetic-secret test runs in CI.
- Before you write the steps, check the exact subcommand and flag names against `gitleaks --help` for v8.30.1 through Context7 or the release README. Also confirm that the CLI needs no license key. The license applies only to `gitleaks-action`. If the CLI needs a license, stop and escalate.

- [ ] **Step 1: Write the failing tests** in `tests/test_ci_workflow.py`:

```python
def test_pr_policy_workflow_triggers():
    wf = yaml.safe_load((REPO_ROOT / ".github/workflows/pr-policy.yml").read_text(encoding="utf-8"))
    triggers = wf.get("on", wf.get(True))
    assert set(triggers["pull_request"]["types"]) == {"opened", "edited", "synchronize", "reopened"}
    assert "paths" not in triggers["pull_request"]
    assert {j["name"] for j in wf["jobs"].values()} == {"PR policy", "Secret scan"}

def test_gitleaks_is_pinned_and_verified():
    text = (REPO_ROOT / ".github/workflows/pr-policy.yml").read_text(encoding="utf-8")
    assert "gitleaks_8.30.1_linux_x64.tar.gz" in text
    assert "551f6fc83ea457d62a0d98237cbad105af8d557003051f41f3e7ca7b3f2470eb" in text
    assert "sha256sum -c" in text

def test_pull_request_workflows_are_read_only():
    for path in (REPO_ROOT / ".github/workflows").glob("*.yml"):
        wf = yaml.safe_load(path.read_text(encoding="utf-8"))
        if "pull_request" not in wf.get("on", wf.get(True)):
            continue
        assert wf["permissions"] == {"contents": "read"}, path.name
        runs = "\n".join(s.get("run", "") for j in wf["jobs"].values() for s in j["steps"])
        assert "git push" not in runs and "git commit" not in runs, path.name
        assert "github.event.pull_request.body" not in runs, path.name
```

Write `tests/test_secret_scan.py`. It skips unless `os.environ.get("GITLEAKS_BIN")` or `shutil.which("gitleaks")` finds a binary.
  - `test_synthetic_secret_is_caught`: write `"aws_key = " + "AKIA" + "Z7QX" + "J4LM" + "NOPQ" + "R2S3"` to a file in `tmp_path` and run `<bin> dir --no-banner <tmp>`. Expected: exit code 1. Build any token that triggers a gitleaks rule only from joined strings, so the repo does not contain a literal one.
  - `test_placeholder_is_not_flagged`: a file that contains `<api_token>` and `your-token-here`. Expected: exit code 0.

- [ ] **Step 2:** Run `python -m pytest -q tests/test_ci_workflow.py`. Expected: FAIL, because `pr-policy.yml` does not exist.
- [ ] **Step 3:** Write `.github/workflows/pr-policy.yml` and `.gitleaksignore` to the shape above.
- [ ] **Step 4:** Run `python -m pytest -q`. Expected: PASS. Then, locally with `brew install gitleaks`: run `GITLEAKS_BIN=$(which gitleaks) python -m pytest -q tests/test_secret_scan.py`. Expected: 2 passed. Then run `gitleaks git --log-opts="origin/pre-prod..HEAD" .`. Expected: no leaks.
- [ ] **Step 5:** Commit: `feat(ci): add PR policy and pinned gitleaks secret scan`.

### Task A4: PR template, CONTRIBUTING, README

**Files:**
- Modify: `.github/pull_request_template.md`. Replace it fully with source spec §4.2. The headings must match `EVIDENCE_HEADINGS`.
- Modify: `CONTRIBUTING.md`, following design §A5.
- Modify: `README.md`, following design §A5.
- Modify: `tests/test_pr_policy.py`

- [ ] **Step 1: Write a failing test** that keeps the template and the check in step:

```python
def test_template_headings_match_policy():
    text = (REPO_ROOT / ".github/pull_request_template.md").read_text(encoding="utf-8")
    assert re.findall(r"^## (.+?)\s*$", text, re.M)[: len(EVIDENCE_HEADINGS)] == list(EVIDENCE_HEADINGS)
```

- [ ] **Step 2:** Run it. Expected: FAIL, because the current template has `Summary` and `Checklist` only.
- [ ] **Step 3:** Write the template. Then edit `CONTRIBUTING.md`:
  - Add the readiness rules, the one-example rule, the review classes and verdicts, self-review, and the review scope (public repo and PR evidence only).
  - Rename "Accelerate Data contributors" to "Internal archive". Its first sentence says the archive is not part of publication review.
  - Rewrite "Branches" for the D1 ruleset.
  - Add a "Secret scan false positives" paragraph about `.gitleaksignore`.

  Then edit `README.md` for the `planned` invocation semantics. Use plain, active-voice prose, and do not hard-wrap mid-sentence. Do not copy schema caps.
- [ ] **Step 4:** Run `python -m pytest -q && python scripts/build_catalog.py --validate && python scripts/check_schema_versions.py --base "$(git merge-base origin/pre-prod HEAD)"`. Expected: all pass.
- [ ] **Step 5:** Commit: `docs: publication review policy, evidence template, planned semantics`.

### Task A5: Open the Track A PR

- [ ] **Step 1:** Push `feat/publication-gate`, then run `gh pr create --base pre-prod`. The body uses the new template headings: write `Not applicable: no Recipe change` where a section does not apply. Add an "Outstanding" section that lists D1 (ruleset after merge) and D2 (consumer issue, link to follow).
- [ ] **Step 2:** Run `gh pr checks --watch`. Expected: `Cookbook contract`, `PR policy`, and `Secret scan` pass.
- [ ] **Step 3:** Revalidation check: edit the PR body to remove `## Summary`, then confirm that `PR policy` re-runs and passes. It passes because this PR changes no `recipe.md`. Restore the body. Record both run URLs in a PR comment.

---

## Track B — `gtm-skills`

Worktree: `git worktree add ../gtm-skills-reviewing-recipe -b feat/reviewing-recipe origin/main` in `~/scratch/ad-plugins/gtm-skills`. Extract the ZIP into a fresh temporary directory that is outside the repo, and copy files from there. Never run anything from inside the extracted folder.

### Task B1: Port and register the skill

**Files:**
- Create: `skills/reviewing-recipe/{SKILL.md,references/review-rubric.md,references/output-format.md,agents/openai.yaml,assets/icon.svg}`, copied from the ZIP's `vibedata-recipe-review/`
- Modify: `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json`. Set `version` to `0.14.0`.
- Modify: `repo-map.json`, in the skills description and any skill list. Modify `AGENTS.md`: add a "Cookbook" group under `## Skills` that lists `skills/reviewing-recipe/SKILL.md - semantic publication review for Vibedata Cookbook Recipe PRs and pre-PR drafts`, and update the skill count.

- [ ] **Step 1:** Copy the files and set `name: reviewing-recipe` in the frontmatter. Keep `agents/openai.yaml` byte-for-byte, except for `display_name`, which becomes `Reviewing Recipe`.
- [ ] **Step 2:** Run `npm run validate:plugin-manifests && npm run check:plugin-version`. Expected: PASS.
- [ ] **Step 3:** Commit: `feat(reviewing-recipe): port Recipe review skill into gtm-skills`.

### Task B2: Rewrite the skill to the publication rubric

**Files:**
- Modify: `skills/reviewing-recipe/SKILL.md`. It holds the frontmatter, the core principle, the 10-step workflow from source spec §3.1 (one line per step, pointing to the rubric), the re-review rule, and resource links. Target: 100 lines or fewer.
- Modify: `skills/reviewing-recipe/references/review-rubric.md`. It holds every rule in source spec §2 and §3.2–§3.3: the readiness and evidence table, platform rules, correctness, `Ask first` policy types, risk list, capability evidence, security scope, no Drive, the class definitions, the four parts of every blocker, and readiness/evidence findings kept separate from contract findings.
- Modify: `skills/reviewing-recipe/references/output-format.md`. It holds the verdict line, the verdict table for multiple PRs, Blockers/Warnings/Suggestions sections, paste-ready comment blocks, the GitHub mapping (`PASS` and `PASS WITH WARNINGS` → Approve; `CHANGES REQUIRED` → Request changes), the re-review layout (resolved, outstanding, new), and a "Comparison scope" line for the Linear duplicate check.

- [ ] **Step 1:** Rewrite the three files. Delete every `APPROVE`, `CHANGES REQUESTED`, and "implementation-example limitations are not blockers" rule from the old text. Do not keep them next to the new rules.
- [ ] **Step 2:** Run `grep -rnE "APPROVE\b|CHANGES REQUESTED" skills/reviewing-recipe`. Expected: no output. Then run `npm run check:skill-prose-wraps && npx markdownlint-cli2 "skills/reviewing-recipe/**/*.md"`. Expected: PASS.
- [ ] **Step 3:** Commit: `feat(reviewing-recipe): apply the Cookbook publication rubric`.

### Task B3: Eval fixtures and suite

**Files:**
- Create: `skills/reviewing-recipe/tests/evals/fixtures/<NN-slug>/{recipe.md,pr-body.md,expected.json}` for the 9 cases in source spec §3.4. Case 09 (re-review) also has `previous-review.md`. The `expected.json` shape is `{"verdict": "PASS"|"PASS WITH WARNINGS"|"CHANGES REQUIRED", "must_flag": [<short topic strings>], "must_not_flag": [<topics>]}`.
- Create: `skills/reviewing-recipe/tests/evals/eval_cases.py`. Follow the style of `skills/updating-personas/tests/evals/eval_cases.py`: a `case` decorator and a standalone runner.

Static cases. There are 7, and the limit is 10:
1. `fixtures-cover-the-nine-spec-cases`: there are exactly 9 fixture directories, and each `expected.json` parses with an allowed verdict.
2. `skill-uses-three-verdicts-only`: `SKILL.md` and `output-format.md` contain all three verdicts and no `APPROVE`.
3. `rubric-has-readiness-evidence-table`: `review-rubric.md` names `planned`, `supported`, and `proven`, and `evidence.evals`.
4. `no-drive-access`: the rubric says Drive is out of scope, and no file under the skill contains `drive.google.com`.
5. `blocker-has-four-parts`: `output-format.md` names the location, the violated requirement, the counterexample, and the smallest correction.
6. `fixture-recipes-are-format-valid`: if `VIBEDATA_COOKBOOKS_ROOT` exists, validate each fixture `recipe.md` with that repo's `scripts/recipe_format.py` plus the schema. Otherwise skip, and print the reason.
7. `frontmatter-name-matches-dir`: `name: reviewing-recipe`.

- [ ] **Step 1:** Write the fixtures. Build each `recipe.md` from the cookbook `templates/recipe.md`, so it is format-valid. Build each `pr-body.md` from the new PR template. Each fixture puts exactly the defect that its §3.4 case names into the smallest possible Recipe.
- [ ] **Step 2:** Write `eval_cases.py`. Run `python3 skills/reviewing-recipe/tests/evals/eval_cases.py`. Expected: 7 cases, all pass or skip with a reason.
- [ ] **Step 3: Behavioral dry run.** The Opus reviewer subagent loads `skills/reviewing-recipe/SKILL.md` and runs it on each fixture as a pre-PR draft review. It records the verdict, compared with `expected.json`, in `tests/evals/dry-run-2026-10-14.md`. Expected: 9 of 9 verdicts match, every `must_flag` topic is raised, and no `must_not_flag` topic is raised. On a mismatch, fix the rubric (not the fixture) and re-run that case.
- [ ] **Step 4:** Commit: `test(reviewing-recipe): eval fixtures and dry-run record`.

### Task B4: Open the Track B PR

- [ ] **Step 1:** Push, then run `gh pr create --base main`. The PR body includes the dry-run table and the note that this skill replaces the `vibedata-recipe-review` ZIP. Run `gh pr checks --watch`. Expected: PASS.

---

## Track C — `vibedata-gtm`

Worktree: `git worktree add ../vibedata-gtm-cookbook-review -b docs/cookbook-publication-review origin/main` in `~/scratch/99_working/vibedata-gtm`.

### Task C1: Readiness and publication review in the cookbook README

**Files:**
- Modify: `docs/gtm/plan/04-demand-inbound/cookbook/README.md`. This is the `## Readiness` section, currently around lines 326–334. Add a new `## Publication review` section right after it.

- [ ] **Step 1:** Replace the Readiness table with the table in source spec §2.2, and keep the `readiness` / `evidence` / `verified_by` paragraph. Add two rules: one example on one platform, DuckDB first; and a platform listed without its own example needs a compatibility rationale in the PR. Then add `## Publication review`: three to six lines that link to `https://github.com/accelerate-data/vibedata-cookbooks/blob/pre-prod/CONTRIBUTING.md` and name `gtm-skills:reviewing-recipe` and the three verdicts.
- [ ] **Step 2:** Run `npx markdownlint-cli2 docs/gtm/plan/04-demand-inbound/cookbook/README.md`. Expected: no new errors compared with `origin/main`.
- [ ] **Step 3:** Commit: `docs(cookbook): readiness evidence and publication review`.

### Task C2: Linear lifecycle follows review

**Files:**
- Modify: `docs/gtm/plan/04-demand-inbound/cookbook/linear-backlog.md`, the lifecycle list around lines 50–60.

- [ ] **Step 1:** Read the live GTM team workflow states with the Linear MCP `list_issue_statuses` tool for team GTM. This is read only.
- [ ] **Step 2:** Write the lifecycle: Backlog → In Progress → In Review → Done, following design §Track C. If `In Review` does not exist, write: "In Progress; post the latest review verdict as an issue comment". Done requires the Recipe URL and the final readiness.
- [ ] **Step 3:** Run markdownlint as in C1, then commit: `docs(cookbook): Linear lifecycle follows publication review`.
- [ ] **Step 4:** Push, then run `gh pr create --base main`.

---

## Track D — external writes (operator checkpoints)

### Task D2: Consumer follow-up issue (operator checkpoint)

- [ ] **Step 1:** Find which repositories render Cookbook Recipes and "Use Recipe". Use `gh search code "catalog.json" --owner accelerate-data` and `gh search code "readiness" --owner accelerate-data`, and check `~/Documents/ailearnings/_docs/projects.md`. Record each repo, with the file path and line.
- [ ] **Step 2:** Draft one Linear issue per consumer repo with the design §D2 behavior and acceptance checks. Propose a team and project for each. Show the drafts to the operator and **stop until they approve**.
- [ ] **Step 3:** After approval, create the issue(s) and link them in the Track A PR. Send a Pushover alert (priority 1) that says "D2 created" and gives the issue IDs.

### Task D1: `pre-prod` ruleset (operator checkpoint; after the Track A PR merges)

- [ ] **Step 1:** Confirm that the Track A PR is merged with `gh pr view <n> --json state,mergedAt`, and that `gh api repos/accelerate-data/vibedata-cookbooks/commits/pre-prod/check-runs --jq '.check_runs[].name'` lists `PR policy` and `Secret scan` on a recent PR head. If the PR is not merged, send a Pushover alert that the run is paused, and stop.
- [ ] **Step 2:** Read the live ruleset `24733664` with `gh api repos/accelerate-data/vibedata-cookbooks/rulesets/24733664`. Build the PUT payload: copy the live ruleset and change only the fields in the design §D1 table. `integration_id` for the new checks: use the GitHub Actions app id that the existing `Cookbook contract` check uses (`15368`). Show the diff between the live and the planned payload, and **stop until the operator approves**.
- [ ] **Step 3:** After approval, run `gh api -X PUT repos/accelerate-data/vibedata-cookbooks/rulesets/24733664 --input payload.json`. Read the ruleset back, then post a comment on the merged PR with the live values. If the live values differ from CONTRIBUTING "Branches", open a follow-up docs PR to fix CONTRIBUTING.

---

## Final review

After Tracks A–C open their PRs, dispatch two Opus reviewers in parallel. Scope them to the three PR diffs plus direct callers.
1. **Race and safety sweep:** workflow trigger and permission interactions, the catalog-app bypass, concurrent PR edits, and injection paths from the PR body.
2. **Dead-code sweep:** obsolete skill prose, template text, and doc sections that the change replaced.

Output rule for each reviewer: "Findings (severity · location · why), then recommended fix. Under 2000 chars." Fix the confirmed findings on the same branches. Report all findings in the final summary, including low-severity ones.
