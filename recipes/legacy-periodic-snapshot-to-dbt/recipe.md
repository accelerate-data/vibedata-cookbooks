---
id: legacy-periodic-snapshot-to-dbt
title: Convert a legacy periodic snapshot load into dbt and prove parity period by period
trigger:
  - A scheduled job publishes one row per entity per period, such as stock on hand at each month-end, and the team wants it in dbt.
  - Consumers read the snapshot's history, so a move needs proof that every period still matches, not only the latest one.
  - Earlier periods are restated by late arrivals or corrections, or a period was never run, and nobody has written down what the legacy job does then.
description: Replace a legacy periodic snapshot load, one row per entity per period, with a dbt model, and prove after every compared run that each period matches the approved legacy result, including the migrated history, a missing period, a rerun, a correction and later runs that change earlier periods.
pitch: Move a legacy period-by-period snapshot into dbt and show every period still matches after each run.
job_category: re-engineer
area: transformation
readiness: supported
function:
  - cross-functional
domain_objects:
  - snapshot_job
  - period_snapshot
  - run_calendar
  - retained_history
  - balance_measure
  - dbt_model
  - approved_baseline
  - parity_report
  - follow_up
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
  - Needs the job's definition and its run record, or inputs from which its runs can be replayed.
  - Needs the tables the job reads landed in the target; landing them belongs to an ingestion Recipe.
  - A job that only keeps the version history of an entity belongs to scd-procedure-to-dbt-snapshot.
  - A new append-only snapshot with no legacy job to match belongs to revops-pipeline-snapshots.
  - A routine that maintains a table with no period grain belongs to stored-procedure-to-dbt.
  - Full-rebuild views and tables with several writers go to legacy-sql-to-dbt and consolidate-legacy-table-writers-to-dbt.
  - Costing or valuing the measure belongs to inventory-valuation-cogs.
  - Other writes, logging and measures outside the snapshot relation are reported, not reproduced.
  - A job that cannot be read or replayed is named unassessed, and its parity is stated unproven.
related:
  - stored-procedure-to-dbt
  - scd-procedure-to-dbt-snapshot
  - dbt-snapshot-history
  - revops-pipeline-snapshots
  - legacy-sql-to-dbt
  - dbt-full-refresh-to-incremental
  - inventory-valuation-cogs
  - consolidate-legacy-table-writers-to-dbt
evidence:
  features:
    - capturing-requirements
    - generating-dbt-model
    - running-dbt-in-sandbox
    - verifying
  evals: []
---

## Prompt

Convert the legacy periodic snapshot load <legacy_snapshot_job>, which publishes <snapshot_table> at the grain <entity_and_period>, into a dbt model in the current Intent. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Read the job's definition, its retained history and its run record, and change nothing in the legacy system unless the owner approves. Deliver the model, the migration of the retained periods, and evidence that after every compared run, starting with the migrated history, the model's relation equals what the approved legacy logic publishes from the same inputs and prior history, at the approved precision, derived independently of the model. Cover a period no run closed, an unchanged rerun, a correction and later runs that change earlier periods, as approved. Add no cross-period sum of a balance unless approved. Report legacy defects apart from parity, handle cutover as approved, and state what the comparison cannot prove.

## Verified by

