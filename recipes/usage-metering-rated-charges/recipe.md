---
id: usage-metering-rated-charges
title: Calculate rated usage charges with pooled allowances, tiers, credits and restated corrections
trigger:
  - Usage charges differ by who calculated them, because graduated and volume pricing, shared allowances and credits are applied differently from one run to the next.
  - A redelivered event spends a shared allowance twice, or a late, revised or cancelled event forces a rerun of every customer.
  - Billing or finance needs each customer's charge per period and meter with every usage event rated or set aside, and a change to an earlier period shown as a restatement.
description: Turn deduplicated usage events and approved contract terms into charge lines per customer, period and meter with allowance, tier method and credits applied, every event accounted for, and corrections restated for only the affected scope.
pitch: Rate usage under pooled allowances, tiers and credits so every event is accounted for and a correction restates only what it touches.
job_category: build
area: transformation
readiness: supported
function:
  - finance
  - revops
domain_objects:
  - usage_event
  - contract_terms
  - billing_period
  - allowance
  - tier_schedule
  - prepaid_credit
  - rated_charge_line
  - event_disposition
  - charge_restatement
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
  - Usage events must already be landed as tables; ingesting them is a separate outcome.
  - Needs approved terms per customer and meter; they may be captured as editable data during the run.
  - Keeps each currency separate; conversion is a separate outcome.
  - Restating earlier results needs the figures as last reported to be kept between runs.
  - Stops at rated charge lines; invoices, payments, tax and revenue recognition are separate outcomes.
  - A flat dated rate with no period-wide allowance or tiers belongs to effective-dated-business-rules.
related:
  - effective-dated-business-rules
  - saas-mrr-waterfall-nrr
  - telecom-cdr-usage
  - utilities-meter-to-bill
  - revops-bookings-billings-cash
  - finance-revenue-recognition
evidence:
  features:
    - capturing-requirements
    - profiling-source-data
    - generating-dbt-model
    - dbt-unit-testing
    - running-dbt-in-sandbox
    - verifying
  evals: []
---

## Prompt

Build <charge_line_model>, <tier_model>, <event_account_model>, <credit_account_model> and <restatement_model> from <usage_event_source>, <contract_terms_source> and any <credit_source>. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and settle with the user only the rating semantics they leave open. Rate each usable event into the approved billing period, apply the approved allowance, price the remaining units by the approved tier method, apply credits as approved, and publish a charge line per customer, period and meter with rated units, allowance used, billable units, tier charge, credit applied and charge due. Give every delivered event one disposition, rated or set aside with its reason, so the counts add back to the events delivered, never let a repeated event use an allowance twice, recompute only what the approved scope says a correction touches and show its change against what was reported before, leave a rerun with no new input unchanged, and report what the inputs cannot prove.

## Verified by

- Every delivered event has one disposition, rated or set aside with its reason; rated plus set-aside quantities equal the delivered quantity of events with a readable quantity, any other event is named, set-aside events add no units, and the outcome states how many were set aside and why.
- Each charge line equals values derived independently from the events and the approved terms by hand or a separate calculation, never by rerunning the models, and one line exists for each key the approved rule publishes.
- Pricing follows the approved method: graduated prices only the units inside each tier and volume prices all units at the tier the total reaches, so one schedule gives different charges, for example bands 0 to 100 at 1 and above at 0.5 give 110 for 120 units graduated and 60 volume.
- A repeated event never consumes an allowance twice: units rated and allowance used equal those of a single delivery, and the repeat is accounted for as the approved rule says.
- Allowance used never exceeds the allowance or the units rated, billable units equal rated units less allowance used, and allowance is shared and consumed as approved, never across a scope the approved rule keeps apart.
- Tier rows sum exactly to the line's tier charge with no residue, a unit on a tier boundary is priced once, and amounts are rounded at the approved point and mode.
- Credit applied never exceeds the credit available or the charge it offsets, charge due is never negative, applied credit across a period's lines equals what the approved rule applies, and unused credit is reported including where a period has no events.
- Events on either side of the approved period boundary fall in different periods, and a change of terms follows the approved rule; an event with no usable term or a schedule the rule cannot price is set aside with its reason, never rated as zero.
- A late, revised or cancelled event changes only the customer and period the approved scope names; every other published figure is identical before and after.
- A restatement row shows previous value, new value, difference and cause for each changed measure, omits unchanged measures, and a rerun with no new input changes no figure and publishes no restatement.
- The outcome states what the inputs cannot prove, such as events not yet delivered, terms the data does not carry, or an earlier report that was not kept.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every decision its approved requirements already record; do not ask the user to confirm them again. Profile the events (identifier, version, status, customer, subscription, meter, quantity, timestamp, delivery order) and the terms (effective date, allowance, tier bands, method, credits), and check that each event can reach a term. Use Ask first only for semantics still open, and record each answer as the user's own. Keep bands, prices, allowances, method, credits and disposition reasons as editable data, never literals in the models. Derive each case's expected result independently of the models, from the events and the terms, before comparing: usage below, at and above an allowance, subscriptions sharing one allowance, two meters of one customer, graduated and volume over the same bands, a boundary quantity, a repeated delivery, a conflicting delivery, a revision, a cancellation, events either side of a period boundary, a term change, a credit larger than the charge, a credit in a period without events, and a correction in one period beside untouched ones. Keep the figures as last reported before applying a correction, so the restatement compares against what was reported rather than a rebuilt state, and leave that state unchanged when a run fails. State what the inputs cannot prove.

### Compose

- capturing-requirements
- profiling-source-data
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, how are an event's identity, version, cancellation, repeated delivery and conflicting delivery recognised, and which events are in scope or set aside (test, internal, zero or negative quantity, unknown meter)?
- If unresolved, how is a billing period defined (calendar or contract anchored, which time zone), which terms version prices it (at period start, per event or split), and which keys link an event to its customer, subscription, meter and terms?
- If unresolved, what scope does an allowance have (per meter or shared across meters, per subscription or customer), in what order is it consumed, and does any unused part roll over?
- If unresolved, is each schedule graduated or volume, are tiers applied per meter or across a customer, on units before or after the allowance, and how are boundaries and a schedule with gaps treated?
- If unresolved, what is a credit's scope, when it applies relative to the charge, how it is split across lines, and what happens to an unused or excess part (expires, carries forward, refunded)?
- If unresolved, which currencies appear, where amounts are rounded, and by which mode?
- If unresolved, what counts as a correction, how far recompute reaches where allowances or credits are shared across periods or lines, and what a restatement shows and attributes?
- If unresolved, which customer, period and meter combinations publish a line (any delivered event, only positive usage, or every active contract), and how is a key with only set-aside events shown?

### Guardrails

- Do not choose the period, terms version, allowance scope, consumption order, tier method, tier basis, credit rules, rounding or restatement scope for the user, and take none from sample data, a vendor default or common practice.
- Never mix pricing methods: a schedule is priced by the approved method only, and a swap of method must visibly change the result.
- Never let a repeated delivery rate or use an allowance twice; a conflict the approved rule cannot resolve is named, not guessed.
- Never rate an event with no usable term as zero, and never drop or double count an event; every set-aside event stays visible with its reason.
- Never sum or blend currencies, and never let credit make a charge negative or apply more than the credit available.
- Never change a published figure outside the approved correction scope, and never restate one silently.
- Never write back to the source systems or alter published models outside the approved outcome.
- Stop at rated charge lines: do not issue invoices, collect payment, calculate tax, recognise revenue or build recurring-revenue movements.
