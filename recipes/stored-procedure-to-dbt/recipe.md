---
id: stored-procedure-to-dbt
title: Convert a stored procedure into a dbt model and prove parity
trigger:
  - A nightly load is a stored procedure nobody fully understands, and it inserts, updates, deletes or merges rows in a table people depend on.
  - The team wants the procedure's logic in dbt with tests and lineage, but consumers need proof the table ends up the same after every run.
  - A procedure that maintains a table in place has to move into the dbt project before it can be retired.
description: Move a stored procedure that maintains a table run after run into dbt, with each procedural step that shapes the table mapped to a dbt equivalent and parity with the unchanged procedure shown after every compared run, procedure defects reproduced and reported, and retirement only as approved.
pitch: Retire a stored procedure by rebuilding it in dbt and proving the table matches after every compared run, not only at the end.
job_category: re-engineer
area: transformation
readiness: supported
function:
  - cross-functional
domain_objects:
  - stored_procedure
  - maintained_table
  - dbt_model
  - consumer_contract
  - step_map
  - approved_baseline
  - parity_report
  - follow_up
works_with:
  platforms:
    - duckdb_local
    - fabric_warehouse
    - redshift
    - databricks
  tools:
    - dbt
qualifiers:
  - Needs the procedure's table after each run from its own runs, approved snapshots or a labelled rule-built baseline.
  - Needs the text of the procedure, its called routines, dynamic SQL and table triggers; unreadable parts are named.
  - Views, one-shot scripts and procedures that rebuild their whole output each run belong to legacy-sql-to-dbt.
  - Procedures that keep row history, such as slowly changing dimensions, belong to scd-procedure-to-dbt-snapshot.
  - A table other routines also write belongs to consolidate-legacy-table-writers-to-dbt.
  - A procedure that writes several consumer tables belongs to split-multi-table-procedure-to-dbt.
  - A procedure that loops or pages through rows belongs to batched-loop-procedure-to-set-based-dbt.
  - Applies when the maintained table, plus any selection state a later run reads, carries all relevant behaviour.
  - Accumulating snapshots, periodic snapshots and fact loads that resolve dimension keys have their own Recipes.
  - Complete outcome assessed for duckdb_local only; the other listed platforms remain unassessed.
related:
  - legacy-sql-to-dbt
  - dbt-full-refresh-to-incremental
  - prove-dbt-change-safe
  - scd-procedure-to-dbt-snapshot
  - consolidate-legacy-table-writers-to-dbt
  - split-multi-table-procedure-to-dbt
  - batched-loop-procedure-to-set-based-dbt
  - accumulating-snapshot-procedure-to-dbt
  - legacy-periodic-snapshot-to-dbt
  - late-arriving-fact-keys-to-dbt
evidence:
  features:
    - capturing-requirements
    - profiling-source-data
    - generating-dbt-model
    - dbt-unit-testing
    - running-dbt-in-sandbox
    - documenting-dbt-models
    - verifying
  evals: []
---

## Prompt

Convert <stored_procedure>, which maintains <target_table> for <consumers> by inserting, updating, deleting or merging rows on each run, into dbt in the current Intent. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Deliver a map from each procedure step that shapes the table to its dbt equivalent, the dbt models that maintain the table, and evidence that after every run in the agreed sequence the table matches what the unchanged procedure leaves after the same run, at the approved precision. Reproduce every procedure behaviour that affects the table, including ones that look like mistakes, and report each defect as follow-up work; an output change someone wants belongs in a separate change. Handle cutover and the procedure as approved, and state what the comparison cannot prove.

## Verified by

