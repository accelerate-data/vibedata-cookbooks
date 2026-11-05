---
id: plan-legacy-warehouse-layers-to-dbt-intents
title: Plan a legacy warehouse layer by layer through its reports and open a requirements-only Intent per unit
trigger:
  - A legacy SQL Server, Oracle or PostgreSQL warehouse is moving to dbt from a landed layer up through dimensions, facts and reports, and nobody holds one plan for the whole chain.
  - Procedures load the layers but only some are reached from one entry routine, and the team needs every object, writer and reader in layer order before converting any.
  - Some targets are empty or already ported elsewhere, so the team needs to know what each layer can be checked against and who owns the overlap.
description: Plan a legacy warehouse from the layer the owner names as its entry through its reports, read over MCP without changing anything, with each object's type, writers, readers and dbt target in layer order and how each layer is checked, then open one Intent per approved unit that stops at approved requirements.
pitch: Turn a legacy warehouse into a layer-ordered migration plan and requirements-only Intents, before anyone converts an object.
job_category: re-engineer
area: re-engineering
readiness: planned
function:
  - cross-functional
domain_objects:
  - legacy_database
  - database_object
  - stored_procedure
  - table_writer_map
  - migration_plan
  - migration_unit
  - requirements_document
  - dbt_model
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
    - sql_server
    - oracle
    - postgresql
qualifiers:
  - Reads SQL Server and Oracle through Google MCP Toolbox for Databases and PostgreSQL through postgres-mcp.
  - None of these MCP servers enforces read-only access by default; a login that can write needs the owner's approval.
  - The entry layer is the owner's choice; layer words such as silver and gold mean different things in different estates.
  - Covers every approved chain object, including ones no entry routine reaches; one routine's package is a sibling Recipe.
  - Stops at approved requirements; building models and proving parity belong to the conversion Recipes.
  - An empty legacy target has no output to compare; its check follows the approved basis.
  - Writers outside the database and objects the login cannot read are named unassessed.
  - Inherits an approved inventory where one exists and adds layer order and the per-unit Intents.
related:
  - plan-legacy-procedure-package-intents
  - inventory-legacy-database-over-mcp
  - stored-procedure-to-dbt
  - legacy-sql-to-dbt
  - scd-procedure-to-dbt-snapshot
  - materialized-view-to-dbt
evidence:
  features:
    - capturing-requirements
    - designing
    - planning
    - verifying
  evals: []
---

## Prompt

Plan <legacy_database> on the connected <source_engine> MCP for re-engineering as dbt models, from <entry_layer> through the reports, reading it through the MCP only and changing nothing in it. Inherit the Intent's repository, Domain, connected sources and approved requirements, and resolve only the semantics they leave open. Deliver one plan that lists every object in the chain in layer order with its type, the writers of each table it touches, its readers and callers, and what it becomes in dbt, then say how each layer is checked, on the approved basis, and what that check can and cannot prove about parity, name the objects an existing model already covers with their owners, and open one Intent per approved unit, or reuse one already open where approved, each stopping once its approved requirements name the dbt model and the agreed tests, traced to the legacy behaviour they check. Measure every figure on this engine's own definitions and data, reproduce legacy behaviour as approved and raise each defect separately, and state what the plan cannot prove.

## Verified by

