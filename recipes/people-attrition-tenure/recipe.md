---
id: people-attrition-tenure
title: Measure attrition, tenure and hire-cohort retention from the headcount outputs
trigger:
  - Leadership asks whether attrition is rising and where, and nobody can answer from one consistent set of figures.
  - HR and finance quote different turnover rates for the same year because each counts leavers and headcount differently.
  - Nobody can say whether recent hires leave faster than earlier ones, or how long people stay before they go.
description: Classify every leaver, compute attrition rates for the approved cuts under the user's approved definitions, show how tenure is spread across current staff and how each hire cohort is retained, and reconcile leavers to the headcount roll-forward, while every termination record stays accounted for and small groups stay hidden where the approved policy hides them.
pitch: One attrition, tenure and retention picture built on the same people the headcount counts, with every leaver accounted for.
job_category: build
area: transformation
readiness: supported
function:
  - hr
domain_objects:
  - worker
  - headcount
  - termination
  - leaver
  - attrition_rate
  - tenure_band
  - hire_cohort
  - retention
  - attrition_exception
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
  - Needs per-worker period-end state with population status (and FTE if the base uses it) and its roll-forward.
  - Needs termination records with a date, a reason code and the worker's placement on the last day worked.
  - Results as known on a past date need kept snapshots; backdated HR changes restate past periods.
  - Stops at attrition, tenure and retention; building headcount, pay and forecasting are separate outcomes.
related:
  - metric-population-and-rollups
  - effective-dated-business-rules
  - pii-classification-and-masking
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

Build <leaver_model>, <attrition_models>, <tenure_spread_model>, <retention_model>, <termination_accounting_model> and <rollforward_tieout_model> from <worker_state_source>, <headcount_rollforward_source> and <terminations_source>. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only the semantics they leave open. Use the headcount population exactly as the worker state gives it. Classify every leaver under the approved reason-code mapping and regret source, compute attrition rates for the approved cuts (such as organisation rolled up through the approved structure, legal entity, location, employment type and tenure band) under the approved numerator, base and window, show how tenure is spread across current staff, and build a retention table for each approved hire cohort. Give every termination record one disposition, reconcile leavers to the headcount roll-forward, keep person-level relations restricted, and publish aggregates only, hiding groups below the approved minimum except at levels the approved policy never hides. Keep sources read-only. Report what the inputs cannot prove.

## Verified by

