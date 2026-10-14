---
id: finance-budget-forecast-actual
title: Compare budget and forecast to actuals at cost-center grain
trigger:
  - Budget-versus-actual is a monthly copy-paste from the general ledger into the budget spreadsheet, and the variances change depending on who built them.
  - Finance needs each cost center's variance against both the approved budget and the current forecast, with the large ones flagged, before the monthly review.
  - Department heads dispute their variances because the GL accounts and cost centers do not line up with the lines they budgeted.
description: For each period the approved rules compare, set GL actuals beside the approved budget and the selected forecast per cost center and budgeted account, with variance, percentage and large-variance flags, rolled up the approved hierarchy and year to date, while every GL and plan line that cannot be placed stays visible with its reason, so no amount is lost, double counted or read as a real zero.
pitch: Compare GL actuals with the approved budget and selected forecast per cost center, account and period, with flagged variances and every line reconciled.
job_category: build
area: transformation
readiness: supported
domain_objects:
  - budget
  - forecast
  - plan_version
  - cost_center
  - cost_center_hierarchy
  - general_ledger_account
  - account_mapping
  - fiscal_period
  - variance
  - budget_exception
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
  - Budget and forecast arrive as landed tables; landing and governing the budget spreadsheet is a separate outcome.
  - A past report as issued needs kept snapshots; without them a later posting into a closed period restates it.
  - Stops at the comparison; allocations, driver-based planning and plan write-back are separate outcomes.
related:
  - governed-spreadsheet-table
  - effective-dated-business-rules
  - finance-trial-balance-close
  - metric-population-and-rollups
  - dbt-snapshot-history
evidence:
  features:
    - capturing-requirements
    - profiling-source-data
    - applying-medallion-data-modelling
    - generating-dbt-model
    - dbt-unit-testing
    - running-dbt-in-sandbox
    - verifying
  evals: []
---

## Prompt

Build <variance_detail_model>, <variance_rollup_model>, <variance_ytd_model>, <gl_reconciliation_model>, <plan_reconciliation_model> and <exceptions_model> from <gl_lines_source>, <plan_lines_source>, <plan_versions_source>, <cost_center_hierarchy>, <account_mapping> and <fiscal_periods>. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only the semantics they leave open. For each period the approved rules compare, place each in-scope GL line on its cost center, budgeted account and period, spread each plan line under its approved method, and compare actuals with the approved budget and the forecast the approved rules select, at the approved grain (with legal entity and currency wherever they apply), with the variance, percentage, direction and large-variance flag the approved rules define. Roll it up the approved hierarchy and year to date, recomputing percentages and flags from rolled-up amounts. List every GL and plan line that cannot be placed as an exception, or fail the run naming it, as the approved policy says, and reconcile every delivered line. Keep sources read-only. Report what the inputs cannot prove.

## Verified by

