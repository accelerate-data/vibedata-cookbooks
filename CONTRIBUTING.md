# Contributing a Recipe

A Recipe is one requirement-sized data-engineering outcome a data engineer adopts into a Studio Intent. This guide covers what belongs here, the Recipe file, and the checks every change must pass. The contract itself is recorded in [ADR 0001](docs/adr/0001-cookbook-recipe-contract.md).

## Feature or Recipe

A candidate is a **Feature**, not a Recipe, when one direct operation or one skill contract is the whole job: testing a source connection, registering a source, adding one test, running a change in isolation, comparing a relation against a baseline, enforcing a contract, or explaining one number. Features are reached by asking for them, and listing one as a Recipe would suggest it needs a Recipe to work.

A candidate is a **Recipe** when it is one recognizable engineering requirement that composes several capabilities or needs real design or modelling judgment, and has its own acceptance behaviour. Every Recipe proves itself: its tests, sandbox runs and comparisons belong in its own `Verified by` section, never in a second Recipe.

## The shape of a Recipe

- **Title:** the literal deliverable, the thing the engineer ends up with, not a slogan.
- **Trigger:** one or more situations, written separately from the title, in which an engineer would reach for the Recipe.
- **Description and pitch:** the bounded outcome in one line, and an optional one-sentence pitch for hero cards.
- **Prompt:** the paste-and-adapt task. Values the engineer adapts are `<lower_snake_case>` placeholders. Never ask for context Studio already knows, such as the platform, the repository or the Domain.
- **Agent guidance:** instructions, composed skills, genuinely open questions and guardrails. The agent reads it; the invocation surface does not show it as the prompt.

## Evidence for a Recipe

The PR description carries the evidence, using the PR template in `.github/pull_request_template.md`. Do not add new evidence files to the repository.

- **One example is enough.** Run the example on one platform. Use `duckdb_local` when the outcome can run there, and another platform only when DuckDB cannot support the outcome. Do not build an example for every declared platform.
- **Other platforms need reasoning, not examples.** For each declared platform, the PR gives the execution path that makes it compatible, says whether you assessed it, and records any limitation.
- **The example must show the defining behaviour.** An example that skips the core promised behaviour does not support the readiness claim. Fix the example, not the contract.
- **The contract carries the correctness rules.** `Verified by` states properties of a correct outcome, not an instruction to run tools. Where the Recipe defines business logic, it describes independent expected results, so a check never repeats the implementation's own calculation. `Ask first` names the types of business decision the agent must settle with the user, such as eligibility, time boundaries or tolerances, and never invents the answers. The Recipe describes honest exceptional states: partial work is never reported as complete. `Guardrails` cover the risks that apply to this outcome, such as silent data loss, join fan-out, wrong grain, late records, deletes, reruns and unsafe mutations.
- **Public content only.** Do not put secrets or sensitive customer data in a Recipe or in the PR. Do not link Drive content as evidence.

## Self-review before you request review

Run the checks below, then review your own change against the PR template's author checklist. In plain terms, confirm that:

