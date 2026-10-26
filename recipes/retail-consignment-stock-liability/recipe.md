---
id: retail-consignment-stock-liability
title: Reconcile consignment stock by owner and the amount owed to each supplier when their stock sells
trigger:
  - A supplier owns stock until it sells, that stock shares a store and SKU with stock we bought outright, and the stock report adds the two together.
  - Finance cannot say what is owed to each supplier because receipts, sales, returns, counts and settlements sit in different places and each treats consigned stock differently.
  - A customer return or a stock count lands against a store and SKU holding several owners' stock and nobody can say whose stock or whose obligation it changes.
description: At the approved dates and grains, publish stock by owner at each store and SKU with owned and consigned stock kept apart, the supplier obligation the approved liability event creates, reverses and settles, one movement ledger tying units and amounts to both, and every input record placed or set aside with a reason.
pitch: Know whose stock is on each shelf and what each supplier is owed, with nothing owed on receipt and every unit and amount tied back.
job_category: build
area: transformation
readiness: supported
industry:
  - retail
function:
  - finance
  - supply-chain-ops
domain_objects:
  - consignment_stock
  - stock_owner
  - supplier_contract_version
  - consignment_obligation
  - supplier_settlement
  - stock_movement
  - stock_count
  - item_location
  - consignment_exception
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
  - Inputs are landed tables; loading files or extracts belongs to file-drop-to-bronze.
  - The owner of a sale comes from the source or an approved attribution rule; a sale with neither is set aside.
  - Amounts stay in the contract currency unless approved conversion rates are supplied.
  - Stops at stock by owner and the supplier obligation; paying suppliers and posting entries are separate.
  - Repricing sales after the terms change needs dated contract versions; without them restatement is unproven.
related:
  - ops-inventory-reconciliation
  - inventory-valuation-cogs
  - procurement-three-way-match
  - procurement-supplier-rebate-accrual
  - retail-sell-through-stockout
  - effective-dated-business-rules
  - file-drop-to-bronze
evidence:
  features:
    - capturing-requirements
    - applying-medallion-data-modelling
    - generating-dbt-model
    - running-dbt-in-sandbox
    - verifying
  evals: []
---

## Prompt

Build <owner_stock_model>, <movement_ledger_model>, <supplier_obligation_model>, <exception_model> and <coverage_model> from <receipt_source>, <sale_source>, <return_source>, <stock_count_source>, <contract_version_source> and <settlement_source>. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only the semantics they leave open. At the approved dates and grains, publish stock by owner at each store and SKU with our own stock and each supplier's consigned stock kept apart even where they share a location and SKU, and create, reverse and settle the supplier obligation under the approved liability event, amount basis, return, count and settlement rules, so that receiving consigned stock never creates an ordinary purchased-stock payable and a return changes only the owner and obligation the approved rules name. Tie units and amounts through one movement ledger to the stock and to the obligation, place every input record once as counted, in a difference or set aside with one reason, keep the contract terms and every rule the approved requirements hold as data, keep sources read-only and report what the inputs cannot prove.

## Verified by

