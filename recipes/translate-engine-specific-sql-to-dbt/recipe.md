---
id: translate-engine-specific-sql-to-dbt
title: Translate a legacy query's engine-specific constructs into dbt and prove each matches or differs only as approved
trigger:
  - A legacy SQL Server, Oracle or PostgreSQL report relies on PIVOT, UNPIVOT, CUBE, ROLLUP, grouping sets, a recursive hierarchy or generated keys that the target platform handles differently.
  - The team wants a reporting routine's pivots, subtotals and hierarchies in dbt, but consumers need proof that every result is the same or differs only as agreed.
  - A migration plan lists routines with engine-specific constructs, and nobody knows which of them translate exactly.
description: Rebuild the pivots, subtotals, recursive hierarchies and generated keys of a legacy reporting query in dbt, reading the source over MCP without changing it, with each construct mapped to a target form, shown equal to the legacy result or different only as approved, and legacy defects reported, not fixed.
pitch: Rebuild a legacy report's pivots, subtotals, hierarchies and keys in dbt and prove each matches the legacy query or differs only as approved.
job_category: re-engineer
area: transformation
readiness: supported
function:
  - cross-functional
domain_objects:
  - legacy_sql
  - construct_map
  - dbt_model
  - approved_baseline
  - parity_report
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
  - Needs the tables the construct reads landed in the target; landing them belongs to an ingestion Recipe.
  - Reads the legacy source over a connected MCP server only, such as Toolbox or postgres-mcp.
  - A login that can write or run routines is reported; whether the run proceeds on it is approved.
  - Compares each construct's own statement; the routine, the table it writes and cutover stay with related Recipes.
  - Constructs in statements the source will not show, such as unreadable dynamic SQL, are named unassessed.
  - Behaviour outside the output rows, such as other writes or logging, is reported, not reproduced.
related:
  - stored-procedure-to-dbt
  - legacy-sql-to-dbt
  - consolidate-legacy-table-writers-to-dbt
  - inventory-legacy-database-over-mcp
  - plan-legacy-procedure-package-intents
  - scd-procedure-to-dbt-snapshot
  - scalar-sql-function-to-dbt-macro
  - cross-platform-dbt-macro
evidence:
  features:
    - capturing-requirements
    - designing
    - planning
    - generating-dbt-model
    - dbt-unit-testing
    - running-dbt-in-sandbox
    - verifying
  evals: []
---

## Prompt

Translate the engine-specific constructs in <legacy_routine_or_query> into dbt in the current Intent: each pivot, unpivot, subtotal (grouping sets, CUBE or ROLLUP), recursive hierarchy and generated key in the approved scope. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Read the legacy source over MCP only and change nothing in it. Deliver a map from each construct occurrence to its target form, the dbt models, built from the inputs as landed in the target, and evidence that each model returns the same rows as the legacy statement holding those occurrences, run on the same inputs, or differs only as approved, including inputs that reach every branch and the exceptional ones the legacy query tolerates or fails on. Reproduce legacy behaviour that looks like a mistake and report each defect as follow-up work; a wanted output change belongs in a separate change. State what the comparison cannot prove.

## Verified by

