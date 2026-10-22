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
  - channel
  - campaign
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
  - Needs dated cost lines, acquisition assignments, first-customer dates and contribution records.
  - Takes contribution, assignments and customer identity as given; the rules may be captured as editable data.
  - Keeps each currency separate unless an approved translation rule applies; rate sourcing is separate.
  - Reports attribution-based accounting to an as-of date; causal lift and forecasting are separate.
  - Stops at cohort cost and payback; touchpoint credit and lifetime value are separate outcomes.
related:
  - marketing-attribution-models
  - customer-historical-ltv
  - effective-dated-business-rules
  - identity-golden-record-crosswalk
  - shared-fx-conversion
evidence:
  features:
    - capturing-requirements
    - generating-dbt-model
    - verifying
  evals: []
---

## Prompt

Build <cost_allocation_model>, <cohort_payback_model>, <cohort_series_model>, <coverage_model> and <exceptions_model> from <cost_source>, <assignment_source>, <customer_source> and <contribution_source> for the acquisition payback questions in this Intent. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only the semantics they leave open. Account for every cost line as allocated shares that add back to it or carry it unallocated with a reason, divide any shared cost once, place each customer under the approved assignment rule, and show customers with no qualifying assignment under the approved treatment. Publish per cohort and channel the fully loaded cost, customers acquired, cumulative contribution by approved period since acquisition and a payback verdict under the approved threshold and rule, with periods not yet reached empty, never zero, and reconcile allocated and unallocated cost to the cost inputs. Report attribution-based accounting only: no causal claim, no touchpoint credit, no forecast.

## Verified by

- Every cost line is accounted for as allocated shares that add back to the line, or carried unallocated or forward as the approved rule says, each with a reason; allocated plus unallocated plus carried forward equals the inputs per input month, cost type and currency, with any difference shown.
- A shared cost line is divided once under the approved basis, its shares add back to the line plus any amount the approved rule leaves unallocated, and no shared amount reaches two cells.
- Each customer is placed under the approved assignment rule, once or by approved shares that add to one customer; a reassigned customer is never counted twice, and cohort counts equal the customers in scope.
- Customers with no qualifying assignment follow the approved treatment, each counted once, and are never silently added to a paid channel's customers or cost.
- Each cell shows fully loaded cost, customers acquired and cumulative contribution by approved period since acquisition; each cumulative figure equals the sum of its periods, and the payback verdict follows the approved threshold and rule.
- A refund lands in the period the approved rule gives it; one after payback can delay or reverse the verdict, and a first crossing and a sustained payback stay distinguishable where the approved rule keeps both.
- A cohort in the approved window that never covered its cost reads not yet recovered with its periods observed; one past it without covering cost reads the approved verdict and shortfall; one that covered then fell back follows the refund rule; none reads zero, and unreached periods are empty.
- A paid cell with customers and no allocated cost reads as the approved treatment with a stated reason, never as paid back at the first period; a total row is recomputed from its own sums under its stated inclusion rule.
- A period with no cost and no acquisition produces no cohort row and appears in coverage; every input row is used or listed once with its reason, and a null or malformed amount is listed, never read as zero.
- Results equal values worked out independently of the model for each applicable agreed case, including a cohort exactly at the threshold, a refund after payback and a shared cost line; an inapplicable case is stated as such.
- Cost, contribution and ratios reconcile per currency, and mixed currencies read as translated under the approved rate rule or unverified, never as a ratio across currencies; totals hold before any suppression, which follows the approved hiding rule.
- Where the approved rule fails a run it names each offending input and publishes no figures, or flags figures incomplete; no output states causation, touchpoint credit or a forecast, and it states what the inputs cannot prove.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile the cost lines (types, periods, channels, shared lines, credits, unmapped lines), the assignments (approval status, effective dates, reassignments, concurrent records), the first-customer dates and the contribution records (periods before acquisition, refunds, currencies, null amounts) before modelling. Use Ask first only for semantics still open, and record each decision as the user's own answer. Keep the threshold, window, as-of date and reason lists editable as data where the approved requirements say so. Work out expected results for the agreed cases independently of the models before trusting them, check that cost reconciles to the inputs and that cohort figures recompute from the records, and say which paths the example did not exercise.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which cost lines count in fully loaded cost (media, agency, creative, shared, overhead, credits, rebates, taxes, backdated corrections, spend with no campaign key), which period each lands in, and where does cost with no acquired customer go (unallocated, carried forward or spread)?
- If unresolved, how is a shared cost line divided (by spend, customers acquired, evenly or left unallocated), which key links a cost line to an assignment's campaign or channel, which channels are paid, and what do unmapped lines become?
- If unresolved, which date anchors a customer's cohort (first order, signup or first paid), is the period a calendar month, a week or a fixed block, and which customers count (staff, test, those after the as-of)?
- If unresolved, which assignment record places a customer (approved only, effective-dated, as known or as of the run), how are rejected, superseded, reassigned, concurrent and tied records placed (one placement or approved shares), and is a customer with none organic, excluded or spread?
- If unresolved, what is contribution (revenue, gross margin or after variable cost), do refunds reduce the period they are recorded or the original one, and how are records before acquisition, beyond the window, after the as-of or null shown?
- If unresolved, what threshold counts as payback (a multiple of cost, at or above), does a later refund undo it, what window applies, when does a running period count as reached, and what do a no-cost cohort and a cohort past the window without recovery read as?
- If unresolved, what is the reporting basis: the currency and rate source or per-currency reporting, the time zone and day boundary for every date, and where does the as-of date come from?
- If unresolved, which rows are published (per channel, a paid total, a total with organic), who may read the table, what minimum cohort size and complementary hiding apply, and should a run with missing, stale or incomplete inputs fail, publish flagged results or publish nothing?

### Guardrails

- Do not choose the cost scope, shared-cost basis, link keys, cohort anchor, assignment rule, organic treatment, refund timing, payback rule, reporting basis or published rows for the user, or take them from the data or common practice; the user may ask for alternatives or a recommendation.
- Never count a shared cost line in two cells beyond its approved shares, spread cost to customers the approved rule does not assign, or let a reassigned customer count twice.
- Never show an uncovered cohort inside the window as zero or failed, never present one past the window as still open, and never fill unreached periods or a payback by extrapolation.
- Never read a cell with no allocated cost as recovered unless the approved treatment says so and labels it.
- Never let organic customers or contribution without cost improve a paid payback figure unless the approved rule says so and labels it.
- Never drop, double count or silently net away a cost line, customer, contribution record or refund; amounts left out stay visible with their reasons.
- Never sum or net two currencies into one figure unless an approved translation rule and rate source say so; otherwise each currency reconciles on its own.
- Never default the as-of date to the clock without approval, and never restate periods the approved rule keeps as known.
- Stop at cohort cost and payback: do not assign touchpoint credit, rebuild customer lifetime value (contribution is taken as given), claim causal or incremental effect, forecast, or recommend budget.
