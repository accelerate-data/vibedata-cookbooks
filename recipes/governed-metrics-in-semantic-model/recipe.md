---
id: governed-metrics-in-semantic-model
title: Define governed metrics once in the Domain's semantic model over a gold fact and prove their values
trigger:
  - Revenue or average order value means different things in different marts and dashboards, and nobody can say which number is right.
  - Each new report re-implements the same KPI in SQL with its own filters, and the copies drift apart.
  - A rate gives a different answer by day than by month because copies aggregate it differently.
  - Analysts need agreed metrics they can slice by agreed dimensions and periods without knowing the joins.
description: Define the approved metrics once in a governed Ossie semantic model over a gold fact mart, prove that what the model returns for each metric it can compile equals an independent computation of the approved definition, keep a refused shape as an independent value, and reconcile to the agreed reference figures, every difference named and sized; code only.
pitch: Define each metric once, prove its numbers, and name and size every difference from the agreed reference figures.
job_category: build
area: semantic-layer
readiness: supported
function:
  - cross-functional
domain_objects:
  - semantic_model
  - governed_metric
  - metric_population
  - dimension
  - metric_reconciliation
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
    - ossie
qualifiers:
  - Needs a gold fact mart with a declared grain; changing marts or building a new fact mart is outside this Recipe.
  - A metric population that reads another dimension's attribute cannot be stated in the model today; see Ask first.
  - A shape the compiler refuses is reported with its refusal and an independent value, not queried.
  - Code only; publishing to a semantic-layer service or BI tool is outside this Recipe.
  - Migrating existing BI measures belongs to bi-calculations-to-governed-metrics.
  - A metric built as a materialised table belongs to metric-population-and-rollups.
related:
  - metric-population-and-rollups
  - bi-calculations-to-governed-metrics
  - fabric-direct-lake-semantic-model
evidence:
  features:
    - capturing-requirements
    - designing
    - planning
    - semantic-model
    - validating-semantic-model
    - running-dbt-in-sandbox
    - verifying
  evals: []
---

## Prompt

Define <metrics> once in a governed Ossie semantic model over <gold_fact_mart>, so analysts can slice them by the agreed dimensions and periods without rewriting the logic. Inherit the Intent's repository, platform, Domain, marts and approved requirements, and resolve only the semantics they leave open. Deliver the approved metrics, each defined once where the model can express it, at the fact's own grain and reaching the dimensions its approved slices need; proof that the value the model returns for each metric, at each approved grain, equals an independent computation of the approved definition at the approved precision, with any metric the model cannot compile reported with its refusal; and a reconciliation of each metric to <reference_figures> that names and sizes every difference. Deliver the definitions as code and publish nothing.

## Verified by

- Each approved metric is defined once in the model with its approved name, description and population, or reported as not governed by the model with its independent value where it cannot be expressed; no mart, grain or governed metric is changed, and no second governed copy exists.
- For each approved metric at each approved grain, unsliced and by each approved slicing dimension, the model's result equals an independent computation of the approved definition from the source records, at the approved precision; a shape the model refuses keeps the independent value and its refusal.
- Every population rule is shown in effect, in the compiled query or by the result it changes on records it covers; a rule the model cannot express is reported as not governed by the model, with the size of the difference it would make, never left as a rule the model silently ignores.
- Every record in the fact is accounted for in each metric as its approved population says; a record whose dimension member is missing or unresolved is shown, excluded and counted, or flagged as approved, never silently dropped by a filter or join.
- Each ratio follows the approved aggregation order over the records its rule names; a missing value or zero denominator shows as approved, never as zero unless the rule says so; a distinct count or balance is recomputed at each level, and currencies or units are never summed.
- Each record falls in the period its approved instant, time zone, day boundary, week start and calendar place it in, at every approved grain; no record in a metric's population is silently lost outside periods covered, and one the approved population leaves out is shown or counted with its reason.
- A cumulative or to-date metric resets and reports each period as the approved rules say, including periods with no activity and periods that cross a reset boundary, and a coarser grain reports what the approved rule says rather than a silent accumulation.
- A dimension used to slice or filter matches each fact record to at most one member under the approved version rule, so no metric is inflated by a join fan-out.
- A derived metric that restates its operand's population keeps it identical to the operand's, held by a check able to fail when they differ.
- Every metric name is unique among the Domain's governed metrics, and its description states its population, so a metric over a different population of the same measure cannot be mistaken for it.
- Each difference from an agreed reference figure is sized and classed as the approved rule says, such as defect, accepted or follow-up; where the reference can be inspected, named causes such as population, column, window or stale data cover all of it, else the rest is sized and named unexplained.
- Each check is shown able to fail, and a gate that is red or could not run is reported with its reason, never counted as a pass.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, marts and approved requirements, and resolve only the semantics they leave open. Confirm the fact mart's declared grain, the fields each population rule can draw on, the dimensions with their versioning, the dates the mart holds including outliers, and the governed metrics the Domain already has. Profile how many records each candidate rule would move, then agree the definitions still open with the user. Author each approved metric once, stating its population in the metric itself, and confirm that each rule is in effect in the compiled query. Compile and run each metric's queries, compare them with an independent computation from the source records, and reconcile each metric to the agreed reference figures, classing each difference as the approved rule says. Report any change the existing marts would need as work outside this Recipe.

### Compose

- capturing-requirements
- profiling-source-data
- designing
- planning
- semantic-model
- validating-semantic-model
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which metrics are governed, over which fact mart, and which column, aggregation, and currency or unit does each one use?
- If unresolved, which records are in each metric's population, such as refunds, zero-value, voided, disputed, test or out-of-window records, and does the rule come from a field on the fact or from master data the business edits?
- If unresolved, where a population needs an attribute of another dimension that a metric cannot read, is that metric left out of the model with its independent computation and the size of the difference, or reached by a route within this Recipe's scope?
- If unresolved, is each ratio a ratio of sums or an average of per-record ratios, what does a zero denominator or a missing value show, and to what precision must values match?
- If unresolved, which instant places a record in a period, in which time zone and day boundary, with which week start and calendar, and at which grains?
- If unresolved, what resets each cumulative or to-date metric, does a coarser period report its last or first value, and does a period with no activity carry a value?
- If unresolved, which dimensions may slice each metric, which version of a changing dimension applies, and is a record whose member is missing or unresolved shown under an explicit member, excluded and counted, or flagged?
- If unresolved, which agreed reference figures and window must the metrics reconcile to, is each difference a defect, an accepted definition difference or a follow-up, in what order are overlapping causes sized, and which metric names and descriptions are official?

### Guardrails

- Do not choose or apply a metric definition, population, ratio rule, period rule or unresolved-member policy without approval; explain the alternatives if asked.
- Do not rely on a population rule the model silently ignores: check that each rule is in effect in the compiled query, and report one the model cannot express.
- Do not let a filter or join on a dimension attribute drop records whose member is missing or unresolved unless the approved policy excludes and counts them.
- Do not treat an existing published figure as ground truth, and do not change an existing mart to make the numbers agree; report the difference, sized, with its cause where it can be found.
- Do not join a dimension unless each fact record matches at most one of its rows under the approved version rule.
- Do not add a second governed copy of a metric beside the model, or rename, re-populate or redefine an existing governed metric or the mart's grain.
- Do not hard-code dimension members into a metric to stand in for an attribute unless the owner approves that copy of master data.
- Do not extend into changing existing marts or building new fact marts, publishing to a semantic-layer service or BI tool, authoring a native BI model, or exporting the model to another format.
- Do not accept a green check without confirming what it examined.
