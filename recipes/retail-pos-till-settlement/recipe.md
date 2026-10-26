---
id: retail-pos-till-settlement
title: Settle store till sessions to counted cash, tender mix and deposit slips with an explicit over or short
trigger:
  - Stores count each till at shift close and Finance cannot tell which shortages are real and which come from how the POS records voids, refunds, change and float moves.
  - A split-tender sale, a voided sale or a float transfer between tills is counted as revenue or cash twice, or not at all, and the till never reconciles.
  - A store deposit differs from what the tills dropped and nobody can say whether cash is missing or simply not yet banked.
description: For approved store till sessions, reconcile POS sales, refunds and voids, tender lines and cash movements to the counted close, publish each session's expected cash, tender mix and signed over or short, and compare each store day's expected deposit with its slips, with every record placed or listed with its reason.
pitch: One settlement row per till session shows expected cash, the count and the difference, with tenders kept apart and every deposit gap explained.
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
  - over_short
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
  - Needs landed POS events, tender lines, till sessions with counted closes, cash movements and deposit slips.
  - Rules, reasons, tolerance and retained float need approval; they may be captured as editable data.
  - Without a recorded event identity, duplicate detection is unproven.
  - Reports the cash the records show, not why a till is short.
  - Stops at the deposit slip; bank statements, processor payouts and order margin are separate.
related:
  - order-return-contribution-margin
  - finance-gl-subledger-tieout
  - retail-sell-through-stockout
  - file-drop-to-bronze
evidence:
  features:
    - capturing-requirements
    - generating-dbt-model
    - verifying
  evals: []
---

## Prompt

Build <till_settlement_model>, <deposit_comparison_model>, <line_trace_model>, <exception_model> and <coverage_model> from <pos_event_source>, <tender_line_source>, <till_session_source>, <cash_movement_source> and <deposit_slip_source>, plus any source the rules need. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only those they leave open. For each approved till session, publish its opening float, net cash received, refunds, paid-ins, paid-outs, drops and transfers as the approved rules count them, expected cash, counted close and signed over or short, with cash, card and other tenders apart. For each approved store and business day, compare the expected deposit with the slips and show undeposited amounts apart from any variance. Count a sale paid in several tenders once, keep change, tips, float moves and voided sales out of revenue as approved, flag refund, void, duplicate and unbalanced cases as approved, and show a session with no counted close as unsettled with no invented figure. Place every input record in a row or list it once with its reason, keep sources read-only and report what the inputs cannot prove.

## Verified by

- On a run that completes, there is one settlement row per approved till session, unique on its declared grain; sessions the approved scope leaves out (training, test) are shown or counted with their reason, the outcome states how many, and they appear in no settlement or deposit figure.
- Each settled row's expected cash follows the approved identity over opening float, net cash received, refunds, paid-ins, paid-outs, drops and transfers; over or short is counted close less expected cash in the approved sign, within approved rounding, zero a real value.
- A session with no counted close follows the approved treatment (unsettled, estimated and labelled, or a named failure), shows its expected cash, and carries no unlabelled count or over or short; it stays out of over or short totals unless approved.
- A sale paid in several tenders counts once at its sale total on the approved basis; change given back reduces only the cash tender and is never revenue, and an amount the approved rules keep apart (such as a tip held outside the till) enters no revenue, tender or expected cash figure.
- A voided or reversed sale leaves no revenue and its tenders reverse as approved, with receipt and reversal both visible; a refund moves at the tender it was paid in, and one in a different tender than its sale, or with no original sale, is flagged and follows the approved rule.
- A float transfer, paid-in, paid-out and drop move expected cash as approved and never revenue or a sale; a transfer between tills nets to zero for the store, and a movement with no reason follows the approved treatment with its reason shown.
- Cash, card and other tenders are published apart, each in the approved measures (such as received, refunded and net), and the nets equal approved revenue plus any amount shown beside it, such as an unbalanced sale's difference or a tip.
- A repeated POS event follows the approved rule, and a repeat with different content is never silently overwritten; a sale whose tenders do not equal its total shows total, tendered amount and difference under the approved treatment, never apportioned or silently corrected.
- For each approved store and business day, expected deposit follows the approved definition and is compared with slips under the approved cover rule; the variance is shown apart from till over or short, and an uncovered amount shows as in transit, or overdue as approved, never as a till shortage.
- On a run that completes, every session, POS event, tender line, cash movement and deposit slip lands in a published row or is listed once with its reason; per-input counts and amounts add up, a record under a set-aside parent follows the parent, and a set-aside record moves no figure.
- Published sessions, tender mix and deposits equal values derived independently from the source records and approved rules, each figure traces to its records, and the outcome states what the inputs cannot prove.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile the POS events, tender lines, till sessions, cash movements and deposit slips for keys, event identity, time zones, business-day boundaries, tender types, reason codes and records that link to nothing before proposing rules. Use Ask first only for semantics still open, and record each answer as the user's own decision. Keep rules, tolerances, reasons and cutovers as editable data where the approved requirements say so. Work out the expected settlement and deposit rows for the agreed cases independently of the models, from the source records and approved rules, before trusting the models, and cover cases the inputs may not carry, such as a void after the session closed, a cash tip, a shared till, one slip covering several days and a foreign-currency tender. Reconcile each figure to its records and tie every input's counts and amounts to the output before declaring the work complete.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- verifying

