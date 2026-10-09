---
id: incremental-dbt-model-with-contract
title: Build an incremental dbt model with an enforced contract and proven idempotency
trigger:
  - A new dbt model must load only new and changed source rows on each run, and downstream consumers depend on its column names and types.
  - A model that grows with history needs an incremental strategy chosen from source behaviour before its first full build.
  - A reviewer wants proof that rerunning the model, or replaying a batch, does not duplicate or alter rows.
description: Build a new incremental dbt model at an agreed grain with a unique key, a strategy chosen from source behaviour, an enforced model contract and tests, and prove that a rerun with nothing new and a replayed batch change no row.
pitch: Ship an incremental dbt model with an enforced contract and evidence that reruns and replays are safe.
job_category: build
area: transformation
readiness: supported
domain_objects:
  - dbt_model
  - model_contract
  - unique_key
  - incremental_strategy
  - idempotency_evidence
works_with:
  platforms:
    - duckdb_local
  tools:
    - dbt
qualifiers:
  - Complete outcome assessed for duckdb_local only; the other four Studio targets remain unassessed.
  - Idempotency is proven for the agreed batches and cases only; source behaviour outside them is not covered.
  - Converting an existing full-refresh model belongs to the dbt-full-refresh-to-incremental Recipe.
related:
  - dbt-full-refresh-to-incremental
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

Build <model_name> as a new incremental dbt model at the grain <grain> from <source_name>, with an enforced model contract and tests. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Choose the unique key and the incremental strategy from how the source adds, changes, deletes and delivers late records, and state what the strategy relies on and what it would miss. Declare the contract with column names, data types and constraints that consumers can rely on, and enforce it. Deliver the model, its contract and tests, and evidence that an initial build, an incremental run with new and changed rows, a rerun with nothing new and a replay of an already loaded batch each leave the table as a full rebuild of the same source data would.

## Verified by

- The model's grain and unique key are documented, supported by source evidence, and the built table has exactly one row per key.
- The contract is enforced: every column has a declared name and data type, the agreed constraints are declared, and a deliberate violation of the declared types fails the build rather than loading.
- The chosen strategy is justified from source evidence and the approved requirements, and what it relies on, such as a reliable change marker or a lateness bound, is stated with what it would miss if that does not hold.
- After an initial build and incremental runs with new and changed rows, the table matches a full rebuild from the same source data on the agreed comparison slice.
- A rerun with nothing new adds, removes or changes no row, and the row count and a content comparison are recorded before and after.
- Replaying an already loaded batch adds no duplicate row and changes no value beyond what the approved handling of changed records allows.
- The agreed late, repeated, changed and deleted cases each end up as the approved rules state, within one run and across runs.
- Tests cover the key, required columns and agreed relationships, and anything the evidence cannot prove is stated with the cases it leaves open.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Profile the source before choosing anything: whether records are only appended or also updated and deleted, whether it carries a trustworthy change marker such as updated_at, CDC operations or batch identifiers, whether a new record can arrive behind a mark already processed, and whether the proposed key is unique at the agreed grain. Choose the strategy the evidence and the approved requirements support, for example append-only inserts, a merge on the unique key with a change-marker watermark, delete and insert, or partition replacement; if none is safe, report that instead of building. Write the contract with explicit data types and constraints and set it to enforced, and add tests for the key and the agreed relationships. Prove idempotency with observed runs in the sandbox: an initial build, an incremental run with new and changed rows, a rerun with nothing new, and a replay of a loaded batch, comparing each result with a full rebuild of the same source data. Report the strategy's assumptions, what it would miss, and any periodic full refresh it still needs.

### Compose

- profiling-source-data
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, what is the grain of the model, and which columns identify one row at that grain?
- If unresolved, how does the source add, change and delete records, can its change marker be trusted, and how late can a record arrive?
- If unresolved, what must the contract guarantee to consumers: column names, data types, nullability and other constraints, and may columns be added later?
- If unresolved, how must a changed or replayed record be handled: replace the stored row, keep both versions or ignore the replay?
- If unresolved, which late, repeated, changed or deleted cases must the idempotency evidence cover, and which differences from a full rebuild may persist until the next one?

### Guardrails

- Do not pick a strategy the source cannot support: append-only needs source rows that never change after loading, a watermark needs a marker no new record can fall behind unless an approved overlap covers it, and a lookback needs an approved lateness bound.
- Do not invent a key to make the merge work; if the key is not unique at the agreed grain, stop and report the duplicates.
- Do not declare a contract without enforcing it, or loosen types or constraints to make a build pass.
- Do not claim idempotency from a single rerun or from row counts alone; compare content against a full rebuild of the same source data.
- Do not let the incremental path treat repeated, changed or deleted records differently from a full rebuild unless the approved rules say so.
- Do not extend the work to downstream or sibling models, warehouse tuning or new marts outside the agreed scope.
