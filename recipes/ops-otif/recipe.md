---
id: ops-otif
title: Measure on-time-in-full delivery by customer, carrier and plant
trigger:
  - Customers report late deliveries, and Sales, Supply Chain and the carriers each quote a different on-time-in-full figure because each applies its own promise date, tolerance and partial-shipment rule.
  - A late or short order cannot be traced to a plant, a carrier or a customer change, so each side blames another.
  - A shipment is split across days, carriers or plants, or the customer moved the promise date, and no report says whether the line counted as on time, in full or neither.
  - Cancelled lines, lines not yet due, undelivered lines and shipments matching no order line fall out of the delivery figure with no stated reason.
description: For each approved as-of date, judge every in-scope order line on time, in full and both under the user's approved promise, tolerance and partial-shipment rules, give each miss one reason, roll the verdicts up by order, customer, carrier and plant from the lines, and keep every excluded record visible with its reason.
pitch: One delivery figure per order line, order, customer, carrier and plant, with a reason for every miss and nothing dropped.
job_category: build
area: transformation
readiness: supported
function:
  - supply-chain-ops
domain_objects:
  - order_line
  - order
  - promise_change
  - shipment_leg
  - delivery_verdict
  - miss_reason
  - customer
  - carrier
  - plant
  - delivery_exception
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
  - Needs order lines (promise date, quantity) and shipment legs (dates, quantities, plus plant and carrier for the cuts).
  - Stops at delivery verdicts and cuts; freight cost, carrier contracts, forecasting and inventory are separate outcomes.
  - A past as-of date reproduces only from kept promise and cancellation history; a rebuild restates it.
  - Order and shipment tables already in the Domain; exported files go to file-drop-to-bronze first.
related:
  - logistics-fleet-utilization
  - service-ticket-sla
  - metric-population-and-rollups
  - effective-dated-business-rules
evidence:
  features:
    - capturing-requirements
    - generating-dbt-model
    - verifying
  evals: []
---

## Prompt

Build <line_model>, <leg_model>, <order_model>, <cut_models>, <worklist_model> and <coverage_model> from <order_source> and <shipment_source>. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only the semantics they leave open. For each approved as-of date, judge every in-scope order line on time, in full and both against the approved promise date, tolerances and partial-shipment rule, give each miss exactly one reason under the approved precedence, roll the verdicts up by order, customer, carrier and plant from the lines under the approved attribution, and list every cancelled, not yet due, undelivered or unmatched record with its reason. Keep sources read-only and report what the inputs cannot prove.

## Verified by

- On a run that completes, each in-scope order line at each published as-of date shows its promise, promised and delivered quantity and date (none if undelivered), separate on-time and in-full verdicts, a combined verdict true exactly when both are, and for a miss exactly one approved reason.
- Deliveries on the promise date, one day beyond it and just outside any approved early limit, and quantities at, below and above the approved in-full limits, are judged as approved, with each approved tolerance applied once and read as stated.
- A line delivered in parts follows the approved partial-shipment rule: its counted legs sum to the delivered quantity in one approved unit, legs excluded or unconvertible are listed, the arrival date used is the one the rule names, and a line that never completes is judged as the rule says.
- A moved promise follows the approved governing-promise rule: where the source keeps promise history the original and the moves stay visible, a change recorded after the as-of date applies to it only under an approved restatement rule, and without history restatement is stated as unproven.
- A delivery date on a weekend or holiday, and any time-zone or cut-off difference, is handled as the approved calendar rule says, and the recorded date stays visible beside any date used for the test.
- The on-time and in-full verdicts stay separate flags, so one reason never hides a failed dimension, and the reason is chosen by the approved precedence when several apply.
- A leg's events after the as-of date do not count for it; goods in transit at the as-of date are judged as approved, and a party is blamed only as the approved attribution allows.
- Order, customer, carrier and plant figures, and any other approved roll-up, are recomputed from the lines, never as an average of rates, and an order is judged by the approved order rule.
- Carrier and plant cuts follow the approved split-line rule and state it; a cut whose parties overlap says so, no cut total is shown as the overall figure, and lines placed in no cut member are counted and shown.
- Cancelled, not yet due, past-due undelivered and unmatched-shipment records are each listed with their reason and handled as approved; none is silently dropped or defaulted to on time.
- At each published as-of date every order line and shipment leg is in exactly one place: in the figure, out with a reason, matched, an exception, or not yet occurred; counts in equal counts out. A failed run names the offending records.
- Expected results for each stated behaviour are derived from the source records and approved rules by a calculation separate from the implementation, every output is unique on its declared grain, and the outcome states what the inputs cannot prove.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile the order lines, promise history, shipment legs and working calendar: keys, grains, quantity units, dates, time zones, and which links the sources really carry. Use Ask first only for semantics still open, and record each answer as the user's own decision. Keep tolerances, reasons and their precedence, attribution lists, the working calendar, planned dates and as-of dates as editable data where the approved requirements say so. Make the line, leg, order, cut, worklist and coverage outputs agree about every record. Prove each stated behaviour on the source records, including the boundary and exceptional cases, with expected results derived independently of the models. Report every miss, exclusion and unmatched record left open, and what the inputs cannot prove.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which order lines are in scope (cancelled, test, zero quantity, returns, drop-ship, customer- or carrier-collected), which as-of dates run, which roll-ups beyond the four cuts, which customer (sold-to, ship-to, parent), and is the figure lines, units or value in one approved unit?
- If unresolved, which promise governs (requested, confirmed, in force at the as-of date, latest ever), is it a date, window or time, who moved it (customer or seller), may a move excuse a miss, and which quantity is promised (ordered, amended, net of cancellation)?
- If unresolved, which event is judged (pickup, dispatch, delivery, proof of delivery), which legs are the customer delivery (final leg versus transfers, cross-dock), how shipments link to lines, which calendar, time zone and cut-off apply, and are refused, damaged or returned goods delivered?
- If unresolved, what makes a line on time and in full (late grace, early limit, short and surplus tolerance in units or percent, rounding, variation by customer, product or lane), how is a line delivered in parts judged, and in which unit are quantities compared?
- If unresolved, how is an order judged from its lines, and how are cancelled, partly cancelled, not yet due and past-due undelivered lines treated: out of the rate with a reason, counted as a miss, or on time when already complete?
- If unresolved, which miss reasons exist, which wins when several apply, which belong to the plant, the carrier, the customer or nobody, and what evidence (planned dispatch dates, committed transit times, multi-leg or carrier changes) attributes a miss?
- If unresolved, how is a line split across carriers or plants counted in the carrier and plant cuts, and how is a line with no shipment placed in them?
- If unresolved, how are shipments with no order line, duplicates, missing dates or quantities and unconvertible units treated, and does an exception or an unplaceable record fail the run or stay visible?

### Guardrails

- Do not choose the promise basis, tolerances, partial-shipment rule, reason precedence, attribution or population for the user, and take none from the data or common practice; the user may ask for alternatives or a recommendation.
- Never average rates across lines, orders or parties; recompute every figure from the lines.
- Never present an overlapping carrier or plant cut total as the overall figure, and never blame a party for a miss the data cannot attribute to it.
- Never drop, double count or default an unplaceable record; a missing date or quantity is not zero or on time unless the approved semantics define it so.
- Never let one reason hide a failed on-time or in-full dimension.
- Never apply a later promise change, delivery or cancellation to an earlier as-of date unless an approved restatement rule says so.
- Stop at the delivery verdicts and cuts: do not compute freight cost or carrier penalties, forecast, plan inventory or change source orders and shipments, and keep sources read-only.
