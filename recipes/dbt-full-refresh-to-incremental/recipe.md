---
id: dbt-full-refresh-to-incremental
title: Convert a full-refresh dbt model to incremental and show the runtime delta
trigger:
  - A dbt model is correct but a full refresh is too slow or too expensive to run routinely.
  - A full-refresh model needs to become incremental without changing its required consumer-visible output.
  - A logistics event model must run incrementally, but loader rows may repeat the same shipment event.
description: Convert an existing full-refresh dbt model to an incremental implementation while preserving its required semantics, handling agreed late-arriving data correctly, and recording the before-and-after runtime.
pitch: Make a slow full-refresh dbt model incremental and prove both the output parity and the runtime saving.
job_category: re-engineer
area: transformation
readiness: supported
domain_objects:
  - dbt_model
works_with:
  platforms:
    - duckdb_local
    - motherduck
    - fabric_lakehouse
    - fabric_warehouse
  tools:
    - dbt
evidence:
  features:
    - profiling-source-data
    - generating-dbt-model
    - running-dbt-in-sandbox
    - verifying
    - dbt-unit-testing
  evals: []
---

## Prompt

Convert the existing full-refresh dbt model to an incremental model in the current Intent. Preserve the required consumer-visible output and downstream contract. Check whether its declared business grain agrees with source identifiers and loader-row identity before selecting the incremental key and strategy. Expose any existing semantic defect that conflicts with output parity and obtain an approved resolution or separate follow-up; do not silently redesign the grain. Verify output parity, idempotency and the agreed late-arriving-data behaviour, and record the runtime change against the current full-refresh baseline.

## Verified by

- Incremental output matches the approved full-refresh baseline on the agreed comparison slice.
- A repeated incremental run produces no duplicate unique keys or unintended row changes.
- The agreed late-arriving-data case updates exactly the expected records.
- The before-and-after runtime is recorded from observed executions.
- Declared business grain, source identifiers and loader-row identity are compared with evidence; conflicts and missing evidence are recorded, with an approved resolution or separate follow-up for each semantic defect.
- Repeated loader rows for one event and distinct events with equal measures have independently specified expected outputs under the approved grain and duplicate policy; both cases pass without losing distinct events.
- Source-to-output traceability and count/amount reconciliation expose excluded, unmapped, ambiguous and unknown cases on the comparison slice.
- A semantic defect that conflicts with parity is disclosed. An approved correction names the contract and baseline changes; a separate follow-up retains the approved contract and records the unresolved limitation.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain and sources. Inspect approved requirements, model dependencies, source behaviour and the current full-refresh result. Establish the required analytical questions and breakdowns; expose missing attributes, history or relationship evidence. Compare the declared business grain with source and loader keys; distinguish observed relationships, approved allocations and synthetic examples. A unique loader key or stable rerun alone does not establish business-event identity. Resolve parity conflicts before implementation: obtain approval for a documented contract/baseline change or a separate follow-up that preserves current semantics and states the defect. Choose a supported incremental strategy and key from the approved contract. Define independent expected results for duplicate, distinct-event and late-arrival cases before implementing the smallest conversion. Run old and new paths on the same agreed slice in the assigned isolated sandbox, then repeat the incremental run and exercise the agreed late-arrival case. Use approved writable fixtures when source changes are needed; keep Domain data read-only. Compare outputs, trace source populations and reconcile counts/amounts, including exceptions. Record actual timings with slice, run conditions and commands. Use verifying to review independent comparisons and test evidence at the exact revision; disclose inherited baseline evidence and unresolved limitations.

### Compose

- profiling-source-data
- generating-dbt-model
- running-dbt-in-sandbox
- verifying
- dbt-unit-testing

### Ask first

- Ask for the intended late-arriving-data policy only if approved requirements do not settle it; existing behaviour is evidence, not permission to change the policy.
- Ask for the intended business grain, key and duplicate policy only if approved requirements and source evidence leave them unresolved.
- Ask which analytical questions and breakdowns are required only if the Intent does not settle them; surface missing evidence that prevents an answer.
- Ask for an approved resolution or separate follow-up when a discovered semantic defect conflicts with output parity, including the scope of any contract or baseline change.

### Guardrails

- Do not invent a unique key merely to make the incremental materialization compile.
- Do not change consumer-visible model semantics merely to make incremental processing easier.
- Do not treat predicted performance as evidence; record observed runtime from actual executions.
- Do not call loader counts unique business events or treat idempotency as proof of business identity.
- Do not discard distinct events or infer business intent from equal sample values or convenient existing code.
- Do not silently replace the baseline to hide a semantic change; parity and the approved contract remain acceptance gates.
- Use the assigned platform sandbox and its supported strategy; Fabric Warehouse microbatch is unavailable. Do not substitute another engine.