1. The Recipe is one bounded outcome with its own acceptance behaviour, not a Feature, a Skill (knowledge the agent applies about tools, platforms and techniques), a Guarantee (cross-cutting Vibedata behaviour that Recipes inherit), a Collection or a duplicate of an existing Recipe. The [Cookbook ontology](https://github.com/accelerate-data/vibedata-gtm/blob/main/docs/gtm/plan/04-demand-inbound/cookbook/README.md) defines these terms.
2. Each `Verified by` bullet states an observable property of a correct result, and defining business logic has an independent expected result.
3. `Ask first` lists the policy decisions the agent must not settle alone, and the Recipe inherits context that Studio already knows.
4. `Guardrails` cover the real risks of this outcome and nothing generic.
5. The `readiness` value and the platform list match what the PR evidence shows.

Accelerate Data contributors can optionally run the `gtm-skills:reviewing-recipe` skill as an aid. The checklist above stands without it.

## How review works

A reviewer reads the public Recipe files and the PR description only. The reviewer does not inspect Drive, a Domain Bundle or any other private source. A new or changed Recipe gets a full review. A re-review after new commits focuses on what changed and on regressions.

Each finding has one class:

- **Blocker:** a defect in the reusable contract, unsafe behaviour, a misleading readiness or capability claim, a `supported` or `proven` example that does not show the core outcome, or missing material evidence in the PR.
- **Warning:** a valid, disclosed limit, such as a compatible platform you did not test.
- **Suggestion:** a non-material editorial improvement.

The review ends with one verdict:

- `PASS`: no blockers and no material warnings.
- `PASS WITH WARNINGS`: no blockers. The PR discloses the remaining limits.
- `CHANGES REQUIRED`: at least one blocker.

`PASS` and `PASS WITH WARNINGS` lead to an approval, and `CHANGES REQUIRED` leads to a request for changes. The approval itself comes from a human reviewer.

## Adding a Recipe

1. Copy `templates/recipe.md` to `recipes/<id>/recipe.md`, where `<id>` is the Recipe's kebab-case id. The directory holds that one file.
2. Fill in the frontmatter and every body section.
3. Add `tests/expected/<id>.json` with the Recipe's agreed `readiness` and `platforms`.
4. Run the checks below and commit `recipe.md` and `tests/expected/<id>.json`. Do not commit `catalog.json`: a workflow regenerates it after the pull request merges to `pre-prod` ([ADR 0003](docs/adr/0003-catalog-generated-after-merge.md)).

## Internal archive

The archive is an author-side step for Accelerate Data employees. It is not part of publication review: CI and reviewers never check it, and review never depends on it.

Every new Recipe that an Accelerate Data employee writes has this archive step.

1. Export the Domain you used to build the Recipe as a Domain Bundle: Domain Settings, General, **Export Domain**. Keep the Intents and their conversations selected. This step is compulsory.
2. Upload the bundle ZIP to the [Cookbooks Drive folder](https://drive.google.com/drive/folders/1CSXifZ4fH5GeNce-mpEeTtpENBSHpdP_), in a subfolder whose name is the Recipe `id`: `Cookbooks/<id>/`.
3. Optionally, add other artifacts you used to build the Recipe, such as notes, sample data or screenshots, to the same subfolder.
4. Upload before you open the pull request. Studio deletes a Domain Bundle 48 hours after the export.

The Drive folder is open to Accelerate Data accounts only.

## Frontmatter

Required keys: `id`, `title`, `trigger`, `description`, `job_category`, `area`, `readiness`, `function`, `works_with.platforms`. Optional keys: `pitch`, `industry`, `domain_objects`, `works_with.tools`, `qualifiers`, `related`, `evidence.features`, `evidence.evals`. Every string is one line. [`schema/recipe.schema.json`](schema/recipe.schema.json) holds the exact rules and length caps, and [`templates/recipe.md`](templates/recipe.md) is the starting file.

`works_with.platforms` uses Studio's own values: `duckdb_local`, `motherduck`, `fabric_lakehouse`, `fabric_warehouse`, `redshift`. There is no generic `fabric` value; a Recipe for both Fabric targets lists both.

`readiness` has three values:

- `planned`: at least one required capability is missing today. A `planned` Recipe can be published and is discoverable, but Studio does not offer it as executable. It needs a complete reusable contract, and it needs no execution evidence. The PR names the missing capability. Platforms listed for a `planned` Recipe are intended targets, not a claim that it runs today.
- `supported`: current capabilities can execute it end to end. The PR shows one end-to-end execution of the defining outcome, with representative verification.
- `proven`: `supported` evidence plus a dedicated, repeatable Recipe-level eval or journey, named in `evidence.evals`. The schema rejects `proven` without one.

## Body

The body holds exactly these headings, in this order, and nothing else that starts with `#`:

- `## Prompt`: one paragraph on one line, no `|`.
- `## Verified by`: one acceptance condition per `- ` bullet.
- `## Agent guidance`: only the four subsections below.
- `### Instructions`: one paragraph on one line.
- `### Compose`: one skill or Feature name per bullet; an advisory hint the cookbook does not check.
- `### Ask first`: one genuinely open question per bullet.
- `### Guardrails`: one Recipe-specific guardrail per bullet.

[`schema/recipe.schema.json`](schema/recipe.schema.json) holds the bullet counts and length caps.

Bullets use `- ` only, never nested or indented, with no blank line inside a list. No line has leading or trailing whitespace. The whole file stays under 16384 bytes.

Nothing may escape its section: no HTML tags or comments, no HTML entities, no code fences, no control, zero-width or bidirectional characters. A `<` is allowed only to open a placeholder such as `<model_name>`, and a placeholder may not be an HTML element name or a tool-call word.

## Collections

A Collection in `collections/<id>.json` is a discovery view over Recipes: a `members` list of existing Recipe ids, a `selector` over Recipe metadata, or both. `schema/collection.schema.json` holds the rules.

Every `function` value a Recipe uses needs a `kind: function` Collection whose selector names it, and a Recipe id that starts with `finance-`, `people-`, `revops-`, `ops-` or `service-` must carry the matching function (`finance`, `people`, `revops`, `supply-chain-ops`, `service`). `build_catalog.py --validate` fails otherwise. Every Recipe must carry at least one `function`, because the website's domain row lists Recipes by function. Use `cross-functional` (shown as Any domain) when no single business function consumes the outcome; a Recipe that serves two functions lists both. A function Collection shows on the website once it holds three supported or proven Recipes.

## Branches

`pre-prod` is the default branch, so a new pull request already targets it. A pull request to `pre-prod` needs:

- one approval from someone other than the author;
- a fresh approval after a new push: a push dismisses earlier approvals, and the last push needs an approval from someone other than the pusher;
- passing checks `Cookbook contract`, `PR policy` and `Secret scan`.

On a first-time contributor's fork pull request, the required checks wait until a maintainer approves the workflow run.

Repository admins can bypass these rules only through a pull request, and GitHub records each bypass. The catalog GitHub App keeps its bypass so that it can push the regenerated `catalog.json` after a merge. CI only reads the repository. The `Catalog` workflow is the only job that writes, and it writes `catalog.json` only.

`main` is what readers follow. It takes changes only as a promotion: a pull request from `pre-prod` to `main`, merged with a merge commit, never a squash. Only `admiraldata`, `hbanerjee74` and `ukakkad` can merge it, and it must pass `Cookbook contract` and `Promotion source`. [ADR 0002](docs/adr/0002-branches-and-promotion.md) records the promotion rules.

## Secret scan false positives

`Secret scan` scans the pull request commits and the PR description. If it reports a reviewed false positive, add its fingerprint to `.gitleaksignore` with a one-line `#` comment above it that gives the reason. Reviewers read that entry like any other change. Do not add a blanket path or rule allowlist. If a secret was pushed or pasted, rotate it: deleting the commit or editing the description does not remove it from GitHub history.

## Checks

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -q
.venv/bin/python scripts/build_catalog.py --validate
.venv/bin/python scripts/check_schema_versions.py --base "$(git merge-base origin/pre-prod HEAD)"
```

`build_catalog.py --validate` checks every Recipe and Collection without touching `catalog.json`; pull requests to `pre-prod` run it. Without a flag it rewrites `catalog.json`, which the `Catalog` workflow does after each merge to `pre-prod`. CI runs `--check` only on pull requests and pushes to `main`, so `main` always receives a fresh catalog.

## Changing a schema

Each schema carries a top-level integer `version`. Raise it by exactly one for a breaking change: removing or renaming a field, making a field required, narrowing an enum, tightening a cap or pattern, or changing the body headings. Adding an optional field, widening an enum or raising a cap is not breaking and keeps the version. `check_schema_versions.py` enforces this in CI against the merge base, and treats any change it cannot prove is loosening as breaking. `catalog.schema.json` copies the Recipe and Collection properties exactly, so a change to either schema is made in `catalog.schema.json` too; a test fails when they drift. Changing a prose file or line rule (the encoding and trailing-newline rule, the bullet or paragraph rule, the no-surrounding-whitespace rule, or what may precede `## Prompt`) is also breaking and raises the Recipe schema version; `check_schema_versions.py` treats any edit inside a `# format-rules` region of `scripts/recipe_format.py` or `scripts/build_catalog.py` as one.
