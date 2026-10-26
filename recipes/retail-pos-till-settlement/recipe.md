---
id: retail-pos-till-settlement
title: Settle store till sessions to counted cash, tender mix and deposit slips with an explicit over or short
trigger:
  - Stores count each till at shift close and Finance cannot tell which shortages are real and which come from how the POS records voids, refunds, change and float moves.
  - A split-tender sale, a voided sale or a float transfer between tills is counted as revenue or cash twice, or not at all, and the till never reconciles.
  - A store deposit differs from what the tills dropped and nobody can say whether cash is missing or simply not yet banked.
description: For approved store till sessions, reconcile POS sales, refunds and voids, tender lines and cash movements to the counted close, publish each session's expected cash, tender mix and over or short in the approved sign, and compare each store day's expected deposit with its slips, with every record placed, listed or counted with its reason.
pitch: One row per till session shows expected cash, the count and the difference, with tenders apart and every deposit gap shown as in transit or a variance.
job_category: build
area: transformation
readiness: supported
function:
  - finance
industry:
  - retail
domain_objects:
  - store
  - till_session
  - pos_event
  - tender_line
  - cash_movement
  - deposit_slip
  - till_settlement
  - settlement_exception
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
  - Needs landed POS events, tender lines, till sessions and their counted closes, cash movements and deposit slips.
  - Rules, reasons, tolerance and retained float need approval; they may be captured as editable data.
  - A rule change restates a published day only as approved.
  - Without a recorded event identity, duplicate detection is unproven.
  - Reports the cash the records show, not why a till is short.
  - Settles the counted drawer; cashier attribution is separate.
  - Stops at the deposit slip; bank statements, processor payouts and order margin are separate.
  - Loading files belongs to file-drop-to-bronze; currency conversion to shared-fx-conversion.
related:
  - order-return-contribution-margin
  - finance-gl-subledger-tieout
  - retail-sell-through-stockout
  - file-drop-to-bronze
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

Build <till_settlement_model>, <deposit_comparison_model>, <line_trace_model>, <exception_model> and <coverage_model> from <pos_event_source>, <tender_line_source>, <till_session_source>, <cash_movement_source> and <deposit_slip_source>, plus any source the rules need. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only those they leave open. For each approved till session, publish its opening float, expected cash from the classes the approved rules count, the counted close and the over or short in the approved sign, with tenders apart under the approved classes. For each approved store and business day, compare the expected deposit with the slips and show undeposited amounts apart from any variance. Count a sale paid in several tenders once, keep change, tips, float moves and voided sales out of revenue as approved, flag refund, void, duplicate and unbalanced cases as approved, and treat a session with no counted close as approved, inventing no figure. Place every input record in a row, list it once with its reason or count it as approved; keep sources read-only and report what the inputs cannot prove.

## Verified by

