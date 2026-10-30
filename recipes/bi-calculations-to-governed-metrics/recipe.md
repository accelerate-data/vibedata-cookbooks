---
id: bi-calculations-to-governed-metrics
title: Rebuild selected BI calculations as governed metrics in the canonical semantic model
trigger:
  - Key numbers live as measures inside BI reports, so each report page defines the same number its own way and nobody can review it.
  - A report total matches the agreed figure but a slice by region, month or channel does not, and the measure behind it cannot be inspected.
  - A measure that overrides the report filter, uses a second date relationship or accumulates year to date has to move to a governed layer, and nobody knows whether its numbers survive the move.
  - A BI migration needs to know which measures can be governed, which change, and which cannot be expressed in the semantic model at all.
description: Rebuild a bounded set of existing BI measures, such as Power BI DAX, as governed metrics in the Domain's canonical semantic model, prove each one the model can query matches the source report in every agreed filter context and slice, declare a shape it cannot yet query with independent proof, list gaps, and write cutover and recovery down without running them.
pitch: Move report-local measures into governed metrics, prove each queryable number in every filter context, and list what cannot move.
job_category: re-engineer
area: semantic-layer
readiness: supported
function:
  - cross-functional
domain_objects:
  - semantic_model
  - governed_metric
  - bi_measure
  - filter_context
  - metric_reconciliation
works_with:
  platforms:
    - duckdb_local
  tools:
    - dbt
qualifiers:
  - Assessed end to end on duckdb_local only; other platforms are unassessed.
  - Defines metrics in the Domain's canonical semantic model, creating it where the Domain has none.
  - A metric shape the model's compiler refuses is declared, proven independently and not queryable until it compiles.
  - The source measures and relationships must be readable as text, such as a TMDL or BIM export.
  - The report's tables must already be Domain relations; loading exported files belongs to file-drop-to-bronze.
  - Rebuilding the report's data preparation, such as Power Query steps, is a separate outcome.
  - Does not author MetricFlow models or publish Direct Lake models; sources are existing BI measures.
  - Code and documents only; the report, its row-level security and access rules are not switched, edited or retired.
related:
  - metricflow-semantic-model
  - fabric-direct-lake-semantic-model
  - metric-population-and-rollups
  - file-drop-to-bronze
evidence:
  features:
    - capturing-requirements
    - semantic-model
    - generating-dbt-model
    - running-dbt-in-sandbox
    - verifying
  evals: []
---

## Prompt

Rebuild <bi_measures> from <bi_report_export> as governed metrics in the Domain's canonical semantic model over <domain_relations> that stand for the report's tables, so each number is defined once. Inherit the Intent's context and approved requirements; resolve only the semantics they leave open. Deliver a per-measure record classing each as preserved, changed with approval, or unsupported; the governed metrics, each defined once in the shape its source semantics need, changing an existing one only as approved; consumer queries replacing each measure whose metric the compiler can run, in each approved filter context and slice; proof that each queried value equals <reference_outputs>, captured from the report or an approved reconstruction, and an independent computation of the measure's semantics at every approved slice member, not only the grand total; for a shape the compiler refuses, its declaration and proof that the independent computation equals the reference, reported not yet queryable; each measure the model cannot carry listed as a gap with its reason; and a written cutover and recovery plan that executes nothing. Leave the report, its layout and access rules unchanged.

## Verified by

