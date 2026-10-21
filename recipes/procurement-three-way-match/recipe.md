---
id: procurement-three-way-match
title: Match purchase orders, receipts and invoices line by line with an exception ledger
trigger:
  - Accounts payable is asked to release payment and cannot say how much of an invoice is covered by the goods actually received.
  - One purchase order line has several receipts and several invoices, and nobody can tell which receipt covers which invoice.
  - Receipts reversed, goods returned, credit notes and different units leave the purchase order, receipt and invoice systems disagreeing, and the differences sit in spreadsheets.
description: For the approved review date, match each purchase order line to its receipts and invoices under the approved quantity, price and unit rules, show what it settles to and what is pending, and keep every source line and every exception visible so nothing is matched beyond what the approved rules allow, lost or counted twice.
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
  - Quantities and prices are compared in the purchase order line's unit and currency under approved conversions.
  - Produces evidence for review; it does not approve, release or pay anything or write back to a source system.
  - Stops at the match; spend cubes, duplicate invoice detection and recovering overpayments are separate.
  - Receipts and invoices link to a purchase order line by an explicit reference or an approved linking rule.
related:
  - ops-procurement-spend
  - finance-duplicate-invoice-detection
  - finance-ap-aging
  - effective-dated-business-rules
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

Build <po_line_settlement_model>, <invoice_line_disposition_model>, <receipt_line_disposition_model>, <allocation_model> and <exception_ledger_model> from <purchase_order_lines_source>, <goods_receipts_source>, <invoice_lines_source>, <tolerance_rules>, <unit_conversions> and, where approved, <currency_rates>. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only the semantics they leave open. For the approved review date, link each receipt and invoice line to its purchase order line as approved, allocate received quantity to invoice lines as approved so no receipt is allocated more than the quantity it carries, and settle each purchase order line to the matched quantity and value, the quantity and value pending receipt or invoice, and the open order quantity, applying the approved tolerances, units, reversals, returns and credit notes. Give every purchase order, receipt and invoice line exactly one disposition, list every exception with its reason and the figures behind it, keep the tolerances, unit conversions and any approved currency rates as editable data, and report what the inputs cannot prove.

## Verified by

- Every in-scope purchase order, receipt and invoice line appears once on its line-level output with one disposition, including lines dated after the review date; each population's disposition counts equal its source count.
- Lines the approved scope leaves out and repeated copies of a document line are shown or counted with their reason as approved, the outcome states how many and why, and a repeated line is never counted twice unless approved.
- Published matched and pending figures equal values derived independently from the sources and the approved rules, and nothing is shown as matched that the approved basis does not allow.
- Matched quantity never exceeds what the approved rules allow on any line, and the quantity allocated from a receipt never exceeds what that receipt carries, so no received unit is counted twice.
- Under the approved definitions, matched, pending and open quantities on each purchase order line add up to its ordered quantity, plus any over-receipt or over-invoicing the approved rule shows beside them.
- A receipt, invoice, reversal, return or credit-note line whose reference to its purchase order line or original document is blank, unknown or disagrees is an exception under the approved rule, never linked by date, supplier or item unless approved.
- Documents after the review date, later receipts, reversed receipts, returns and credit notes change matched quantities as the approved rules say, and a change to an earlier match is shown, not applied silently.
- Quantities and prices exactly on each approved tolerance edge and one step beyond it are classified as the approved tolerance defines, and units or currencies without an approved conversion stay unmatched and listed.
- Each exception row names its source line, reason and the quantity and value behind it, and a line with two problems appears under both as approved.
- Changing an approved tolerance, unit conversion or the review date changes the result accordingly without a code change, within the approved rule form.
- On a run that completes, each output is unique on its declared grain with required fields populated, every figure carries the review date it describes, the outcome states what the inputs cannot prove, and no output approves or pays anything.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile the three sources first: how receipts and invoices reference the purchase order line, the units, currencies and dates present, how reversals, returns and credit notes are recorded and what they cite, and whether one document can arrive twice. Use Ask first only for semantics still open, and record each decision as the user's own answer. Keep tolerances, unit conversions and any scope lists as editable data. Compute expected results independently of the models from the same source rows and the approved rules, and test each tolerance edge, a reversal and a return after a match, each credit-note and return effect the approved rule defines, and a line with several problems at once. Report every exception and what the inputs cannot prove.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which purchase orders, receipts and invoices are in scope (types, statuses, entities, currencies, service or non-stock lines, blanket call-offs), which lines expect no receipt and how they settle, and are left-out records shown or only counted?
- If unresolved, which reference links a receipt or invoice line to its purchase order line (within an entity), what happens to a blank, unknown or disagreeing one, what identifies one document line sent twice and how it is treated, and what an exception row carries when a line has several problems?
- If unresolved, which ordered quantity and price count (as placed, as amended, net of cancellation or closure), what does a line settle to (received, invoiced or ordered quantity, at the order or invoice price), and what counts as pending?
- If unresolved, how is received quantity allocated when a line has several receipts and several invoices, and in what order?
- If unresolved, what are the price and quantity tolerances (percentage or amount, direction, edges), which price is compared (net or gross of tax, discount and freight), how are tax, freight and discount lines shown, and how is a receipt or invoice above the ordered quantity treated?
- If unresolved, how are different units and currencies handled (factor direction and scope, rate date, or an exception), and what quantity and money precision and rounding apply before tolerance and matching?
- If unresolved, how do reversed receipts, returns and credit notes affect a match already made, what original document do they cite, does a credit free received quantity, and is a reduced match an exception?
- If unresolved, which review date applies, which date on each document decides (document, posting or entry), at what cutoff time and zone, and how are documents after it treated?

### Guardrails

- Do not choose the settlement basis, allocation order, tolerances, unit or currency handling, reversal and return treatment or linking rule for the user, and take none from the data, a vendor default or common practice; the user may ask for alternatives or a recommendation.
- Never link a receipt or invoice to a purchase order line by nearest date, supplier or item unless an approved rule says so.
- Never match more than the approved rules allow, allocate more from a receipt than it carries, or silently restate an earlier match.
- Never drop, double count or silently clear a source line; lines the approved scope leaves out are shown or counted with their reason as approved, and a repeated document line is never counted twice unless approved.
- Never default a missing quantity, price or unit to a value, or convert a unit or currency without an approved factor or rate.
- Do not approve, release, pay or write back to any purchase order, receipt, invoice or payment system; the output is evidence for a reviewer.
- Do not hard-code a tolerance, unit factor or the review date in the models; a change to them must change the result without a code change, within the approved rule form.
- Stop at the match: do not build the spend cube, detect duplicate invoices or recover overpayments.
