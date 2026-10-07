---
id: dbt-full-refresh-to-incremental
title: Convert a full-refresh dbt model to incremental and show the runtime delta
trigger:
  - A dbt model is correct but a full refresh is too slow or too expensive to run routinely, and gets slower as history grows.
  - A full-refresh model needs to become incremental without changing what its consumers see.
  - Raw files are not deduplicated, and a newly landed file can carry records for periods that are already loaded.
description: Convert an existing full-refresh dbt model to incremental so each run processes only newly landed data, keeping consumer-visible output identical to a full refresh, handling late and repeated arrivals under the approved rules, and reporting the observed runtime change and any defects or gaps found.
pitch: Make a slow full-refresh dbt model incremental and prove both the output parity and the runtime saving.
job_category: re-engineer
area: transformation
readiness: supported
domain_objects:
  - dbt_model
  - consumer_contract
  - landing_watermark
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
  - Needs a per-row arrival marker in the source, such as a load timestamp, that increases with each landing.
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

Convert <target_model> from a full refresh to an incremental model in the current Intent, so each run processes only newly landed source data while <consumers> see exactly what they see today. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only what they leave open: which models are in scope, the grain, key and duplicate rule, what marks data as newly landed, which late and repeated arrivals must be handled, whether the model may carry internal tracking columns, how output and runtime are compared, and what to do with a defect that conflicts with parity. Build the baseline from the unchanged code on the same inputs and engine, keep the approved duplicate rule across run boundaries, and compare the incremental result with the baseline in both directions. Show that a rerun with nothing new changes nothing, that the agreed late and repeated arrivals land as approved, and how the model's own run time changed. Report defects, assumptions and downstream gaps instead of fixing them silently.

## Verified by

- Consumer-visible columns keep their names, order and types, and any column added to the relation is one the user approved as internal and no consumer reads.
- On the approved comparison slice, consumer-visible rows match a fresh full-refresh baseline of the unchanged code as multisets in both directions, with no tolerance the user did not approve.
- After incremental runs, the relation equals a full refresh over the same source population on every column, including any approved internal columns.
- A rerun with nothing newly landed changes no row and leaves exactly one row per key.
- A late record for a period already loaded is picked up because the run tracks arrival, not event time, and an exact repeat of a loaded record adds no row and leaves the stored row unchanged.
- The approved duplicate rule holds across run boundaries: a key arriving later from a source the rule ranks earlier replaces the stored row, one the rule ranks later is ignored, and repeats within one batch resolve by the same rule.
- Runtime before and after comes from observed runs, reports the model's own execution time apart from fixed tool start-up, and states the run conditions and the data each side processed.
- The result does not change with the session time zone.
- Declared grain, source identifiers and loader-row identity are compared with evidence, and each defect, such as distinct records that share a key or a tie the duplicate rule leaves open, is disclosed with an approved fix or a follow-up.
- The arrival-order assumption is stated with what it would skip, and downstream models whose own filters would miss a late row this model now absorbs are reported.
- The cutover is stated: whether the existing relation must be rebuilt once before the first incremental run.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements. Read the target model, its source and every consumer before changing anything, and check which columns each consumer actually reads. Profile the source for what identifies a record, how often keys repeat across and within files, and which loader columns mark a landing; record whether landing times strictly increase. Compare the declared grain with source and loader identity, and settle any conflict with parity before implementing. Choose the incremental strategy, key and landing filter from the approved contract. Filter on arrival, never on event time, so late records for loaded periods are not lost. Where the duplicate rule picks a survivor by source order, carry what the rule needs, so a later run can replace a stored row that the rule ranks behind a new one. Build the baseline from the unchanged code first. Then run the incremental path from an earlier state, land the agreed late and repeated cases, rerun with nothing new, and compare against both the baseline and a full refresh of the same population. Time each path from the same starting state, separate the model's own execution from tool start-up, and state what each side processed. Report the defects found, the arrival assumption, downstream gaps and the cutover step.

### Compose

- profiling-source-data
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which models are converted now, and do sibling models built the same way follow in a later piece of work?
- If unresolved, what are the grain, key and duplicate rule, and is today's behaviour preserved even where distinct records share a key, or is identity changed under an approved contract and baseline change?
- If unresolved, what marks a record as newly landed, and can a new landing reuse an arrival marker already seen?
- If unresolved, which late and repeated arrivals must the incremental run handle, how far back can a late record fall, and what outcome does each case require?
- If unresolved, may the model carry internal tracking columns that no consumer reads, or must its column set stay exactly as it is today?
- If unresolved, which slice is compared, exactly or within an approved precision, and how is runtime measured: which runs, how many, and under which conditions?
- If unresolved, is a defect that conflicts with parity preserved and logged as a follow-up, or fixed under an approved contract and baseline change?

### Guardrails

- Do not filter incremental runs on event time or a fixed lookback window unless the user approved it; a late record for an already-loaded period would be silently dropped.
- Do not let the first copy to arrive win when the approved duplicate rule ranks copies by source order; a late copy that ranks earlier must replace the stored row.
- Do not invent a unique key to make the incremental materialization work, and do not treat a stable rerun as proof of business identity.
- Do not change what consumers see to make incremental processing easier, and do not add columns beyond the ones the user approved.
- Do not present predicted performance, or wall-clock time dominated by tool start-up, as the runtime saving; report what was observed and what each run processed.
- Do not silently fix a defect or replace the baseline to hide a semantic change; parity with the approved contract remains the acceptance gate.
- Do not write to the shared source data; simulate new landings in an isolated, clearly labelled copy.
- Do not extend the work to downstream models, sibling models or warehouse tuning beyond the approved scope.
