---
id: materialized-view-to-dbt
title: Convert a materialized view into a dbt model and preserve its required refresh semantics
trigger:
  - Warehouse logic lives in a materialized view that nobody can test, review or trace, and the team wants it in the dbt project.
  - Consumers depend on how the view refreshes, so the dbt model must keep its refresh behaviour as well as its rows.
  - The view's refresh is opaque, and the team wants its refresh rule stated and owned in code before the view is retired.
description: Bring a materialized view into dbt as a model that publishes the same contract and refreshes under the same approved rule, proven against the view's own output after each compared refresh, with view defects reproduced and reported as follow-up work.
pitch: Retire a materialized view by rebuilding it in dbt with the same refresh behaviour and proving every refresh returns what the view did.
job_category: re-engineer
area: transformation
readiness: supported
domain_objects:
  - materialized_view
  - refresh_policy
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
  - duckdb_local has no materialized views; there the view is a table that its refresh script maintains.
  - Needs the view's definition, its refresh rule and its output at known refresh points on the same inputs.
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

Convert <materialized_view> into a dbt model in the current Intent so that it can replace the view for <consumers> under the view's approved refresh behaviour. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Deliver the dbt model and its run definition, with evidence that after each compared refresh the published result keeps the approved contract and matches the view's output on the same inputs at the approved precision, and that a full rebuild relates to the refreshed result as the approved refresh rule says. Reproduce every view behaviour that affects the published output, including ones that look like mistakes, and report each defect as follow-up work. Handle the view as approved, and state what the comparison cannot prove.

## Verified by

- The published model keeps the approved contract, covering whichever of relation name, columns, column order, types and materialization the approved contract counts as unchanged output.
- After each compared refresh, published rows match the view's output on the same inputs at the approved precision; any difference left is reported and parity is not claimed for it.
- Each refresh changes only what the approved refresh rule lets it change, such as the window it recomputes, and rows outside that reach keep their earlier values, as they do in the view.
- Records that arrive after the refresh can reach them are treated as the approved refresh rule says, and any difference between a full rebuild and the refreshed result is exactly the records that rule leaves out, no more and no fewer, and is reported.
- Where the run definition is in scope, it states what each scheduled refresh runs and on what cadence, and how a first run, a full rebuild and a missed refresh behave.
- The match holds in each approved execution environment and time zone.
- Every view behaviour that affects the published output is reproduced, and each defect found is listed with the output it affects, the rule it appears to break and what correcting it would change, as follow-up work.
- Refresh behaviours the compared refreshes do not exercise, such as a missed refresh or a record on the window edge, are verified against the view's refresh logic or another approved oracle where one exists; otherwise the gap is stated.
- Output parity is kept separate from consumer cutover: the view is retired as approved only after parity is accepted and its consumers read the dbt model.
- Anything the comparison cannot prove is stated.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements. Read the view end to end first: its definition, sources, filters, joins, null handling and aggregation, and its refresh rule, meaning what each refresh recomputes and by which key or window, its trigger and cadence, what a full refresh does and what readers see while it runs; then find every consumer of its output. Confirm that its sources exist in the Domain and settle how the view's output at each compared refresh point is obtained. Choose the materialization and refresh mechanism from the approved refresh rule and the source evidence, for example a full rebuild per run, an incremental model that replaces a recomputed window, or partition replacement, and state what it relies on, such as a landing or update marker, and what it would miss. Compare the published result with the view after each compared refresh, including refreshes that bring new and late records, compare a full rebuild with the refreshed result, reproduce each view behaviour that shapes the output, list each defect as follow-up work, handle the view as approved, and state what the comparison cannot prove.

### Compose

- capturing-requirements
- profiling-source-data
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- documenting-dbt-models
- verifying

### Ask first

- If unresolved, what counts as unchanged output: rows and values only, or also the relation name, column names, column order, types and materialization; and does the model take over the view's name, or do consumers move later?
- If unresolved, which refresh behaviours must the model keep: full recompute or incremental, the window or key each refresh recomputes, its trigger and cadence, a staleness limit, and whether readers may see a partly refreshed result?
- If unresolved, how are records that arrive after the refresh can reach them treated: left out as the view leaves them, or recovered by a later refresh or rebuild?
- If unresolved, must a full rebuild equal the refreshed result, or may it include the records the refreshes missed?
- If unresolved, which refresh points, inputs and precision form the comparison, and in which execution environments and time zones must the result match?
- If unresolved, where does the view's output at each compared refresh point come from when it cannot be re-run on the same inputs, and who approves it?
- If unresolved, does the work deliver the model only, or also its run definition (selection, command and cadence), and is scheduling it on an orchestrator in scope?
- If unresolved, once parity is accepted and consumers read the dbt model, is the view kept and marked retired, or dropped?

### Guardrails

- Do not edit the view, its refresh logic or its captured output to make the comparison pass.
- Do not drop or disable the view before the parity result has been accepted, or while consumers still read it.
- Do not change the refresh behaviour, such as recovering late records or widening the recomputed window, without approval; report a wanted change as follow-up work.
- Do not correct a view defect; reproduce it, report it as follow-up work, and route any wanted output change to a separate change.
- Do not treat a green build or a matching final state as proof of parity; the proof is the comparison after each refresh.
- Do not claim exact parity when the view's own output varies from run to run; report what cannot be proven.
- Do not widen a tolerance, or narrow the contract, the compared refreshes or the approved precision, to make the comparison pass.
- Do not change the output of models outside the conversion.
- Do not extend the conversion into scheduling on an orchestrator, restructuring other models, performance tuning, repointing dashboards or moving to another platform.
