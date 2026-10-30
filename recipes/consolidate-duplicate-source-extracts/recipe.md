---
id: consolidate-duplicate-source-extracts
title: Consolidate overlapping extracts of one source table into a shared feed and per-team projections
trigger:
  - Several downstream teams each pull their own extract of the same source table, each with its own filter, cursor, delete handling and cutoff, so the source is read repeatedly.
  - When an extract drifts nobody can say whose output is right, and the old extracts have to stay in place until each team has proof.
  - A measured number is needed for how many source reads one shared feed saves, and a written, bounded plan for moving each team over.
description: Land one shared feed of the source table through one row pass per run, build one explicit projection per team that reproduces that team's approved baseline per key and column, prove replay and the counted read saving, and plan each team's cutover and recovery in writing.
pitch: Consolidate overlapping extracts into one shared feed and per-team projections that match each baseline, with reads counted and cutover planned.
job_category: re-engineer
area: ingestion
readiness: supported
function:
  - cross-functional
domain_objects:
  - shared_landed_feed
  - team_projection
  - extract_baseline
  - behaviour_register
  - read_saving_report
  - cutover_plan
works_with:
  platforms:
    - duckdb_local
    - motherduck
    - fabric_lakehouse
    - fabric_warehouse
    - redshift
  tools:
    - dlt
    - dbt
qualifiers:
  - Needs read access to the source table, a stable key, and a change signal or an approved full read.
  - Studio's source setup cannot register a sql_database connection; it is declared with approval.
  - Stops at the feed, projections, proof and a written plan; switching off or repointing extracts is out of scope.
  - Replacing a managed connector belongs to managed-connector-to-dlt.
  - Landing a table with no team extracts to reproduce belongs to database-tables-to-bronze.
  - Extracts that are models over an already-landed table belong to dbt-refactor-output-identical.
  - Log-based CDC replication is out of scope; each run reads the source table.
related:
  - database-tables-to-bronze
  - managed-connector-to-dlt
  - dbt-refactor-output-identical
  - versioned-data-contract-cutover
  - cross-platform-live-reconciliation
  - batch-cdc-current-state
evidence:
  features:
    - capturing-requirements
    - generating-dlt-pipeline
    - generating-dbt-model
    - ingestion-data-testing
    - verifying
  evals: []
---

## Prompt

Consolidate the overlapping extracts <extract_list> of <source_table> into one shared landed feed read in one row pass per run, plus any approved key-level pass, and one explicit projection per consuming team that gives that team back its approved baseline output. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Land the rows any team needs at the approved grain, covering every team's rule, handle deletes as approved (normally kept as marked rows), and record each run's source reads and freshness. Build each projection from the feed with that team's own selection, delete and historical-cutoff rules, never merging populations that differ. Class every behaviour of each extract as kept, changed on purpose with approval, or not supported, and keep an inherited quirk in the baseline, listed. Prove each projection against its own baseline per key and column, prove that a run that fails part-way and is replayed loses and duplicates no record, measure the source reads before and after, and write each team's cutover and recovery plan without switching off an extract or repointing a team.

## Verified by

