---
id: spark-ingestion-notebook-to-dlt
title: Convert a Spark ingestion notebook into a dlt pipeline and prove landed parity
trigger:
  - A Spark notebook lands raw files into bronze, and the team wants that load as tested pipeline code without keeping a cluster for it.
  - An ingestion notebook nobody can change safely mixes parsing, renames and deduplication in cells with no tests, and reruns surprise people.
  - Models read the tables a Spark notebook lands, so a replacement has to land the same data and prove it before anyone switches.
description: Convert a Spark ingestion notebook into an owned dlt pipeline that lands beside the notebook's tables, accounts for every source record and every notebook step, and is reconciled table by table with a cause for every difference.
pitch: Turn a Spark ingestion notebook into a dlt pipeline you own, and prove table by table what it lands and why any row differs.
job_category: re-engineer
area: ingestion
readiness: supported
domain_objects:
  - spark_notebook
  - dlt_pipeline
  - bronze_table
  - rejected_record
  - consumer_contract
  - reconciliation_report
works_with:
  platforms:
    - duckdb_local
  tools:
    - dlt
qualifiers:
  - Complete outcome assessed for duckdb_local only; the other four Studio targets remain unassessed.
  - Needs the notebook's code, the tables it landed, and read access to the files it reads.
  - Source files must be reachable from the workspace; Studio's cloud-bucket route (ADLS, S3) is not supported today.
related:
  - managed-connector-to-dlt
  - notebook-transformation-to-dbt
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

Convert the <notebook_name> Spark notebook that lands <source_files> into <notebook_tables> into a dlt pipeline in the current Intent, so that <consumers> can later move to it. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Read what each notebook step does, carry each into the dlt load, list it as follow-up work or drop it as approved, land the approved tables beside the notebook's tables without changing them, prepare them in the approved consumer shape without taking over the relations consumers read today, and reconcile both loads table by table over the approved runs, accounting for every source record and giving every difference a cause, from the approved list where that list is closed. Report switch-over readiness and what the reconciliation cannot prove; leave the notebook running and consumers unchanged.

## Verified by

- Every approved table is landed by the dlt pipeline next to the notebook's tables, and neither load overwrites the other.
- Every step the notebook performs is accounted for: carried into the dlt load, listed as follow-up work for a downstream model, or dropped, as approved, and none is lost without being stated.
- The relations prepared for consumers keep the approved shape, covering whichever of names, columns, column order, types and the notebook's own metadata columns the approved contract includes, and none of them replaces a relation consumers read today.
- Every source record in each run is accounted for on both sides, landed, kept, set aside or dropped as the approved malformed-record policy says, and every record either side drops is counted and reported.
- For each table in each run, the two loads are compared under the approved agreement rule, and every disagreement, a record on one side only or a differing value, is reported for the table and for the record.
- Every difference carries a cause, from the approved list where that list is closed, and the reconciliation fails on any difference without one; a difference the notebook itself introduced is reported as such.
- Re-sent and corrected records land as the approved rule says, and a rerun of an already-loaded file neither duplicates nor loses records.
- A source field the notebook's schema ignored, a new field and a changed type are handled as the approved schema policy says, and each is reported.
- Malformed-record, re-sent, corrected, rerun and schema-change behaviour the compared runs do not exercise is verified where an executable check of it exists; otherwise the gap is stated and agreement is not claimed for it.
- Switch-over readiness is stated with the reconciliation's open differences, the consumers each one would reach, and its limits, and the notebook, its tables and the consumers are left as they were.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements. Read the notebook cell by cell first: its reader options and declared schemas, how it treats malformed records, renames, flattening, casts, filters, deduplication, the metadata columns it adds, and what its write does to the existing table on each run. Then read its landed tables and which consumers use each. Confirm the dlt pipeline can read the same files through a route Studio supports; if another route is needed, say what it changes. List each notebook step with where it goes, and note behaviour in the notebook that the approved rules treat as a defect. Choose the write disposition, keys and file selection from source evidence and the approved requirements, and state what the choice relies on and what it would miss. Land where both loads can exist at once, prepare the landing in the approved consumer shape beside what consumers read today, run both loads over the approved runs, and reconcile each run table by table, accounting for every source record. Investigate every difference to its cause and report switch-over readiness and what the reconciliation cannot prove.

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

- If unresolved, which of the notebook's landed tables are in scope, and which consumers read each one?
- If unresolved, for each notebook step (parsing, renames, flattening, casts, filters, deduplication, metadata columns), does it move into the dlt load, become follow-up work for a downstream model, or get dropped?
- If unresolved, must consumers see exactly the notebook's table names, columns, order and types, or may dlt land its own shape behind a compatibility layer, and how are the notebook's metadata columns, such as source file or load time, filled?
- If unresolved, what happens to a record the notebook's reader drops or nulls as malformed: is it dropped, kept with nulls, or set aside with its file, position and reason?
- If unresolved, how must a re-sent record and a corrected record land, and where the notebook's own behaviour differs from that rule, does the dlt load keep the notebook's behaviour or follow the rule?
- If unresolved, beyond row counts and key sets, must every value agree, and compared exactly or after which stated normalisations of representation?
- If unresolved, how many runs over which files, and is "a cause for every difference" a closed list of allowed causes, and which?
- If unresolved, what should the pipeline do with a field the notebook's schema ignores, a newly added field, and a changed field type?

### Guardrails

- Do not modify, disable or reschedule the notebook, its job or its landed tables; proven agreement alone does not authorize switching over.
- Do not repoint consumers, change downstream models, or retire the notebook as part of this work.
- Do not treat the notebook's output as ground truth; a difference the notebook itself introduced is reported with its cause.
- Do not decide on your own whether to keep or correct a notebook behaviour that departs from the approved rules; report it and follow the approved choice.
- Do not drop a malformed record without counting and reporting it.
- Do not edit either side's data, widen a normalisation, extend a closed cause list or narrow the compared tables to make the reconciliation agree.
- Do not treat the same instant landed with different time-zone handling as a difference, or present consumers a different timestamp type, except as the approved contract and agreement rule say.
- Do not add business transformation to the landed tables beyond the notebook steps the approved step map keeps in the load.
