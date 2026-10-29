---
id: bi-calculations-to-governed-metrics
title: Rebuild selected BI calculations as governed metrics in the canonical semantic model
trigger:
  - Key numbers live as measures inside BI reports, so each report page defines the same number its own way and nobody can review it.
  - A report total matches the agreed figure but a slice by region, month or channel does not, and the measure behind it cannot be inspected.
  - A measure that overrides the report filter, uses a second date relationship or accumulates year to date has to move to a governed layer without changing its numbers.
  - A BI migration needs to know which measures can be governed, which change, and which cannot be expressed in the semantic model at all.
description: Rebuild a bounded set of existing BI measures, such as Power BI DAX, as governed metrics in the Domain's canonical semantic model, prove they match the source report in every agreed filter context and slice, list what the model cannot carry as gaps, and write the cutover and recovery down without running them.
pitch: Move report-local measures into governed metrics, prove each number in every filter context, and list what cannot move.
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
  - Needs the Domain's canonical semantic model; a metric shape its compiler refuses is declared and proven independently.
  - The source measures and relationships must be readable as text, such as a TMDL or BIM export.
  - Does not author MetricFlow models or publish Direct Lake models; sources are existing BI measures.
  - Code and documents only; the report, its row-level security and access rules are not switched, edited or retired.
related:
  - metricflow-semantic-model
  - fabric-direct-lake-semantic-model
  - metric-population-and-rollups
evidence:
  features:
    - capturing-requirements
    - generating-semantic-model
    - generating-dbt-model
    - running-dbt-in-sandbox
    - verifying
  evals: []
---

## Prompt

Rebuild <bi_measures> from <bi_report_export> as governed metrics in the Domain's canonical semantic model, so each number is defined once and queried the same way in every agreed filter context. Inherit the Intent's repository, platform, Domain and approved requirements, and resolve only the semantics they leave open. Deliver a per-measure record that classes each measure as preserved, changed with approval, or unsupported; the governed metrics, each defined once in the shape its source semantics need; the consumer queries that replace each report measure, returning each metric the compiler can run in every approved filter context and slice; proof that each queried metric's values equal <reference_outputs> and an independent computation of the measure's semantics, and that the independent computation of a shape the compiler refuses equals <reference_outputs>, including a check that fails a result matching at the grand total but differing by a dimension; every measure the model cannot carry listed as a gap with its reason; and a written cutover and recovery plan that executes nothing. Leave the report, its layout and its access rules as they are.

## Verified by

- Every in-scope measure has a record of what is preserved, what changes with the approval it rests on, and what is unsupported; each governed measure is defined once in the semantic model, and no measure the model cannot carry has a stand-in metric.
- For each governed metric the compiler can run, in every approved filter context and slice, a query's value equals the reference output and an independent computation from the source data and the measure's semantics, at the approved precision; each difference is an approved change or a gap.
- The reference's origin and capture context are stated, and where that context cannot be fixed, parity is reported unproven, never passed.
- A deliberately mis-built variant that ties the reference at the grand total but differs at a named dimension member is flagged, so a grand-total match alone never passes.
- A distinct count is recomputed at each level and never summed from lower levels, a balance-style measure follows its approved time rule and is never summed across time, and a ratio follows the source measure's approved aggregation order and is never a stored value that a rollup adds up.
- An empty group and a zero denominator show what the approved rule says for every metric, and the comparison never treats a blank as equal to zero.
- A measure that reads its population through a relationship other than the default follows the approved rule, and the comparison includes a period where the two relationships give different figures, or reports that the data has none.
- A time-intelligence measure follows the approved rule at the first, last and cut-short period; a cut-short period is marked incomplete where shown, and if excluded, the exclusion and its reason are recorded.
- A row with a null or unmatched dimension key follows the approved disposition and stays in every total, and the blank amounts each measure skipped or counted as zero are reported; an additive measure's members sum to its unfiltered total, and a non-additive one is recomputed at the total.
- Records outside each measure's approved population are shown or counted with their reason, never silently dropped.
- A metric shape the compiler cannot run is declared with its correct semantics and its refusal recorded; its independent computation equals the reference output in every approved context, and a structural check that did not run is reported unrun.
- Cutover and recovery are written as separate paths with the proof each needs before it runs; nothing is executed, and the report, its layout and its access rules are unchanged.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain and approved requirements, and resolve only the semantics they leave open. Read each in-scope measure's definition, the relationships it uses and the filter context it runs in, and agree with the user which contexts and slices must match. Build the independent computation of each measure's semantics before the metrics exist, then build the thin dbt models the metrics read and define the governed metrics in the canonical semantic model, declaring a shape the compiler cannot run rather than redefining it. Query every metric in each agreed context and slice, compare with the reference output and the independent computation, and add a mis-built variant that matches at the grand total. Record each measure as preserved, changed with approval, or unsupported, check the empty-group and zero-denominator cases for every metric ungrouped as well as grouped, and write the cutover and recovery plan without running it.

### Compose

- capturing-requirements
- generating-semantic-model
- generating-dbt-model
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which measures, from which report and model, are in scope, which records each counts, in which currency and unit, and which filter contexts and slices must match?
- If unresolved, is the reference captured from the live report or reconstructed independently, under which viewer role, refresh time, parameters and versions, and to what precision must values match?
- If unresolved, is each measure that overrides the report filter, uses another relationship or direction, several facts, a currency conversion, a parameter or another measure reproduced, changed with approval where the model can represent it, or unsupported?
- If unresolved, what may change with approval, such as rounding, naming or expression form, and what must stay identical?
- If unresolved, what does an empty group or a zero denominator show, and are empty groups kept?
- If unresolved, which calendar, fiscal year, period edges and time-intelligence variants apply, how is a cut-short final period treated, and does a balance take its last, first or average value?
- If unresolved, which member holds a null or unmatched dimension key, and is a blank amount skipped or counted as zero?
- If unresolved, which proof gates must pass before the report switches, who repoints consumers, and do the old measures stay until a separate retirement decision?

### Guardrails

- Do not choose or apply an evaluation-context, blank, period, key-disposition or rounding rule without approval; explain the alternatives if asked.
- Do not carry a report expression over unchanged; a metric reproduces the measure's semantics or the measure is listed as unsupported.
- Do not approximate a measure the model cannot carry, or redefine a refused shape into one the compiler runs; list the gap, or declare the correct shape as non-executable.
- Do not accept a runnable substitute whose figures match at the grand total but differ by a dimension; report it as a failed comparison.
- Do not let a relationship's cardinality or filter direction inflate, hide or double count a population in a slice; a slice that fans out is a failed comparison.
- Do not store a precomputed distinct count, balance or ratio and let a rollup add it up.
- Do not treat a reference reconstructed by an independent computation as output of the live BI engine; state where the reference came from.
- Do not edit, switch, reconfigure or delete the report, its layout or its access rules, and do not execute the cutover.