- Every occurrence of an engine-specific construct in the approved scope maps to a target form or a stated reason none is needed; one the source does not show is named unassessed, and one with no equivalent is reported as a gap with the target limit that rules it out, never approximated.
- Each model reads its inputs as landed in the target and returns the rows the legacy statement holding its occurrences returns on the same inputs, compared both ways as multisets at the approved precision; each difference an approved choice makes is listed with its rows, and nothing else differs.
- The compared inputs reach every branch of each mapped construct that the legacy logic can be run on, including the exceptional states it tolerates or fails on; expected rows come from the legacy engine, and any other branch is proven by an approved oracle or stated unproven.
- Subtotal and rollup rows carry the approved level encoding; where the legacy labels cannot tell two grouping levels, or a real null, from a rolled-up value, the affected rows are reported; input with no rows gives the approved result.
- Pivoted and unpivoted output has the approved column set and null-row handling; values outside it and spelling variants follow the approved rule, and none creates a column or drops a row silently.
- Orphaned, looping, over-deep and duplicated hierarchy input follow the approved treatment, and rows it leaves out are counted with their reason; a build that would not end or would exhaust resources fails with a message naming the offending rows.
- Where the legacy logic raises an error on an input, the model fails the same way or follows the approved treatment, which is reported; a bound the translation adds raises an error, or truncates only as approved with the cut rows flagged and counted.
- A generated key follows the approved stability rule, is distinct per output row at the approved grain, and is never claimed to equal a legacy identity value; tables or consumers holding legacy key values are mapped or reported.
- Text, number, ordering and rounding behaviour, such as null handling, declared widths, case and space matching, null order, ties and exact decimals, matches at the approved precision, and each difference is reported.
- Each legacy defect is listed with its evidence, affected rows and what fixing it would change; one shaping the statement's rows is reproduced, not fixed, one only the routine's write shows is reported; where the logic cannot run as written, parity is only against approved adjusted logic beside it.
- Every statement sent to the legacy source is recorded in order with its outcome, and none changes it.
- Anything the comparison cannot prove is stated, including constructs the inputs never exercise, results the legacy logic does not determine, and inputs not shown identical on both sides.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Read the legacy routine end to end over MCP, with its catalogue, grants and consumers, profile the tables it reads, and find every engine-specific construct, including those inside dynamic or nested statements. Map each occurrence to a target form under the Intent's project structure and state what each form relies on and what it would miss. Build comparison inputs that reach every branch of each construct and the exceptional states, such as missing values, unmatched keys, repeated identifiers, empty input, exact ties and very deep or looping chains, show them identical on both sides, and obtain the legacy result by running the routine's own query logic over the same inputs, without running the routine or writing to the source. Record every statement sent to the source. Compare in both directions after each model, and prove behaviour the inputs cannot reach by another approved oracle or state the gap. Reproduce each defect, list it with its evidence and report it as follow-up work, and state what cannot be proven.

### Compose

- capturing-requirements
- profiling-source-data
- designing
- planning
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which occurrences of the pivot, unpivot, subtotal, recursion and generated-key families are in scope, and which statement holding each is compared; other constructs go to the routine's conversion Recipe, and each one left out is listed with its reason.
- If unresolved, what replaces a legacy identity, sequence or rowversion key: carried, replaced or dropped, at what grain, what happens when rows at that grain are not unique, must it stay stable across rebuilds and as other rows change, and how do tables holding legacy key values map to it?
- If unresolved, how are subtotal levels published, as the legacy labels or explicit per-column flags, how are label collisions handled, and what does the output show when there are no input rows?
- If unresolved, what does a pivot or unpivot publish: which columns, what happens to values outside them, spelling variants, null rows and missing cells?
- If unresolved, how are orphaned, looping, over-deep and duplicated hierarchy rows treated, must the model fail where the legacy logic errors on an input, such as a recursion limit, or follow another approved treatment, and what must a failing build report?
- If unresolved, which text and number semantics must match exactly: null handling, declared widths, case and space matching, null order, rounding at ties and precision?
- If unresolved, which parameters, environments and session settings form the comparison, and do row order, column names and types count as unchanged output?
- If unresolved, may a login that can write be used, where does the legacy answer come from when the source tables are empty or the routine cannot run, and who approves an adjusted read or another oracle?

### Guardrails

- Do not run, edit or recompile the legacy routine, and do not write to the legacy source; every statement sent to it only reads.
- Do not correct a legacy defect that shapes the statement's rows; reproduce it and report it as follow-up work, and report any output change an approved choice makes as a deliberate difference.
- Do not trim, case-fold, truncate, round or cast values to hide a difference from the legacy result beyond what the approved comparison rule allows; reproduce it or report it.
- A depth limit, cycle stop or recursion error the legacy logic applies is reproduced unless an approved treatment replaces it, which is reported as a difference; a bound the translation adds never truncates rows silently.
- Do not build the expected rows from the model's own logic, copy result rows by hand into the evidence, or claim a comparison the legacy query's logic did not produce.
- Do not claim exact parity for a result the legacy logic does not determine, such as ties under a row limit or unordered string aggregation.
- Do not treat a generated key as matching a legacy identity value.
- Do not widen a tolerance or leave out rows or columns to make the comparison pass.
- Do not extend the work into scheduling, performance tuning, moving other objects or retiring the legacy routine.
