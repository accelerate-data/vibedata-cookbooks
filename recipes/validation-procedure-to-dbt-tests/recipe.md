---
id: validation-procedure-to-dbt-tests
title: Convert a validation procedure into dbt tests and source checks that gate the build
trigger:
  - A load runs behind a stored procedure that checks the staging data, and nobody can say which checks it makes or what happens when one fails.
  - The team wants the checks as dbt tests and source checks, so bad input stops the work that depends on it inside the build.
  - A procedure that only validates, writing no table, has to move into the dbt project before it can be retired.
description: Replace a legacy validation procedure with dbt tests and source checks, read from the legacy database over MCP without changing it unless approved, with every check mapped to a replacement, the approved failure policy kept, each check shown to pass on good data and fail on bad, and retirement only as approved.
pitch: Move a staging-data validation procedure into dbt so bad input fails the build and stops the work that reads it, or warns where you approve.
job_category: re-engineer
area: data-quality
readiness: supported
function:
  - cross-functional
domain_objects:
  - stored_procedure
  - check_map
  - source_check
  - dbt_test
  - failure_policy
  - check_report
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
  - Needs the checked tables landed in the target; landing them belongs to an ingestion Recipe.
  - Reads over a connected MCP server only, such as Toolbox for SQL Server and Oracle or postgres-mcp for PostgreSQL.
  - A login that can write or run routines is reported; whether the run proceeds on it is approved.
  - A procedure that also loads a table belongs to stored-procedure-to-dbt; freshness to source-freshness-sla.
  - Notices, logging and other side effects of the procedure are replaced as approved or reported as not reproduced.
related:
  - stored-procedure-to-dbt
  - source-freshness-sla
  - consolidate-legacy-table-writers-to-dbt
  - inventory-legacy-database-over-mcp
  - plan-legacy-procedure-package-intents
  - legacy-sql-to-dbt
evidence:
  features:
    - capturing-requirements
    - designing
    - planning
    - registering-dbt-sources
    - generating-dbt-model
    - running-dbt-in-sandbox
    - verifying
  evals: []
---

## Prompt

Replace the legacy validation procedure <legacy_procedure>, which checks <checked_tables> before a load, with dbt tests and source checks in the current Intent that fail the build, or warn, as the approved failure policy says. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Read the legacy database over its connected MCP server, and change nothing in it unless the owner approves. Deliver a check map that lists every check the procedure makes, its condition, how it reports and what it does to the run, with the test or source check that replaces it or the approved reason it has none, the approved failure policy kept with any parameter or flag that changed it, the checks placed so one failing at error severity stops the work that reads the checked data and nothing else, and evidence that each check passes on good data and fails on data that breaks only that check, naming the table and rows at fault. State what the replacement cannot prove, handle cutover and retirement as approved, and report each legacy defect as follow-up work.

## Verified by

- Every check the readable definition makes, including those behind a parameter, those that only report and those a called routine makes, is listed with its condition, how it reports and its replacement or approved reason for none; an unreadable, string-built or outside check is named unassessed.
- Each replacement check passes on data that meets its condition and fails on data that breaks only that condition, naming the table and the rows or count at fault and the legacy condition it stands for; the legacy outcome for the same data, derived independently of the dbt checks, agrees.
- The approved failure policy holds for each check: what the legacy fails, warns on or only reports becomes an error, a warning or a report as approved, and a parameter or flag that changed this stays one approved setting; under the warning setting the same findings appear and the build continues.
- A check that fails at error severity stops, in the same build, the work that reads the checked data and nothing else; one at warning severity reports and lets it build, as does a passing check, and work the approved scope leaves out stays buildable when a check fails.
- Each check runs in every build that selects the work it protects; a check that no selection reaches is reported as not gating and never counted as passing.
- Condition edges follow the approved reading of the legacy: a boundary value, empty against null, a single row and which rows are in scope each pass or fail as the legacy does, and no threshold or condition is added or dropped without approval.
- Legacy behaviour beyond pass or fail, such as notices, logging, notifications or writes, is replaced as approved or reported as not reproduced, and the build outcome never claims it.
- The legacy database changes only as approved, shown by a record of every statement sent: by default only reads and no routine run, and any approved run of the procedure is recorded with what it changed.
- Results computed from authored stand-in data are labelled as such, and checks not yet run on the real landed data are stated unproven against it.
- Parity is kept separate from cutover: the legacy procedure stops being called only after the checks are accepted, and it is kept, marked retired or removed as approved.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Read the procedure end to end over the MCP connection: its parameters and defaults, every condition it tests, what it does when one fails, the routines it calls and who calls it, and say plainly when the definition cannot be read and the behaviour comes from the owner's account. Compare each legacy condition with what a dbt test or source check can express, and report any it cannot. Place each check so the work that reads the checked data is stopped by it, then confirm with a build that a check failing at error severity skips that work and a passing one lets it build, and that the selection the approved scope names includes every check. Prove each check on good data and on data that breaks only its condition, include the edges the legacy conditions turn on, derive the legacy outcome independently of the dbt checks, report every legacy defect as follow-up work, and handle cutover and retirement as approved.

### Compose

- capturing-requirements
- designing
- planning
- registering-dbt-sources
- generating-dbt-model
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which checks count as the procedure's, such as conditions behind a parameter, called routines or checks made outside it, which tables and rows are checked, and whether any check the procedure does not make is added.
- If unresolved, which findings fail the build and which only warn, whether a parameter or flag of the procedure is kept and where it is set, and what its default is.
- If unresolved, where each check sits, such as on the landed source or on a model, which work a failure stops, and which builds must run the checks.
- If unresolved, whether a finding shows the rows or a count, and which procedure notices or logging are replaced, reported or not reproduced.
- If unresolved, how each condition reads at its edges, such as a threshold, empty against null, a single row or a comparison with another table, including any tolerance.
- If unresolved, where the legacy outcome for the same data comes from, such as the procedure's logic read over MCP, a run of the procedure or approved snapshots, what bad data stands for each check, and whether a login that can write may be used.
- If unresolved, once the checks are accepted, is the procedure kept, marked retired or removed, and do the jobs that call it move now or later.

### Guardrails

- Do not write to the legacy database or run its routines to obtain a baseline unless the owner approves it.
- Do not add a check, a threshold or a condition the procedure does not have, and do not drop one it has, without approval.
- Do not weaken a check, widen a threshold or edit the data to make a check pass.
- Do not lower a failing check to a warning unless the approved failure policy says so.
- Do not scope a check so widely that unrelated work fails, or so narrowly that an error-severity failure leaves the work reading the checked data building.
- Do not report a check as protecting work it does not reach, or count a check that no build runs as passing.
- Do not take a threshold or an expected count from today's data; take it from the legacy condition or an approved value.
- Do not remove or stop calling the legacy procedure before the checks are accepted and nothing depends on it.