- Every in-scope measure has a record of what is preserved, what changes with the approval it rests on, and what is unsupported; each governed measure is defined once, no measure the model cannot carry has a stand-in metric, and an existing governed metric changes only by a listed approved change.
- For each governed metric the compiler can run, in every approved filter context and slice, a query's value equals the reference output and an independent computation from the approved relations and the measure's semantics, at the approved precision; each difference is an approved change or a gap.
- The reference's origin and capture context are stated; where that context cannot be fixed, or a Domain relation differs from the data the report reads, parity is reported unproven, never passed, and a reconstructed reference proves no parity with the live report.
- Parity is judged at every approved slice member, not only the grand total: a result that ties the total but differs at a named member fails unless the difference is an approved change.
- A distinct count is recomputed at each level and never summed from lower levels, a balance-style measure follows its approved time rule and is never summed across time, and a ratio follows the source measure's approved aggregation order and is never a stored value that a rollup adds up.
- An empty group and a zero denominator show what the approved rule says for every metric, and the comparison never treats a blank as equal to zero.
- A measure that reads its population through a relationship other than the default follows the approved rule, and the comparison includes a period where the two relationships give different figures, or reports that the data has none.
- A time-intelligence measure follows the approved rule at the first, last and cut-short period; the comparison marks a cut-short period incomplete, and if it is excluded, the exclusion and its reason are recorded.
- Null or unmatched dimension keys and records outside a measure's population are included, excluded and counted, or flagged as the source measure's approved rules require, with their reason, and none is silently lost; blank amounts skipped or counted as zero are reported.
- An additive measure's members sum to its total where each row reaches one member, otherwise the total is recomputed.
- A metric shape the compiler cannot run is declared with its correct semantics, its refusal recorded and reported not yet queryable; its independent computation equals the reference output in every approved context, and a structural check that did not run is reported unrun.
- Cutover and recovery are separate written paths, each with the proof the approved gates need, naming any row-level security the report applies; a metric that cannot be queried has no switch path; nothing is executed, and the report, its layout and access rules are unchanged.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain and approved requirements, and resolve only the semantics they leave open. Read each in-scope measure's definition, the relationships it uses and the filter context it runs in, check which Domain relation stands for each report table and which existing governed metrics it touches, and agree with the user which contexts and slices must match. Build the independent computation of each measure's semantics before the metrics exist, then build the thin dbt models the metrics read and define and validate the governed metrics in the canonical semantic model, declaring a shape the compiler cannot run rather than redefining it. Query every metric in each agreed context and slice, compare with the reference output and the independent computation, and show that the comparison fails a result that ties the grand total but differs by a dimension. Record each measure as preserved, changed with approval, or unsupported, check the empty-group and zero-denominator cases for every metric ungrouped as well as grouped, and write the cutover and recovery plan without running it.

### Compose

- capturing-requirements
- semantic-model
- validating-semantic-model
- generating-dbt-model
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which measures, from which report and model, are in scope, which Domain relation stands for each report table, which records each counts, in which currency and unit, and which filter contexts and slices must match?
- If unresolved, is the reference captured from the live report or reconstructed independently, under which viewer role, refresh time, parameters and versions, and to what precision must values match?
- If unresolved, is each measure that overrides the report filter, uses another relationship or direction, several facts, a currency conversion, a parameter or another measure reproduced, changed with approval where the model can represent it, or unsupported?
- If unresolved, what may change with approval, such as rounding, naming or expression form, what must stay identical, does a measure reuse, rename or extend an existing governed metric, and how is a conflicting definition settled?
- If unresolved, what does an empty group or a zero denominator show, and are empty groups kept?
- If unresolved, which calendar, fiscal year, period edges and time-intelligence variants apply, how is a cut-short final period treated, and does a balance take its last, first or average value?
- If unresolved, is a null or unmatched dimension key included under an explicit member, excluded and counted, or flagged, as the source population rules require, and is a blank amount skipped or counted as zero?
- If unresolved, which proof gates, including access matching any row-level security, must pass before the report switches, who repoints consumers, and do the old measures stay until a separate retirement decision?

### Guardrails

- Do not choose or apply any Ask first answer without approval, such as scope, table mapping, reference, evaluation context, relationship, blank, period, key disposition or rounding; explain the alternatives if asked.
- Do not carry a report expression over unchanged; a metric reproduces the measure's semantics, changes them only as approved and recorded, or the measure is listed as unsupported.
- Do not approximate a measure the model cannot carry, or redefine a refused shape into one the compiler runs; list the gap, or declare the correct shape as not yet queryable.
- Do not accept a runnable substitute whose figures match at the grand total but differ by a dimension, unless the difference is an approved change recorded for that measure; report it as a failed comparison.
- Do not let a relationship's cardinality or filter direction inflate, hide or double count a population; a slice that counts a row under more members than the source relationship does is a failed comparison.
- Do not store a precomputed distinct count, balance or ratio and let a rollup add it up.
- Do not change an existing governed metric, dimension or relationship that other consumers read without approval, and name every consumer an approved change reaches.
- Do not treat a reference reconstructed by an independent computation as output of the live BI engine; state where the reference came from.
- Do not edit, switch, reconfigure or delete the report, its layout or its access rules, and do not execute the cutover.
