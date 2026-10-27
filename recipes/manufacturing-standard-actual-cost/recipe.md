---
id: manufacturing-standard-actual-cost
title: Reconcile production-order standard cost to actual by element, with variance effects, overhead allocation and exceptions
trigger:
  - Production-order variances are worked out in a spreadsheet that values each order at today's standard, so a standard changed after release shows up as a variance.
  - Actual cost differs from standard on an order and nobody can split the difference into price, usage, rate, efficiency and overhead effects.
  - Overhead is absorbed by hand, the allocations never add back to the cost-centre pool, and a missing labour rate or conversion factor quietly becomes zero.
description: From production orders, dated standards with their bills of material and routings, material issues, labour and machine time, rates, overhead pools and good receipts, publish standard and actual cost per order and element at the approved cutoff, the approved variance effects, overhead allocations that add back to each pool, and every incomplete element or set-aside record.
pitch: Reconcile each production order's standard cost to actual cost by element, so every difference has a named effect and no missing rate becomes zero.
job_category: build
area: transformation
readiness: supported
function:
  - finance
  - supply-chain-ops
industry:
  - manufacturing
domain_objects:
  - production_order
  - standard_cost_version
  - bom_line
  - routing_operation
  - material_issue
  - labour_time
  - machine_time
  - labour_rate
  - goods_receipt
  - unit_conversion
  - cost_center
  - cost_allocation
  - cost_variance
  - cost_exception
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
  - Needs dated standard cost versions with the bill of material, routing, prices and rates behind each.
  - Needs recorded issues, hours, receipts and pools per order; planned quantities never stand in for actuals.
  - One currency per run; translating currencies is upstream work.
  - Quantity flow, yield and work-in-progress reconciliation are separate outcomes.
  - Setting or rolling up standards, purchase price variance at receipt and ledger posting are separate outcomes.
  - Valuing inventory, finished goods and cost of goods sold belongs to inventory-valuation-cogs.
  - Co-products, by-products and joint-cost splits are a separate outcome.
  - Inputs are landed tables; loading files or extracts belongs to file-drop-to-bronze.
  - A source with no recorded posting time cannot show late postings; restatement is then reported unproven.
related:
  - inventory-valuation-cogs
  - effective-dated-bom-requirements
  - finance-gross-margin-variance-bridge
  - manufacturing-oee-downtime
  - file-drop-to-bronze
evidence:
  features:
    - capturing-requirements
    - generating-dbt-model
    - verifying
  evals: []
---

## Prompt

Build <order_cost_model>, <cost_element_model>, <overhead_allocation_model>, <overhead_pool_model>, <cost_exception_output> and <cost_coverage_output> from <production_order_source>, <standard_cost_source>, <standard_bom_source>, <standard_routing_source>, <material_movement_source>, <labour_time_source>, <labour_rate_source>, <machine_time_source>, <machine_rate_source> where approved, <overhead_pool_source>, <goods_receipt_source> and <unit_conversion_source>. Inherit the semantics the Intent already approved; resolve with the user only those left open. For each production order the approved population compares at <cutoff>, publish standard cost for the approved output quantity from the approved standard version and actual cost, per material, labour, overhead and any approved machine element, and split each difference into the approved effects so standard plus effects equals actual. Allocate each overhead pool on the approved basis so allocations, unabsorbed amount and rounding add back to it. Never cost a missing price, rate, pool or factor at zero, and keep orders, postings and pools left out visible with their reason. Keep sources read-only; report what inputs cannot prove.

## Verified by

