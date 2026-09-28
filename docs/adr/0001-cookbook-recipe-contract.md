# 1. Cookbook Recipe contract

- Status: Accepted
- Date: 2026-09-25
- Issue: VD-6115

## Context

Recipes were JSON even though most of each one is guidance written by people and read by agents. The catalog embedded a second full copy of every Recipe and had no schema, neither schema had a version, the hand-written catalog revision always named an earlier commit, platform names differed from Studio's, and a Recipe could omit its platforms. Consumers had to guess the contract, and Studio's Recipe discovery (VD-6112) returned nothing as a result.

## Decision

1. **Markdown Recipes with schema-validated frontmatter.** Each Recipe is `recipes/<id>/recipe.md`: YAML frontmatter validated by `schema/recipe.schema.json`, then a body with a closed, required set of headings (`## Prompt`, `## Verified by`, `## Agent guidance` with `### Instructions`, `### Compose`, `### Ask first`, `### Guardrails`). The prompt is one paragraph that fits a table cell, each acceptance condition is one bullet, every field has a length cap, and markup that could escape its section is rejected. The body and markup rules are published as data under `x-body` in the Recipe schema, so every validator applies the same rules.
2. **A generated, metadata-only catalog.** `scripts/build_catalog.py` generates `catalog.json` from frontmatter alone. Entries are sorted by id, regeneration is byte-stable, and each entry carries the Recipe file's `path` and `sha256`. The catalog holds no prompt, acceptance conditions or guidance; `evidence` stays because it backs the `proven` claim. `schema/catalog.schema.json` validates it, and Collections may name only existing Recipes.
3. **Versioned schemas published with the catalog.** Each schema carries a top-level integer `version`, raised by one only for a breaking change. The catalog records `schema_versions`. CI compares each schema with the merge base and fails a breaking change without a bump, or a bump without a breaking change. The prose file and line rules (UTF-8, LF, no BOM and exactly one trailing newline; the bullet line rule; the paragraph rule; no leading or trailing whitespace on body lines; nothing but blank lines before `## Prompt`) are not `x-body` data, so readers hard-code them: changing any of them is breaking and raises the Recipe schema version, and the version check treats an edit inside a `# format-rules` region of `scripts/recipe_format.py` or `scripts/build_catalog.py` as such a change.
4. **The Git commit is the served identity.** The hand-written `revision` is removed. A reader reports the commit it fetched; the schema version only says whether it can parse what it fetched.
5. **Studio's platform values.** `works_with.platforms` is required and uses `duckdb_local`, `motherduck`, `fabric_lakehouse`, `fabric_warehouse` and `redshift`, so no mapping exists anywhere. `compose` stays an advisory hint the cookbook does not validate.

## Consequences

- Readers fetch `recipe.md` at the catalog's commit for the body and can verify it against `sha256`.
- The catalog no longer carries `canonical_url`; a consumer derives a link from `source` and `path`.
- Adding an optional frontmatter field is not breaking, but it touches both `recipe.schema.json` and `catalog.schema.json`, whose copies a test keeps identical.
- The caps were set from the published Recipes with headroom; a legitimate Recipe that hits one raises the cap, which is not a breaking change.
- Signed releases and release tags stay out of scope; readers keep following `main`. Branches and protection are recorded in [ADR 0002](0002-branches-and-promotion.md).
- Markup rules apply to frontmatter values, not to YAML comments. A comment is stripped by the parser before the frontmatter becomes fields, so it never reaches the catalog or a reader's parsed Recipe; this is an accepted limitation, and it must be revisited if a reader ever serves raw frontmatter text verbatim.

## Alternatives considered

- **Keep JSON Recipes.** Rejected: guidance written as escaped JSON strings is hard to author and review, and the body is what people and agents read.
- **Embed Recipe bodies in the catalog.** Rejected: two copies drift, and the catalog is a discovery index, not a distribution format.
- **Keep a revision field in the catalog.** Rejected: a file cannot name the commit that contains it, so it always named an earlier one.
- **Semantic-version strings for schemas.** Rejected: readers only need to know whether they can parse a schema, which one integer says.
