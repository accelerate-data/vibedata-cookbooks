---
id: logistics-fleet-utilization
title: Build fleet utilisation against explicit asset availability
trigger:
  - A fleet dashboard labels observed vehicle occupancy as utilisation without an authoritative available-time denominator.
  - Fleet capacity reports omit available vehicles that never come online or subtract overlapping maintenance twice.
  - Daily and monthly vehicle utilisation disagree because roster, observation and downtime windows differ.
description: Build fleet utilisation with authoritative asset availability, maintenance-adjusted time, separate observation coverage and traceable numerator and denominator components that reconcile across daily and monthly reporting.
pitch: Measure fleet use against defensible available asset time while keeping missing observations and maintenance evidence visible.
job_category: build
area: transformation
readiness: supported
industry:
  - logistics
domain_objects:
  - asset
  - availability_interval
  - maintenance_interval
  - operational_observation
  - reporting_period
works_with:
  platforms:
    - duckdb_local
    - motherduck
    - fabric_lakehouse
    - fabric_warehouse
    - redshift
  tools:
    - dbt
evidence:
  features:
    - profiling-source-data
    - applying-medallion-data-modelling
    - generating-dbt-model
    - dbt-unit-testing
    - running-dbt-in-sandbox
    - verifying
  evals: []
---

## Prompt

Build <fleet_utilisation_model> for the fleet questions and breakdowns required in this Intent. Inspect approved requirements and source evidence, then settle the resource, asset population, availability basis, usage numerator, maintenance downtime and observation coverage policies. Distinguish calendar, rostered, online and observed time; separate driver occupancy, asset utilisation and availability where relevant. Produce traceable asset-time intervals and daily and monthly numerator, denominator, downtime and coverage components, with explicit unknowns and approved zero-denominator behaviour. Preserve available assets without online records and distinguish them from maintenance-unavailable assets. Materialize the outputs in the Intent's sandbox. Verify independent never-online, unavailable, missing-evidence, overlapping-downtime and reporting-boundary cases; reconcile daily and monthly components and recompute rates. Identify missing attributes, history, mappings or relationship evidence that prevent an agreed question from being answered.

## Verified by

- The contract defines resource and asset identity, population, active dates, authoritative availability basis, usage numerator, downtime exclusions, observation coverage, units, time zone, interval boundaries, daily/monthly grains and zero-denominator behaviour.
- Output separates calendar, rostered, available, online and observed time as applicable; driver occupancy has its own driver-time grain and denominator. Asset utilisation cannot be relabelled occupancy or computed only over assets with observations.
- A labelled two-hour fixture has A available throughout but never online, with complete evidence of no use; A retains 120 available and zero used minutes. B is unavailable throughout due to confirmed maintenance, retaining zero available minutes and a distinct status.
- Missing observations leave use and coverage explicitly unknown under the approved policy, distinct from confirmed zero use. Missing maintenance evidence remains distinct from confirmed zero downtime; neither absence silently determines availability or utilisation.
- A labelled fixed-offset fixture spans month-end midnight: maintenance 23:30-00:30 overlaps 00:00-01:00. Expected union downtime is 90 minutes, split 30 before midnight and 60 after, not the summed 120 minutes or 90 minutes in each period.
- With two fully available 24-hour calendar days in that fixture and no other exclusions, adjusted available minutes are 1410 and 1380. Daily and respective monthly fragments reconcile to 2790 available and 90 downtime minutes, independent of interval input order.
- Independent cases cover availability-window clipping, asset entry/exit, exact boundaries, duplicate and nested intervals, open maintenance ends and applicable daylight-saving changes. Union downtime removes only eligible available time; elapsed time is not assumed from dates.
- Empty populations and maintenance removing all available time produce the approved zero-denominator value and status. Independently fixed usage expectations reconcile at daily/monthly grain; rates recompute from approved components, never unapproved averages of daily rates.
- Each source asset, observation and maintenance record has lineage and an auditable included, excluded or unresolved disposition. Counts close to scoped inputs; ambiguous mappings, missing history, conflicting use/downtime and unmapped assets remain visible with reasons.
- Interval fragments have the agreed unique grain and no double subtraction or join fan-out. Independent component totals reconcile base availability, each approved exclusion and adjusted availability; usage and coverage reconcile at every required rollup within approved precision.
- Every required question and breakdown has supporting evidence or an explicit input gap. Observed relationships, approved allocations and labelled synthetic fixtures stay distinct; independent expectations cover meaningful policy branches before comparison with model output.
- dbt checks and independent acceptance queries pass on the actual Intent platform after materialization and rerun; every output is read back. The report records revision, commands, exits, counts, daily/monthly components, rates, coverage and unresolved exceptions.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain and sources. Inspect approved requirements, asset registry and active dates, calendars/rosters, operational observations, maintenance start/end evidence and relationship cardinalities. Profile coverage and missingness separately from activity. Use Ask first only for unresolved semantics; samples or existing SQL cannot approve policy. Record resource grain, numerator, authoritative availability, exclusions, coverage, interval conventions, open-end rules, reporting zone and zero policy. Build the asset-time population from authority, preserving assets absent from observations. Union overlapping exclusions within availability before splitting reporting periods; retain exclusion provenance and unknown status. Keep driver and asset measures distinct when relevant. Fix independent expected values before model SQL, including never-online versus unavailable, missing evidence, month-end overlap, zero denominators and clock changes. Design traceable interval, component and audit outputs; label synthetic evidence and approved allocations. Implement with composed skills and current target dialect/sandbox guidance. Materialize, read back outputs, rerun and reconcile dispositions, interval unions and daily/monthly components; independently recompute rates. Keep Domain read-only; changed-data fixtures need an approved writable area. Report unsupported questions and untested required cases as incomplete verification.

