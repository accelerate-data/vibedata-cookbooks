---
id: customer-historical-ltv
title: Compute historical customer lifetime value with margin
trigger:
  - The payback conversation uses a customer value from a spreadsheet nobody can reproduce, and it counts order revenue only, with no refunds and no cost of serving the orders.
  - Finance and growth quote different customer values because one counts gross order revenue and the other nets refunds and cost.
  - Young and old customer cohorts are compared at different tenure and look better or worse for the wrong reason.
description: Compute realised revenue, cost and margin per customer and tenure period under the user's approved rules, roll them up by acquisition cohort as cumulative value, and tie the totals back to source revenue with every order and refund accounted for.
pitch: One reproducible, cohort-by-tenure customer value built on net revenue and margin, with refunds, unknown cost and unreached months shown honestly.
job_category: build
area: transformation
readiness: supported
function:
  - finance
domain_objects:
  - customer
  - order
  - refund
  - cost_component
  - cohort
  - tenure_period
  - lifetime_value
  - margin
  - ltv_exception
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
  - Needs revenue events with a customer key, a date and an amount, refunds with a recorded date, and a cost source.
  - Takes cost at order grain or as an order rate; allocating pooled cost is a separate outcome.
  - Keeps each currency separate; currency conversion is a separate outcome.
  - Needs a signup date source when the cohort anchors on signup, and kept history to reproduce a past as-of result.
  - Reports realised history to an as-of date; predictive value and forecasting are separate outcomes.
  - Takes one customer key as given; customer matching and merging are separate outcomes.
  - Uses order or billed amounts as given; recognition, deferral, churn and retention are separate outcomes.
  - Stops at value by cohort and tenure; acquisition cost, payback and segmentation are separate outcomes.
related:
  - effective-dated-business-rules
  - metric-population-and-rollups
  - identity-golden-record-crosswalk
  - finance-revenue-recognition
evidence:
  features:
    - capturing-requirements
    - generating-dbt-model
    - verifying
  evals: []
---

## Prompt

Build <order_value_model>, <customer_period_model>, <cohort_value_model>, <comparability_model> and <revenue_tieout_model> from <orders_source>, <refunds_source> and <cost_source> for the customer value questions in this Intent. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only the semantics they leave open. Give every revenue event one disposition, counted or set aside with a reason, and compute its net revenue, cost and margin under the approved revenue basis, reversal treatment and cost rule. Assign each customer to the approved acquisition cohort and publish revenue, cost and margin per customer, currency and tenure period, then the same rolled up by cohort as cumulative value, with periods not yet reached empty, never zero, and a view of the periods each cohort has reached. Keep unknown cost visibly unknown, reconcile totals to the source revenue with nothing unexplained for each currency, and report realised history only, with no forecast.

## Verified by

