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
    - verifying
  evals: []
---

## Prompt

Build a daily append-only snapshot <pipeline_snapshot> of <opportunity_source>, its capture log <snapshot_capture_log>, and the consumers <stage_transition_model>, <stage_conversion_model> and <slippage_model> for the pipeline questions required in this Intent. Inspect approved requirements and source evidence before settling opportunity identity, snapshot grain, snapshot date and time zone, same-day rerun policy, tracked attributes, stage order, and the definitions of conversion, cohort, slippage and open pipeline. Capture each day once and idempotently, keep rerunning safe, protect captured days from rebuilds, and make missed days visible rather than filling them. Derive stage transitions with forward, backward and skipped moves, then conversion by cohort and slippage by close date and amount change. Keep Domain sources read-only; use a labelled synthetic fixture or an approved writable fixture with reset. Prove multi-day runs, reruns, a missed day, a forced full rebuild, regressions, reopened and deleted opportunities. Reconcile counts and amounts to the source for each snapshot date and report what the history cannot answer.

## Verified by

- The approved contract defines opportunity key, snapshot grain and date, time zone, same-day rerun policy, tracked attributes, stage order, open and closed stage sets, currency handling, and exact conversion, cohort and slippage definitions, including which close-date moves count as slippage.
- Rerunning a snapshot date against an unchanged source leaves row counts, keys and values unchanged; a rerun after the source changed follows the agreed same-day policy without duplicate keys. Opportunity and snapshot date together pass uniqueness and null checks.
- A forced full rebuild, such as a dbt full-refresh run, keeps every captured snapshot date, row, value and capture-log entry; an unprotected capture that a full refresh rebuilds from present source state fails this check.
- Per snapshot date, opportunity counts and open-pipeline amounts reconcile to the source as read at that run. Closed, deleted and unmapped opportunities remain visible with reasons.
- Every derived output passes uniqueness and null tests on its declared grain. The capture log appends one row per run, including same-day reruns, and rows captured reconcile to the snapshot for that date.
- A multi-day fixture yields the expected transitions. The first captured date is a baseline, not a transition. Forward, backward, skipped, repeated, reopened, deleted and re-created moves are classified under the agreed stage order, independent of consumer SQL; one move may carry several labels.
- Stage conversion rates match independently computed expected values for a fixed cohort, with numerator, denominator and open-at-cutoff deals shown separately. A consumer that counts open deals as lost fails at least one case.
- Slippage cases cover a close date pushed out, pulled in, unchanged and changed several times, plus amount increase and decrease. Each is attributed to the snapshot date on which the change was first observed.
- A missed snapshot day appears as a gap in the capture log and has no filled snapshot rows. Changes across the gap are labelled as observed over several days, and no transition or slippage is dated to a day without a snapshot.
- Reopened, deleted and re-created opportunities, and opportunities that skip stages between snapshots, follow the agreed policy and are not counted as new pipeline or double-counted in conversion.
- A consumer that joins to today's opportunity state instead of the snapshot fails at least one historical expectation. Reports for an earlier date reproduce exactly after later days are added.
- Checks pass on the supported Intent target with outputs read back and fixture reset verified. The report records revision, installed versions, commands, exits, expected and actual results and unresolved exceptions.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain and sources. Inspect approved requirements, confirm source references resolve on the Intent target, and profile opportunity keys, duplicates, nulls, stages, close dates, amounts, currencies and update times. Use Ask first only for unresolved semantics. Record identity, grain, snapshot date and time zone, same-day rerun policy, stage order, open and closed sets, and the conversion, cohort and slippage definitions. Check installed dbt and adapter versions, then author an incremental model with generating-dbt-model or a dbt snapshot with authoring-dbt-project-artifact. Either way, expose one row per opportunity per captured date with a stable key, pass the snapshot date explicitly on every run, replace a rerun's whole date rather than merging rows, expand change-only versions only to captured dates, append one capture-log row per run, and protect captured history and the log from full refresh. Then author bounded transition, conversion and slippage consumers. Fix expected values and tests before model SQL. Use only an approved, labelled synthetic fixture or approved writable fixture with reset. Run consecutive days, a same-day rerun, a missed day, a forced full rebuild and the edge cases, reading back after each run. Run open-as-lost and today's-state consumers against the same expectations. Reconcile counts and amounts per date, then restore and verify the fixture. Report unexecuted required cases as incomplete verification.

### Compose

- profiling-source-data
- applying-medallion-data-modelling
- authoring-dbt-project-artifact
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which pipeline questions must this history answer, and which stages, pipelines, owners and currencies are in scope for conversion and slippage?
- If evidence does not settle it, which stable opportunity key identifies deals across stage, owner and merge changes, and does the source expose a last-modified time or stage history?
- If unspecified, what time zone and cutoff define a snapshot day, should a snapshot capture the source as read at run time or as of a day boundary, and does a same-day rerun keep the first capture or replace it?
- If unresolved, how should conversion be defined: by cohort of entry date, by period of exit, or by stage-reached, and how are open deals treated at the cutoff?
- If unresolved, does slippage mean any later close date or only a move out of the forecast period, and how should pulled-in dates and amount increases or decreases be reported?
- If unspecified, how should reopened, deleted, merged and re-created opportunities, backward stage moves and missed days affect pipeline totals and conversion?

### Guardrails

- A snapshot taken today cannot reconstruct earlier pipeline. State the first defensible snapshot date and leave earlier periods unanswered unless authoritative history supports an approved backfill.
- Do not date a change to a day without a snapshot. Changes across a missed day are observed over an interval and remain labelled as such in transition and slippage outputs.
- Daily capture cannot see changes that happen and revert between snapshots; report that limit rather than inferring intraday moves. Scheduling the daily run is outside this Recipe; the capture log shows whether each expected day was captured.
- Keep Domain sources read-only. Mutate only an approved, labelled synthetic fixture or an approved writable fixture with a verified reset. Isolate fixture-derived relations in every layer and never mix synthetic rows into observed totals.
- Do not overwrite or backfill prior snapshot rows when the source later changes. Corrections arrive as new observations with their own snapshot date, so earlier reports stay reproducible.
- Do not let a rebuild erase history. A full refresh or re-created relation must keep every captured date and capture-log entry; disable full refresh on incremental capture models, because a present-state source cannot restore past days.
- Do not treat open deals as lost, or exclude them silently, when computing conversion. Show numerator, denominator and open-at-cutoff counts separately under the agreed definition.
- Do not assume stage order, currency conversion or amount fields. Use the approved stage order and report mixed currencies or missing amounts as explicit gaps instead of coercing them.
- Execute on the actual supported Intent target and supplied sandbox. Do not switch engines or synthesize an absent sandbox; support here covers duckdb_local only.
- Keep the deliverable to the snapshot, its capture log, transitions, conversion and slippage with their checks. Do not build a forecast, quota or bookings model, or require a second Recipe to prove the snapshot.
