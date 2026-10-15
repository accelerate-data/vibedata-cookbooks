---
id: revops-bookings-billings-cash
title: Tie bookings to billings to cash and classify every break
trigger:
  - RevOps and Finance each quote booked, billed and collected, and the three numbers never agree because every team ties them together with its own spreadsheet.
  - A signed booking is billed late, billed twice or billed after it was cancelled, or an invoice has no booking behind it, and nobody sees it until the customer calls.
  - Cash arrives that nobody can match to an invoice, or an invoice is part paid, and the gap between billed and collected has no stated reason.
description: For each approved as-of date, tie every in-scope booking line to what was scheduled, billed after credit memos and collected, split each gap into breaks classed under the user's approved rules, show any residual as unexplained, and keep every unplaceable record visible with its reason.
pitch: Reconcile what was booked to what was billed and what was collected, with every gap named and nothing quietly absorbed.
job_category: build
area: transformation
readiness: supported
domain_objects:
  - booking_line
  - billing_plan
  - invoice_line
  - credit_memo
  - payment
  - cash_application
  - reconciliation_break
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
  - Assessed end to end on duckdb_local only; the other listed targets rely on dbt support and are unassessed.
  - Billing needs a stated booking-line reference and cash a stated invoice application, or an approved matching rule.
  - Stops at the classified tie; revenue recognition, ageing, commission and ledger tie-out are separate outcomes.
  - Reproducing a past as-of result after back-dated changes needs kept history; a rebuild restates it.
related:
  - finance-gl-subledger-tieout
  - finance-ar-aging-dso
  - revops-quota-commission
  - finance-revenue-recognition
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

Build <bridge_model>, <breaks_model>, <exceptions_model> and <totals_model> from <booking_source>, <billing_source> and <cash_source>. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only the semantics they leave open. For each approved as-of date, at booking-line grain with legal entity and currency kept apart, set what was booked beside what was scheduled to be billed, what was billed after credit memos and what was collected, explain each difference as breaks classed under the approved rules, leave any residual visible as unexplained, and list every record that cannot be placed or processed with its reason. Keep sources read-only and report what the inputs cannot prove.

## Verified by

- On a run that completes, at each in-scope as-of date and booking line, the booked-to-billed and billed-to-collected reconciliations each balance exactly: every difference is an approved class, an approved non-break term (such as not yet scheduled or not yet due) or a visible residual.
- On a run that completes, for each as-of date every amount of every in-scope record lands exactly once: on a booking line, as a break with no line, out of scope with its reason, or as an exception; counts and amounts reconcile per entity and currency, with nothing lost or counted twice.
- On a run that completes, each amount is in exactly one class under the approved precedence, records just inside and outside each approved window, tolerance edge, due date and as-of date are classed as approved, and an amount within tolerance stays visible as such.
- Amendments and cancellations act on booked and the billing plan as approved, and a billing after a cancellation stays visible; whether back-dated changes restate a past as-of follows the approved rule, and is unproven without kept history.
- Credit memos are treated as approved and never reported as cash received; a billing matching no booking line, a repeated billing and an over-billing are each shown as approved, as a class or an exception, with their own amounts and not merged unless approved.
- Payments with no application, and applications to an unknown or excepted record, stay visible with their amounts and settle nothing, and sit on no booking line, unless an approved rule applies them.
- No figure combines two entities or two currencies; where conversion is approved, the rates and rules applied are stated and the result reconciles as they say.
- Records dated after the as-of date on the approved date basis are not counted for it, and bookings placed after it on that basis are listed out of scope with their amounts and given no break class.
- Where the approved policy shows an unexplained residual it is published per line and never absorbed into a class; where it fails the run on a residual, an exception or a mismatch, the run fails explicitly, naming each offending line or record and its amount.
- On a run that completes, totals per as-of date, entity and currency, and any approved roll-up, equal the per-line figures, carry every class total, and show exception counts and amounts per reason beside the classes, not netted into them.
- Expected results for each stated behaviour are derived from the source records and approved rules independently of the implementation, and each output is unique on its declared grain.
- The outcome states which breaks, exceptions and residuals remain open and what the inputs cannot prove.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile the booking lines, their versions and billing plans, the invoice and credit lines, the payments and the applications: keys, entities, currencies, dates, signs and which links the sources actually carry. Use Ask first only for semantics still open, and record each answer as the user's own decision. Keep the break classes, their precedence, tolerances, timing windows, as-of dates, entities and currencies as editable data where the approved requirements say so, and make the bridge, breaks, exceptions and totals agree about every record. Prove each stated behaviour on the source records, including the boundary and exceptional cases, with expected results derived independently of the models. Report every break, exception and residual left open and what the inputs cannot prove.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which booking lines are in scope (status, cancelled, test, zero value, other populations), which entities, currencies and fiscal calendar apply, which as-of dates are run, and which roll-ups beyond the booking line are published?
- If unresolved, what links a billing to a booking line and plan installment, and cash to an invoice, may one document span several lines or invoices, and what happens to a missing, unknown, voided or reissued reference?
- If unresolved, how do amendments and cancellations act on booked and the billing plan, what counts as expected to be billed by the as-of date (advance, arrears, usage, milestone), and do back-dated changes restate past as-ofs?
- If unresolved, which break classes exist and how is each identified, which wins when several fit, what is the rounding tolerance, and what separates a repeated billing from an over-billing?
- If unresolved, how does timing work: a grace period before late becomes never billed, whether collection timing follows invoice due dates, and which date places each record?
- If unresolved, how are credit memos, refunds, part payments, overpayments, prepayments or on-account cash, write-offs, disputes, short-pays and fees treated, and is cash applied only through stated applications or may a rule infer them?
- If unresolved, which records are exceptions rather than breaks, and does an exception, an unexplained residual or a currency or entity mismatch fail the run, stay visible or force the line unexplained?
- If unresolved, is any currency conversion or tax treatment approved, and under which rates and rules; otherwise are figures kept per currency and net of tax?

### Guardrails

- Do not choose break classes, precedence, tolerance, timing windows, population or exception handling for the user, and take none from the data or common practice; the user may ask for alternatives or a recommendation.
- Never match a billing or a payment on customer, amount or date alone unless the approved rules say so; report an unlinked record under the approved rule and do not infer which installment or invoice it meant.
- Never net or convert across legal entities or currencies because they share a booking or an account; convert only under approved rates and rules.
- Never drop, double count or absorb an amount; an excepted record settles nothing, and its amount stays visible and counted once.
- Never report a credit memo as cash received, never hide an overpayment by clamping it to zero, and never force an unapplied payment onto a booking line unless an approved rule applies it.
- Never default a missing amount, date or key to zero or to a convenient value unless the approved semantics define it so.
- Never absorb a residual into a class, a tolerance or an adjustment to make a line tie; an unexplained difference stays visible.
- A break records a difference, not which system is wrong; do not assume the booking, the invoice or the payment is correct.
- Stop at the classified tie: do not recognise revenue, age receivables, credit commission, tie to the ledger or post corrections, and keep sources read-only.