- The plan lists every object in the approved chain once, in layer order and in dependency order within a layer, cycles marked, with its type; the object counts equal an independent read of the source catalog, and objects outside the chain are named.
- Every table shows each writer, inside or outside any entry routine, with statement kinds read from definition text including built statements, or says no writer was found in the readable definitions; it never says the table is never written.
- Every object shows who calls or reads it, or that nothing readable does and what that does not prove; objects no entry routine reaches are listed, and a call or write the catalog cannot see is reported beside the catalog's own reading.
- Each object has one disposition, the dbt artifact it becomes with kind, layer and name, or the reason it becomes none; an object an existing model covers names that model and its owner, and this run deletes or renames nothing existing.
- Each layer states its check per the approved basis, naming inputs and comparison, or that none exists; no check rests on a row count alone, a shape-only check is reported as proving no parity, and an empty target is stated with its measured count and never cited as legacy rows.
- Every measured figure cites the query or definition behind it and equals what that query returns; a figure from a procedure's own select over defined inputs says so, and a figure measured on live data is never presented as a test result.
- Where a table's contents disagree with its loader, or an engine behaviour changes a result, the plan reports both with the measurement and states which the approved rule treats as the promise and what the target must do to keep it.
- Each object with a dbt disposition is covered by an Intent of the approved unit, or listed as not yet opened with the approved reason; none is left uncovered, and one covered twice shows the approved reason.
- Each opened Intent stops at requirements naming the dbt models, each upstream it reads with its supplier, and tests whose expected values the plan measures or proves; none designs or builds.
- Legacy behaviour is reproduced as approved, including behaviour that looks like a defect; each defect is raised separately with its measured effect, and each approved correction is recorded as its own change.
- A record lists every statement sent to the legacy database and each is a read; no routine is called and nothing in the database changes.
- Anything the plan cannot prove is stated, such as loaders outside the database, unreadable definitions, missing run history or behaviour only defined inputs reach.

## Agent guidance

### Instructions

Inherit the Intent's repository, Domain, connected sources and approved requirements, and resolve only the semantics they leave open. Read the catalog and every definition in the chain through the MCP with reads only, and follow calls and writes in the definition text, including built statements; compare the catalog's reading with the text's and report each difference. Order the objects by layer and by dependency measured from the definitions, not from names, and record each layer's inputs and consumers. Measure each figure on this engine's own definitions and data within the approved load limits, and where a target is empty measure what the procedure's own select returns over defined inputs and say so. Compare each table's contents with what its loader would produce. Check the engine behaviours that change results and record what the target must do to keep each. Give each Intent its object's plan section and the approved decisions, since an Intent cannot see an unmerged plan. Settle the entry layer, the Intent unit, the overlap with existing models, the check basis and the parity rule with the user before planning, audit each requirements document against the source before it is approved, and stop each Intent there.

### Compose

- capturing-requirements
- designing
- planning
- verifying

### Ask first

- If unresolved, which layer is the entry and what forms the chain: schemas, views, synonyms, links, other databases, triggers, scheduler jobs, objects no entry routine reaches and the entry routine itself.
- If unresolved, what counts as a writer or reader, including triggers, called routines, external loaders and report tools, and how an object that spans or skips layers is assigned.
- If unresolved, the Intent unit, per procedure, per written table or a named group, which objects open now and in what order, whether an existing Intent is reused, and who authors the staging views, sources and shared upstream models each reads.
- If unresolved, how objects an existing model already covers are treated, named and escalated, extended or rebuilt, and who decides which of several ports survives.
- If unresolved, what each layer's check uses where a target is empty or disagrees with its loader, defined inputs replayed, a copy of legacy data with a named owner and cleanup, or shape only, and whether the loader or the live contents is the promise.
- If unresolved, the parity rule: reproduce legacy exactly or correct named behaviours as recorded changes, and whether surrogate key values are compared.
- If unresolved, how clock- and history-dependent logic is checked: a pinned, run-supplied or legacy clock, incremental or full load, the time zone, prior state or empty, and how SCD, deleted and late rows compare.
- If unresolved, the load, locking or time window the legacy database may take, whether the run proceeds on a login that can write, and whether sensitive columns appear as shape only or as values.

### Guardrails

- Do not run a query beyond the approved load limits; record the figure as unmeasured instead.
- Do not send a statement that writes, even one that matches no rows or would be refused, or call any procedure in the legacy database; read through the MCP only.
- Do not copy legacy or Domain data into a committed file unless the user approves it.
- Do not treat catalog dependency metadata as the complete call or write graph; built statements hide calls and writes.
- Do not show sensitive column values beyond what is approved.
- Do not describe a figure from an empty legacy table as its contents, or claim parity against rows that do not exist.
- Do not repair a legacy defect the approved parity rule keeps, or settle a choice Ask first lists; raise the defect and ask.
- Do not delete, rename or rebuild an existing model yourself, or decide which of several ports survives.
- Do not map one estate's layer words onto another's; use the layer names the approved chain defines.
- Do not let an opened Intent design, build or ship.
