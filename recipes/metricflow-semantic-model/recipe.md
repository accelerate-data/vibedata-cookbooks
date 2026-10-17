---
id: metricflow-semantic-model
title: Define governed metrics as a MetricFlow semantic model over a gold mart
trigger:
  - Revenue or average order value means different things in different marts and dashboards, and nobody can say which number is right.
  - Each new report re-implements the same KPI in SQL with its own filters, and the copies drift apart.
  - A rate gives a different answer by day than by month because copies aggregate it differently.
  - Analysts need agreed metrics they can slice by agreed dimensions and periods without knowing the joins.
description: Define the approved metrics once as dbt MetricFlow semantic models over a gold fact mart, prove that the values the semantic layer returns equal an independent computation of each approved definition at the approved precision, and reconcile them to the agreed reference figures, every difference named and sized; code only, nothing published.
pitch: Define each metric once, prove its numbers, and name and size every difference from the agreed reference figures.
job_category: build
area: semantic-layer
readiness: supported
domain_objects:
  - semantic_model
  - governed_metric
  - metric_population
  - dimension
  - time_spine
  - metric_reconciliation
works_with:
  platforms:
    - duckdb_local
    - motherduck
    - redshift
  tools:
    - dbt
    - metricflow
qualifiers:
  - Assessed end to end on duckdb_local only; motherduck and redshift rely on MetricFlow support and are unassessed.
  - Needs MetricFlow installed where metrics are queried; Studio's managed runtime does not include it today.
  - Needs a gold fact mart with a declared grain; changing existing marts or building new fact marts is outside this Recipe.
  - Code only; publishing to a semantic-layer service or BI tool is outside this Recipe.
related:
  - metric-population-and-rollups
evidence:
  features:
    - capturing-requirements
    - profiling-source-data
    - generating-semantic-model
    - generating-dbt-model
    - running-dbt-in-sandbox
    - verifying
  evals: []
---

## Prompt

Define <metrics> once as dbt MetricFlow semantic models over <gold_fact_mart>, so analysts can slice them by the agreed dimensions and periods without rewriting the logic. Inherit the Intent's repository, platform, Domain, marts and approved requirements, and resolve only the semantics they leave open. Deliver semantic models over the fact mart, at its own grain, that reach every dimension its metrics filter or slice by, with the time spine they need; the approved metrics, each defined once; proof that the values the semantic layer returns equal an independent computation of each approved definition, at the approved precision, at every approved grain, unsliced and by each approved slicing dimension; and a reconciliation of each metric to <reference_figures> that names and sizes every difference. Deliver the definitions as code and publish nothing.

## Verified by

- Each approved metric is defined once in the semantic definitions with its approved definition, name and description; a shared population rule applies identically, read from flags or master data where so approved; no existing mart is changed and the mart's grain is not redefined.
- For every approved metric at every approved grain, unsliced and by each approved slicing dimension, the value the semantic layer returns equals an independent computation of the approved definition from the mart, at the approved precision, using the dimension version the approved rule names.
- Each ratio is formed as the approved rule says, its numerator and denominator cover the records that rule names, a record missing a value a metric uses is handled as the approved rule says, and a zero denominator shows as approved, never as zero unless the rule says so.
- Every record in the mart is accounted for in each metric as its approved population says; a record whose dimension member is missing or unresolved is shown, excluded and counted, or flagged as the approved policy says, never silently dropped by a filter or join.
- Each record falls in the period its approved instant, time zone, day boundary, week start and calendar place it in, at every approved grain, and no record in a metric's approved population, including outliers at either end of the data, is lost because it falls outside the periods the metrics cover.
- A cumulative or to-date metric resets and reports each period as the approved rules say, including periods with no activity and periods that cross a reset boundary.
- Each difference from an agreed reference figure is sized and classed as the approved rule says, such as defect, accepted or follow-up; where the reference can be inspected, named causes such as population, column, window or stale data cover all of it, else the rest is sized and named unexplained.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, marts and approved requirements, and resolve only the semantics they leave open. Confirm the fact mart's declared grain, the columns and flags each population rule can draw on, the conformed dimensions with their versioning, and the dates the mart holds, including outliers. Profile how many records each candidate rule would move, such as unmapped members, refunds or records outside a window, and agree the definitions still open with the user. Then author semantic models over the fact mart that reach every dimension its metrics filter or slice by, the approved metrics, and a time spine covering every period the metrics report. Query the metrics through the semantic layer and compare them with an independent computation of each approved definition. Reconcile each metric to the agreed reference figures, class each difference as the approved rule says, and report any change the existing marts would need as work outside this Recipe.

### Compose

- capturing-requirements
- profiling-source-data
- generating-semantic-model
- generating-dbt-model
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which metrics are governed, over which fact mart, and which column and aggregation does each one use?
- If unresolved, which records are in each metric's population, such as refunds, zero-value, voided, disputed, test or out-of-window records, and does a rule come from flags or master data the business edits, or from the definition itself?
- If unresolved, is each ratio a ratio of sums or an average of per-record ratios, what does a zero denominator or a missing value show, and to what precision must values match?
- If unresolved, which instant places a record in a period, in which time zone and day boundary, such as calendar or operating day, with which week start and calendar, and at which grains?
- If unresolved, what resets each cumulative or to-date metric, does a coarser period report its last or first value, and does a period with no activity carry a value?
- If unresolved, which dimensions may slice each metric, which version of a changing dimension applies, and is a record whose member is missing or unresolved shown under an explicit member, excluded and counted, or flagged?
- If unresolved, which agreed reference figures, from existing marts or reports and over which window, must the metrics reconcile to, and is each difference a defect, an accepted definition difference or a follow-up?
- If unresolved, which metric names and descriptions are official?

### Guardrails

- Do not choose or apply a metric definition, population, ratio rule, period rule or unresolved-member policy without approval; explain the alternatives if asked.
- Do not let a filter or join on a dimension attribute drop records whose member is missing or unresolved unless the approved policy excludes and counts them.
- Do not treat an existing published figure as ground truth, and do not change an existing mart to make the numbers agree; report the difference, sized, with its cause where it can be found.
- Do not join a dimension unless each fact record matches at most one of its rows under the approved version rule; a fan-out inflates or distorts every metric sliced or filtered by it.
- Do not add a second governed copy of a metric beside the semantic definitions, such as a new mart column or report formula, or redefine the mart's grain.
- Do not extend into changing existing marts or building new fact marts, publishing to a semantic-layer service or BI tool, or authoring a native BI semantic model.
