---
id: finance-ap-aging
title: Age payables from open items as of any chosen date and reconcile the total
trigger:
  - Finance needs the aged payables for a past month or quarter end, but the payables system only shows what is owed today.
  - The payables aging is rebuilt by hand in a spreadsheet each month, and its total never ties back to what was billed and paid since the last close.
  - Treasury or an auditor asks what was owed to which supplier at a past date, how overdue it was and how much was on hold.
description: For each approved as-of date, list every in-scope supplier bill open then with its open amount, days past due, aging bucket and hold status, total it at the approved grain and reconcile the total to the previous date through its movements, keeping every unprocessable record visible so no amount is lost, counted twice or settled early.
pitch: Rebuild aged payables and a reconciling roll-forward for any approved as-of date from dated supplier bills, credits, payments and applications.
job_category: build
area: transformation
readiness: supported
domain_objects:
  - accounts_payable
  - vendor_bill
  - vendor_credit
  - vendor_payment
  - payment_application
  - payment_hold
  - aging_bucket
  - payables_roll_forward
  - payables_exception
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
  - Settling as of a past date needs dated applications, or an approved rule linking payments and credits to bills.
  - Reproducing results as known on a past date needs entry timestamps or kept snapshots of the results.
  - Stops at aging and its roll-forward; duplicate detection, payment runs and ledger tie-out are separate.
related:
  - dbt-snapshot-history
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

Build <aging_detail_model>, <supplier_aging_model>, <supplier_summary_model>, <roll_forward_model> and <exceptions_model> from <supplier_bills_source>, <supplier_credits_source>, <supplier_payments_source>, <as_of_dates> and, where recorded or approved, <applications_source>, <holds_source> and <opening_balances_source>. Resolve with the user only the semantics the Intent's approved requirements leave open. For each approved as-of date, list every in-scope bill in payables and open on that date and not excluded as an exception, with its open amount, days past due, and aging bucket and hold status under the approved rules; total it at the approved grain (supplier by bucket, with legal entity and currency where they apply), with unapplied credits and net payable shown as the approved rules say; explain how the total moved since the previous as-of date through the approved movement classes; and list every record that cannot be processed as an exception, or fail the run naming it, as the approved policy says. Where consolidation or translation is approved, apply and reconcile it under the approved mapping, rates and rules. Keep sources read-only. Report what the inputs cannot prove.

## Verified by

- On a run that completes, for each as-of date, every in-scope bill in payables by then under the approved rule, still owing and not excluded as an exception appears once, at its amount less approved settlements; nothing effective, or if computed as known entered, after it changes the result.
- Days past due and the aging bucket follow the approved basis, terms, hold rule, bucket bounds and precision, including bills due exactly on the as-of date and those on each side of every bucket edge.
- Partial settlements, discounts taken, write-offs, voided payments and over-applications are applied as the approved rules say; a voided or reversed payment never leaves credit available that the approved rules do not allow.
- Holds are reported as the approved rules say, including holds starting or released on the as-of date, and never change a bill's amount or appear twice.
- On a run that completes, per as-of date, every amount of each in-scope bill, credit, payment, application and hold effective by it (and, if computed as known, entered by it) or undated lands once: open, settled, unapplied credit or left out as approved, or excluded as an exception.
- On a run that completes, at the approved grain (entity and currency where relevant), valid aged items less settlements equal the open detail, and its bucket totals plus any held amount kept out of buckets; unapplied credit ties to valid credits and payments net of reversals and applications.
- On a run that completes, each as-of date's total equals the previous date's (for the first, the approved opening) plus the approved movement classes since, including amounts entering or leaving exceptions, on the same time basis and grain; each supplier with a non-zero balance or movement is shown.
- Entities and currencies are never netted together unless an approved consolidation or translation rule is stated, and the totals reconcile under that rule.
- On a run that completes, every unprocessable record is listed with its reasons under the approved exception grain, its effect follows the approved policy, and it is counted on its supplier at the approved grain, or as unattributed, appearing in summaries as the row rule says.
- Where the approved policy fails the run on an unprocessable record, the run fails explicitly and names each offending record with its reason.
- On a run that completes, balances, movements, exceptions and completeness roll up to the same approved grain, and each output is unique on its declared business grain with required fields populated.
- The outcome states which exceptions remain open and what the inputs cannot prove, such as whether backdated entries restate past results or whether the records reach back far enough for the first date's opening.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile the supplier bills (dates, amounts, terms, entities, currencies, supplier invoice numbers), the credits, the payments, the applications and any holds, and check whether applications carry their own dates and name the bill and the payment or credit they settle. Use Ask first only for semantics still open, and record each decision as the user's own answer. Keep the terms, aging buckets, as-of dates, movement classes and hold reasons explicit and editable where the approved requirements say so. The detail, supplier totals, roll-forward and exceptions must never disagree about a record or an amount. Report every exception left open and what the inputs cannot prove.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which bills are aged, which entities, currencies and suppliers are in scope, at what grain and under what consolidation or translation rule, and how are supplier credits, prepayments and payments not yet applied shown: as unapplied credit, as negative aged items, or left out?
- If unresolved, which date puts a bill in payables (invoice date, receipt date or posting date), and which date settles it (the application date or the payment date)? How is a payment or credit linked to the bills it settles: recorded applications, oldest first, or a reference?
- If unresolved, how are partial settlements, early-payment discounts, write-offs and voided payments treated, and what happens when an application exceeds what the bill owes or what its payment or credit holds?
- If unresolved, is age measured from the due date or the bill date, how is the due date set, which aging buckets apply with which inclusive edges, and at what precision?
- If unresolved, what does a hold do (stay aged and flagged, leave the buckets, or pause the age), when is a bill on hold on an as-of date, and which reason is shown when several holds apply?
- If unresolved, what identifies a bill, what counts as an exact repeat of that identity, and which copy, if any, is aged?
- If unresolved, which as-of dates are reported, are results computed from business dates or as known on each date using entry timestamps, and what does the roll-forward open from on the first date: zero, or an approved opening balance?
- If unresolved, which records cannot be processed, one row per reason or one primary reason, which supplier (and entity and currency where relevant) each is reported on, is it excluded with a visible count or does it fail the run, and which suppliers get a summary row?

### Guardrails

- Do not choose the payables entry date, settlement date, cash-linking rule, aging basis, buckets, hold treatment, duplicate rule or exception handling for the user, and take none from the data or common practice; the user may ask for alternatives or a recommendation.
- Do not link payments or credits to bills oldest-first, by amount or by inference unless the approved rules say so; report payments and credits left unapplied.
- Never let a record effective after an as-of date under the approved rules affect it, and never present today's open payables as a past date's.
- Never drop or double count a record or an amount beyond what the approved rules leave out; every record that cannot be processed stays visible, as an exception or in an explicit run failure, with its reason.
- Never net distinct legal entities or currencies together because they share a supplier; consolidate or translate only under the approved mapping, rates and rules.
- Never default a missing amount to zero, or fill a missing date, unless the approved semantics say so.
- Do not claim results as known on a past date when the source has no entry timestamps or kept snapshots; say backdated entries restate them.
- Stop at aging and its roll-forward: do not detect fuzzy duplicate invoices, schedule payments, accrue unbilled receipts or post adjustments to the source systems.
