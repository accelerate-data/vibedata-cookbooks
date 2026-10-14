# Cookbook publication gate: rollout design

**Date:** 2026-10-14
**Source spec:** [2026-10-14-publication-gate-source-spec.md](2026-10-14-publication-gate-source-spec.md) (the approved requirements). This document says *where* and *how* each requirement is applied across three repositories. Where this document and the source spec differ, this document records an approved decision.
**Skill input:** `/Users/shwetanksheel/Downloads/vibedata-recipe-review.zip`

## Approved decisions

| # | Decision | Effect on the source spec |
| --- | --- | --- |
| D1 | The `pre-prod` ruleset gives repository admins `pull_request` bypass, not `always`. The `vibedata-cookbooks-catalog` GitHub App keeps `always` bypass. | Satisfies §4.4. Admins can still merge in an emergency; GitHub records each bypass. |
| D2 | The skill moves into `gtm-skills` as `reviewing-recipe` (`gtm-skills:reviewing-recipe`). | Overrides §3 "preserve the skill name". The ZIP is not maintained after the move. |
| D3 | GTM cookbook docs: the README Readiness section is rewritten, a "Publication review" section is added, and the `linear-backlog.md` lifecycle follows the review. | Extends §1 "Sources and authority": the ontology README must agree with the gate. |
| D4 | The consumer gap (§4.5) becomes drafted Linear issue(s). Creation needs operator approval. | Satisfies deliverable 5. |
| D5 | A fresh session runs one kickoff prompt. Three tracks run in parallel. Sonnet implements, Opus reviews. The output is three PRs. Nothing merges automatically. | Execution model only. |

## Repositories

| Track | Repository | Local path | Branch | PR target |
| --- | --- | --- | --- | --- |
| A | `accelerate-data/vibedata-cookbooks` | `~/scratch/99_working/vibedata-cookbooks` | `feat/publication-gate` from `origin/pre-prod` | `pre-prod` |
| B | `accelerate-data/gtm-skills` | `~/scratch/ad-plugins/gtm-skills` | `feat/reviewing-recipe` from `origin/main` | `main` |
| C | `accelerate-data/vibedata-gtm` | `~/scratch/99_working/vibedata-gtm` | `docs/cookbook-publication-review` from `origin/main` | `main` |

Each track works in its own git worktree. The local cookbook checkout is on `main` and has untracked files. Leave those files alone.

## Track A: `vibedata-cookbooks`

### A1. Fix the `proven` test contradiction

`tests/test_published_recipes.py` asserts `entry["evidence"]["evals"] == []` for every Recipe. Replace that assertion: a `proven` Recipe has nonempty `evals`. Do not assert anything about `evals` for other readiness values. `schema/recipe.schema.json` does not change. It already requires `evals` for `proven`.

### A2. PR policy check

- **Script:** `scripts/check_pr_policy.py`. Input: the event payload path (`$GITHUB_EVENT_PATH`) and the list of changed files. The script computes the changed files with `git diff --name-only <base_sha>...<head_sha>`, and both SHAs come from the payload. The PR body is read in Python only. It is never interpolated into a shell command.
- **Workflow:** `.github/workflows/pr-policy.yml`. Job name `PR policy`. Trigger: `pull_request` with types `opened, edited, synchronize, reopened`. No `paths` filter. A required check that a path filter skips stays pending, so the job always runs and passes when no rule applies. `permissions: contents: read`. Checkout with `fetch-depth: 0`.
- **Scope:** rules apply only when the base is `pre-prod` and the head is not `pre-prod`. A promotion PR to `main`, or a PR to any other base, passes.
- **Rule 1, evidence headings:** if any `recipes/**/recipe.md` changed, the body contains each of these level-2 headings exactly: `Summary`, `Distinct outcome and overlap`, `Readiness and required capabilities`, `Platform compatibility`, `Implementation example and execution evidence`, `Limitations and material risks`. Each section has text after HTML comments are removed. `Not applicable: planned` counts as text. The check validates structure only, never quality. A Collection-only or docs-only PR passes.
- **Rule 2, catalog:** if `catalog.json` changed, the job fails. The failure message points to ADR 0003.
- **Failure output:** one `::error::` line for each missing heading, empty section, or offending path.
- **No semantic checks:** do not search the body or the Recipe for keywords such as `late`, `null`, `guardrail`, or `ask first`. Do not validate `Compose` names.

