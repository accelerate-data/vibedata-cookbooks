---
id: inventory-legacy-database-over-mcp
title: Inventory a legacy SQL Server, Oracle or PostgreSQL database over MCP and plan its migration
trigger:
  - A legacy SQL Server, Oracle or PostgreSQL database is due to be re-engineered and nobody can say which routines call which, or which objects write each table.
  - A set of stored routines has to be planned object by object, and the plan needs the objects, callers, writers and the shape of the data first.
  - The estate has dynamic SQL, nested calls, tables with two writers or objects nothing calls, and the team needs them found before any conversion starts.
description: Read a legacy SQL Server, Oracle or PostgreSQL database through its connected MCP, report its objects, call graph, table writers and profile without changing the source, then plan its migration by units, order and what each object becomes.
pitch: Find out what a legacy database holds, who calls and writes what, and what its data looks like, then get a saved plan for migrating it.
job_category: re-engineer
area: re-engineering
readiness: planned
function:
  - cross-functional
domain_objects:
  - legacy_database
  - database_object
  - stored_procedure
  - legacy_sql
  - procedure_call_graph
  - table_writer_map
  - table_profile
  - inventory_report
  - migration_plan
  - migration_unit
works_with:
  platforms:
    - duckdb_local
    - motherduck
    - fabric_lakehouse
    - fabric_warehouse
    - redshift
    - databricks
  tools:
    - sql_server
    - oracle
    - postgresql
qualifiers:
  - Reads over a connected MCP server only, such as Toolbox for SQL Server and Oracle or postgres-mcp for PostgreSQL.
  - A login that can write or run routines is reported; whether the run proceeds on it is approved.
  - Exported definition files are out of scope; a Synapse or SSIS estate bound for Fabric is assess-synapse-ssis-for-fabric.
  - It profiles tables to understand them, not to reconcile a load, which database-tables-to-bronze covers.
  - Planning stops at an approved plan; converting objects and loading are other Recipes.
  - Writers outside the database, and objects the login cannot read, are named unassessed.
related:
  - stored-procedure-to-dbt
  - legacy-sql-to-dbt
  - assess-synapse-ssis-for-fabric
  - database-tables-to-bronze
evidence:
  features:
    - capturing-requirements
    - verifying
  evals: []
---

## Prompt

Inventory and profile <legacy_database> through its connected MCP before it is re-engineered, then plan its migration: list its objects, the call graph from each <entry_routine>, the objects that write each table, profile the tables the entry routines touch, then group the objects into migration units, order them and propose what each becomes. Read the database through the MCP only and issue no statement that changes it. Inherit the Intent's repository, Domain and connected sources, resolve only the semantics they leave open, and commit the inventory and the plan to the repository as reports that cite the query or definition text behind every figure and state what they cannot prove. Convert and load nothing and open no further Intents.

## Verified by

- Every in-scope object of an approved kind is listed with schema, kind, stored name and, if repeated, signature; tables carry a row count labelled exact or catalog estimate as approved, or the reason none was taken; out-of-scope ones are counted with their rule; an absent kind names its view.
- Each entry routine's call graph shows each caller-callee pair once, to the approved depth, cycles marked; each call is cited to definition text and resolved to one listed object by the definition's own name resolution or unresolved; a hidden or unreadable call is found or unresolved, never dropped.
- Each table lists its writers and statement kinds under the approved writer definition, transitive writes as approved or unresolved; two writers are visible; none found is shown as none in the readable definitions, or unassessed where an unreadable, string-built or outside writer could write it.
- A second reading made a different way is compared with the first; each difference in the calls or writers is reported with its cause, and neither reading is resolved silently, and the second is not claimed to prove completeness.
- Touched tables follow the approved definition, and one outside it is shown with the reason; each table the approved limits cover carries the approved profile, labelled a sample where it is one, and one left unprofiled (limit, no read access) shows the reason; samples are never stated as table-wide.
- Every figure and edge cites the query or definition text it came from and equals what that query returns or that text shows.
- No value of a column marked sensitive appears in the inventory or its citations, ranges and frequent values included, and the statement record shows no candidate column's values read before the owner answered; credentials in definition text appear only by location, personal literals as approved.
- Only reads reached the source, shown by a statement record listing every statement sent: no statement changing data, schema or settings was issued and no user routine that could was called; any change between reads, or one the reads themselves cause, is reported as source activity.
- Anything the profile shows that would change a rebuild is reported with its measurement and left uncorrected in the source; objects with no caller found in the readable definitions are listed with the evidence read, never called unused.
- Each object in the approved plan scope is in exactly one migration unit, none unassigned or duplicated; each unit lists its objects and dependencies. Objects outside that scope are labelled outside the approved scope with its rule; unreachable or unreadable ones are placed or unassessed.
- Each unit follows every unit it depends on unless a stated reason says otherwise, with an entry and exit criterion per step; each in-scope object has an approved disposition and target form with its reason, and a defect found is carried or fixed as approved, never silently.
- The inventory and the plan are committed to the repository as reports a later step can read, each stating when the source was read, any read beyond the inventory, the plan's open owner questions, and what it cannot prove, such as runtime behaviour and writers outside the database.