- Before any later run, the migrated retained history equals the approved legacy result for every period in the approved parity scope at the approved precision, and periods outside it are counted with their reason; a period the legacy never published has no row.
- After every compared run, the relation equals the rows the approved legacy logic publishes from the same inputs and prior history, or its recorded output where inputs are not retained, derived independently of the model; columns outside parity and approved differences are named with their rows.
- Each entity has at most one row per period at the approved grain, unless that grain carries a version; the approved rule decides which entities have a row in a period, including at the start and end of an entity's life, and entities it leaves out are counted with their reason.
- A period no run closed follows the approved rule, with no value outside it, and a later run that applies the rule is compared after it runs.
- Every in-scope event is placed in one period by the approved cut-off and boundary rule, or counted as set aside with its reason; an event with no usable date or outside every period is never silently dropped.
- A rerun, correction or late arrival changes published rows only as the approved rule states, shown by comparing the relation before and after with each changed cell listed; a rerun on unchanged inputs changes none unless the approved rule says otherwise.
- A later run that changes an earlier period is compared at every period it changes, not only the latest, and the changed cells are listed.
- The model adds no cross-period sum of a balance; one the approved legacy logic publishes is reproduced and listed as a legacy behaviour, and each measure's aggregation rule is stated.
- The comparison fails where it should: a deliberately wrong period assignment, a wrong historical value and a changed input each differ from the baseline at the comparison itself, in the cells they affect and nowhere else.
- Legacy defects and reproduced legacy behaviours, such as a folded period, a dropped record or a negative balance, are listed apart from parity with the periods they affect, and none is corrected here without approval.
- Parity is kept apart from cutover: the legacy job and the model do not both publish the consumer-facing relation unless approved, and the legacy job is kept, retired or removed as approved only after parity is accepted.
- The comparison states what it cannot prove, such as legacy branches the inputs never reach and runs it did not compare.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Read the legacy job end to end: how it chooses the period, what it reads, whether it recomputes its whole series or restates a window, what it does on a rerun and what it keeps between runs. Get its run record or the sequence of past runs, settle how the legacy answer is produced for each compared run without changing the legacy system unless approved, and migrate the retained history before any later run. Build the model so a run reproduces the approved rules, with the run calendar held as data. Use inputs that separate rival rules: a period no run closed, an unchanged rerun, a correction, a late arrival dated in an earlier period, an event on a boundary, an entity that starts or ends inside a period and a balance that falls below zero. Compare after every run in order, with expected results derived outside the model from the inputs and the approved rules, and show the comparison fail on a perturbed input. Report legacy defects apart, and state what the comparison cannot prove, including whether a history built with skipped runs is recoverable.

### Compose

- capturing-requirements
- generating-dbt-model
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, what is the period, such as calendar month-end, fiscal period or week, its cut-off, how an event on the boundary is placed, any time zone, and what happens to an event with no usable date or outside every period?
- If unresolved, which entities have a row in each period, including a quiet period and the first and last period of an entity's life, how a merge, split or rename is treated, and where activity of an entity with no row goes?
- If unresolved, what does the legacy job do with a period no run closed or closed only partly, such as leave a gap, carry a row or fold its activity into the next period, and which such legacy behaviours are reproduced, corrected in a separate change or accepted as differences?
- If unresolved, how is each measure derived, rolled forward, recounted or captured, is it a balance, a flow or another non-additive measure, which unit or currency does it carry, do attributes and calendars apply as of the period or the run, and how is a negative value treated?
- If unresolved, what does a rerun, correction or late arrival do: restate the changed period and every later one, only the changed one, append, or, for a closed period, refuse it or post an adjustment in the current one?
- If unresolved, how is retained history migrated, loaded as it stands or rebuilt from events, and which periods, columns and precision count as parity?
- If unresolved, where do the legacy answers come from, the job re-run on the same inputs, its recorded outputs or an independent calculation, and may a login that can write be used?
- If unresolved, which columns does the consumer contract carry, when do consumers move once parity is accepted, and is the legacy job kept, retired or removed?

### Guardrails

- Do not add a cross-period sum or running total of a balance measure unless the approved legacy logic publishes it; publish its value at each period.
- Do not compare only the latest period: every period a run changes is compared.
- Do not fill a period or invent a value where the approved rule and the legacy publish no row.
- Do not rewrite a closed period except as the approved rerun and correction rule restates it.
- Do not edit a baseline or widen the approved precision to make a comparison pass.
- Do not derive an expected result from the model under test.
- Do not correct a legacy defect the approved rule reproduces; report it apart from parity.
- Do not write to the legacy system or run its job to obtain a baseline unless the owner approves it.
- Do not let the legacy job and the model both publish the consumer-facing relation, or retire the legacy job before parity is accepted.
- Do not report parity for a run sequence that differs from the approved run record or is applied out of its order.