### A3. Secret scan

- **Job:** `Secret scan` in `pr-policy.yml`, so it also re-runs when the body is edited. `permissions: contents: read`.
- **Tool:** the `gitleaks` CLI binary at a pinned release, with its SHA-256 checksum verified before it runs. The kickoff session confirms the licensing first: `gitleaks-action` needs a license key for organization repositories. If the CLI also needs a license, stop and report.
- **Coverage:** the PR commit range (`gitleaks git --log-opts="<base>..<head>"`), plus the PR body. The job writes the body to a temporary file and scans it with `gitleaks dir`. It does not scan Drive or any other external store.
- **False positives:** a reviewed `.gitleaksignore` entry (a fingerprint) with a one-line comment that gives the reason. CONTRIBUTING documents this process. Do not add blanket path or rule allowlists.

### A4. Tests

`tests/test_pr_policy.py` calls the script with synthetic event payloads and file lists. It covers these cases:

- a PR with no Recipe change
- a Recipe change where every heading is filled
- a missing heading
- an empty, comment-only section
- `Not applicable: planned`
- a PR edit event with a fixed body
- a promotion PR from `pre-prod` to `main`
- a catalog edit

The secret-scan test builds a fake token at runtime by joining strings, so the repository never holds one. The test runs `gitleaks` on that token and is skipped when the binary is not present. CI installs the binary, so the test runs there. Extend `tests/test_ci_workflow.py`: every workflow triggered by `pull_request` has only read permissions and no step that pushes or commits.

### A5. PR template and docs

- `.github/pull_request_template.md`: the template in source spec §4.2, with headings identical to Rule 1. Remove the Domain Bundle checkbox.
- `CONTRIBUTING.md` covers each point in source spec §4.3. Also:
  - Move "Accelerate Data contributors" (Drive and Domain Bundle) to a section called "Internal archive". Its first sentence says the archive is an author-side step and is not part of publication review. Keep the archival rule itself.
  - Rewrite "Branches" to match the D1 ruleset: one approval from someone other than the author, a new push dismisses stale approvals, required checks, and admin bypass by PR only.
  - Describe self-review in plain terms. Name `gtm-skills:reviewing-recipe` as an optional aid that Accelerate Data contributors can use. The checklist must make sense without the skill.
  - Link the schema and template. Do not copy their caps.
- `README.md`: `planned` Recipes are published and discoverable, but they are not invocable. Only `supported` and `proven` count toward Collection thresholds.

### A6. Track A deliverable

One PR to `pre-prod`. The PR body states two things: the ruleset change (Track D1) happens after the merge, and the consumer issue (Track D2) is linked once it exists.

## Track B: `gtm-skills/skills/reviewing-recipe/`

- Port the ZIP contents. Rename the directory, and set `name: reviewing-recipe` in the frontmatter.
- Rewrite `SKILL.md`, `references/review-rubric.md`, and `references/output-format.md` to cover source spec §3.1 to §3.3:
  - the 10-step workflow
  - Blocker, Warning, and Suggestion classes
  - the `PASS`, `PASS WITH WARNINGS`, and `CHANGES REQUIRED` verdicts, mapped to Approve and Request changes
  - the four required parts of every blocker
  - readiness evidence rules for `planned`, `supported`, and `proven`
  - the Linear duplicate check, with its scope stated when Linear is not reachable
  - no Drive access
  - no automatic fixes or posts

  Keep `SKILL.md` short and put the rules in the rubric. Delete the obsolete `APPROVE`/`CHANGES REQUESTED` logic. Do not keep it alongside the new rules.
