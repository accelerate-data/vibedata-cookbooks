---
id: file-drop-to-bronze
title: Load a recurring file drop into bronze with file-completeness and schema controls
trigger:
  - A partner or vendor drops files into a folder on a schedule, and bronze has to pick up each delivery without a rerun loading it twice.
  - Files arrive late, twice, empty, cut short or with a changed layout, and nobody finds out until a report is wrong.
  - Downstream teams need to know, for every delivery the team expected, whether it arrived complete before they build on it.
description: Build a dlt pipeline that lands a recurring file drop into bronze so a rerun over an unchanged drop duplicates no delivery's records, reports a delivery complete only when it passes the approved completeness and layout checks, keeps what fails visible with its reason, recovers a part-way failure without loss or duplication, and reports the status of every expected delivery after each run.
pitch: Land a recurring file drop into bronze so a rerun duplicates nothing, with completeness checks, a schema contract and a status for each expected delivery.
job_category: build
area: ingestion
readiness: supported
domain_objects:
  - dlt_pipeline
  - dlt_resource
  - bronze_table
  - rejected_records
  - delivery_status_report
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
  - Needs a Studio route for dlt to read the drop; cloud buckets (ADLS, S3) have none today.
  - Needs each delivery to state its own completeness, such as a control file.
  - Covers delimited text files such as CSV; JSON, Parquet and Excel are out of scope.
  - Reading an API or a database belongs to api-to-bronze-incremental-contract or database-tables-to-bronze.
  - A hand-maintained sheet re-exported whole belongs to governed-spreadsheet-table.
related:
  - api-to-bronze-incremental-contract
  - managed-connector-to-dlt
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

Build a dlt pipeline in the current Intent that lands the recurring file drop from <drop_location> into bronze, with deliveries expected on <delivery_cadence>. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Report a delivery complete only when it passes the approved completeness and layout checks, handle one that fails as approved with its outcome and reasons visible, and handle repeated and corrected deliveries, late and stray files, bad rows and layout changes as approved. A rerun over an unchanged drop duplicates no delivery's records and leaves every landed record's content as it was; only load identifiers and timestamps and the counts and times of a file's repeat sightings may change. Recover a run that fails part-way without losing or duplicating a record. Carry the approved lineage on each landed row. After each run, report every file seen and the status of every expected delivery, reconcile what landed against the files themselves, and report what the checks cannot prove.

## Verified by

- A rerun over an unchanged drop duplicates no delivery's records and leaves every landed record's content as it was, and only load identifiers and timestamps and the counts and times of a file's repeat sightings may change; a part-way failure is recovered without losing or duplicating a record.
- A delivery is reported complete only when it passes the approved completeness check against what the delivery itself states and the approved layout; one that fails is handled as the approved failure rule says, and its outcome and reasons stay visible.
- A failed delivery and a later file for its period, a late file, and an identical, changed or failing re-delivery are each handled as the approved rules say, and bronze never mixes two versions of one delivery unless the rule keeps both.
- A delivery with no records, a zero-byte file, a file that does not match what its delivery states, a data file with no completeness statement, a statement with no data file and a name matching no pattern are each given the status the approved rule assigns.
- A new column, a missing, renamed or reordered column, a changed type and invalid encoding are handled as the approved layout rule says, and no value is silently dropped, repaired or retyped.
- A row that cannot be parsed is handled as the approved rule says, and for every delivery that lands, any row count it states equals the rows landed plus the rows set aside.
- Timestamps, decimals and the delivery's period land as the approved type and time-zone rule says, and no value shifts or loses scale except as that rule allows.
- A record key repeated within or across deliveries is handled as the approved rule says, and no repeat is removed or collapsed without being reported.
- Each landed row carries the approved lineage back to the file it came from and the delivery it belongs to, and to the file's version where the approved rule keeps more than one.
- After each run, every file the run finds in the drop is accounted for once per version (a file's distinct content), and every expected period has exactly one status from the approved status set, from the files actually present.
- Each landed file's values, with what was set aside, equal the file's own contents by content and record key after the approved type rules, and the result states what the checks cannot prove, such as a change to or removal of a file after the run that read it.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements. Confirm the drop first: how a delivery is named and which period it covers, what states it complete, the file format, encoding and columns, how late, repeated, corrected and stray files arrive, and whether the folder keeps past deliveries. Where the approved requirements leave them open, propose for approval the completeness check, how a failing delivery is handled, the re-delivery rule, the layout contract, bad-row handling and the expected window, and state what each relies on and what it would miss. Decide what is new in a way that survives reruns and a folder that keeps its history, because an unchanged folder looks the same on every run and, under the approved rule, a later file may complete or replace an earlier delivery. Land the approved deliveries without business transformation, keep every file and period status visible after each run, and reconcile each file against its own contents.

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

- If unresolved, which files and periods are in scope, what names a delivery and which date places it in a period, and is a delivery one file or several parts?
- If unresolved, what is the file format: encoding, header, delimiter, how nulls and quoted values read, and which columns and types are expected?
- If unresolved, what states a delivery complete, and what do a data file whose completeness statement has not arrived, a statement with no data file, a name matching no pattern, and a zero-row or zero-byte file mean?
- If unresolved, what becomes of a delivery that fails a check and of a later corrected file; how are a late file, an identical re-delivery, a changed one and a changed one that fails handled; are all failure reasons recorded or the first?
- If unresolved, which periods are expected (every day or only business days, from which start to which as-of date), which statuses a file or period can have, and does a missing period only report or also fail the run?
- If unresolved, what does the contract do when a column is added, missing, renamed, reordered or changes type, what type does an added column take, where does a row that cannot be parsed go, and how many bad values make it a type change rather than bad rows?
- If unresolved, how do timestamps (zone, offset), decimals (scale, values with fewer or more places) and the delivery's period land, which column identifies a record, and is a repeated key kept as delivered or removed?
- If unresolved, which lineage does each landed row carry, do processed files stay in place, how is an older file re-sent after a newer version treated, and is a part-way failure retried automatically or only when someone reruns?

### Guardrails

- Do not choose or apply a completeness, failure-handling, re-delivery, layout, bad-row or type rule without approval.
- Do not report a delivery as complete when it fails the approved completeness check.
- Do not repair, coerce or drop a value silently, such as re-encoding bytes, padding a scale or ignoring an unknown column.
- Do not treat a rescan of an unchanged folder as a new delivery.
- Do not move, rename or delete files in the drop without approval.
- Do not claim a delivery that never arrived, or a change made to a file after the run that read it, was captured.
- Do not force business deduplication or transformation into the landed tables beyond the approved rule.
- Do not read an API or a database through this Recipe, nor load a hand-maintained spreadsheet's whole-copy exports here; those belong to api-to-bronze-incremental-contract, database-tables-to-bronze and governed-spreadsheet-table.
- Do not add a schedule or downstream models as part of this work.
