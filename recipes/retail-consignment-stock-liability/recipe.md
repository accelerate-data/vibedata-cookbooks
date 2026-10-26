---
id: retail-consignment-stock-liability
title: Reconcile consignment stock by owner and the amount owed to each supplier when their stock sells
trigger:
  - A supplier owns stock until it sells, that stock shares a store and SKU with stock we bought outright, and the stock report adds the two together.
  - Finance cannot say what is owed to each supplier because receipts, sales, returns, counts and settlements sit in different places and each treats consigned stock differently.
  - A customer return or a stock count lands against a store and SKU holding several owners' stock and nobody can say whose stock or whose obligation it changes.
description: At the approved dates and grains, publish stock by owner at each store and SKU with owned and consigned stock kept apart, the supplier obligation the approved liability event creates, reverses and settles, one movement ledger tying units and amounts to both, and every input record accounted for.
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
  - supplier
  - supplier_contract
  - supplier_settlement
  - consignment_stock
  - stock_owner
  - consignment_obligation
  - stock_movement
  - stock_count
  - item_location
  - consignment_exception
works_with:
  platforms:
    - duckdb_local
    - motherduck
    - fabric_warehouse
    - redshift
  tools:
    - dbt
qualifiers:
  - Assessed end to end on duckdb_local only; the other listed targets rely on dbt support and are unassessed.
  - Inputs are landed tables; loading files or extracts belongs to file-drop-to-bronze.
  - A sale's owner comes from the source or an approved rule; a sale with neither follows the approved disposition.
  - Amounts stay in the contract currency unless approved conversion rates are supplied.
  - Stops at stock by owner and the supplier obligation; valuing stock, comparing systems, matching and paying are separate.
  - Obligations from the passage of time (aged-stock title transfer), minimum guarantees or tax postings are separate.
  - Repricing sales after the terms change needs dated contract versions; without them restatement is unproven.
  - A late or backdated record is detected only with a posted time; without one restatement is unproven.
related:
  - ops-inventory-reconciliation
  - inventory-valuation-cogs
  - procurement-three-way-match
  - procurement-supplier-rebate-accrual
  - retail-sell-through-stockout
  - effective-dated-business-rules
  - shared-fx-conversion
  - shared-calendar-fiscal-periods
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

Build <owner_stock_model>, <movement_ledger_model>, <supplier_obligation_model>, <exception_model> and <coverage_model> from <receipt_source>, <sale_source>, <return_source>, <stock_count_source>, <contract_version_source>, <settlement_source> and, where approved, <opening_position_source>, <statement_source> and <adjustment_source>. Inherit approved semantics; ask only what they leave open. At the approved dates and grains, publish stock by owner at each store and SKU with our own stock and each supplier's stock kept apart even at a shared location and SKU, and create, reverse and settle the supplier obligation under the approved liability, amount, return, count and settlement rules, so that receiving consigned stock never creates an ordinary purchased-stock payable and a return changes only the owner and obligation the approved rules name. Tie units and amounts through one movement ledger to the stock and the obligation from the approved opening, account for every input record as counted, in a difference or set aside with one reason, keep the contract terms and every rule the approved requirements hold as data, keep sources read-only and report what the inputs cannot prove.

## Verified by

