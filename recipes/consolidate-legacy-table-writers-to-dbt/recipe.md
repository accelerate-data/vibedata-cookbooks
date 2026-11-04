---
id: consolidate-legacy-table-writers-to-dbt
title: Consolidate a table's legacy writers into one incremental dbt model and prove parity per load mode
trigger:
  - One legacy table is written by more than one stored procedure or job, and the team wants one dbt model to replace them all.
  - A daily load and a separate historical rebuild both write the same fact table, and nobody can say whether they define its rows the same way.
  - An inventory of a legacy SQL Server, Oracle or PostgreSQL warehouse shows a table with two or more writers that has to move to dbt.
description: Replace every legacy writer and load mode of one table with one incremental dbt model, reading the legacy database over MCP without changing it unless approved, with each approved mode mapped to one way of running the model, parity per mode on the same inputs, writer disagreements and legacy defects reported, and retirement only as approved.
pitch: Replace the routines that write one table with one incremental dbt model, proven against the approved legacy logic for each load mode.
job_category: re-engineer
area: transformation
readiness: planned
function:
  - cross-functional
domain_objects:
  - stored_procedure
  - maintained_table
  - table_writer_map
  - load_mode
  - dbt_model
  - approved_baseline
  - parity_report
  - follow_up
works_with:
  platforms:
    - duckdb_local
    - motherduck
    - fabric_lakehouse
    - fabric_warehouse
    - redshift
    - databricks
  tools:
    - dbt
    - sql_server
    - oracle
    - postgresql
qualifiers:
  - Reads over a connected MCP server only, such as Toolbox for SQL Server and Oracle or postgres-mcp for PostgreSQL.
  - A login that can write or run routines is reported; whether the run proceeds on it is approved.
  - A table one routine maintains, in one or several modes, belongs to stored-procedure-to-dbt.
  - Writers outside the database, string-built writes and objects the login cannot read are named unassessed.
  - Writers that keep row history belong to scd-procedure-to-dbt-snapshot.
  - Behaviour outside the table's rows, such as other writes or logging, is reported, not reproduced.
  - Planned until Databricks moves from design-partner access to a supported Studio build target.
related:
  - stored-procedure-to-dbt
  - inventory-legacy-database-over-mcp
  - plan-legacy-procedure-package-intents
  - legacy-sql-to-dbt
  - scd-procedure-to-dbt-snapshot
  - dbt-full-refresh-to-incremental
evidence:
  features:
    - capturing-requirements
    - generating-dbt-model
    - running-dbt-in-sandbox
    - verifying
  evals: []
---

## Prompt

Replace every legacy writer of <target_table>, the routines <legacy_writers> and their load modes, with one incremental dbt model in the current Intent. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Read the legacy database over its connected MCP server, and change nothing in it unless the owner approves. Deliver a writer map that shows what each writer and mode does to the table, the one model with each approved legacy mode mapped to one way of running it, and evidence that after each compared run in each mode the table equals what the approved legacy logic for that mode produces from the same inputs and the same prior table, at the approved precision. Show where the writers disagree and apply the approved rule, reproduce legacy behaviours that change rows as approved, state any the model cannot reproduce as an approved difference, leave corrections to a separate change and report each one as follow-up work, handle cutover and retirement as approved, and state what the comparison cannot prove.

## Verified by

