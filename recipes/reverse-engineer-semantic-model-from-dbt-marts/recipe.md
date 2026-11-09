---
id: reverse-engineer-semantic-model-from-dbt-marts
title: Reverse-engineer a semantic model from existing dbt marts and prove it matches the SQL
trigger:
  - A team inherited dbt marts nobody has described, and no one can say what each table is, what one row stands for or how its numbers roll up.
  - Aggregate marts sit beside a detail fact and nobody has shown they add up to it, or which of them are not a true rollup at all.
  - A semantic layer has to start from marts that already exist, without definitions copied by hand that then drift from the SQL.
description: Describe the approved existing dbt marts as a governed Ossie semantic model, with each table's row grain and how its numbers roll up. Prove each aggregate described as a rollup matches its SQL and the detail and each field matches the warehouse, and name every mart that cannot honestly be described, with the reason. No mart is changed.
pitch: Turn marts nobody has described into a checked semantic model, and name every table that cannot honestly be described.
job_category: explain
area: semantic-layer
readiness: supported
function:
  - cross-functional
domain_objects:
  - semantic_model
  - dbt_model
  - dimension
  - governed_metric
  - aggregate_mart
works_with:
  platforms:
    - duckdb_local
    - motherduck
    - fabric_lakehouse
    - fabric_warehouse
    - redshift
    - databricks
  tools:
    - dbt
    - ossie
qualifiers:
  - Needs marts that already compile; changing a mart, seed or configuration to fit the description is outside this Recipe.
  - Describes the semantic layer only; ontology, data contracts, new metrics and BI export are other Recipes.
  - Checking aggregation needs compiled SQL only; equality and field-type checks need the marts built.
  - Defining new governed metrics from approved definitions over a gold fact is governed-metrics-in-semantic-model.
related:
  - governed-metrics-in-semantic-model
  - bi-calculations-to-governed-metrics
  - metric-population-and-rollups
  - fabric-direct-lake-semantic-model
evidence:
  features:
    - capturing-requirements
    - designing
    - planning
    - semantic-model
    - validating-semantic-model
    - running-dbt-in-sandbox
    - verifying
  evals: []
---

## Prompt

Describe <mart_scope> as a governed Ossie semantic model, so analysts and BI tools can learn what each table is, what one row stands for and how its numbers roll up without reading the SQL. Inherit the Intent's repository, platform, Domain, marts and approved requirements, and resolve only the semantics they leave open. Deliver the model documents, with each aggregate mart approved as a rollup bound to the detail it summarises at its own stated population; every mart in scope either described or named with the reason it cannot be, inside the documents; and proof that each aggregate binding rolls up the way its compiled SQL computes the column, that each aggregate described as a rollup equals the detail over its own population, and that every described field exists in the warehouse with a compatible type. Change no mart.

## Verified by

- Every mart in the approved scope is described or named with the reason it is not, no mart is both, and the counts add up to the scope; each exclusion names what in the mart's SQL or data defeats an honest description, and a mart that can be described is not excluded for convenience.
- The model describes each detail fact in scope with the dimensions it reaches, or states that none is in scope; an aggregate whose detail is out of scope is recorded as not described, never described as a rollup of nothing.
- Each described table states its row grain as approved; where that differs from the grain the mart declares, the difference is reported with its evidence.
- Each aggregate described as a rollup states the population it covers, and each additive measure in it equals the same measure recomputed independently from the detail over that population, within the approved tolerance.
- A mart whose rows depend on a group-level floor, a lossy or inverted join, or a population the detail cannot state is never described as a rollup of the detail; it is excluded or kept outside the rollup claim as approved, with its own population stated.
- A column that averages, takes a median, ranks, windows over rows, counts distinct values or holds a balance is never described as a total across levels; it is recomputed at each level or refused.
- A rate is formed after aggregation from its numerator and denominator; each measure states its unit or currency, and amounts in different currencies are never summed.
- Every aggregate described as a rollup is reported proven or unproven against its compiled SQL, with the reason where unproven; an unproven aggregate never counts as agreeing, and a check that examined nothing is not a pass.
- Every field described exists in the built relation with a compatible type; a difference of type class is an error, and a difference within a class is reported as a finding about the mart, not hidden.
- Levels, keys and hierarchies follow the marts' declared keys and the approved intent, not what the data happens to satisfy; a departure the data shows is reported as a finding and the declaration stays as approved.
- Every figure and count a description states equals what the build compared returns, a stated grain the relation does not hold carries its reported difference, no description claims a population or rollup the relation does not show, and a stale build is reported as stale, not compared as current.
- No existing mart, seed or configuration is changed to fit the description, and only the model documents and the tests generated from them change; a mart defect is reported with its evidence, and each check is shown able to fail.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, marts and approved requirements, and resolve only the semantics they leave open. Read the SQL of every mart in scope with its inputs, and route each by what its SQL does: the detail fact with its dimensions, an aggregate that rolls the fact up, a narrower population a row filter states, or a table to leave out with its reason. Measure each mart's actual grain and population against the declared ones and agree what is still open with the user. Author the documents from the SQL, never from names or sibling tables; declare levels from the marts' keys and the approved intent, declare only the metrics the marts already compute or the detail form of the same column, give each an aggregation, and express a rate a mart carries from its parts or refuse it. Where marts are not built, build them apart from published relations and compile them, then run the structural checks, the check of each aggregate binding against the compiled SQL, the generated content and level tests, and the check of every described field against the warehouse catalog. Confirm each check can fail and state which items it examined, and report a mart defect as a finding, never a fix.

### Compose

- capturing-requirements
- profiling-source-data
- designing
- planning
- semantic-model
- validating-semantic-model
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which marts are in scope, such as which schemas or layers, which relations upstream of the boundary stay out, and does a mart built on a different business process share the model, get its own, or stay outside it?
- If unresolved, how is a mart handled whose population the detail cannot state, such as a group-level floor, a lossy or inverted join, rows the detail lacks or a day it does not carry: excluded with its reason, or kept outside the rollup claim with its own population stated?
- If unresolved, which grain does a mart state when its declared and actual grains differ: the actual grain with the declared one named as its rollup, the declared grain, or exclusion?
- If unresolved, which levels, hierarchies and keys does each dimension declare, and does a changing dimension report the version in force at the event or the current one?
- If unresolved, how are rates, averages, medians, windowed columns, distinct counts and balances expressed or refused, which unit or currency does each measure carry, and which metric names and descriptions are official?
- If unresolved, what does each mart's filter mean in business terms, which records count in an aggregate's population, such as a reporting window, billable-only or test records, and are the excluded ones counted with their reason?
- If unresolved, which build or as-of state is compared, and how is a window driven by a variable or the current date pinned, so a mart built before a detail refresh is not read as wrong?
- If unresolved, to what tolerance must recomputed totals match, and what does a column held as floating point mean for it?

### Guardrails

- Do not describe a mart as a rollup of the detail when a group-level floor, a lossy or inverted join, or a population the detail cannot state defines it; record the reason instead.
- Do not edit a mart, seed or configuration to make the description fit; report the defect with its evidence.
- Do not accept a green check without confirming which items it examined; a check with nothing to examine proves nothing.
- Do not declare a level, key or hierarchy because the data happens to satisfy it; declare it from the marts' keys and the approved intent.
- Do not choose the scope, grain, population, tolerance or the disposition of a mart that cannot be described without approval.
- Do not define a new metric no mart computes, or edit an existing ontology or data contract; report where the new documents leave an existing one out of step.