- On a run that completes, each approved store, SKU, owner and date has a row of opening, received, sold, returned and closing units; no stock figure adds owned to supplier stock or one supplier's to another's, and a count above owner level meets combined units only as a labelled reconciliation line.
- Receiving consigned stock creates no payable and its ledger row carries no amount; an obligation arises only on an event the approved rules name, such as the sale or an approved shortfall treatment, dated and priced as approved.
- A customer return or void changes only the owner and obligation the rule names, at the approved amount, moving no other owner's stock or obligation; a return the approved link rule cannot match, or that exceeds its sale, follows the approved disposition, listed with its reason if the run completes.
- A sale the approved attribution rule cannot place (no owner, beyond its stock, or no terms in force) follows the approved disposition, listed with its reason when the run completes; it is never priced at zero or from an unapproved default, and a split sale keeps each part with its own owner.
- A stock count changes an owner's stock or obligation only as the approved rule says; a difference inside the approved tolerance stays visible and is matched only as the rule says, and one no approved rule attributes stays visible with its reason, never absorbed into an owner or an obligation.
- A settlement discharges only what the approved rule lets it; an excess, and any return amount that cannot be reversed against an open balance, is shown as its own amount or listed as approved, and nets into another period or supplier only as approved, labelled, never as a silent negative balance.
- Each priced amount uses the contract version the approved rule selects; a change in terms, a crossed tier or a late record moves an earlier published figure only as the approved rule says, shown and never silent, and a date no version governs follows the approved disposition.
- Per store, SKU and owner the approved opening plus the ledger's signed units equal closing units, and per supplier the ledger's amounts, each on the event the approved rules name, equal the obligation created and reversed plus any difference the approved rule shows, up to the approved rounding.
- Per supplier and period, opening, created, reversed, discharged and closing foot from the approved opening up to the approved rounding, with any credit or excess the approved rules show beside them; amounts keep their currency and entity and sum across currencies only under an approved translation.
- On a run that completes, every input record is counted, in a difference or set aside with one reason; one both counted and listed (a sale that moved units but had no price) shows as both, per-input counts sum to the records read, and out-of-scope records are shown or counted with their reason.
- Published stock, obligation and exception figures equal values derived independently from the sources and the approved rules, and each output is unique on its declared grain.
- Changing a rule held as data (contract terms, dates, tolerances) changes the published figures without a code change, within the approved rule form, and the result still ties out.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile each input for owner tags, keys, units, dates and posted times, and check the contract version windows for gaps and overlaps, the level at which counts are taken and what supplies the opening position before modelling. Derive the expected results independently of the models from the source rows and the approved rules, and include a case for each approved branch at its edge, such as owned and consigned stock sharing a location, a sale that cannot be placed or is split across owners, terms that change inside the window, returns with and without their sale, after the supplier was settled, and a voided sale, explained and unexplained count differences, settlements that cover, undershoot, overshoot or name a period holding no obligation, a shortfall, a transfer, a rounding edge and a late-posted record. Keep each rule the approved requirements treat as data as data that the models and tests read, never as a literal. Before declaring the outcome complete, check that units and amounts tie through the ledger from the approved opening, that every input record is accounted for, and that a changed rule moves only what it should; report what the inputs cannot prove.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which stores, SKUs, suppliers and legal entities are in scope, which ownership types count, which statuses stay out, how each source's codes resolve to one key, which units, pack factors and precision apply, and which records are left out, shown or only counted?
- If unresolved, what makes a sale qualify to create the obligation and which date it carries, does the sale or the supplier's statement fix the amount, does an unpriced sale move stock, and do a shortfall or damage reduce supplier stock, create an obligation or stay held?
- If unresolved, which amount basis applies (fixed unit cost, share of net price, tiers), what net price and tax mean, for tiers which volume counts, whether a crossed tier reprices earlier sales and how it reaches each sale line, and what rounding point and mode apply?
- If unresolved, which contract version governs (sale, receipt or settlement date), how a gap, overlap or ambiguity is handled, does a later change in terms or a late-posted record restate priced sales, and what supplies the opening stock, open obligations and the sales they come from?
- If unresolved, how a sale reaches an owner where own and consigned stock share a location (names it, oldest receipt first, own first, consigned first, split), is a sale beyond its owner's stock an exception, held or allowed negative, and which store transfers are in scope?
- If unresolved, which key links a customer return to its sale, is it reversed at the original or current terms, what happens to one after settlement, beyond what was sold or naming a set-aside sale, how is a voided or cancelled sale treated, and what does a return to the supplier change?
- If unresolved, at what level is a count taken, which owner absorbs a shortfall or surplus (own stock, pro rata, supplier or held), what tolerance applies, and which dates, grain, owner rows, cutoff, time zone and calendar publish stock, and which period a return or settlement lands in?
- If unresolved, how is a settlement applied (named period, oldest first, reference), how are a reversal, deduction, short, excess or other-currency payment shown or converted (rate and date), how is a bad record treated, and does a leftover fail the run?

### Guardrails

- Do not choose the liability event, amount basis, contract version rule, owner attribution, return, count or settlement treatment, scope or bad-record handling for the user, and take none from the data, a vendor default or common practice; the user may ask for alternatives or a recommendation.
- Never create an ordinary purchased-stock payable from the receipt of consigned stock, and never read a missing owner, price, quantity or contract version as owned stock or as zero unless an approved rule defines it.
- Never publish owned stock added to a supplier's, or one supplier's to another's, as a stock figure (a count above owner level meets the combined units only as a labelled reconciliation), and never let a return, void, count or settlement change an owner or obligation the approved rules do not name.
- Never absorb an unexplained difference into an owner or an obligation, net a credit or excess into another supplier or period unless approved, or convert a currency without an approved rate.
- Never add or net quantities across units of measure, legal entities or currencies the approved rules keep apart, and never convert a unit the approved rules do not convert.
- On a run that completes, never drop or double count a record: every record of every input stays accounted for, including excluded, set-aside and problem records; one both counted and listed shows as both, once each.
- Do not hold a contract term or any rule the approved requirements treat as data as a literal in the models; keep it as data that the models and tests read.
- Do not pay a supplier, post an entry or write back to a source system, and stop at stock by owner and the supplier obligation: do not value owned stock or match invoices.