- On a run that completes, each order, standard, issue, return, hour, receipt and pool record is used once, set aside with one reason, or shown or counted out of scope as approved; counts and amounts per source foot to the input, and every copy of a repeat follows the approved duplicate rule.
- Each compared order's standard comes from the version the approved rule selects; a standard changed after that point never moves the order's standard or effects, and an order with no or several qualifying versions is published with its reason while its actuals stay counted.
- For each complete element, standard cost for the approved output quantity plus its effects equals actual cost, exactly or up to the approved rounding shown where it arises; each order's totals equal the sum of its elements plus any residual the approved rule shows.
- Each effect follows its approved definition and is published with the quantities, prices, rates and hours it uses; a price or rate effect and a usage or efficiency effect never share one amount, and a unit conversion never creates an effect.
- For each cost centre and approved period, allocations to every order the approved basis reaches, plus any unabsorbed amount and rounding, equal the pool; a pool with no basis follows the approved disposition and is never spread silently or dropped.
- A missing price, rate, pool or factor is never costed at zero: an approved fallback is labelled with its source; else the element is incomplete (effects unpublished, known actual shown with one reason by the approved precedence, no total needing it complete), or the run fails naming it, as approved.
- A component or operation posted outside the standard, and a standard line with no posting, each stays identifiable at the approved element grain, flagged as off-standard or unused as approved, never dropped or hidden inside a standard line's usage or price effect.
- Orders outside the approved comparison, such as open at the cutoff, are listed with their reason and their cost handled as approved, never reported as a variance.
- A closed order with no good output, a negative net quantity and a posting after close are each published with their amount and flag, or named in a run failure, as approved; none is clamped, netted away at order level or divided by zero.
- Postings are placed by the approved date; one after the cutoff is counted and excluded, and a late posting or changed cost reaching a reported cutoff is restated, entered as a labelled adjustment, or held out of a frozen cutoff and listed, as approved, never silently changing published figures.
- Each output is unique on its approved grain, and orders, components, operations or cost centres from different plants are never merged because their identifiers match.
- Published costs, effects, allocations and pool ties equal values derived independently from sources and approved rules, on cases such as a standard revised after release, an issue in another unit, missing factors and rates, a substitute component, a rounded shared pool and a zero-output order.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile each input for plant, order, component, operation and cost-centre keys, standard version dates, units of measure, posting dates, source line identifiers and repeated records before modelling. Write the expected elements, effects, allocations, pool ties, exceptions and coverage by hand from the approved rules and the input data before any model, with a case for each rule at its edge, such as overlapping standard versions, an issue return larger than the issue, two missing inputs on one element, a pool split into amounts that need rounding and a pool no order absorbs. Keep each rule the requirements treat as data (versions, prices, rates, factors, bases, cutoffs, reason precedence) as data that the models and tests read, never as a literal. Before declaring the outcome complete, recompute every element closure and pool tie independently of the models, check that every input record is accounted for once and that no incomplete element was published as complete; report what the inputs cannot prove.

### Compose

- capturing-requirements
- generating-dbt-model
- verifying

### Ask first

- If unresolved, which plants, orders and statuses are compared at the cutoff (closed only, or work in progress to date), how other orders and their cost are shown, and which keys link a posting to its order, component, operation and cost centre?
- If unresolved, which standard an order is measured against (version in force at release and frozen, current, or period standard), how a version's dates apply, and what overlapping or missing versions do?
- If unresolved, which output quantity the standard is applied to (good receipts net of reversals, planned or started), where scrap sits, and how a closed order with no good output is compared?
- If unresolved, at what grain elements are kept (component or group, operation or labour class, cost centre), which actual cost an issue carries, which effects each is split into, whether machine time has its own rate or sits in overhead, and how off-standard and unused standard lines are treated?
- If unresolved, which basis absorbs each cost centre's overhead, which pool periods meet the cutoff, which orders share a pool, how spending and efficiency are split, what rounding applies to elements, totals and pool shares and where it lands, and what happens to a pool no order absorbs?
- If unresolved, what a missing price, rate, pool or factor does (incomplete element, fallback or failure), which reason wins when several are missing, which conversion factors are approved, whether rates and factors are dated, and whether an order with an incomplete element publishes totals?
- If unresolved, which date places a posting (posting or event date), how a posting after close or after the cutoff is treated, and whether a reported cutoff is frozen, restated or adjusted when a late posting or changed cost arrives?
- If unresolved, what identifies a duplicate, how a correction or conflicting repeat is treated, and how an unknown order or component, a negative net quantity and a missing recorded time are handled: set aside, flagged or failed?

### Guardrails

- Do not choose the standard version rule, output quantity, element grain, effects, absorption basis, pool disposition, rounding, incomplete-cost handling, cutoff, duplicate rule or population for the user, and take none from the data or common practice; the user may ask for a recommendation.
- Never cost a missing price, rate, pool or conversion factor at zero or at a substitute value without approval, and never publish an order as complete while one of its elements is incomplete.
- Never let a standard changed after the approved selection point move an order's standard or effects.
- Never close an element or a pool by plugging, rounding beyond the approved rule or spreading an unabsorbed pool silently; keep any residual labelled and visible.
- Never count overhead twice, such as machine time valued at its own rate and again inside the overhead pool, unless the approved effects say how the two meet.
- On a run that completes, never drop or double count a record: every order, posting, receipt and pool record stays accounted for, including duplicates, conflicts and set-aside records.
- Do not hold a rule the approved requirements treat as data, such as a version date, price, rate, factor or basis, as a literal in the models.
- Stop at order cost and its effects: do not set standards, value inventory, post to a ledger or change the production system, and keep sources read-only.
