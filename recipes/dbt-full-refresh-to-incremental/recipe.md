---
id: dbt-full-refresh-to-incremental
title: Convert a full-refresh dbt model to incremental and show the runtime delta
trigger:
  - A dbt model is correct but a full refresh is too slow or too expensive to run routinely, and gets slower as history grows.
  - A full-refresh model needs to become incremental without changing what its consumers see.
  - Source records can arrive late, arrive more than once, or change after they were first loaded.
description: Convert an existing full-refresh dbt model to incremental using a strategy chosen from source behaviour and approved requirements, keeping consumer-visible output identical to a full refresh, handling late, repeated and changed records under the approved rules, and reporting the observed runtime change and any defects or gaps found.
pitch: Make a slow full-refresh dbt model incremental and prove both the output parity and the runtime saving.
job_category: re-engineer
area: transformation
readiness: supported
domain_objects:
  - dbt_model
  - consumer_contract
  - incremental_strategy
  - approved_baseline
  - runtime_measurement
  - follow_up
works_with:
  platforms:
    - duckdb_local
  tools:
    - dbt
qualifiers:
  - Complete outcome assessed for duckdb_local only; the other four Studio targets remain unassessed.
  - Needs source evidence of how new, changed and late records can be identified, or an approved lateness bound.
  - Downstream models with their own incremental filters may still miss late rows; converting them is separate work.
  - Structural refactors with no materialization change belong to the dbt-refactor-output-identical Recipe.
related:
  - prove-dbt-change-safe
evidence:
  features:
    - profiling-source-data
    - generating-dbt-model
    - dbt-unit-testing
    - running-dbt-in-sandbox
    - verifying
  evals: []
---

## Prompt

Convert <target_model> from a full refresh to an incremental model in the current Intent, so routine runs avoid rebuilding everything while <consumers> see exactly what a full refresh would give them. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only what they leave open: which models are in scope, the grain, key and duplicate or update rule, how the source signals new, changed, late and deleted records, how late a record may arrive, whether the model may carry internal tracking columns, how output and runtime are compared, and what to do with a defect that conflicts with parity. Choose the incremental strategy from that source behaviour and the approved requirements, and state what the strategy relies on. Build the baseline from the unchanged code on the same inputs and engine, and compare the incremental result with it in both directions. Show that a rerun with nothing new changes nothing, that the agreed late, repeated and changed records land as approved, and how the model's own run time changed. Report defects, assumptions and downstream gaps instead of fixing them silently.

## Verified by

- Consumer-visible columns keep their names, order and types, and any column added to the relation is one the user approved as internal and no consumer reads.
- On the approved comparison slice, consumer-visible rows match a fresh full-refresh baseline of the unchanged code as multisets in both directions, with no tolerance the user did not approve.
- After incremental runs, the relation equals a full refresh over the same source population, including any approved internal columns.
- A rerun with nothing new changes no row and adds no duplicate at the approved grain.
- Every late, repeated, changed or deleted record the approved requirements cover lands as a full refresh would show it, across run boundaries as well as within one run.
- The chosen strategy is justified from source evidence, and what it relies on, such as an append-only source, a reliable change marker or a lateness bound, is stated with what it would miss if that does not hold.
- Runtime before and after comes from observed runs, reports the model's own execution time apart from fixed tool start-up, and states the run conditions and the data each side processed.
- The result does not change with the session time zone.
- Declared grain, source identifiers and loader-row identity are compared with evidence, and each defect, such as distinct records that share a key or a tie the duplicate rule leaves open, is disclosed with an approved fix or a follow-up.
- Downstream models whose own incremental filters would miss a record this model now picks up are reported.
- The cutover is stated: whether the existing relation must be rebuilt once before the first incremental run.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements. Read the target model, its source and every consumer, and check which columns each consumer reads. Profile the source to learn how it behaves: whether records are only appended or also updated and deleted, whether it carries a change marker such as an updated_at column, CDC operations or version identifiers, how batches, loads or partitions are marked, how late records arrive relative to event time, and how often keys repeat. Compare the declared grain with source and loader identity, and settle any conflict with parity before implementing. Choose the strategy that the evidence and the approved requirements support, for example append-only inserts, a change-marker or batch watermark, partition replacement, or a bounded lookback when an approved lateness bound makes it complete. Apply the same duplicate and update rule as the full refresh, including when an earlier version is already stored. Build the baseline from the unchanged code first. Then run the incremental path from an earlier state, land the agreed late, repeated and changed cases, rerun with nothing new, and compare against both the baseline and a full refresh of the same population. Time each path from the same starting state, separate the model's own execution from tool start-up, and state what each side processed. Report the defects found, the strategy's assumptions, downstream gaps and the cutover step.

### Compose

- profiling-source-data
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which models are converted now, and do sibling models built the same way follow in a later piece of work?
- If unresolved, what are the grain, key and duplicate or update rule, and is today's behaviour preserved even where distinct records share a key, or is identity changed under an approved contract and baseline change?
- If unresolved, how does the source signal new, changed and deleted records, and can that signal be trusted, for example whether a load or update marker always increases?
- If unresolved, which late, repeated and changed records must the incremental run handle, how late can a record arrive, and what outcome does each case require?
- If unresolved, may the model carry internal tracking columns that no consumer reads, or must its column set stay exactly as it is today?
- If unresolved, which slice is compared, exactly or within an approved precision, and how is runtime measured: which runs, how many, and under which conditions?
- If unresolved, is a defect that conflicts with parity preserved and logged as a follow-up, or fixed under an approved contract and baseline change?

### Guardrails

- Do not pick an incremental strategy the source cannot support: an event-time filter or lookback needs an approved lateness bound, and a watermark needs a marker that reliably increases.
- Do not let the incremental path resolve repeated or changed records differently from the full refresh, within a run or across runs.
- Do not invent a unique key to make the incremental materialization work, and do not treat a stable rerun as proof of business identity.
- Do not change what consumers see to make incremental processing easier, and do not add columns beyond the ones the user approved.
- Do not present predicted performance, or wall-clock time dominated by tool start-up, as the runtime saving; report what was observed and what each run processed.
- Do not silently fix a defect or replace the baseline to hide a semantic change; parity with the approved contract remains the acceptance gate.
- Do not write to the shared source data; simulate new landings in an isolated, clearly labelled copy.
- Do not extend the work to downstream models, sibling models or warehouse tuning beyond the approved scope.
