---
id: marketing-acquisition-cost-payback
title: Build fully loaded acquisition cost and contribution payback by customer cohort
trigger:
  - Marketing says a channel pays back quickly and Finance says it never does, and nobody can show the sum from the spend and contribution records.
  - Shared campaign cost, agency and creative fees are counted in two channels or left out, so acquisition cost differs between reports.
  - A customer reassigned between campaigns, or a refund after payback, changes the answer and nobody can say whether the cohort has really recovered its cost.
description: Compute fully loaded acquisition cost, customers acquired and cumulative contribution by acquisition cohort and channel under the user's approved rules, with a payback verdict per cohort and every cost and customer accounted for.
pitch: One reproducible cohort table that shows what each channel cost, what it has earned back and whether it has paid back, with shared cost counted once.
job_category: build
area: transformation
readiness: supported
function:
  - finance
  - revops
domain_objects:
  - acquisition_cost
  - cost_allocation
  - acquisition_assignment
  - customer
  - cohort
  - contribution
  - refund
  - payback_verdict
  - cost_exception
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
  - Needs dated cost lines, acquisition assignments, first-customer dates and contribution records.
  - Takes contribution and assignments as given; the rules may be captured as editable data.
  - Keeps each currency separate; currency conversion is a separate outcome.
  - Reports attribution-based accounting to an as-of date; causal lift and forecasting are separate.
  - Stops at cohort cost and payback; touchpoint credit and lifetime value are separate outcomes.
related:
  - marketing-attribution-models
  - customer-historical-ltv
  - effective-dated-business-rules
  - identity-golden-record-crosswalk
evidence:
  features:
    - capturing-requirements
    - generating-dbt-model
    - verifying
  evals: []
---

## Prompt

Build <cost_allocation_model>, <cohort_payback_model>, <cohort_series_model>, <coverage_model> and <exceptions_model> from <cost_source>, <assignment_source>, <customer_source> and <contribution_source> for the acquisition payback questions in this Intent. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only the semantics they leave open. Allocate every cost line to one cohort cell or carry it unallocated with a reason, split any shared cost once, place each customer in one cohort and one channel under the approved assignment rule, and show customers with no qualifying assignment under the approved treatment. Publish per cohort and channel the fully loaded cost, customers acquired, cumulative contribution by month since acquisition and a payback verdict under the approved threshold and rule, with months not yet reached empty, never zero, and reconcile allocated and unallocated cost to the cost inputs. Report attribution-based accounting only: no causal claim, no touchpoint credit, no forecast.

## Verified by

- Every cost line is allocated to one cohort cell or carried unallocated with one reason, and allocated plus unallocated cost equals the cost inputs per month, per cost type and in total, with any difference shown, never hidden.
- A shared cost line is split once under the approved basis, its shares add back to the line plus any amount the approved rule leaves unallocated, and no shared amount reaches two cells.
- Each customer counts in one cohort and one channel under the approved assignment rule, a reassigned customer counts once, and cohort customer counts equal the customers in scope with a first-customer date.
- Customers with no qualifying assignment follow the approved treatment, each counted once, and are never silently added to a paid channel's customers or cost.
- Each cell shows fully loaded cost, customers acquired and cumulative contribution by month since acquisition, each cumulative figure equals the sum of its months, and the payback verdict follows the approved threshold and crossing rule.
- A refund lands in the month the approved rule gives it, a refund after payback can delay or reverse the verdict, and a first crossing and a sustained payback stay distinguishable where the approved rule keeps both.
- A cohort that has not covered its cost and has not reached the approved window reads not yet recovered with the months observed, never zero, failed or recovered by extrapolation; unreached months are empty and a reached month with no activity is zero.
- A paid cell with customers and no allocated cost reads as the approved treatment with a stated reason, never as paid back at the first month; a total row is recomputed from its own sums under its stated inclusion rule.
- A month with no cost and no acquisition produces no cohort row and appears in coverage, and every input row is used in the answer or listed once with its reason.
- Cost, customers, cumulative contribution and verdicts match values worked out independently of the model for each agreed case, including a cohort exactly at the threshold, a refund after payback and a shared cost line.
- Where the approved rule fails a run, it names each offending input and the reason and publishes no figures; where it flags instead, flagged figures are marked incomplete.
- No column or description states or implies causation, incrementality, touchpoint credit or a forecast, and the outcome states what the inputs cannot prove, such as corrections recorded after the as-of date.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile the cost lines (types, months, channels, shared lines, unknown channels), the assignments (approval status, effective dates, reassignments), the first-customer dates and the contribution records (months before acquisition, refunds, currencies) before modelling. Use Ask first only for semantics still open, and record each decision as the user's own answer. Keep the threshold, window, as-of date and reason lists editable as data where the approved requirements say so. Work out expected results for the agreed cases independently of the models before trusting them, check that cost reconciles to the inputs and that cohort figures recompute from the records, and say which paths the example did not exercise.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which cost types make up fully loaded cost (media, agency, creative, shared, overhead), which period each lands in (spend month, lagged or per campaign), and where does cost with no acquired customer go (unallocated, carried forward or spread)?
- If unresolved, how is a shared cost line divided across channels or campaigns (by media spend, customers acquired, evenly or left unallocated), and what happens when no basis exists?
- If unresolved, which date anchors a customer's cohort (first order, signup or first paid), is the period a calendar month or a fixed block, and which customers count (staff, test, those after the as-of)?
- If unresolved, which record links a customer to a campaign or channel (approved only, effective-dated, as known or as of the run), how are rejected, superseded and reassigned records treated, and is a customer with none organic, excluded or spread?
- If unresolved, what is contribution (revenue, gross margin or after variable cost), do refunds reduce the month they are recorded or the original month, and how are records before acquisition, beyond the window or after the as-of shown?
- If unresolved, what threshold counts as payback (a multiple of cost, at or above), does a later refund undo it, what window applies, when does a running month count as reached, and what does a cohort with customers but no cost read as?
- If unresolved, which rows are published (per channel, a paid total, a total with organic), what does a total include, and who may read the table, with what minimum cohort size?
- If unresolved, where does the as-of date come from, and should a run with missing, stale or incomplete inputs fail, publish flagged results or publish nothing?

### Guardrails

- Do not choose the cost scope, shared-cost basis, cohort anchor, assignment rule, organic treatment, refund timing, payback threshold or window, or published rows for the user, and take none from the data or common practice; the user may ask for alternatives or a recommendation.
- Never count a shared cost line in two cells, spread cost to customers the approved rule does not assign, or let a reassigned customer count twice.
- Never show an uncovered cohort that has not reached the window as zero or failed, and never fill unreached months or a payback by extrapolation.
- Never read a cell with no allocated cost as recovered, and never let organic customers or contribution without cost improve a paid payback figure unless the approved rule says so and labels it.
- Never drop, double count or silently net away a cost line, customer, contribution record or refund; amounts left out stay visible with their reasons.
- Never sum or net two currencies into one figure; each currency reconciles on its own.
- Never default the as-of date to the clock without approval, and never restate periods the approved rule keeps as known.
- Stop at cohort cost and payback: do not assign touchpoint credit, rebuild customer lifetime value, claim causal or incremental effect, forecast, or recommend budget.
