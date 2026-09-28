---
id: shift-unit-economics
title: Build shift revenue, cost and margin with reconciled rollups
trigger:
  - A fleet dashboard reports revenue per shift but cannot establish whether a shift covers its applicable costs.
  - Driver performance or vehicle economics need supported trip assignments and shared costs allocated at shift grain.
  - Shift margins disagree with driver, vehicle or period totals, or low-exposure shifts dominate a ranking.
description: Build shift-grain revenue, cost and margin components from defensible event assignments and approved cost allocations, with visible cost completeness and reconciled driver, vehicle and period rollups.
pitch: Explain shift economics with traceable revenue, complete cost status and allocations that conserve source amounts.
job_category: build
area: transformation
readiness: supported
industry:
  - logistics
domain_objects:
  - shift
  - driver
  - vehicle
  - revenue_event
  - cost_component
  - allocation
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

Build <shift_economics_model> for the shift profitability questions and breakdowns required in this Intent. Inspect approved requirements, shift identity, event assignments and applicable cost sources; settle unresolved economic-unit, attribution and allocation rules. Produce traceable shift revenue, direct and allocated cost components, cost completeness and margin, with driver, vehicle and period rollups. Preserve shifts without revenue and expose unresolved assignments, unallocated costs and missing required costs. Surface incompatible currencies or units and missing upstream conversions. Materialize the outputs in the Intent's sandbox. Verify independently specified assignments, formulas, allocation conservation and rollups, including missing costs, join fan-out and zero allocation bases. If rankings are requested, apply approved exposure and eligibility rules and verify their effect. Identify missing attributes, history, mappings or relationship evidence that prevent an agreed question from being answered.

## Verified by

- The contract fixes shift identity and grain, scoped population, event/driver/vehicle assignments and provenance, reporting time and boundaries, revenue basis, applicable cost components, allocation policies, currencies, units, precision and required breakdowns.
- Each scoped shift, revenue event and cost record has source lineage and an included, excluded or unresolved disposition. Counts close to inputs; missing, ambiguous and unmapped assignments remain visible. Independent wrong-shift and boundary cases reject plausible but unsupported links.
- Shift revenue reconciles to attributed event amounts; input totals close through unresolved and excluded amounts. Driver/vehicle joins cannot multiply revenue, costs or exposure. No-revenue shifts remain represented under the approved population and completeness rules.
- Each cost component reconciles to its source scope: direct plus allocated plus unallocated/excluded amounts equal source totals within approved precision. Policy versions, eligibility, basis, weights, rounding and residuals are auditable; each cost is counted once within its policy scope.
- A labelled complete-cost fixture has shifts S1/D1/V1 and S2/D2/V1 in one period: 1 and 3 hours, revenue 100 and 300, direct cost 20 and 60, and shared cost 80 in one currency. An approved hours allocation yields shared costs 20 and 60, not 80 on each shift.
- That fixture yields shift costs 40/120 and margins 60/180; D1 and D2 match their shifts, while V1 and the period total revenue 400, cost 160 and margin 240. Independent expectations catch duplicated shared costs, equal splits and swapped assignments despite plausible grand totals.
- Missing required costs remain unknown with explicit completeness status; known subtotals cannot become claimed profit. A fixture removing a required cost leaves total cost and profit unknown, distinct from a source-confirmed zero and an approved not-applicable component.
- Cases cover zero/null allocation bases, empty eligible sets, duplicate candidates, multiple events/costs per shift, negative adjustments and reporting boundaries. Unallocated balances remain visible; incompatible currency/unit inputs block affected totals pending approved upstream conversion.
- Driver, vehicle and period rollups reconcile revenue and each cost component to shifts, including explicit unknown/unassigned balances and completeness propagation. Margins recompute from components; ratios use approved denominators, not unapproved averages of shift rates.
- If rankings are requested, approved exposure, hours and cost-completeness eligibility is applied before ranking, with exclusions explained. A labelled minimum-two-hours case admits S2 and excludes S1; independent threshold-edge, missing-exposure and tie cases match the approved rules.
- Expected assignments, amounts, statuses and rollups are fixed independently of model SQL before comparison. Every required question has supporting evidence or an explicit input gap; observed relationships, approved allocations and synthetic examples remain distinguishable.
- dbt checks and independent acceptance queries pass on the actual Intent platform after materialization and rerun; every output is read back. The report records revision, commands, exits, counts, revenue/cost components, margins, allocation balances, rollups and unresolved exceptions.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain and sources. Inspect approved questions, shift/event identities, authoritative assignments and cost evidence first. Profile keys, timing, cardinalities, missingness, currencies and units. Use Ask first only for unresolved semantics; samples or existing SQL cannot approve economic policy. Record shift and reporting grains, revenue recognition, applicable costs, completeness, attribution and allocation scope, basis, eligibility, rounding and residuals. Establish required relationships here without requiring another Recipe. Preserve shift/event/cost lineage, provenance classes, unallocated balances and unresolved cases. Keep known cost subtotals distinct from complete cost and profit; propagate unknowns through rollups. Fix expected fixtures independently before model SQL, including wrong assignments, duplicate joins, uneven allocation, missing costs, zero bases and any ranking threshold. Build shift components and driver/vehicle/period rollups using composed skills and current target dialect/sandbox guidance. Materialize, read back and rerun; reconcile source dispositions, attributed revenue, each cost pool and all rollups, then independently recompute margins and optional rates/rankings. Keep Domain read-only; changed-data fixtures need an approved writable area. Report absent inputs, upstream conversions and untested required cases as incomplete verification.

