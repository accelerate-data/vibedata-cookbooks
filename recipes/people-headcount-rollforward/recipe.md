---
id: people-headcount-rollforward
title: Build period-end headcount and FTE by org and a roll-forward that ties every period
trigger:
  - HR, finance and the board deck each report a different headcount for the same month-end, and nobody can say why.
  - Every month someone rebuilds opening plus hires minus leavers plus transfers in a spreadsheet, and it never equals the closing headcount.
  - Leadership asks how many people a team had at a past month-end, under the org structure that applied then.
description: From effective-dated job history, place every worker in the approved population at each reporting date, publish headcount and FTE at the approved grain with org roll-ups, explain each period's change through approved movement classes, and keep every excluded or unprocessable record visible so no worker is lost or counted twice.
pitch: Turn effective-dated HR job history into one month-end headcount and FTE everyone can use, with a roll-forward that ties every period.
job_category: build
area: transformation
readiness: supported
function:
  - people
domain_objects:
  - worker
  - job_record
  - employment_type
  - org_unit
  - org_hierarchy
  - legal_entity
  - work_location
  - headcount
  - fte
  - headcount_roll_forward
  - workforce_exception
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
  - Past headcount needs effective-dated job history; a current-state worker table cannot show past moves.
  - Reproducing figures as known on a past date needs entry timestamps or kept snapshots of the results.
  - Stops at headcount, FTE and the roll-forward; attrition, tenure, payroll and positions are separate.
related:
  - effective-dated-business-rules
  - dbt-snapshot-history
  - metric-population-and-rollups
  - master-b2b-account-hierarchy
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

Build outputs for worker state, headcount and FTE, the headcount and FTE roll-forward, the out-of-population and problem lists, and completeness (for example <worker_state_model>, <headcount_model>, <roll_forward_model>) from <job_history_source>, <org_hierarchy_source>, <reporting_dates> and the approved rule lists (<counted_population_rules>, <fte_basis_rules>). Resolve with the user only the semantics the Intent's approved requirements leave open. For each approved reporting date, place every worker in the approved population once, at the approved grain (legal entity, org unit, location, employment type or the dimensions approved), with FTE on the approved basis; publish headcount and FTE with roll-ups through the approved org structure for that date; explain each period's change from the previous date through the approved movement classes, for headcount and FTE; list every record left out of the population with its reason, and every record that cannot be processed as a problem, or fail the run naming it, as the approved policy says; and prove every worker and record is accounted for. Keep sources read-only. Report what the inputs cannot prove.

## Verified by

