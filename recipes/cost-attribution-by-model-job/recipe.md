---
id: cost-attribution-by-model-job
title: Attribute warehouse spend to the models and job runs behind it, keeping idle and untied cost visible
trigger:
  - The warehouse bill keeps growing and nobody can say which models or jobs are behind it.
  - Billed time that nobody used, or work nobody can tie to a model or job, is spread across whoever ran last or dropped.
  - Concurrent queries are each charged their full time, so the shares add up to more than the bill.
  - Failed, cancelled, retried and re-sent log rows change the answer and nobody can explain how.
description: Within each billed interval, share the billed cost among the queries that ran in it under an approved driver, publish it by model and by job run, keep idle and untied cost visible with reasons, and close attributed, idle and unattributed to each bill within the approved tolerance.
pitch: Show which models and job runs drive the warehouse bill, with idle and untied cost visible and each interval closing to its bill as approved.
job_category: explain
area: governance-cost
readiness: supported
function:
  - it-finops
domain_objects:
  - warehouse_bill_interval
  - query_log_entry
  - model
  - job_run
  - cost_attribution
  - idle_cost
  - unattributed_cost
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
  - Billed cost per interval and the query log arrive as landed tables; landing either is a separate outcome.
  - Stops at attribution; query tuning, budgets, forecasts and chargeback are separate outcomes.
  - Cost follows the model and job tags the log carries; a wrong but valid tag is not detectable.
  - Allocating the whole cloud bill to teams and tags is a separate outcome.
related:
  - finops-cloud-allocation
  - finops-saas-license-utilization
  - source-freshness-sla
  - file-drop-to-bronze
  - database-tables-to-bronze
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

Build <attribution_model>, <unattributed_model> and <coverage_model> from <metering_source>, <query_log_source> and, where recorded or approved, <model_register_source> and <job_register_source>. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only those they leave open. Within each billed interval, share its billed cost among the queries that ran in it under the approved driver and concurrency rule, with a query that spans intervals placed as approved, publish the result by model and by job run at the approved grain, keep billed time no query used visible as idle under the approved treatment, keep work that no model or job run can be tied to visible as unattributed with its reason, account for every log row as counted or set aside with its reason and every billed interval as attributed, idle or unattributed, so that attributed, idle and unattributed cost add back to each interval's bill at the approved precision. Materialize the outputs in the Intent's sandbox and verify them against independent expectations.

## Verified by

- Per billed interval and in each published split, attributed plus idle plus unattributed cost equals the bill within the approved tolerance, or the gap is shown with its amount and reason, or the run fails naming the interval; none is plugged, and window totals follow the same rule.
- Every log row is counted or set aside with one approved reason (such as duplicate, superseded, unreadable, out of scope or no bill interval); counts tie to the input, and a set-aside row carries no cost into any interval.
- A query that spans intervals or runs alongside others is charged under the approved concurrency and interval rule; attributed cost never exceeds the interval's bill and idle cost is never negative.
- Billed time no query used is shown as idle, a wholly idle interval included, under the approved treatment; it reaches models or job runs only as a separate labelled share if approved.
- Work with a missing or unknown model, job run or warehouse stays visible with one reason, in the split or splits the approved rule names, and is never silently spread or dropped; an approved share is a separate labelled share.
- Failed, cancelled and retried queries follow the approved treatment and show their status where attributed; a re-sent row follows the approved duplicate and revision rule with earlier revisions visible, and no query's time is charged twice.
- A row with an unreadable time, a missing end, an end before its start or a still-running state is set aside with its raw values or fails the run naming it, as approved; none is coerced to a default.
- A changed approved rule value (driver, reason set, treatment) changes the output where the data reaches it, within the approved rule form.
- Each published split foots to the same bill on its own; a model's cost and a job run's cost are never added together as if each landed once.
- Published results equal values derived independently from the sources and approved rules, including how split cents are assigned.
- A late log row or a restated bill changes a past interval only as the approved rule says; where the source gives no approved revision signal, restatement is stated as unproven.
- The outcome states what the inputs cannot prove, such as cost with no log row, uncharged system work or a wrong but valid tag, and shows user names and query text only at the approved audience and grain.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile the metering rows (interval length, billed time and cost, currency) and the query log (start and end times, status, warehouse, model and job run references, duplicates, re-sends, unreadable and open-ended rows) before proposing rules. Use Ask first only for semantics still open, and record each decision as the user's own answer. Keep the reason vocabulary, status treatment, registers and thresholds as data a reader can change. Fix expected results independently before model SQL, with one named case for each concurrent overlap, interval-spanning query, failed, cancelled, exact duplicate, differing re-send, missing and unknown model or job run, unknown warehouse, unbilled interval, wholly idle and partly idle interval, and each kind of unreadable row, and compute shares and cents in a separate script. Build the attribution, the unattributed detail and the coverage using composed skills and current target dialect and sandbox guidance. Materialize, read back and rerun, compare every output row with the expectations, and show that a changed rule value moves the output. Keep the Domain read-only. Report untested cases as incomplete verification.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, the warehouses or capacities, window and cost measure (billed, net of credits), billing interval and time zone, the currency and any approved rate source, which log fields name a model and a job run, and which keys link a log row to a bill interval, model and job run.
- If unresolved, the attribution driver (elapsed time, data scanned, compute-seconds), how concurrent queries share a moment, and whether a query spanning intervals is split by overlap or charged to its start.
- If unresolved, how idle time and any billing minimum or resume tail are treated: shown as idle, or shared to models and job runs as a separate labelled share, and on what basis.
- If unresolved, which query classes count (system, metadata, ad hoc, dashboard), which are attributed to a model or job run, and where the rest go.
- If unresolved, what counts as work that cannot be tied to a model or job run and the reason each carries, whether a query missing one reference is unattributed in one split or both, and whether untied cost stays unattributed or is shared as a labelled share.
- If unresolved, how failed, cancelled, retried and still-running queries are treated, and how exact duplicates and differing re-sends are recognised, and which revision governs.
- If unresolved, whether an unreadable time or cost, or a missing or negative duration, is set aside with the raw values or fails the run, and whether late log rows or restated bills restate past intervals.
- If unresolved, the published grain, the gap tolerance and rounding rule for split cents, who may see user names and query text, and whether a gap is published and flagged or fails the run.

### Guardrails

- Do not spread idle or unattributed cost over models or job runs, or give it to a default owner, without approval; it stays visible with its reason.
- Do not charge a concurrent or interval-spanning query its full measure in each place it overlaps, or attribute more cost to an interval than it was billed for.
- Do not drop or net failed, cancelled, duplicate, superseded or unreadable rows; they stay visible with their reason, and only the governing row of a query carries cost.
- Do not coerce an unreadable time or cost to a default or invent a missing end.
- Do not force attributed, idle and unattributed cost to equal a bill by dropping, plugging or netting; every gap stays an exception with its amount and reason.
- Do not sum or convert across currencies without an approved rate source, date and type.
- Do not read a model or job tag as proof of who caused the work, or present a synthetic log as real spend.
- Do not show user names or query text below the approved audience and grain.