## Agent guidance

### Instructions

Inherit the Intent's repository, Domain and connected sources, and resolve only the semantics they leave open. Confirm the MCP connection reaches the intended database, record what the login can do (read-only comes from the login, not the server), and keep a record of every statement sent. Read the engine's catalog and each in-scope routine and view definition through the views that show everything the login may read, since a view limited to what the login can use hides objects, and note any definition it cannot read. Derive calls and writes from that text, including string-built statements where the approved writer definition counts them, and cite it; names and comments are not evidence. Repeat the derivation a second way and report each difference with its cause; where the engine keeps no usable routine dependency catalog, say so and re-derive from the text, stating this tests extraction, not completeness. Profile touched tables with bounded read-only queries, label samples, handle sensitive columns as approved, and report read-caused changes such as engine-created statistics as source activity. Build the plan from the saved inventory: read the source only where it leaves something open, date and attribute any such read, group, order and assign dispositions as approved, and state what it cannot prove.

### Compose

- capturing-requirements
- verifying

### Ask first

- If unresolved, which schemas and object kinds are in scope, such as routines, functions, packages, triggers and synonyms, which routines are entry points, and which tables count as touched: written only, also read, or also reached through views, triggers or dynamic SQL?
- If unresolved, what counts as a writer (direct statements, triggers, views, string-built), how far calls are followed, who is credited with a transitive write, and how hidden or unreadable references are treated: found from text, unresolved, or stop and ask?
- If unresolved, which columns are sensitive: the agent proposes candidates by name and shape and reads no values until the owner answers; are they excluded, masked or shape only, and are personal literals in definition text redacted?
- If unresolved, how deep is the profile, are rows counted exactly or by catalog estimate, and what row, time or load limit and run window apply, including tables backed by another system?
- If unresolved, may the run proceed on a login that can write, or stop until a read-only login is supplied?
- If unresolved, where in the repository does the inventory report go, and may definition text be quoted or committed in it, or only referenced by object and line?
- If unresolved, how are objects grouped into migration units (load path, layer, subject area or one per object), in what order do they migrate (dependency, call-graph or value or risk first), and which dispositions may an object take (model kind, orchestration only, out of scope, retire)?
- If unresolved, is a defect the inventory finds, such as row loss or colliding keys, reproduced, fixed or flagged for a separate decision, and does the plan cover the whole estate or only part, the rest being labelled outside the approved scope?

### Guardrails

- Do not issue a statement that changes data, schema or settings or call a user routine that could; if the login could write, say so and issue only read-only statements.
- Do not read the source with local client tools or scripts; the connected MCP is the only route.
- Do not infer a call or a writer from a name or a comment; cite the definition text.
- Do not drop an object, call or writer the text shows, or one the login cannot read, and do not report an object kind absent because a view the login can use does not show it; list it as unresolved or unassessed.
- Do not state a sampled figure as a property of the whole table, and do not scan a large table beyond the approved limit.
- Do not treat an unmarked column as non-sensitive when its name or content suggests otherwise; ask, read no value of a candidate column before the answer, and print no raw value of a sensitive column.
- Do not convert or load objects, open Intents or write requirements here, and do not choose grouping, order or disposition without approval; never correct a defect in the source, report it, and record whether the port reproduces, fixes or flags it as approved.
- Do not treat an empty table, missing history or an absent caller as proof that an object never ran or is unused.
