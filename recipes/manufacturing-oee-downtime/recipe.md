---
id: manufacturing-oee-downtime
title: Build overall equipment effectiveness and a downtime Pareto
trigger:
  - Plant OEE comes from a hand-built spreadsheet and nobody can say whether stops, slow running or scrap cost a line its points.
  - Line and plant OEE averages machine OEEs, so a small machine moves the number as much as a large one.
  - Stops with no reason, no end or a shift-change crossing distort availability and leave the downtime ranking unable to tie back to OEE.
description: Build availability, performance, quality and OEE per machine, shift and day with weighted line and plant roll-ups and a reason-ranked downtime Pareto, with every stop, count and machine accounted for.
pitch: Show what cost each line its OEE points with every stop, piece and machine accounted for.
job_category: build
area: transformation
readiness: supported
function:
  - supply-chain-ops
industry:
  - manufacturing
domain_objects:
  - machine
  - production_schedule
  - downtime_event
  - production_count
  - production_line
  - ideal_cycle_time
qualifiers:
  - Needs scheduled windows, a stop log, production counts and ideal cycle times
  - Stops at OEE and downtime ranking; yield and work-in-progress reconciliation are separate
  - Starts from reported stop intervals and period piece counts, not raw signals or counters
works_with:
  platforms:
    - duckdb_local
    - motherduck
    - fabric_lakehouse
    - fabric_warehouse
    - redshift
  tools:
    - dbt
related:
  - operational-state-duration
  - logistics-fleet-utilization
  - metric-population-and-rollups
  - effective-dated-business-rules
evidence:
  features:
    - profiling-source-data
    - applying-medallion-data-modelling
    - generating-dbt-model
    - dbt-unit-testing
    - running-dbt-in-sandbox
    - verifying
  evals: []
---

## Prompt

Build <oee_model> from the machine schedule, stop log, production counts and ideal cycle times in this Intent to publish availability, performance, quality and OEE per machine and scheduled shift, per machine and production day, and as line and plant roll-ups, with the minutes and pieces behind every factor, plus a downtime Pareto of reasons for a chosen scope and period. Settle planned production time, stop classes, performance and quality bases, production day and unmeasured machines from approved requirements. Split stops at shift and day boundaries on elapsed time. Place every stop in a loss class, a named set-aside or unassigned, and list every machine as measured or not with its reason. Roll up from summed components over one stated set of machines, never an average of machine OEEs. Materialize in the Intent's sandbox and verify against independent expected results, including each contended rule changed alone. Label synthetic data and report what the inputs cannot answer.

## Verified by

