---
id: retail-sell-through-stockout
title: Build sell-through and stockout risk by store, SKU, and day
trigger:
  - Planners cannot tell which items are about to run out because sell-through and stock-outs live in spreadsheets, and each one counts a day with no stock differently.
  - A SKU that was empty for several days looks like a slow seller, because zero sales on an empty shelf is read as weak demand instead of lost sales.
  - Store, planning and merchandising reports disagree about what was out of stock because returns, voided sales, case-pack sales and items a store does not range are each treated differently.
  - Stock counts are missing, negative, duplicated or conflicting, and nobody can say whether a shelf was empty or the count was wrong.
description: For each approved store, SKU and day, publish units sold, sellable stock on hand, the sell-through rate, and out-of-stock and at-risk states under the approved definitions, each flag with its reason, unknown where the stock position cannot be trusted, and every input record placed or listed with why not.
pitch: One row per store, SKU and day that says what sold, what is left and what is about to run out, with a reason on every flag and nothing dropped.
job_category: build
area: transformation
readiness: supported
function:
  - supply-chain-ops
industry:
  - retail
domain_objects:
  - store
  - sku
  - assortment_range
  - stock_position
  - sale_line
  - sell_through
  - stockout_state
  - stockout_risk
  - coverage_exception
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
  - Needs sale lines, a stock position per store, SKU and day (or movements), the ranging and any source the rules need.
  - A risk measure that reads past sales needs history before the first published day; shorter shows the approved treatment.
  - Stops at the day-grain states; forecasting, reorder quantities, available-to-promise and shelf life are separate.
  - Inputs are landed tables; loading files or extracts belongs to file-drop-to-bronze.
  - Conforming item codes across systems belongs to master-product-sku-hierarchy.
related:
  - ops-inventory-reconciliation
  - master-product-sku-hierarchy
  - effective-dated-business-rules
  - metric-population-and-rollups
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

Build <day_table>, <coverage_model> and <completeness_model> from <sale_line_source>, <stock_position_source>, <ranging_source> and any further source the approved definitions need. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only the semantics they leave open. For each approved store, SKU and day, publish the units sold, the sellable stock on hand, the sell-through rate, an out-of-stock state and an at-risk state under the approved definitions, give every state its reason, treat a day whose stock position cannot be trusted as the approved rules say and never infer an empty shelf from the gap unless they define it so, keep a day with no stock out of the rate of sale the risk reads unless the approved basis counts it, and place every record of every input in the table or list it with its reason. Keep sources read-only and report what the inputs cannot prove.

## Verified by

