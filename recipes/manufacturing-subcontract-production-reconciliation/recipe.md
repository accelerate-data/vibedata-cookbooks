---
id: manufacturing-subcontract-production-reconciliation
title: Reconcile components held at a subcontractor and processing charges to delivered work, with exceptions and coverage
trigger:
  - Nobody can say how much of the company's material is sitting at a subcontractor, because transfers, returns, scrap reports and finished receipts live in different places and are never netted.
  - A subcontractor's processing invoice is paid or disputed without checking it against what was accepted, so unbilled work, over-billing and price differences go unseen.
  - A subcontractor reports its own consumption or scrap and nobody can compare it with what the approved bill of material allows for the finished parts received.
description: From subcontract orders, approved components, transfers, returns, supplier reports, finished receipts and processing invoices, publish what is held at the subcontractor at the approved cutoff, the charge earned on delivered work with invoice lines matched to it, each supplier report compared with the approved quantity, and every exception.
pitch: Show what sits at the subcontractor, how its reports compare with approved usage, and whether its invoices match delivered work, every input accounted for.
job_category: build
area: transformation
readiness: supported
function:
  - supply-chain-ops
  - finance
industry:
  - manufacturing
domain_objects:
  - subcontract_order
  - supplier
  - bom_line
  - stock_transfer
  - goods_receipt_line
  - supplier_invoice_line
  - credit_note
  - unit_conversion
  - reconciliation_exception
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
  - Needs each order's approved components, quantity per finished unit, any allowance, its price basis and supplier.
  - Needs recorded transfers, returns, supplier reports, receipts with an accepted result, and invoice lines.
  - Covers components still company-owned at the subcontractor; buy-sell or consume-at-transfer is a separate outcome.
  - Supplier-reported figures never stand in for approved quantities unless the approved rule says so.
  - One subcontract process per order; chains of subcontract steps are a separate outcome.
  - One currency per order; translating currencies is upstream work.
  - Valuing components, WIP or COGS is inventory-valuation-cogs; purchased-goods matching is procurement-three-way-match.
  - A source with no recorded time cannot show late changes; restatement then reads unproven.
  - In-house production, standard cost, physical counts, supplier payment and ledger posting are separate outcomes.
  - Inputs are landed tables; loading files or extracts belongs to file-drop-to-bronze.
related:
  - procurement-three-way-match
  - inventory-valuation-cogs
  - ops-inventory-reconciliation
  - effective-dated-bom-requirements
  - file-drop-to-bronze
evidence:
  features:
    - capturing-requirements
    - generating-dbt-model
    - verifying
  evals: []
---

## Prompt

Build <component_ledger>, <processing_charge>, <invoice_line_match>, <report_comparison>, <exception_output> and <coverage_output> from <subcontract_order_source>, <approved_component_source>, <component_transfer_source>, <transfer_reversal_source>, <component_return_source>, <supplier_report_source>, <finished_receipt_source>, <processing_invoice_source>, <credit_note_source> and <unit_conversion_source>. For each approved subcontract order and component at <cutoff>, publish in the component's base unit the quantity transferred, relieved, returned, declared as scrap and still held, by the approved relief and scrap rules. Publish the processing charge earned on finished work by the approved price and earning rules, match each invoice line to delivered work or charges by the approved link so nothing is matched twice, and show unbilled work, quantity billed beyond delivered work, price differences and credit notes. Compare each supplier report with the approved quantity for the parts it reports. Never treat a transfer as a sale or consumption, and show or count each record left out with its reason, as approved. Report what the inputs cannot prove.

## Verified by

