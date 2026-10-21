---
id: cross-platform-dbt-macro
title: Port a dbt macro to each warehouse a project targets without changing its callers
trigger:
  - Part of a dbt project is moving to another warehouse, and a macro its models call only compiles, or only returns correct values, on the old one.
  - A macro renders SQL in one warehouse's dialect, so a model that calls it fails on a new target or quietly returns a different value.
  - The team wants one macro name that every model keeps calling, whichever warehouse builds it.
description: Make an existing dbt macro render the right SQL for each approved warehouse behind one name and signature with callers unchanged, prove every target the Intent can run matches the current output, and report each target it cannot run as unproven.
pitch: Port one dbt macro to each warehouse you target, with the models that call it left alone.
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
    - redshift
  tools:
    - dbt
qualifiers:
  - Needs the macro's current output on the agreed inputs, runnable or captured, as the baseline.
  - A target Studio cannot run is written and reviewed only, and reported unproven.
  - Macros that return a value from their arguments only; side effects or run-time state are out of scope.
  - Turning a warehouse function into a macro belongs to scalar-sql-function-to-dbt-macro.
related:
  - scalar-sql-function-to-dbt-macro
  - legacy-sql-to-dbt
  - prove-dbt-change-safe
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

Make <macro_name> work on <target_warehouses> in the current Intent without changing its name, its arguments or the models that call it. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Keep the output on the current warehouse exactly as it is today, add the approved warehouse implementations behind the one macro name, and make any other warehouse stop at compile time with a clear message instead of rendering another warehouse's SQL. Deliver evidence that each caller keeps its approved output, that every target the Intent can run returns the same values and types as the baseline on the agreed inputs, and, for each target it cannot run, the SQL the macro itself renders with a statement that it is unproven. Handle the behaviours that differ between warehouses as approved, and state what the evidence cannot show.

## Verified by

- Each caller keeps its approved output contract, covering whichever of rows, columns, column order and types the approved contract counts as unchanged, and no caller's code or the macro's name or arguments changed.
- On every target the Intent can run, the macro returns the same value and warehouse type as the baseline at the approved precision for every agreed input; any difference is reported, never claimed as equal.
- The compared inputs include the values the callers pass, each input the macro treats specially (null, a boundary, an empty or extreme value) and the agreed edge inputs, with expected values taken from the baseline or an approved oracle, never from the new implementation.
- Every approved target is either run on those same inputs with matching results or listed as unproven; no target is called equal to the baseline unless it ran.
- The SQL for a target that was not run is the one the macro itself renders, reproducible on a second render, and each construct beyond standard SQL is checked against that warehouse's documentation with source and as-of date.
- A warehouse with no approved implementation stops at compile time with a message naming it and the supported ones; it never gets another warehouse's SQL.
- A check with no per-warehouse branch of its own ships with the macro, covers the agreed inputs, fails if one expected value is wrong, and lists each type spelling a first run on another target still has to map.
- Each behaviour that differs between the approved warehouses (null handling, types, rounding, time zones, collation) is listed with how each target treats it and the approved decision; none is left implicit.
- Anything the evidence cannot show is stated, including each unrun target and each class of input not covered.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements. Read the macro and every caller first: its arguments, the SQL it renders, the type it returns, and each place it uses syntax or functions that differ between warehouses. Settle which warehouses must be supported and how the baseline is obtained on the agreed inputs, and keep that baseline unchanged. Keep the macro's name and signature, and keep the current warehouse's rendered SQL as it is; if portability cannot be reached without changing the name, the arguments or a caller, stop and report that instead. Add one implementation for each approved warehouse behind that name using dbt's adapter dispatch, with a default that raises a compiler error naming the unsupported adapter. Compare the current warehouse's output with the baseline on the agreed inputs, then compare each caller's output before and after. For a target the Intent cannot run, render the macro's own SQL for it, review each non-standard construct against that warehouse's documentation, and record it as unproven. Add a check with no per-warehouse branch so the first run on another target exercises it unchanged. State what the evidence cannot prove.

### Compose

- capturing-requirements
- profiling-source-data
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- documenting-dbt-models
- verifying

### Ask first

- If unresolved, which warehouses must the macro support now, and which of them can the Intent run?
- If unresolved, are values compared exactly or within an approved precision, and what counts as the same type?
- If unresolved, which inputs form the comparison, and where does the baseline come from if the current macro cannot run on them?
- If unresolved, where warehouses legitimately differ (null handling, rounding, time zones, collation, integer division), which behaviour wins, and is a difference a failure or a reported exception?
- If unresolved, which callers use the macro, inside and outside this project, and which must keep their output unchanged?
- If unresolved, which argument types must each target accept: only those the callers pass, or every type the macro accepts?

### Guardrails

- Do not change the current warehouse's output, the macro's name or its arguments to make another target match.
- Do not type the SQL for a target that was not run; render it from the macro.
- Do not report a target as matching unless it ran on the agreed inputs.
- Do not fall back to another warehouse's SQL for a target with no approved implementation.
- Do not edit the baseline or its captured outputs to make a comparison pass.
- Do not compare the new implementation against itself.