- On a run that completes, each approved store, SKU, owner and date has its own row with opening, received, sold, returned and closing units, and owned stock and each supplier's stock are never added together or read from one summed position.
- Receiving consigned stock creates no payable and its ledger row carries no amount; the obligation arises on the event the approved liability event names, dated and priced as approved from the approved amount basis, and no obligation exists without that event.
- A customer return changes only the owner and obligation the approved rule names, at the approved amount, and no other owner's stock or obligation moves; a return the approved link rule cannot match, or that exceeds what it returns, is listed with its reason.
- A sale that names no owner, exceeds its owner's stock or has no contract terms in force follows the approved disposition, is listed with its reason, is never charged to another owner's stock and is never priced at zero or from a default.
- A stock count changes an owner's stock or obligation only as the approved rule says; a difference no approved rule attributes stays visible with its reason and is never absorbed into an owner or an obligation.
- A settlement discharges only what the approved rule lets it; an excess, and any return amount that rule cannot reverse against an open balance, is shown as its own amount or listed as approved, never netted into another supplier or period or hidden as a silent negative balance.
- Each priced amount uses the contract version the approved rule selects; a change in terms or a late record moves an earlier published figure only as the approved rule says, shown and never silent, and a date no version governs follows the approved disposition.
- Per store, SKU and owner the ledger's signed units equal closing units, and per supplier the ledger's sale and return amounts equal the obligation created and reversed, plus any difference the approved rule shows with its reason.
- Per supplier and period the obligation rolls forward: opening, created, reversed, discharged and closing foot, with any credit or excess the approved rules show beside them; amounts keep their currency and are never summed across currencies.
- On a run that completes, every input record is placed once as counted, in a difference or set aside with one reason, per-input counts sum to the records read, and records the approved scope leaves out are shown or counted with their reason as approved.
- Published stock, obligation and exception figures equal values derived independently from the sources and the approved rules, and each output is unique on its declared grain.
- Changing a rule held as data (contract terms, dates, tolerances) changes the published figures without a code change, within the approved rule form, and the result still ties out.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile each input for owner tags, keys, units, dates and posted times, and check the contract version windows for gaps and overlaps and the level at which counts are taken before modelling. Derive the expected results independently of the models from the source rows and the approved rules, and include a case for each approved branch at its edge, such as owned and consigned stock sharing a location, a sale that names no owner or exceeds its owner's stock or has no terms in force, terms that change inside the window, a return with and without its sale and one after the supplier was settled, a count that is explained and one that is not, and settlements that cover, undershoot, overshoot or name a period holding no obligation. Keep each rule the approved requirements treat as data as data that the models and tests read, never as a literal. Before declaring the outcome complete, check that units and amounts tie through the ledger, that every input record is placed once, and that a changed rule moves only what it should; report what the inputs cannot prove.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which stores, SKUs, suppliers and entities are in scope, which ownership types count and which statuses stay out (quarantine, in transit), and which locations or item classes are left out, shown or only counted?
- If unresolved, what makes a sale qualify to create the obligation and which date the obligation carries, does the sale or the supplier's statement fix the amount, and does a sale that cannot be priced still move the owner's stock?
- If unresolved, which amount basis applies (fixed unit cost, share of net price, tiers, tax in or out), which contract version governs (sale, receipt or settlement date), how a gap, overlap or ambiguity is handled, and does a later change in terms restate priced sales?
- If unresolved, how a sale reaches an owner where own and consigned stock share a location (the sale names it, oldest receipt first, own first or consigned first), and is a sale beyond its owner's stock a permanent exception, held until covered or allowed to run negative?
- If unresolved, which key links a customer return to its sale, is it reversed at the original or the current terms, what happens to one after the supplier was settled or beyond what was sold or naming a set-aside sale, and what does a return to the supplier change?
- If unresolved, at what level is a count taken, which owner absorbs a shortfall or surplus (own stock, pro rata, the supplier, or held unexplained), what tolerance applies, and which dates, grain and cutoff is stock published at?
- If unresolved, how is a settlement applied (named period, oldest first or by reference), how is a short, excess or other-currency payment shown or converted, and which liability grain, months and event month are published?
- If unresolved, how each source's codes resolve to one key, how a duplicate, blank, unknown, unreadable or late-posted record is treated, which unit and precision apply, and does a leftover difference fail the run or stay listed?

### Guardrails

- Do not choose the liability event, amount basis, contract version rule, owner attribution, return, count or settlement treatment, scope or bad-record handling for the user, and take none from the data, a vendor default or common practice; the user may ask for alternatives or a recommendation.
- Never create an ordinary purchased-stock payable from the receipt of consigned stock, and never read a missing owner, price, quantity or contract version as owned stock or as zero unless an approved rule defines it.
- Never add owned stock to a supplier's stock or one supplier's stock to another's, and never let a return, count or settlement change an owner or obligation the approved rules do not name.
- Never absorb an unexplained difference into an owner or an obligation, net a credit or excess into another supplier or period unless approved, or convert a currency without an approved rate.
- On a run that completes, never drop or double count a record: every record of every input stays accounted for, including excluded, set-aside and problem records.
- Do not hold a contract term or any rule the approved requirements treat as data as a literal in the models; keep it as data that the models and tests read.
- Do not pay a supplier, post an entry or write back to a source system, and stop at stock by owner and the supplier obligation: do not value owned stock or match invoices.
