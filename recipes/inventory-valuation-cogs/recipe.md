---
id: inventory-valuation-cogs
title: Value inventory movements, closing stock and cost of goods sold under an approved costing policy
trigger:
  - Finance cannot say what closing inventory is worth or how much cost of goods sold a month carries because receipts, issues, returns and adjustments are costed by hand.
  - A late or backdated receipt arrives and nobody can say which issues, periods and cost figures it changes.
  - The books are about to close and a missing cost, a return or an issue beyond stock on hand has quietly become zero in the valuation.
description: Under one approved costing policy and reporting currency, value each stock movement in a ledger, publish closing stock and cost of goods sold by approved period, keep quantity and value conserved, and list what cannot be valued instead of costing it at zero.
pitch: Value every stock movement and cost of goods sold under one approved costing policy, with no missing cost quietly becoming zero.
job_category: build
area: transformation
readiness: supported
function:
  - finance
  - supply-chain-ops
domain_objects:
  - inventory_valuation
  - stock_movement
  - costing_pool
  - cost_of_goods_sold
  - period_rollforward
  - valuation_exception
  - item_location
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
  - Inputs are landed stock-movement tables; loading files or extracts belongs to file-drop-to-bronze.
  - One costing policy and one reporting currency per run; currency conversion is upstream work.
  - Stops at valued inventory and COGS; counts, stockout risk and ledger posting are separate outcomes.
  - Restating for a backdated movement needs an entry or posting time on each movement; without it restatement is unproven.
related:
  - ops-inventory-reconciliation
  - finance-gl-subledger-tieout
  - shared-fx-conversion
  - effective-dated-business-rules
  - bitemporal-business-history
  - shared-calendar-fiscal-periods
  - file-drop-to-bronze
---

## Prompt

Build <inventory_ledger_model>, <stock_rollforward_model>, <cogs_model> and <unvaluable_model> from <stock_movement_source>. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only the semantics they leave open. Under the one approved costing policy and reporting currency, value each approved receipt, issue, return and adjustment in the approved order and costing grain, publish quantity and value running balances, a period roll-forward whose opening plus movements equals closing, and cost of goods sold by period that ties to it. List every movement or amount that cannot be valued with its reason instead of valuing it at zero, place every input movement once, keep sources read-only and stop at valued inventory and cost of goods sold.

## Verified by

- Under one approved policy and reporting currency, each applied movement appears once in the ledger with quantity, value and running balances; every output names the policy and currency, and values under different policies are never mixed in one figure.
- Ledger values, closing stock and cost of goods sold equal values derived independently from the movements and the approved rules, including a hand-calculated case for each approved rule at its edge, such as an issue drawing on stock bought at different costs.
- Per approved costing grain and period, opening plus receipts, returns, gains and approved transfers in, minus issues, losses and transfers out, equals closing in quantity, and in value where known, plus any residue or variance the approved rule shows; the first opening is the approved opening.
- Where values are known, cost of goods sold per period and in total ties to the roll-forward at the approved precision, counts only what the approved rules call cost of goods sold, counts each correction once, and keeps other consumption and adjustments visible as their own terms.
- A movement with no usable cost, a gain with no stated cost basis, an unlinked return or an amount in another currency is never valued at zero: it follows the approved disposition, listed with its reason or failing the run naming it, and affected values are never a complete total.
- A movement that arrives after later movements were valued follows the approved rule: later figures are restated with changed amounts and their cause identifiable, or it posts as a current-period adjustment; no published figure changes silently.
- A return is valued and linked to what it reverses as approved; a return the approved keys cannot link, or that exceeds what it reverses, follows the approved disposition, listed with its reason, and no link or cost is guessed.
- An issue beyond stock on hand follows the approved rule (blocked, costed provisionally and flagged, or left unvalued): it never silently takes zero cost, its state stays visible, and a later settling receipt shows its difference as a labelled amount where the rule provides one.
- On a run that completes, every input movement is accounted for once as applied, set aside with a reason or listed as a problem, counts sum to the rows read, and duplicates, transfers, other units and unknown codes follow approved dispositions without moving other keys' values.
- Records the approved scope leaves out are shown or counted with their reason as approved, and the outcome states how many were excluded and why.
- Each output is unique on its declared grain, nothing is summed across locations, currencies or periods the approved rules keep apart, a movement at a period edge falls in exactly one period, and quiet periods appear where the approved grain publishes them.
- A conservation or tie-out gap the approved tolerance does not allow is shown with its amount and reason and reported failed or unverified for that key, or fails the run as approved; it is never a pass.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile the movements for keys, types, reasons, units, currencies, event and entry times, duplicates and costs before modelling. Derive the expected results independently of the models, by hand from the approved rules, and include a case for each approved rule at its edge: an issue drawing on stock bought at different costs, a late or backdated receipt, a return of such an issue, a shortfall followed by a covering receipt, a missing cost, a period boundary and the same item in two locations. Keep each approved rule the requirements treat as data as data that the models and tests read, never as a literal. Before declaring the outcome complete, check conservation in quantity and value, that cost of goods sold ties to the roll-forward, that every input movement is placed once and that what cannot be valued is listed; report what the inputs cannot prove.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which costing method (first-in first-out, weighted average, specific, standard), costing grain (item, location, lot) and reporting currency apply, and is a movement in another currency listed or a failure?
- If unresolved, which items, locations, entities and ownership types are in scope (consigned, third-party, memorandum, test), are codes no master resolves listed or failed, and which movement types count in valuation and which count as cost of goods sold (transfers, scrap, samples, adjustments)?
- If unresolved, in which order are movements valued (event or posting time, tie-break), which time zone and period boundaries apply, what supplies opening stock and its cost, and does a backdated movement restate later figures or post as a current-period adjustment; is a closed period locked?
- If unresolved, at what cost does a return re-enter stock, which keys link it to the issue it reverses, and is an unlinked or over-returned quantity listed, valued another way or a failure?
- If unresolved, may stock go negative, how is an issue beyond stock costed (last known cost, standard cost or left unvalued), how does a later receipt settle it, and where does a cost difference land, including a standard-cost variance?
- If unresolved, what happens to a receipt with no cost or a zero cost, how is a gain costed, and how far does an unvaluable movement reach (that costing grain, the item or the run)?
- If unresolved, how are duplicate movement ids handled when identical or conflicting, which units of measure are valid per item and is any other unit converted or listed, and what quantity precision and rounding apply and where does a residue go?
- If unresolved, which periods and cuts are published, are quiet periods shown, are out-of-scope records listed or only counted, what tolerance applies to a conservation or tie-out gap, and does an unvaluable item or a gap beyond it fail the run or stay listed?

### Guardrails

- Do not choose the costing method, costing grain, backdating rule, return cost, shortfall rule, missing-cost handling or period boundary for the user, and take none from the data or common practice; the user may ask for alternatives or a recommendation.
- Never read a missing, blank or unusable cost as zero, never present a partial sum as a closing value or total, and keep every unvaluable movement visible with its reason.
- Never mix values from different costing policies, currencies, locations or periods in one figure, and never convert a currency or a unit the approved rules do not convert.
- Never let a backdated movement change a published figure silently, and never count a restatement, true-up or correction twice.
- On a run that completes, never drop or double count a movement: duplicates, transfers, out-of-scope, other-unit and problem records stay accounted for.
- Do not hold a rule the approved requirements treat as data as a literal in the models; keep it as data that the models and tests read.
- Stop at valued inventory and cost of goods sold: do not post journals, reconcile quantities to counts, plan stock or model stockout risk, and keep sources read-only.
