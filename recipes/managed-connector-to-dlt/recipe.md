---
id: managed-connector-to-dlt
title: Replace a Fivetran or Airbyte connector with a dlt pipeline and reconcile the result
trigger:
  - A managed connector's bill changed shape, or it broke and the vendor fix has been pending for weeks, and the team wants the load in code it owns.
  - dbt models read a Fivetran or Airbyte connector's tables, so a replacement has to keep landing data those models can use.
  - Before switching off a managed connector, the team needs proof that its replacement lands the same records, with a reason for every difference.
description: Replace a managed connector with an owned dlt pipeline landed side by side with the connector's tables, reconciled table by table over parallel runs with a cause for every difference, and stopped short of cutover.
pitch: Swap a Fivetran or Airbyte connector for a dlt pipeline you own, and prove table by table that it lands what the connector did before you cut over.
job_category: re-engineer
area: ingestion
readiness: supported
domain_objects:
  - managed_connector
  - dlt_pipeline
  - bronze_table
  - consumer_contract
  - reconciliation_report
  - cutover_readiness
works_with:
  platforms:
    - duckdb_local
  tools:
    - dlt
    - dbt
qualifiers:
  - Complete outcome assessed for duckdb_local only; the other four Studio targets remain unassessed.
  - Needs read access to the connector's landed tables and to the source the connector reads.
  - Database sources need a dlt route Studio supports; its sql_database route is not supported today.
related:
  - api-to-bronze-incremental-contract
  - legacy-sql-to-dbt
  - prove-dbt-change-safe
evidence:
  features:
    - capturing-requirements
    - add-or-update-source
    - discovering-source-schema
    - generating-dlt-pipeline
    - dlt-unit-testing
    - running-dlt-in-sandbox
    - ingestion-data-testing
    - verifying
  evals: []
---

## Prompt

Replace the <connector_name> connector that lands <source_name> into <connector_schema> with a dlt pipeline in the current Intent, so that <consumers> can later move to it. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Land the approved tables with dlt beside the connector's tables without changing them, present them to consumers in the approved shape, run both loads in parallel over the approved runs, and reconcile them table by table, giving every difference a cause, from the approved list where that list is closed. Report cutover readiness and what the reconciliation cannot prove; leave the connector running and consumers unchanged.

## Verified by

- Every approved table is landed by the dlt pipeline next to the connector's tables, and neither load overwrites the other.
- The relations the dlt pipeline presents to consumers keep the approved shape, covering whichever of names, columns, column order, types and the connector's own metadata columns the approved contract includes, and the unchanged consumers build against them.
- For each table in each parallel run, the reconciliation reports row counts and, where the table has a key, key sets compared both ways, and values compared under the approved agreement rule, as a table-level summary and row-level detail.
- Every difference carries a cause, from the approved list where that list is closed, and the reconciliation fails on any difference without one; a source change counts as the cause only where the approved timing rule allows it and the record really changed between the two loads' extractions.
- A duplicate key, a missing record or a difference the connector itself introduced is reported; none is collapsed, dropped or counted as agreement.
- Deletes reach the landing as the approved policy says, whether flagged, removed or recorded separately, and the result states which deletes the chosen load mechanism cannot see.
- Each later run loads the records the approved load mechanism selects, a rerun neither duplicates nor loses records, a new source column reaches existing records as approved, and a source schema change is handled as the approved schema policy says.
- Delete, new-column, schema-change and rerun behaviour the parallel runs do not exercise is verified where an executable check of it exists; otherwise the gap is stated and agreement is not claimed for it.
- Cutover readiness is stated with the reconciliation's open differences, the consumers each one would reach, and its limits, and the connector, its tables and the consumers are left as they were.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements. Read the connector's landed tables first: their names, columns, types, the connector's own metadata columns, how it marks deletes and history, and which consumers read each table. Confirm what the source exposes for identity, change tracking and deletes, and that the dlt pipeline can reach the same source the connector reads; if it cannot and another route is needed, say what that route changes. Choose the write disposition, keys and load mechanism from source evidence and the approved requirements, and state what the choice relies on and what it would miss, such as deletes or backfills of new columns. Land where both loads can exist at once, present the dlt landing in the approved consumer shape, and run both loads over the approved runs. Reconcile each run's pair of loads table by table under the approved agreement and cause rules, investigate every difference to its cause, and report cutover readiness and what the reconciliation cannot prove.

### Compose

- capturing-requirements
- add-or-update-source
- discovering-source-schema
- generating-dlt-pipeline
- dlt-unit-testing
- running-dlt-in-sandbox
- ingestion-data-testing
- verifying

### Ask first

- If unresolved, which of the connector's tables are in scope, and which consumers read each one?
- If unresolved, must consumers see exactly the connector's table names, columns, order and types, or may dlt land its own shape behind a compatibility layer, and which of the connector's metadata columns, such as sync time or a deleted flag, must be filled, and how?
- If unresolved, how does a delete reach the source (a flag or timestamp, or the record erased outright), how should the landing show it, and must records erased outright be detected?
- If unresolved by the source's evidence, which write disposition and key each table uses, whether loads are incremental and on which change marker and starting point, and how existing records get the values of a newly added column?
- If unresolved, beyond row counts and key sets, must every value agree, and compared exactly or after which stated normalisations of representation?
- If unresolved, how many parallel runs over what period, and how a record that changed in the source between the two loads' extractions is told apart from a defect?
- If unresolved, is "a cause for every difference" a closed list of allowed causes, and which?
- If unresolved, what should the pipeline do when the source adds a column or changes a column's type?

### Guardrails

- Do not disable, pause, reconfigure or modify the connector or its landed tables; proven agreement alone does not authorize cutover.
- Do not repoint consumers, change the dbt models, or decommission the connector as part of this work.
- Do not treat the connector's output as ground truth; a difference may be the connector's own error and is reported with its cause.
- Do not edit either side's data, widen a normalisation, extend a closed cause list or narrow the compared tables to make the reconciliation agree.
- Do not choose or apply a delete, history, schema or agreement rule without approval.
- Do not claim deletes are handled when the source erases records and the load mechanism cannot see them.
- Do not treat different instants as agreement, or the same instant landed with different time-zone handling as a difference, except as the approved agreement rule says.
- Do not force business deduplication or transformation into the landed tables.
