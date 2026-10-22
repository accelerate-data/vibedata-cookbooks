---
id: sales-forecast-backtesting
title: Score submitted sales forecasts against realized bookings by forecast horizon
trigger:
  - Leaders submit a sales forecast every week, but nobody can say how close each submission came to what booked, or whether the misses run over or under.
  - A forecast is revised after its cutoff and the earlier submission's accuracy quietly improves.
  - Forecast and bookings totals disagree because deals slipped, were never forecast or were cancelled, and nobody can say how much of the gap each explains.
description: For each approved forecast period, score every submission as it stood at its cutoff against the bookings that landed, with signed error by approved forecast horizon split into named components, every deal accounted for, and each submission that cannot be scored kept visible with its reason.
pitch: Show how accurate each submitted forecast was and why it missed, without a later revision ever improving an earlier score.
job_category: build
area: transformation
readiness: supported
function:
  - revops
domain_objects:
  - forecast_submission
  - forecast_category
  - booking
  - forecast_error
  - forecast_horizon_cohort
  - forecast_exception
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
  - Submissions must have been captured when made; a present-day CRM export cannot supply missing history.
  - Scores forecast accuracy only; capturing pipeline state and building a forecast are separate outcomes.
related:
  - revops-pipeline-snapshots
  - revops-bookings-billings-cash
  - finance-budget-forecast-actual
  - metric-population-and-rollups
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

Score each submitted forecast in <forecast_submission_source> against the bookings in <booking_ledger> for each approved forecast period, publishing <submission_score_model>, <horizon_cohort_model>, <deal_attribution_model> and <reconciliation_model>. Inherit the Intent's semantics and settle only what it leaves open: the submission key and cutoff, revision rule, period and horizon bucket, actuals authority, period placement and cancellation, currency, error sign, headline category, component classes, reconciliation treatment and scope. Fix an expected result per submission before model logic. Score each submission as its cutoff snapshot so a later revision never changes it, split signed error into named components that sum to it, account for every forecast line and in-scope booked deal, set aside what cannot be scored with its reason, and report what the history cannot answer.

## Verified by

- The approved contract fixes the submission key, cutoff, revision rule, period and horizon bucket, actuals authority and placement, cancellation and currency treatment, error sign, categories and component classes, with an independent expected result per submission written before model logic.
- Each submission is scored as its cutoff snapshot. A revision made after the cutoff, even one that would shrink the error, leaves that submission's forecast, actual and error unchanged and appears only in its own later submission.
- Actuals come only from the approved authority, count each booking once in its approved period under the approved cancellation rule, and equal totals derived independently from the ledger for every scored period.
- Forecast equals the snapshot's lines and, where approved, the submitted header total within the approved tolerance; a submission that does not reconcile follows the approved disposition, and one set aside is unscored and listed with both totals.
- Signed error splits into approved components that at least separate booked but not forecast, forecast but booked outside the period, and forecast but never booked. They sum to it on every row, and an empty one shows 0.
- A category scores only the deals the submission placed in it. Booked-not-forecast has no category, so the total carries it and total error equals the category errors plus that component, with no allocation invented.
- Every in-scope booking in a scored period appears in every scored submission for it, as a line or as booked-not-forecast, with its deal named. Every line is counted once or set aside with a reason, and every submission is scored or set aside.
- The horizon cohort combines the approved submitters from their deal lines, never by averaging submission scores. A consumer averaging submission errors gets a different figure wherever submitters differ.
- A period not closed under the approved as-of rule is reported as not closed and never scored. A period or cutoff with no submission is listed as a gap, never as zero error.
- Lines the approved rules cannot place (other currency, missing deal, amount or category, tied revisions) follow the approved disposition, and a set-aside line carries its reason and enters no figure.
- Published results equal values derived independently from the sources and approved rules, and a consumer reading the current CRM state instead of the snapshot gets a different, wrong score.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain and sources. Confirm the submission and booking references resolve on the target and profile keys, categories, cutoffs, revisions, amounts and currencies. Use Ask first only for unresolved semantics, then record the contract and a per-submission expected result, derived by hand from the sources, before model logic. Read period boundaries from the Domain's governed calendar where one exists. Resolve each submission to its cutoff snapshot first, then attribute each deal to exactly one component, so components and category rows follow from the same attribution. Read actuals from the approved authority only, build the cohort from deal lines, and publish a reconciliation that shows each check's population and unaccounted count. Keep a set-aside reason vocabulary as data. Keep sources read-only, label any synthetic fixture, and report cases not executed as incomplete verification.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which forecast periods and horizon bucket (weeks before period end or another), which calendar, and which as-of date decides a period is closed and scorable?
- If the submissions are not settled, what identifies a submission (submitter, period, cutoff), which revision is in force at a cutoff, what does the headline forecast include, and how are tied revisions handled?
- Which population does a submission cover (whole period, or only the submitter's own deals, territory or segment), and which bookings or deals are out of scope and how are they shown?
- Which ledger is the authority for actuals, which measure and date place a booking in a period, and how do cancellations, amendments and reversals count, including after the period ends?
- If unspecified, which currency is reported, and how are other-currency lines handled (converted under an approved rate or set aside)?
- If unresolved, which sign convention and percentage base, which categories exist, which further component classes name a miss, and how a deal that changes category, amount or scope after a submission is classed?
- When a header total differs from its lines beyond any tolerance, a line has no deal or amount, or revisions tie, does the run fail, or is the line or submission set aside or scored with a flag?
- Which cuts are published (submitter, category, horizon bucket, period), and which submitters or segments combine into one horizon figure?

### Guardrails

- Never apply a revision made after a submission's cutoff to that submission, and never let a later submission replace an earlier one's score.
- Do not reconstruct missing historical submissions from today's CRM state. Absent history stays absent, and an unobserved submission is a gap, not a zero.
- Do not average submission scores to publish a cohort figure, and do not add a total row to its category rows.
- Do not charge booked-not-forecast, which has no category, to any category.
- Do not convert currencies unless the approved rule says how, and do not equate a missing figure with zero.
- Keep sources read-only. Score forecasts, not people: no ranking, coaching or target-setting output.