- The feed holds rows at the approved grain (one per key at latest state, or versions), each column at a precision that reproduces every baseline, and every row any team's rules need; each run records its row pass, any key-level pass and each team's freshness against its approved expectation.
- Each projection equals its team's approved baseline per key and per column in both directions, with nulls as values, apart from approved differences listed with both values, against expected outputs derived independently from the extract definitions and source; matching counts or totals never pass.
- Populations that differ stay apart: each projection applies its own approved selection and cutoff, and a row one team needs and another's filter excludes, or one older than a team's cutoff, appears only where that team's approved rules put it.
- A delete the approved detection sees stays in the feed as a marked row with its basis unless an approved erasure removes it, counted, and each projection follows its team's rule; a delete the detection cannot see is stated as unproven, never claimed absent.
- A change inside the feed's lookback but outside a team's narrower one follows the approved rule; any difference from the baseline appears only as a listed approved difference per key and column, and the baseline is never edited.
- A source change the cursor cannot pick up follows the approved rule (re-read and counted, or counted per run as declared missed and never reported as current); a change the run cannot see is stated as unproven.
- Every behaviour of each extract is classed as kept, changed on purpose with named approval, or not supported; an inherited quirk stays in its baseline and is listed, and one that cannot be determined stays visible as unknown.
- A run that fails part-way and is replayed leaves every record once in the feed and in every projection, equal to an independent uninterrupted reference; a rerun with no source change adds, changes and duplicates nothing.
- Each run accounts for every source row read as inserted, updated, unchanged, marked deleted or set aside with its reason, and the counts foot to keys counted independently, not to the run's own totals.
- Source reads before and after are reported as rows read and key-level reads separately, signed, so no saving or an increase can show; before reads come from observed extract runs or, where unavailable, their definitions, labelled derived; other readings never feed the result.
- Each team's plan states preconditions, dual-run, switch order and rollback as approved, and how data is restored as approved, with what that restore cannot recover; a code revert alone is never offered as data recovery.
- The existing extracts stay in place and unchanged and no team is repointed; a team whose approved difference or freshness expectation is unmet is shown as not ready to cut over.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements. Read each extract's written definition and approved baseline first, with its selection, cursor and lookback, delete handling, historical cutoff, freshness expectation, time zones and column typing, and discover the source table's schema and types, and find where the teams' populations and rules overlap and where they differ. If the source has no stable key or change signal, or a baseline or definition is missing, stop and raise it; do not infer one. Write the expected baseline outputs by hand from the definitions and source before any pipeline code, and compare built to expected per key and column. Land the feed through a supported dlt route without team filters, derive each projection in the models from the feed under that team's rules, and keep team rules as data the models read. Where a team's rule cannot be reproduced from the shared feed, say so and ask rather than widening or editing the baseline. State which conditions the run does not exercise, such as an erased row or a failure point, and what the read cannot see.

### Compose

- capturing-requirements
- discovering-source-schema
- generating-dlt-pipeline
- generating-dbt-model
- ingestion-data-testing
- verifying

### Ask first

- If unresolved, which extracts and consuming teams are in scope, what each baseline output holds (keys, columns, types, window), and who can confirm each extract's real read pattern for the saving?
- If unresolved, what is the feed's grain (one row per key at its latest state, or versions), which rows, columns and precision must it hold so every team's rules can be met, and does a team whose population differs keep its own projection?
- If unresolved, what shared cursor and lookback cover the widest team rule, and where a narrower team lookback would have kept an older value, is that staleness preserved or corrected with that team's acceptance?
- If unresolved, how does each team treat deleted rows (flagged, removed, erased), what basis marks a delete, and how is a row erased without a trace treated, and must a legal erasure also leave the feed?
- If unresolved, how are rows with a missing or duplicate key or an invalid value, a change the cursor cannot pick up, and a source schema or type change treated (set aside, re-read, evolve or fail), and how are inherited quirks and unknown behaviours classed?
- If unresolved, what freshness does each team expect, in which time zone and how measured, and must the feed's cadence satisfy the tightest team?
- If unresolved, after a run fails part-way, is it resumed or discarded and re-read, and how is data restored (re-land, snapshot or retained outputs) when the feed or a projection is wrong?
- If unresolved, which reads count toward the saving (rows, key-level reads, calls), and what cutover window, switch order and rollback applies to each team?

### Guardrails

- Do not merge populations that differ into one projection, or force one team's rules on another.
- Do not edit a baseline or silently fix an inherited quirk; a correction needs approval and is listed apart.
- Do not drop a delete the approved detection sees from the feed without an approved erasure; mark it with its basis and let each projection apply its team's rule.
- Do not report a missed, late or erased row as current or as absent when the read cannot see it.
- Do not accept equal row counts or one matching total as parity between a projection and its baseline.
- Do not derive expected outputs from the feed, projections or pipeline they check.
- Do not switch off, alter or repoint an existing extract, or delete anything in the source.
- Do not present a code revert as data recovery, or claim a saving beyond the reads measured.
- Do not call a team ready to cut over while its approved difference or freshness expectation is unmet.
- Do not replace a managed connector or load tables beyond the source table in scope.
