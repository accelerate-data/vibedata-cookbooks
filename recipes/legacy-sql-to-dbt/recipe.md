---
id: legacy-sql-to-dbt
title: Convert a legacy SQL script or view into a dbt model and prove parity
trigger:
  - A report or table is still produced by a hand-run SQL script or a database view outside dbt, with no tests, lineage or review.
  - The team wants to retire a legacy script, but its consumers need proof that the dbt version returns exactly the same rows.
  - Transformation logic written as step-by-step SQL (temp tables, updates, deletes) has to move into the dbt project.
description: Bring a legacy SQL script or view into dbt as models that publish the same contract, proven against the legacy logic's own output on the same inputs, with legacy defects reproduced and reported as follow-up work.
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
  - Needs the legacy output on the same inputs, from the legacy SQL or its current table.
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

Convert <legacy_sql> into dbt models in the current Intent so that the published model can replace it for <consumers>. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Deliver the dbt models with evidence that the published result keeps the approved contract and matches the output of the unchanged legacy logic on the agreed inputs at the approved precision. Reproduce every legacy behaviour that affects the published output, including ones that look like mistakes, and report each defect as follow-up work; an output change someone wants belongs in a separate change. Handle the legacy artifact as approved, and state what the comparison cannot prove.

## Verified by

- The published model keeps the approved contract, covering whichever of relation name, columns, column order, types and materialization the approved contract counts as unchanged output, so its consumers need no change.
- Published rows match the output of the unchanged legacy logic on the agreed inputs at the approved precision; any difference left is reported and parity is not claimed for it.
- The match holds in each approved execution environment and time zone; independence from the time zone is required only where the consumer contract already includes it.
- Every legacy behaviour that affects the published output is reproduced, including implicit ones such as nulls that void a sum or inner joins that drop unmatched records.
- Each legacy defect found is listed with the output it affects, the rule it appears to break and what correcting it would change, as follow-up work.
- The models and the legacy logic also agree on behaviours the agreed inputs never reach, such as a boundary outside the compared period or a key with no match.
- The legacy artifact is handled as the approved policy says, whether it is kept and marked retired or removed.
- Anything the comparison cannot prove is stated.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements. Read the legacy SQL end to end first: its sources, every intermediate step, each update or delete, its window and filters, its joins and its null handling, and find every consumer of its output. Confirm that its sources exist in the Domain, and settle how the legacy output on the agreed inputs is obtained, from the legacy SQL or its current table. Design the models under the approved project structure so that each legacy step that shapes the published output has one owner. Reproduce each such behaviour, including the ones that look like mistakes, and list each defect as follow-up work. Compare the published result with the legacy output in each approved environment, cover each behaviour the agreed inputs never exercise another way, handle the legacy artifact as approved, and state what the comparison cannot prove.

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
- If unresolved, does the published model take over the legacy relation's name, or do consumers move to it later as separate work?
- If unresolved, which project structure and layering conventions must the models follow, or should they mirror the legacy SQL as one model?
- If unresolved, which inputs and period form the comparison, are values compared exactly or within an approved precision, and in which execution environments and time zones must the result match?
- If unresolved, after parity is proven, is the legacy artifact kept and marked retired, or removed?
- If unresolved, when the legacy SQL cannot run on the target engine, where does the baseline output come from, for example the legacy relation's current table, and who approves it?

### Guardrails

- Do not edit the legacy logic or its captured output to make the comparison pass.
- Do not correct a legacy defect, such as turning an inner join into an outer join; reproduce it, report it as follow-up work, and route any wanted output change to a separate change.
- Do not treat a green build or a passing test suite as proof of parity; the proof is the comparison against the legacy output.
- Do not claim exact parity when the legacy output itself varies from run to run; report what cannot be proven.
- Do not widen a tolerance, or narrow the contract, the compared inputs or the approved precision, to make the comparison pass.
- Do not change the output of models outside the conversion.
- Do not extend the conversion into restructuring other models, incremental loading, performance tuning, repointing dashboards or moving to another platform.
