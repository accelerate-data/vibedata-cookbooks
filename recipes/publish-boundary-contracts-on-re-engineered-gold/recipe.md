---
id: publish-boundary-contracts-on-re-engineered-gold
title: Publish boundary data contracts on re-engineered gold tables and queue what the legacy output leaves open
trigger:
  - A legacy warehouse is re-engineered into dbt and consumers read its gold tables, but nothing states their grain, nulls or allowed values, or how they differ from the legacy reports.
  - The legacy report tables are the only evidence of what consumers used to get, and the new tables' promises must be written down and checked against them.
  - A re-engineered report table is about to replace a legacy one, and the owner wants its contract reviewed before consumers move.
description: Publish one boundary data contract on each re-engineered gold table in the approved scope, drafted from the built table and checked against the legacy output it replaced, read over MCP without changing the source, with every difference and doubt queued and, where the owner approves, the contracts enforced in the build.
pitch: Put a reviewed data contract on each re-engineered gold table in scope and check it against the legacy report.
job_category: re-engineer
area: re-engineering
readiness: supported
function:
  - cross-functional
domain_objects:
  - legacy_database
  - gold_table
  - data_contract
  - output_contract
  - review_queue
  - legacy_report
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
qualifiers:
  - Needs the gold tables already built and a legacy source readable over a connected MCP.
  - Key and uniqueness enforcement varies by target; where unenforced, tests carry them.
  - Moving consumers, retiring legacy reports and non-gold layers belong elsewhere.
related:
  - inventory-legacy-database-over-mcp
  - plan-legacy-warehouse-layers-to-dbt-intents
  - legacy-sql-to-dbt
  - versioned-data-contract-cutover
  - incremental-dbt-model-with-contract
evidence:
  features:
    - data-contract
    - validating-data-contract
    - running-dbt-in-sandbox
    - verifying
  evals: []
---

## Prompt

Publish an ODCS boundary contract on each re-engineered gold table in <gold_scope>, drafted from the built table and checked against what <legacy_source> returned for the report it replaced, read over its connected MCP without changing it. Each contract records what the built table does today: grain and key, nullability, and each closed value set and relationship the data proves, as a rule or a written no rule as approved, with any approved known-failing rule described as failing. Queue every doubt and every difference from the legacy output with its evidence, and turn each answer into a description, a rule, a relationship, a written no rule because, an accepted difference or a finding for a separate change. Where the owner approves writing the model properties, have the build enforce each contract's column types and constraints, and run the gates, reporting any gate that did not run as unrun. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Change no model logic.

## Verified by

- Every gold table in the approved scope has exactly one contract or is reported without one with its reason, and gold tables left out of the scope are listed with the reason.
- Each contract states the table's grain, key and nullability, and each closed value set and reference as a rule or a written no rule as approved; every stated rule is true of the built table or described as failing, shown by a query that derives it independently from the table's rows.
- A claim the data contradicts is corrected with a recorded finding that shows the data, or kept as a described known-failing rule as approved, and is never weakened silently or stated as true.
- Where a comparison can be made, each table's legacy columns, grain and key are compared with the built table's, and each match and difference is listed with the legacy and built query and result; no contract says the built table equals the legacy report.
- Where the legacy output cannot be compared, such as an empty table, a different population or a loader that fails, the comparison is reported unproven with the reason and the exact error, never as matching.
- Every doubt and every difference ends, as approved, as a description, a rule, a relationship, a written no rule because, an accepted difference, a finding for a separate change, or an open question, each with its evidence.
- Where the owner approves writing the model properties, the build enforces each contract's types and constraints where the platform enforces them, and the rest is carried by tests or stated as not enforced; otherwise generation is reported not done.
- Existing tests stay enforced or their absence is stated, and a rebuild leaves each table's rows and values unchanged.
- A gate that could not run is reported unrun with its reason, and no unrun gate counts as passing.
- The legacy source is unchanged by the run, shown by a record of the statements sent.
- What the comparison cannot show is stated, including value equivalence and any branch the legacy rows do not exercise.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Read the legacy source over its connected MCP only, confirm what the login can do, and keep a record of every statement sent. Declare which gold tables owe a contract, draft each contract from the built table with the contract tool, and profile each claim against the table before stating it. Compare the legacy output with the built table on structure and behaviour, and label every value claim unproven where the populations differ. Where a legacy report is empty or its loader fails, say so with the exact error and use what is available as labelled evidence. Contracts state the built behaviour, with any approved known-failing rule described as failing; fixes to data or models belong to a separate change. Where model properties may be written, carry each existing test the contract can express into it, keep or state the rest as approved, and rebuild to show the output and the tests are unchanged. Run the review and the gates, and report each doubt in the queue, never in contract prose. Where enforcement is approved, build the tables with the contracts enforced before declaring completion; parse success is not build success.

### Compose

- data-contract
- validating-data-contract
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which gold tables owe a contract: every re-engineered one, a named subset, or those with named consumers?
- If unresolved, how is each difference between the built table and the legacy output recorded: an accepted difference, a finding to fix outside this run, or left open?
- If unresolved, what counts as a difference: type mapping, rounding and precision, case and whitespace, null versus empty, row order, and which legacy filters define the compared population?
- If unresolved, what evidence stands in for a legacy report that is empty, loads a different population or fails: a replay over the same rows, another population, or none?
- If unresolved, when the data contradicts a drafted rule, is the claim corrected with a finding or kept as a described known-failing rule? Data and model fixes belong to a separate change.
- If unresolved, is a closed value set or a reference declared as a rule or recorded as no rule, is a failing rule an error or a warning, and who owns the business questions the data cannot answer?
- If unresolved, may the model properties files be rewritten to enforce the contracts, and what happens to an existing test a contract cannot express?
- If unresolved, what version do the first contracts carry, and what change needs a version bump?

### Guardrails

- Do not change model logic, and do not state legacy behaviour as the built table's behaviour or the reverse.
- Do not report a gate that did not run as passing, or a comparison that could not be made as matching.
- Do not read the legacy source with local client tools, and do not run a statement that changes it.
- Do not weaken a contract claim to clear a gate without a finding that says why.
- Do not drop an existing test silently when generating enforcement, and do not hand-write what generation owns.
- Do not invent a semantic document or a business answer to clear a warning; queue it.
