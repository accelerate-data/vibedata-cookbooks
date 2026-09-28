---
id: dbt-snapshot-history
title: Add dimension history with verified historical fact classification
trigger:
  - Customer, asset or vendor attributes change, but past events need a defensible historical classification.
  - Reports join facts to today's dimension row and silently restate earlier results after master data changes.
  - A vehicle, driver or delivery zone changes classification and logistics reporting must select the version valid for each event.
description: Record dimension changes with dbt snapshots and build a bounded historical consumer that selects the agreed version for each fact, with controlled changes, boundary tests and reconciliation.
pitch: Preserve recorded dimension changes and prove that historical events select the right version.
job_category: build
area: transformation
readiness: supported
domain_objects:
  - dimension
  - business_event
  - history
works_with:
  platforms:
    - duckdb_local
  tools:
    - dbt
qualifiers:
  - Complete snapshot outcome assessed for duckdb_local only; the other four Studio targets remain unassessed.
  - Records available changes; present-state snapshots cannot reconstruct unobserved history.
evidence:
  features:
    - profiling-source-data
    - authoring-dbt-project-artifact
    - generating-dbt-model
    - dbt-unit-testing
    - running-dbt-in-sandbox
    - verifying
  evals: []
---

## Prompt

Add dbt snapshot history for <dimension_name> and a bounded historical consumer <history_consumer> for the analytical questions and breakdowns required in this Intent. Inspect approved requirements and source evidence before settling entity identity, tracked attributes, preservation versus restatement, fact time and validity policy. Distinguish source effective time from observation time and expose history the source cannot supply. Record actual version changes and select each fact's version under the agreed boundaries, late-change and deletion rules. Keep Domain sources read-only; use a labelled synthetic fixture or an approved writable fixture with reset. Prove changed and unchanged runs, facts before, exactly at and after a change, current-row and wrong-boundary disproofs, and absence of fact fan-out. Surface gaps, overlaps and unresolved cases; reconcile counts and relevant amounts. Report missing attributes, history or mappings that prevent an agreed question from being answered.

## Verified by

- The approved contract defines entity and fact keys, grains, tracked attributes, preserve-versus-restate policy, event time, source-effective versus observation validity, time zones, precision, boundaries, late changes and deletions.
- Installed dbt and adapter versions support the selected timestamp or check strategy and options. Snapshot configuration matches the accepted unique key, updated_at or check_cols, current-row representation and deletion policy.
- Actual dbt snapshot runs capture a controlled entity changing from A to B. Read-back shows the old version closed and the new version current at the agreed boundary; new entities and unchanged controls have the expected version counts.
- An unchanged snapshot run before the change and another after it leave version counts, attributes and validity unchanged. Changed-run evidence includes fixture inputs, commands, exits and the recorded intervals, not only compiled SQL.
- Independent expected values cover facts before, exactly at and after the change. For an approved start-inclusive, end-exclusive boundary, A/B versions yield A, B, B respectively; equivalent explicit expectations cover any other agreed policy.
- A deliberately current-row consumer and a consumer with an incorrect boundary rule each fail at least one expected case. Expected versions and classifications are fixed independently of the consumer SQL before comparison.
- Every scoped fact has at most one accepted version. Fact keys, counts and relevant additive amounts reconcile before and after consumption at required breakdowns; unmatched, ambiguous, unknown and excluded facts remain visible with reasons.
- Version keys and entity identity pass uniqueness and null checks. Overlaps, gaps, invalid intervals and multiple current rows are detected; approved exceptions retain reasons, and unresolved competing versions cannot become arbitrary winners.
- Independent cases cover a new entity, unchanged and changed attributes, late source updates, missing entity keys, missing history and relevant deletion branches. Outputs follow the agreed policy without silently backdating observations or inventing versions.
- Source entity, version, fact and classification lineage is retained. Each agreed analytical question and breakdown is answerable or has an explicit gap tied to missing attributes, history, mappings or relationship evidence.
- Snapshot and consumer checks pass on the actual supported Intent target, with outputs read back and fixture reset verified. The report records revision, installed versions, commands, exits, intervals, expected/actual results and unresolved exceptions.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain and sources. Inspect approved requirements, source keys, tracked attributes, update timestamps and available history; profile duplicates, nulls and changes. Use Ask first only for unresolved semantics. Record identity, grains, required questions, fact time, validity basis, boundaries, precision, late-change and deletion policies. Check installed dbt/adapter versions and target guidance before selecting supported snapshot syntax and options. Author the snapshot with authoring-dbt-project-artifact and its snapshot branch, then a bounded consuming model with an explicit version-selection rule. Fix expected versions and classifications independently before implementation. Use labelled synthetic data or an approved writable fixture and reset procedure, never Domain mutations. Run dbt snapshot on initial data, unchanged data, a controlled A-to-B change and unchanged data again; retain inputs and read back history after each run. Add before/at/after facts and policy edge cases; exercise wrong current-row and boundary consumers against the same expectations. Materialize and read back the consumer, test keys and intervals, and reconcile scoped fact counts and amounts including unresolved populations. Restore fixture state and verify reset. Report missing source evidence or unexecuted required cases as incomplete verification.

### Compose

- profiling-source-data
- authoring-dbt-project-artifact
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which analytical questions, breakdowns, fact population and changing attributes must this history support, and should past classifications be preserved or restated?
- If evidence does not settle it, which stable entity key and source establish identity and changes, and what historical coverage or authoritative backfill actually exists?
- If unspecified, does validity mean source effective time or observation time, which fact timestamp selects a version, and what time zone, precision and endpoint rules apply?
- If unresolved, how should late or out-of-order changes, corrected timestamps, deletions and reappearing entities affect recorded versions and historical classifications?
- If unspecified, how should missing history, null or unknown keys, gaps, overlaps and ambiguous versions appear in outputs and totals, and which evidence can resolve exceptions?

### Guardrails

- Snapshots of present-state data cannot reconstruct unobserved past versions. State the earliest defensible coverage and leave earlier classifications unresolved unless authoritative history supports an approved backfill.
- Source effective time and observation time are distinct. A check snapshot's observation boundary does not establish when a business change took effect; unsupported restatement or late-change requirements remain explicit gaps.
- Keep Domain sources read-only. Mutate only an independently authored synthetic fixture or an approved writable fixture with a verified reset; never seed a missing production source or mix synthetic rows into observed totals.
- Execute on the actual supported Intent target and supplied sandbox. Do not switch engines or synthesize an absent sandbox; support here covers duckdb_local, while the other four targets remain unassessed for the complete outcome.
- Apply only installed-version snapshot options and supported deletion behavior. Do not infer identical snapshot capabilities across dbt adapters or promise complete change capture between source observations.
- Preserve materially distinct versions and facts. Do not suppress fan-out with arbitrary row selection, erase overlaps by deduplication or discard unmatched facts through inner joins to make checks pass.
- Keep the deliverable to dimension history and its necessary consumer and checks. Add only attributes required by agreed questions; do not build an unrelated fact warehouse or require a second Recipe to prove history.
- Snapshot creation, compilation and unchanged two-run success do not prove historical use. The changed entity, independent boundary results, incorrect-consumer failures and count reconciliation are required future execution evidence.