- On a run that completes, for each compared period, every in-scope GL line not excluded as an exception lands on exactly one cell at the approved grain under the approved placement rules, and the actual per cell equals the sum of those lines in the approved sign convention.
- Each plan line that is spread has periods summing to its stated total, where it has one, under its approved spread method and rounding, with any approved rounding residual reported; a plan line with no valid spread contributes nothing to any period.
- The budget and forecast compared for each period are the versions the approved selection rules name, including the boundary on the approved selection date, where the rule uses one; draft or unapproved versions never enter a comparison unless the approved rules say so.
- Where no plan applies to a cell or period, the plan is shown as the approved rules say, with its reason, and never as a silent zero; a cell affected by an excluded plan line shows that as the approved exception policy says, never as a clean plan.
- Variance, variance percentage and direction follow the approved definitions, signs and precision, and a zero plan is reported as the approved rule says, never as zero percent or infinite unless the approved semantics define it so.
- The large-variance flag follows the approved thresholds at their approved level, edges and precision, for each comparison and for month and year to date as approved, including cells exactly on and just inside each threshold.
- Each roll-up level equals the sum of the cells beneath it, with variance percentage and flags recomputed from its own amounts and never averaged, and year to date uses the version or versions the approved rule names per period, never an unapproved mix.
- On a run that completes, per period and in total, every delivered GL line lands once: placed, excluded with its reasons, in a period the approved rules do not compare, or outside the approved scope, and the placed amounts equal the actuals reported.
- On a run that completes, every delivered plan line and any separately delivered period amount lands once: spread or excluded with its reasons, and spread totals equal the valid lines' stated totals, where they have them, plus any approved residual.
- On a run that completes, every unplaceable line is listed with its reasons under the approved exception grain and its amount and count reach its cell (where known), roll-ups and period as the approved policy says, never a silently clean variance; a run the policy fails names each offending line.
- Entities, currencies and units of measure are never netted together unless an approved consolidation or translation rule is stated, and the totals reconcile under that rule.
- On a run that completes, each output is unique on its declared business grain with required fields populated, and the outcome states which exceptions remain open and what the inputs cannot prove, such as whether a posting into a closed period restates it.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile the GL lines (accounts and their classes, cost centers, posting periods, signs, amounts, entities, currencies, record identifiers), the plan lines and versions (types, statuses, publish dates, spread methods, profiles, totals) and the hierarchy and account mapping. Use Ask first only for semantics still open, and record each decision as the user's own answer. Keep the account mapping, hierarchy, period statuses and report dates, version selection, spread profiles and thresholds as editable data where the approved requirements say so, and fail the build on a value outside an editable list's allowed set rather than placing it silently. The detail, roll-ups, year to date, reconciliations and exceptions must never disagree about a line or an amount. Report every exception left open and what the inputs cannot prove.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which accounts and postings are compared (statistical or non-monetary lines, allocations, intercompany), for which entities, currencies and periods, at what grain and translation rates; and how are out-of-scope lines shown?
- If unresolved, how do GL accounts map to the budgeted accounts and cost centers to the reporting hierarchy, does a past period use the current hierarchy and mapping or the one then in effect, and where do retired or merged cost centers go?
- If unresolved, which field places a GL line in a period, how adjustment or extra periods are treated, which periods count as closed, what happens to lines in open periods, and may a later posting restate a closed period or must past reports be kept as issued?
- If unresolved, how is an annual plan line spread to periods (equally, by a seasonal profile, as given per period, or otherwise), at what precision, where any rounding remainder goes, and when is a profile or a given set of period amounts invalid?
- If unresolved, which budget version is compared per fiscal year, which forecast version is selected for each period and by what rule and date, what is shown before any forecast applies, and which version year to date uses?
- If unresolved, which sign convention applies per account type, how are variance, percentage and direction defined, at what rounding, and what does a cell show with a zero plan, actuals but no plan line, a plan but no postings, or an excluded plan line?
- If unresolved, which thresholds flag a large variance and at what level (account, account type, cost center, net or total rows), whether both an amount and a percentage must be reached, which edges are inclusive, and are they applied to month and year to date?
- If unresolved, which lines can't be placed (unknown keys, periods or versions, amounts in an unaccepted format), are duplicates by record id or business key excluded or one copy kept, one row per reason or one primary, is each excluded with a visible amount and count, flagged, or does the run fail?

### Guardrails

- Do not choose the mapping, hierarchy version, period placement, spread method, version selection, signs, variance definition, thresholds or exception handling for the user, nor take them from the data, the planning tool or common practice; the user may ask for options or a recommendation.
- Never show a missing or excluded plan, or a period with no applicable forecast, as a zero plan unless the approved semantics say so, and never average variance percentages across cells.
- Never mix forecast versions within one comparison or one year to date unless the approved rules say so.
- Never drop, round away or double count a line or an amount beyond what the approved rules leave out; every line that cannot be placed stays visible, as an exception or in an explicit run failure, with its reasons.
- Never net distinct legal entities, currencies or units of measure together because they share a cost center or account; consolidate or translate only under the approved mapping, rates and rules.
- Do not claim a past report as issued when no snapshots are kept; say later postings restate it, and route reports as issued to dbt-snapshot-history.
- Stop at the comparison: do not edit the budget file, post adjustments to the ledger or write plans back to the planning tool.
