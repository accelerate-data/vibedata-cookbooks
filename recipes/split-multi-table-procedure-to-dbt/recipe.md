---
id: split-multi-table-procedure-to-dbt
title: Split a procedure that writes several tables into one dbt model per table, with parity for each
trigger:
  - One legacy stored procedure loads several tables in a single run, and each table should become its own dbt model.
  - A procedure that rebuilds several report or mart tables has to move into dbt before it can be retired, and each table has its own consumers.
  - Part of a procedure's work is hidden in dynamic SQL or routines it calls, and splitting it into models first needs every table it writes.
description: Split a legacy procedure that writes several tables into one dbt model per table, reading the legacy database without changing it, with every table it writes found, shared logic defined once, parity shown for each table separately, run order and failure behaviour recorded, and each table's cutover and the procedure's retirement handled as approved.
pitch: Turn one procedure that loads several tables into one dbt model per table, each with its own parity proof.
job_category: re-engineer
area: transformation
readiness: planned
function:
  - cross-functional
domain_objects:
  - stored_procedure
  - maintained_table
  - table_writer_map
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
  - Not yet assessed end to end on motherduck, fabric_lakehouse, fabric_warehouse, redshift or databricks.
  - Reads over a connected MCP server only, such as Toolbox for SQL Server and Oracle or postgres-mcp for PostgreSQL.
  - A login that can write or run routines is reported; whether the run proceeds on it is approved.
  - Needs the tables the procedure reads landed in the target; landing them belongs to an ingestion Recipe.
  - A procedure with one in-scope table belongs to stored-procedure-to-dbt.
  - Tables that keep row history, such as hand-rolled slowly changing dimensions, belong to scd-procedure-to-dbt-snapshot.
  - A table other routines also write belongs to consolidate-legacy-table-writers-to-dbt.
related:
  - stored-procedure-to-dbt
  - consolidate-legacy-table-writers-to-dbt
  - scd-procedure-to-dbt-snapshot
  - plan-legacy-procedure-package-intents
  - inventory-legacy-database-over-mcp
  - legacy-sql-to-dbt
evidence:
  features:
    - capturing-requirements
    - designing
    - planning
    - generating-dbt-model
    - dbt-unit-testing
    - running-dbt-in-sandbox
    - verifying
  evals: []
---

## Prompt

Split <legacy_procedure> in <legacy_database> on the connected <source_engine> MCP, which writes several tables in one run, into one dbt model per table in the current Intent, reading it over the MCP only and changing nothing in it. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Deliver a map of every table the procedure writes, including dynamic SQL and routines it calls, with each table's disposition and any write it cannot resolve; one dbt model per in-scope table, built from its inputs as landed in the target, with logic the approved design names as shared defined once; and, for each table separately, evidence that its model's rows match what the procedure leaves in it, per the approved baseline and precision, each difference listed with the rule that permits it. Record, per converted mode, the procedure's write order and how a failure part-way leaves its tables, reproduce legacy behaviour as approved and raise each defect separately, keep parity, cutover and retirement apart for each table, recording any change to the procedure for its owner, and state what the comparison cannot prove.

## Verified by

