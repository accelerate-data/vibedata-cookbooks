---
id: accumulating-snapshot-procedure-to-dbt
title: Convert a legacy accumulating snapshot load into dbt and prove milestone parity
trigger:
  - A fact table holds one row per order, claim or case, filled in place as each milestone date arrives, by a procedure nobody wants to maintain.
  - The team is moving that load into dbt, but consumers need proof every row and milestone date still matches after each run, not only today.
  - A migration must keep the legacy fill, cancel and correction behaviour exactly before anyone improves it.
description: Move a legacy accumulating snapshot load into dbt, with later milestone dates filled in place, and prove after every run that process rows, milestone dates, statuses and duration measures match the approved baseline.
pitch: Retire a hand-rolled milestone-filling load by proving dbt keeps every process row and milestone date after each run.
job_category: re-engineer
area: transformation
readiness: supported
function:
  - cross-functional
domain_objects:
  - legacy_load
  - accumulating_snapshot
  - business_process
  - milestone_date
  - replay_runs
  - approved_baseline
  - parity_report
works_with:
  platforms:
    - duckdb_local
    - motherduck
    - fabric_lakehouse
    - fabric_warehouse
    - redshift
    - databricks
  tools:
    - dbt
qualifiers:
  - Needs the load's per-run output or an approved rule baseline; history it never kept is not rebuilt.
  - One row per process filled in place; period, version and all-dates-at-insert loads belong elsewhere.
related:
  - stored-procedure-to-dbt
  - scd-procedure-to-dbt-snapshot
  - dbt-snapshot-history
  - batched-loop-procedure-to-set-based-dbt
  - legacy-sql-to-dbt
evidence:
  features:
    - capturing-requirements
    - authoring-dbt-project-artifact
    - generating-dbt-model
    - dbt-unit-testing
    - running-dbt-in-sandbox
    - verifying
  evals: []
---

## Prompt

Convert <legacy_load>, which keeps one row per <business_process> in <fact_table> by inserting it at the first milestone and filling later milestone dates in place as they arrive, into dbt for <fact_consumers> in the current Intent. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Deliver a map from each load rule that inserts a row, fills a milestone, leaves one unchanged or reacts to a cancellation, reopening, delete, correction or missing row to its dbt equivalent, the dbt model, and evidence that after every run in the agreed replay the dbt table matches the approved baseline for that run: the same rows, milestone dates, statuses, duration measures and other contract columns, at the approved precision. Reproduce load behaviours that look like mistakes and report each as follow-up work. Keep agreement on today's rows separate from agreement after every run, and keep parity separate from cutover and retirement of the load.

## Verified by

- Each load rule that inserts a row, fills or keeps a milestone, or reacts to a cancellation, reopening, delete, correction or missing row maps to a dbt behaviour or a stated reason none is needed; behaviour the table cannot show, such as error paths, is out of scope.
- The load is confirmed to be an accumulating snapshot: a row per process inserted at its first milestone and filled in place. A load that adds a row per period, keeps versions, or fills every date at insert is reported and routed elsewhere.
- After every run in the agreed replay, which holds both incomplete and completed processes, the dbt table equals the approved baseline for that run on every consumer-contract column at the approved precision, except columns the comparison excludes, which are listed.
- Expected tables per run are the load's own output or approved extracts where they exist, otherwise built from the feed and approved rules; they are never read from the dbt output, and a rule-built baseline is labelled as rules, not legacy output.
- The comparison can fail: a milestone date moved by one unit of the approved precision, or an earlier milestone overwritten where the approved rule keeps it, fails on the first run it appears, while a check on row counts or the last run alone would still pass.
- Each process has one row from its first appearance; an unfilled milestone is shown as the approved contract shows it and never mistaken for a real date; a filled date is not cleared or changed except as the approved rule says.
- A different value for a filled milestone, a corrected date, and a late or out-of-order milestone each follow the approved rule, and the processes they affect are counted with the rule applied.
- Duration measures follow the approved derivation and emptiness rule, are empty only where it says so, and any value the rule keeps, such as a negative count, stays visible.
- A cancelled, reopened, first-seen-cancelled or deleted process follows the approved rules for its status and its milestones, and nothing already filled is erased or rewritten except as those rules say.
- A process absent from a run, an unchanged redelivery and a repeated run follow the approved rules; repeating a run leaves the table unchanged unless the approved rule says otherwise.
- Where the run feeds are retained, a rebuild from the approved starting table plus the runs in order equals the incrementally built table after each run, otherwise reported unproven; each load behaviour that looks like a defect is reproduced and listed with what correcting it would change.
- The published table keeps the approved consumer contract; relations outside the approved scope are unchanged or named with parity unverified; the load is neither changed nor retired until cutover is approved; what the comparison cannot prove, including unexercised branches, is stated.