- Every termination record has exactly one disposition (counted, left out with its reason, or a problem with its reason), and they add up to the input; a problem the approved policy still counts in rates is marked so, and where the policy fails the run, it fails naming each offending record.
- Every counted leaver meets the approved rule under the approved termination-date convention (in headcount before leaving, hired within the period, or terminated from a status outside it such as leave); excluded terminations are left out with their reason; the population is never recomputed.
- Each leaver's class follows the approved reason-code mapping, and an unmapped code is handled as approved and stays visible; regret follows the approved source and missing-value rule, and a regret value that rule leaves unknown stays visibly unknown.
- Each rate uses the approved leavers over the approved base, window and annualisation rule, and its numerator states which records it includes; class components add up to the headline before hiding, a hidden one is marked hidden, and subsets such as regretted voluntary are reported as subsets.
- Where a period lacks the history its window needs, its rate is empty with a reason, or follows the approved rule; a partial window is never presented as a full one.
- A parent organisation's rate is its subtree's leavers over its subtree's base, under the approved structure for each period (as it stood or as it stands); it is never an average of its children's rates.
- Tenure follows the approved start date, unit, boundary and reference dates, including month-end and day-of-month edges; each worker falls in one band under the approved edges or is shown unbanded with its reason, and early exits follow the approved window at its edge days.
- Each cohort's retained count changes only as the approved retained rule allows: where once lost means always lost it never rises, any approved return is shown as a return, and cells a cohort has not reached are empty, never zero.
- The leavers the rates count reconcile to the headcount roll-forward's leavers per period at the approved grain; every difference is failed or flagged with a reason as the approved policy says, never silently absorbed.
- Published outputs carry no person-level rows, every group below the approved minimum is hidden as approved except at levels the approved policy never hides, and the outcome states whether a hidden group can be worked back from its parent, siblings or adjacent periods.
- Every attrition cut reconciles to one shared base at the approved grain; cohort exits that are counted leavers tie to them by cohort, other exits show their reason; transfers counted as leavers for a losing unit stay separate, never counted for the company or a parent of both units.
- The outcome states what the inputs cannot prove, such as whether backdated HR changes restate past periods or what was known on a past date.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile the worker state (population status and reasons, placements, hire dates, concurrent jobs, period ends), the headcount roll-forward (its grain and leaver counts) and the termination records (dates, reason codes, regret flags, placements, rescinded terminations, duplicates, quick rehires). Check that the roll-forward and the worker state describe the same population. Use Ask first only for semantics still open, and record each decision as the user's own answer. Keep the reason-code mapping, tenure bands, early-exit window, minimum group size and reported periods editable as data where the approved requirements say so. Compute independent expected results for the agreed cases (period-end leavers, hire-and-leave in one period, rehires, unmapped codes, transfers, reorganisations, duplicates and groups at the minimum size) before trusting the models. Keep person-level leaver and termination relations readable only by the approved audience. Report every problem record left open and what the inputs cannot prove.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which terminations of headcount members count as leavers (interns, fixed-term ends, retirements, deaths), is a leaver a person or an employment record when someone holds several jobs, and are rescinded terminations and unprocessable records set aside, counted or made to fail the run?
- If unresolved, is the termination date the last day worked or the first day gone, which period gets a period-end termination, and are a hire and termination in one period, a termination from leave or another status outside headcount, and a quick rehire (such as an entity change) leavers?
- If unresolved, which reason codes are voluntary, involuntary or other and who maintains that mapping, is an unmapped code counted as unclassified, excluded or a failure, where does regret come from, how is a missing regret value treated, and who may read person-level leaver or termination data?
- If unresolved, which leavers form the headline rate, is the base heads or full-time equivalents and averaged how (period ends, opening and closing, or daily), over which window and calendar, is a rate for less than a year annualised, and what is shown for periods without enough history?
- If unresolved, is a leaver placed by the last day worked or the period start, do internal transfers count as leavers for the losing unit, is history shown under the structure as it stood or as it stands, and at which grain do leavers reconcile to the roll-forward, failing or flagging a mismatch?
- If unresolved, does tenure start at the latest hire, the original hire or an adjusted service date, in what unit and with which boundary rule, taken at which reference dates (at leaving, period end or window start), with which band edges and which early-exit window?
- If unresolved, how is a hire cohort defined, is a rehire a new cohort entry or a return, what counts as retained, and how are exits without a termination (such as a move out of the population) shown?
- If unresolved, which cuts (organisation, legal entity, location, employment type, tenure band) are published, what are the minimum group size and its base (also for class splits and consecutive periods), which levels are never hidden, is complementary hiding required, and how are rates rounded?

### Guardrails

- Do not choose the leaver population, rate definition, termination-date convention, tenure basis, cohort rule, published cuts, mismatch handling or disclosure threshold for the user, and take none from the data or common practice; the user may ask for alternatives or a recommendation.
- Never recompute the headcount population or rebuild the headcount roll-forward; use them as given, so leavers and headcount describe the same people.
- Never take regret from a source, or fill a missing regret value, in a way the approved rule does not name, and never guess a class for an unmapped reason code.
- Never drop or double count a termination record; every record outside the counted leavers stays visible with its reason.
- Never average child rates to make a parent's rate, and never compare periods built under different organisation structures without saying so.
- Never publish a person-level row, or a group below the approved minimum outside the levels the approved policy never hides; never let a hidden group be read off totals or adjacent periods when the approved policy forbids it; never widen access to person-level relations beyond the approved readers.
- Never show a partial window or an unreached cohort cell as a complete figure or as zero.
- Do not claim results as known on a past date when the source keeps no snapshots; say backdated HR changes restate them.
- Stop at attrition, tenure and retention: do not change worker records, post to HR systems or forecast future attrition.
