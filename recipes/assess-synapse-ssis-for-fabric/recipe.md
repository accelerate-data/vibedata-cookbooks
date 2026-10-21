---
id: assess-synapse-ssis-for-fabric
title: Assess a Synapse dedicated pool or SSIS estate for a Fabric rebuild and recommend whether to go
trigger:
  - A Synapse dedicated SQL pool or a set of SSIS packages is due to move to Fabric, and nobody can say what is in it, what each piece would take or what stops it.
  - The move is scoped from a feature checklist or a gut feeling, and the team needs an inventory, an order and a recommendation it can accept or reject.
  - The estate has dynamic SQL, script tasks, cross-database references, protected packages or objects that look unused, and nobody knows which of them block the move.
  - A steering group needs a go, go with named blockers or no-go before any conversion work is funded.
description: Inventory the exported definitions and usage of a Synapse dedicated pool or SSIS estate, give each item a verdict from a Fabric rule table with cited sources, or unconfirmed where no rule matches, a typed blocker where blocked, a complexity class with its drivers and a place in a dependency-ordered wave, and recommend go, go with named blockers or no-go from approved criteria.
pitch: Find out what a Synapse or SSIS estate would take to rebuild on Fabric, what blocks it and whether to go, before anyone converts a line.
job_category: cross-platform
area: re-engineering
readiness: supported
domain_objects:
  - synapse_dedicated_pool
  - ssis_package
  - compatibility_rule
  - migration_wave
  - assessment_report
works_with:
  platforms:
    - duckdb_local
    - motherduck
    - fabric_lakehouse
    - fabric_warehouse
    - redshift
qualifiers:
  - Reads exported definition files and any usage evidence; it never connects to a live pool, SSISDB or Fabric workspace.
  - Fabric support claims come from cited documentation with an as-of date, never from a Fabric run.
  - It assesses and recommends only; conversion, data movement and cutover belong to other Recipes.
  - A protected, unreadable or unmatched item is named as unassessed or unconfirmed, never counted as compatible.
related:
  - legacy-sql-to-dbt
  - stored-procedure-to-dbt
  - fabric-data-pipeline-as-code
evidence:
  features:
    - capturing-requirements
    - verifying
  evals: []
---

## Prompt

Assess <estate_exports>, the exported DDL and SSIS packages of <pool_or_ssis_estate>, together with <usage_export> and any <declared_consumers>, for a rebuild on <fabric_target>. Inherit the Intent's repository, Domain and approved requirements, and resolve only the semantics they leave open. Inventory every item of the approved kinds and their dependencies, then give each item a verdict from a published, sourced rule table (unconfirmed, with no matching rule as its reason, where none matches), its blockers, a complexity class with its counted drivers, a usage class and a place in a dependency-ordered wave. Recommend go, go with named blockers or no-go from approved criteria stated in advance. Keep what cannot be read, resolved or matched visible with its reason, report secrets by location only, and state what the evidence cannot show. Nothing is converted, moved, deployed or retired, and the recommendation is not a pilot plan, a budget or a schedule.

## Verified by

