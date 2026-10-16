---
id: finance-revenue-recognition
title: Generate the revenue-recognition schedule and deferred-revenue roll-forward from contracts
trigger:
  - Revenue is spread across months by hand in a spreadsheet and never agrees with the deferred revenue balance or with what was invoiced.
  - Every month-end someone rebuilds the deferred revenue roll-forward and cannot explain its movement contract by contract.
  - An auditor asks how much of a contract was recognised in each period and why, including after it was upsold, repriced or cancelled part way through.
description: Schedule each contract line's allocated price by period under the approved recognition rules, net billing against it into deferred revenue or the approved asset or receivable at the approved netting level, roll the positions forward at the approved grain, and keep every unprocessable contract or billing line visible, so no amount is lost, counted twice or recognised early.
pitch: Turn contracts and invoices into a revenue schedule and a deferred-revenue roll-forward that tie to each other and to every invoice line.
job_category: build
area: transformation
readiness: supported
function:
  - finance
domain_objects:
  - contract
  - contract_line
  - performance_obligation
  - billing_line
  - revenue_schedule
  - deferred_revenue
  - contract_asset
  - revenue_exception
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
  - Needs contract lines carrying their allocated price and dated terms; price allocation is a separate outcome.
  - Treats each contract line as one performance obligation; combining lines into one obligation is a separate outcome.
  - On business dates alone, a backdated change restates earlier periods; reproducing them needs kept history.
  - Stops at the schedule and roll-forward; journal postings, period locking and translation are separate.
related:
  - finance-ar-aging-dso
  - finance-gl-subledger-tieout
  - effective-dated-business-rules
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

Build <revenue_schedule_model>, <contract_position_model>, <deferred_revenue_rollforward_model>, <revenue_exceptions_model> and <revenue_completeness_model> from <contracts_source>, <contract_lines_source> and <billing_lines_source> for <as_of_date>. Inherit the semantics the approved requirements establish and resolve only those left open. Schedule each in-scope contract line's allocated price across the approved periods under the approved method, proration and rounding, apply modifications and cancellations as approved, and mark each period recognised (on or before the as-of) or scheduled, treating a period the as-of splits as approved. Net in-scope billing against recognised revenue into each contract's position at the approved netting level, as deferred revenue or the approved asset or receivable, and roll positions forward per period at the approved grain (entity and currency where more than one is in scope) with opening, billed, recognised and closing. List every contract line and billing line that cannot be processed, or fail the run naming it, as approved, and account for every source record and amount. Keep sources read-only and report what the inputs cannot prove.

## Verified by

- On a completed run, each in-scope line's periods sum exactly to its governing price, except a line stopped by approved modification rules (what it recognised) and an undelivered point-in-time line (what the approved rule shows); no period is negative unless the approved rules allow it.
- An undelivered point-in-time line shows its unrecognised price as the approved rule for undelivered lines says, and recognises nothing until delivered.
- Each period's amount follows the approved method, proration basis and rounding, including lines starting or ending mid-period, leap-year periods and prices that do not divide evenly, independently recomputed from the line's dates and price.
- A modification or cancellation changes the schedule only as the approved policy says; under a prospective policy, amounts for service days before its effective date are identical with and without it.
- A point-in-time line recognises only on the approved delivery evidence on or before the as-of, and any amount billed for it before then is not recognised until delivery.
- Revenue follows the allocated price, not the invoices; a billed total that differs from the price is shown as the approved policy says, at the approved netting level, and changes revenue only through an approved price change on the line.
- On a completed run, in every rolled-forward period at the approved grain, opening plus billed minus recognised equals closing exactly, closing balances equal the positive and negative positions under the approved netting and classification, and amounts shown apart as approved stay in the identity.
- Roll-forward totals trace to the positions, the recognised periods and the in-scope billing; an opening position not derived from the sources names its source and any difference from the schedule is listed; entities and currencies are never netted.
- A billing line counts as billed from its approved billing date, and billing for service after the as-of is shown as the approved policy says; nothing dated after the as-of on that basis changes any reported figure.
- On a completed run, every source contract, line version and billing line lands once, in scope, out of scope with its reason, or an exception with its reasons under the approved grain; counts and known amounts add up to the source, and missing amounts are counted, never shown as zero unless approved.
- Where the approved policy fails the run on an unprocessable record, the run fails explicitly and names each offending record with its reason.
- The outcome states which exceptions remain open and what the inputs cannot prove, such as whether a backdated change restates earlier periods.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile the contracts, contract lines and their versions (types, service and delivery dates, effective dates, prices, entities, currencies, statuses) and the billing lines (dates, amounts, credit memos, which line each bills), and check that each line carries an allocated price and that versions can be ordered by effective date; where versions are not kept, schedule only what the kept versions prove, list lines whose terms may have changed as exceptions or stop, and report modification treatment as unproven. Use Ask first only for semantics still open, and record each decision as the user's own answer. Keep recognition methods, eligible statuses and line types, and the as-of date editable data, not literals. Recompute the expected schedule and roll-forward independently of the models before trusting them. The schedule, contract positions, roll-forward, exceptions and completeness must never disagree about a record or an amount. Report every exception left open and what the inputs cannot prove.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which contract statuses, line types (such as pass-through taxes or amounts collected as agent), entities and currencies are in scope, and at what grain the roll-forward is reported?
- If unresolved, which recognition method applies to each line type (over the service period, at a point in time, or another approved pattern), what evidence marks delivery, and what an undelivered line shows?
- If unresolved, how a period's share is computed (by days, by whole periods or another convention), whether service dates are inclusive, how amounts are rounded so a line sums exactly, and whether periods are calendar or fiscal?
- If unresolved, how a contract modification or cancellation is applied (prospectively from its effective date, by catch-up, or as a separate contract), and what happens when a revised price falls below what is already recognised or a point-in-time line is repriced after delivery?
- If unresolved, which date places a billing line in a period, and is billing for future service that is not yet due or paid recorded as billed?
- If unresolved, at what level billing nets against recognition, is revenue recognised ahead of billing a contract asset or an unbilled receivable, how is billing above the price or a credit memo shown, and where do opening positions for contracts older than the sources come from?
- If unresolved, which records cannot be processed, one row per reason or one primary reason, how a contract, line version or billing line delivered twice is treated, and whether an unprocessable record is excluded with a visible count or fails the run?
- If unresolved, which as-of dates are reported, whether they must be period ends, and how a period an as-of splits is treated?

### Guardrails

- Do not choose the recognition method, proration, rounding, modification treatment, netting level, classification of positions or exception handling for the user, and take none from the data or common practice; the user may ask for alternatives or a recommendation.
- Never recognise from invoices, cash or bookings instead of the allocated price, and never derive an allocation; a line without one is unprocessable under the approved policy, and if no line carries one, stop and say so.
- Never restate a period the approved modification policy leaves untouched, and never book negative revenue unless the approved rules allow it.
- Never net or translate distinct legal entities or currencies together.
- Never drop or double count a record or an amount; every contract line and billing line that cannot be processed stays visible, as an exception or in an explicit run failure, with its reason.
- Never default a missing price, amount or date to zero or to another date unless the approved semantics say so.
- Stop at the schedule and roll-forward: do not post journals, lock periods or change the source contracts or invoices.
