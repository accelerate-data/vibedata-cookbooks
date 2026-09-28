# VibeData Cookbooks

Public, canonical definitions for **materialized VibeData Recipes and Collections**.

A Recipe is one requirement-sized data-engineering outcome that a data engineer can adopt into an Intent. It contains the task specification, an observable acceptance contract, and guidance the VibeData agent reads when the Recipe is invoked.

## Source ownership

- **Linear Cookbook project**: canonical backlog and lifecycle for Recipe candidates: <https://linear.app/acceleratedata/project/cookbook-fb2483d9868a/overview>
- **This repository**: canonical definition of Recipes and Collections once they are materialized.

The VibeData website and Studio consume the materialized catalog from this repository. They do not own separate Recipe registries. The served identity of a Recipe is the Git commit a reader fetched; the catalog carries no revision of its own.

## Execution model

A Recipe executes inside an existing Studio Intent.

```text
Recipe definition + current Intent context = execution
```

The Recipe does not require the engineer to restate environment, repository, Domain, platform, or source context that Studio already knows. `works_with.platforms` is used for discovery and compatibility; it is not a set of invocation arguments.

## Three prompt concepts

1. **Website invocation pointer**: small copyable text that names the Recipe and its path and tells the agent to read it in the current Intent context.
2. **The Recipe's `## Prompt`**: the canonical task specification; what outcome the agent must deliver.
3. **The Recipe's `## Agent guidance`**: how the agent should approach execution.

The website may display the prompt and guidance for evaluation, but they are not the copy-and-paste invocation payload.

## Repository layout

```text
recipes/<recipe-id>/recipe.md      canonical Recipe: YAML frontmatter + Markdown body
collections/<collection-id>.json   canonical Collection
schema/recipe.schema.json          Recipe frontmatter contract, with the body rules under x-body
schema/collection.schema.json      Collection contract
schema/catalog.schema.json         catalog.json contract
scripts/build_catalog.py           validation + catalog generator
scripts/check_schema_versions.py   schema version-bump check
catalog.json                       generated metadata-only discovery index
templates/recipe.md                starting point for a new Recipe
```

`recipe.md` and the Collection files are authoritative. `catalog.json` is generated and must not be edited by hand. It holds each Recipe's metadata plus its `path` and `sha256`, never the prompt, acceptance conditions or guidance; readers fetch `recipe.md` for those. `schema_versions` records the schema versions the catalog was built against.

## Checks

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -q
.venv/bin/python scripts/build_catalog.py --check
```

Run `scripts/build_catalog.py` without `--check` to regenerate `catalog.json`. CI (`.github/workflows/ci.yml`) runs the tests, the `--check` build and the schema version-bump check on every pull request and every push to `pre-prod` and `main`. Work lands on `pre-prod`, the default branch; `main` takes only promotions from `pre-prod`. See [CONTRIBUTING.md](CONTRIBUTING.md#branches).

## Platforms

Exact execution-target values, shared with Studio: `duckdb_local`, `motherduck`, `fabric_lakehouse`, `fabric_warehouse`, `redshift`. There is no generic `fabric` value; the website may group the two Fabric targets under one Microsoft Fabric Collection with All, Lakehouse and Warehouse views.

## Readiness

- `proven`: a dedicated Recipe-level eval or journey proves the exact Recipe shape end to end, named in `evidence.evals`. The schema rejects `proven` without one.
- `supported`: current capabilities can execute the Recipe end to end, without a dedicated Recipe-level eval.
- `planned`: at least one required capability, integration or object type is unsupported today.

## Collections

Collections are non-executable discovery views over Recipes; they never copy Recipe definitions and may name only Recipes that exist. Website publication thresholds: a function Collection needs at least 3 `supported` or `proven` Recipes, any other Collection at least 1; `planned` Recipes do not count.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) and the Recipe template in [templates/recipe.md](templates/recipe.md). The contract is recorded in [ADR 0001](docs/adr/0001-cookbook-recipe-contract.md).

## Recipes

- [Convert a full-refresh dbt model to incremental and show the runtime delta](recipes/dbt-full-refresh-to-incremental/recipe.md)
- [Land a SaaS or REST API into bronze with an incremental cursor and a schema contract](recipes/api-to-bronze-incremental-contract/recipe.md)
- [Author a Fabric Data Pipeline that sequences ingestion, dbt, and downstream refresh as committed code](recipes/fabric-data-pipeline-as-code/recipe.md)
- [Schedule a dlt load and a dbt build on MotherDuck as a committed MotherDuck Flight](recipes/motherduck-flight-scheduling/recipe.md)

## License

Elastic License 2.0. See [LICENSE](LICENSE).
