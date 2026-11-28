---
id: stored-procedure-to-dbt
title: Convert a stored procedure into a dbt model and check parity after every compared run
trigger:
  - A nightly load is a stored procedure nobody fully understands, and it inserts, updates, deletes or merges rows in a table people depend on.
  - The team wants the procedure's logic in dbt with tests and lineage, but consumers need proof the table ends up the same after every run.
  - A procedure that maintains a table in place has to move into the dbt project before it can be retired.
description: Move a stored procedure that maintains a table run after run into dbt, with each procedural step that shapes the table mapped to a dbt equivalent or an approved listed difference, parity with the unchanged procedure shown after every compared run or stated unproven where the baseline is not its output, defects reproduced where the model can and reported, and retirement only as approved.
pitch: Retire a stored procedure by rebuilding it in dbt and checking the table after every compared run, proven where the baseline is the procedure's own output.
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
  - Needs the tables the procedure reads landed in the target; landing them belongs to an ingestion Recipe.
  - Views, one-shot scripts and procedures that rebuild their whole output each run belong to legacy-sql-to-dbt.
  - A table other routines also write belongs to consolidate-legacy-table-writers-to-dbt.
  - A procedure with more than one in-scope consumer table belongs to split-multi-table-procedure-to-dbt.
  - A procedure that loops or pages through rows belongs to batched-loop-procedure-to-set-based-dbt.
  - Applies when the maintained table, plus any selection state a later run reads, carries all relevant behaviour.
  - Row-history procedures use scd-procedure-to-dbt-snapshot; snapshot and key-resolving fact loads have their own Recipes.
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

Convert <stored_procedure>, which maintains <target_table> for <consumers> by inserting, updating, deleting or merging rows on each run, into dbt in the current Intent. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Deliver a map from each procedure step that shapes the table to its dbt equivalent, the dbt models that maintain the table, and evidence that after every run in the agreed sequence the compared columns match what the unchanged procedure leaves after the same run, at the approved precision, with any approved difference listed and any run whose baseline is not the procedure's own output stated unproven. Reproduce every procedure behaviour that affects the table, including ones that look like mistakes, unless the model cannot reproduce it and the difference is approved and listed, and report each defect as follow-up work; an output change someone wants belongs in a separate change. Handle cutover and the procedure as approved, and state what the comparison cannot prove.

## Verified by

- Each procedure step that shapes the table, including the conditions that make an insert, update, delete or merge fire, maps to a dbt equivalent, to a stated reason none is needed, or, where the model cannot reproduce it, to an approved listed difference.
- Behaviour the table's state cannot show, such as writes to tables no later run reads, output parameters or external side effects, is reported out of scope; after a failed run the table holds what the procedure leaves, or where the model cannot, follows the approved failure rule, listed.
- The maintained table keeps the approved contract, covering whichever of relation name, columns, column order, types, keys, nullability and materialization it counts as unchanged output; any column outside parity is approved and named with its reason.
- After every agreed run in each approved mode, the compared columns match the procedure's table after that run from the same inputs and approved starting table at the approved precision, apart from approved listed differences, including, where the baseline allows, runs making each kind of change.
- The comparison runs the published model's logic, differing only in named inputs and stand-ins; it holds in each approved environment and time zone and can fail: a value changed beyond the approved precision, a lost row or an added duplicate row fails it unless it is an approved listed difference.
- A repeat in the agreed sequence leaves the compared columns as the procedure leaves them after the same repeat, at the approved precision, apart from approved listed differences; any change a repeat makes is stated, and is follow-up where it is a defect or breaks an approved operational rule.
- Where the model starts from, or can rebuild, the table from current inputs, each row where that build differs from the procedure's table after the same run, such as a row only that table holds, is listed and kept as the procedure keeps it unless the model cannot and the approved rule says otherwise.
- Each procedure behaviour that affects the table, including source-engine collation in key matches, empty strings and rounding, is reproduced unless the model cannot reproduce it and the difference is approved and listed; each defect is listed with its rows, the rule it breaks and what a fix changes.
- A run whose inputs hold several rows for one key leaves the table as the procedure would, whether its engine rejects the run, applies every row or applies one; an outcome that is not deterministic, or that the model cannot reproduce, follows the approved rule and is listed with its rows.
- Each generated key follows the procedure's rule or, where the model cannot reproduce it, an approved rule that keeps it distinct and non-null wherever the procedure's keys are; its values are compared where the approved contract keeps them, and any key assigned differently is listed with its rows.
- Behaviours the compared runs never exercise, such as a row removed on one run and changed on a later one, are checked with the procedure or another approved oracle where available; any gap, and any run whose baseline is not the procedure's own output, is stated unproven.
- Parity is kept separate from cutover and retirement: where the dbt model takes over the table, the procedure stops maintaining it after parity is accepted; where consumers move later, its table stays maintained until the cutover; the procedure is kept, removed or changed as approved.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements. Read the procedure end to end first: its parameters, what it reads on each run, every step in order, the conditions under which each insert, update, delete or merge fires, its temporary tables, joins and null handling, and find every consumer of the table it maintains. Report behaviour the table's state cannot represent as out of scope. In every build that writes the table, check each run's inputs for several rows per key before applying them, and match what the procedure does with them. Settle how the procedure's table after each compared run is obtained, by running the unchanged procedure on the same inputs or from the approved baseline, and which run sequence is compared, including runs that exercise each kind of change the procedure makes. Map each step to a dbt equivalent under the approved project structure, and choose how the model maintains the table from the procedure's behaviour and the approved requirements, and state what it relies on and would miss. Reproduce each behaviour, including the ones that look like mistakes, and report each defect as follow-up work. Compare the model's table with the procedure's after every compared run, check behaviours the compared runs never exercise against the unchanged procedure or another approved oracle where one exists, stating the gap where none does, handle cutover and the procedure as approved, and state what cannot be proven.

