---
id: marketing-campaign-budget-pacing
title: Build a campaign-day budget pacing ledger against versioned flight plans
trigger:
  - Campaign owners ask whether a campaign is on pace and the answer changes with which budget version and which cost number someone used.
  - A mid-flight budget change rewrote last month's plan, so nobody can show what was approved at the time.
  - Platform spend is restated after the day and billed credits arrive late, and marketing finance cannot tell provisional cost from settled cost.
description: Build a campaign-day plan and actual ledger as of each approved reporting cutoff, with the approved budget revision at that cutoff, provisional and settled cost kept apart, remaining budget and eligible delivery days left, and campaign totals that reconcile to the portfolio at every cutoff.
pitch: A point-in-time pacing ledger where earlier plans never change and every cost, credit and set-aside reconciles to the portfolio.
job_category: build
area: transformation
readiness: supported
function:
  - finance
domain_objects:
  - campaign
  - flight
  - budget_revision
  - pause
  - platform_spend
  - billed_adjustment
  - reporting_cutoff
  - pacing_ledger
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
  - Flights, revisions, spend and bills arrive as landed tables; ingesting them is a separate outcome.
  - Needs a recorded time on each revision, pause, restatement, bill and adjustment; past knowledge is never rebuilt.
  - Reporting only; bid changes, forecasts and acquisition payback are separate outcomes.
related:
  - finance-budget-forecast-actual
  - bitemporal-business-history
  - effective-dated-business-rules
  - dbt-snapshot-history
  - marketing-attribution-models
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

Build <campaign_day_ledger_model>, <campaign_totals_model>, <portfolio_totals_model>, <credit_audit_model> and <coverage_model> from <flight_source>, <budget_revision_source>, <pause_source>, <platform_spend_source>, <billed_line_source>, <adjustment_source> and <reporting_cutoffs>. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only the semantics they leave open. For each campaign, flight day and reporting cutoff, read every input as known at that cutoff, take the budget revision the approved rules select, pace it over the approved eligible delivery days, and show the day's cost on one approved basis, provisional or settled, with approved credits applied once. Publish remaining budget and eligible days left, totals per campaign and per portfolio that reconcile at every cutoff, and every input counted or set aside with its reason. Keep sources read-only, change no bid or budget, forecast nothing, and report what the inputs cannot prove.

## Verified by

- At each cutoff the plan in force is the revision the approved as-of rule selects, and a later revision changes only later cutoffs: an earlier cutoff's plan, paced amounts and remaining budget match the expected values for that cutoff, never the latest plan.
- Every revision, pause, restatement, bill and adjustment enters a cutoff only when the approved rule says it was known there, and an input that arrives later never changes an earlier cutoff's rows, whichever of plan and cost the approved rule freezes.
- Paced amounts follow the approved spreading and rounding rule and sum to the plan in force across the approved eligible days, plus any approved residue; a paused day's planned amount and eligibility follow the approved pause rule.
- Eligible delivery days left at each row equal the count of approved eligible days after it, as known at the cutoff, and a pause recorded later never changes an earlier cutoff's counts or plan.
- Each campaign day carries exactly one approved cost basis, and a settled day's cost comes from the approved settled source, never added to the provisional cost of the same day; the same day can be provisional at one cutoff and settled at a later one.
- Where a platform restates a day, the restatement the approved rule selects replaces the earlier ones rather than adding to them, and a day with no reported cost shows the approved state, never a silent zero.
- A credit or adjustment lands once on its approved basis: one that appears in several sources moves cost by one amount, and one with no approved backing, unmatched or outside the flight moves no cost and is handled as the approved exception policy says.
- Remaining budget equals the plan in force less cumulative cost on each day's own basis, shown as the approved rules say where no plan applies or spend exceeds the plan, never clipped or shown as a clean zero.
- Campaign totals add to the portfolio total for plan and cost at every cutoff, recomputed from the sources; any campaign without an approved plan appears in the difference as the approved rules say, never dropped from cost.
- On a run that completes, every input record is counted in the ledger or set aside with one approved reason, the counts add up per check, and an input that cannot be placed is listed rather than lost; a run the policy fails names each offending input.
- Published results equal values derived independently from the sources and approved rules for several cutoffs, covering one before a flight starts, one inside a pause, and one after a bill and a late credit.
- Each output is unique on its declared grain, a rerun on unchanged inputs gives identical results, and the outcome states what the inputs cannot prove, such as costs not yet restated.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record. Profile the flights, revisions, pauses, restatements, billed lines and adjustments for recorded times, versions, duplicates, currencies and keys that link a credit to its day, and stop and report when an input has no recorded time. Use Ask first only for semantics still open, and record each decision as the user's own answer. Keep cutoffs, reason lists and status vocabularies as editable data. Author expected ledgers by hand from the inputs and approved rules for several cutoffs before the models exist, and compare exactly. Build each cutoff from the inputs known at it, derive campaign and portfolio totals separately, and check they agree. Prove untested branches such as several flights, overlapping flights and flightless campaigns with unit tests. Report every set-aside input and what the inputs cannot prove.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, what a reporting cutoff means (end of which day, in which time zone), which instant selects the revision in force (approval or effective), and whether the cutoff freezes cost inputs as well as the plan?
- If unresolved, how a budget is spread over delivery days (evenly or by profile), at what precision and where any remainder goes, and whether a mid-flight revision re-paces the whole flight or only the budget still unspent?
- If unresolved, which days are eligible delivery days (weekdays, dayparts), how a pause moves planned spend (re-spread, carry or drop), and what happens to a pause recorded after spend and to spend recorded on a paused day?
- If unresolved, which source is provisional and which settled, when a day counts as settled and whether a void or later version returns it to provisional, which platform restatement wins, and which cost lines (fees, taxes) count?
- If unresolved, which keys link a credit or adjustment to its campaign, day and its copies in other sources, which copy applies, and how a credit with no matching bill or restatement is handled?
- If unresolved, what a campaign with no approved revision, a day with no reported spend, a flight not yet started or already ended, and spend above the plan each show?
- If unresolved, which campaigns, portfolios, currencies and translation rates are in scope, how a campaign without a plan enters portfolio remaining, and how a campaign with several or overlapping flights is paced?
- If unresolved, is an input that cannot be placed (unknown campaign, day outside the flight, missing key, bad amount) set aside with a reason, flagged, or does the run fail naming it?

### Guardrails

- Do not choose the cutoff meaning, revision selection, pacing rule, eligible days, pause handling, settlement rule, credit precedence or exception handling for the user, nor take them from the data, the ad platform or common practice.
- Never let a later revision, restatement, bill, credit or pause change an earlier cutoff's rows beyond what the approved as-of rule allows, and never rebuild past knowledge from a current snapshot.
- Never add platform cost and billed cost for the same day, apply one credit twice, or let a credit that appears in several sources count more than once.
- Never show a missing plan or an unreported day as a clean zero, and never clip remaining budget or hide overspend unless the approved rules say so.
- Never drop, round away or double count an amount or input beyond what the approved rules leave out; every input stays counted or listed with its reason, or the run fails naming it.
- Never sum a campaign's day rows across cutoffs or currencies as if each amount landed once, and never net distinct currencies unless an approved rate rule exists.
- Do not change any bid, budget or flight, forecast spend or recommend an action, and keep sources read-only; stop at the ledger.
