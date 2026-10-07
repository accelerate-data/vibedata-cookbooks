---
id: bounded-partition-backfill
title: Backfill a bounded date range after a logic change without a full refresh
trigger:
  - A business rule in an incremental model was corrected, and only a known date range of published history should be restated.
  - A full refresh would take too long, or would restate history that must stay as first published.
  - A normal incremental run only loads new data, so it cannot reprocess a date range already loaded.
description: Apply a corrected rule to one approved date range of an incrementally loaded model and carry its effect through everything built from it, prove the range matches the new rule and nothing moved except by that effect, and keep normal loads working afterwards.
pitch: Restate one date range after a logic change, and prove nothing else moved because of it.
job_category: re-engineer
area: transformation
readiness: supported
domain_objects:
  - dbt_model
  - restatement_window
  - consumer_contract
  - approved_baseline
  - follow_up
works_with:
  platforms:
    - duckdb_local
  tools:
    - dbt
qualifiers:
  - Complete outcome assessed for duckdb_local only; the other four Studio targets remain unassessed.
  - Converting a model to incremental for routine runs belongs to the dbt-full-refresh-to-incremental Recipe.
related:
  - dbt-full-refresh-to-incremental
  - dbt-refactor-output-identical
  - prove-dbt-change-safe
evidence:
  features:
    - evaluating-dbt-project
    - generating-dbt-model
    - dbt-unit-testing
    - running-dbt-in-sandbox
    - verifying
  evals: []
---

## Prompt

Restate <restatement_window> of <affected_models> under <corrected_rule>, without a full refresh, and leave the detail outside the window as published. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Find every relation that applies the rule or is built from it, including those that read it through a shared definition and rebuild in full, and carry the restatement through them by lineage. Deliver the corrected models, a repeatable way to restate an approved window, and evidence that the window matches what a full rebuild under the corrected rule gives, that detail outside it is unchanged, that every downstream result moved only by the restatement's effect, and that normal loads still work afterwards. A defect found along the way is reported as separate work.

## Verified by

- Inside the approved window, every affected row follows the corrected rule and equals what a full rebuild under that rule gives, at the approved precision.
- Detail outside the window keeps its published values and the approved historical rule, after the restatement and after later loads.
- Every downstream result, including aggregates that span the window or carry no date, changes only by the restatement's effect on its contributing detail and reconciles to the restated detail.
- Rebuilt downstream results match a rebuild of the unchanged code within the approved reproducibility contract, apart from the restatement's effect; where that rebuild itself differs from the published state, the difference and its cause are reported.
- Repeating the same restatement changes nothing, and a restatement that reaches only some of the affected relations does not complete as if it had succeeded.
- A later normal load adds new data under the approved rule, changes published history only as its approved load strategy allows, and handles late arrivals as the approved policy says.
- Which rule built which rows can be read as approved, from documentation by date or from a marker on the row.
- What a later full refresh would do to history outside the window is stated and follows the approved policy, and defects found during the work are reported as follow-up with the output they affect.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Find where the rule is defined and every relation that applies it or is built from it: incremental models, tables that rebuild in full from a shared definition, and every consumer. Establish which rows of each downstream relation draw on detail inside the window, including aggregates that span it or carry no date. Record the published state before changing anything. Choose a way to restate the window that the source, the platform and the approved requirements support, and change the normal load path only as the approved rule requires. Where a published relation needs a new column or materialization to take part, plan how it switches over without its first normal run changing published history beyond what the approved load strategy allows. Restate, then compare the window with a full rebuild under the corrected rule, the detail outside it with the published state, and each rebuilt downstream result with a rebuild of the unchanged code, and report where that rebuild differs from the published state. Reconcile consumers, run a normal load afterwards, document which rule applies to which rows, and report follow-up work.

### Compose

- evaluating-dbt-project
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which rule changes and what exactly is the corrected definition?
- If unresolved, which date range is restated, which date places a record in it (event, load or business date, in which time zone), and are both edges inclusive?
- If unresolved, does the corrected rule also apply to every later load, or only to the window, and what should a later full refresh do to history outside it?
- If unresolved, should each row record which rule built it, or is documentation by date enough?
- If unresolved, what reproducibility contract applies to rebuilt results (exact, or a stated precision), and how are late arrivals into restated or published periods handled by later loads?

### Guardrails

- Do not choose or apply the corrected rule, the window, or its edges without approval.
- Do not use a full refresh as the backfill, and do not let a relation that rebuilds in full from a shared definition apply the corrected rule to detail outside the window.
- Do not leave affected relations disagreeing with each other: a model restated while an input it reads still holds the old rule is not done.
- Do not let a later normal load or rebuild silently undo, extend or repeat the restatement outside the window.
- Do not claim published values are unchanged when a rebuild of the unchanged code does not reproduce them; state what moved, why, and the reproducibility that holds.
- Do not change how normal loads handle late arrivals unless the approved policy says so, and do not convert other models to incremental or fix other defects here; report them as follow-up.