- On a published run every revenue event has exactly one disposition, counted or set aside with its reason, and the dispositions add up to the input events and amounts, so the source revenue is reproduced with no unexplained remainder and every set-aside amount stays visible.
- Net revenue follows the approved revenue basis, and each reversal follows the approved period and as-of treatment; a reversal with no order or on a set-aside order stays visible with its reason, and one above the order amount is shown as approved, never silently lost or clamped.
- Each counted order's cost comes from the approved source and date rule with the applied cost visible; an order with no cost follows the approved rule (unknown margin or an assumed rate); an unknown margin is never shown as zero, and its revenue still counts.
- A customer period or cohort cell holding an order with unknown or assumed cost says so and is never read as a full margin, and that flag carries onto the cumulative figures built from it.
- A customer the approved anchor cannot place is in no cohort and is listed with its reason, each other customer is in exactly one cohort, and an order on a period boundary lands in exactly one period under the approved calendar and time zone.
- Each cumulative figure equals the sum of its own periods, each cohort figure equals the sum of its member customers' figures at the approved grain, which carries currency, and any per-customer average states the approved base.
- A period a cohort has not reached at the as-of date is empty, never zero, while a reached period with no activity is zero, and the two stay distinguishable; cohorts are compared only at periods they have all reached.
- Totals reconcile to the source revenue for each currency on its own, every amount being counted, set aside, reversed or a named exception, and no output sums two currencies into one figure.
- Every figure matches expected results worked out independently of the model for each agreed case, including a boundary order, a refund and an order with unknown cost; a dropped order or an unreached period shown as zero is caught.
- Where the approved rule fails a run, it names each offending input and the reason and publishes no figures.
- No column, description or output states or implies a forecast, projection, discounted or expected lifetime value, and the outcome states what the inputs cannot prove, such as orders or cost corrections recorded after the as-of date.
- Where an approved minimum cohort size or customer-level access rule applies, no published cohort figure falls below it and customer-level rows are published only to the approved audience; suppressed cells say so and are distinguishable from empty and zero.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile the revenue events (statuses, amounts, dates and time zones, customer keys, currencies, test and internal accounts), the reversals (recorded dates, links to orders, amounts above the order) and the cost source (grain, effective dates, gaps) before modelling. Use Ask first only for semantics still open, and record each decision as the user's own answer. Keep the revenue and cost rules, reason lists, time zone, as-of date and horizon editable as data where the approved requirements say so. Work out expected results for the agreed cases independently of the models before trusting them, check that totals tie to the source and that cohort figures recompute from the orders, and say which paths the example did not exercise.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which accounts count as customers (staff, test, guest or unattributed orders), which revenue events qualify (orders, order lines or subscription charges) by status, channel or type, and where does unattributed revenue go?
- If unresolved, what is revenue (gross or net of discount, with or without fees and surcharges), which amounts are pass-through (tips, taxes, shipping), which date places it in a period (order, payment or shipment), and are other currencies reported separately or set aside?
- If unresolved, which reversals reduce revenue (refunds, returns, credits, chargebacks), at line or order level, in the order's period or the issue period, how are those after the as-of date, above the order amount or with no order shown, and does a fully reversed order count?
- If unresolved, where does cost come from (per-order cost, an order rate or a percentage), which costs are included, which date selects the rate, does cost reverse on a return, and are late cost corrections restated or kept as known?
- If unresolved, what is shown for an order with no cost (unknown margin or an assumed rate), is a partly known margin published flagged incomplete, and should a run with missing, stale or incomplete inputs fail, publish flagged results or publish nothing?
- If unresolved, what anchors a customer's cohort (first qualifying order, signup or first paid order), is a period a calendar month or a fixed block, which time zone and day boundary apply, and can a later reversal move the cohort?
- If unresolved, what is the horizon, where does the as-of date come from, are orders and corrections recorded after it shown as known then or restated, when does a running period count as reached, and what base do per-customer averages use?
- If unresolved, which cuts are published (per customer, per cohort, by channel or product), who may read customer-level rows, and what minimum cohort size applies to published cohort figures?

### Guardrails

- Do not choose the revenue basis, reversal treatment, cost source, missing-cost rule, cohort anchor, period calendar, horizon or published cuts for the user, and take none from the data or common practice; the user may ask for alternatives or a recommendation.
- Never treat unknown cost as zero or fill it with a rate the user has not approved, and never present a margin over the known-cost orders as a full margin; the incomplete flag stays on every cumulative figure built from it.
- Never show a period a cohort has not reached as zero, and never compare cohorts at periods they have not all reached.
- Never drop, double count or silently net away an order or a reversal; amounts outside the counted revenue (set aside, unattributed, after the as-of date, in another currency) stay visible with their reasons.
- Never sum or net two currencies into one figure; each currency reconciles on its own, and conversion is a separate outcome.
- Never default the as-of date to the clock without approval, and never restate periods the approved rule keeps as they were known.
- Stop at realised value by cohort and tenure: do not forecast, predict or discount lifetime value, compute acquisition cost or payback, segment customers or write results back to source systems.
