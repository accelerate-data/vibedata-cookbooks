---
id: procurement-three-way-match
title: Match purchase orders, receipts and invoices line by line with an exception ledger
trigger:
  - Accounts payable is asked to release payment and cannot say how much of an invoice is covered by the goods actually received.
  - One purchase order line has several receipts and several invoices, and nobody can tell which receipt covers which invoice.
  - Receipts reversed, goods returned, credit notes and different units leave the purchase order, receipt and invoice systems disagreeing, and the differences sit in spreadsheets.
description: For the approved review date, match each purchase order line to its receipts and invoices under the approved quantity, price and unit rules, show what it settles to and what is pending, and keep every source line and every exception visible so nothing is approved beyond the approved rules, lost or counted twice.
pitch: See what each purchase order line settles to against goods received and invoiced, with every exception listed before anyone pays.
job_category: build
area: transformation
readiness: supported
function:
  - finance
  - supply-chain-ops
domain_objects:
  - purchase_order_line
  - goods_receipt_line
  - supplier_invoice_line
  - credit_note
  - three_way_match
  - match_allocation
  - match_exception
  - tolerance_rule
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
  - Produces evidence for review; it does not approve, release or pay anything or write back to a source system.
  - Stops at the match; spend cubes, duplicate invoice detection and recovering overpayments are separate.
  - Receipts and invoices link to a purchase order line by an explicit reference or an approved linking rule.
related:
  - ops-procurement-spend
  - finance-duplicate-invoice-detection
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

Build <po_line_settlement_model>, <invoice_line_disposition_model>, <receipt_line_disposition_model>, <allocation_model> and <exception_ledger_model> from <purchase_order_lines_source>, <goods_receipts_source>, <invoice_lines_source>, <tolerance_rules> and <unit_conversions>. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only the semantics they leave open. For the approved review date, link each receipt and invoice line to its purchase order line as approved, allocate received quantity to invoice lines as approved so no receipt is allocated more than the quantity it carries, and settle each purchase order line to the matched quantity and value, the quantity and value pending receipt or invoice, and the open order quantity, applying the approved tolerances, units, reversals, returns and credit notes. Give every purchase order, receipt and invoice line exactly one disposition, list every exception with its reason and the figures behind it, keep the tolerances and unit conversions as editable data, and report what the inputs cannot prove.

## Verified by

- Every purchase order, receipt and invoice line appears once on its line-level output with one disposition; each population's disposition counts equal its source count, including lines dated after the review date or left out by the approved scope.
- Published matched and pending figures equal values derived independently from the sources and the approved rules, including an order of 10 units at 10 with 6 received and 8 invoiced, which matches and shows pending exactly what the approved basis defines.
- Matched quantity never exceeds what the approved rules allow on any line, and the quantity allocated from a receipt never exceeds what that receipt carries, so no received unit is counted twice.
- Under the approved definitions, matched, pending and open quantities on each purchase order line add up to its ordered quantity, plus any over-receipt or over-invoicing the approved rule shows beside them.
- A receipt or invoice line whose reference is blank, unknown or disagrees with its purchase order line is listed as an exception under the approved rule and is never linked by date, supplier or item unless an approved rule says so.
- Documents after the review date, later receipts, reversed receipts, returns and credit notes change matched quantities as the approved rules say, and a change to an earlier match is shown, not applied silently.
- Quantities and prices exactly on each approved tolerance edge and one step beyond it are classified as approved, and units or currencies without an approved conversion stay unmatched and listed.
- Each exception row names its source line, reason and the quantity and value behind it, and a line with two problems appears under both as approved.
- Changing an approved tolerance, unit conversion or the review date changes the result accordingly without a code change.
- On a run that completes, each output is unique on its declared grain with required fields populated, every figure carries the review date it describes, and no output approves or pays anything.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile the three sources first: how receipts and invoices reference the purchase order line, the units, currencies and dates present, how reversals, returns and credit notes are recorded and what they cite, and whether one document can arrive twice. Use Ask first only for semantics still open, and record each decision as the user's own answer. Keep tolerances, unit conversions and any scope lists as editable data. Compute expected results independently of the models from the same source rows and the approved rules, and test each tolerance edge, a reversal and a return after a match, a credit note that frees received quantity, and a line with several problems at once. Report every exception and what the inputs cannot prove.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which purchase orders, receipts and invoices are in scope (types, statuses, entities, currencies, service or non-order lines), and how are records the scope leaves out shown or counted?
- If unresolved, which reference links a receipt or an invoice line to a purchase order line, and what happens to a blank, unknown or disagreeing reference: an exception, or a linking rule you approve?
- If unresolved, what does a line settle to when quantities differ: the received, invoiced or ordered quantity, at the order price or the invoice price, and what counts as pending?
- If unresolved, how is received quantity allocated when a line has several receipts and several invoices, and in what order?
- If unresolved, what are the price and quantity tolerances (percentage or amount, direction, edges), and how is a receipt or invoice above the ordered quantity treated?
- If unresolved, how are different units and currencies handled: converted by which approved factors or rates, or listed as exceptions?
- If unresolved, how do reversed receipts, returns and credit notes affect a match already made, what do they cite, and is a reduced match an exception?
- If unresolved, which review date applies, how are documents dated after it treated, and what does an exception row carry when one line has several problems?

### Guardrails

- Do not choose the settlement basis, allocation order, tolerances, unit or currency handling, reversal and return treatment or linking rule for the user, and take none from the data, a vendor default or common practice; the user may ask for alternatives or a recommendation.
- Never link a receipt or invoice to a purchase order line by nearest date, supplier or item unless an approved rule says so.
- Never match more than the approved rules allow, allocate more from a receipt than it carries, or silently restate an earlier match.
- Never drop, double count or silently clear a source line; lines the approved scope leaves out stay visible with their reason.
- Never default a missing quantity, price or unit to a value, or convert a unit or currency without an approved factor or rate.
- Do not approve, release, pay or write back to any purchase order, receipt, invoice or payment system; the output is evidence for a reviewer.
- Do not hard-code a tolerance, unit factor or the review date in the models; a change to them must change the result without a code change.
- Stop at the match: do not build the spend cube, detect duplicate invoices or recover overpayments.
