---
id: revops-pipeline-snapshots
title: Build a periodic opportunity pipeline snapshot with stage conversion and slippage
trigger:
  - The CRM overwrites opportunity stage, amount and close date, so past pipeline cannot be reproduced as it stood at an earlier point.
  - RevOps needs stage-to-stage conversion rates by cohort, but only the current opportunity state is available.
  - Forecast reviews need to know which deals slipped their close date, shrank or grew, and between which snapshots it happened.
description: Capture one row per opportunity per user-confirmed snapshot period, such as hourly, daily, weekly or monthly, in an append-only snapshot, then derive stage transitions, conversion rates and close-date slippage with explicit handling of missed periods, reopened and deleted opportunities.
pitch: Reproduce the pipeline as it stood at each captured snapshot period and measure how deals move, convert and slip.
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
  - Capture cannot see changes that happen and revert between two captures; longer periods hide more.
  - Assessed with a labelled synthetic fixture standing in for the CRM; no live opportunity source was captured.
  - Assessed at a daily period only; rules for other periods, capture moments, late runs and empty reads are unassessed.
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

Build a periodic snapshot <pipeline_snapshot> of <opportunity_source> at the user-confirmed <snapshot_period> with an append-only capture log <snapshot_capture_log>, and from the snapshot alone derive <stage_transition_model>, <stage_conversion_model> and <slippage_model>. Settle from approved requirements the period boundaries, time zone, capture moment and lateness window, deal key and re-created-deal linkage, stage order with open, won and lost sets, amount unit, conversion cohort and slippage direction. Fix a period-by-period scenario with expected transitions, conversion and slippage before model SQL. Capture only the requested period per run, replace that whole period on rerun, leave earlier periods untouched, protect history and the log from full refresh, and leave missed periods empty, labelling changes across them with the captured periods they span. Keep Domain sources read-only; use an approved, labelled synthetic fixture or writable fixture with reset. Replay the periods in order with one skipped, prove immutability, unchanged and changed reruns, a full refresh, per-period reconciliation and two wrong consumers, and report what the history cannot answer.

## Verified by