- On a run that completes, there is one settlement row per approved till session, unique on its declared grain; records the approved scope leaves out are shown or counted with their reason as approved, the outcome states how many and why, and they move no figure.
- Each settled row's expected cash equals the approved identity over opening float, net cash received, refunds, paid-ins, paid-outs, drops and transfers plus any other class the approved rules show; over or short is counted close less expected cash, signed as approved.
- A session with no counted close follows the approved treatment (unsettled, estimated and labelled, or a named failure); where the run completes it shows its expected cash, carries no unlabelled count or over or short, and stays out of over or short totals unless approved.
- A balanced sale paid in several tenders counts once at its sale total on the approved basis; change reduces only the cash tender and is never revenue; a tip or other amount the approved rules keep apart is its own labelled amount and enters only the figures they name.
- A voided sale nets to zero revenue and a partial reversal by its amount, across the sessions the approved rules place receipt and reversal in, both visible; a refund moves at the tender paid, and one in another tender or with no original sale is flagged as approved.
- A float transfer, paid-in, paid-out, drop and cash back move expected cash as approved, never revenue; a transfer between tills nets to zero for the store where both legs are in scope and linked; an unmatched leg or a movement with no reason is listed with its reason.
- Cash, card and other tenders are published apart under the approved tender classes, each in the approved measures (such as received, refunded and net), and nets equal approved revenue plus any amount the approved rules show beside it (an unbalanced sale's amount, a tip, tax, rounding).
- A repeated POS event follows the approved rule and a repeat with different content is never silently overwritten; a sale whose tenders do not equal its total shows total, tendered amount and difference under the approved treatment, never silently repaired.
- Expected deposit follows the approved definition and is compared with slips under the approved cover rule; allocated amounts plus any listed unallocated amount sum to each slip; variance stays apart from till over or short, and an uncovered amount is in transit or overdue, never a till shortage.
- On a run that completes, every session, POS event, tender line, cash movement and deposit slip lands in a row, is listed once with its approved reason, or is counted with its reason where the approved scope only counts it; counts and amounts add up and a set-aside record moves no figure.
- A session beyond the approved tolerance is flagged and one within it is not, each with its exact signed amount; a run that cannot settle a session follows the approved behaviour and never shows it as settled; a late or corrected record changes no published figure silently.
- Published sessions, tender mix and deposits equal values derived independently from the source records and approved rules, each figure traces to its records, and the outcome states what the inputs cannot prove.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile the POS events, tender lines, till sessions, cash movements and deposit slips for keys, event identity, time zones, business-day boundaries, tender types, reason codes and records that link to nothing before proposing rules. Use Ask first only for semantics still open, and record each answer as the user's own decision. Keep rules, tolerances, reasons and cutovers as editable data where the approved requirements say so. Work out the expected settlement and deposit rows for the agreed cases independently of the models, from the source records and approved rules, before trusting the models, and cover the allowed branches the inputs may not carry, such as a reversal landing in a later session, a record that fits several reasons, one slip fitting several days and amounts in another currency. Reconcile each figure to its records and tie every input's counts and amounts to the output before declaring the work complete.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- verifying

### Ask first

- If unresolved, what starts and ends one till session (a shift, a drawer swap, a shared drawer, one left open or spanning the cutover), how is its business day set (open, close or a cutover, in which time zone), and are the cutover, tolerance and retained float effective-dated?
- If unresolved, which sessions, tills, tenders and sales count (training, test, no-sale, other currencies), are excluded records listed or only counted, and which reason wins when a record fits several?
- If unresolved, what moves expected cash (float transfers, paid-ins, paid-outs and their reasons, drops, safe loans, cash tips, card cash back, rounding, foreign cash), and does opening float come from the count, a standard or the prior close, and how is a gap to the prior close shown?
- If unresolved, how do tender types (checks, gift cards, wallets, house accounts) map to cash, card and other, which sit in the drawer, how is the mix shown, what is a sale's revenue (tax, discounts), and are tips or non-sale receipts (gift card sales, layaway) revenue, liability or drawer cash?
- If unresolved, how do voids (before or after tender, after close), partial reversals, exchanges and refunds (in another tender, with no original sale, at another store) count, and in which session and business day does each land?
- If unresolved, which count governs (first, recount, adjusted), how is over or short signed, what tolerance flags it, what follows a session with no counted close, does a run that cannot settle a session fail or publish it flagged, and are late or corrected records applied to published days?
- If unresolved, which keys link a tender line to its sale, a refund or void to its original and a movement to its session, what makes a repeat a duplicate or a conflict, and what follows an unbalanced sale or a record that links to nothing?
- If unresolved, what is the expected deposit (drops, counted close less retained float or both), which slip dates cover a business day, how is a slip allocated across days, stores or banks or shown when it matches none, and when is an uncovered amount overdue?

### Guardrails

- Do not choose the session boundaries, business day, population, cash identity, tender classes, void, refund and tip rules, count that governs, tolerance, deposit definition, cover and allocation rule or failure behaviour for the user or take them from the data; the user may ask for a recommendation.
- Never count a float transfer, change, set-aside record or a voided sale once its reversal applies as revenue, a tip except as approved, or a sale paid in several tenders more than once.
- Never read a missing count, tender or reason as zero, or present an estimated or substituted count, over or short or tender as recorded; show it as the approved rules say, and never show a total that depends on a missing count as zero.
- Never present an undeposited or in-transit amount as a till shortage, and never net a deposit variance into a till over or short.
- Never silently apportion, repair or drop an unbalanced sale, duplicate, conflicting or unlinked record; the recorded total, tendered amount and difference stay visible beside any approved treatment, and every record stays accounted for with its reason.
- Never add or net amounts in different currencies.
- Never infer theft, fault or cause from a difference; report only what the records show.
- Never publish a session or day as settled when the run could not establish its count, movements or slips, and never restate a published session or day silently when a late or corrected record arrives.
- Stop at the store deposit slip: do not reconcile to bank statements, settle processor payouts or fees, or compute order margin or revenue recognition, and keep sources read-only.