### Compose

- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, what is one economic shift, which profitability questions and breakdowns are required, and which shifts, drivers, vehicles and periods belong in scope?
- If evidence is incomplete, which keys and time-valid assignments establish shift, driver and vehicle responsibility for each event, and how should gaps, overlaps, shared responsibility and unassigned records appear?
- If not approved, which revenue basis, adjustments and recognition time apply; which direct and shared cost components belong to the economic unit, and what proves complete, missing, confirmed-zero or not-applicable cost?
- If allocation is needed but unresolved, which policy, pool, eligible shifts, basis, weights, zero-basis handling, rounding, residuals and unallocated treatment are approved for costs recorded at another grain?
- If unspecified, which reporting time zone, cutoffs, currencies, units, upstream conversions and precision apply; how should cross-period shifts, incomplete costs and unassigned balances affect rollups and margin labels?
- If comparisons or rankings are requested, which measure, minimum exposure or hours, cost-completeness conditions, zero-denominator behaviour and tie rules make shifts, drivers or vehicles eligible and comparable?

### Guardrails

- Do not claim profit from incomplete costs or silently zero-fill missing required components. Label known subtotals and incomplete margins; a missing record does not establish zero cost.
- Do not invent shift identity, driver/vehicle links or historical assignments. Separate observed relationships, approved allocation policies and labelled synthetic fixtures; expose missing evidence.
- Do not charge a full shared cost to every shift, mix allocation scopes or drop unallocated balances to force reconciliation. Preserve policy provenance and exact source-to-component closure.
- Do not discard materially distinct events or costs to suppress join fan-out. Verify relationship cardinality and retain unresolved, excluded and unknown cases with reasons.
- Do not sum incompatible currencies or units, add unapproved FX logic or design accounting policy. Surface required upstream conversions and unresolved policy decisions.
- Keep this outcome to shift economics and required driver/vehicle/period rollups. Do not expand it into a fleet analytics bundle or payroll engine, or require another Recipe to implement prerequisites or verify it.
- Rankings are conditional on the agreed questions. Do not compare revenue alone as profitability or rank incomplete or insufficient-exposure units outside an approved eligibility rule.
- Use the actual Intent platform and provided sandbox. Do not substitute another engine, synthesize an absent sandbox or mutate Domain sources to manufacture evidence.
- Build success alone does not prove economic semantics. Required independent assignments, cost completeness, allocation conservation, rollup checks and output read-back must pass before claiming completed verification.
