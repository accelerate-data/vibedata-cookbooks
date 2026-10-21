---
id: cross-platform-dbt-macro
title: Port a dbt macro to each approved warehouse without changing its callers
trigger:
  - Part of a dbt project is moving to another warehouse, and a macro its models call only compiles, or only returns correct values, on the old one.
  - A macro renders SQL in one warehouse's dialect, so a model that calls it fails on a new target or quietly returns a different value.
  - The team wants one macro name that every model keeps calling, whichever warehouse builds it.
description: Make an existing dbt macro render the right SQL for each approved warehouse behind one name and signature with callers unchanged, prove every target the Intent can run matches the current output apart from approved differences, and report each target it cannot run as unproven.
pitch: Port one dbt macro to each approved warehouse, with the models that call it left alone.
job_category: cross-platform
area: transformation
readiness: supported
domain_objects:
  - dbt_macro
  - dbt_model
  - warehouse_target
  - consumer_contract
  - approved_baseline
  - parity_report
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
  - Needs the macro's current output on the agreed inputs, runnable or captured, as the baseline.
  - A target the Intent's platform cannot run is written and reviewed only, and reported unproven.
  - Macros that return a value from their arguments only; side effects or run-time state are out of scope.
  - Turning a warehouse function into a macro belongs to scalar-sql-function-to-dbt-macro.
related:
  - scalar-sql-function-to-dbt-macro
  - legacy-sql-to-dbt
  - prove-dbt-change-safe
  - dbt-refactor-output-identical
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

Make <macro_name> work on <target_warehouses> in the current Intent without changing its name, its arguments or the models that call it. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Keep the output on the current warehouse exactly as it is today, add the approved warehouse implementations behind the one macro name, and make any warehouse without an approved implementation stop at compile time with a clear message instead of silently rendering another warehouse's SQL. Deliver evidence that each caller keeps its approved output, that every target the Intent can run returns the same values and types as the baseline on the agreed inputs apart from approved differences, and, for each target it cannot run, the SQL the macro itself renders with a statement that it is unproven, plus a check another target's first run can reuse. Handle the behaviours that differ between warehouses as approved, and state what the evidence cannot show.

## Verified by

- Each caller keeps its approved output contract, covering whichever of rows, columns, column order and types the approved contract counts as unchanged, and neither the macro's name or arguments nor any caller's code changed; callers that could not be enumerated or run are stated.
- On every target the Intent can run, the macro returns the same value and type as the baseline at the approved precision for every agreed input, except where an approved decision accepts a difference; each such difference is listed with its inputs.
- The compared inputs include the values the callers pass, each input the macro treats specially (null, a boundary, an empty or extreme value) and the agreed edge inputs, with expected values taken from the baseline or an approved oracle, never from the new implementation.
- Every approved target is either run on those same inputs with matching results or listed as unproven; no target is called equal to the baseline unless it ran.
- The SQL for a target that was not run is the one the macro itself renders, reproducible on a second render, and each construct beyond standard SQL is checked against that warehouse's documentation with source and as-of date.
- A target that would resolve to an implementation written for another warehouse, through a shared or inherited adapter, either is approved as sharing it with the shared behaviour listed, or stops at compile time with a message naming it and the supported ones.
- Any check shipped with the macro takes its expected values from the baseline or an approved oracle, not from the new implementation, and lists the inputs it can check only as a property and each target-specific type spelling a first run must map.
- Each behaviour that differs between the approved warehouses (null handling, types, rounding, integer division, time zones, collation, quoting, overflow) is listed with how each target treats it, taken from documentation for a target not run, and the approved decision.
- Anything the evidence cannot show is stated, including each unrun target and each class of input not covered.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements. Read the macro and every use of it first, including tests, seeds, hooks and other macros, any macro it calls, any package macro that dispatches itself, and the project's dispatch settings: its arguments, the SQL it renders, the type it returns, and each place it uses syntax or functions that differ between warehouses. Settle which warehouses must be supported and how the baseline is obtained on the agreed inputs, and keep that baseline unchanged. Keep the macro's name and signature, and keep the current warehouse's rendered SQL as it is; if portability cannot be reached without changing the name, the arguments or a caller, stop and report that instead. Add one implementation for each approved warehouse behind that name using dbt's adapter dispatch, with a default that raises a compiler error naming the unsupported adapter. Compare the current warehouse's output with the baseline on the agreed inputs, then compare each caller's output before and after. For a target the Intent cannot run, render the macro's own SQL for it, review each non-standard construct against that warehouse's documentation, and record it as unproven. Add a check with no per-warehouse branch so a later run on another target can reuse it. State what the evidence cannot prove.

### Compose

- capturing-requirements
- profiling-source-data
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- documenting-dbt-models
- verifying

### Ask first

- If unresolved, which warehouses must the macro support now, and which adapters may share an implementation?
- If unresolved, are values compared exactly or within an approved precision, and what counts as the same type?
- If unresolved, which inputs form the comparison, and where does the baseline come from if the current macro cannot run on them?
- If unresolved, where warehouses legitimately differ (null handling, rounding, time zones, collation, integer division), which behaviour must each target reproduce, and is a difference a failure or an accepted, reported exception?
- If unresolved, which callers and uses (models, tests, seeds, hooks, other macros, anything outside this project) are in scope, and which output changes, if any, are approved?
- If unresolved, which argument types must each target accept: only those the callers pass, or every type the macro accepts?

### Guardrails

- Do not change the current warehouse's output, the macro's name or its arguments to make another target match.
- Do not present hand-written SQL as the macro's own rendering for a target that was not run.
- Do not report a target as matching unless it ran on the agreed inputs.
- Do not let a target silently use another warehouse's SQL; share an implementation only as approved.
- Do not edit the baseline or its captured outputs to make a comparison pass.
- Do not compare the new implementation against itself.
