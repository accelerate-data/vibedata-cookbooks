---
id: cpg-promotion-lift
title: Measure trade-promotion lift and the post-promotion dip against an explicit baseline
trigger:
  - Trade marketing reports promotion results with whatever comparison each analyst chose, and nobody can say what "without the promotion" meant for a given event.
  - A promotion's lift looks inflated or deflated because the comparison weeks held another promotion, a holiday, a stock-out or missing sales.
  - Two promotions on one account and product overlap or run back to back, and the lift is credited to both or to neither.
  - Cancelled events, events with bad dates and events with no sales history vanish from the results with no stated reason.
  - The dip after a promotion is hidden inside the lift, so lifts cannot be compared from one event to the next.
description: For each approved promotion event, compare actual sales in the event weeks with a baseline built under the user's approved method, show the method and its evidence on every row, report the post-event dip as its own figure, and give each unmeasurable event one reason or fail the run as approved.
pitch: One lift and dip figure per promotion event, with the baseline method shown and a reason for every event that cannot be measured.
job_category: build
area: transformation
readiness: supported
function:
  - revops
industry:
  - cpg
domain_objects:
  - promotion_event
  - promotion_calendar_line
  - weekly_sales
  - baseline
  - promotion_lift
  - post_promotion_dip
  - lift_exception
  - holiday_calendar
  - account
  - product
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
  - Needs weekly sales by account and product, and a promotion calendar with account, product or product group, and dates.
  - Stops at lift and dip figures; trade spend, ROI, forecasting and price elasticity are separate outcomes.
  - Applies the approved baseline method; it does not prove causal incrementality.
  - Sales and calendar tables already in the Domain; exported files go to file-drop-to-bronze first.
related:
  - master-product-sku-hierarchy
  - effective-dated-business-rules
  - metric-population-and-rollups
evidence:
  features:
    - capturing-requirements
    - generating-dbt-model
    - verifying
  evals: []
---

## Prompt

Build <lift_model>, carrying measured and listed events, and <coverage_model> from <promotion_calendar_source> and <weekly_sales_source>. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only the semantics they leave open. For each approved promotion event at the approved result grain, measure actual sales in the approved measure over the event weeks against a baseline built under the approved method, weeks and minimum evidence, publish the baseline, the lift in that measure and as a percentage, the method name and the evidence it used, report the post-event dip as its own figure, and, in a published run, list every event that cannot be measured with exactly one reason. Keep sources read-only and state what the inputs cannot prove.

## Verified by

