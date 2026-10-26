---
id: procurement-open-commitment-rollforward
title: Build the open purchase commitment balance and a roll-forward that explains every cutoff
trigger:
  - Procurement and finance are asked what is still owed to suppliers on open orders at a month-end, and each answer comes from a different spreadsheet.
  - After a partial receipt, an amendment or a cancel-and-reopen, nobody can say how much of an order line is still committed or why the balance moved.
  - An invoice, a receipt reversal or a return arrives and the open balance is relieved twice or not at all.
description: From purchase order line history, build each line's outstanding quantity and value at each approved reporting cutoff under the approved discharge rule, explain every movement from the previous cutoff, show received-not-invoiced goods as approved, and account for every record that moves nothing, shown or counted with its reason as approved.
pitch: See what is still committed on every open purchase order line at each cutoff, with a roll-forward that ties or shows its gap and every exception kept.
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
  - open_commitment
  - commitment_roll_forward
  - commitment_exception
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
  - Needs dated line history with receipts, cancellations and invoices linked to a line by an approved key; else unproven.
  - Holding reported cutoffs or detecting late changes needs a recorded load time; without one it is unproven.
  - Keeps currencies and units apart unless an approved conversion applies.
  - Stops at the commitment balance; matching receipts to invoices and spend analysis are separate outcomes.
  - Received-not-invoiced is per line; allocating receipts to invoice lines belongs to procurement-three-way-match.
  - Produces evidence; it does not forecast cash, post accruals, approve anything or write back to a source system.
related:
  - procurement-three-way-match
  - ops-procurement-spend
  - bitemporal-business-history
  - effective-dated-business-rules
  - shared-fx-conversion
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

Build <commitment_balance_model>, <commitment_rollforward_model> and <commitment_exception_model> from <purchase_order_line_history_source>, <goods_receipt_source>, <receipt_adjustment_source>, <invoice_source>, <reporting_cutoffs> and, where available, <opening_balances>, <recorded_load_time>, <unit_conversions> and <currency_rates>. Inherit the semantics the Intent already establishes and resolve with the user only what it leaves open. For each approved reporting cutoff, give each in-scope purchase order line its outstanding quantity and value under the approved discharge, amendment, cancellation and valuation rules, show received-not-invoiced goods as approved, and explain each cutoff's change through the approved movement classes so that, where it closes, opening plus each movement equals closing in quantity and value with any approved remainder shown. Publish approved totals that foot to the line rows. Account for every source record: applied, set aside as an exception with its reason, or outside the approved scope; a record split across these, such as a capped over-receipt, is traced to each part. Report what the inputs cannot prove.

## Verified by

