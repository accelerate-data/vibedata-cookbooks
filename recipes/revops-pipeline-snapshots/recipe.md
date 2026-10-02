---
id: revops-pipeline-snapshots
title: Build a daily opportunity pipeline snapshot with stage conversion and slippage
trigger:
  - The CRM overwrites opportunity stage, amount and close date, so past pipeline cannot be reproduced for a given day.
  - RevOps needs stage-to-stage conversion rates by cohort, but only today's opportunity state is available.
  - Forecast reviews need to know which deals slipped their close date, shrank or grew, and when it happened.
description: Capture one row per opportunity per day in an append-only snapshot, then derive stage transitions, conversion rates and close-date slippage with explicit handling of missed days, reopened and deleted opportunities.
pitch: Reproduce the pipeline as it stood on any day and measure how deals move, convert and slip.
job_category: build
area: transformation
readiness: supported
domain_objects:
  - opportunity
  - pipeline_snapshot
  - stage_transition
  - close_date_slippage
works_with:
  platforms:
    - duckdb_local
  tools:
    - dbt
qualifiers:
  - Complete outcome assessed for duckdb_local only; the other four Studio targets remain unassessed.
  - History starts at the first snapshot; earlier pipeline cannot be reconstructed from present state.
  - Daily capture cannot see changes that happen and revert between two snapshots.
related:
  - dbt-snapshot-history
  - metric-population-and-rollups
  - operational-state-duration
  - business-event-fact
evidence:
  features:
    - profiling-source-data
    - applying-medallion-data-modelling
    - authoring-dbt-project-artifact
    - generating-dbt-model
    - dbt-unit-testing
    - running-dbt-in-sandbox
    - evaluating-dbt-project
    - verifying
  evals: []
---

## Prompt

Build a daily snapshot <pipeline_snapshot> of <opportunity_source> with an append-only capture log <snapshot_capture_log>, and from the snapshot alone derive <stage_transition_model>, <stage_conversion_model> and <slippage_model>. Settle from approved requirements the deal key and how re-created deals link to it, the snapshot day and time zone, same-day rerun policy, stage order with open, won and lost sets, amount unit, conversion cohort and slippage direction. Fix a day-by-day scenario with expected transitions, conversion and slippage before model SQL. Capture exactly the requested day per run, replace that whole day on rerun, leave earlier days untouched, protect history and the log from full refresh, and leave missed days empty, labelling changes across them with the captured days they span. Keep Domain sources read-only; use an approved, labelled synthetic fixture or writable fixture with reset. Replay the days in order with one skipped, prove immutability, unchanged and changed reruns, a full refresh, per-date reconciliation and two wrong consumers, and report what the history cannot answer.

## Verified by