### Compose

- capturing-requirements
- profiling-source-data
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- documenting-dbt-models
- verifying

### Ask first

- If unresolved, what counts as unchanged output (rows and values, or also relation name, columns, order, types and materialization), is any column outside parity, must generated keys keep the procedure's values, and does the model take over the table's name or do consumers move later?
- If unresolved, what does the model's table start from at the first compared run and at takeover: the procedure's table as of an approved run or a build from current inputs, and where the model cannot keep rows only the procedure's table holds, how are they handled?
- If unresolved, which parameter values, modes and selection rules, such as a date window or a watermark or processed flag the procedure keeps in another table, are in scope, how does each map to one way of running the model, and which compared runs exercise each?
- If unresolved, which run sequence and inputs form the comparison, what stands in for any clock, session, random or sequence value the procedure reads, is the match exact or within an approved precision, and in which environments and time zones must it hold?
- If unresolved, where and with which login may the unchanged procedure run, where else may its table after each run come from and who approves it, and where and for how long may copies of its tables and inputs be kept?
- If unresolved, which repeated runs, such as a retry, does the sequence include, may a repeat change rows under an approved operational rule, and after a run the procedure fails partway, which approved rule applies where the model cannot leave the table as the procedure does?
- If unresolved, which rule decides an outcome the procedure leaves to chance or the model cannot reproduce, such as which of several rows for one key wins or how a generated key is assigned and kept, and may such a difference be accepted and listed?
- If unresolved, which project structure and layering conventions must the models follow, and once parity is accepted, is the procedure kept and marked retired or removed after any cutover, or, where it still writes other tables, changed by its owner to stop writing this one before the model does?

### Guardrails

- Do not claim parity from the final state alone or from one-off queries; each comparison reruns from its recorded starting table and run sequence while approved copies exist, and copies of customer rows stay only where and as long as approved, never committed unless approved.
- Do not ship a partial translation: a procedure step that affects the table and has no dbt equivalent blocks the conversion and is reported, unless the user approves it as a listed difference.
- Do not correct a procedure defect; reproduce it, report it as follow-up work, and route any wanted output change to a separate change.
- Do not let the procedure and the dbt model both maintain the consumer-facing table at the same time.
- Do not remove or disable the procedure before parity is accepted, or while consumers still depend on it; proven parity alone does not authorize removal.
- Do not fix a stand-in for the clock or another run-dependent value into the model; use it only for the comparison, and keep reading the value where the procedure does, or for a generated key the model cannot reproduce, follow the approved key rule.
- Do not let constructed proof inputs or comparison runs of the procedure reach the consumer-facing table, the copies the published build reads, or, unless approved, the live legacy database; run them only in a separate, named test build and report their results separately.
- Do not edit the procedure or its captured per-run output, widen a tolerance, or narrow the contract, the compared columns, the compared runs or the approved precision, to make the comparison pass; a rule-built baseline shares no logic with the model.
- Do not change models outside the conversion; at takeover, name each consumer an approved listed difference reaches and what it will see, and take over only as approved.
- Do not extend the conversion into keeping row history the procedure did not keep, scheduling, performance tuning or moving the model off the Intent's platform.