- On a run that completes, each in-scope line appears once per approved cutoff under the approved population rule, unique on line, cutoff and any approved currency or unit, and never for a cutoff the approved list lacks.
- Outstanding quantity and value equal values derived independently from the sources and approved rules at each cutoff; a partial discharging document relieves only its own portion under the approved rule, and quantity no approved rule relieves stays outstanding.
- A document the approved discharge rule does not count never moves the commitment, and a later document never relieves again a portion already relieved; once both documents are in, the relieved quantity is the same whichever arrived first, as the approved rule says.
- On a run that completes, each line interval and total holds opening plus every approved movement class equal to closing, in quantity and value, up to approved rounding shown; each opening is the prior closing or the approved opening; a flagged interval shows its gap and reads not closed.
- A change takes effect on its approved date. Where the approved rule restates, earlier cutoffs reproduce from the approved date basis and show what changed where a load time or prior figures exist; otherwise it enters the next cutoff as a labelled movement. Without a recorded time it is unproven.
- A cancel-and-reopen sequence, and a receipt, reversal, return or invoice dated inside a cancelled period, follow the approved rules; a quantity the approved rules do not apply is an exception, never netted silently.
- Receipt reversals, returns and over-receipt follow the approved treatment; a balance below zero is never shown unless approved, and the unclipped amount stays observable beside any floor.
- Received-not-invoiced and invoiced-ahead-of-receipt quantity and value follow the approved representation and are never counted both inside the commitment and beside it unless approved.
- Every source record is applied, set aside as an exception, or shown or counted as outside the approved scope with its reason, and the outcome states how many and why; counts reconcile per record type, and no record is linked to a line by date, supplier or item unless an approved rule says so.
- Each exception names its source record, reason, cutoff, quantity and value; a repeated or persisting condition appears at each cutoff the approved rule says, with no duplicate of the same record, reason and cutoff.
- Currencies and units are never netted unless an approved conversion applies; each approved total foots to its line rows within one currency and unit, and a record at an approved cutoff boundary or after the last cutoff follows the approved date basis.
- Where the roll-forward cannot close under the approved rules, the run fails naming each line and cutoff or publishes flagged with the gap, never passed; the outcome states what the inputs cannot prove, and nothing is approved, accrued, forecast or written back.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile the order history, receipts, adjustments and invoices first: how each cites a line, which dates and units are present, how amendments, cancellations and reopenings are recorded, and whether a document can arrive twice. Use Ask first only for semantics still open, and record each decision as the user's own answer. Keep cutoffs, conversions and reason lists as editable data where the approved requirements say so. Work out expected balances and bridges independently of the models, from the source records and the approved rules, before trusting them, including branches the inputs do not exercise, and check that every interval and total closes. Say which paths the inputs did not exercise.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which lines and documents are in scope (types, statuses, entities, blanket, service, non-receipted or test lines), at what grain a commitment is held, when a line first appears and stops appearing, what opening stands for earlier history, and are excluded records shown or counted?
- If unresolved, which key links a receipt, adjustment or invoice to its line, what happens to a blank, unknown, disagreeing or missing key, quantity, price or date, and what a document that arrives twice does?
- If unresolved, which event discharges a commitment (receipt, invoice, the earlier, or by line type), what a document of the other kind or one arriving first does, and how received-not-invoiced goods are shown (inside, own balance or accrual candidate) and whether negative or floored?
- If unresolved, at which price are a commitment and each relief valued (order, as amended, invoice), net or gross of tax, discount, freight and charge lines, does an amendment pending approval count, and does a price amendment revalue the open quantity?
- If unresolved, how does a late or changed record reach published cutoffs (restate, labelled movement or only what remains), which movement classes show each effect, and does a persisting exception repeat at each cutoff or appear once?
- If unresolved, what does a cancellation or closure relieve, do tolerances or a delivery-complete flag close a remainder, what does a reopening reinstate, how are documents dated inside a cancelled period treated, and may earlier reported cutoffs change?
- If unresolved, how do a receipt reversal, a return and a credit note affect a relieved portion (reinstate, memo only or exception), and how is a receipt above the open quantity treated (capped, flagged or negative)?
- If unresolved, which cutoffs, date basis, time and zone apply, which unit and currency are the basis, how others convert (rate date, translation as its own movement), which totals are published, what rounding applies, and does an unclosable roll-forward fail or publish flagged?

### Guardrails

- Do not choose the discharge rule, received-not-invoiced representation, valuation basis, tolerances, cancellation and reopening treatment, reversal and return effect, linking key, cutoff basis or conversion for the user, or take them from the data or an ERP default; the user may ask for options.
- Never relieve a commitment twice for one quantity, or by a document the approved discharge rule does not count.
- Never change a reported earlier cutoff except as the approved restatement rule says, and never silently; a change the rule does not restate enters as its own labelled movement.
- Never absorb a gap in an unlabelled line or an unapproved class so a roll-forward closes; any remainder is shown where the approved rule puts it.
- Never drop, double count or silently clear a source record, link one to a line by nearest date, supplier or item, or read a missing quantity, price or date as a value unless an approved rule says so.
- Never net two currencies or units into one figure, or convert without an approved factor or rate.
- Stop at the commitment balance: do not match receipts to invoices, build a spend cube, forecast cash, post accruals, approve or pay, or write back to any source system.
