---
id: incremental-dbt-model-with-contract
title: Author an incremental dbt model with its contract and prove idempotency
trigger:
  - A new dbt model must be brought up to date incrementally on each run, and nobody can show that a rerun or a re-delivery of records already applied leaves it unchanged.
  - Downstream consumers need a guaranteed set of columns, types and keys, and a build should fail when the output drifts from them.
  - A loader resends or corrects records, and the table must stay correct when the same batch is delivered twice.
description: Author a new incremental dbt model with an enforced output contract, then prove that a rerun and a re-delivery of records already applied leave it unchanged under the approved definition, with records the approved rules set aside kept visible.
pitch: Build an incremental dbt model with an enforced contract and show that a rerun or a re-delivery of records already applied leaves it unchanged.
job_category: build
area: transformation
readiness: supported
domain_objects:
  - incremental_model
  - output_contract
  - delivered_record
  - set_aside_record
  - rerun_proof
works_with:
  platforms:
    - duckdb_local
    - motherduck
    - fabric_lakehouse
    - fabric_warehouse
    - redshift
  tools:
    - dbt
qualifiers:
  - Assessed end to end on duckdb_local only; the other listed targets rely on dbt support and are unassessed.
  - Needs a source that carries a key and a version or update timestamp for each record, and can be read in full.
  - Converting an existing full-refresh model belongs to the dbt-full-refresh-to-incremental Recipe.
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

Author <model_name> as an incremental dbt model over <delivered_source>, so each run brings the model up to date with the records that are new or genuinely newer under the approved rules, without a full rebuild, and consumers read a table with an enforced output contract. Prove that a rerun with nothing new and a re-delivery of records already applied leave the model unchanged under the approved definition of unchanged, and keep records the approved rules set aside visible instead of dropping them. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open.

## Verified by

- At the approved grain and key, no key appears twice in the model, and each key with a placeable record shows the copy the approved rules select.
- A copy that is not newer under the approved rules is handled as the approved resend and version rules say and never regresses a key to an older copy, including when its batch arrives out of order.
- The output contract matches what was approved: columns, types, nullability and the unique key; a source schema change is handled as the approved policy says, with the change visible.
- A rerun with nothing new, and a re-delivery of records already applied, leave the model's rows, values, column names, column order and column types unchanged, as the approved definition of unchanged says.
- A partly overlapping batch and a re-delivered correction leave the model as if only the new and changed records had been applied.
- A record that would change the model and arrives within the approved lateness bound is applied; one beyond it is handled as the approved policy says and stays visible.
- A record the approved rules cannot place, such as a contract break or a tie that cannot be resolved, is handled as the approved policy says, and one set aside stays visible with a reason.
- Every delivered record whose batch has arrived and can be identified is accounted for as applied, set aside with a reason, or superseded by another copy of its key.
- Where the approved policy allows a full refresh, the table it gives matches what the incremental runs gave for the same landed data under unchanged rule values, and any difference is listed.
- What the proof cannot show is stated.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Profile the source to learn what identifies a record, which field orders versions of the same record, how batches arrive and whether records can be resent, corrected, late or out of order. Choose the incremental strategy from that evidence and the approved requirements, and state what it relies on and what it would miss if that does not hold. Settle the output contract first, then build in dependency order: the rule that picks the current copy of each key, the incremental selection, the enforced contract with its key, and a visible place for any record the approved rules set aside.

### Compose

- profiling-source-data
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, what is the model's grain and unique key, can a record for an existing key change after it lands, which version is current, and how are ties between copies of one key broken?
- If unresolved, what counts as an exact resend rather than a correction, and may a resend change any published value, including the batch or version a row carries?
- If unresolved, how late can a record arrive and measured from what, and what happens to one beyond that bound: applied, set aside or flagged, even when it would not change the model anyway?
- If unresolved, what does the first run load, when is a full refresh allowed, and must it reproduce exactly what the incremental runs produced?
- If unresolved, which columns, types, nullability and unique key does the contract guarantee, what happens when the source adds, drops or retypes a column, and who owns that change?
- If unresolved, what happens to a record that breaks the contract, repeats within one batch with differing content, or cannot be ordered: fail the run, set it aside or load it flagged?
- If unresolved, what does unchanged mean after a rerun: rows, values, column names, order, types and any bookkeeping column, and to what precision are decimals compared?
- If unresolved, which replays must be proven, can the source delete or cancel a record and how is that shown, and can a rule value such as the lateness bound change after rows are applied?

### Guardrails

- Do not choose or apply the key, the version rule, the resend rule, the lateness bound or the handling of bad records without approval.
- Do not decide without approval whether a resend may change a published value, including bookkeeping such as the batch a row carries.
- Do not change a rule value after rows are applied without approved handling of those rows, whether reconciled or kept under their earlier handling.
- Do not extend the Recipe past its stop-line: no source-side ingestion and no conversion of an existing model.
