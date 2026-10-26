---
id: procurement-open-commitment-rollforward
title: Build the open purchase commitment balance and a roll-forward that ties every cutoff
trigger:
  - Procurement and finance are asked what is still owed to suppliers on open orders at a month-end, and each answer comes from a different spreadsheet.
  - After a partial receipt, an amendment or a cancel-and-reopen, nobody can say how much of an order line is still committed or why the balance moved.
  - An invoice, a receipt reversal or a return arrives and the open balance is relieved twice or not at all.
description: From purchase order line history, build each line's outstanding quantity and value at each approved reporting cutoff under the approved discharge rule, explain every movement from the previous cutoff, show received-not-invoiced goods as approved, and keep every record that moves nothing visible with its reason.
pitch: See what is still committed on every open purchase order line at each cutoff, with a roll-forward that ties and every exception kept.
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
  - Needs dated purchase order line history with amendments, receipts, cancellations and invoices that cite a line.
  - Past cutoffs reproduce from event dates; restating them for late-loaded documents needs a recorded load time.
  - Keeps currencies and units apart unless an approved conversion applies.
  - Stops at the commitment balance; matching receipts to invoices and spend analysis are separate outcomes.
  - Produces evidence; it does not forecast cash, post accruals, approve anything or write back to a source system.
related:
  - procurement-three-way-match
  - ops-procurement-spend
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

Build <commitment_balance_model>, <commitment_rollforward_model> and <commitment_exception_model> from <purchase_order_line_history_source>, <goods_receipt_source>, <receipt_adjustment_source>, <invoice_source>, <reporting_cutoffs> and, where approved, <unit_conversions> and <currency_rates>. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only the semantics they leave open. For each approved reporting cutoff, give each in-scope purchase order line its outstanding quantity and value under the approved order, amendment, cancellation, discharge and valuation rules, show received-not-invoiced goods as approved, and explain each cutoff's change from the previous one through the approved movement classes so that opening plus each movement equals closing in quantity and value, with any approved remainder shown. Publish the approved totals, which foot to the line rows. Give every source record one disposition, applied or an exception with its reason, quantity and value, and report what the inputs cannot prove. Keep sources read-only.

## Verified by

- On a run that completes, each in-scope line appears once per approved cutoff under the approved population rule, unique on line, cutoff and any approved currency or unit, and never for a cutoff the approved list lacks.
- Outstanding quantity and value equal values derived independently from the sources and approved rules at each cutoff; a partial receipt relieves only its own portion, and quantity no approved rule relieves stays outstanding.
- A document the approved discharge rule does not count never moves the commitment, and a later document never relieves again a portion already relieved; the outcome is the same whichever of the documents arrives first, as the approved rule says.
- On a run that completes, each line interval and each total holds opening plus every approved movement class equal to closing, in quantity and value, up to any approved rounding shown beside it; each opening is the prior closing and the last closing equals the balance.
- An amendment, cancellation or reopening takes effect from its own date; an earlier reported cutoff changes only as the approved restatement rule says, and the change then appears as its own labelled movement.
- A cancel-and-reopen sequence, and a receipt, reversal, return or invoice dated inside a cancelled period, follow the approved rules; a quantity the approved rules do not apply is an exception, never netted silently.
- Receipt reversals, returns and over-receipt follow the approved treatment; a balance below zero is never shown unless approved, and the unclipped amount stays observable beside any floor.
- Received-not-invoiced and invoiced-ahead-of-receipt quantity and value follow the approved representation and are never counted both inside the commitment and beside it unless approved.
- Every source record is applied, set aside as an exception, or shown or counted as outside the approved scope with its reason; counts reconcile per record type, and a record is never linked to a line by date, supplier or item unless an approved rule says so.
- Each exception names its source record, reason, cutoff, quantity and value; a repeated or persisting condition appears at each cutoff the approved rule says, with no duplicate of the same record, reason and cutoff.
- Currencies and units are never netted unless an approved conversion applies; each approved total foots to its line rows within one currency and unit, and a record at an approved cutoff boundary or after the last cutoff follows the approved date basis.
- Where the roll-forward cannot close under the approved rules, the run fails naming each line and cutoff or publishes flagged with the gap, never passed; the outcome states what the inputs cannot prove, and nothing is approved, accrued, forecast or written back.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile the order history, receipts, adjustments and invoices first: how each cites a line, which dates and units are present, how amendments, cancellations and reopenings are recorded, and whether a document can arrive twice. Use Ask first only for semantics still open, and record each decision as the user's own answer. Keep cutoffs, conversions and reason lists as editable data where the approved requirements say so. Work out expected balances and bridges independently of the models, from the source records and the approved rules, before trusting them, including cases the inputs do not carry such as an over-receipt, a sub-cent product or an event on a cutoff, and check that every interval and total closes. Say which paths the inputs did not exercise.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which purchase order lines and documents are in scope (types, statuses, entities, blanket, service, non-receipted or test lines), from which cutoff does a line first appear, and are excluded records shown or only counted?
- If unresolved, which key links a receipt, adjustment or invoice to its line, and what happens to a blank, unknown or disagreeing one, or to a document that arrives twice?
- If unresolved, which event discharges a commitment (receipt, invoice, the earlier, or by line type), what a document of the other kind does to a portion already relieved, and what an invoice ahead of receipt does?
- If unresolved, how are received-not-invoiced goods shown (inside the commitment, as their own balance or as an accrual candidate), and may that figure be negative or floored?
- If unresolved, which quantity and price count (as placed, as amended) from which date, does a price amendment revalue the open quantity, how does a later change to a valued line reach published cutoffs (restate or labelled movement), and which movement classes show each effect?
- If unresolved, what does a cancellation or closure relieve, what does a reopening reinstate, how are documents dated inside a cancelled period treated, and may earlier reported cutoffs ever change?
- If unresolved, how do a receipt reversal, a return and a credit note affect a relieved portion (reinstate, memo only or exception), and how is a receipt above the open quantity treated (capped, flagged or negative)?
- If unresolved, which cutoffs and date basis apply, which unit and currency are the basis and how others convert, which totals and cuts are published, what precision and rounding apply, and does a roll-forward that cannot close fail or publish flagged?

### Guardrails

- Do not choose the discharge rule, received-not-invoiced representation, valuation, cancellation and reopening treatment, reversal and return effect, linking key, cutoff basis or conversion for the user, or take them from the data or an ERP default; the user may ask for options.
- Never relieve a commitment twice for one quantity, or by a document the approved discharge rule does not count.
- Never restate a reported earlier cutoff silently; a change reaches earlier figures only as the approved rule says, as its own labelled movement.
- Never absorb a gap in an unlabelled line or an unapproved class so a roll-forward closes; any remainder is shown where the approved rule puts it.
- Never drop, double count or silently clear a source record, link one to a line by nearest date, supplier or item, or read a missing quantity, price or date as a value unless an approved rule says so.
- Never net two currencies or units into one figure, or convert without an approved factor or rate.
- Stop at the commitment balance: do not match receipts to invoices, build a spend cube, forecast cash, post accruals, approve or pay, or write back to any source system.