- Each procedure step that shapes the table, including the conditions that make an insert, update, delete or merge fire, maps to a dbt equivalent or to a stated reason none is needed.
- Any procedure behaviour the maintained table's state cannot show, such as writes to other tables that no later run reads, rollback semantics, output parameters, external side effects or error handling beyond what a run leaves in the table, is reported as out of scope.
- The maintained table keeps the approved contract, covering whichever of relation name, columns, column order, types, keys, nullability and materialization it counts as unchanged output; any column outside parity is named with its reason.
- After every run in the agreed sequence and each approved mode, not only the last, the compared columns match the procedure's table after that run from the same inputs and approved starting table at the approved precision, including, where the baseline allows, runs that make each kind of change.
- The match holds in each approved execution environment and time zone.
- A repeated run in the agreed sequence leaves the table as the unchanged procedure leaves it after the same repeat, at the approved precision; any change a repeat makes is stated, and is follow-up work only where it violates an approved operational requirement.
- Where the model starts from, or can rebuild, the table from current inputs, every row in which that build differs from the procedure's table after the same run, such as a row only the procedure's table holds, is listed and handled as the approved starting rule says.
- Every procedure behaviour that affects the table, including source-engine semantics such as collation in key matches, empty strings and rounding, is reproduced or, where approved, listed as a difference; each defect is listed with its rows, the rule it appears to break and what fixing it changes.
- A run whose inputs hold several rows for one key leaves the table as the procedure would, whether its engine rejects the run, applies every row or applies one; an outcome that is not deterministic, or that the model cannot reproduce, follows the approved rule and is listed with its rows.
- Each generated key follows the approved rule for assigning and keeping it; it is distinct and non-null wherever the procedure's keys are, and any key the model assigns differently from the procedure is listed with its rows.
- Behaviours the compared runs never exercise, such as a row removed on one run and changed on a later one, are checked with the procedure or another approved oracle where available; any gap, and any run whose baseline is not the procedure's own output, is stated unproven.
- Output parity is kept separate from cutover and retirement: where the dbt model takes over the table, the procedure stops maintaining it after parity is accepted; where consumers move later, its table stays maintained until the cutover; the procedure is kept or removed as approved.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Read the procedure end to end first: its parameters, what it reads on each run, every step in order, the conditions under which each insert, update, delete or merge fires, its temporary tables, joins and null handling, and find every consumer of the table it maintains. Report any behaviour the table's state cannot represent, such as writes no later run reads, rollback semantics, output parameters, side effects or error paths, as out of scope. Settle how the procedure's table after each compared run is obtained, by running the unchanged procedure on the same inputs or from the approved baseline, and which run sequence is compared, including runs that exercise each kind of change the procedure makes. Map each step to a dbt equivalent under the approved project structure, and choose how the model maintains the table from the procedure's behaviour and the approved requirements, and state what it relies on and would miss. Reproduce each behaviour, including the ones that look like mistakes, and report each defect as follow-up work. Compare the model's table with the procedure's after every compared run, check behaviours the compared runs never exercise against the unchanged procedure or another approved oracle where one exists, stating the gap where none does, handle cutover and the procedure as approved, and state what cannot be proven.

### Compose

- capturing-requirements
- profiling-source-data
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- documenting-dbt-models
- verifying

### Ask first

- If unresolved, what counts as unchanged output (rows and values, or also relation name, columns, order, types and materialization), is any column outside parity, how is a generated key assigned and kept, and does the model take over the table's name or do consumers move later?
- If unresolved, what does the model's table start from at the first compared run and at takeover: the procedure's table as of an approved run or a build from current inputs, and how are rows only the procedure's table holds handled?
- If unresolved, which parameter values, modes and selection rules, such as a date window or a watermark or processed flag the procedure keeps in another table, are in scope, how does each map to one way of running the model, and which compared runs exercise each?
- If unresolved, which run sequence and inputs form the comparison, what stands in for any clock, session, random or sequence value the procedure reads, is the match exact or within an approved precision, and in which environments and time zones must it hold?
- If unresolved, where and with which login may the unchanged procedure run for the comparison, and when it cannot run beside the model, for example on another engine, where does its table after each run come from, and who approves that baseline?
- If unresolved, which repeated runs, such as a retried run, does the agreed sequence include, and does an approved operational requirement limit what a repeat may change?
- If unresolved, which rule decides an outcome the procedure leaves to chance or the model cannot reproduce, such as which of several rows for one key wins, and may such a difference be accepted and listed?
- If unresolved, which project structure and layering conventions must the models follow, and once parity is accepted and any cutover is complete, is the procedure kept and marked retired, or removed?

### Guardrails

- Do not claim parity from the final state alone or from one-off queries; a table that matches only after the last run has not been shown to match on the runs consumers read in between, and each comparison is kept so it reruns from its recorded starting table and run sequence.
- Do not ship a partial translation: a procedure step that affects the table and has no dbt equivalent blocks the conversion and is reported, unless the user approves it as a listed difference.
- Do not correct a procedure defect; reproduce it, report it as follow-up work, and route any wanted output change to a separate change.
- Do not let the procedure and the dbt model both maintain the consumer-facing table at the same time.
- Do not remove or disable the procedure before parity is accepted, or while consumers still depend on it; proven parity alone does not authorize removal.
- Do not fix a stand-in for the clock or another run-dependent value into the model; use it only for the comparison, and keep reading the value where the procedure does.
- Do not let constructed proof inputs or comparison runs of the procedure reach the consumer-facing table, the copies the published build reads, or, unless approved, the live legacy database; run them only in a separate, named test build and report their results separately.
- Do not edit the procedure or its captured per-run output, widen a tolerance, or narrow the contract, the compared runs or the approved precision, to make the comparison pass.
- Do not change the output of models outside the conversion.
- Do not extend the conversion into keeping row history the procedure did not keep, scheduling, performance tuning or moving the model off the Intent's platform.
