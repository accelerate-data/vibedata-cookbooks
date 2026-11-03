---
id: plan-legacy-procedure-package-intents
title: Plan a legacy procedure package and open one requirements-only Intent per object
trigger:
  - A legacy SQL Server, Oracle or PostgreSQL warehouse is moving to dbt, and its loads run as packages of procedures that one routine calls in order.
  - The team wants to convert a package object by object, but first needs to know every object in it, what writes each table and what each object becomes.
  - Each object needs agreed requirements, the dbt model and the tests, before anyone builds it.
description: Plan the procedures, views, materialized views and other objects that one legacy routine runs, read over MCP without changing anything, with each object's type, the writers of each table, its callers and what it becomes in dbt, then open, or reuse where approved, one Intent per object that stops at approved requirements naming the dbt models and the agreed tests.
pitch: Turn a legacy procedure package into a measured plan and one requirements-only Intent per object, before anyone converts a line.
job_category: re-engineer
area: re-engineering
readiness: planned
function:
  - cross-functional
domain_objects:
  - stored_procedure
  - legacy_sql
  - materialized_view
  - migration_plan
  - requirements_document
  - dbt_model
  - follow_up
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
  - None of these MCP servers enforces read-only access as shipped; a login that can write needs the owner's approval.
  - A package here is the set of objects one entry routine runs, not an Oracle PL/SQL package.
  - Stops at approved requirements; building and proving parity belong to the conversion Recipes.
related:
  - stored-procedure-to-dbt
  - legacy-sql-to-dbt
  - materialized-view-to-dbt
  - scd-procedure-to-dbt-snapshot
  - scalar-sql-function-to-dbt-macro
  - assess-synapse-ssis-for-fabric
evidence:
  features:
    - capturing-requirements
    - designing
    - planning
    - verifying
  evals: []
---

## Prompt

Plan the legacy package that <entry_routine> runs in <legacy_database> on the connected <source_engine> MCP, for re-engineering as dbt models on the Domain's platform or an approved target, reading it through the MCP only and changing nothing in it. Inherit the Intent's repository, Domain, connected sources and approved requirements, and resolve only the semantics they leave open. Deliver a package plan that lists every procedure, view, materialized view and other object in the package with its type, the writers of each table it touches, its callers and what it becomes, then open one Intent per object as the approved unit defines it, or reuse one already open where approved, each stopping once its approved requirements name the dbt models and the agreed tests, traced to the legacy behaviour they check. Measure every figure on this engine's own definitions and data, reproduce legacy behaviour as approved and raise each defect separately, and state what the plan cannot prove.

## Verified by

- The plan lists every object reached from the entry routine within the approved boundary, including calls made through dynamic SQL, with type, callers and depth; a call whose target the text cannot resolve is listed unresolved with its statement, and objects outside are named.
- Every table the package reads or writes shows each writer, inside or outside the package, with its statement kinds, from the definition text; a second reading made another way is compared, each difference or unresolved write is reported, and agreement is not claimed as completeness.
- Each object in the boundary has one disposition, the dbt artifact it becomes or the reason it becomes none; each with a dbt disposition is covered by exactly one per-object Intent, opened or reused as approved, and a grouping joins only objects the plan names together for a stated reason.
- Every measured figure in the plan and the requirements comes from this engine's own definitions and data through the MCP, cites its query and equals what that query returns, and says when it is a procedure's own select because the legacy table holds no rows.
- Each requirements document names its dbt models and the agreed tests, traces each test to the legacy behaviour it checks, records the approved answer to each of its open questions, and shows personal values only as approved.
- Legacy behaviour is reproduced as the approved parity rule says, including behaviour that looks like a defect; each defect is raised separately with its measurement, and each approved correction is recorded as its own change.
- Engine behaviour that changes a result is recorded where it applies, with what the target must do to keep it, such as null and empty-string handling, text comparison, grouping over empty input, grouping-level encoding and commit behaviour on failure.
- A tested behaviour the source data cannot exercise, such as a quantity that is always 1 or a guard that never fires, is named and covered by synthetic input or recorded as unverified, as approved.
- Every input the package reads that no object in it writes, and every table it writes that something outside it also writes, has its approved owner or dependency.
- The plan, or the entry routine's Intent where approved, states the run order, which part of it data dependencies enforce, and how a failure leaves the target compared with the legacy, each difference recorded as a behaviour change.
- No per-object Intent designs, builds or ships anything; a record lists every statement sent to the legacy database and each is a read: none would modify data, schema or settings, even matching no rows or refused, no procedure is called, and any change reads cause is reported as source activity.
- Anything the plan cannot prove is stated, such as an unreadable or wrapped definition, an object across a link, a caller in a scheduler the MCP cannot read, missing run history or an empty target.