### Compose

- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, utilisation of which resource and usage activity, over which asset population and available time, answers the required questions; which breakdowns and separate driver occupancy or availability measures are needed?
- If not established, which registry, active dates, calendar or roster authoritatively defines availability, how do calendar, rostered, online and observed time differ, and what removes an asset from availability?
- If unspecified, which maintenance evidence establishes start/end and exclusions, how should open ends and missing maintenance evidence be treated, and is any date-only duration policy explicitly approved and evidence-backed?
- If not approved, what proves observation completeness or no use, how should unobserved periods and unknown availability affect components and rates, and how should use recorded during downtime be resolved?
- If still open, which time zone, elapsed-time units, interval inclusivity, reporting cutoffs, precision and zero-denominator value/status apply, and what daily/monthly aggregation is valid?
- If required relationships remain unresolved, what maps observations and maintenance to assets and drivers over time, and are any allocations approved and distinguishable from observed relationships?

### Guardrails

- Do not derive the fleet denominator from assets that happen to be online or observed. Use the authoritative asset-time population and retain never-online assets with explicit coverage status.
- Do not infer a maintenance duration from a single date without an approved policy and supporting evidence. Missing maintenance records are not proof of zero downtime; a cutoff is not an observed repair completion.
- Do not interpret missing observations as confirmed zero usage, downtime or availability. Preserve unknown status and policy effects even when approved reporting assigns a contribution.
- Do not subtract overlapping maintenance twice or remove downtime outside eligible availability. Split at reporting boundaries with a consistent interval convention and use elapsed instants for clock changes.
- Do not silently discard usage during downtime, unmapped assets or materially distinct maintenance records to meet expected totals. Preserve conflicts, evidence and approved resolution rules.
- Maintenance-adjusted availability is part of this fleet outcome. Do not split it into a subtraction Recipe or require another Recipe to verify utilisation.
- Do not invent driver-to-asset links, history or dimensions for requested breakdowns. Cite source relationships and approved allocations; label synthetic examples and expose missing evidence.
- Use the actual Intent platform and provided sandbox. Do not substitute another engine, synthesize an absent sandbox or mutate Domain sources to manufacture evidence.
- Build success alone does not prove utilisation semantics. Required independent cases, component and rollup reconciliation, and output read-back must pass before claiming completed verification.
