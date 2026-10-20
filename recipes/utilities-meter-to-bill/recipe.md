---
id: utilities-meter-to-bill
title: Reconcile meter reads to bills and quantify unbilled energy
trigger:
  - Revenue assurance compares metered usage with billed usage in a spreadsheet each month, and nobody can say which differences are real and which are timing, estimates or a meter swap.
  - A meter with a multiplier, a register that rolled over or a meter exchanged mid-period makes billed energy disagree with the reads, and the cause is found by hand.
  - Finance asks how much energy was delivered but never billed, and the answer changes with every join, because a period with no read or no bill looks like zero.
description: Set metered energy beside billed energy for every in-scope service point and billing period, give each period one verdict under approved tolerance rules, quantify unbilled energy to an approved as-of date, and account for every read and bill line, with no missing read treated as zero.
pitch: Match metered to billed energy for every in-scope period and quantify what was never billed, with nothing silently dropped.
job_category: build
area: transformation
readiness: supported
function:
  - finance
industry:
  - utilities
domain_objects:
  - service_point
  - meter_read
  - billing_period
  - bill_line
  - tolerance_rule
  - reconciliation_verdict
  - unbilled_energy
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
  - Reads, a meter master and bill lines must already be landed as tables, with periods from a calendar or approved source.
  - Quantities only; tariffs, pricing and revenue accruals in money are separate outcomes.
  - Energy commodities only; volume-only commodities such as water are a separate outcome.
  - Stops at the classified reconciliation; correcting bills and estimating missing reads are separate.
  - Reproducing a past as-of date after rule or source changes needs kept history of the sources.
related:
  - finance-gl-subledger-tieout
  - ops-inventory-reconciliation
  - effective-dated-business-rules
  - shared-calendar-fiscal-periods
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

Build <reconciliation_model>, <unbilled_model> and <coverage_model> from <meter_reads>, <meter_master>, <bill_lines>, <billing_periods> and <tolerance_rules>. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only the semantics they leave open. At one row per in-scope service point and billing period, derive metered energy from the reads under the approved rules, derive billed energy from the approved bill lines, and give each period exactly one verdict under the approved tolerance rules. Quantify unbilled energy to the approved as-of date, show a period no read covers as unmeasured and never zero, and account for every read, meter, bill line and period as placed once or set aside with one reason. Keep the tolerance rules as data the user can change, within the approved rule form, keep sources read-only and report what the inputs cannot prove.

## Verified by

- Every in-scope service point and billing period appears once with exactly one verdict from the approved set, including a period with no read, a period with no bill and a period with neither; the verdict counts add back to the number of periods.
- Metered energy, the verdicts and the unbilled figures equal values recomputed independently of the build from the approved reads, bill lines and rules; a period that no usable read covers is empty, never zero.
- A multiplier, a register rollover, a decrease the approved rules do not accept as a rollover, an estimated read and a meter exchange each land as approved, and an exchange stretch no read bridges is shown as unmeasured, never filled.
- Billed energy for each period is the approved bill lines, with credits and adjustments handled as the approved rule says and never dropped; a cancelled, superseded or orphan line stays visible with its reason, and a cancelled-and-rebilled pair is never counted twice.
- A period only partly covered by reads shows its coverage as the approved rule measures it and its partial metered energy, is classed as the approved rule says and is never presented as a full-period comparison unless the approved rules say so.
- A variance exactly at, just inside and just outside the approved tolerance is classed as the approved rule says, and the tolerance applied is published with the row; changing a tolerance row changes the verdicts with no change to the logic, within the approved rule form.
- Unbilled energy is quantified in the approved unit over the periods the approved as-of rule selects, itemised by service point and period with the as-of date stated; moving the as-of date changes what the approved rule says it restricts and nothing else.
- Every read, meter, service point, bill line and period is placed once or set aside with one reason; the energy placed ties to the energy read and billed with the residue shown, and a service point with reads and no bill is listed.
- Every output is unique on its declared grain, each verdict traces to the reads and bill lines behind it, and the verdicts, the unbilled figures and the accounting never disagree about a period.
- The outcome states what the inputs cannot prove, such as reads not yet taken, estimates not yet replaced by an actual read, bills not yet issued and any period or stretch left unmeasured.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile the reads (meter, register, date, value, actual or estimated), the meter master (multiplier, rollover span, service point assignment and its dates), the bill lines (status, version, period, unit, sign) and the billing calendar before modelling. Use Ask first only for semantics still open, and record each decision as the user's own answer. Keep the tolerance rules, the reason vocabulary and the as-of date explicit and editable within the approved rule form. Derive independent expected results by hand from the inputs before reading any output, and probe each rule at its edge. The reconciliation, the unbilled figures and the coverage must never disagree about a period. Publish every unmeasured period, every set-aside record and what the inputs cannot prove.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which service points, commodities and periods are in scope, how is a read or bill in another unit converted (volume to energy by which dated factor), and which service points are exempt (unmetered, inactive, test), shown with a reason?
- If unresolved, which meters and registers feed each service point from which dates (time-of-use, total, delivered or received, demand, shared), are reads cumulative or interval quantities, and do values already include the multiplier?
- If unresolved, where do billing periods come from for each service point, in which time zone are reads dated, and does a read on a boundary day close the period or open the next?
- If unresolved, which reads anchor consumption (actual only, or estimates too), how is energy between reads placed into periods (by day, at the read date or otherwise), and what does a later actual read do to an earlier estimate?
- If unresolved, where does each multiplier come from and from which date, is a lower later reading a rollover by a declared span, an export or a fault, and what happens when a meter is exchanged mid-period?
- If unresolved, which bill lines count as billed (live, cancelled, rebilled, estimated, credits, adjustments), which supersedes which, which date or key places each line, a prior-period adjustment included, in a period, and where does a line that fits no period go?
- If unresolved, which verdicts and reasons exist and which wins when several fit, what tolerance applies from which date and is its edge inside it, may a partly covered period or one no read covers be compared, and which side is over-billed?
- If unresolved, what counts as unbilled energy (days no live bill covers, or also an under-billed shortfall, netted against over-billing or not), which as-of date limits it, how much billing lag is expected, and are partly covered periods reported apart?

### Guardrails

- Do not choose period source, register selection, estimate and exchange rules, bill-line placement and linking keys, verdict precedence, tolerances, the unbilled definition, as-of date or exempt population for the user, or take them from the data; the user may ask for a recommendation.
- Never treat a missing read as zero consumption; show it as unmeasured. Never treat a missing bill as zero billed unless an approved rule says so.
- Never count a cancelled-and-rebilled pair twice, drop a credit, or add energy across a meter exchange no read bridges.
- Never join reads to bills so that a service point with reads and no bill vanishes, or a period is multiplied by its number of reads or lines.
- Never mix units of measure or commodities in one total without an approved conversion.
- Stop at the energy reconciliation: do not price, accrue revenue in money, correct, cancel or rebill any bill, or write to the sources, which stay read-only.