- On a run that completes, there is one row per approved store, SKU and day for every pair the approved ranging covers that day, including days with no sale and no stock movement, and none for a pair the ranging leaves out; each output is unique on its declared grain.
- Each row's sell-through rate equals the approved definition over its approved period, recomputed from figures shown on the row or traceable to source records; a non-positive approved denominator follows the approved treatment with its reason and is never silently zero unless approved.
- Units sold follow the approved treatment of returns, voids and recorded units: each return lands on the day the approved rule gives it, a voided line counts as the approved rule says, and a sale in a unit with no approved conversion is never guessed and is handled as approved.
- Sellable stock on hand follows the approved eligibility, units the approved rules hold out stay visible beside it, and a position that cannot be trusted is shown as recorded, as missing, or with the approved substitute labelled as such.
- Out of stock follows the approved definition on every row, a day that ran out and was restocked is judged as approved, each flagged row carries its reason, and where the definition needs evidence the inputs lack (such as intraday stock) the state reads unknown with that reason.
- A day whose stock count is missing, negative, duplicated or conflicting is handled as approved: out-of-stock and at-risk read unknown, never false, unless the approved rule gives another disposition, and no empty shelf or zero stock is inferred from the gap unless the approved rule defines it so.
- The at-risk state follows the approved measure with its reason and the figures behind it; a day the approved basis leaves out of the rate of sale does not lower it, and an item with too little history or no recent sales shows the approved treatment and says why.
- On a run that completes, every sale line, stock count and ranging record lands in a row or is listed with one approved reason, per-input counts sum to the records read, and units sold and returned tie per store and day as the rules place them, each line placed once or split as approved.
- Records for a pair or day the approved ranging leaves out are listed with their reason and move no row.
- A run that cannot produce a trustworthy day, such as a missing or stale position feed, follows the approved behaviour (fail naming the cause, publish flagged, or publish nothing) and never publishes the day as complete.
- Changing a rule the approved requirements hold as data (thresholds, windows, minimum history, reasons and their order, unit conversions, ranging) changes the published figures without a code change, within the approved rule form, and the result still reconciles.
- Expected results for each stated behaviour are derived from the source records and approved rules by a calculation separate from the implementation, and the outcome states what the inputs cannot prove.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile the sale lines, stock positions and ranging for keys, grains, recorded units, statuses, day boundaries and time zones, and for how often a store-SKU-day has no position. Use Ask first only for semantics still open, and record each answer as the user's own decision. Keep thresholds, windows, minimum history, reasons and their order, unit conversions and ranging as editable data where the approved requirements say so. Derive expected results independently of the models and include a case for each approved treatment at its edge: an empty shelf inside the rate-of-sale window, a boundary at the risk threshold, a day restocked after running out, a return dated after its sale, a net-negative day, a missing, negative, duplicate and conflicting count, a sale of an unranged item, and a sale in a unit with no conversion. Before declaring the outcome complete, check that every row's states and reasons agree with the figures behind them, that every input record is placed once, that units tie per store and day, and that a changed rule moves only what it should.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which stores, SKUs and days are in scope, what is the day boundary and time zone, how is ranging held and dated, and which items count as ranged (new, delisted, seasonal, test, display-only)?
- If unresolved, how is sell-through defined (sold over sold plus closing stock, opening stock, or opening plus receipts) over what period, what does a non-positive denominator show, and what makes a day out of stock (closing at or below zero, any point in the day, all day)?
- If unresolved, what makes an item at risk (cover under a threshold, run-out projected from the approved rate of sale, unit floor), at what threshold and window, counting which days, does on-order or in-transit stock count toward cover, and what minimum history and no-sales display apply?
- If unresolved, which stock counts as sellable (damaged, quarantined, held, display, in transit, on order), is the position a closing snapshot or built from movements, and is stock above or below the recorded position a value or a problem?
- If unresolved, which sales channels count and on which date (transaction or fulfilment), how do returns (also to another store), voids, exchanges, bundles and sales in another or fractional unit count, on which day does a return land, and what do an unknown pack size and a net-negative day show?
- If unresolved, what happens on a day with no count (unknown, carried forward, or no row meaning zero stock), a negative count, two identical counts or two that disagree, and which reason is given when several fit?
- If unresolved, when a run cannot produce a trustworthy day (a stale feed, an unplaceable record), does it fail, publish flagged or publish nothing, are late or corrected counts and sales applied to published days, and which reasons name records set aside?
- If unresolved, how do sale, stock and ranging item and store codes resolve to one key, and is a code that resolves to none listed, excluded or a failure?

### Guardrails

- Do not choose the sell-through definition, out-of-stock test, risk measure, threshold, window, stock eligibility, return and unit treatment, missing-count rule, ranging or failure behaviour for the user, or take them from common practice; the user may ask for a recommendation.
- Never read a missing, negative or conflicting stock position as an empty shelf or as zero stock unless the approved rules define it so, and never carry a count forward unless approved.
- Never let a day with no stock lower the rate of sale the risk reads unless the approved basis counts it, and never present infinite cover as a number.
- Never guess a unit conversion the approved rules do not give, and never drop, double count or default an unplaceable record; every record of every input stays accounted for, including voided, unranged and duplicate records.
- Never publish a day as complete when the run could not establish the stock feed for that day.
- Never restate a published day with a late or corrected count or sale unless the approved rules say so.
- Do not hold a rule the approved requirements treat as data as a literal in the models; keep it as data that the models and tests read.
- Stop at the day-grain states: do not forecast demand, set reorder quantities or promise availability, and keep sources read-only.
