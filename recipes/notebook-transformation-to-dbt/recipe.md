---
id: notebook-transformation-to-dbt
title: Convert a notebook transformation into a dbt model and prove parity
trigger:
  - A table or report is still produced by running a notebook by hand, pulling warehouse data into dataframes, with no tests, lineage or review.
  - The team wants the notebook's logic in the dbt project, but its consumers need proof that the dbt version returns the same results.
  - Dataframe code (merges, group-bys, fills, de-duplication, pivots) has to move into dbt models without changing what the notebook published.
description: Bring a hand-run notebook transformation into dbt as models that publish the same contract, proven against what the unchanged notebook writes on the same inputs, with its implicit dataframe behaviour and defects reproduced and reported as follow-up work.
pitch: Retire a hand-run notebook by rebuilding its dataframe logic in dbt and proving the new models publish what the notebook did.
job_category: re-engineer
area: transformation
readiness: supported
domain_objects:
  - notebook
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
  - Needs the notebook's output on the same inputs, from a run of the unchanged notebook or its current table.
related:
  - legacy-sql-to-dbt
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

Convert <notebook> into dbt models in the current Intent so that the published model can replace the notebook's output for <consumers>. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Deliver the dbt models with evidence that the published result keeps the approved contract and matches what the unchanged notebook writes on the agreed inputs at the approved precision. Reproduce every notebook behaviour that affects the published output, including implicit dataframe behaviour and ones that look like mistakes, and report each defect as follow-up work; an output change someone wants belongs in a separate change. Handle the notebook as approved, and state what the comparison cannot prove.

## Verified by

- The published model keeps the approved contract, covering whichever of relation name, columns, column order, types and materialization the approved contract counts as unchanged output.
- Published rows match what the unchanged notebook writes on the agreed inputs at the approved precision; the baseline is the table the notebook publishes, not its in-memory dataframes, and any difference left is reported and parity is not claimed for it.
- The match holds in each approved execution environment and time zone, with the notebook run in the same environment wherever it is re-run; independence from the time zone is required only where the consumer contract already includes it.
- Every notebook behaviour that affects the published output is reproduced, including implicit dataframe defaults such as group-bys that drop missing keys, missing values in sums, de-duplication across a whole frame, fills, join types, and measures over different rows.
- Where the notebook's output shape depends on the data, such as one column per value found, the published shape and what happens when the data gains or loses a value are stated, and handled as the approved contract says.
- Each notebook defect found is listed with the output it affects, the rule it appears to break and what correcting it would change, as follow-up work.
- For material notebook behaviours the comparison inputs do not exercise, such as a missing key, an empty group or a value the data lacks, parity is verified by running the unchanged notebook on inputs that exercise them where that is possible; otherwise the gap is stated.
- Output parity is kept separate from consumer cutover: where the published model takes over the notebook's output relation, the notebook is retired as approved after parity is accepted; where consumers move later, the notebook's output stays available until the cutover.
- Anything the comparison cannot prove is stated.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements. Read the notebook end to end first, in execution order: what each cell reads, every dataframe step, its merges, group-bys, fills, de-duplication and reshapes, any values written into cells, the defaults each operation relies on, and how it writes its result; find every consumer of that result. Confirm that its sources exist in the Domain, and settle how the notebook's output on the agreed inputs is obtained, from a run of the unchanged notebook or its current table, and with which library versions. Design the models under the approved project structure and model language so that each step that shapes the published output has one owner, and translate each implicit dataframe behaviour explicitly rather than relying on a default of the new construct that only looks equivalent. Reproduce each such behaviour, including the ones that look like mistakes, and list each defect as follow-up work. Compare the published result with the notebook's output in each approved environment, check each behaviour the agreed inputs never exercise against the unchanged notebook where it can run, stating the gap where it cannot, handle the notebook as approved, and state what the comparison cannot prove.

### Compose

- capturing-requirements
- profiling-source-data
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- documenting-dbt-models
- verifying

### Ask first

- If unresolved, what counts as unchanged output: rows and values only, or also the relation name, column names, column order, types and materialization?
- If unresolved, does the published model take over the notebook's output relation, or do consumers move to it later as separate work?
- If unresolved, must the logic become SQL models under the project's layering conventions, or may some of it stay in a dbt Python model?
- If unresolved, how is the notebook run for the baseline (parameters, inputs, library versions, environment), which inputs form the comparison, is it exact or within an approved precision, and in which environments and time zones must it match?
- If unresolved, where the notebook's output shape depends on the data, such as one column per value found, what should the published model do when the data gains or loses such a value?
- If unresolved, once parity is accepted and any consumer cutover is complete, is the notebook kept and marked retired, or removed?

### Guardrails

- Do not edit the notebook or its captured output to make the comparison pass, and do not take the baseline from a run with stale state or cells out of order.
- Do not remove or disable the notebook before the parity result has been accepted, or while current consumers still use it; proven parity alone does not authorize removal.
- Do not correct a notebook defect, such as counting rows a group-by silently dropped; reproduce it, report it as follow-up work, and route any wanted output change to a separate change.
- Do not assume a dbt construct behaves like the dataframe operation it replaces; missing values, duplicates, empty groups and fills often differ.
- Do not treat a green build or a passing test suite as proof of parity; the proof is the comparison against the notebook's output.
- Do not widen a tolerance, or narrow the contract, the compared inputs or the approved precision, to make the comparison pass.
- Do not change the output of models outside the conversion.
- Do not extend the conversion into restructuring other models, incremental loading, scheduling, performance tuning, repointing dashboards or moving to another platform.
