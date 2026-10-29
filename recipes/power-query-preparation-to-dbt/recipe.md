---
id: power-query-preparation-to-dbt
title: Move a Power Query data preparation into tested dbt models and prove parity
trigger:
  - A workbook or report prepares its data in Power Query, and the M code is the only place that logic lives, with no tests and nobody able to review it.
  - Dates, numbers, merges or error cells in the preparation have behaved differently after a refresh, and the team wants the logic as models it can test and review.
  - Someone has to show the preparation, rebuilt in the warehouse, returns the same rows as the queries on an agreed window before the workbook is pointed at it.
description: Move the preparation of selected Power Query outputs into dbt models over landed source tables, with a verdict for every step, each output compared with a reference refresh on an agreed window, the points where M and SQL part ways reported, and a cutover and recovery plan that keeps the workbook untouched.
pitch: Move a Power Query preparation into tested dbt models, prove each output against a reference refresh, and plan the cutover without touching the workbook.
job_category: re-engineer
area: transformation
readiness: supported
function:
  - cross-functional
domain_objects:
  - power_query_query
  - dbt_model
  - consumer_contract
  - reference_refresh
  - conversion_report
  - parity_report
works_with:
  platforms:
    - duckdb_local
  tools:
    - dbt
qualifiers:
  - Needs the exported M of the selected queries, the parameter values they run with and the project locale.
  - Needs the queries' own refresh output on the agreed window, or an approved reference built from their semantics.
  - Reads landed source tables; Studio has no Power Query engine, so the queries are read from their export.
  - Incremental-refresh partitions, fuzzy merges and privacy-level behaviour are out of scope and reported as not converted.
related:
  - file-drop-to-bronze
  - visual-etl-mapping-to-dlt-dbt
  - adf-mapping-data-flow-to-dlt-dbt
  - legacy-sql-to-dbt
  - notebook-transformation-to-dbt
evidence:
  features:
    - capturing-requirements
    - add-or-update-source
    - generating-dlt-pipeline
    - ingestion-data-testing
    - generating-dbt-model
    - dbt-unit-testing
    - running-dbt-in-sandbox
    - documenting-dbt-models
    - verifying
  evals: []
---

## Prompt

Move the preparation that <query_names> do in Power Query into the current Intent as tested dbt models, so that <consumers> of the workbook or report can review it and later read from it. Inherit the Intent's repository, platform, Domain, landed sources and approved requirements, and resolve only the semantics they leave open. Give every step of the exported queries one verdict, implemented, removed with approval or not converted, with its reason and the code or gap, and record for each step where it ran in Power Query, folded into the source or in the mashup engine, and how much source data each side read. Reproduce what the queries do under <project_locale>, including date and number parsing, merge matching and fan-out, null keys, error cells and which rows each filter and removal step drops, and prove each output in <outputs> equals the queries' reference refresh on <agreed_window> in both directions and independently from the sources. Report every behaviour that looks wrong and every approved difference without correcting it, state what cannot be converted, write the cutover and recovery as a plan only, and leave the workbook, its queries and its refresh schedule untouched.

## Verified by

- Every step of the exported queries has one verdict, implemented, removed with approval or not converted, with its reason and the code or gap, and the counts add up to the steps; a step that cannot be converted is named, never silently dropped.
- Each step records where it ran in Power Query and the source data each side read; the warehouse side is measured, the Power Query side is labelled as from the export or recorded diagnostics, and no speed or cost claim is made without a measurement.
- Every output equals the reference on the agreed window as a multiset in both directions, never by row order, except what depends on a set-aside step or a live clock, which is named as unproven; the reference is labelled a recorded refresh or declared semantics.
- Each awkward input on the window has a hand-written expected result from the documented M semantics that the reference refresh agrees with, such as an ambiguous date, a locale-format number, a key with several merge matches, a null key, an error cell and a duplicate line.
- Each input row is traced to all its output rows or to the one step that first drops it, and output rows equal kept rows plus the extra rows from each multiplying step such as a merge, unpivot or append, each counted with no residue.
- For date and number parsing, merge multiplicity, null keys, and error cells and removal steps, the query's construct, the model's construct and the verdict are stated, with the rows where each bites.
- A column fed by a step that cannot be converted carries no parity claim, and the report says so.
- Each deliberate difference is named with its approval and kept out of the parity baseline; every behaviour of the queries that looks wrong is reproduced, reported with its trigger and rows, and left uncorrected.
- A cutover and recovery plan is written as a plan only, with the parallel run, the comparison that opens and closes its gate, the approver, and a data-level recovery that restores the consumer table, since reverting code does not reverse data.
- The workbook, its queries, its refresh schedule and every existing model, source and test are unchanged, and nothing is cut over.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, landed sources and approved requirements. Read the export end to end first: each query's steps in order, the parameters, the project locale and which queries are load-disabled staging for another, and give each step a stable identifier the report can cite. Settle where the reference refresh on the agreed window comes from and what the awkward inputs are for each place M and SQL part ways. Build the preparation as models that apply the steps in the queries' own order, publish each consumer output as a relation with an enforced contract and typed columns, and count every dropped row against the one step that dropped it. Give every step its verdict, compare every output with the reference refresh, derive the awkward rows by hand from the documented semantics, list every difference with its cause, and state what the comparison cannot prove. Write the cutover and recovery as a plan only.

### Compose

- capturing-requirements
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- documenting-dbt-models
- verifying

### Ask first

- If unresolved, which queries are moved, which are load-disabled staging for another, which parameter values form the agreed window and are its bounds inclusive, and who owns the consuming workbook?
- If unresolved, where does the reference refresh on that window come from, a recorded refresh or one built from the declared semantics, and who approves it?
- If unresolved, what is the project locale, which culture parses each date and number column, and how is an error cell that reaches a load represented, whatever its cause?
- If unresolved, does the consumer need any difference from what the queries do with unparseable values, several merge matches, null or unmatched keys or text comparers, and who approves each difference?
- If unresolved, which rows do the filters and the de-duplication keep, how is a tie broken, and what counts as equal at each output: exact or an approved precision, and which types must hold?
- If unresolved, how is a value that depends on the current date or time handled, frozen to a declared date or computed live, and who approves the difference, and what time zone applies?
- If unresolved, what happens to a step that runs a script or cannot be reproduced, and to what depends on it: fail the move, set it aside and report it, or use a named substitute; and which steps with no data effect may be removed, and who approves each?
- If unresolved, who approves the cutover, how long the parallel run lasts, and what restores the consumer table if the move goes wrong?

### Guardrails

- Do not edit the workbook or report, its queries or its refresh schedule, and do not commit connection strings, credentials or workbook data found in the export.
- Do not correct a behaviour of the queries that looks wrong, such as a merge that multiplies rows or a null key that matches; reproduce it, report it as follow-up work, and route any wanted output change to a separate change.
- Do not replace M's parsing, null, error or ordering behaviour with the SQL default; where the two differ, the query's declared result is the target and the difference is reported.
- Do not leave a step, an input row or a difference unaccounted for; a step that cannot be converted gets a stated verdict or fails the move as approved.
- Do not compare on row order, widen the precision, narrow the window or change the expected output to make the comparison pass.
- Do not claim parity for a column, window or platform the comparison did not cover, claim a speed or cost improvement without a measurement, or equate a reference built from declared semantics with a live refresh of the queries.
- Do not treat a green build or passing tests as proof of parity; the proof is the comparison with the reference refresh.
- Do not perform the cutover, repoint the workbook, retire the queries or change a schedule; this work plans them only.
