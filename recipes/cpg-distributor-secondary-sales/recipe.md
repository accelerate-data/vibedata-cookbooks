---
id: cpg-distributor-secondary-sales
title: Reconcile sell-in, sell-out and channel stock in a distributor ledger and a market view labelled by feed coverage
trigger:
  - Sales ops, demand planning and channel finance each report a different sell-in, sell-out and channel stock figure, because distributors report in different units, codes and cutoffs.
  - A distributor's reported closing stock does not equal its opening stock plus receipts less sales, and nobody can say whether a movement, a late feed or a restatement explains it.
  - Sell-in is read as demand, although stock sits in transit, in the channel, or moves between distributors, and a missing distributor feed makes the market total look smaller than it is.
  - Distributor feeds arrive separately and are resubmitted, and records with unmapped codes or unconvertible packs drop out with no stated reason.
description: Per approved distributor, product and fiscal month, publish a stock ledger in the base unit with exact variance, split sell-in into received and in transit, give a market view labelled by feed coverage, and place every input record once or set it aside with a reason.
pitch: One stock ledger per distributor and product that foots to the unit, a market view that says what feed is missing, and a reason on every record set aside.
job_category: build
area: transformation
readiness: supported
function:
  - supply-chain-ops
  - revops
industry:
  - cpg
domain_objects:
  - distributor
  - product
  - shipment_line
  - receipt_line
  - secondary_sale
  - inventory_snapshot
  - channel_stock
  - unit_of_measure
  - feed_coverage
  - channel_exception
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
  - Needs landed shipment, distributor sale and stock tables; other feeds and pack or code maps where held or supplied.
  - Resubmission precedence needs a submission identity and recorded time; without them, restatement is reported unproven.
  - Base-unit quantities only; retail sell-through, gross-to-net and forecasting are separate outcomes.
  - Reconciling one company's WMS, ERP and counts belongs to ops-inventory-reconciliation.
  - Assessed end to end on duckdb_local only; other listed targets rely on dbt support and are unassessed.
  - Exported files go to file-drop-to-bronze first.
related:
  - retail-sell-through-stockout
  - ops-inventory-reconciliation
  - cpg-promotion-lift
  - effective-dated-business-rules
  - master-product-sku-hierarchy
  - file-drop-to-bronze
evidence:
  features:
    - capturing-requirements
    - generating-dbt-model
    - verifying
  evals: []
---

## Prompt

Build <ledger_model>, <market_model>, <feed_coverage_model> and <exceptions_model> from <shipment_source>, <secondary_sales_source>, <inventory_snapshot_source>, <receipt_source> where receipts are a separate feed, <return_source> where returns are a separate feed, <transfer_source> where transfers are a separate feed, <pack_mapping_source> and <code_crosswalk_source> where held or supplied. Inherit the semantics the Intent's approved requirements establish, and resolve with the user only those they leave open. Per approved distributor, product and fiscal month in the base unit, publish opening, receipts, transfers in and out, returns to the manufacturer, sell-out, outlet returns, adjustments, computed closing, the distributor's reported closing and the exact variance between them. Split manufacturer shipments into received and in transit at the approved cutoff, publish a market view with sell-in beside sell-out and channel stock, the last two each saying which distributor feeds are missing, show each distributor's feed state per month, and place every input record once or set it aside with one reason. Keep sources read-only and report what the inputs cannot prove.

## Verified by

