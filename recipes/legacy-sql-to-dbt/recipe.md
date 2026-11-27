---
id: legacy-sql-to-dbt
title: Convert a legacy SQL script or view into a dbt model and prove parity
trigger:
  - A report or table is still produced by a hand-run SQL script, a database view or a procedure that rebuilds it in full each run, outside dbt, with no tests, lineage or review.
  - The team wants to retire a legacy script, but its consumers need proof that the dbt version returns exactly the same rows.
  - Transformation logic written as step-by-step SQL (temp tables, updates, deletes) has to move into the dbt project.
description: Bring a legacy SQL script, view or procedure that rebuilds its whole output each run into dbt as models that publish the same contract, proven against the legacy logic's own output on the same inputs, with legacy defects reproduced and reported as follow-up work.
pitch: Retire a hand-run SQL script by rebuilding it in dbt and proving the new models return exactly what the old one did.
job_category: re-engineer
area: transformation
readiness: supported
function:
  - cross-functional
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
    - motherduck
    - fabric_lakehouse
    - fabric_warehouse
    - redshift
    - databricks
  tools:
    - dbt
qualifiers:
  - Needs the tables the legacy SQL reads landed in the target; landing them belongs to an ingestion Recipe.
  - Needs the legacy output on the same inputs, from the legacy SQL or its current table.
  - Covers procedures that rebuild their whole output each run; ones keeping rows between runs use stored-procedure-to-dbt.
  - Row-history routines use scd-procedure-to-dbt-snapshot.
  - A procedure that writes several published tables uses split-multi-table-procedure-to-dbt.
  - A row-by-row or batched loop uses batched-loop-procedure-to-set-based-dbt.
  - Other writes and side effects of the legacy SQL, such as logging or audit rows, are reported, not reproduced.
  - Complete outcome assessed for duckdb_local only; the other listed platforms remain unassessed.
related:
  - prove-dbt-change-safe
  - dbt-full-refresh-to-incremental
  - stored-procedure-to-dbt
  - scd-procedure-to-dbt-snapshot
  - split-multi-table-procedure-to-dbt
  - batched-loop-procedure-to-set-based-dbt
  - translate-engine-specific-sql-to-dbt
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

- The published model keeps the approved contract, covering whichever of relation name, columns, column order, types, materialization and generated key values the approved contract counts as unchanged output.
- Published rows match the output of the unchanged legacy logic, with only an approved stand-in for the current date or time, on the agreed inputs at the approved precision, compared both ways with duplicate rows counted; any difference left is reported and parity is not claimed for it.
- The comparison can fail: a compared value changed beyond the approved precision, a lost row or an added duplicate row fails it.
- The match holds in each approved execution environment and time zone; independence from the time zone is required only where the consumer contract already includes it.
- Every legacy behaviour that affects the published output is reproduced, including implicit ones such as nulls that void a sum, inner joins that drop unmatched records or the source engine's collation; a rejection or failed run the model cannot reproduce follows the approved treatment.
- Each legacy defect found is listed with the output it affects, the rule it appears to break and what correcting it would change, as follow-up work.
- For material legacy behaviours the comparison inputs do not exercise, such as a boundary outside the compared period or a key with no match, parity is verified with the unchanged legacy logic or another approved oracle where one is available; otherwise the gap is stated.
- Parity is kept separate from cutover: where the published model takes over the consumer-facing interface, the legacy implementation stops writing it after parity is accepted and before the model first writes it, then is retired as approved; where consumers move later, it stays until cutover.
- Where the legacy SQL or its target table rejects an input or fails the run, such as a duplicate key or a value too wide for its column, the model fails the same way and leaves the published output as the legacy run leaves it, or where it cannot, follows the approved treatment, which is reported.
- Anything the comparison cannot prove is stated.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements. Read the legacy SQL end to end first, from its source of record, checking any copy against it byte for byte: its sources, every intermediate step, each update or delete, its window and filters, its joins and its null handling, and find every consumer of its output. Confirm that its sources exist in the Domain, and settle how the legacy output on the agreed inputs is obtained, from the legacy SQL or its current table; where both exist, compare them on the same inputs and report any difference before choosing. Reproduce the source engine's semantics wherever the target's differ in a way that can change the published output, such as collation, trailing spaces, null order, empty strings, division, rounding and dates. Design the models under the approved project structure so that each legacy step that shapes the published output has one owner. Reproduce each such behaviour, including the ones that look like mistakes, and list each defect as follow-up work. Compare the published result with the legacy output in each approved environment, keeping each comparison on the agreed inputs as a committed check for reruns while their approved retention lasts, check each behaviour the agreed inputs never exercise against the unchanged legacy logic or another approved oracle where one exists, stating the gap where none does, handle the legacy artifact as approved, and state what the comparison cannot prove.

### Compose

- capturing-requirements
- profiling-source-data
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- documenting-dbt-models
- verifying

### Ask first

- If unresolved, what counts as unchanged output: rows and values only, or also the relation name, column names, column order, types and materialization, and must generated or surrogate key values and how they are assigned stay the same?
- If unresolved, does the published model take over the legacy relation's name, or do consumers move to it later as separate work?
- If unresolved, which project structure and layering conventions must the models follow, or should they mirror the legacy SQL as one model?
- If unresolved, which parameters does the legacy SQL take, what value stands in for any current date or time it reads while comparing, which values and inputs form the comparison, are values compared exactly or within an approved precision, and in which environments and time zones must it match?
- If unresolved, once parity is accepted and any consumer cutover is complete, is the legacy artifact kept and marked retired, or removed?
- If unresolved, where does the baseline output come from (the legacy SQL run on the agreed inputs, its current table, or both where they agree), what happens when they differ, who approves it, and where may the frozen comparison inputs and legacy baseline be kept for reruns, and for how long?
- If unresolved, may the legacy SQL be run where it writes, and where: on the live source, on an approved copy, or only as its read-only query, and what other oracle may prove behaviour the agreed inputs never reach?
- If unresolved, where the legacy SQL or its target table rejects an input or fails the run, such as a duplicate key or a value too wide, what does a failed or partly applied run leave, and which approved treatment applies where the model cannot copy it?

### Guardrails

- Do not edit the legacy logic or its captured output to make the comparison pass; do not run anything that writes to the legacy source, or commit copies of source or legacy data to the repository, unless approved.
- Do not remove or disable the legacy artifact before the parity result has been accepted, or, except a takeover of its interface after acceptance, while current consumers still use it; proven parity alone does not authorize removal.
- Do not correct a legacy defect, such as turning an inner join into an outer join; reproduce it, report it as follow-up work, and route any wanted output change to a separate change.
- Do not treat a green build or a passing test suite as proof of parity; the proof is the comparison against the legacy output.
- Do not claim exact parity for output the legacy logic does not determine, such as ties in a ranking or values that vary between runs; leave it out of the comparison only as the approved comparison does, and report it as unproven.
- Do not let constructed proof inputs reach the published relations or the copies that stand for the legacy data; run them only in a separate, named test build, and report their results separately.
- Do not fix the stand-in for a current date or time into the published model; use it only for the comparison, and keep reading the clock where the legacy SQL does.
- Do not widen a tolerance, or narrow the contract, the compared inputs or the approved precision, to make the comparison pass.
- Do not change the output of models outside the conversion.
- Do not extend the conversion into restructuring other models, incremental loading, performance tuning, repointing dashboards or moving to another platform.
