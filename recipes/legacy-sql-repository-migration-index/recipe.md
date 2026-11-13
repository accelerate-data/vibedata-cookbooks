---
id: legacy-sql-repository-migration-index
title: Index a legacy SQL repository's objects and dependencies for migration planning
trigger:
  - A legacy warehouse's SQL, or a DDL snapshot, is committed to a repository and nobody can say what objects exist or what depends on what before migration scope is chosen.
  - The team needs the tables, views, procedures and functions found, with what reads, writes or calls each, before it picks what to migrate first.
  - The repository holds duplicate definitions, objects with no definition, string-built SQL or files that do not parse, and the team needs them listed, not guessed.
description: Scan the SQL files of a legacy repository at a named revision without changing them, index its tables, views, procedures and functions and the reads, writes and calls between them with source evidence, and report what cannot be resolved, the dependency order, blockers and candidate migration scopes.
pitch: Know what a legacy SQL repository holds and what depends on what, with evidence and honest gaps, before anyone picks a migration scope.
job_category: re-engineer
area: re-engineering
readiness: planned
function:
  - cross-functional
domain_objects:
  - legacy_sql
  - database_object
  - stored_procedure
  - procedure_call_graph
  - table_writer_map
  - inventory_report
  - migration_plan
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
  - Planned until a product parser splits and classifies routine bodies and calls in T-SQL, PL/SQL and PL/pgSQL.
  - Reads files in the Intent's repository; a live database is inventory-legacy-database-over-mcp.
  - Fabric verdicts and a go or no-go for a Synapse or SSIS export belong to assess-synapse-ssis-for-fabric.
  - Stops at the index and candidate scopes; plans, dispositions, conversion and Intents are other Recipes.
  - Business-domain ownership of tables and views is not assigned; the index is an engineering input.
  - A dialect the scan cannot read is reported unparsed, never guessed or skipped.
  - Static reading cannot show runtime behaviour, string-built targets or objects created outside the repository.
related:
  - inventory-legacy-database-over-mcp
  - plan-legacy-procedure-package-intents
  - plan-legacy-warehouse-layers-to-dbt-intents
  - stored-procedure-to-dbt
  - legacy-sql-to-dbt
  - assess-synapse-ssis-for-fabric
evidence:
  features:
    - capturing-requirements
    - verifying
  evals: []
---

## Prompt

Index the SQL in <repository_path> at <repository_revision> for migration planning: list its tables, views, procedures and functions, the reads, writes and calls between them, what cannot be resolved or parsed, and the dependency order, blockers and candidate migration scopes with what each needs first, and, where a comparison is wanted, what changed since <earlier_index>. Read the files only and change none of them. Inherit the Intent's repository, Domain and approved requirements, resolve only the semantics they leave open, and commit the index (machine-readable where approved) and the report to the repository with the file and line behind every entry and a statement of what a static reading cannot prove. Convert nothing, migrate nothing and open no Intents.

## Verified by

