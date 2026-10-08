---
id: database-tables-to-bronze
title: Load a database table set into bronze with a bounded incremental strategy and landed-data proof
trigger:
  - An operational database's tables have to land in bronze, and reloading every table in full on each run is too slow or too heavy on the source.
  - The tables change in different ways (rows updated in place, append-only events, small reference tables, deleted rows), so one load strategy does not fit them all.
  - Downstream teams need a table-by-table, run-by-run reconciliation of what landed in bronze against the source database before they build on it.
description: Build a dlt pipeline that lands a set of database tables into bronze, each loaded under its own approved strategy, with deletes, schema changes and failed runs handled as approved, and a per-run, table-by-table reconciliation of bronze against the source in which every difference has a cause.
pitch: Land a database's tables into bronze, each the way it changes, and reconcile every run against the source with a cause for every difference.
job_category: build
area: ingestion
readiness: supported
domain_objects:
  - dlt_pipeline
  - dlt_resource
  - bronze_table
  - reconciliation_report
works_with:
  platforms:
    - duckdb_local
    - motherduck
    - fabric_lakehouse
    - fabric_warehouse
    - redshift
  tools:
    - dlt
qualifiers:
  - Assessed end to end on duckdb_local only; the other listed targets rely on dlt support and are unassessed.
  - Studio's source setup cannot register a sql_database connection; it is declared with approval.
  - Replacing an existing managed connector belongs to managed-connector-to-dlt.
  - Log-based CDC replication is out of scope; each run selects changes by querying the source tables.
  - Needs read access to the source database, a key per merged table, and a change signal per incremental table.
related:
  - api-to-bronze-incremental-contract
  - managed-connector-to-dlt
evidence:
  features:
    - capturing-requirements
    - discovering-source-schema
    - generating-dlt-pipeline
    - dlt-unit-testing
    - running-dlt-in-sandbox
    - ingestion-data-testing
    - verifying
  evals: []
---

## Prompt

Build a dlt pipeline in the current Intent that lands <table_list> from the <source_database> database into bronze, loading each table in the way that table changes, incrementally wherever a full reload is not the approved strategy. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Select each run's records under the approved change and late-arrival rules, handle deletes, schema changes and timestamp and decimal types as approved, and make every run safe to repeat: a rerun with no source change leaves every record's content as it was, and a run that fails part-way resumes without losing or duplicating records. After every run, reconcile bronze against the source table by table, giving every difference a cause the approved rules allow, and report what each table's load mechanism cannot see and what a partial comparison scope cannot prove.

## Verified by

- Every approved table lands in bronze from the source database, each under its approved write disposition, key and change mechanism.
- Each later run loads the records the approved change mechanism selects, and records inside its approved late-arrival bound land; a rerun with no source change changes no record's content and neither duplicates nor loses a record.
- A record committed later than the approved bound covers is handled as the approved late-arrival rule says, and one that did not land is never claimed as landed.
- Deletes reach bronze as the approved policy says, whether kept and marked or removed; a deleted key that returns to the source is handled as approved, and the result states which deletes the chosen mechanism cannot see.
- A table without a change marker of its own picks up the changes its approved selection can see, and the result states the changes that selection would miss.
- A new source column and a changed column type are each handled as the approved schema policy says.
- Timestamps and decimals land as the approved type and time-zone rule says, and no value shifts or loses scale except as that rule allows.
- Each run's proof compares bronze with the source as of extraction, or under the approved timing rule, over the approved scope: counts, key sets both ways where keyed, values as the approved agreement rule says, and where each incremental table resumes. A difference without an allowed cause fails.
- A run that fails part-way leaves no table's resume point past records that never landed, and the next run lands every outstanding record exactly once.
- Delete, late-arrival, schema-change and failure behaviour the runs do not exercise is verified where an executable check exists; otherwise the gap is stated and correctness is not claimed for it.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements. Read the source database first: each table's key, the column that marks a change, whether rows are updated, appended or deleted, how a delete shows (a flag or timestamp, or the row erased), which tables depend on a parent for their change marker, and how timestamps and amounts are typed. Confirm the pipeline can read the database through a dlt database route; if Studio's source setup cannot configure it, say so and declare the connection directly only with approval. Choose each table's write disposition, key, change mechanism and late-arrival bound from source evidence and the approved requirements, and state what each relies on and would miss, such as rows committed late, rows erased outright, or child rows changed without their parent changing. Keep each table's resume point at or behind what has committed in bronze, so a failed run cannot skip records. Where a run re-reads records an earlier run landed, state how the chosen disposition keeps them from landing twice. Land into the Intent's approved bronze location without business transformation, run it over the approved runs, prove each run table by table against the source, and report the proof with what it cannot see.

### Compose

- capturing-requirements
- discovering-source-schema
- generating-dlt-pipeline
- dlt-unit-testing
- running-dlt-in-sandbox
- ingestion-data-testing
- verifying

### Ask first

- If unresolved, which tables are in scope, and how does each change: rows updated in place, appended only, a small reference table, rows deleted, or child rows that change through a parent?
- If unresolved by the source's evidence, which write disposition, key and change marker each table uses, where the first load starts, and how a table with no marker of its own is selected?
- If unresolved, how late may a record be committed relative to its change marker, what bound each run re-reads, and what happens to a record committed later than that bound covers?
- If unresolved, how does a delete reach the source, how should bronze show it (kept and marked, or removed), and what happens when a deleted key returns?
- If unresolved, what should the pipeline do when the source adds a column or changes a column's type?
- If unresolved, how should timestamps (which time zone, with or without one) and decimals (which scale) land in bronze?
- If unresolved, does each run's proof cover the full tables or an approved scope, must every value agree (exactly or after which normalisations), and how is a record changed after the run read it told apart from a defect?
- If unresolved, what must the next run do after a run that failed part-way, and may a failed run's unloaded work be discarded and re-read?

### Guardrails

- Do not choose or apply a load, late-arrival, delete, schema or type rule without approval.
- Do not write to the source database; read it only.
- Do not claim late or deleted records are handled when the chosen change mechanism cannot see them; state the gap.
- Do not edit source or landed data, widen a normalisation or drop a table from the proof to make it agree.
- Do not switch to file exports or full reloads in place of the approved database read without approval.
- Do not force business deduplication or transformation into the landed tables.
- Do not add a schedule or downstream models as part of this work.