- The approved contract fixes deal key and re-created-deal linkage, snapshot day and time zone, same-day rerun policy, stage order with open, won and lost sets, amount unit, conversion cohort and slippage direction, plus a day-by-day scenario with expected outputs written before model SQL.
- Each run captures only the day passed to it. Snapshot rows for a date match the source rows for that date, and deal key plus snapshot date is unique and non-null.
- An earlier date's rows are byte-identical right after its own run and after every later run, and an unchanged same-day rerun produces an identical result.
- A same-day rerun after a source change replaces the whole date: the changed value appears once with no duplicate or stale rows, and restoring the fixture and rerunning returns the original result.
- A forced full refresh, run with the same explicit snapshot date, keeps every captured date and row, adds a capture-log row instead of rebuilding the log, and leaves the skipped day absent.
- The capture log holds one row per run, including same-day reruns, and rows captured reconcile to the snapshot for that date. A skipped day has neither log nor snapshot rows.
- For every captured date, open-deal counts and open-pipeline amounts reconcile exactly to the source rows for that date.
- Transitions compare consecutive captured days and match the expected set exactly. The first date is a baseline. Labels are independent, so one move can be both reopened and repeated, and a change across a gap carries both observed dates and a gap flag.
- A deleted and re-created deal continues its own series under the stable deal identity and is never counted as new pipeline or twice in conversion.
- Conversion matches the expected cohort, with won, lost and still-open shown separately, a won-so-far rate and a win rate among closed deals. A consumer counting open deals as lost gives a wrong win rate.
- Slippage puts date slips, pull-ins, amount increases and decreases in separate rows and flags slips into a later month. A consumer reading today's source state gives a wrong open count for an earlier date.
- Every model, staging included, has uniqueness and null tests on its declared grain, with unit tests for classification edge cases. The report records revision, dbt and adapter versions, commands, exits, expected and actual results and exceptions.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain and sources. Confirm source references resolve on the target and profile keys, duplicates, stages, dates, amounts and currencies. Use Ask first only for unresolved semantics, then record the contract and a fixed scenario with expected outputs before SQL. Check dbt and adapter versions. Put the snapshot-day rule in one macro that the snapshot and the log both call: use a snapshot date variable when supplied, otherwise the run's local calendar date. Build a staging view of the source, then the snapshot as an incremental model using delete+insert keyed on snapshot date, full refresh disabled, reading only that day's rows. Build the capture log as an append-only incremental model with full refresh disabled, counting rows captured from the snapshot. Derive transitions, conversion and slippage from the snapshot only, comparing consecutive captured days and keying deals on the stable identity. Add grain tests to every model and unit tests for the classifications. Pass the snapshot date on every run, including the full refresh. Replay the days in order, skipping one, and read back after each run; then run the immutability, unchanged-rerun, changed-rerun with restore, full-refresh, reconciliation and both wrong-consumer checks. Isolate fixture-derived relations in every layer, restore and verify the fixture, and report unexecuted cases as incomplete verification.

### Compose

- profiling-source-data
- applying-medallion-data-modelling
- authoring-dbt-project-artifact
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- evaluating-dbt-project
- verifying

### Ask first

- If unresolved, which pipeline questions must this history answer, and which stages, pipelines, owners and currencies are in scope?
- If evidence does not settle it, which stable key identifies a deal across stage changes, and which business key links a deleted and re-created deal to the original?
- If unspecified, which time zone defines a snapshot day, is the source captured as read at run time, and does a same-day rerun keep the first capture or replace it?
- If unresolved, what is the stage order, which stages are open, won and lost, and is conversion measured by cohort reaching a stage, with open deals kept apart at the cutoff?
- If unresolved, does slippage mean any later close date or only a move out of the period, and how should pulled-in dates and amount increases or decreases be reported?
- If no scenario is supplied, which day-by-day fixture and expected transitions, conversion and slippage results are approved as acceptance before model SQL?
- If unspecified, how should reopened, deleted, merged and re-created deals, backward moves and missed days affect pipeline totals and conversion?

### Guardrails

- A snapshot taken today cannot reconstruct earlier pipeline. State the first defensible snapshot date and leave earlier periods unanswered unless authoritative history supports an approved backfill.
- Derived outputs read only the snapshot, never the live source. A consumer joined to today's source state silently rewrites history.
- Never date a change to a missed day. Leave the day empty and label changes across it with the captured days they were observed between.
- Daily capture cannot see changes that happen and revert between snapshots; report that limit. Scheduling is outside this Recipe; the capture log shows which days were captured.
- Replace a rerun's whole date rather than merging rows, which leaves stale rows for deals that vanished between runs. Never overwrite or backfill earlier dates.
- Disable full refresh on the snapshot and the capture log, and pass the snapshot date on every run. That setting is a configuration guard; a rebuild by other means still loses history, so report the limit.
- Keep Domain sources read-only. Mutate only an approved, labelled synthetic fixture or writable fixture with verified reset. Isolate fixture-derived relations by schema in every layer, not by name alone.
- Do not treat open deals as lost or exclude them silently. Show won, lost and open counts separately under the agreed definition.
- Do not assume stage order, currency conversion or amount fields. Report mixed currencies or missing amounts as gaps, and never add day changes and amount changes into one total.
- Execute on the actual supported Intent target and sandbox; support covers duckdb_local only. Keep to the snapshot, log, transitions, conversion and slippage; build no forecast, quota or bookings model.
