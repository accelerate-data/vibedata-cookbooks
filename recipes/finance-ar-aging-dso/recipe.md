---
id: finance-ar-aging-dso
title: Age receivables and compute DSO from open invoices as of any chosen date
trigger:
  - Finance needs the aged receivables report and DSO for a past month or quarter end, but the receivables system only shows what is open today.
  - The aging report and DSO are rebuilt by hand in a spreadsheet each month, and their totals never quite agree with the open invoices.
  - An auditor asks what was open at a past date and how overdue it was, and someone has to rebuild the answer by hand.
description: For each approved as-of date, list every in-scope receivable open on that date with its open amount, days past due and aging bucket, total it at the approved grain, and compute DSO under the user's approved rules, while every record that cannot be processed stays visible, as an exception or in an explicit run failure, so no amount is lost, counted twice or settled early.
pitch: Rebuild aged receivables and DSO for each approved as-of date from dated receivable documents, payments and, where recorded, cash applications.
job_category: build
area: transformation
readiness: supported
domain_objects:
  - accounts_receivable
  - invoice
  - credit_memo
  - payment
  - cash_application
  - aging_bucket
  - days_sales_outstanding
  - receivables_exception
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
  - Settling as of a past date needs dated cash applications, or an approved rule linking payments to documents.
  - Reproducing results as known on a past date needs entry timestamps or kept snapshots of the results.
  - Stops at aging and DSO; collections, disputes and bad-debt provisioning are separate outcomes.
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

Build <aging_detail_model>, <customer_aging_model>, <customer_summary_model>, <dso_model> and <exceptions_model> from <receivable_documents_source>, <payments_source>, <as_of_dates> and, where recorded, <cash_applications_source>. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only the semantics they leave open. For each approved as-of date, list every in-scope receivable open on that date and not excluded as an exception, with its open amount, days past due and aging bucket, total it at the approved grain (customer by bucket, with legal entity and currency wherever they apply) with credits and net balance shown as the approved rules say, compute DSO under the approved formula, and list every record that cannot be processed as an exception, or fail the run naming it, as the approved policy says. Where consolidation or currency translation is approved, apply the approved mapping, rates and rules and reconcile the result as they say. Keep sources read-only. Report what the inputs cannot prove.

## Verified by

- On a run that completes, for each as-of date, every in-scope receivable open then and not excluded as an exception appears once, at its original amount less settlements under the approved rules; nothing effective after it, or where computed as known, entered after it, changes the result.
- Days past due and the aging bucket follow the approved basis, terms, bucket bounds and precision, including receivables due exactly on the as-of date and those on each side of every bucket edge.
- Partial settlements, write-offs, over-applications, reversed or bounced payments and credits are applied as the approved rules say; a reversal never leaves credit available that the approved rules do not allow.
- On a run that completes, per as-of date, every amount of each in-scope document, payment and application effective by it (and, if computed as known, entered by it) or undated lands once: open, settled, held as credit or left out as approved, or excluded with its record as an exception.
- On a run that completes, at the approved reconciliation grain, including entity and currency wherever relevant, valid aged documents less their settlements equal the open detail and its bucket totals; any unapplied credit reconciles to valid credits net of reversals and amounts applied.
- Entities and currencies are never netted together unless an approved consolidation or translation rule is stated, and the totals reconcile under that rule.
- DSO follows the approved formula, window, grain and inputs, its receivables reconcile to the detail and credits the approved inclusion rule names, documents just inside and outside the window are treated as approved, and rounding is as approved.
- Where the approved window has no positive sales, DSO is reported as the approved rule says, never as zero or infinite unless the approved semantics define it so.
- On a run that completes, every unprocessable record is listed with its reasons under the approved exception grain, its effect follows the approved policy, and it is counted on its customer at the approved grain, or as unattributed, appearing in summaries as the row rule says.
- Where the approved policy fails the run on an unprocessable record, the run fails explicitly and names each offending record with its reason.
- On a run that completes, balances, exceptions and completeness roll up to the same approved grain, and each output is unique on its declared business grain with required fields populated.
- The outcome states which exceptions remain open and what the inputs cannot prove, such as whether backdated entries restate past results.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile the receivable documents (types, dates, amounts, terms, entities, currencies), the payments and the cash applications, and check whether applications carry their own dates and name the document and the payment or credit they settle. Use Ask first only for semantics still open, and record each decision as the user's own answer. Keep the terms, aging buckets, as-of dates, DSO window and document-type behaviour explicit and editable where the approved requirements say so. The detail, customer totals, DSO and exceptions must never disagree about a record or an amount. Report every exception left open and what the inputs cannot prove.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which document types are aged, which entities, currencies and customers are in scope, at what grain and under what consolidation or translation rule, and how are credit memos and payments not yet applied shown: as unapplied credit, as negative aged items, or left out?
- If unresolved, which date settles a receivable (the application date or the payment's receipt date), and how is a payment or credit linked to the documents it settles: recorded applications, oldest first, or a reference?
- If unresolved, how are partial settlements, write-offs and reversed or bounced payments treated, and what happens when an application exceeds what the document owes or what its payment or credit holds?
- If unresolved, is age measured from the due date or the document date, how is the due date set, which aging buckets apply with which inclusive edges, and at what precision?
- If unresolved, which as-of dates are reported, and are results computed from business dates or as known on each date, using entry timestamps?
- If unresolved, which DSO method, window and grain apply, which receivables and credits and which sales enter it, how is it rounded (including a negative numerator), and what is shown when the window has no positive sales?
- If unresolved, which records cannot be processed, one row per reason or one primary reason, which customer (and entity and currency where relevant) each is reported on, and is it excluded with a visible count or does it fail the run?
- If unresolved, which customers get a summary row on an as-of date: only those with an open balance or unapplied credit, or also those with excluded records?

### Guardrails

- Do not choose the settlement date, cash-linking rule, aging basis, buckets, DSO formula or exception handling for the user, and take none from the data or common practice; the user may ask for alternatives or a recommendation.
- Do not link cash to documents oldest-first, by amount or by inference unless the approved rules say so; report payments and credits left unapplied.
- Never let a record effective after an as-of date under the approved rules affect it, and never present today's open balances as a past date's.
- Never drop or double count a record or an amount beyond what the approved rules leave out; every record that cannot be processed stays visible, as an exception or in an explicit run failure, with its reason.
- Never net distinct legal entities or currencies together because they share a customer; consolidate or translate only under the approved mapping, rates and rules.
- Never default a missing amount or sales figure to zero, or fill a missing date, unless the approved semantics say so.
- Do not claim results as known on a past date when the source has no entry timestamps or kept snapshots; say backdated entries restate them.
- Stop at aging and DSO: do not chase collections, change customer balances or post adjustments to the source systems.
