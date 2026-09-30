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

## Adding a Recipe

1. Copy `templates/recipe.md` to `recipes/<id>/recipe.md`, where `<id>` is the Recipe's kebab-case id. The directory holds that one file.
2. Fill in the frontmatter and every body section.
3. Run the checks below and commit `recipe.md` together with the regenerated `catalog.json`.

## Accelerate Data contributors

This section applies to every new Recipe that an Accelerate Data employee writes.

1. Export the Domain you used to build the Recipe as a Domain Bundle: Domain Settings, General, **Export Domain**. Keep the Intents and their conversations selected. This step is compulsory.
2. Upload the bundle ZIP to the [Cookbooks Drive folder](https://drive.google.com/drive/folders/1CSXifZ4fH5GeNce-mpEeTtpENBSHpdP_), in a subfolder whose name is the Recipe `id`: `Cookbooks/<id>/`.
3. Optionally, add other artifacts you used to build the Recipe, such as notes, sample data or screenshots, to the same subfolder.
4. Upload before you open the pull request. Studio deletes a Domain Bundle 48 hours after the export.

The Drive folder is open to Accelerate Data accounts only.

## Frontmatter

Required keys: `id`, `title`, `trigger`, `description`, `job_category`, `area`, `readiness`, `works_with.platforms`. Optional keys: `pitch`, `function`, `industry`, `domain_objects`, `works_with.tools`, `qualifiers`, `related`, `evidence.features`, `evidence.evals`. Every string is one line. `schema/recipe.schema.json` holds the exact rules and length caps.

`works_with.platforms` uses Studio's own values: `duckdb_local`, `motherduck`, `fabric_lakehouse`, `fabric_warehouse`, `redshift`. There is no generic `fabric` value; a Recipe for both Fabric targets lists both.

`readiness` is `proven` only when a dedicated Recipe-level eval or journey proves the exact Recipe shape; name it in `evidence.evals`. `supported` means current capabilities can execute it end to end without such an eval. `planned` means at least one capability is missing today.

## Body

The body holds exactly these headings, in this order, and nothing else that starts with `#`:

| Heading | Content | Cap |
| --- | --- | --- |
| `## Prompt` | one paragraph on one line, no `\|` | 1200 characters |
| `## Verified by` | one acceptance condition per `- ` bullet | 1 to 12 bullets, 300 characters each |
| `## Agent guidance` | only the four subsections below | none |
| `### Instructions` | one paragraph on one line | 1500 characters |
| `### Compose` | one skill or Feature name per bullet; an advisory hint the cookbook does not check | 1 to 12 bullets, 80 characters each |
| `### Ask first` | one genuinely open question per bullet | 1 to 8 bullets, 300 characters each |
| `### Guardrails` | one Recipe-specific guardrail per bullet | 1 to 10 bullets, 300 characters each |

Bullets use `- ` only, never nested or indented, with no blank line inside a list. No line has leading or trailing whitespace. The whole file stays under 16384 bytes.

Nothing may escape its section: no HTML tags or comments, no HTML entities, no code fences, no control, zero-width or bidirectional characters. A `<` is allowed only to open a placeholder such as `<model_name>`, and a placeholder may not be an HTML element name or a tool-call word.

## Collections

A Collection in `collections/<id>.json` is a discovery view over Recipes: a `members` list of existing Recipe ids, a `selector` over Recipe metadata, or both. `schema/collection.schema.json` holds the rules.

## Branches

`pre-prod` is the default branch, so a new pull request already targets it. Every pull request to `pre-prod` must pass the `Cookbook contract` CI job; anyone with write access can merge it.

`main` is what readers follow. It takes changes only as a promotion: a pull request from `pre-prod` to `main`, merged with a merge commit, never a squash. Only `admiraldata`, `hbanerjee74` and `ukakkad` can merge it, and it must pass `Cookbook contract` and `Promotion source`. [ADR 0002](docs/adr/0002-branches-and-promotion.md) records the rules.

## Checks

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -q
.venv/bin/python scripts/build_catalog.py
.venv/bin/python scripts/check_schema_versions.py --base "$(git merge-base origin/pre-prod HEAD)"
```

`build_catalog.py` validates everything and rewrites `catalog.json`; CI runs it with `--check` and fails when the committed catalog is stale.

## Changing a schema

Each schema carries a top-level integer `version`. Raise it by exactly one for a breaking change: removing or renaming a field, making a field required, narrowing an enum, tightening a cap or pattern, or changing the body headings. Adding an optional field, widening an enum or raising a cap is not breaking and keeps the version. `check_schema_versions.py` enforces this in CI against the merge base, and treats any change it cannot prove is loosening as breaking. `catalog.schema.json` copies the Recipe and Collection properties exactly, so a change to either schema is made in `catalog.schema.json` too; a test fails when they drift. Changing a prose file or line rule (the encoding and trailing-newline rule, the bullet or paragraph rule, the no-surrounding-whitespace rule, or what may precede `## Prompt`) is also breaking and raises the Recipe schema version; `check_schema_versions.py` treats any edit inside a `# format-rules` region of `scripts/recipe_format.py` or `scripts/build_catalog.py` as one.