- In a published run every calendar key is in scope, measured or listed with one reason (events the overlap rule combines count as one), or shown as outside scope with its reason; rows equal the in-scope keys, and repeated calendar lines stay visible with a count.
- Each measured row shows actual sales and the baseline in the approved measure, the lift as a difference and as a percentage on the approved basis, the method name and the evidence used; published figures equal values derived independently from the source records and approved rules.
- A baseline never reads the promoted account and product's own sales from the event's weeks, or a week the approved rule excludes, such as another promotion, a post-promotion tail, a holiday or unusable sales; the weeks or accounts used and the weeks excluded, with reasons, can be listed for any row.
- Where a minimum amount of evidence is approved, an event whose baseline would rest on less is listed, not measured, unless an approved fallback applies and the method name shows it; an event with exactly the minimum is measured.
- A zero baseline is handled as approved and never shows an infinite or invented percentage; a negative lift is shown as negative unless the user approved another treatment, which the output states.
- Overlapping events on one account and product follow the approved overlap rule and name the other events; a lift is attributed to overlapping events only as that rule says and is never counted twice in any total.
- The approved status rule decides which promotions ran: one that did not run changes no other event's baseline or weeks; a placed one that ran follows the approved clean-week and overlap rules even if itself listed, and an unplaceable one that ran has its neighbours handled as approved and shown.
- The post-event dip is its own figure over the approved length, read against the baseline and equal to an independent derivation; any net-of-dip lift is a separate labelled figure, and a dip the data cannot support is shown as approved with its reason.
- A week with no row, or a duplicated, negative or null one, is never silently turned into zero, summed or picked: it is treated as approved and the treatment is shown; where it is unknown it leaves the baseline, and an event week with one is handled as approved.
- In a published run each unmeasurable event is listed with the first approved reason that applies under its documented precedence; none is dropped or both measured and listed. A failed run names the offending records and publishes no partial figures.
- Actual sales on measured rows equal the source values over the event weeks under the approved partial-week rule, and every input sales row is accounted for as used, set aside by cause or outside every event and baseline, with counts and totals that close.
- Every output is unique on its declared grain, and the outcome states what the inputs cannot prove, such as price changes, distribution gains and stock-outs the data does not carry.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile the promotion calendar and the weekly sales first: keys, grains, week boundaries, units, repeated calendar lines, duplicated weeks, negative or null values and the span the sales cover. Use Ask first only for semantics still open, and record each answer as the user's own decision. Keep the baseline window, minimum evidence, post-promotion length, holiday list, status flags, reason codes and their precedence as editable data where the approved requirements say so. Make the published lift and coverage outputs agree about every event and every input sales row. Prove each stated behaviour on the source records, including boundary and exceptional cases such as exactly the minimum evidence where one is approved, a promotion in another event's look-back, overlapping events and a missing week, with expected results derived independently of the models. State what the inputs cannot prove.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which events are in scope: which statuses are measurable and which count as having run, which mechanics, accounts and products are in or exempt, and how bundle or group-level calendar lines map to promoted products.
- If unresolved, what the baseline is: the method (the pair's own recent weeks, the same weeks a year earlier, matched non-promoted accounts or another), look-back, gap before the event, minimum evidence, and any fallback for thin history.
- If unresolved, which weeks may enter a baseline: exclusions for other promotions, post-promotion tails, holidays and seasonal peaks, stock-outs, price or distribution changes where the Domain holds them, and whether a week with no row means no sales or unknown.
- If unresolved, what is measured and how lift is expressed: sell-out or shipments, source grain and roll-up to account, product and week (what counts as a duplicate), units, volume or value, unit and currency conversion and precision, returns and negative weeks, percentage basis and rounding.
- If unresolved, how weeks and windows are defined: week start or each retailer's fiscal calendar, lead or lag between event dates and measured weeks, partial weeks (whole, prorated, excluded), and the result grain (event, account and product, or event total).
- If unresolved, how neighbouring promotions are treated: events sharing weeks on one account and product (set aside, split or combined), promotions that ran just before, and whether other products' weeks are flagged; cannibalisation itself stays unproven.
- If unresolved, how the dip is handled: its length, whether a net-of-dip lift is also published, and how a dip inside another promotion or past the data is shown.
- If unresolved, how exceptions are handled: unknown accounts or products, unusable dates, disagreeing calendar lines, their effect on neighbours, zero baseline, negative lift, reasons and precedence, restatement, and whether an unmeasurable event fails the run or stays listed.

### Guardrails

- Do not choose the baseline method, window, minimum evidence, clean-week rule, overlap rule, dip rule, population or measure for the user, and take none from the data or common practice; the user may ask for alternatives or a recommendation.
- Never silently turn a missing, duplicated, negative or null week into zero, sum duplicates or pick one; treat each as approved and show the treatment.
- Never let the promoted account and product's own sales from the event's weeks, or a week the approved rule excludes, enter a baseline.
- Never count one lift twice across overlapping events, and never hide a promotion that ran because it was not itself measured or placed.
- Never fold the dip into the lift, floor a negative lift or invent a percentage for a zero baseline unless the user approved it and the output says so.
- Never drop, double count or default an unplaceable event or sales record; in a published run each is measured, listed with its reason, or set aside by cause with counts.
- Never present lift as proof of causal incrementality; effects of price changes, distribution gains, stock-outs and cannibalisation that the data cannot show are stated as unproven.
- Stop at lift and dip figures: do not compute trade spend, ROI, forecasts or elasticity, do not plan promotions, and keep sources read-only.
