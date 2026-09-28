---
id: metric-population-and-rollups
title: Build a metric with explicit eligibility and reconcilable rollups
trigger:
  - A new percentage, rate or average needs a defensible eligible population and missing-value policy.
  - Daily and monthly metrics disagree, or totals change when a report groups the same records differently.
  - Trip tips, vehicle occupancy or delivery service rates depend on eligibility, measurement coverage and weighting.
description: Implement a metric with approved eligibility, numerator and denominator components, missing-value and zero-denominator policies, weighting, dimension coverage and verified rollups at supported grains.
pitch: Make the metric's population and components explicit so its values and supported totals can be checked.
job_category: build
area: transformation
readiness: supported
domain_objects:
  - metric
  - eligible_population
  - calculation_component
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

Build <metric_name> for the analytical questions, dimensions and aggregation grains required in this Intent. Inspect approved requirements and source evidence, then settle the numerator, denominator, eligibility, unknown or unmeasurable cases, weighting and zero-denominator policy. Implement the approved calculation and retain the underlying components, source lineage and population dispositions needed to explain and recompute it. Validate eligibility mappings and required dimension coverage. State which components are additive and which metric rollups are valid. Materialize the outputs in the Intent's sandbox and verify independently specified inclusion, exclusion, unknown-versus-zero, zero-denominator and unequal-group cases. Reconcile every requested supported rollup to the approved calculation from underlying components, and report missing evidence that prevents an agreed question or breakdown from being answered.

## Verified by

- The documented definition states the source and output grains, eligible population, numerator, denominator, units, weighting, missing-value treatment, zero-denominator policy and supported rollups; outputs implement that approved definition.
- A small independently specified fixture checks numerator and denominator membership separately, including eligible, ineligible and unresolved cases and any eligibility thresholds; expected components and values are fixed before comparison with model output.
- An unknown or unobserved measurement and a measured zero produce the approved, distinguishable dispositions and contributions; unmeasurable cases and missing weights remain visible instead of becoming zero or silently leaving the population.
- Empty eligible populations and non-empty groups whose denominator is zero produce the explicitly approved value and status, without division errors or an unapproved zero, NULL or exclusion.
- Unequal groups discriminate weighting choices: a labelled synthetic rate example with components 1/2 and 9/10 gives 5/6 for a pooled ratio or 7/10 for an equal-group mean. The approved rule selects the expectation; other formulas get equivalent independent cases.
- Each requested supported dimension and time rollup matches independent recomputation from retained underlying components under the approved formula, weights and missing-value rules; rounded display values are not used as inputs.
- The outputs retain sufficient components, weights and lineage to recompute values at all supported grains. Additive, semi-additive and non-additive restrictions are explicit; unsupported rollups are identified rather than given misleading totals.
- Eligibility and required dimension mappings match approved meanings and cardinalities without fan-out; unmapped, ambiguous and unknown cases are visible, with counts and component amounts reconciled before and after joins.
- Every scoped source row has one auditable included, excluded or unresolved disposition, with reasons and measurement status; disposition counts close to the source population, and additive component totals reconcile under the approved adjustments.
- Required analytical questions and breakdowns are supported or have explicit gaps tied to missing attributes, history, mappings or relationship evidence; absent optional breakdowns are reported without invented inputs.
- Independent expected results cover every meaningful formula, eligibility, weighting and missing-value branch; synthetic fixtures are labelled, observed relationships cite source evidence and approved allocations cite their rule.
- dbt checks and independent acceptance queries pass on the actual Intent platform after materialization and rerun; outputs are read back, and the report records revision, commands, exits, population counts, components, values and unresolved exceptions.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain and sources. Inspect approved requirements, source measurement semantics, eligibility codes and required dimension relationships. Profile missingness, unknown mappings, fan-out, weights and zero denominators. Use Ask first only for unresolved semantics; source samples or existing SQL cannot authorize business policy. Record the metric contract, formula, component grains, membership rules, weighting, missing-value and zero policies, supported rollups and precision/tolerance. Design component and metric outputs with source lineage, reasons and measurement status. Derive fixture expectations independently before implementation, covering inclusion/exclusion, boundaries, unknown versus zero, empty and zero-denominator groups, unequal group sizes and every requested rollup. Label synthetic examples and approved allocations. Implement with the composed skills and current target's dialect and sandbox guidance. Preserve the inputs needed by the approved formula; choose its aggregation method explicitly. Materialize, read back outputs and rerun; reconcile population dispositions, mapping coverage and component totals, then independently recompute rollups. Keep Domain sources read-only and use only an approved writable fixture area. Report missing inputs and untested required cases as incomplete verification, not success.

### Compose

- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If requirements do not settle them, which analytical questions, dimensions, time grains and higher-grain totals must the metric support, and which source population is in scope?
- If unresolved, what makes a record eligible for the numerator and denominator, what do eligibility codes mean, and how should unknown, unmapped or ambiguous membership be represented?
- If not approved, what are the formula, component units and weighting rule; is the desired result a pooled ratio, a mean of individual or group values, or another calculation?
- If unspecified, does an unobserved or unmeasurable value mean zero, exclusion or unknown, and how should missing weights, empty populations and zero denominators affect the value and status?
- If still open, which aggregation methods are valid across each dimension and time grain, what precision and tolerance apply, and are any allocations needed and explicitly approved?

### Guardrails

- Do not mandate ratio-of-sums, average rates or choose weights for convenience. Use the approved definition, including non-ratio formulas and metrics that do not aggregate additively.
- Do not substitute zero for absence or silently remove unknown, unmapped, ambiguous or unmeasurable records. Retain reasons and show their effect on coverage and components under the approved policy.
- Do not sum percentages or average precomputed averages unless that is the approved formula. Retain sufficient components and weights; distinguish calculation precision from display rounding.
- A fully specified simple ratio is a Feature, not a new Recipe. This Recipe resolves population, measurement and rollup semantics for one bounded metric outcome.
- Do not invent dimensions, history, mappings or relationships for optional analytical breakdowns. Expose missing evidence for required questions; label synthetic fixtures and approved allocations accurately.
- Never discard materially distinct records to make reconciliation pass or let a dimension join change the metric population without an approved rule.
- Use the actual Intent platform and provided sandbox. Do not substitute another engine, synthesize an absent sandbox or mutate Domain sources to manufacture evidence.
- Build success alone does not prove metric semantics. Required independent cases, component reconciliation and output read-back must pass before claiming completed verification.
