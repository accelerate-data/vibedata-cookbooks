---
id: manufacturing-standard-actual-cost
title: Reconcile production-order standard cost to actual by element, with variance effects, overhead absorption and exceptions
trigger:
  - Production-order variances are worked out in a spreadsheet nobody can audit, and nobody can say which standard version each variance was measured against.
  - Actual cost differs from standard on an order and nobody can split the difference into price, usage, rate, efficiency and overhead effects.
  - Overhead is absorbed by hand, the amounts charged to orders never tie back to the cost-centre pool, and a missing labour rate or conversion factor quietly becomes zero.
description: From production orders, standard versions with their bills of material and routings, material issues, labour and machine time, other order costs, rates, overhead pools and good receipts, publish standard and actual cost per order and element at the approved cutoff, the approved variance effects, overhead absorbed so each pool ties, and every incomplete element or set-aside record.
pitch: Reconcile each production order's standard cost to actual by element, with every difference a named effect or a labelled exception and no rate made zero.
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
  - stock_movement
  - labour_time
  - machine_time
  - goods_receipt
  - unit_conversion
  - cost_center
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
  - Needs standard versions, dated where the approved rule selects by date, with BOM, routing, prices and rates behind each.
  - Needs recorded issues, hours and receipts per order, and overhead pools; planned quantities never stand in for actuals.
  - One currency per run; translating currencies is upstream work.
  - Quantity flow, yield, and reconciling or valuing work in progress are separate outcomes.
  - Setting or rolling up standards, purchase price variance at receipt and ledger posting are separate outcomes.
  - Valuing inventory, finished goods and cost of goods sold belongs to inventory-valuation-cogs.
  - Co-products, by-products and joint-cost splits are a separate outcome.
  - Inputs are landed tables; loading files or extracts belongs to file-drop-to-bronze.
  - A source with no recorded time on postings, rates or pools cannot show late changes; restatement then reads unproven.
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

Build <order_cost_model>, <cost_element_model>, <overhead_allocation_model>, <overhead_pool_model>, <cost_exception_output> and <cost_coverage_output> from <production_order_source>, <standard_cost_source>, <standard_bom_source>, <standard_routing_source>, <material_movement_source>, <labour_time_source>, <labour_rate_source>, <machine_time_source>, <machine_rate_source> where approved, <overhead_pool_source>, <goods_receipt_source>, <unit_conversion_source> and <other_cost_source> where approved. For each production order the approved population compares at <cutoff>, publish standard cost for the approved output quantity from the approved standard version and actual cost, per approved element, such as material, labour, machine, subcontracting or overhead, and split each difference into the approved effects so standard plus effects equals actual. Absorb overhead by the approved method so amounts reaching orders, any under- or over-absorbed amount and rounding add back to each pool. Never cost a missing price, rate, pool or factor at zero, and show or count orders, postings and pools left out with their reason, as approved. Report what the inputs cannot prove.

## Verified by

- On a completed run, each input record is accounted for once, traced to each element or allocation it drives, set aside with one reason, or shown or counted out of scope as approved; counts and amounts per source and currency foot to the input, and each repeat follows the approved duplicate rule.
- Each compared order's standard comes from the version the approved rule selects; a standard changed after that point never moves its standard or effects, and an order the rule leaves with no or several versions is listed with its reason or named in a run failure, as approved, actuals still counted.
- For each complete element, standard cost for the approved output quantity plus its effects equals actual cost, exactly or up to the approved rounding shown where it arises; each order's totals equal the sum of its elements plus any residual the approved rule shows.
- Each effect follows its approved definition and is published with the quantities, prices, rates and hours it uses; a price or rate effect and a usage or efficiency effect never share one amount, and a unit conversion never creates an effect.
- For each approved pool and period, amounts reaching the orders the approved basis covers, plus any under- or over-absorbed amount and rounding, equal the pool; a pool with no basis follows the approved disposition and is never spread silently or dropped.
- A missing price, rate, pool or factor is never costed at zero: an approved fallback is labelled with its source; else the element is incomplete (effects unpublished, known actual shown with one reason by the approved precedence, no total needing it complete), or the run fails naming it, as approved.
- A component or operation posted outside the standard, and a standard line with no posting, each stays identifiable at the approved element grain, flagged as off-standard or unused as approved, never dropped or hidden inside a standard line's usage or price effect.
- Orders outside the approved comparison, such as open at the cutoff, are shown or counted with their reason and their cost to date as approved, never split into effects or reported as a variance; the outcome states how many were left out and why.
- A closed order with no good output, a negative net quantity and a posting after close are each published with their amount and flag, or named in a run failure, as approved; none is clamped, netted away at order level or divided by zero.
- Postings are placed by the approved date; one after the cutoff is counted and excluded, and a late posting or changed cost reaching a reported cutoff is restated, entered as a labelled adjustment, or held out of a frozen cutoff and listed, as approved, never silently changing published figures.
- Each output is unique on its approved grain, and orders, components, operations or cost centres from different plants are never merged because their identifiers match.
- Published costs, effects, allocations and pool ties equal values derived independently from the sources and approved rules, including a standard revised after its selection point, an issue in another unit, a missing input, a shared pool that needs rounding and a zero-output order.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile each input for plant, order, component, operation and cost-centre keys, currencies, standard version dates, units of measure, posting dates, source line identifiers and repeated records before modelling. Write the expected elements, effects, allocations, pool ties, exceptions and coverage by hand from the approved rules and the input data before any model, with a case for each rule at its edge, such as overlapping standard versions, an issue return larger than the issue, two missing inputs on one element, a setup amount on a small lot, a pool split into amounts that need rounding and a pool no order absorbs. Keep each rule the requirements treat as data (versions, prices, rates, factors, bases, cutoffs, reason precedence) as data that the models and tests read, never as a literal. Before declaring the outcome complete, recompute every element closure and pool tie independently of the models, check that every input record is accounted for once and that no incomplete element was published as complete; report what the inputs cannot prove.

