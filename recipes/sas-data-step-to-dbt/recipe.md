---
id: sas-data-step-to-dbt
title: Rebuild a SAS DATA-step batch job in dbt and prove the rows match
trigger:
  - A monthly or nightly table is still produced by a SAS batch job whose DATA steps keep running totals, merge by key or write only some rows, and nobody left can explain it.
  - The team wants the job's logic in the dbt project, but its consumers need proof the new models return the same rows, keys, types and amounts.
  - A plain join and group-by would look like a faithful translation of the SAS code, but the job's retained state, merge behaviour or output conditions say otherwise.
description: Rebuild a bounded tabular SAS DATA-step job as dbt models that publish the same contract, proven against the job's output, or an approved reference, on the same inputs, with each behaviour classed preserved, changed with approval or unsupported and each defect reported as follow-up work.
pitch: Retire a SAS batch job by rebuilding it in dbt and proving the models return what it returned, row by row, bar approved changes.
job_category: re-engineer
area: transformation
readiness: supported
function:
  - cross-functional
domain_objects:
  - sas_program
  - dbt_model
  - consumer_contract
  - approved_baseline
  - parity_report
  - follow_up
works_with:
  platforms:
    - duckdb_local
  tools:
    - dbt
qualifiers:
  - Complete outcome assessed for duckdb_local only; the other four Studio targets remain unassessed.
  - Needs the resolved SAS program and formats; the job's output may come from a run or an approved reference.
  - Covers tabular DATA-step preparation only; statistical procedures, model fitting and report layouts are out of scope.
related:
  - legacy-sql-to-dbt
  - notebook-transformation-to-dbt
  - prove-dbt-change-safe
evidence:
  features:
    - capturing-requirements
    - generating-dbt-model
    - verifying
  evals: []
---

## Prompt

Rebuild <sas_job> as dbt models in the current Intent so that the published models can take over its output for <consumers> as approved. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Deliver the models with evidence that the published rows, keys, types and amounts match the job's output on the agreed inputs at the approved precision, including the value on every row of any retained state. Reproduce each DATA-step behaviour that affects the output, covering row order and ties, missing values, the merge of repeated keys, BY-group boundaries, output conditions and format lookups, unless an approved change or an unsupported class says otherwise; class each as preserved, changed with approval or unsupported, report each defect as follow-up work, and keep any approved output change apart from the parity baseline. Handle the old job as approved, and state what the comparison cannot prove.

## Verified by

- The published models keep the approved contract, covering whichever of relation names, column names and order, types, amounts and materialization the approved contract counts as unchanged output.
- Published rows equal the job's output on the agreed inputs at the approved precision, with none missing or extra, except rows touched by an approved change or an unsupported behaviour, which are listed and carry no parity claim; any retained running state is shown on every row.
- Where the job retains state, it starts and restarts where the SAS code says at each BY-group boundary, and each published value equals one derived independently from the inputs and the approved rules.
- Where the approved contract keeps row order it follows the approved SAS rules; ties on sort keys and missing keys follow them wherever they decide a value, and each is shown matching.
- Where the job merges by key, at least one independently derived case with a key repeated on both sides, labelled constructed if the data lacks it, shows the merge result and the rows an ordinary join returns differing; published rows follow the job's merge for repeated and unmatched keys.
- A missing value, including special missing codes and blank characters, gives what the job gives in sums, running totals, comparisons and format lookups, and is never read as zero unless the job does so; a value no format maps follows the job's result.
- Each input observation is traced to the rows the job's output statements produce in each dataset it writes, or to a non-write shown or counted with its reason as approved, and each published dataset matches its job dataset with row counts reconciling under the job's own multiplicity.
- Every behaviour that affects the output is classed preserved, changed with approval or unsupported, unknown ones stay visible, and each defect is listed with the output it affects and what correcting it would change.
- Where the agreed inputs do not exercise a material behaviour, parity is checked against the job or an approved reference, or the gap is stated; a reference not produced by running the job is labelled so.
- The old job stays untouched and available until the proof is accepted, and where the models take over its output relation the job is retired as approved only after that; parity is kept apart from consumer cutover.
- Anything the comparison cannot prove is stated, including where the job's output varies from run to run.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements. Read the SAS program end to end in execution order: each DATA step, its sorts, merges and BY statements, retained and accumulating variables, conditions that write a row and the defaults each relies on, then the formats and how the job writes its result, and find every consumer of that result. Confirm the sources exist in the Domain and settle how the job's output on the agreed inputs is obtained and under which SAS release. Profile the inputs, then freeze the program, formats, inputs and reference output, and any independently derived expectation, before any model is written. Reproduce each DATA-step behaviour explicitly instead of relying on a join, window or aggregate that only looks equivalent: order and ties, retained state restarting at each group, where the job merges, the positional pairing of repeated keys with the shorter side carrying its last row forward, missing values, conditional output and format lookups. Prove at least one repeated-key case that a plain join answers differently. Run the models in the sandbox with a unit test per behaviour, compare each published relation with the job's output in both directions, check unexercised behaviours against an independent oracle or state the gap, class each behaviour, report each defect as follow-up work, handle the old job as approved, and state what the comparison cannot prove.

### Compose

- capturing-requirements
- profiling-source-data
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which SAS release, and which options and defaults of it, apply to row order and ties on the sort keys, missing values in keys and sums, the merge of repeated keys and numeric precision?
- If unresolved, what counts as unchanged output: rows and values only, or also relation and column names and order, row order, types (how SAS dates, character length and padding, and special missing codes are carried) and materialization?
- If unresolved, which behaviours, if any, may change on purpose, with approval and kept apart from the parity baseline, and which stay reproduced as the job has them?
- If unresolved, how is the job's output on the agreed inputs obtained (a run of the job, its current table or an approved hand-worked reference), which parameters, macro variables, run date and inputs apply, and is the match exact or within an approved precision?
- If unresolved, are the rows the job does not write listed with their reason or only counted with it, and which of the datasets the job writes are in scope?
- If unresolved, how is a step handled that calls a macro, routine or include whose code is not available: left out as unsupported, or supplied as an approved input?
- If unresolved, do the published models take over the job's output relation, or do consumers move later as separate work?
- If unresolved, once the proof is accepted and any cutover is complete, is the SAS job kept and marked retired, or removed?

### Guardrails

- Do not edit the SAS program, its formats or the job's output to make the comparison pass, and do not take the reference from a run with stale state or a different release than approved.
- Do not translate a DATA step by syntax alone; a join, window or aggregate that looks equivalent is not evidence, and the proof is the comparison with the job's output.
- Do not correct a defect in the job, such as a merge that repeats a row or a sum that skips a missing amount, unless the change is approved; reproduce it, report it as follow-up work, and keep any approved change apart from the parity baseline.
- Do not read a missing value as zero, collapse ties, or reorder rows unless the job's behaviour or an approved change does.
- Do not remove or disable the old job before the proof is accepted or while current consumers still use it; proven parity alone does not authorize removal.
- Do not treat a green build, equal row counts or one matching grand total as proof of parity.
- Do not claim exact parity where the job's output varies from run to run; report what cannot be proven.
- Do not widen a tolerance, or narrow the contract, the compared inputs or the approved precision, to make the comparison pass.
- Do not change the output of models outside the rebuild.
- Do not extend the rebuild into statistical procedures, model fitting, report layouts, scheduling, performance tuning, repointing dashboards or moving to another platform.