- Each contended rule the approved requirements leave open is editable data. Within its approved form, changing one rule alone moves exactly the figures it governs, and each published row records the rule values it used.
- On every measured row planned time equals run time plus availability loss plus any unobserved time the approved coverage rule leaves. Each factor recomputes from its published minutes and pieces, and OEE equals their product within a stated rounding tolerance.
- Any approved capping of performance or OEE is published beside the raw value with a flag, and the capped and raw figures are each recomputable.
- Independent expected results, fixed apart from the model code, cover each case the inputs carry: a clean shift, a loss shift, a stop crossing a shift change, a rate changing on a date, a mid-shift product change, a clock-change day. The published figures match them.
- A stop crossing a shift or production-day boundary gives each side its own elapsed minutes with the total unchanged, a clock-change day keeps true elapsed minutes, each fragment traces to its stop, and shuffling the input rows changes no result.
- Every reported stop sits in exactly one of a loss class, a set-aside with one named reason, or unassigned. Duplicates and overlaps follow the approved rule without counting any minute twice. Stop minutes outside planned production time show their approved treatment, and no stop disappears.
- A stop with no end follows the approved open-stop rule, never receives an invented end, and is marked still open. A stop with no reason or an unknown one stays visible as unassigned and is counted as approved, never dropped.
- A count row the approved rules cannot use stays visible with its original figures and reason. A shift that lost such a row says so on its row, so a lower performance is not read as slow running.
- Each roll-up's factors come from summed components over one stated set of machines, the minutes and pieces left out are published beside it, and where machines differ in planned time and OEE the roll-up shows its difference from the mean of machine OEEs.
- Every machine in the schedule, stop log, counts and rates is measured or listed once with one named reason such as no planned time or no ideal rate. A missing factor stays empty and is never shown as zero or 100%.
- Reasons are ranked by the approved measure at the approved reason level with a deterministic tie order. A tail cut off by the approved rule shows as one other row, so cumulative share reaches 100% and lost minutes equal the approved scope's loss minutes in the OEE rows, with zero residue.
- A second run over identical inputs changes no row, the whole area builds from a fresh environment, and every output is read back on the Intent's platform.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain and sources. Inspect approved requirements and profile the schedule windows, planned exclusions, stop log, counts and ideal rates for duplicates, overlaps, open stops, unmapped reasons, count periods that cross shifts and missing rates. Use Ask first only for unresolved decisions. Hold every contended rule as editable data and carry the values used on each row. Cut stops at shift and day boundaries with lineage to the reported stop, give every stop and count one disposition from a closed set of reasons, and compute machine-shift time before performance and quality. Roll up from summed components over one stated population. Where the Domain holds no plant data, build a labelled synthetic fixture with the awkward cases and say so. Fix expected results by hand before the model code, then change each contended rule alone and confirm the figures it governs move. Materialize, read back, rerun and reconcile stops, machines and the Pareto against the OEE rows. Record untested cases as incomplete verification.

### Compose

- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If requirements do not settle it, which scheduled time counts as planned production time (breaks, planned maintenance, changeover, no-demand, holidays), is scheduled time left inside it availability loss, and what happens to stop minutes outside planned production time?
- How is a stop classed as availability loss, minor stop or planned time: by reason mapping, a duration floor and whether the floor applies to the whole stop, and does a missing or unknown reason count as loss?
- What fixes the performance basis: the ideal-rate source, which date picks the rate, how a mid-shift product change is weighted, what happens above 100% and to a machine or product with no rate?
- What does good mean for quality, how are rework and scrap treated, and what happens to a count row that contradicts itself or spans shifts?
- Does the absence of a stop record mean running, how are open stops, duplicates, overlaps (and which reason owns overlapping minutes), late and out-of-order records bounded, and what cutoff applies?
- Which production-day start hour, time zone, shift definition and clock-change handling apply per plant or machine, and which period does the Pareto cover?
- Which machine-to-line-to-plant membership rolls up, which machines enter a roll-up and what shows for those left out, and at which reason level are the Pareto ranked, cut off and scoped?
- Which machines or lines are in scope, which are exempt (unscheduled, unconstrained, test), and where is each exempt or unmeasurable one listed with its reason?

### Guardrails

- Do not average machine OEEs for a line or plant. Roll up summed components over one stated set of machines and publish what was left out.
- Do not infer running time from missing stop records beyond the approved coverage rule, or treat a reporting cutoff as an observed end.
- Do not drop, zero-fill or reclassify a stop to make a total pass. Unassigned and set-aside stops stay visible with reasons.
- Do not count duplicate or overlapping stop minutes twice, cut at midnight instead of the approved production day, or assume a 24-hour day on a clock-change date.
- Do not invent planned time, counts or an ideal rate beyond an approved fallback. A missing factor stays empty with its reason, not zero or 100%.
- Do not repair, clamp or fill a count row beyond the approved rule, or cap performance without publishing the raw value and a flag. Show the original and the figure used.
- Do not hard-code a contended rule in SQL. A rule change must move figures without a code change, within the approved rule forms.
- This is OEE and downtime ranking, not yield, scrap or work-in-progress reconciliation to production orders, TEEP, targets, maintenance prediction, root cause or machine signal ingestion.
- Do not present a labelled synthetic fixture as observed plant history, and do not mutate Domain sources to manufacture evidence.
- Use the actual Intent platform and provided sandbox. Build success alone does not prove the semantics.
