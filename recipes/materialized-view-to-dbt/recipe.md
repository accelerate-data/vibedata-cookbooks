---
id: materialized-view-to-dbt
title: Convert a materialized view into a dbt model and preserve its required refresh semantics
trigger:
  - Warehouse logic lives in a materialized view that nobody can test, review or trace, and the team wants it in the dbt project.
  - Consumers depend on what each refresh of the view produces, so the dbt model must keep what every refresh computes, not only its final rows.
  - The view's refresh is opaque, and the team wants its refresh rule stated and owned in code before the view is retired.
description: Bring a materialized view into dbt as a model that publishes the same contract and computes each refresh under the same approved rule, proven against the view's own output after each compared refresh, with view defects reproduced and reported as follow-up work.
pitch: Retire a materialized view by rebuilding it in dbt and proving each compared refresh matches the view's.
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
    - fabric_lakehouse
    - redshift
  tools:
    - dbt
qualifiers:
  - Not yet assessed end to end on fabric_lakehouse or redshift.
  - Needs the view's definition (Studio can't yet read it on these targets), refresh rule and output at refresh points.
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

Convert <materialized_view> into a dbt model in the current Intent so that it can replace the view for <consumers>, computing each refresh as the view's approved refresh rule does. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Deliver the dbt model, and its run definition or execution mechanism where that is in scope, with evidence that after each compared refresh the published result keeps the approved contract and matches the view's output on the same inputs at the approved precision, and, where the view's full refresh is available, that a full rebuild matches it. Reproduce every view behaviour that affects the published output, including ones that look like mistakes, and report each defect as follow-up work. Claim the view's operational refresh guarantees, such as cadence, a staleness limit or what readers see during a refresh, only where the approved scope gives them to the delivered run definition or execution mechanism and they are verified. Handle the view as approved, and state what the comparison cannot prove.

## Verified by

- The published model keeps the approved contract, covering whichever of relation name, columns, column order, types and materialization the approved contract counts as unchanged output.
- After each compared refresh, published rows match the view's output on the same inputs at the approved precision; any difference left is reported and parity is not claimed for it.
- Each refresh changes only what the approved refresh rule lets it change, such as the window it recomputes, and rows outside that reach keep their earlier values, as they do in the view.
- Where the view's full refresh on the same inputs is available from the view or another approved oracle, a full rebuild matches it at the approved precision, and what the view's refresh rule leaves out of the refreshed result is identified and reported; otherwise the gap is stated.
- The view's operational guarantees (cadence, staleness, what readers see mid-refresh) that the approved scope gives the delivered run definition or execution mechanism are enforced and verified; its other guarantees are recorded as cutover or unverified requirements, not claimed.
- Where a run definition or execution mechanism is in scope, it states what each scheduled refresh runs and on what cadence, and how a first run, a full rebuild and a missed refresh behave.
- The match holds in each approved execution environment and time zone.
- Every view behaviour that affects the published output is reproduced, and each defect found is listed with the output it affects, the rule it appears to break and what correcting it would change, as follow-up work.
- Refresh behaviours the compared refreshes do not exercise, such as a missed refresh or a record on the window edge, are verified against the view's refresh logic or another approved oracle where one exists; otherwise the gap is stated.
- Output parity is kept separate from consumer cutover: where the dbt model takes over the view's consumer-facing name, the view is retired as approved after parity is accepted; where consumers move later, the view stays available until the cutover.
- Anything the comparison cannot prove is stated.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements. Read the view end to end first: its definition, sources, filters, joins, null handling and aggregation, and its refresh rule, meaning what each refresh recomputes and by which key or window, its trigger and cadence, what a full refresh does and what readers see while it runs; then find every consumer. Confirm that its sources exist in the Domain and settle how the view's output at each compared refresh point is obtained. Choose the materialization and refresh mechanism within the approved contract, from the approved refresh rule and the source evidence, for example a full rebuild per run, an incremental model that replaces a recomputed window, or partition replacement, and state what it relies on, such as a landing or update marker, and what it would miss. Separate what each refresh computes, which the model owns, from operational guarantees such as cadence, staleness and reader visibility, which depend on how the model is run: enforce and verify those the approved scope gives the run definition or execution mechanism, and record the rest as cutover or unverified requirements. Compare the published result with the view after each compared refresh, including refreshes that bring new and late records where the approved comparison has them, and compare a full rebuild with the view's full refresh where one is available.

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
- If unresolved, what does each refresh of the view compute: full recompute or incremental, and the window or key it recomputes?
- If unresolved, what does the view's refresh rule do with records that arrive after a refresh can reach them, and what does its full refresh produce?
- If unresolved, which refresh points, inputs and precision form the comparison, and in which execution environments and time zones must the result match?
- If unresolved, where does the view's output at each compared refresh point come from when it cannot be re-run on the same inputs, and who approves it?
- If unresolved, does the work deliver the model only, or also a run definition or execution mechanism (selection, command, cadence, scheduling), and which of the view's operational guarantees (cadence, staleness, whether readers may see a partly refreshed result) must it enforce?
- If unresolved, once parity is accepted and consumers read the dbt model, is the view kept and marked retired, or dropped?

### Guardrails

- Do not edit the view, its refresh logic or its captured output to make the comparison pass.
- Do not drop or disable the view before the parity result has been accepted or, where consumers move later, before they have moved.
- Do not change what the view's refresh computes, such as recovering records the view's rule leaves out or widening the recomputed window, or correct a view defect; reproduce the view's behaviour and report any wanted change as follow-up work for a separate change.
- Do not treat a green build or a matching final state as proof of parity; the proof is the comparison after each compared refresh.
- Do not claim exact parity when the view's own output varies from run to run; report what cannot be proven.
- Do not widen a tolerance, or narrow the contract, the compared refreshes or the approved precision, to make the comparison pass.
- Do not change the output of models outside the conversion.
- Do not extend the conversion beyond the approved scope, for example into restructuring other models, performance tuning, repointing dashboards or moving to another platform.
