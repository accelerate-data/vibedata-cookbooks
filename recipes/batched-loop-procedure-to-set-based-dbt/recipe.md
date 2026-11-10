---
id: batched-loop-procedure-to-set-based-dbt
title: Replace a batched row-loop procedure with one set-based dbt model and prove parity
trigger:
  - A nightly or historical load is a procedure that pages through its rows in a loop, with a batch size, a size threshold or a commit after every page, and nobody trusts replacing it.
  - The team wants one set-based dbt model, but consumers need proof of what the table holds however the loop paged, failed or restarted.
  - A SQL Server, Oracle or PostgreSQL estate is moving to dbt, and its procedures loop, page or commit in batches where a set-based model should do the work.
description: Replace the looping, paging or batching of one legacy load procedure with one set-based dbt model, reading it over MCP without changing it unless approved, with every loop construct mapped, parity with the procedure on each branch the comparison can reach, and failed pages, loop bounds, iteration state and reruns reported against the approved rule.
pitch: Drop the loop from a legacy load and prove one set-based model leaves the same rows, or the differences you approve, including after a failed page and a rerun.
job_category: re-engineer
area: transformation
readiness: supported
function:
  - cross-functional
domain_objects:
  - stored_procedure
  - maintained_table
  - batch_loop
  - loop_map
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
  - Reads the legacy database over a connected MCP server; any run of the procedure is approved and recorded.
  - A login that can write or run routines is reported; whether the run proceeds on it is approved.
  - Needs the tables the loop reads landed in the target; an ingestion Recipe lands them.
  - Unifying several writers of one table is consolidate-legacy-table-writers-to-dbt; this replaces one procedure's loop.
  - A procedure with no loop is stored-procedure-to-dbt; one that keeps row history is scd-procedure-to-dbt-snapshot.
  - A loop with no stated set rule, or one the MCP cannot read, is reported unassessed, not converted.
  - Behaviour outside the table's rows, such as logging and checkpoint tables, is reported, not reproduced.
  - In-place update or delete loops are in scope and are compared from the same prior table.
  - A loop that writes several tables is one outcome per table; the other tables are reported.
related:
  - stored-procedure-to-dbt
  - scd-procedure-to-dbt-snapshot
  - consolidate-legacy-table-writers-to-dbt
  - legacy-sql-to-dbt
  - inventory-legacy-database-over-mcp
  - plan-legacy-procedure-package-intents
  - dbt-full-refresh-to-incremental
evidence:
  features:
    - capturing-requirements
    - designing
    - planning
    - generating-dbt-model
    - running-dbt-in-sandbox
    - verifying
  evals: []
---

## Prompt

Replace the batch loop of <legacy_procedure>, which loads <target_table> for <consumers> by looping, paging or committing in batches, with one set-based dbt model in the current Intent. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Read the procedure and its data over the MCP and change nothing in the legacy database unless approved. Deliver a loop map that shows each looping, paging, batching, commit and error-handling construct, what it does to the rows and what the model does instead, the one model, built from its inputs as landed, and evidence that its rows equal those the procedure leaves, observed or reconstructed and labelled so, at the approved precision, on inputs that reach each branch the comparison can reach, including each arm the procedure chooses by size, with the rest stated unproven. Show what a failed page or row leaves behind and what a rerun leaves, apply the approved rule to each difference instead of reproducing it silently, report each defect as follow-up work, handle cutover as approved, and state what the comparison cannot prove, such as runtime, locking and volume.

## Verified by

