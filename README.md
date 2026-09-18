# VibeData Cookbooks

Public, canonical definitions for **materialized VibeData Recipes and Collections**.

A Recipe is one requirement-sized data-engineering outcome that a data engineer can adopt into an Intent. It contains the task specification, observable acceptance contract, and guidance the VibeData agent reads when the Recipe is invoked.

## Source ownership

The Cookbook uses two sources of truth for two different lifecycle stages:

- **Linear Cookbook project** — canonical backlog/lifecycle for Recipe candidates: <https://linear.app/acceleratedata/project/cookbook-fb2483d9868a/overview>
- **This repository** — canonical definition of Recipes and Collections once they are materialized.

The VibeData website and Studio consume the materialized catalog from this repository. They do not own separate Recipe registries.

## Execution model

A Recipe executes inside an existing Studio Intent.

```text
Recipe definition + current Intent context = execution
```

The Recipe does not require the engineer to restate environment, repository, Domain/project, platform, or source context that Studio already knows. Recipe metadata such as `works_with.platforms` is used for discovery and compatibility; it is not a set of invocation arguments.

Studio does not need a separate Recipe-execution Skill. Studio discovers/recommends a Recipe, then the normal agent reads the Recipe definition from this repository and executes it with the current Intent context and existing Features/Skills/tools.

## Three prompt concepts

These are deliberately separate:

1. **Website invocation pointer** — small copyable text that names the Recipe and canonical GitHub URL and tells the agent to read it in the current Intent context.
2. **Recipe `prompt`** — canonical task specification in the Recipe definition; explains what outcome the agent must deliver.
3. **`agent_guidance`** — canonical guidance for how the agent should approach execution.

The website may display the Recipe prompt and agent guidance for evaluation, but they are not the large copy/paste invocation payload.

## Repository layout

```text
recipes/<recipe-id>/recipe.json    canonical Recipe source
recipes/<recipe-id>/README.md      generated human/agent-readable page
collections/<collection-id>.json   canonical Collection source
schema/recipe.schema.json          Recipe contract
schema/collection.schema.json      Collection contract
scripts/build_catalog.py           validation + page/catalog generator
catalog.json                       generated machine-readable discovery index
```

`recipe.json` and Collection JSON files are authoritative. Generated `README.md` Recipe pages and `catalog.json` must not be hand-maintained.

Run:

```bash
python3 scripts/build_catalog.py
```

Use `--check` in CI/review to fail if generated output is stale:

```bash
python3 scripts/build_catalog.py --check
```

## Required Recipe fields

Every materialized Recipe requires:

- `id`
- `title`
- one or more `trigger` entries
- `description`
- `job_category`
- `area`
- `readiness`
- `prompt`
- one or more `verified_by` entries
- `agent_guidance.instructions`

Optional contextual metadata includes `function`, `industry`, `domain_objects`, compatible platforms/tools, qualifiers, related Recipes, and evidence.

## Readiness

- `proven` — a dedicated Recipe-level eval/journey proves the exact Recipe shape end to end.
- `supported` — current capabilities and supported objects can execute the Recipe end to end, without a dedicated Recipe-level eval for that exact shape.
- `planned` — at least one required capability, integration, or object type is unsupported today.

`scripts/build_catalog.py` enforces `proven` as a checkable claim rather than an unenforced convention: any Recipe with `readiness: "proven"` must declare at least one non-empty entry in `evidence.evals`, naming the eval/journey that proves it. A `proven` Recipe with an empty or missing `evidence.evals` fails both the plain build and `--check`.

## Platform compatibility

Current exact execution-target values are:

- `fabric_lakehouse`
- `fabric_warehouse`
- `motherduck`
- `duckdb`

There is no generic `fabric` execution value. Website discovery may group the two Fabric targets under one Microsoft Fabric Collection with All/Lakehouse/Warehouse views.

## Collections

Collections are non-executable discovery views over Recipes. They do not copy Recipe definitions.

Website publication thresholds:

- **Function Collection:** at least 3 materialized `supported`/`proven` Recipes.
- **Any non-function Collection:** at least 1 materialized `supported`/`proven` Recipe.
- `planned` Recipes do not count toward those thresholds.
- The six primary job categories are navigation, not Collections, and are not threshold-gated.

## Reference Recipe

The first complete reference Recipe is:

- [Convert a full-refresh dbt model to incremental and show the runtime delta](recipes/dbt-full-refresh-to-incremental/README.md)

It demonstrates the schema, multi-platform compatibility, Recipe prompt, acceptance contract, and mandatory agent guidance.
