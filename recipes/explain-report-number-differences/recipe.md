---
id: explain-report-number-differences
title: Explanation of why two reports differ on one measure, with each cause measured and closed to the gap
trigger:
  - Two reports that should show the same measure disagree, and nobody can say which table, filter, grain or definition accounts for the gap.
  - A small gap has been called rounding or timing without being shown, and two opposite causes may be cancelling inside it.
  - A new or migrated report shows a different figure from the one it replaces, and the gap has to be explained before anyone signs off.
  - The totals agree but a month, region or service slice does not, or the other way round.
description: Re-derive both reports' values for one measure from their sources, align them to one grain, and name each cause of the gap with its amount, record count and re-runnable query, closing causes, residual and unexplained to the measured gap to the approved precision.
pitch: Show which filter, definition or grain makes two reports disagree, with every cause measured and closed to the gap.
job_category: explain
area: data-quality
readiness: supported
function:
  - cross-functional
domain_objects:
  - report
  - metric
  - difference_cause
  - reconciliation_finding
works_with:
  platforms:
    - duckdb_local
    - motherduck
    - fabric_lakehouse
    - fabric_warehouse
    - redshift
    - databricks
qualifiers:
  - Stops at the explanation, so changing a report or restating a figure belongs to its owner.
  - Proving the same data across two live systems for cutover belongs to cross-platform-live-reconciliation.
  - Rebuilding a report measure as a governed metric belongs to bi-calculations-to-governed-metrics.
  - Building a metric with reconcilable rollups belongs to metric-population-and-rollups.
  - A figure whose logic cannot be read stays as published, with its causes unproven.
related:
  - cross-platform-live-reconciliation
  - bi-calculations-to-governed-metrics
  - metric-population-and-rollups
evidence:
  features:
    - reconciliation
    - querying-semantic-model
  evals: []
---

## Prompt

Explain why <report_a> and <report_b> give different values for <measure> at <period_and_grain>. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Re-derive both values from their sources under each report's own definition, bring them to one grain, and name each cause of the difference, such as a population filter, a definition, a grain or join, or a snapshot time, with its signed amount, record count and a query that can be re-run, so that causes plus any residual plus any unexplained remainder equal the measured difference to the approved precision. Where the governed semantic model defines the measure, show its value beside the two reports and say where it stops. Deliver the explanation as <deliverable_form>. The explanation does not change either report, restate a published figure or decide which report is right unless the approved reference says so.

## Verified by

- Each report's value is re-derived from its sources under its own definition and equals the published figure within the approved tolerance, and its source (deployed relation, loaded figure or replayed definition) is named. A figure that cannot be re-derived is unproven, with no cause built on it.
- Both sides are brought to one approved grain and period. Key uniqueness on each side is shown or the fan-out is counted, and each side's read time or snapshot is stated. A grain, join, snapshot or unit or currency conversion (approved rate) is a named cause, never silent.
- Each cause shows its mechanism (which filter, definition, grain, join or time cut), signed amount, record count and a query that can be re-run against the sources.
- Causes plus residual plus unexplained equal the measured difference to the approved precision; residual is only rounding within tolerance. Opposite-sign causes are each shown, never netted. For a ratio, distinct count or balance, causes apply in the approved order, interaction shown.
- A result that books the gap under one catch-all cause, rounding or a plug, or leaves part unlabelled, fails. A remainder above the approved threshold stops the run or is reported partly explained, as approved, and stays visible. Outcome: explained, partly explained, unexplained or unproven.
- Records each report leaves out are counted with amount and reason as approved, so for a summed measure included plus excluded equals each side's total. A NULL, missing or filtered value counts as a cause only with its count and amount.
- Where several causes touch the same record, the amount is attributed by the approved rule and each record is counted once, with the overlap shown.
- Where the governed semantic model defines the measure, its value, source and revision are shown beside the two reports. A shape it refuses or does not cover is recorded with the refusal and an independent computation, and no refused query is claimed as run.
- Published amounts and counts equal values recomputed independently from the sources with a separate method, and no check reuses the explanation's own calculation.
- An independent expected case with two causes of opposite sign and one unexplained remainder reports each cause and the remainder, never a single netted figure.
- No verdict on which report is right appears unless the approved reference names one. Both reports and their sources are read-only, and no credential or unmasked sensitive value appears in the output.
- The explanation is reachable by its reader in the approved form, naming the pair, measure, period, sources and their read times.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Establish what each report is and how to read it before comparing: its relation or definition, its population, its grain and the time it was taken, and mark any figure whose logic cannot be read as unproven. Profile key uniqueness on each side before any join. Measure both values under each report's own definition and compare them at one grain, then test candidate causes from the reports' definitions and populations, count each excluded population with its amount and reason, and attribute amounts by the approved rule so that causes, residual and unexplained close to the difference to the approved precision. Take the governed semantic model's value for any measure it defines, and record where it refuses or does not cover a shape. Recompute every published amount by an independent method and prove the closure can fail with a labelled case before running it on the real pair. Write the explanation to the approved form and leave both reports untouched.

### Compose

- reconciliation
- querying-semantic-model
- profiling-source-data

### Ask first

- Ask which two reports or relations, measure, period and grain are compared, and whether either report is the reference or neither is, only if the Intent does not already name them.
- Ask which records belong in the comparison population, such as refunds, zero or negative totals, test records, unresolved labels or records outside a reporting window, whether left-out records are listed or only counted, and which differences are intended and only to be documented.
- Ask what tolerance and rounding point apply, exact or an approved amount, and in which unit or currency each report states the measure and, where they differ, which approved rate and rate date relate them.
- Ask when each report was taken, as which viewer role, which timezone cuts the dates, whether any mapping or hierarchy it uses is versioned, and how a snapshot-time difference is treated.
- Ask how amounts are attributed when several causes touch the same record, which cause claims it first and, for a non-additive measure, in what order causes apply.
- Ask what happens to an unexplained remainder: stop, report partly explained, or an amount below which it is accepted.
- Ask how a published figure whose logic cannot be read (a filter held in a reporting tool, a figure supplied as a file) is treated, and who supplies the missing definition.
- Ask in what form the explanation is delivered, to whom, how many example records to show and whether sensitive values must be masked.

### Guardrails

- Do not change either report, relation or definition, or restate a published figure, to close the gap.
- Do not call a gap rounding, timing or noise without its measured amount, and do not book any part of it to a plug cause.
- Do not net causes of opposite sign into one figure.
- Do not join sides on a key with duplicate or null values without counting them.
- Do not name which report is right unless the approved reference says so.
- Do not answer the governed model's own value of a measure it defines with hand-written SQL where the model can answer it, and do not claim a refused query ran.
- Do not present a replayed definition or a loaded figure as the deployed report.
- Do not put credentials or unmasked sensitive values in the output.