### Compose

- capturing-requirements
- generating-dbt-model
- verifying

### Ask first

- If unresolved, which plants, order types and statuses are compared at the cutoff (such as closed or delivered), how other orders and their cost to date are shown or counted, and which keys link a posting to its order, component, operation and cost centre?
- If unresolved, which standard an order is measured against (version in force at release and frozen, current, or period standard), how a version's dates apply, and what overlapping or missing versions do?
- If unresolved, which output quantity the standard is applied to (good receipts net of reversals, planned or started), how lot-size-fixed amounts such as setup scale, where scrap sits, and how a closed order with no good output is compared?
- If unresolved, which postings make up actual cost (issues, hours, subcontracted work, direct charges, sub-order settlements) and how receipt or settlement credits stay out, which cost an issue carries, the element grain, the effects, and how off-standard and unused lines are treated?
- If unresolved, how overhead reaches orders (actual pool allocated on a basis, or a predetermined rate leaving under- or over-absorption at the pool), whether machine time has its own rate, which pools and periods meet the cutoff, how its effects split, and what a pool no order absorbs does?
- If unresolved, what a missing price, rate, pool or factor does (incomplete element, fallback or failure), which reason wins when several are missing, which factors are approved, whether rates and factors are dated, what rounding applies where, and do orders with an incomplete element publish totals?
- If unresolved, which date places a posting (posting or event date), how a posting after close is treated, and whether a reported cutoff is frozen, restated or adjusted when a late posting or changed cost arrives?
- If unresolved, what identifies a duplicate, how a correction or conflicting repeat is treated, and how an unknown order or component, a negative net quantity and a missing recorded time are handled (set aside, flagged or failed), and is a record in another currency set aside or failed?

### Guardrails

- Do not choose any Ask first answer for the user, such as population, linking keys, standard rule, output quantity, actual-cost postings, issue cost, element grain, effects, absorption, rounding, missing inputs, dates, late changes or duplicates, nor take one from the data or common practice.
- Never cost a missing price, rate, pool or conversion factor at zero, nor at a substitute value unless it is an approved fallback labelled with its source, and never publish an order as complete while one of its elements is incomplete.
- Never let a standard changed after the approved selection point move an order's standard or effects.
- Never close an element or a pool by plugging, rounding beyond the approved rule or spreading an under- or over-absorbed amount silently; keep any residual labelled and visible.
- Never count overhead twice, such as machine time valued at its own rate and again inside the overhead pool, unless the approved effects say how the two meet.
- On a run that completes, never drop or double count a record: every order, posting, receipt and pool record stays accounted for, including duplicates, conflicts and set-aside records.
- Do not hold a rule the approved requirements treat as data, such as a version date, price, rate, factor or basis, as a literal in the models.
- Never sum, compare or net amounts in different currencies; a record outside the run's approved currency is set aside or fails the run, as approved, and is never summed in.
- Stop at order cost and its effects: do not set standards, value inventory, post to a ledger or change the production system, and keep sources read-only.