- Every writer the readable definitions show, including triggers, string-built writes and ones nothing schedules or calls, is listed with its modes, callers, effect on the table and replacement or approved retirement; a writer outside the database or unreadable is named unassessed.
- One model publishes the table's replacement, and each approved legacy mode, such as a normal load, a full reload or a historical rebuild, maps to exactly one way of running it.
- After each compared run in each approved mode, the table equals the rows the legacy logic approved for that mode produces from the same inputs and prior table, derived independently of the model, at the approved precision; columns approved as outside parity are named.
- A normal run adds exactly the rows the legacy logic approved for normal runs adds on the same prior table, including rows at the edges of its selection, changes or removes an existing row only where that logic does, and a repeat on unchanged inputs changes the table only as a legacy repeat does.
- In each compared run, source rows the approved legacy logic leaves out, such as lines whose dimension match is missing or no longer current, are counted with their reason, so no row is lost without a stated cause.
- Rows each writer owns are traced to it; where writers or modes publish different rows for the same inputs and key, the differing rows are shown, the approved rule decides which wins in each way of running the model, and each conflict is reported as follow-up work.
- Legacy behaviours that change rows, such as row multiplication, filters that depend on other rows or batches that skip their failures, are reproduced or handled as approved, and each is listed with the rows it affects as follow-up work.
- Where a construct such as a filter that depends on other rows or a selection window makes a full rebuild publish a different table from the one the compared normal runs reached, the affected rows are reported.
- The published grain is stated and holds: rows are unique where the legacy rows are unique and multiplied only where approved legacy behaviour multiplies them, and any generated key the approved contract keeps follows the approved rule and is never null.
- Branches the compared runs cannot reach, such as size thresholds or failure paths, are shown equivalent by an approved check, or stated unproven.
- The legacy database changes only as approved, shown by a record of every statement sent: by default only reads and no routine run, and any approved run of a writer is recorded with what it changed.
- Parity is kept separate from cutover: the legacy writers stop maintaining the table only after parity is accepted, and each is kept, marked retired or removed as approved.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Read every writer of the table end to end over the MCP connection: its modes and parameters, what it reads, whether it truncates, appends or updates, its joins, filters and row multiplication, its batching and error handling, and who calls it. Compare the writers with each other before choosing anything, and use inputs that would separate them, such as rows each filter drops, orders that multiply, rows at the edges of the selection window, rows already loaded and records whose dimension match is missing or no longer current. Settle how the legacy answer for each mode is obtained without changing the legacy database, and how a prior table is set up so the incremental mode is really exercised. Build one model under the approved project structure with each approved mode mapped to one way of running it, compare its table with the legacy answer after each compared run, show branches the inputs cannot reach equivalent by another check or state the gap, report every disagreement and defect as follow-up work, and handle cutover and retirement as approved.

### Compose

- capturing-requirements
- generating-dbt-model
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, what counts as a writer, such as triggers, string-built statements, partition swaps, bulk loads or jobs outside the database, which writers and load modes are in scope, including ones nothing calls, and which retire once the model takes over?
- If unresolved, do the writers own separate rows or columns or define the same rows differently, and where they overlap or disagree, which writer's behaviour does each way of running the model reproduce, with any wanted output change left to a separate change?
- If unresolved, which way of running the model stands for each legacy mode, and which run sequence forms the comparison, including the order, overlap and schedule of the writers, such as a rebuild followed by normal runs?
- If unresolved, how is the legacy selection reproduced on a normal run, such as its window, its default date and time zone, and how a row already loaded is recognised?
- If unresolved, which legacy behaviours that change rows, such as multiplication, filters that depend on other rows or batches that skip failures, are reproduced, and which are corrected in a separate change?
- If unresolved, which columns count as unchanged output, how is a generated key assigned, and is any column outside parity?
- If unresolved, where do the legacy answers come from, such as the legacy logic read over MCP against the same inputs, running the writers or approved snapshots, at what precision, and may a login that can write be used?
- If unresolved, once parity is accepted, do consumers move now or later, and is each legacy writer kept, marked retired or removed?

### Guardrails

- Do not write to the legacy database or run its routines to obtain a baseline unless the owner approves it.
- Do not leave out a writer because nothing calls it, and do not merge writers that disagree without the approved rule.
- Do not claim the writers agree from inputs on which their differences cannot show.
- Do not correct a legacy defect the approved rule reproduces; a behaviour a set-based model cannot reproduce, such as a skipped failed batch, is an approved difference, stated and reported.
- Do not edit a legacy answer or expected output, or widen the approved precision, to make a comparison pass.
- Do not let a normal run update or remove a row the approved legacy logic for normal runs leaves untouched.
- Do not let the legacy writers and the model maintain the consumer-facing table at the same time.
- Do not remove or disable a legacy writer before parity is accepted and consumers no longer depend on it.
