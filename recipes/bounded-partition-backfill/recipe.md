---
id: bounded-partition-backfill
title: Backfill a bounded date range after a logic change without a full refresh
trigger:
  - A business rule in an incremental model was corrected, and only a known date range of published history should be restated.
  - A full refresh would take too long, or would restate history that must stay as first published.
  - A normal incremental run only loads new data, so it cannot reprocess a date range already loaded.
description: Apply a corrected rule to one approved date range of an incrementally loaded model and everything built from it, prove the range now matches the new rule and everything outside it is unchanged, and keep normal loads working afterwards.
pitch: Restate one date range after a logic change, and prove nothing outside it moved.
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

Apply <corrected_rule> to <affected_models> for <restatement_window> only, without a full refresh, and leave every published value outside the window as it is. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Find every relation that applies the rule or is built from it, including those that read it through a shared definition and rebuild in full, and restate them consistently for the window. Deliver the corrected models, a repeatable way to restate an approved window, and evidence that the window matches what a full rebuild under the corrected rule gives, that nothing outside it changed, that consumers still agree with the restated data, and that normal loads still work afterwards. A defect found along the way is reported as separate work.

## Verified by

- Inside the approved window, every affected row follows the corrected rule and equals what a full rebuild under that rule gives, at the approved precision.
- Outside the window, every published row of every affected relation is unchanged at the approved precision, after the restatement and after later normal loads; relations the comparison cannot cover are named.
- A row whose grain spans the window edge, such as a shift, day or month holding records on both sides, changes only as the approved window rule says.
- Every relation that applies or is built from the changed rule shows the same window scope, and every consumer reconciles to the restated detail.
- Repeating the same restatement changes nothing, and a restatement that reaches only some of the affected relations does not complete as if it had succeeded.
- A later normal load adds new data under the approved rule, reprocesses no published history, and handles late arrivals as the approved policy says.
- Which rule built which rows can be read as approved, from documentation by date or from a marker on the row.
- What a later full refresh would do to history outside the window is stated, and defects found during the work are reported as follow-up with the output they affect.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Find where the rule is defined and every relation that applies it or is built from it: incremental models, tables that rebuild in full from a shared definition, and every consumer. For each, establish how its rows map to the window, including grains that can span the window edge. Record the published state before changing anything. Choose a way to restate the window that the source, the platform and the approved requirements support, and change the normal load path only as the approved rule requires. Where a published relation needs a new column or materialization to take part, plan how it switches over without its first normal run reprocessing published history. Restate, then compare the window with a full rebuild under the corrected rule and everything outside it with the published state; if a rebuild of the unchanged code cannot reproduce the published state, compare against that rebuild and report the difference. Reconcile consumers, run a normal load afterwards, document which rule applies to which rows, and report follow-up work.

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
- If unresolved, which dependent relations must follow the window, and how is a row whose grain spans the window edge treated?
- If unresolved, should each row record which rule built it, or is documentation by date enough?
- If unresolved, at what precision must restated and untouched rows match, and how are late arrivals into restated or published periods handled by later loads?

### Guardrails

- Do not choose or apply the corrected rule, the window, or its edges without approval.
- Do not use a full refresh as the backfill, and do not let a relation that rebuilds in full from a shared definition restate history outside the window.
- Do not leave affected relations disagreeing with each other: a model restated while an input it reads still holds the old rule is not done.
- Do not let a later normal load or rebuild silently undo, extend or repeat the restatement outside the window.
- Do not claim exact preservation when rebuilds of the unchanged code do not reproduce the published state; state the precision that holds.
- Do not change how normal loads handle late arrivals, convert other models to incremental, or fix other defects unless that is approved; report them as follow-up.