### Ask first

- If unresolved, what is one settlement (till session, cashier, till day), which sessions count (training, test, no-sale, house accounts) and are those listed or only counted, and how is the business day set (open, close or a cutover, in which time zone)?
- If unresolved, what moves expected cash (float transfers, paid-ins, paid-outs and their reasons, drops, safe loans, cash tips, rounding, checks, foreign cash), which tenders sit in the drawer, and does opening float come from the count, a standard or the prior close?
- If unresolved, what is a sale's revenue (tax, discounts) and are tips revenue, a liability or held in the drawer, how do change, voids after tender or after close, exchanges, and refunds in another tender or with no original sale count, and in which session and business day does each land?
- If unresolved, how is over or short signed and charged (till, cashier, shared), what tolerance flags it, and what follows a session with no counted close, a recount or an adjusted count (unsettled, estimated or a failure)?
- If unresolved, which keys link a tender line to its sale, a refund or void to its original, and a movement to its session, what makes a repeated event a duplicate or a conflict, and what follows a sale whose tenders do not equal its total or a record that links to nothing?
- If unresolved, what is the expected deposit (drops, counted close less retained float or both), which slip dates cover a business day, may one slip cover several days or several stores, when is an uncovered amount overdue, and how is a slip matching no day shown?
- If unresolved, how is the tender mix shown (received, reversed, refunded, net), is card or other tender compared with terminal batch totals, which currency applies, and are other-currency tenders converted, kept apart or set aside?
- If unresolved, when the run cannot close a session or day (an unplaceable record, a missing feed), does it fail, publish flagged or publish nothing, are late or corrected records applied to published days, and which reasons name records set aside?

### Guardrails

- Do not choose the settlement unit, business day, population, cash identity, tender treatment, void, refund and tip rules, tolerance, deposit definition, cover rule or failure behaviour for the user or take them from the data; the user may ask for a recommendation.
- Never count a float transfer, change, voided sale or set-aside record as revenue, a tip except as approved, or a sale paid in several tenders more than once.
- Never read a missing count, tender or reason as zero, or present an estimated or substituted count, over or short or tender as recorded; show it as the approved rules say.
- Never present an undeposited or in-transit amount as a till shortage, and never net a deposit variance into a till over or short.
- Never apportion, repair or silently drop an unbalanced sale, duplicate, conflicting or unlinked record; every record of every input stays accounted for with its reason.
- Never infer theft, fault or cause from a difference; report only what the records show.
- Never restate a published session or day silently when a late or corrected record arrives.
- Stop at the store deposit slip: do not reconcile to bank statements, settle processor payouts or fees, or compute order margin or revenue recognition, and keep sources read-only.