- `agents/openai.yaml`: keep the original content, including `allow_implicit_invocation: true`. Keep `assets/icon.svg`.
- `tests/evals/eval_cases.py`: the 9 cases in source spec §3.4, written in the format the other skills in this repo use. The repo limit is 10 cases.
- Repository housekeeping, from `AGENTS.md`:
  - bump the Claude and Codex plugin manifests together to `0.14.0`, then run `npm run validate:plugin-manifests`
  - update `repo-map.json` and the skill list in `AGENTS.md`
  - run `npm run check:skill-prose-wraps` and `markdownlint`
- Deliverable: one PR to `main`.

## Track C: `vibedata-gtm` cookbook docs

Path: `docs/gtm/plan/04-demand-inbound/cookbook/`.

- `README.md` "Readiness": replace the table with the table in source spec §2.2, which states the evidence each state needs and whether it is invocable. Add the one-platform example rule (DuckDB first), and the rule that a platform listed without its own example needs a compatibility rationale.
- `README.md`: add a short "Publication review" section. It links to `vibedata-cookbooks` `CONTRIBUTING.md` and to `gtm-skills:reviewing-recipe`. It lists the three verdicts. Do not copy the rubric.
- `linear-backlog.md`: the lifecycle becomes Backlog → In Progress → In Review (PR open, latest verdict recorded on the issue) → Done (merged to `pre-prod`, with the Recipe URL and final readiness recorded). First read the live GTM team states. If there is no `In Review` state, record the verdict as an issue comment under In Progress. Do not create Linear states.
- Deliverable: one PR to `main`.

## Track D: external writes (checkpoints that need operator approval)

### D1. `pre-prod` ruleset (id `24733664`)

Apply this only **after** the Track A PR merges. The new check names must exist on `pre-prod` first, or every open PR blocks. Show the exact `gh api` PUT payload, and get approval before you run it.

| Parameter | Current | Target |
| --- | --- | --- |
| `required_approving_review_count` | 0 | 1 |
| `dismiss_stale_reviews_on_push` | false | true |
| `require_last_push_approval` | false | true |
| `require_code_owner_review` | false | false |
| required status checks | `Cookbook contract` | `Cookbook contract`, `PR policy`, `Secret scan` |
| bypass: RepositoryRole 5 (admin) | `always` | `pull_request` |
| bypass: Integration 5239200 (catalog app) | `always` | `always` |

Keep every other rule (deletion, non_fast_forward, merge methods). Do not change the `main` protection. After the PUT, read the ruleset back and record the live values in the Track A PR. Update `CONTRIBUTING.md` if the live values differ from the plan.

### D2. Consumer follow-up issue(s)

Draft a Linear issue with the §4.5 behavior:

- a `planned` Recipe is discoverable and readable
- it shows a `planned` label and the missing capabilities
- "Use Recipe" is hidden or disabled
- entries in `works_with.platforms` do not mean it is executable
- the Collection threshold logic does not change

Find which repositories own the website and the Studio discovery surface, and propose the team or project for each. Show the draft and get approval before you create anything. Link the created issue(s) in the Track A PR.

## Verification

| Check | Track |
| --- | --- |
| `pytest -q`, `build_catalog.py --validate`, `check_schema_versions.py` pass | A |
| A `planned` Recipe with no example passes `PR policy`; a `proven` Recipe with evals passes the tests; `proven` without evals fails the schema | A |
| The PR policy cases in A4 pass and fail as listed; the synthetic secret fails `gitleaks` | A |
| The Track A PR shows `PR policy` and `Secret scan` running, and both re-run after a body edit | A |
| No workflow triggered by a PR has write permission | A |
| Plugin manifests validate; prose-wrap and markdownlint pass; the eval suite runs | B |
| Each of the 9 eval cases produces its expected verdict in a dry run | B |
| markdownlint passes; links resolve | C |
| The ruleset read-back matches the D1 table | D |

## Out of scope

Everything in source spec §7. Also: implementing the consumer behavior, creating Linear workflow states, and changing `main` branch protection.