- On a completed run, each input record is accounted for once: traced to each ledger line, charge or match it feeds, set aside with one reason, or shown or counted out of scope with its reason, as approved; per-source counts foot to the input, and a repeat follows the approved duplicate rule.
- A transfer to the subcontractor stays company-owned at the supplier, never consumed or sold; per ledger line, net quantity transferred equals relief applied, plus returns applied, plus scrap applied, plus quantity held, and what the approved floor could not apply stays beside it as unapplied.
- Relief follows the approved basis; a rejected receipt relieves components or earns a charge only if the approved rule says so; each supplier report is shown beside the approved quantity for the parts it reports, relieves only where the approved basis uses it, and any difference stays visible.
- Declared scrap is classified against the approved allowance, with the quantity beyond it as its own class; returns and scrap reduce the held quantity as the approved rule applies them, and any quantity the held quantity could not absorb stays visible as unapplied with its reason.
- The held quantity follows the approved floor rule and the unclipped amount stays observable; an order closed with material at the supplier keeps its remaining quantity visible and flagged as approved, and is never written off silently.
- A component off the approved list, a transfer with no approved unit conversion and a transfer to another supplier each stay identifiable, flagged or set aside with a reason, never relieved or turned into a quantity by an assumed factor; an incomplete line is never published as complete.
- The charge earned follows the approved price and earning rules, up to the approved rounding shown where it arises; each invoice line's matched quantity or amount traces to the earned work or charge it was matched to, never exceeds it, and any excess shows as billed beyond it.
- A delivered unit or charge is matched at most once; unbilled work, a line citing a foreign receipt or a rejected one earning nothing, a price beyond any approved tolerance and a credit's effect stay visible as their own amounts or classes, never netted into one total or added to matched totals.
- Movements are placed by the approved date; one the approved date places after the cutoff is counted and excluded, and a later change reaching a reported cutoff follows the approved restatement, adjustment or hold-out rule, never changing published figures silently.
- Each output is unique on its approved grain; orders, components or receipts from different plants are never merged because identifiers match, and amounts in different currencies are never summed.
- Published quantities, charges, matches, exceptions and coverage equal values derived independently from the sources and approved rules, including a partial receipt, scrap beyond the allowance, a return above the held quantity, an invoice line spanning receipts and a credit above the billed amount.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile each input for plant, order, component, supplier, receipt and invoice keys, units of measure, currencies, dates and repeated records before modelling. Write the expected ledger lines, charges, invoice matches, exceptions and coverage by hand from the approved rules and the input data before any model, with a case for each rule at its edge, such as a partial receipt, scrap beyond the allowance, a return after relief, a transfer reversed, an invoice line spanning receipts, a credit note and an order closed with material still at the supplier. Keep each rule the requirements treat as data (allowances, prices, conversion factors, cutoffs, reason codes) as data that the models and tests read, never as a literal. Before declaring the outcome complete, recompute every ledger identity and invoice match independently of the models, check that every input record is accounted for once and that no incomplete line was published as complete; report what the inputs cannot prove.

### Compose

- capturing-requirements
- profiling-source-data
- generating-dbt-model
- verifying

### Ask first

- If unresolved, which plants, suppliers, order types and statuses are in the run, which keys link each record to its order, component and receipt, and what an unknown order or component, another supplier, a supplier-sourced component, a direct delivery or a by-product does?
- If unresolved, which date places a movement, what is excluded after the cutoff, and whether a reported cutoff is frozen, restated or adjusted when a late movement or changed record arrives?
- If unresolved, which quantity relieves (approved per accepted unit, reported consumption or the lower), whether quantities per unit are dated, whether rejected receipts relieve or earn, how the allowance applies, how receipts beyond the order count, and what a supplier report is compared with?
- If unresolved, how declared scrap is treated against the allowance, whether the held quantity may go negative or is floored with the unapplied quantity shown, in what order movements apply within a date, and what a closed order with material at the supplier or an off-list component shows?
- If unresolved, how an invoice line matches delivered work (by cited receipt, order or both), in what order uncited lines are allocated, whether a line may span receipts, how a setup, lot or minimum charge line matches, and what a line citing a rejected or foreign receipt does?
- If unresolved, which price basis the charge uses (per unit, lot, setup or minimum) and whether it is dated, what price difference is tolerated, how a credit note reduces the billed amount, including one above it, and whether a record in another currency is set aside or fails the run?
- If unresolved, what identifies a duplicate, how an exact or conflicting repeat is treated, how a reversed transfer or receipt and finished parts sent back for rework apply to relief, charge and matches, and what a missing recorded time does?
- If unresolved, which unit conversions are approved and whether they are dated, what a missing conversion does, what rounding applies and where, and which cuts of the ledger and invoice outputs are published?

### Guardrails

- Do not choose any Ask first answer for the user, such as population, linking keys, dates, relief basis, rejected receipts, allowance, scrap treatment, floor, closed-order handling, invoice matching, price basis, credit, duplicates or conversions, nor take one from the data or common practice.
- Never show a transfer to the subcontractor as consumed or sold, and never relieve components for rejected parts or for a quantity only the supplier reports unless the approved relief rule says so.
- Never match more invoice quantity or amount than the delivered work or earned charge allows, never match one delivered unit or charge twice, and never match a line to rejected parts unless the approved rule lets them earn.
- Never invent a conversion factor, price or approved component; an incomplete ledger line or an unmatched invoice line is labelled with its reason, never published as complete or costed at zero.
- Never hide an excess, a residual or an unapplied quantity by clamping, netting or writing it off; any such amount stays visible with its reason.
- On a run that completes, never drop or double count a record: every order, transfer, report, receipt, invoice line and credit note stays accounted for, including duplicates, conflicts and set-aside records.
- Do not hold a rule the approved requirements treat as data, such as an allowance, price or factor, as a literal in the models.
- Never sum or compare amounts in different currencies, and never merge orders from different plants because their identifiers match.
- Stop at the quantity ledger and the processing-charge match: do not value components, post to a ledger, pay the supplier or change the source systems, and keep sources read-only.
