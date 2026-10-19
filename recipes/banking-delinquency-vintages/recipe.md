---
id: banking-delinquency-vintages
title: Build loan delinquency roll rates and vintage curves from loan, schedule, payment and event records
trigger:
  - Credit risk reads delinquency off a servicer status field that each system refreshes on its own day, so bucket counts and roll rates differ from report to report.
  - Roll rates only show loans that stayed or got worse, because loans that paid off, were charged off or dropped out of the data vanish and the rows stop adding up.
  - Vintage curves look better for older cohorts than they should because they divide by today's balance, and young cohorts show a zero where the data does not reach yet.
  - A month that was already reported changes when late or backdated payments arrive, and nobody can say which version a published figure came from.
description: For each approved month-end, place every in-scope term loan in a delinquency bucket, show where each bucket's loans and balance went by the next month-end including exits, and show how each origination cohort turns delinquent as it ages, with every record left out or unplaceable listed with its reason.
pitch: Month-end buckets, roll rates and vintage curves for a term-loan book that add up, keep currencies apart and never invent a cure.
job_category: build
area: transformation
readiness: supported
industry:
  - banking
domain_objects:
  - loan
  - repayment_schedule
  - payment
  - delinquency_bucket
  - roll_rate
  - vintage_curve
  - delinquency_exception
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
  - Needs loans, dated payments and status events, and repayment schedules where delinquency is derived from them.
  - Covers instalment (term) loans; revolving and card products are a separate outcome.
  - Stops at delinquency measurement; provisioning, collections and recoveries are separate outcomes.
  - Results as known on a past month-end need entry timestamps on payments, events and schedule changes.
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

Build <placement_model>, <roll_rate_model>, <vintage_model> and <exceptions_model> from <loan_master_source>, <repayment_schedule_source>, <payments_source> and <status_events_source>. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only the semantics they leave open. For each approved month-end, place every in-scope loan open then in a delinquency bucket under the approved rule, show where each bucket's loans and balance went by the next month-end, including loans that left or cannot be followed, and show for each origination cohort how delinquency builds with age, leaving ages the cohort has not reached empty rather than zero. Keep currencies apart, list every record left out or unplaceable with its reason, and keep a published month-end stable as the approved time basis says. Keep sources read-only. Report what the inputs cannot prove.

## Verified by

