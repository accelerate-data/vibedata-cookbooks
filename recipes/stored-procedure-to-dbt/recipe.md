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
    - fabric_warehouse
    - redshift
  tools:
    - dbt
qualifiers:
  - Not yet assessed end to end on fabric_warehouse or redshift.
  - Needs the procedure's table after each compared run, from the unchanged procedure or approved snapshots.
  - Views and one-shot scripts that rebuild their whole output each run belong to the legacy-sql-to-dbt Recipe.
  - Procedures that keep row history, such as hand-rolled slowly changing dimensions, are out of scope.
  - Applies when the maintained table is the required outcome and all relevant behaviour is represented through its state.
related:
  - legacy-sql-to-dbt
  - dbt-full-refresh-to-incremental
  - prove-dbt-change-safe
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
- Any procedure behaviour that cannot be represented through the maintained table's state, such as writes to other tables, transaction or rollback semantics, output parameters, external side effects or error paths, is reported as out of scope.
- The maintained table keeps the approved contract, covering whichever of relation name, columns, column order, types and materialization the approved contract counts as unchanged output.
- After every run in the agreed sequence, not only the last, the table matches what the unchanged procedure leaves after the same run on the same inputs at the approved precision, including, where the procedure can be run or its snapshots allow, runs that exercise each kind of change it makes.
- The match holds in each approved execution environment and time zone.
- A repeated run in the agreed sequence leaves the table exactly as the unchanged procedure leaves it after the same repeat, at the approved precision; any change a repeat makes is stated, and is follow-up work only where it violates an approved operational requirement.
- Where the model can also rebuild the table from scratch, any input for which a rebuild as of a run would differ from the procedure's table after that run is reported.
- Every procedure behaviour that affects the table is reproduced, and each defect is listed with the rows it affects, the rule it appears to break and what correcting it would change, as follow-up work; a repeat's behaviour follows the repeated-run rule.
- For procedure behaviours the compared runs never exercise, such as a row removed on one run and changed on a later one, parity is checked with the unchanged procedure or another approved oracle where available; otherwise the gap is stated.
- Output parity is kept separate from cutover and retirement: where the dbt model takes over the table, the procedure stops maintaining it after parity is accepted; where consumers move later, its table stays maintained until the cutover; the procedure is kept or removed as approved.
- Anything the comparison cannot prove is stated.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Read the procedure end to end first: its parameters, what it reads on each run, every step in order, the conditions under which each insert, update, delete or merge fires, its temporary tables, joins and null handling, and find every consumer of the table it maintains. Report any behaviour the table's state cannot represent, such as other writes, rollback semantics, output parameters, side effects or error paths, as out of scope. Settle how the procedure's table after each compared run is obtained, by running the unchanged procedure on the same inputs or from approved snapshots, and which run sequence is compared, including runs that exercise each kind of change the procedure makes. Map each step to a dbt equivalent under the approved project structure, and choose how the model maintains the table from the procedure's behaviour and the approved requirements, and state what the choice relies on and what it would miss. Reproduce each behaviour, including the ones that look like mistakes, and report each defect as follow-up work. Compare the model's table with the procedure's after every compared run, check behaviours the compared runs never exercise against the unchanged procedure or another approved oracle where one exists, stating the gap where none does, handle cutover and the procedure as approved, and state what cannot be proven.

### Compose

- capturing-requirements
- profiling-source-data
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- documenting-dbt-models
- verifying

### Ask first

- If unresolved, what counts as unchanged output: rows and values only, or also the relation name, column names, column order, types and materialization? Does the dbt model take over the table's name, or do consumers move to it later?
- If unresolved, which run sequence and inputs form the comparison, are values compared exactly or within an approved precision, and in which execution environments and time zones must the table match?
- If unresolved, when the procedure cannot run beside the model, for example on another engine, where does its table after each run come from, and who approves that baseline?
- If unresolved, which repeated runs, such as a retried run, does the agreed sequence include, and does an approved operational requirement limit what a repeat may change?
- If unresolved, which project structure and layering conventions must the models follow?
- If unresolved, once parity is accepted and any cutover is complete, is the procedure kept and marked retired, or removed?

### Guardrails

- Do not edit the procedure or its captured per-run output to make the comparison pass.
- Do not claim parity from the final state alone; a table that matches only after the last run has not been shown to match on the runs consumers read in between.
- Do not ship a partial translation: a procedure step that affects the table and has no dbt equivalent blocks the conversion and is reported.
- Do not correct a procedure defect; reproduce it, report it as follow-up work, and route any wanted output change to a separate change.
- Do not let the procedure and the dbt model both maintain the consumer-facing table at the same time.
- Do not remove or disable the procedure before parity is accepted, or while consumers still depend on it; proven parity alone does not authorize removal.
- Do not widen a tolerance, or narrow the contract, the compared runs or the approved precision, to make the comparison pass.
- Do not change the output of models outside the conversion.
- Do not extend the conversion into keeping row history the procedure did not keep, scheduling, performance tuning or moving to another platform.