- Every table the procedure writes, including through dynamic SQL, routines it calls, triggers its writes fire and other databases, is listed with how it was found and one approved disposition: its own dbt model, a handoff or an exclusion with its reason; a write it cannot resolve is named unresolved.
- Each in-scope table has exactly one dbt model that produces it from the procedure's inputs as landed in the target; logic the approved design names as shared is defined once and used by every model that needs it, and no model repeats it.
- Where the procedure reads a table it wrote, or is about to rewrite, earlier in the same run, the reading model sees that table's state at that point in the run through the approved dependency or shared logic, with no cycle; tables loaded independently build independently.
- Per table, the model's rows equal what the procedure leaves for the same input, per an approved baseline not taken from the model's SQL, after every run in the agreed sequence for a table kept over its prior state, whole rows, duplicates counted, at the approved precision, bar permitted differences.
- Each table's differences from its baseline are listed with their rows and the approved rule permitting each; where surrogate key values are exempt, a key to another table is compared by the row it resolves to; any other difference fails that table, and no pass stands in for another.
- The compared input exercises, per table and converted mode, each behaviour that shapes it, such as rows a join or filter drops, a join that multiplies rows, null grouping values, a zero divisor, rounding boundaries and a branch deciding whether a table is written, or names it unverified.
- Engine behaviour that changes a result, such as text comparison, totals over empty input, the precision of computed decimals, division and rounding, and grouping-level encoding, is recorded for each table with how the model keeps it or the approved difference.
- The write order and the state a failure part-way leaves each table are recorded for each converted mode; the dbt run's behaviour on such a failure is shown or marked unverified, and an approved choice the platform cannot meet is raised before approval and reported unmet, never passed.
- Legacy behaviour is reproduced as the approved parity rule says, including behaviour that looks like a defect, such as a join that drops rows or a value rounded twice; each defect is raised separately with the rows it affects.
- A record lists every statement sent to the legacy database and each is a read: none would change data, schema or settings, and the procedure is not run there; any change seen in its tables is traced to source activity, never to this work.
- Parity, cutover and retirement are kept apart for each table: none moves before its parity is accepted, consumers read one maintained copy at a time, and the approved change that stops the procedure writing it, or retires it, is recorded for its owner, not made over the read-only connection.
- Effects no table shows, such as output parameters, result sets, messages and raised errors, are reported out of scope, and anything the comparison cannot prove is stated, such as an unreadable dynamic statement or a result that depends on the order rows arrive.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements, including any approved package plan, and resolve only the semantics they leave open. Read the procedure end to end through the MCP with reads only, including statements it builds as strings, routines it calls and triggers its writes fire, and list each table it writes, how the write was found, what the table reads, under which parameters and conditions it is written, whether it is rebuilt or kept over its prior state, and any other writer; send tables with other writers or row history to their own Recipes. Keep a record of every statement sent to the legacy database and check it against the call history before verification. Settle scope, modes, shared logic, run and failure semantics, the parity rule and each table's baseline with the user, and check the engine behaviours that change each result on both engines through the same expressions and types the procedure uses. When legacy tables are empty or cannot be compared directly, build input that exercises each table's behaviours and obtain the rows the write leaves as approved. Share logic only where tables really share it, build one model per table, compare each table on its own as published, over a run sequence where it is kept over its prior state, and explain every difference rather than normalizing it away. Raise defects separately, record cutover and any procedure change for its owner, and state what cannot be proven.

### Compose

- capturing-requirements
- designing
- planning
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which tables are in scope: every table the procedure writes, including through dynamic SQL, routines it calls and triggers, or a named subset; how temporary, log, audit and control or watermark tables are treated; and whether a write the text cannot resolve stops the run.
- If unresolved, which parameter values and run modes are converted, and how a table written only under some of them, or only when a data condition holds, is built, skipped or recorded as an unconverted branch.
- If unresolved, which logic the tables share and in what form, such as one shared model, a macro or none, and how a table the procedure reads after writing it in the same run reaches the model that reads it.
- If unresolved, the run semantics: keep the legacy order and the state a failure part-way leaves, or require that all tables load or none do, and how a failed table is reported.
- If unresolved, each table's parity rule: exact or within a precision, whether surrogate key values and the spelling a case-insensitive group shows count, how engine behaviours such as case folding, totals over empty input and rounding are kept, and whether each defect is reproduced or corrected.
- If unresolved, whether each table is rebuilt each run or kept over its prior state, where its baseline comes from, such as the procedure on an approved copy, snapshots or its select logic run read-only with the write applied, which input, runs and starting state are compared, and who approves.
- If unresolved, what load, locking or time window the legacy database may take, and whether the run may proceed on a login that can write or stops until a read-only login is supplied.
- If unresolved, whether tables cut over together or one at a time, who, outside this work, changes the procedure so it stops writing a table that has moved, and whether the procedure is kept or removed once its tables have moved.

### Guardrails

- Do not send a statement that writes, even one that matches no rows or would be refused, or run the procedure in the legacy database; read through the MCP only, within the approved limits.
- Do not treat catalog dependency metadata as the complete list of tables the procedure writes; dynamic SQL, called routines, triggers, synonyms and views hide writes.
- Do not normalize, trim, re-case or round values in a comparison beyond the approved parity rule to make a table pass; compare each table as published and explain each difference.
- Do not claim parity for one table from another table's result, for every table from one combined comparison, or for every mode from the default one.
- Do not invent shared logic for tables that share nothing, or copy logic the approved design shares into each model.
- Do not correct a legacy defect the approved parity rule keeps; reproduce it and raise it.
- Do not let consumers read a table that the procedure and a dbt model both maintain, or record a table as moved before its parity and cutover are accepted.
- Do not convert a table that other routines also write or that keeps row history here; hand it to its own Recipe or leave it on the legacy.
