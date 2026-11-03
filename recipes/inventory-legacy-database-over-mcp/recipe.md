---
id: inventory-legacy-database-over-mcp
title: Inventory and profile a legacy SQL Server, Oracle or PostgreSQL database over MCP
trigger:
  - A legacy SQL Server, Oracle or PostgreSQL database is due to be re-engineered and nobody can say which routines call which, or which objects write each table.
  - A set of stored routines has to be planned object by object, and the plan needs the objects, callers, writers and the shape of the data first.
  - The estate has dynamic SQL, nested calls, tables with two writers or objects nothing calls, and the team needs them found before any conversion starts.
description: Read a legacy SQL Server, Oracle or PostgreSQL database through its connected MCP and report its objects, the call graph from each entry routine, the objects that write each table and a profile of the tables the entry routines touch, without issuing any statement that changes the source.
pitch: Find out what a legacy database holds, who calls and writes what, and what its data looks like, before anyone plans a rebuild.
job_category: re-engineer
area: re-engineering
readiness: supported
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
  - Planning, conversion and loading belong to other Recipes.
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

Inventory and profile <legacy_database> through its connected MCP before it is re-engineered: list its objects, the call graph from each <entry_routine>, the objects that write each table, then sample and profile the tables the entry routines touch. Read the database through the MCP only and issue no statement that changes it. Inherit the Intent's repository, Domain and connected sources, resolve only the semantics they leave open, and deliver an inventory that cites the query or definition text behind every figure and states what it cannot prove.

## Verified by

- Every in-scope object of an approved kind is listed with schema, kind, stored name and, if repeated, signature; tables carry a row count labelled exact or catalog estimate as approved, or the reason none was taken; out-of-scope ones are counted with their rule; an absent kind names its view.
- Each entry routine's call graph shows each caller-callee pair once, to the approved depth, cycles marked; each call is cited to definition text and resolved to one listed object by the definition's own name resolution or unresolved; a hidden or unreadable call is found or unresolved, never dropped.
- Each table lists the objects that write it and the statement kind under the approved writer definition; a transitive write is shown against the writing object, its entry routine or both, or marked unresolved, as approved.
- A table with two writers is visible; a table with no writer found is shown as none in the readable definitions, and as unassessed where an unreadable object, a string-built statement whose target the text does not fix, or a writer outside the database could write it.
- A second reading made a different way is compared with the first; each difference in the calls or writers is reported with its cause, and neither reading is resolved silently, and the second is not claimed to prove completeness.
- Touched tables follow the approved definition, and one outside it is shown with the reason; each table the approved limits cover carries the approved profile, labelled a sample where it is one, and one left unprofiled (limit, no read access) shows the reason; samples are never stated as table-wide.
- Every figure and edge cites the query or definition text it came from and equals what that query returns or that text shows.
- No value of a column marked sensitive appears in the inventory or its citations, ranges and frequent values included, and the statement record shows no candidate column's values read before the owner answered; credentials in definition text appear only by location, personal literals as approved.
- Only reads reached the source, shown by a statement record listing every statement sent: no statement changing data, schema or settings was issued and no user routine that could was called; any change between reads, or one the reads themselves cause, is reported as source activity.
- Anything the profile shows that would change a rebuild, such as join coverage, duplicate grain or empty tables, is reported with its measurement and left uncorrected.
- In-scope objects with no caller found in the readable definitions are listed as such with the evidence read, and are not reported as unused.
- The inventory is delivered where approved, states when the source was read, and names what it cannot prove, such as runtime behaviour, objects the login cannot read, encrypted or wrapped definitions and writers outside the database.

## Agent guidance

### Instructions

Inherit the Intent's repository, Domain and connected sources, and resolve only the semantics they leave open. Confirm the MCP connection reaches the intended database and record what the login can do, since read-only comes from the login and not from the server, and keep a record of every statement sent to the source. Read the engine's own catalog for the objects and the definition text of each routine and view in scope, using the catalog views that show everything the login may read, since a view that shows only what the login can use hides objects it cannot run, and note any definition it cannot read. Derive calls and writes from that text, including statements built as strings where the approved writer definition counts them, and cite the text; names and comments are not evidence. Repeat the derivation a second way and report every difference with its cause; where the engine keeps no usable dependency catalog for routines, say so, and re-derive from the text a different way, stating that this tests extraction, not completeness. Profile the touched tables with bounded read-only queries at the approved depth, label sampled figures and how the sample was drawn, and handle sensitive columns as approved. Report any change the reads themselves cause, such as statistics the engine creates for profiling queries, as source activity and leave it in place. State what the inventory cannot prove.

### Compose

- capturing-requirements
- verifying

### Ask first

- If unresolved, which schemas and object kinds are in scope, such as routines, functions, packages, triggers, synonyms and materialized views, and which routines are entry points?
- If unresolved, which tables count as touched by the entry routines: written only, also read, and also reached through views, synonyms, triggers, other databases or dynamic SQL?
- If unresolved, what counts as a writer, direct statements only or also triggers, views and string-built statements, how far are calls followed, and is a transitive write credited to the writing object, its entry routine or both?
- If unresolved, how are references the definitions hide or the login cannot read treated: listed as found from the text, listed as unresolved, or does the run stop and ask?
- If unresolved, which columns are sensitive: the agent proposes candidates by name and shape and reads no values until the owner answers; are they excluded, masked or shape only, and are personal literals in definition text redacted?
- If unresolved, how deep is the profile, are rows counted exactly or by catalog estimate, and what row, time or load limit and run window apply, including tables backed by another system?
- If unresolved, may the run proceed on a login that can write, or stop until a read-only login is supplied?
- If unresolved, where does the inventory land, in the conversation only or also as a report in the repository, and may definition text be quoted or committed, or only referenced by object and line?

### Guardrails

- Do not issue a statement that changes data, schema or settings or call a user routine that could; if the login could write, say so and issue only read-only statements.
- Do not read the source with local client tools or scripts; the connected MCP is the only route.
- Do not infer a call or a writer from a name or a comment; cite the definition text.
- Do not drop an object, call or writer the text shows, or one the login cannot read, and do not report an object kind absent because a view the login can use does not show it; list it as unresolved or unassessed.
- Do not state a sampled figure as a property of the whole table, and do not scan a large table beyond the approved limit.
- Do not treat an unmarked column as non-sensitive when its name or content suggests otherwise; ask, read no value of a candidate column before the answer, and print no raw value of a sensitive column.
- Do not plan, convert or load objects here, and do not correct a defect the profile finds; report it.
- Do not treat an empty table, missing history or an absent caller as proof that an object never ran or is unused.