- Every loop, cursor, paging, batching, commit and error-handling construct is listed with its parameters, thresholds and arm, its effect on the rows and its replacement or approved difference; a part left unconverted is named unassessed, the model is labelled partial, and no parity is claimed for it.
- One model builds the table's rows from the loop's inputs as landed in the target, at the legacy grain and columns unless an approved rule differs; its compiled SQL has no procedural loop or cursor; page arithmetic, a batch-size input or a set recursion appears only where an approved rule needs one.
- On inputs reaching each branch the comparison can reach, such as each side of a size threshold, a final partial page, an empty or inverted range and a page edge splitting related rows, the model's rows equal what the procedure leaves in the table at the approved precision; differences are named.
- A branch the inputs cannot reach is shown equivalent by an approved check or stated unproven, with no parity claimed. The procedure's rows are observed from an approved run or reconstructed from its readable rules independently of the model and labelled so; behaviour only a run shows stays unproven.
- Rows are compared as multisets on named columns, so a row present twice on one side and once on the other is a difference; the model adds no filter or de-duplication the procedure lacks except as an approved difference. A generated key follows the approved rule.
- Each tested value of a loop parameter, such as the batch size, gives the same rows, or the differing rows are listed with their cause. Where order is undefined or batches run concurrently, that is reported, an outcome no rule fixes is stated unproven, and order that matters is an approved column.
- Where the loop's bound, order or paging key counts or orders something other than what it inserts, such as a bound taken from one set while paging another, the rows it misses or repeats are counted and listed on an input that triggers it.
- Where an iteration uses what an earlier one produced, such as a running value, a counter, a work table or a read of the target, that dependence is itemised and tested on an input where the order changes the result, and is reproduced by an approved set rule or reported as not replaceable.
- Each failure the approved rules cover, such as a skipped page, a row error or pages committed before an error, is computed independently from the loop's rules as a count and an itemised list, and the model's rows beyond it are reported as the difference.
- Where the platform replaces tables atomically a failed build leaves the previous table, otherwise what it leaves is shown; a rerun leaves what a clean run leaves, or the difference is listed. Where the procedure resumes, appends or updates in place, the comparison starts from the same prior state.
- Each legacy defect and each behaviour the model cannot reproduce, such as a mark that skips or repeats committed rows, is listed with the rows it affects and what correcting it would change, as follow-up work.
- The legacy database changes only as approved, shown by a record of every statement sent, by default only reads; parity is kept separate from cutover, which keeps, retires or removes the procedure as approved after parity is accepted.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Read the procedure end to end over the MCP connection with reads only: its parameters and defaults, what it clears first, what it counts to choose between arms, each loop with its bound, order and paging key, any state carried between iterations in variables, work tables or reads of the target, marks, flags or deletes the loop applies to its source rows, where it commits and what its error handler does, concurrency, who calls it, and the triggers, constraints and defaults on the target. Compare the bound with what the loop pages, and use inputs that would separate them, such as a join that multiplies rows, ties on the paging key, rows at each page edge, an empty input and sizes on each side of every threshold. Settle how the procedure's rows are obtained without changing the legacy database unless approved, and how failure and restart outcomes are derived from the loop's rules when it cannot be run. Build one model under the approved project structure, compare its rows with the procedure's as multisets from the same prior table, show branches the inputs cannot reach equivalent by another check or state the gap, report every difference and defect as follow-up work, state what the comparison cannot prove, and handle cutover as approved.

### Compose

- capturing-requirements
- profiling-source-data
- designing
- planning
- generating-dbt-model
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which parameters, modes, thresholds, batch sizes and range, partition or entity-list loops, with their end points and defaults, are in scope, which values does the comparison use around each threshold, and does the run stop or proceed, named unassessed, on a part the MCP cannot read?
- If unresolved, what must the model do when a page, row or step fails: fail the build and publish nothing, or publish the rows that load and report the rows the failure would have lost?
- If unresolved, what must a run and a rerun leave in the table, such as a truncate and full reload, a resume from a mark or an append, does the model rebuild or add, and how is a half-loaded table recognised?
- If unresolved, how are ties, unordered paging keys and concurrent batches handled, and does the order of rows within or across pages matter to consumers?
- If unresolved, which behaviours that change rows are reproduced by an approved set rule, including recursion where the platform allows, corrected separately or accepted as differences: rows missed past a bound, repeated at an edge, dropped by joins or depending on earlier iterations?
- If unresolved, which columns and grain count as unchanged output, how is a generated key assigned, and at what precision are rows compared?
- If unresolved, where do the rows the procedure leaves come from, such as its select logic run read-only on the same inputs with the write applied, an approved copy over the MCP or approved snapshots, how are unreachable branches checked, and may a login that can write be used?
- If unresolved, once parity is accepted, do consumers move now or later, is the procedure kept, marked retired or removed, and may readers ever see a table loaded only in part?

### Guardrails

- Do not run the legacy procedure or write to the legacy database unless the owner approves it.
- Do not put a procedural loop or cursor in the model to make parity pass, or reproduce a page, row or step failure as page logic, since a failure is environmental, not a data rule; page arithmetic, a batch-size input or a recursion is allowed only where an approved rule needs one.
- Do not claim parity from inputs that cannot reach a loop branch, such as an input below the size threshold when the loop runs only above it.
- Do not filter or de-duplicate rows the procedure does not, and do not repair a legacy defect the approved rule reproduces.
- Do not take the procedure's rows from the model, or from a table the procedure wrote that the inputs do not match.
- Do not describe a reconstruction of the procedure's rows as an observed run.
- Do not edit a legacy answer or expected output, or widen the approved precision, to make a comparison pass.
- Do not present a partial table after a failed load as a complete one, or hide that the procedure can leave one.
- Do not copy a loop's checkpoint, control or log tables into the model; derive any resume rule from the table or an approved rule.
- Do not remove or disable the procedure before parity is accepted, or let it and the model maintain the consumer-facing table at the same time.