- On a run that completes, each in-scope loan appears once at each month-end it is open under the approved population rule, in the bucket the approved measure gives, including loans either side of every approved edge; a loan the approved ending rule has ended has no later row.
- Delinquency and balance follow the approved balance definition and payment-application rules: partial payments, prepayments and payments dated before but recorded after a month-end are applied as approved, and the approved rule says whether a payment ahead of schedule can change a bucket.
- On a run that completes, per from month-end, from-bucket and currency, the loans and balance across all roll-rate destinations reconcile on each approved roll-rate measure; a new loan is never counted in a from-bucket it did not hold; cured and worse follow the approved bucket order.
- A loan that leaves without an ending event the approved rule recognises, cannot be followed, or cannot be bucketed is shown as the approved rule says, never silently as cured or current, and is listed with its reason.
- Published placements, roll rates and vintage measures equal values derived independently from the sources and approved rules: each share uses the approved denominator, exits follow the approved cohort treatment, and an age not fully reached is absent, null or marked as approved, never zero.
- Where the approved vintage measures include a reading on outstanding balance, its bucket split sums to the cohort's outstanding balance at that age, and an empty denominator follows the approved treatment, never a silent zero.
- Modified, restructured or deferred loans follow the approved schedule rule and are flagged as approved; one never reads as current without it, and the delinquency it had before the change is kept or dropped as approved.
- Every total and rate is keyed by currency; no published figure adds currencies unless an approved translation rule is stated and the totals reconcile under it; entities and products are combined only at the approved reporting cuts.
- On a run that completes, every input row contributes to an output or is listed with its reason under the approved listing rule: orphans, duplicates, excluded products, loans with no schedule, loans missing from a month; none is dropped or counted twice and the residue is zero.
- Where the approved basis is as known at each month-end, a payment, event, schedule version or loan change recorded later does not alter an earlier month-end; where restated, a rerun on unchanged inputs reproduces the same results and the outcome reports which month-ends changed.
- The month-end series is contiguous over the approved window except month-ends the approved untrusted-month rule withholds, which are listed; a month-end with no in-scope loan is empty, not missing; where that rule is to fail, the failure names the offending records and publishes no results.
- The outcome states what the inputs cannot prove, such as whether late entries restate past months or whether a vanished loan was repaid.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile the loans, schedules, payments and status events: loan types, currencies, origination and end dates, schedule versions, the principal and interest split of each instalment, how payments name what they settle, and whether payments, events and schedule changes carry the instant they were recorded. Use Ask first only for semantics still open, and record each decision as the user's own answer. Keep the bucket edges and the exception reasons editable rather than hard-coded, and derive delinquency from the schedules and payments instead of trusting a stored status unless the user approves it. The placements, roll rates, vintages and exceptions must never disagree about a loan or an amount. Report every exception left open and what the inputs cannot prove.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which loans are in scope (term products, entities, portfolios, secured or unsecured), which cuts are published, are currencies kept apart or translated at which approved rates, and how are revolving and other excluded records listed?
- If unresolved, what measures delinquency (days past due on the oldest unpaid instalment, missed instalments or a stored status), what grace period, buckets, inclusive edges and due-date convention apply, and how do payments, partial payments and prepayments settle instalments?
- If unresolved, how are payoff, charge-off, sale or default recognised, what balance does an exiting loan carry out, is a transferred or re-keyed loan matched to its earlier key, and are acquired loans new originations and from which date?
- If unresolved, what does a loan's balance hold (principal, accrued interest, fees, net of write-offs), what do the roll rates measure (balance or count) over what interval, and what counts as worse, cured or stayed?
- If unresolved, how are cohorts formed (month, quarter or other), what counts as delinquent for the curve (a depth, a charge-off) and on which balance, when is age zero, do exited loans stay in the cohort and its ever-delinquent count, and how are partly observed ages and empty denominators shown?
- If unresolved, how are modified, restructured, forborne or payment-holiday loans treated: which schedule governs the bucket, is earlier delinquency kept, whether and how are they flagged, and may they cure at the change?
- If unresolved, which month-ends are reported (window, whether the latest open month publishes), are they computed as known on each date using entry timestamps for payments, events and schedule changes or restated from final data, and which calendar defines month-end?
- If unresolved, how is each excluded, unplaceable, new or missing record (orphan, duplicate, no schedule, malformed value) listed and counted, and does a month that cannot be trusted publish flagged, withhold or fail?

### Guardrails

- Do not choose the delinquency measure, edges, balance, payment application, ending rule, roll-rate or cohort definition, modification treatment or time basis for the user, or take one from the data or common practice, unless the approved requirements settle it; the user may ask for a recommendation.
- Never silently read a loan that disappeared, cannot be followed or has no schedule as current or cured, and never infer a payoff or charge-off from days past due unless the user approves that rule.
- Never let a loan that leaves the book vanish from a roll rate: the from-bucket must still reconcile to what it held, with each exit under the approved destinations.
- Never divide a cohort's delinquency by a balance the user has not approved, and never show an age the cohort has not reached as zero.
- Never rewrite a published month-end under an as-known basis, and never present later-recorded input as if it were known earlier.
- Never sum loans or balances across currencies, and across entities or products only at the approved reporting cuts; translate currencies only under an approved rate rule.
- Never default a missing amount, date or rate to zero or fill it without approval, and never drop or double count a record; every record that cannot be processed stays visible with its reason.
- Do not re-age a modified loan or drop its earlier delinquency except as the user approves, and never without the flag the approved rule requires.
- Stop at delinquency measurement: do not provision, set collection actions, value recoveries or change the source loan records.