## Agent guidance

### Instructions

Read the load end to end first: how a row is created and what the first milestone is, which statements fill later milestone dates and under which conditions, what it does with a different later value, an out-of-order milestone, a cancellation, a reopening, a delete and a process that stops arriving, how status and duration measures are set, and every consumer of the table. Confirm it is an accumulating snapshot, and report any other pattern. Report behaviour the table cannot show, such as writes elsewhere or error paths, as out of scope. Settle where the table after each run comes from, then author the dbt model. Where the run feeds are retained, make a rebuild from the approved starting table and an incremental run reach the same table. Where the baseline is rule-built, build the expected table per run with a committed builder that never reads the dbt output. Replay the agreed runs in order from the approved starting table, compare after each one, and run negative controls that prove the comparison can fail. Record which replay branches were exercised and which were not.

### Compose

- capturing-requirements
- profiling-source-data
- authoring-dbt-project-artifact
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, what identifies one business process, including any entity or currency part of the key, can a closed identifier be reused, and which processes belong, with excluded ones listed with their reasons?
- If unresolved, which milestones exist and in what order, which source and date sets each (an event date, a load date or the run date), how are blank and sentinel dates read, and what are the precision and time zone?
- If unresolved, what happens when the feed brings a different value for a filled milestone, a correction, or a late or out-of-order milestone: keep, overwrite, hold, flag, refuse or clear?
- If unresolved, how is status set, and what do a cancellation, reopening, first-seen-cancelled process and delete do to status and later milestones, including those arriving in the same run?
- If unresolved, how are duration measures derived, when are they empty, is a negative count kept, clamped or refused, and which other contract columns are set at insert or refreshed later?
- If unresolved, is each run a set of changes, event rows or a full extract, and how are a process absent from a run, duplicates, redelivery, retries and rows with no usable key treated?
- If unresolved, where does the table after each run come from, who approves that baseline, which run sequence and starting table form the replay, which columns are compared, and is the comparison exact?
- If unresolved, what counts as unchanged output (name, columns, types, order), does dbt take over the table's name or do consumers move later, and is the load kept or removed after parity?

### Guardrails

- Do not edit the load or its captured per-run output to make the comparison pass, or widen a tolerance, shorten the replay or narrow the approved contract to do so.
- Do not accept agreement on the final table as run-by-run parity; a table that matches only after the last run has not been shown to match what consumers read in between.
- Do not overwrite or clear a filled milestone unless the approved rule says so, and never let an unfilled milestone pass as a real date unless the approved contract shows it that way.
- Where the approved rule uses the run date, supply each run's date as an input to the replay; otherwise do not use the run clock as a milestone date, and a replay must not depend on when it ran.
- Do not clamp, hide or repair a duration measure the approved rule keeps as computed, and do not carry a measure from the feed where the approved rule recomputes it from stored dates.
- Do not rebuild history the load never kept, and do not assign a milestone a date the feed or approved rule does not give it; coverage starts where the approved starting table does.
- Do not correct a load defect; reproduce it, report it as follow-up work and route any wanted change to a separate change.
- Do not let the load and dbt both maintain the consumer-facing table at once, or retire the load before parity is accepted and consumers have moved.
- Do not present a synthetic or rule-built baseline as the load's real output; label it and state that cutover needs validation against the real load.
- Keep Domain sources read-only and the published table within the approved contract; use a labelled synthetic fixture or an approved writable one, and do not change relations outside the conversion.