- On a run that completes, each worker the approved rules count (or job, if jobs are counted) with a countable record in effect on a reporting date, under the approved time basis, appears exactly once, placed and with FTE as approved, under the approved boundary rule for same-day and edge records.
- On a run that completes, a record the approved rules leave out of the population is never in headcount or FTE and is listed with its reason at each date it is in effect; each output is unique on its declared business grain, with required fields populated.
- On a run that completes, before any approved suppression, headcount and FTE at the approved grain sum to the worker state for each date, and each roll-up row equals the workers in its subtree under the approved org structure for that date, each counted once.
- Where a minimum group size is approved, it is applied consistently to headcount, FTE, roll-ups and roll-forward movements, so no withheld value can be derived from published totals or movements; a withheld cell is marked, never shown as zero.
- On a run that completes, before any approved suppression, each roll-forward row and approved total holds opening plus each approved movement class equal to closing; the first opening is the approved opening, each later opening equals the prior closing, and each closing equals that date's headcount.
- On a run that completes, a transfer or reclassification between two rows inside the counted population leaves one and enters the other, netting to zero across rows; a move across the counted line, including to or from an out-of-scope entity, changes the total as the approved rules say.
- On a run that completes, movements match results derived independently from the approved rules and records; a change the policy does not restate (late correction, dated rule change) enters as its own approved class, and a change the rules do not count, such as hours alone, moves no row.
- On a run that completes, the FTE roll-forward ties the same way on every row, with FTE entering and leaving through headcount movements kept apart from FTE changes of workers who stay in the same row.
- On a run that completes, at each reporting date, under the approved time basis, every worker and job record in effect lands once: counted (incl. another job of a counted worker), out of the population, or a problem, with its reason; across all dates every record lands once, with its reason.
- On a run that completes, every unprocessable record is listed with its reasons and its effect on the worker follows the approved policy; a worker in an org unit the approved structure cannot place under its top is listed with its reason and the roll-ups it misses.
- Where the approved policy fails the run on an unprocessable record, the run fails explicitly, names each offending record with its reason, and publishes nothing as complete.
- The outcome states which problems remain open and what the inputs cannot prove, such as whether backdated changes restate past dates, whether results are as known on each date, or whether history reaches back to the first opening.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile the job history first: whether it is effective-dated and versioned, how terminations, rehires, leaves and several jobs per worker are recorded, which employment types, entities, locations and org units occur, whether the org structure is dated, whether placement runs through positions with their own dated org assignment, and how rescinded or cancelled actions appear. A current-state worker table cannot support past dates or transfers; say so instead of inventing history. Use Ask first only for semantics still open, and record each decision as the user's own answer. Keep the counted population, FTE basis, reporting dates, movement classes and reasons explicit and editable where the approved requirements say so. Derive expected results independently from the approved rules, not from the models under test. The worker state, headcount, roll-forwards, lists and completeness must never disagree about a worker or a record. Report every problem left open and what the inputs cannot prove.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, who counts: which employment types and statuses (fixed-term, part-time, interns, contractors, agency staff, leave of absence, pending starts, test records), which entities, and does a change to these rules apply from a date or restate every past date?
- If unresolved, what identifies one person across entities and rehires, is headcount per person or per job, which job places a worker holding several at once, how is their FTE combined and capped, and is a termination followed by a hire in another entity a transfer?
- If unresolved, what makes a record count on a reporting date: are start and end dates inclusive, is the termination date the last day worked or the first day gone, and which record wins when several are dated the same day?
- If unresolved, how is FTE set: contracted hours over a standard (per location, contract or entity), a stored fraction, or another basis, with which caps and precision, and what FTE does a worker on leave or with no fixed hours carry?
- If unresolved, which reporting dates and calendar apply, what does the first period open from, and does a late or backdated change restate published dates or appear as an adjustment in a later period?
- If unresolved, at which grain and totals are headcount and the roll-forward reported, which org structure rolls up and as of that date or today, how is a unit with a missing or cyclic parent shown, and does any demographic dimension carry a minimum group size, over which outputs?
- If unresolved, which movement classes explain the change: hire or rehire, transfer or reclassification, conversions across the counted line, leaves, hours-only and FTE changes, late corrections and rule changes; and are movements net between dates or every event in between?
- If unresolved, which records cannot be processed, what happens to the worker (skip the record and keep the last valid state, exclude the worker, or fail the run), how is a gap with no termination treated, and are results computed from effective dates or as known on each date?

### Guardrails

- Do not choose the counted population, placement rule, FTE basis, date boundaries, org structure version, movement classes or problem handling for the user, and take none from the data or common practice; the user may ask for alternatives or a recommendation.
- Never count a worker twice at one date because they hold several jobs unless the approved rules count jobs, and never add roll-up rows together across hierarchy levels.
- Never turn an hours change, a leave or a conversion into a hire or leaver, or invent a leaver or rehire from a gap in the data, unless the approved rules say so.
- Never restate a past date to today's org structure unless the approved rules say so.
- Never drop or double count a worker or record beyond what the approved rules leave out; every excluded or unprocessable record stays visible with its reason.
- Never default missing hours to zero or full time, or fill a missing date, unless the approved semantics say so.
- Expose worker-level outputs only to the audience the Domain's access policy allows; if that is unclear, ask who may see them and whether only the aggregates are kept.
- Land only the identifiers and attributes the approved outputs need: no names or pay, and a demographic dimension only where approved, with the approved minimum group size.
- Do not claim figures as known on a past date when the source has no entry timestamps or kept snapshots; say backdated changes restate them.
- Stop at headcount, FTE and the roll-forward: do not compute attrition rates, tenure cohorts, payroll cost or open positions, or write back to the HR system.