## Agent guidance

### Instructions

Inherit the Intent's repository, Domain, connected sources and approved requirements, including any approved database inventory, and resolve only the semantics they leave open. Read the catalog and every definition in the package through the MCP with reads only, and follow calls and writes in the definition text, including those built as dynamic SQL; where the text cannot resolve a target, record it unresolved, and compare the graph with a second reading made another way. Keep a record of every statement sent to the legacy database, checked against the call history before verification. Look for triggers on written tables, functions, synonyms, overloads, other databases and scheduler jobs that call the routine, and settle the boundary, the Intent unit, the parameters and modes, and the parity rule with the user before planning. Measure each figure on this engine's own definitions and data within the approved load limits; when a legacy table is empty, measure what the procedure's own select returns and say so. Check the engine behaviours that change results, such as null parts in built strings, text comparison, grouping over empty input and commits on failure, and record what the target must do to keep each. Design and plan the package, open the approved Intents without starting work they do not own, give each one its object, the approved plan and the approved decisions, and audit each requirements document against the source before it is approved, stopping each Intent there.

### Compose

- capturing-requirements
- designing
- planning
- verifying

### Ask first

- If unresolved, which objects form the package: direct calls or the full call closure including dynamic SQL, and whether views it reads, triggers on tables it writes, functions, synonyms, objects in other databases, scheduler jobs, loaders of its inputs and fellow members of a PL/SQL package count.
- If unresolved, how an object that writes several tables, a view used only inside the package, an overloaded routine and the entry routine are covered, by one Intent per object or a named group with its reason, and whether an existing per-object Intent stopped at requirements is reused.
- If unresolved, which parameter values and run modes the package is planned for, and how branches outside them are recorded.
- If unresolved, the parity rule: reproduce legacy exactly or correct named behaviours as recorded changes, whether surrogate key values are a parity target, and whether a stateful load is compared over the legacy's prior state or from empty.
- If unresolved, who owns inputs the package reads but no object in it writes, and tables it writes that something outside it also writes: a declared source, an upstream dependency, or a ported object.
- If unresolved, what load, locking or time window the legacy database may take, and whether the run may proceed on a login that can write or stops until a read-only login is supplied.
- If unresolved, which figures become standing tests and which are verification evidence only, and how behaviour the source data cannot exercise is proven.
- If unresolved, how sensitive columns appear in plans and requirements, such as shape only or values, and whether personal-data governance is in scope or a follow-up.

### Guardrails

- Do not send a statement that writes, even one that matches no rows or would be refused, or call any procedure in the legacy database; read through the MCP only.
- Do not run a query on the legacy database beyond the approved limits on load, locking or time window; record the figure as unmeasured instead.
- Do not take a figure, a join shape or a filter from another engine, environment or documentation for this object; measure this engine's own definition.
- Do not treat catalog dependency metadata as the complete call or write graph; dynamic SQL hides calls and writes.
- Do not describe a figure from an empty legacy table as its contents; say it is what the procedure's own select returns.
- Do not let a per-object Intent design, build or ship, or start work on an object it does not own.
- Do not correct a legacy defect the approved parity rule keeps, or settle an open question Ask first lists; raise the defect and ask.
- Do not copy personal values into a plan or requirements document unless the user approves it.
