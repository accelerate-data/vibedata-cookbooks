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
  - exchange_rate
  - credit_note
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
  - Needs agreements, invoice lines and approved baselines, or the price history an approved baseline basis derives from.
  - Baselines, agreements, conversions and rates need an approval, and dates where versioned; else no saving.
  - Supplier identity and item specifications arrive conformed; matching suppliers is separate.
  - Stops at the savings ledger; spend cube, contract compliance, rebate accrual, rate setting and forecasting are separate.
  - States a price difference from the approved baseline, never that procurement caused it.
related:
  - ops-procurement-spend
  - procurement-three-way-match
  - shared-fx-conversion
  - effective-dated-business-rules
evidence:
  features:
    - capturing-requirements
    - generating-dbt-model
    - verifying
  evals: []
---

## Prompt

Build <savings_ledger_model>, <line_accounting_model> and <coverage_model> from <baseline_price_source> or the price history the approved basis uses, <agreement_source>, <invoice_line_source> and the unit conversion, rate and rebate sources the approved rules use. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only those they leave open. For the approved period, link each in-scope invoice line to its agreement and item, find the approved baseline in force, compare baseline and paid price on a comparable unit and currency, and give each ledger row its baseline, negotiated price, actual quantity, paid price, saving and approved class or components with its reason. Keep a lower negotiated target, a unit or currency change, an increase, a rebated amount and an unsupported comparison visible or account for it as the approved disposition says, and count each only as the approved rules say. Account for every invoice line once in a row or once as left out with its reason, or name it in a failed run, and reconcile each claimed saving to baseline, quantity and paid price.

## Verified by

- On a run that completes, each row the approved rules compare carries the amounts its approved class definitions derive from the baseline, quantity, paid amount and other approved references, on a comparable unit and currency within approved rounding, recomputed independently; others carry none.
- A row whose paid price equals the approved baseline shows no realized saving even when the negotiated price is lower; any negotiated-but-unrealized amount appears apart as approved and is never counted as realized.
- A change of pack size, unit or specification creates no saving unless an approved conversion or comparability rule makes the prices comparable; a pair with none is never a saving and is shown as unsupported, set aside with its reason, or named in a failed run, as approved.
- A change of currency alone creates no realized saving; a converted amount states its rate source and date and keeps any currency effect apart from realized saving; without an approved rate the line follows the approved disposition, never converted by a default.
- A paid price above the approved baseline on a comparable unit and currency gives its row no net saving; under an approved split each component keeps its class, and an increase stays visible and reduces a saving or total only where an approved rule nets it.
- Cost avoidance and realized saving stay separate, each shown only where its approved evidence is present; a row's difference from the approved baseline splits as approved and adds back plus any part shown unattributed; an amount against another approved reference sits beside it.
- A rebated amount counts here or in the rebate ledger as approved, never both, and the outcome lists what it leaves to the other; a rebate earned over a wider scope reaches rows only by the approved allocation, which sums back to it plus any part shown unallocated.
- A credit note, or a later change to an invoice line, baseline, agreement, conversion, rate or rebate source, reaches a published period only as approved, restated or as a labelled adjustment, never silently; no change time reads unproven, and a row missing its time follows the approved policy.
- On a run that completes, every input invoice line, credit note included, lands once in a ledger row or is left out with one reason, shown or counted as approved, and the outcome states how many and why; counts and amounts per currency tie to the input; a failed run names each line that stopped it.
- Each approved rule value, such as a baseline basis, tolerance, class definition or rate, changes the output where the data reaches it, within the approved rule form.
- Totals follow the approved cuts and hold only amounts whose class counts toward them; each row and total keeps one currency unless an approved rate converts it, and excluded classes appear beside the totals, not in them.
- Each row traces to the baseline version, agreement, invoice lines, conversion and rate it used; published descriptions state a price difference from the approved baseline, never that procurement caused it, and the outcome states what the inputs cannot prove.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile the baselines (versions, effective dates, approval flags), agreements (terms, negotiated prices, overlaps), invoice lines (dates, quantities, units, currencies, credits, rebate markers, lines with no agreement) and the conversion and rate sources before proposing rules. Use Ask first only for semantics still open, and record each decision as the user's own answer. Work out the expected ledger for the agreed cases independently of the models, from the source lines and the approved rules, before trusting the models, and include cases the inputs may not carry, such as a row mixing rebated and unrebated lines, overlapping agreements or terms, a unit or currency pair with only an unapproved row, and several invoice currencies in one row. Keep the baseline, conversion and rate rules editable as data where the approved requirements say so. Reconcile every ledger saving to its baseline, quantity and paid amount, and tie the line accounting to the input before declaring the work complete.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- verifying

### Ask first

- If unresolved, what sets an approved baseline (last paid, average, list, budget) and what counts as its approval, at what level (supplier and item, or item and specification), how long a saving counts, how versions apply to an invoice date, and what follows when none or several are in force?
- If unresolved, how is each saving class defined (realized, negotiated not realized, cost avoidance and its evidence, currency effect, price increase), which wins when several apply, is a mixed difference split (order, constant rate or price) or assigned whole, and which classes count toward totals?
- If unresolved, which keys link an invoice line to an agreement and item (supplier, item, contract or order reference, specification), which agreement wins when several apply, does a volume cap split a line, and how are lines with no agreement, or outside its term, shown?
- If unresolved, which units, pack sizes and specifications are comparable, which approved conversions apply (per item or general, dated), how is a tiered, indexed or formula price evaluated, is an index-driven change its own class, and what happens to a price that cannot be compared?
- If unresolved, which currency reports, are others converted (rate source and date), kept apart or set aside, is a currency effect its own class or an unattributed part (never realized), does it count toward totals, and is currency part of each row's key?
- If unresolved, is paid price before or after discounts, rebates and fees, how is a rebate earned over a wider scope allocated to rows, which ledger holds a rebated amount so it counts once, and how do credit notes post (own period or the original's), including a price-only one?
- If unresolved, what is one ledger row (month, agreement, item, supplier, currency), which date sets its period, which periods and totals are published, are months with no purchase shown, how are several prices weighted, and what precision and tolerance apply?
- If unresolved, which suppliers, spend types and invoice statuses are in scope, what happens to an unplaceable, incomparable or missing-time line (set aside, excluded or the run fails), and how does a later change to an input reach a published period?

### Guardrails

- Do not choose the baseline, class definitions, effect attribution, linking keys, comparability and price-form rules, currency or rebate treatment, credit-note posting, restatement, grain, weighting, period, population or exceptions for the user or take them from the data.
- Never count a negotiated target, a unit, specification or currency change by itself, or an increase as a realized saving; a rebated amount counts here only where the approved rule assigns it to this ledger, shown apart.
- Never compare prices across units or currencies unless an approved conversion or rate applies and states its source and date; never use a factor or rate of one, or a default, for a missing one.
- Never count a rebated amount in this ledger and in a rebate ledger.
- Never drop, double count or silently net away an invoice line, a credit note or an amount; a line left out stays accounted for with its reason and zero counted saving.
- Never read a missing baseline, agreement or price as zero, or call a row a saving on a baseline the inputs do not show; report what the inputs cannot prove.
- Never claim that procurement caused a price difference.
- Never restate a published period silently when a baseline, agreement, invoice line, conversion, rate or rebate source changes later.
- Stop at the savings ledger: do not build the spend cube, check contract compliance, accrue rebates, set rates or forecast.
