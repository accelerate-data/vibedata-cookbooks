---
id: procurement-savings-realization
title: Reconcile negotiated procurement savings to realized invoice prices in a traceable savings ledger
trigger:
  - Procurement reports savings from negotiated agreements and Finance cannot trace them to the prices actually paid.
  - A lower negotiated target, a new pack size or a different currency is reported as a saving although the price paid did not fall.
  - A rebated amount is counted in a savings figure and again in a rebate figure, and nobody can say which.
description: For the approved period, compare approved baseline prices with the quantities and prices actually invoiced to build a ledger that classifies each claimed saving under the approved classes, such as realized, negotiated but not realized, cost avoidance, currency effect, price increase or unsupported, with every invoice line accounted for.
pitch: Show which procurement savings were actually paid, which were only negotiated, and why, line by line.
job_category: build
area: transformation
readiness: supported
function:
  - finance
  - supply-chain-ops
domain_objects:
  - baseline_price
  - supplier_contract
  - invoice_line
  - unit_conversion
  - savings_ledger
  - saving_class
  - savings_exception
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
  - Needs approved baseline prices, negotiated agreements and invoice lines; landing them is a separate outcome.
  - Baselines, conversions and rates need approval flags and effective dates; without them a row reads unproven.
  - Supplier identity and item specifications arrive conformed; matching suppliers is separate.
  - Stops at the savings ledger; spend cube, contract compliance, rebate accrual, rate setting and forecasting are separate.
  - States a price difference from the approved baseline, never that procurement caused it.
related:
  - ops-procurement-spend
  - procurement-three-way-match
  - shared-fx-conversion
evidence:
  features:
    - capturing-requirements
    - generating-dbt-model
    - verifying
  evals: []
---

## Prompt

Build <savings_ledger_model>, <line_accounting_model> and <coverage_model> from <baseline_price_source>, <agreement_source>, <invoice_line_source> and the unit conversion, rate and rebate sources the approved rules use. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only those they leave open. For the approved period, link each in-scope invoice line to its agreement and item, find the approved baseline in force, compare baseline and paid price on a comparable unit and currency, and give each ledger row its baseline, negotiated price, actual quantity, paid price, saving and approved class with its reason. Keep a lower negotiated target, a unit or currency change, an increase, a rebated amount and an unsupported comparison visible, and count each only as the approved rules say. Account for every invoice line once in a row or once as left out with its reason, and reconcile each claimed saving to baseline, quantity and paid price.

## Verified by

- On a run that completes, each ledger row's saving equals the approved baseline price times the actual quantity less the paid amount, on a comparable unit and currency within the approved rounding, recomputed independently from the baselines and invoice lines, never from a claimed total.
- A row whose paid price equals the approved baseline shows no realized saving even when the negotiated price is lower; any negotiated-but-unrealized amount appears apart as approved and is never counted as realized.
- A change of pack size, unit or specification creates no saving unless an approved conversion makes the prices comparable; a pair with no approved conversion shows as unsupported with its reason and stays visible.
- A change of currency creates no saving; an amount reached through an approved rate states the rate source and date and appears as the approved class, and without an approved rate the row is unsupported, never converted by a default.
- A paid price above the approved baseline shows as an increase with its amount and follows the approved treatment; it never reduces another row's saving unless an approved rule nets it.
- Cost avoidance and realized saving stay separate and each is shown only where the approved definition's evidence is present; where one row carries both, the components add to its saving, and totals never add them together unless approved.
- A rebated amount counts in this ledger or in the rebate ledger as approved, never both; a row carrying one states which, and an amount whose treatment is unproven is shown with that status.
- Credit notes and later changes to an invoice line follow the approved period treatment, and a period already published changes only as the approved rule says, never silently.
- On a run that completes, every input invoice line, credit note included, lands once in a ledger row or is left out with one reason, shown or counted as approved, and counts and amounts per currency tie to the input; a left-out line has zero counted saving.
- Each approved rule value, such as a baseline basis, tolerance, class definition or rate, changes the output where the data reaches it, within the approved rule form.
- Totals follow the approved cuts and hold only rows whose class counts toward them; each currency totals separately unless an approved conversion applies, and excluded classes appear beside the totals, not in them.
- Each row traces to the baseline version, agreement, invoice lines, conversion and rate it used; published descriptions state a price difference from the approved baseline, never that procurement caused it, and the outcome states what the inputs cannot prove.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile the baselines (versions, effective dates, approval flags), agreements (terms, negotiated prices, overlaps), invoice lines (dates, quantities, units, currencies, credits, rebate markers, lines with no agreement) and the conversion and rate sources before proposing rules. Use Ask first only for semantics still open, and record each decision as the user's own answer. Work out the expected ledger for the agreed cases independently of the models, from the source lines and the approved rules, before trusting the models, and include cases the inputs may not carry, such as a row mixing rebated and unrebated lines, overlapping agreements or terms, a unit or currency pair with only an unapproved row, and several invoice currencies in one row. Keep the baseline, conversion and rate rules editable as data where the approved requirements say so. Reconcile every ledger saving to its baseline, quantity and paid amount, and tie the line accounting to the input before declaring the work complete.