- On a run that completes, each ledger row foots exactly in the base unit: opening plus receipts and transfers in, less transfers out, returns to the manufacturer and sell-out, plus outlet returns and adjustments equals computed closing, up to any approved rounding shown beside it.
- Variance is the distributor's reported closing less computed closing, shown and never plugged into a movement; it is blank where no snapshot was reported, and a month that opens away from the prior reported closing shows the break.
- Each shipment line splits into received and in transit at the approved cutoff; a receipt with no shipment, one before its shipment and one beyond the shipped quantity are each flagged with the amount, and move stock only as approved.
- Transfers between distributors and sales to a distributor in the panel never enter market sell-out unless approved; a one-sided transfer stays visible, and in-transit quantity keeps shipments from the manufacturer apart from transfers between distributors where approved.
- Each market row shows sell-in beside sell-out, never sell-in read as demand, and labels sell-out and channel stock complete or incomplete, naming the distributors whose feed is missing; no missing feed is imputed or carried forward unless approved.
- Each distributor, month and feed has a state under the approved expected range and lateness rule; a month with no feed shows as missing, never as zero.
- A resubmitted or duplicate submission follows the approved precedence, the superseded one stays visible with its count, and a restated month is counted once.
- A computed negative stock is flagged and kept; any displayed floor follows the approved rule and the unclipped amount stays observable; a month, record or distributor the approved rules leave out is listed with its reason and moves no ledger measure.
- On a run that completes, every input record is placed in the ledger, the in-transit split or the market view, or set aside with one reason, traced to all its contributions (a transfer reaches both sides); per input the counts sum to the records read; a flag on a counted record is listed apart.
- A record with an unconvertible or ambiguous pack, an unmapped or ambiguous code, an unknown distributor or a late submission follows the approved disposition: listed with its reason, or the run fails naming it; it never changes another key.
- The published ledger, market view and coverage equal values derived independently from the sources and the approved rules, and each output is unique on its declared grain.
- Changing a rule the approved requirements hold as data (pack mapping, crosswalk, cutoff, tolerance, expected range) changes the published figures without a code change within the approved rule form, and the ledger still foots.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile each feed for keys, units, versions, dates and submission times before modelling. Derive expected results independently of the models, from the approved rules and the input rows, before any model is built, and include a case for each approved treatment at its edge: a pack change within a period, a code no mapping resolves, a transfer seen by one side only, a receipt beyond its shipment, a month with no snapshot, a resubmitted month, and a stock that goes negative. Keep each rule the requirements treat as data as data that the models and tests read, never as a literal. Before declaring the outcome complete, check that every ledger row foots, that every input record is placed once, and that a changed rule moves only what it should; report what the inputs cannot prove.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which distributors, sites (several may roll up to one distributor, a move between them internal), products and calendar are in scope, what is the base unit, which pack mappings apply on each date, and how is a record with a missing, ambiguous or fractional pack factor handled?
- If unresolved, how does each distributor's product and distributor code resolve to one key on a date, and is a code that resolves to none or to several set aside, failed or listed?
- If unresolved, which keys link a receipt to a shipment line, what makes a shipment received or in transit, when does an unreceived remainder stop being in transit (refused, lost, written off), and how are a receipt with no shipment, one before it and one beyond the shipped quantity handled?
- If unresolved, is a transfer a movement between distributors, how is a sale to another panel distributor or an outside sub-distributor treated, and is a transfer one side reports sell-out, a transfer or unmatched?
- If unresolved, how are returns to the manufacturer, outlet returns, adjustments, free, scheme or sample goods and cancelled or negative sale lines carried, and is market sell-out gross or net of outlet returns?
- If unresolved, what opens the first month and each later month (prior reported or prior computed closing), what happens when they differ, which months a pair covers, what tolerance applies to variance, and is a negative computed stock flagged or floored?
- If unresolved, which submission wins per distributor, month and feed, how are ties and duplicates handled, which cutoff and period rule decide late or restated records, how does a record date map to a fiscal month, and what are each feed's expected range, lateness and missing-time handling?
- If unresolved, which distributors does a market row expect per product, which stock statuses, ownership and lots count in closing and channel stock, and with a feed missing does channel stock cover every holder (missing feed named) or only those reporting, or is anything imputed?

### Guardrails

- Do not choose units, mappings, link keys, transfer treatment, opening basis, tolerance, precedence, cutoff or the channel stock basis for the user, and take none from the data or common practice; the user may ask for alternatives or a recommendation.
- Never read sell-in as demand, never count a transfer between distributors as sell-out unless approved, and never present a market figure as complete while a distributor feed is missing.
- Never plug a variance into a movement, never hide a negative stock (a clipped display needs an approved rule), and keep a difference no rule explains visible.
- Never read an absent feed or snapshot as zero, and never guess a pack size or map a code by name.
- On a run that completes, never drop or double count a record: every record of every input stays accounted for, including superseded, late, set-aside and flagged ones.
- Do not hold a rule the approved requirements treat as data as a literal in the models; keep it as data that the models and tests read.
- Stop at the channel quantities: do not value stock, plan replenishment or post adjustments to a distributor or ERP system, and keep sources read-only.