- The approved contract fixes the snapshot period and lateness window, deal key and re-created-deal linkage, stage order with open, won and lost sets, amount unit, conversion cohort and slippage direction, plus a period-by-period scenario with expected outputs written before model SQL.
- The user confirmed the snapshot period, its boundaries, time zone and capture moment; none was inferred from a schedule or source refresh. The period key holds that grain, in UTC when sub-daily.
- Each run captures only the period passed to it: its capture instant maps to one period start under the agreed capture moment, and a run past the lateness window fails. Snapshot rows for a period match its source rows, and deal key plus period start is unique and non-null.
- An earlier period's rows are byte-identical right after its own run and after every later run, and an unchanged same-period rerun at the same capture instant produces an identical result.
- A same-period rerun after a source change replaces the whole period: the changed value appears once with no duplicate or stale rows, and restoring the fixture and rerunning returns the original result. An empty read fails and leaves the earlier capture intact.
- A forced full refresh, run with the same explicit capture instant, keeps every captured period and row, adds a capture-log row instead of rebuilding the log, and leaves the skipped period absent.
- The capture log holds one row per run, including same-period reruns, and rows captured reconcile to the snapshot for that period. A skipped period has neither log nor snapshot rows. Open-deal counts and open-pipeline amounts reconcile exactly to each captured period's source rows.
- Transitions compare consecutive captured periods and match the expected set exactly. The first period is a baseline. Labels are independent, so one move can be both reopened and repeated. A change across a missed period carries both observed periods and a gap flag; adjacent periods are not flagged.
- A deleted and re-created deal continues its own series under the stable deal identity and is never counted as new pipeline or twice in conversion.
- Conversion matches the expected cohort at the last captured period, with won, lost and still-open shown separately, a won-so-far rate and a win rate among closed deals. A consumer counting open deals as lost gives a wrong win rate.
- Slippage puts date slips, pull-ins, amount increases and decreases in separate rows and flags slips out of the agreed forecast period. A consumer reading the current source state gives a wrong open count for an earlier captured period.
- Every model, staging included, has uniqueness and null tests on its declared grain, with unit tests for classification edge cases and period boundaries. The report records revision, dbt and adapter versions, commands, exits, expected and actual results and exceptions.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain and sources. Confirm source references resolve on the target and profile keys, duplicates, stages, dates, amounts and currencies. The user confirms the period; never infer it from a refresh or schedule. Use Ask first only for unresolved semantics, then record the contract and a fixed scenario with expected outputs before SQL. Check dbt and adapter versions. Put the period rule in one macro the snapshot and the log both call: from a supplied capture instant or the run start, return the start of the period it files under, a UTC timestamp when sub-daily. Build a staging view of the source, then the snapshot as an incremental model using delete+insert keyed on period start, full refresh disabled, reading only that period's rows and storing the capture instant. Build the capture log as an append-only incremental model with full refresh disabled, counting rows captured from the snapshot. Derive transitions, conversion and slippage from the snapshot only, comparing consecutive captured periods and keying deals on the stable identity. Add grain tests to every model and unit tests for the classifications and period boundaries. Replay the periods in order, skipping one, reading back after each run, then run the immutability, rerun, restore, full-refresh, reconciliation and both wrong-consumer checks. Isolate fixture-derived relations in every layer, restore and verify the fixture, and report unexecuted cases as incomplete verification.

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
- Unless the user has confirmed it, which snapshot period is wanted (hourly, daily, weekly, monthly or fiscal), where does a period start (week start day, calendar month or approved fiscal calendar), which time zone sets the boundaries, and, if hourly, what reason and row volume are accepted?
- If unspecified, which moment does a snapshot represent (opening, closing or any time inside the period), is the source read as it stands at run time, and how late may a run or rerun still file under its period?
- If unresolved, what is the stage order, which stages are open, won and lost, and is conversion measured by cohort reaching a stage, with open deals kept apart at the cutoff period?
- If unresolved, does slippage mean any later close date or only a move out of the forecast period (month or quarter), and how should pulled-in dates and amount increases or decreases be reported?
- If no scenario is supplied, which period-by-period fixture, spaced at the confirmed period, and which expected transitions, conversion and slippage results are approved as acceptance before model SQL?
- If unspecified, how should reopened, deleted, merged and re-created deals, backward moves and missed periods affect pipeline totals and conversion?

### Guardrails

- A snapshot taken now cannot reconstruct earlier pipeline. State the first defensible snapshot period and leave earlier periods unanswered unless authoritative history supports an approved backfill.
- Derived outputs read only the snapshot, never the live source. A consumer joined to the current source state silently rewrites history.
- Never assign a change or an out-of-window run to a missed period: such a run fails. Leave the period empty and label changes across it with the captured periods they were observed between. Detect gaps by period sequence, never by a fixed day count.
- Capture misses changes that revert between captures, more so for longer periods; report it. Allow hourly only with a stated reason, a source that changes hourly and accepted volume, about 24 times the daily rows. Scheduling is outside this Recipe; the capture log shows which periods were captured.
- Replace a rerun's whole period rather than merging rows, which leaves stale rows for deals that vanished between runs, and fail an empty read rather than keep the old capture. Never overwrite or backfill earlier periods.
- Disable full refresh on the snapshot and the capture log, and pass the capture instant on every run. That setting is a configuration guard; a rebuild by other means still loses history, so report the limit. Keep one period per history; a new period starts a new history.
- Keep Domain sources read-only. Mutate only an approved, labelled synthetic fixture or writable fixture with verified reset. Isolate fixture-derived relations by schema in every layer, not by name alone.
- Do not treat open deals as lost or exclude them silently. Show won, lost and open counts separately under the agreed definition.
- Do not assume stage order, currency conversion or amount fields. Report mixed currencies or missing amounts as gaps, and never add close-date shifts and amount changes into one total.
- Execute on the actual supported Intent target and sandbox; support covers duckdb_local only. Keep to the snapshot, log, transitions, conversion and slippage; build no forecast, quota or bookings model.
