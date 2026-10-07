---
id: legacy-sql-to-dbt
title: Convert a legacy SQL script or view into a dbt model and prove parity
trigger:
  - A report or table is still produced by a hand-run SQL script or a database view outside dbt, with no tests, lineage or review.
  - The team wants to retire a legacy script, but its consumers need proof that the dbt version returns exactly the same rows.
  - Transformation logic written as step-by-step SQL (temp tables, updates, deletes) has to move into the dbt project's layers.
description: Bring a legacy SQL script or view into dbt as layered models that publish the same contract, proven against the legacy logic's own output on the same inputs, with every legacy defect reproduced and listed rather than silently fixed.
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

Convert <legacy_sql> into dbt models in the current Intent so that <consumers> keep getting the same result from a tested, reviewed model instead of the legacy script or view. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Deliver the dbt models, built under the approved layering, with evidence that the published result keeps the approved contract and matches the output of the unchanged legacy logic on the agreed inputs. Reproduce every legacy behaviour, including the ones that look like mistakes, and report each defect as follow-up work rather than correcting it. Handle the legacy artifact the approved way, and state what the comparison cannot prove.

## Verified by

- The published model keeps the approved contract, covering whichever of relation name, columns, column order, types and materialization the approved contract counts as unchanged output, so its consumers need no change.
- Published rows match the output of the unchanged legacy logic on the agreed inputs, at the approved precision; every difference is explained, never absorbed by a tolerance the user did not approve.
- Every behaviour of the legacy logic is reproduced, including implicit ones such as nulls that void an arithmetic sum, inner joins that drop unmatched records, inclusive or date-only window bounds, and labels merged by an update.
- Each legacy defect found is listed with the output it affects and its follow-up, stating the intended rule and what correcting it would change.
- The models and the legacy logic also agree on behaviours the agreed inputs never reach, such as a window boundary outside the compared period or a key with no match.
- An existing model is reused only where the published output stays identical.
- The match holds in each approved execution environment and time zone; independence from the time zone is required only where the consumer contract already includes it.
- The conversion changes neither the configuration nor the output of models outside it.
- The legacy artifact is handled as approved, and the comparison can be re-run from what remains.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements. Read the legacy SQL end to end first: its sources, every intermediate step, each update or delete, its window and filters, its joins and its null handling, and find every consumer of its output. Confirm that its sources exist in the Domain and that it runs on the target engine; if not, settle how its baseline output is obtained before converting. Keep the legacy logic and its output on the agreed inputs as the baseline. Design the models under the approved layering so that each legacy step, from source reads through joins, relabels and filters to the published result, has one owner. Reuse an existing model only where the published output is shown to stay identical. Reproduce each legacy behaviour, including the ones that look like mistakes, and list each defect with the output it affects and its follow-up. Compare the published result with the legacy output on the agreed inputs, cover each behaviour those inputs never exercise, handle the legacy artifact the approved way, and state what the comparison cannot prove.

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
- If unresolved, which inputs and period form the comparison, are values compared exactly or within an approved precision, and in which execution environments and time zones must the result match?
- If unresolved, is any change to the legacy output actually wanted? If so, it belongs in a separate change, not in this conversion.
- If unresolved, after parity is proven, is the legacy artifact kept and marked retired, or removed?
- If unresolved, when the legacy SQL cannot run on the target engine, how is its baseline output obtained and who approves it?

### Guardrails

- Do not edit the legacy logic or its captured output to make the comparison pass; a difference is resolved in the models.
- Do not correct a legacy defect, such as adding the house null handling to a sum or turning an inner join into an outer join; reproduce it and report it as follow-up work.
- Do not substitute an existing model for a legacy step because it looks equivalent; reuse it only when the published output is shown to be identical.
- Do not treat a green build or a passing test suite as proof of parity; the proof is the comparison against the legacy output.
- Do not widen a tolerance, narrow the compared inputs or drop a column from the comparison to make it pass.
- Do not change the configuration or output of models outside the conversion.
- Do not extend the conversion into restructuring other models, incremental loading, performance tuning, repointing dashboards or moving to another platform.
