---
id: effective-dated-bom-requirements
title: Explode an effective-dated bill of materials into component requirements
trigger:
  - Component demand for an approved quantity of finished goods is worked out by hand or in a spreadsheet, and nobody can show which BOM revision, unit conversion or scrap rate produced a figure.
  - A component is used by several assemblies, and its total demand depends on every path through the bill of materials.
  - BOM revisions change over time and a past or future demand must use the revision in force on its own date.
  - Bills of materials contain loops, overlapping revisions or missing unit conversions that silently drop or distort component demand.
description: Explode approved demand into component requirements through the BOM revisions in force under approved date, unit, scrap and yield rules, with gross beside adjusted quantities, the paths behind totals published as approved, and cycles, ambiguous revisions and missing conversions handled as approved and never dropped silently.
pitch: Component demand from the BOM revision in force, with every broken BOM explained.
job_category: build
area: transformation
readiness: supported
function:
  - supply-chain-ops
domain_objects:
  - demand_line
  - bom_revision
  - bom_line
  - unit_conversion
  - component_requirement
  - explosion_path
  - requirement_exception
  - input_disposition
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
  - Past or future requirements need dated BOM revisions; without dates the revision in force cannot be chosen.
  - Demand quantities and dates come from approved demand; this Recipe does not forecast or schedule.
  - Unit conversions may be captured as editable data during the run.
related:
  - master-product-sku-hierarchy
  - effective-dated-business-rules
  - ops-inventory-reconciliation
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

Build <component_requirement_model> that explodes each approved line in <demand_source> through <bom_revision_source> into component requirements, <explosion_path_model> that publishes the paths behind the totals as approved, and <requirement_exception_model> for every path that cannot complete under the approved rules. Inherit the Intent's sources, platform and approved requirements, and settle any BOM semantics they leave open. At every level use the revision in force on the approved date, convert quantities with approved unit conversions, apply the approved scrap and yield rules, and publish gross beside adjusted quantities. Components reached through several paths sum across every valid path. Cycles, ambiguous or missing revisions, missing conversions and over-deep chains follow the approved handling and stay visible, never silent drops or guesses. Stop at component requirements.

## Verified by

- The contract fixes the demand grain and population, revision date and boundaries, base quantities, units, scrap and yield rules, rounding, structure options, exception reach and published grains. Lines outside the population are shown or counted with their reason.
- A labelled fixture with revision 1 of an assembly valid until date T and revision 2 from T selects revision 1 before T and revision 2 after T. At T the approved boundary convention decides between them or the approved overlap outcome. A current-revision join fails it.
- A labelled fixture where one A needs two B and each B needs three C yields a gross requirement of six C for one A before approved adjustments. Independent expectations cover three or more levels, and every published gross equals the explosion with scrap and yield omitted, at the approved rounding.
- A component used on two paths has one summed requirement per demand line equal to the sum of its contributing path quantities exactly at the published precision. Approved path rows carry parent chain and level, every contribution traces to its path, and no row counts twice.
- Adjusted quantities follow the approved scrap and yield formula, including whether an assembly's own allowance carries into its components. Independent recomputation reproduces every published figure, and unit conversions turn each stated quantity into the approved requirement unit.
- A conversion absent from the approved table ends in the approved outcome and names the item and both units. No factor is inferred or chained unless approved, and a component reached in different units still has one summed figure.
- Overlapping revisions of one parent, a gap with none in force and a parent with no bill of materials each end in the approved outcome. An ambiguity exception names the parent and every revision in force, and a latest-wins pick appears only where the approved rule allows it.
- A cycle is handled as approved, naming the repeating item and chain, and never loops the build. A path deeper than the approved bound is handled as approved and never truncated silently, while a path exactly at the bound completes.
- Failures follow the approved reach. Quantity a failure leaves behind is labelled incomplete and never joins a total shown as complete. Paths attempted equal completed plus excepted plus any set aside by the reach, each with its reason, and a line with an excepted path is flagged incomplete.
- Every demand line, BOM line and conversion row is accounted for as used, excepted, not in scope or not reached, with its reason per demand line where outcomes differ. Counts reconcile to the sources, and a repeated or invalid BOM line is dispositioned as approved, never silently merged.
- Published requirements equal values derived independently from the sources and approved rules at demand-line and component grain, fixed before the model is built, and results are identical on rerun. Totals of incomplete lines are never presented as complete.
- No lead time, derived date, forecast, stock netting or availability figure appears. Results are read back from the actual platform, and the depth bound and unit handling are confirmed there or reported unverified.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements. Ask only about BOM semantics they leave open; sample data, ERP defaults and existing code are evidence, never policy. Profile demand lines, BOM revisions and lines, unit tables and any scrap or yield fields: identities, validity dates and their precision, status values, base quantities, units, nulls and duplicate line keys. Fix expected quantities for every required case before any model SQL: revision boundaries, multi-level paths, shared components, unit conversions, scrap and yield, loops, depth bound, overlaps, gaps and missing conversions. Bound the explosion by the approved depth, detect loops from the path itself, and build with the composed skills and the target's dbt and SQL dialect, using bounded level-by-level expansion where the target has no recursive queries. Publish the summed requirements, the approved path rows and the exceptions from one explosion so they never disagree. Confirm on the Intent's platform that the depth bound and unit handling work, or report them unverified there. Report any untested required case as incomplete verification.