- Every item of the approved kinds appears exactly once under its qualified name with its approved target, counts by kind tie to an independent count of the export files, and anything else or out of scope is shown or counted with its reason as approved, with how many and why.
- Each dependency the definitions declare resolves, under the approved name resolution, to an inventoried item or is listed as unresolved with its source item and the reference that could not be placed (dynamic SQL, an unplaceable name, a missing object); none is dropped.
- A matched item carries one verdict citing its rule, and each rule carries its cited source and as-of date; an item no rule covers is unconfirmed with no matching rule as its reason, no invented rule or citation, reported as uncovered and never compatible, whatever verdict set is approved.
- Every protected, unreadable or unparsed item, and every item read only by a labelled fallback, is listed and counted with its reason, or, as approved, the run stops naming them and gives no recommendation; none is counted as compatible, and a report names the part of the estate it could not read.
- The span the usage evidence covers is stated and an item it cannot cover is classed unknown, never unused; an item with no approved use in a covered window is a candidate for its owner's sign-off, never retired, and declared seasonal or critical status that conflicts with usage is reported.
- Every blocker an item carries is listed with its type, who resolves it and the wave it gates, one marked primary; every item whose verdict needs a decision, is unconfirmed or is unreadable is covered, and blocker counts reconcile with the verdicts.
- Each item carries a complexity class with its counted or measured drivers, recomputing the drivers under the approved rules reproduces every class, and any effort figure comes from stated drivers or calibration the user supplied, never from an invented number.
- Each item sits in one wave and none depends on a resolved item in a later wave; an item with an unresolved dependency is marked as gated by it, dependency cycle members share a named wave, each wave states its entry and exit criteria, and blockers that gate other waves are placed as approved.
- Where the run completes, one recommendation follows from the approved criteria, stated before use, and reproduces from the report's counts; it states the unassessed and unconfirmed counts and the remaining blockers with their gated waves, and has no pilot design, conversion plan, budget or schedule.
- No secret value appears in any output, committed evidence or log; each secret-bearing field is reported by location with an approved remediation class.
- Counts, classes, waves and any recommendation equal values derived independently from the exports and the approved rules, every report figure comes from that analysis, and a value that disagrees with the independent derivation is reported, never absorbed.
- A report states that its totals describe the assessed export as of its export date only, and what the evidence cannot show: Fabric behaviour known only from cited documentation, and consumers, schedulers and reports outside the export unless declared.

## Agent guidance

### Instructions

Inherit the Intent's repository, Domain and approved requirements, and resolve only the semantics they leave open. Work from the exported files only. Read each definition as fully as the tooling allows, keeping every statement or package it cannot read as an item flagged with its reason. Hold the Fabric rules as published data, each with its source and as-of date, apply the approved precedence, list conflicts between rules of equal specificity, and give a construct no rule covers an unconfirmed verdict with no matching rule as its reason and no invented rule or citation. Resolve dependencies statically and list the rest as unresolved. Classify usage over the approved window, derive each class from counted or measured drivers under a published table, order waves by dependency under the approved rules, and derive the recommendation from the stated criteria. Render the report from the analysis output so no figure is typed by hand, derive expected results independently of the analysis, and report what could not be shown.

### Compose

- capturing-requirements
- verifying

### Ask first

- If unresolved, which item kinds and objects are in scope, which excluded items (system, temporary, test, staging) are listed or only counted, which Fabric target applies to each, how names and usage rows link to items, and at what item level are counts stated?
- If unresolved, which Fabric documentation counts as authoritative and as of what date, what verdict set and meanings apply, and which rule wins when several match (a construct no rule covers is unconfirmed in any set)?
- If unresolved, over what window is use measured, which access counts as use and what minimum, how are declared seasonal windows and critical status treated against silence, and who signs off a retirement candidate when an item has no owner?
- If unresolved, which drivers and thresholds set a complexity class, and is effort expressed as a class only or with calibration data you supply?
- If unresolved, which blocker types apply, who resolves each, which verdicts count as blocked, and which blocker is primary when several apply to one item?
- If unresolved, how are waves ordered beyond dependency, what floor a verdict sets, where blockers that gate other waves are placed, which priority breaks ties, and what must hold to enter and leave each wave?
- If unresolved, what makes an item load-bearing or heavily used, which declared consumers outside the export count, and what thresholds separate go, go with named blockers and no-go?
- If unresolved, are protected, unreadable or unparsed items listed and counted or does the run stop naming them, who supplies the access that would let them be read, and which remediation classes apply to secret-bearing fields?

### Guardrails

- Do not report an item compatible because no rule matched, a parser skipped it or its content could not be read.
- Do not drop, merge or count as handled a dependency, statement or package the analysis cannot resolve or read; list it with its reason.
- Do not copy a connection string, password or other secret value into any output; report its location and a remediation class only.
- Do not retire, rename or recommend deleting an object for showing no recent use; report it as a candidate for its owner and report declared seasonal or critical status as declared.
- Do not turn a verdict, class or wave into a person-day, cost or schedule figure unless the user supplies the calibration it rests on.
- Do not connect to a live pool, SSISDB or Fabric workspace, convert code, move data or deploy anything; state Fabric behaviour as documented, with its source date.
- Do not present the totals of a sample or partial export as the whole estate's.
