---
id: dbt-full-refresh-to-incremental
title: Convert a full-refresh dbt model to incremental and show the runtime delta
trigger:
  - A dbt model is correct but a full refresh is too slow or too expensive to run routinely, and gets slower as history grows.
  - The nightly build is past its window, and one full-refresh model accounts for most of it.
  - A full-refresh model needs to become incremental without changing what its consumers see.
description: Convert an existing full-refresh dbt model to incremental with a strategy chosen from source behaviour and the approved requirements, prove that consumers still see what a full refresh would show under the approved contract, and record the run time before and after.
pitch: Make a slow full-refresh dbt model incremental, prove its output still matches, and measure the runtime change.
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
  - Downstream incremental models may still miss late, changed or deleted rows; fixing them is separate work.
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

Convert <target_model> from a full refresh to an incremental model, so routine runs no longer rebuild it from scratch while <consumers> still see what a full refresh would show under the approved contract. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Choose the incremental strategy from how the source adds, changes, deletes and delivers late records and from the approved requirements, and state what the strategy relies on and what it would miss. Deliver the converted model, evidence that its output matches a baseline of the unchanged code after incremental runs and after a rerun with nothing new, and its run time before and after. A defect found along the way, or an output change someone wants, is reported as separate work; it is not part of this conversion.

## Verified by

- Every column a consumer reads keeps its approved contract, and any column added to the relation is internal: no consumer reads it and the approved contract allows it.
- After incremental runs, the rows consumers read match a full-refresh baseline of the unchanged code on the agreed comparison slice, over the same source data and under the approved contract, at the approved precision and in each approved execution environment and time zone.
- The agreed late, repeated, changed and deleted cases end up as the full refresh would show them under the approved contract, within one run and across runs.
- Every difference from the full refresh that the approved contract accepts, such as a record later than an approved lateness bound, is listed.
- A rerun with nothing new adds, removes or changes no row a consumer reads.
- The chosen strategy is justified from source evidence and the approved requirements, and what it relies on, such as an append-only source, a reliable change marker or a lateness bound, is stated with what it would miss if that does not hold.
- Run time before and after is recorded from observed runs, with the conditions and the data each side processed.
- Defects found and output changes requested during the conversion are reported as follow-up work, with the output they affect, and are not applied; anything the comparison cannot prove is stated.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements. Read the target model and every consumer, noting which columns each reads. Profile the source to learn how it behaves: whether records are only appended or also updated and deleted, whether it carries a change marker such as updated_at, CDC operations or version identifiers, how loads, batches or partitions are marked and whether a new record can arrive behind a mark already processed, and how late records arrive. Choose the strategy the evidence and the approved requirements support, for example append-only inserts, a change-marker or batch watermark, partition replacement, or a bounded lookback or microbatch when an approved lateness bound makes it complete; if none is safe, report that instead of converting. Keep the full refresh's handling of repeated, changed and deleted records, including when an earlier version is already stored. Build a baseline from the unchanged code, then compare consumer-visible output after an incremental run from an earlier state, after the agreed cases, and after a rerun with nothing new. Time both paths on the same source data, apart from fixed start-up time. Report defects and wanted output changes as follow-up work, the strategy's assumptions, downstream models that would miss a late or changed record, and any full refresh the strategy still needs, once at cutover or periodically.

### Compose

- profiling-source-data
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which models are converted, and what is the consumer contract: which columns consumers read, whether internal columns may be added, which slice is compared, and must rows match exactly or within an approved precision?
- If unresolved, how does the source add, change and delete records, can those signals be trusted, and how late can a record arrive?
- If unresolved, may a record later than the approved lateness bound differ from a full refresh until the next one, and which late, repeated, changed or deleted cases must the evidence cover?
- If unresolved, in which execution environments and time zones must the output match the baseline, and under which conditions is run time compared?
- If unresolved, is any output change actually wanted? If so, it belongs in a separate change, not in this conversion.

### Guardrails

- Do not pick a strategy the source cannot support: append-only needs stored rows that later source data never changes, a watermark needs a marker no new record can fall behind unless an approved overlap covers it, and an event-time filter or lookback needs an approved lateness bound.
- Do not let the incremental path treat repeated, changed or deleted records differently from the full refresh, within a run or across runs, unless the approved contract says so.
- Do not deduplicate rows or invent a key to make the incremental strategy work; if a key the strategy needs is not unique at the approved grain, stop and report the duplicates.
- Do not change anything a consumer reads, even to fix a wrong number; route any output change to a separate change.
- Do not report predicted performance, or a wall-clock difference dominated by fixed start-up time, as the runtime change.
- Do not extend the conversion to downstream or sibling models, warehouse tuning or new marts outside the agreed scope.
