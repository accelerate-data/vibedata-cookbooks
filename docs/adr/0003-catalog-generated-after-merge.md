# 3. Catalog generated after merge

- Status: Proposed
- Date: 2026-10-08

## Context

Every Recipe pull request committed a regenerated `catalog.json` and appended its id to one shared `EXPECTED` dictionary in `tests/test_published_recipes.py`. Both files change for every new Recipe, so whichever of several pending Recipe pull requests merged second conflicted on both. Fixing that meant merging `pre-prod` into the branch, keeping every id and regenerating the catalog. On 2026-10-08 four Recipe pull requests were open at once, and #44 needed that fix after #45 and #47 merged. The Recipe files themselves never conflicted, because each lives in its own directory.

## Decision

1. **Pull requests do not edit `catalog.json`.** `scripts/build_catalog.py --validate` checks every Recipe and Collection and builds the catalog in memory, without writing or comparing the committed file. Pull requests to `pre-prod` run it.
2. **The catalog is regenerated after merge.** The `Catalog` workflow (`.github/workflows/catalog.yml`) runs on every push to `pre-prod`, regenerates `catalog.json` and commits it as the `vibedata-cookbooks-catalog` GitHub App when it changed. Runs are serialised. When a newer merge lands first, the older run exits, because the newer run regenerates the catalog.
3. **`main` still receives a fresh, committed catalog.** CI runs `--check` on pull requests and pushes to `main`, so a promotion fails if `pre-prod`'s catalog is stale. Readers keep fetching `catalog.json` from `main` at the same path and in the same format (ADR 0001).
4. **Agreed Recipe values live in one file per Recipe.** The shared `EXPECTED` dictionary is replaced by `tests/expected/<id>.json`, holding the Recipe's agreed `readiness` and `platforms`. The inventory test compares those files with a catalog built in memory, so an unreviewed change to a Recipe's readiness or platforms, or a Recipe without its file, still fails.

## Consequences

- Two pull requests that add different Recipes touch no common file.
- For about a minute after each merge, `pre-prod`'s committed catalog lags until the workflow commits. `main` is unaffected, because it changes only on promotion.
- The workflow pushes to `pre-prod` directly with a token from the `vibedata-cookbooks-catalog` GitHub App (Contents: write, installed on this repository only). The `pre-prod` ruleset lists the App as a bypass actor. The App's client ID is the `CATALOG_APP_CLIENT_ID` variable and its private key the `CATALOG_APP_PRIVATE_KEY` secret. If the push fails, the next promotion's `--check` reports the stale catalog.
- A push by the App starts workflows, so CI and the `Catalog` workflow run again on the bot's commit. The second `Catalog` run finds the catalog fresh and exits.
- `CONTRIBUTING.md`, the README and the pull request template now describe the new steps.

## Alternatives considered

- **A `.gitattributes` merge driver for `catalog.json`.** Rejected: GitHub's conflict detection and merge button ignore custom merge drivers, so the conflicts would still appear on pull requests.
- **Keeping `EXPECTED` sorted.** Rejected: it spreads insertions, but two Recipes with neighbouring ids still conflict.
- **Publishing the catalog only as a build artifact (Pages or a release asset).** Rejected for now: readers would have to change where they fetch it.