### Compose

- capturing-requirements
- applying-medallion-data-modelling
- generating-dbt-model
- verifying

### Ask first

- If unresolved, what sets an approved baseline price (last paid, prior-period average, list, budget or another basis), who approves it, how are its versions and effective dates applied to an invoice date, and what follows when none is in force or several overlap?
- If unresolved, which saving classes exist and how is each defined (realized, negotiated but not realized, cost avoidance, currency effect, price increase), what evidence does cost avoidance need, which class wins when several apply, and which classes count toward totals?
- If unresolved, which keys link an invoice line to an agreement and item (supplier, item, contract or order reference, specification), which agreement wins when several apply, and how are lines with no agreement, or outside its term, shown?
- If unresolved, which units, pack sizes and specifications are comparable, which approved conversions apply (per item or general, with effective dates), and what happens to a price that cannot be compared?
- If unresolved, which currency reports, are other currencies converted (rate source and date), kept apart or set aside, and is a currency effect its own class or part of another?
- If unresolved, is the paid price taken before or after line discounts, rebates and fees, which ledger holds a rebated amount so it counts once, and how do credit notes post (own period or the original's) and may they restate a published period?
- If unresolved, what is one ledger row (month, agreement, item, supplier or another cut), which date sets the period, how are several prices in one row weighted, and are periods with no purchase shown?
- If unresolved, which suppliers, spend types and invoice statuses (voided, held, disputed) are in scope, what happens to an unplaceable line (set aside and flagged, excluded or the run fails), what precision and reconciliation tolerance apply, and which totals are published?

### Guardrails

- Do not choose the baseline basis, class definitions, linking keys, comparability rules, currency treatment, rebate treatment, credit-note posting, grain, period or exception handling for the user, nor take them from the data or common practice; the user may ask for options or a recommendation.
- Never count a negotiated target, a unit or specification change, a currency change, an increase or a rebated amount as a realized saving unless an approved rule says so.
- Never compare prices across units or currencies unless an approved conversion or rate applies and states its source and date; never use a factor or rate of one, or a default, for a missing one.
- Never count a rebated amount in this ledger and in a rebate ledger.
- Never drop, double count or silently net away an invoice line, a credit note or an amount; a line left out stays accounted for with its reason and zero counted saving.
- Never read a missing baseline, agreement or price as zero, or call a row a saving on a baseline the inputs do not show; report what the inputs cannot prove.
- Never claim that procurement caused a price difference.
- Never restate a published period silently when a baseline, agreement or invoice line changes later.
- Stop at the savings ledger: do not build the spend cube, check contract compliance, accrue rebates, set rates or forecast.