- The report names the revision scanned, the approved scan boundary and each file's dialect; every file in the boundary has a disposition (indexed, parse failure, or not SQL or excluded with its reason), and the file, object and dependency counts reconcile to the listed rows.
- Every table, view, procedure and function the parsed files define is listed with its name as written and, where the dialect allows overloading, signature, type, file and line; a name defined more than once shows every definition and file and follows the approved handling, none dropped.
- Where files are ordered migration scripts, each object shows its state after the last script with the statements that altered, renamed or dropped it, and a reference to a dropped or renamed-away object is listed unresolved, never resolved.
- Each read, write and call cites its file and line and shows its direction, so upstream inputs can be told from downstream consumers; no dependency rests on a comment or a name alone.
- Undefined objects, string-built statements with no fixed target, unclassified statements and unparsed files are listed, or counted out as approved, with what they affect; an unknown dependency is never shown as none, and an unparsed file's apparent dependencies are never shown as confirmed.
- For each entry routine, the writes reached through the routines it calls are shown apart from its direct dependencies and traced to the dependencies that cause them, within the approved reach.
- Dependency order, cycles and blockers are reported, and each candidate migration scope lists what it needs first; a scope that omits a prerequisite or hides a blocker fails.
- The objects and dependencies equal an expectation derived independently from the same files, over the boundary or an approved sample covering every statement and object kind found, stated as such; an unresolved item or object cannot drop out of the comparison unnoticed.
- A second scan of the same revision and inputs gives the same semantic inventory; against an earlier index, a changed file gives a difference naming each object or dependency added, removed or moved and why, and a shift in line numbers alone is a move.
- A run stopped under an approved rule names each offending file or statement and its reason and claims no index or scopes it did not produce; the other bullets hold for a completed run.
- The reports sit at the approved location and state the revision, the open owner questions and what a static scan cannot establish, such as runtime behaviour and objects created outside the repository; completeness is claimed only for the files, revision, parser limits and checked sample stated.
- No scanned file is changed, nothing outside the approved boundary is read, and credentials and personal literals found in definition text appear by location only, unless quoting is approved.

## Agent guidance

### Instructions

Inherit the Intent's repository, Domain and approved requirements, and resolve only the semantics they leave open. Fix the revision and boundary first, determine each file's dialect and say how it was determined. Split each file into statements and classify them, derive reads, writes and calls from the definition text alone, cite file and line, and check every target against the defined objects, as they stand after the last script where files are ordered migration scripts, so an undefined, dropped or renamed-away one is listed. Build the index by a repeatable process with stable ordering, so a rerun and a comparison between runs mean something. Write the expected objects and dependencies from the files independently, over the boundary or the approved sample, before trusting the result, and show on throwaway copies that the comparison fails when a dependency is removed, added or reversed, an object is missing or an unresolved item is dropped. Exercise inputs the files do not show, such as statements sharing a line, shifted line numbers and references to undefined objects. Never change the source. State what a static reading cannot prove and what the owner still has to settle.

### Compose

- capturing-requirements
- verifying

### Ask first

- If unresolved, which paths and revision are in scope, which dialect each path uses, and what happens to files that are not SQL or sit in generated or tool folders: read, or excluded with a reason?
- If unresolved, which object kinds count, such as triggers, synonyms, packages and sequences, and how names resolve when they carry no schema, other quoting or case, or deploy-time variables: as written, by a default, by supplied values or listed unresolved?
- If unresolved, which routines are entry points (named, or every routine nothing in the boundary calls), what counts as a dependency, how far calls are followed from them, do temporary tables and string-built SQL count, and who is credited with a write reached through a call?
- If unresolved, whether files are ordered migration scripts whose later ALTER, DROP or rename change an object or one definition per object, and how an object defined more than once is handled: all listed as a conflict, one chosen by a stated rule, or stop and ask?
- If unresolved, what a file that does not parse or a statement the scan cannot classify does to the run: continue and list, or stop, and how its apparent dependencies are shown?
- If unresolved, how candidate migration scopes are formed and ordered, such as by entry routine, schema or folder, or one per object, and which findings count as blockers?
- If unresolved, where the reports go, whether definition text is quoted or only cited by file and line, whether a machine-readable index is kept, and is the independent check run over the whole boundary or an approved sample?

### Guardrails

- Do not change, reformat or move any scanned file, and do not read outside the approved boundary.
- Do not infer a dependency from a name or a comment; cite the definition text.
- Do not report an unknown dependency as none, an unparsed file as empty, or an object kind as absent because the scan cannot read it.
- Do not choose between duplicate definitions or credit a write reached through a call without an approved rule.
- Do not convert objects, start a migration, open Intents or assign business-domain ownership.
- Do not claim completeness beyond the files, revision and parser limits stated.
- Do not commit credentials or personal literals found in definitions beyond their location unless quoting is approved.