### Compose

- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which demand lines are approved, at what grain with which quantity, unit and need date, which lines are out of scope, and how are zero, negative and unapproved quantities handled?
- If not established, which date selects the revision at every level (the demand date or a date supplied with each line), are bounds inclusive or exclusive, which statuses count, and what besides date picks a parent's bill (plant, site, usage or alternative BOM)?
- If not approved, what happens when two revisions of one parent are in force, when none is, or when a parent has no bill of materials: an exception, the latest revision, or a purchased leaf?
- If incomplete, what parent quantity do a bill's component quantities state, which lines are fixed rather than per parent, which conversions are approved and held where, which unit is each item's requirement unit, and what if a conversion is absent?
- If unresolved, is scrap an added allowance or a loss rate, do scrap and yield sit on the line, revision or item, does an assembly's allowance carry into its components, how are zero, negative or missing quantities, scrap and yield handled, and to what precision is it rounded?
- If not decided, does every assembly appear as its own requirement beside its leaves or only its leaves, and how are phantom assemblies, alternates, optional lines, by-products and repeated line keys treated?
- If unresolved, what depth bound applies, how are cycles and over-deep chains handled, does a failed path void only itself, its whole demand line or only the quantities above the break, and how is an incomplete line flagged?
- If not decided, are the summed requirements published with the paths behind them, and are source-row dispositions published per row or counted?

### Guardrails

- Do not invent BOM policy. Revision dates, boundaries, base quantities, units, scrap and yield, structure options and exception handling come from approved requirements or the user. Values from another Intent, ERP defaults or sample data are never defaults.
- Do not pick a revision by recency or arbitrary row order unless an approved rule says so, hide an overlap with deduplication, or default a missing revision, conversion or quantity to a value. Each ends in the approved outcome with its reason.
- Do not truncate an over-deep chain silently or let a cycle loop. Do not count a path twice, and do not let a failed path leave a partial quantity inside a total that looks complete.
- Do not infer or chain unit conversions, and do not apply scrap or yield outside the approved formula and level.
- Select revisions by date only. Do not apply lot, serial or engineering-change effectivity, which is out of scope.
- Do not mutate source demand, revision or conversion data to force a result, and keep synthetic fixtures labelled apart from real data.
- Stop at component requirements. Do not schedule, derive lead times, forecast demand, net against stock or availability, cost components, choose suppliers or trace observed production lots.
- Use the actual Intent platform and sandbox. Build success does not prove quantities are right: the independent expected results and reconciliations must pass before claiming completed verification.
