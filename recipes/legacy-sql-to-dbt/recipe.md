---
id: legacy-sql-to-dbt
title: Convert a legacy SQL script or view into a dbt model and prove parity
trigger:
  - A report or table is still produced by a hand-run SQL script or a database view outside dbt, with no tests, lineage or review.
  - The team wants to retire a legacy script, but its consumers need proof that the dbt version returns exactly the same rows.
  - Transformation logic written as step-by-step SQL (temp tables, updates, deletes) has to move into the dbt project's layers.
description: Bring a legacy SQL script or view into dbt as layered models that publish the same contract, proven by a two-way row comparison against the legacy logic's own output on the same inputs, with every legacy defect reproduced and listed rather than silently fixed.
pitch: Retire a hand-run SQL script by rebuilding it in dbt and proving the new models return exactly what the old one did.
job_category: re-engineer
area: transformation
readiness: supported
domain_objects:
  - legacy_sql
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
  - An exact baseline needs the legacy SQL to run on the target engine against the same inputs.
  - Parity is proven only on the compared inputs; a rule those inputs never exercise needs its own case.
related:
  - prove-dbt-change-safe
  - dbt-full-refresh-to-incremental
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

Convert <legacy_sql> into dbt models in the current Intent so that <consumers> keep getting the same result from a tested, reviewed model instead of the legacy script or view. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only what they leave open: what counts as unchanged output, how the conversion is layered and which existing models it may reuse, the comparison inputs and precision, what to do with a defect in the legacy logic, and what happens to the legacy artifact afterwards. Capture the legacy logic and its output on the agreed inputs before writing any model, then build the dbt models under the approved layering, compare the published result with the legacy output in both directions under the approved contract, reproduce or resolve every legacy behaviour under the approved rule, and retire the legacy artifact the approved way. Report every difference with its explanation and state what the comparison cannot prove.

## Verified by

- The legacy logic and its output on the agreed inputs are captured unchanged before conversion, and the comparison uses that captured output or a fresh run of the unchanged logic on the same inputs and engine.
- The published model keeps the approved contract, covering whichever of relation name, columns, column order, types and materialization the user counts as unchanged output, so its consumers need no change.
- Published rows match the legacy output as multisets in both directions with equal row counts on the agreed comparison inputs; any difference is listed row by row with its explanation, never absorbed by a tolerance the user did not approve.
- Every behaviour of the legacy logic is either reproduced or changed under an approved resolution, including implicit ones such as nulls that void an arithmetic sum, inner joins that drop unmatched records, inclusive or date-only window bounds, and labels merged by an update.
- Each legacy defect found is listed with the output it affects and its follow-up, stating the intended rule and what correcting it would change.
- Behaviours the comparison inputs never reach, such as a window boundary outside the compared period or a key with no match, have their own case showing the models and the legacy logic agree.
- An existing model is reused only where the published output stays identical; each place the conversion reads the legacy logic's own sources instead carries its reason.
- Repeated builds give identical results, the result does not change with the session time zone, and the conversion changes neither the configuration nor the output of models outside it.
- The legacy artifact is retired under the approved rule, and the comparison can be re-run from what remains.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements. Read the legacy SQL end to end first: its sources, every intermediate step, each update or delete, its window and filters, its joins and its null handling, and find every consumer of its output. Confirm that its sources exist in the Domain and that it runs on the target engine; if not, agree how the baseline is obtained first. Capture the legacy logic and its output on the agreed inputs and leave both unchanged from then on. Agree the contract, layering, reuse and comparison approach, then design the models under the approved layering so that each legacy step, from source reads through joins, relabels and filters to the published result, has one owner. Where an existing model looks equivalent, prove its output is identical before reusing it; a conformed relation can hold the same rows yet change sums of floating-point values through a different row order. Handle each legacy behaviour, including the ones that look like mistakes, under the approved defect rule, and list each defect with the output it affects and its follow-up. Compare in both directions on the agreed inputs and on any wider window the inputs allow, add a case for each behaviour those inputs never exercise, and make floating-point comparisons deterministic without changing how the rest of the project builds. Retire the legacy artifact the agreed way and state what the comparison cannot prove.

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
- If unresolved, should the conversion follow the project's staging, intermediate and mart layers, or mirror the legacy SQL as one model, and may it reuse existing models where their output is identical?
- If unresolved, which inputs and period form the comparison, and are values compared exactly or within an approved precision for floating-point columns?
- If unresolved, when the legacy logic has a defect, is its behaviour reproduced and listed as a follow-up, or corrected under an approved change to the expected output?
- If unresolved, after parity is proven, is the legacy artifact kept and marked retired, or removed?
- If unresolved, when the legacy SQL cannot run on the target engine, how is its baseline output obtained and who approves it?

### Guardrails

- Do not edit the legacy logic or its captured output to make the comparison pass; a difference is resolved in the models.
- Do not silently correct a legacy defect, such as adding the house null handling to a sum or turning an inner join into an outer join; reproduce it and list it, or obtain an approved change.
- Do not substitute an existing model for a legacy step because it looks equivalent; reuse it only when the published output is shown to be identical.
- Do not treat a green build or a passing test suite as proof of parity; the proof is the two-way comparison against the legacy output.
- Do not widen a tolerance, narrow the compared inputs or drop a column from the comparison to make it pass.
- Do not change the configuration or output of models outside the conversion, including engine settings used to make comparisons deterministic.
- Do not extend the conversion into restructuring other models, incremental loading, performance tuning, repointing dashboards or moving to another platform.
