---
id: governed-spreadsheet-table
title: Promote a spreadsheet or CSV to a governed, tested table
trigger:
  - A spreadsheet that reports and models depend on is edited by hand, and a moved, renamed or retyped column keeps breaking them quietly.
  - Nobody can say what each column of a hand-maintained file means, who owns it or which row is the key.
  - A team keeps editing a sheet and re-exporting it, and wants a warehouse table of it that is checked on every new export.
description: Build a dlt pipeline and a governed table that load each new export of a hand-maintained spreadsheet under an approved structure contract, keep the last accepted version live when an export breaks it, set aside bad rows with reasons, keep every accepted version, and document every column with its owner.
pitch: Turn the spreadsheet everyone depends on into a governed table that fails loudly when its structure breaks.
job_category: build
area: ingestion
readiness: supported
domain_objects:
  - dlt_pipeline
  - bronze_table
  - dbt_model
  - rejected_records
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
    - dbt
qualifiers:
  - Assessed end to end on duckdb_local only; the other listed targets rely on dlt support and are unassessed.
  - Covers one hand-maintained file; a feed of system-generated files with completeness controls is file-drop-to-bronze.
  - Sized for spreadsheet-scale files; the CSV is read in full for each presentation.
  - Needs a Studio route for dlt to read the file; cloud buckets (ADLS, S3) have none today.
related:
  - api-to-bronze-incremental-contract
evidence:
  features:
    - capturing-requirements
    - add-or-update-source
    - generating-dlt-pipeline
    - dlt-unit-testing
    - running-dlt-in-sandbox
    - ingestion-data-testing
    - generating-dbt-model
    - dbt-unit-testing
    - documenting-dbt-models
    - verifying
  evals: []
---

## Prompt

Promote <file_name>, a spreadsheet that <owner_team> keeps by hand and re-exports as a CSV, to a governed table called <table_name> in the current Intent. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Load each new export with dlt and check it against the approved structure contract, so that a structural break fails loudly while consumers keep reading the last accepted version. Set aside every row that fails an approved value rule with its reason instead of losing it, keep every accepted version with its acceptance history, show the latest accepted version as the governed table, with one row per <key_column>, as the approved policy says, and document every column with its approved description and owner. Account for every row of every accepted export exactly once, record a refused export with its reason, and report what the checks cannot prove.

## Verified by

- Every export presented is recorded with its outcome under the approved version rules, and a refused export is recorded with its reason and retained as the approved acceptance-history rule says.
- An export that breaks the approved structure contract fails loudly, and what consumers read does not change.
- A change the approved contract tolerates, such as column order, header case or spacing, or an added column, is accepted without altering published values, and an added column the contract tolerates is reported.
- Every data row of every accepted export is accounted for exactly once, by source row, as published, set aside with its reason or reasons as the approved rule says, or handled under the approved duplicate rule, with none lost or counted twice; a refused export publishes nothing.
- Published values follow the approved normalisation and typing, and no value the contract refuses is coerced into a published column.
- The governed table shows the latest accepted version as the approved policy says, with one row per key, and every earlier accepted version stays queryable with when it was accepted.
- Re-presenting identical, older accepted or previously refused content follows the approved version rule, and leaves the governed table with no duplicated or stale row for any key.
- A record that was bad in an export, or absent from it, is shown in the governed table as the approved policy says.
- A change to a value list the user owns reaches later exports, and earlier accepted versions or not, as the approved rule says.
- Every governed column carries an approved description and owner.
- The result states what the checks cannot prove, such as a well-formed but wrong value or a record dropped from the sheet by mistake.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements. Confirm what the file holds first: its columns, their meanings and types, the key, which columns have value lists, and how the owner overwrites or re-exports it. Where the approved requirements leave them open, propose for approval the structure contract, the value rules, the normalisation, the version identity and what the governed table shows for a bad or absent record, and state what each choice relies on and what it would miss. Load each export with dlt, keep a record of every export presented and its outcome, retain each as approved, and set aside each failing row with its reason and the approved identifying detail. Build the governed table from the latest accepted version as the approved policy says, keep earlier versions queryable, and document every column with its owner. Reconcile each export to its rows by source row.

### Compose

- capturing-requirements
- add-or-update-source
- generating-dlt-pipeline
- dlt-unit-testing
- running-dlt-in-sandbox
- ingestion-data-testing
- generating-dbt-model
- dbt-unit-testing
- documenting-dbt-models
- verifying

### Ask first

- If unresolved, what the sheet holds: its columns and meanings, the key, required and optional columns, the types, the value lists the business edits, and who owns each column.
- If unresolved, what breaks the structure contract: a renamed, removed or retyped column, a reorder, an extra column, header case or spacing, repeated headers, an export with no data rows; and how a refusal is reported.
- If unresolved, which row problems are set aside, with which reasons: a missing required value, a value outside a list, the wrong kind of value, an impossible date order, a malformed key, a blank row or surplus cells; and whether a row with several problems records one reason or all.
- If unresolved, what a duplicated key means: whether identical copies collapse, whether differing copies are all set aside, and whether blank keys count as duplicates.
- If unresolved, how values are normalised before the checks (trimming, key case, list spelling), which date and number forms are accepted, and what a value that fits none does.
- If unresolved, what the governed table shows for a record that was bad in, or absent from, the latest accepted export: left out, or kept from the last accepted version.
- If unresolved, what makes a new version and what happens when an export repeats identical, older accepted or refused content, and whether a list edit reaches earlier accepted versions.
- If unresolved, which acceptance history to keep, whether a refused export is retained for inspection, and for how long.

### Guardrails

- Do not choose or apply a structure, value, duplicate, normalisation or version rule without approval.
- Do not coerce a value the contract refuses into a published column, and do not drop a row silently.
- Do not edit or overwrite the owner's file.
- Do not let a refused export change what consumers read.
- Do not infer a column's meaning, owner or key that neither the file nor an approved requirement states.
- Do not treat a matching row count as reconciliation; compare by source row.
- Do not extend the Recipe into scheduling, a feed of files with completeness checks, or downstream marts.
