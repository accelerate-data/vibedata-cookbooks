---
id: late-arriving-fact-keys-to-dbt
title: Resolve late-arriving facts and unseen dimension members in a dbt fact and list every line it cannot place
trigger:
  - A legacy fact load looks up dimension keys, and a line that arrives late or names a member never seen lands on a key nobody can explain, or vanishes.
  - The load is moving to dbt, and consumers need proof that late lines and unseen-member lines land where the legacy load put them, or are shown with a reason.
  - A SQL Server, Oracle or PostgreSQL fact load moves to dbt, and a line set aside for a missing member must be placed once it arrives, with loaded rows undisturbed.
description: Move one legacy fact load's dimension-key resolution into dbt, read over MCP without changing the legacy unless approved, with late and unseen-member lines landing as the approved rule gives, every staged line published or listed once with its approved reason, and a set-aside line placed once its member arrives.
pitch: Prove a dbt fact puts late and unseen-member lines where the legacy load did, with each line it cannot place listed with its reason.
job_category: re-engineer
area: transformation
readiness: supported
function:
  - cross-functional
domain_objects:
  - stored_procedure
  - fact_table
  - dimension_member
  - late_arriving_line
  - unplaced_line
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
  - Reads over a connected MCP server, such as Toolbox for SQL Server and Oracle or postgres-mcp for PostgreSQL.
  - Any run of a legacy routine is approved and recorded; a login that can write or run routines is reported.
  - Needs the fact's inputs and dimensions landed in the target; an ingestion Recipe lands them.
  - Several writers of one table is consolidate-legacy-table-writers-to-dbt.
  - A paging loop is batched-loop-procedure-to-set-based-dbt; a load with no dimension lookup is stored-procedure-to-dbt.
  - Keeping dimension history is scd-procedure-to-dbt-snapshot; replayed deliveries belong to business-event-fact.
  - A lookup the MCP cannot read is reported unassessed, not converted.
  - Behaviour outside the fact's rows, such as logging, is reported, not reproduced.
related:
  - consolidate-legacy-table-writers-to-dbt
  - batched-loop-procedure-to-set-based-dbt
  - stored-procedure-to-dbt
  - scd-procedure-to-dbt-snapshot
  - business-event-fact
  - legacy-sql-to-dbt
  - inventory-legacy-database-over-mcp
  - plan-legacy-procedure-package-intents
evidence:
  features:
    - capturing-requirements
    - designing
    - planning
    - generating-dbt-model
    - running-dbt-in-sandbox
    - verifying
  evals: []
---

## Prompt

Move the dimension-key resolution of <legacy_fact_load>, which fills <fact_table> from <staging_inputs> and <dimension_tables>, into one dbt model in the current Intent. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Read the legacy load and its data over the MCP and change nothing in the legacy database unless approved. Deliver a lookup map that shows each dimension lookup with its version rule, what a miss does, and each filter or window deciding which lines a run reaches, the one model, built from its inputs as landed, with each approved load mode mapped to one way of running it, and evidence that a line arriving after its period and a line naming a member the dimension has not seen both land exactly as the approved legacy rule puts them, at the approved precision. Publish or list every staged line once with its approved reason, place a listed line as approved once its member arrives without disturbing rows already loaded, report each legacy defect as follow-up work instead of repairing it, handle cutover as approved, and state what the comparison cannot prove.

## Verified by

- Every dimension lookup, version rule, join kind, filter and run window of the legacy load is listed with what it does to a line whose member or date does not fit, and each is reproduced or an approved difference; one the MCP cannot read is named unassessed with no parity claimed.
- A line that arrives after its period lands on the key and date the approved legacy rule gives it, in each approved way of running the model; the dimension version follows the approved version rule and never an assumed record timestamp.
- A line naming a member the dimension has not seen follows the approved disposition for that dimension, and no unknown member, sentinel key or default row is created unless approved; the line is never silently lost.
- A key the legacy leaves null where an optional lookup misses stays null unless the approved disposition places it elsewhere; a null key is not counted as a drop and carries no not-null promise.
- In each completed run every staged line is published or listed once with its reason from the approved set, the first in the approved order or every one as approved; distinct published plus listed lines equal staged lines with zero residue.
- A line a normal run's own window or filter skips is listed in that run with that reason, and it lands only where the approved rule lets it, such as a full rebuild.
- A listed line whose member later arrives follows the approved placement, such as the next normal run with its real keys, and then leaves the list; every published row keeps its values and key, and a repeat on unchanged inputs changes neither the fact nor the list.
- Published rows, built from the inputs as landed, equal the rows the legacy load leaves in the fact for the same inputs and prior table, derived independently of the model, at the approved precision, after a rebuild and a normal run; columns outside parity and approved differences are named.
- Legacy behaviours that change rows, such as join multiplication, filters that depend on other rows or ties with no defined order, are reproduced or approved as differences and listed with their rows as follow-up work; the published grain is stated and holds.
- A generated key is unique, never null and stable across rebuilds and reruns, so a late line never renumbers an existing key; it is left out of parity unless the legacy value is reproducible.
- The legacy database changes only as approved, shown by a record of every statement sent, by default only reads; parity is kept separate from cutover, which keeps, retires or removes the legacy load as approved.
- A branch the inputs cannot reach, such as a miss that the data never contains, is shown equivalent by an approved check or stated unproven.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Read the legacy load end to end over the MCP connection with reads only: its modes and parameters, every dimension join with its version predicate and join kind, the filters and windows that decide which lines a run reaches, any row multiplication, how its keys are generated, and who calls it. Use inputs that would separate the branches, such as a line dated before everything loaded, a member that exists in two versions, a member the dimension has never held, a line failing two checks at once, a line a normal run skips but a rebuild loads, and a member that arrives after its line was set aside. Settle how the legacy answer is obtained without changing the legacy database unless approved, and how a prior table is set up so a normal run is really exercised. Build one model under the approved project structure with a published list of unplaced lines that reflects the current inputs on every run, compare the rows with the legacy answer, show branches the inputs cannot reach equivalent by another check or state the gap, report every difference and defect as follow-up work, and handle cutover as approved.

### Compose

- capturing-requirements
- profiling-source-data
- designing
- planning
- generating-dbt-model
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which fact load, load modes and dimension lookups are in scope, which way of running the model stands for each mode, and does the run stop or proceed, named unassessed, on a lookup the MCP cannot read?
- If unresolved, which version of a member does a line take, such as the current one or the one valid at its date, and how is a late line's date key obtained?
- If unresolved, what happens to a line whose member is missing or not current, such as drop it, keep it with a null key, place it on a stated unknown member or fail the run, and does the answer differ by dimension?
- If unresolved, which reasons exist, does a line failing several checks show the first in an approved order or every one, and which lines does a normal run skip before any lookup, such as those outside a date window?
- If unresolved, when a member arrives after its line was set aside, is the line placed on the next normal run, only on a rebuild or left listed?
- If unresolved, which behaviours that change rows are reproduced, corrected separately or accepted as differences, which columns count as unchanged output, how is a generated key assigned and at what precision are rows compared?
- If unresolved, where do the rows the legacy load leaves come from, such as its select logic run read-only on the same inputs with the write applied, an approved copy or approved snapshots, how are unreachable branches checked, and may a login that can write be used?
- If unresolved, once parity is accepted, do consumers move now or later, is the legacy load kept, marked retired or removed, and who reads the list of unplaced lines?

### Guardrails

- Do not write to the legacy database or run its routines to obtain a baseline unless the owner approves it.
- Do not invent an unknown member, sentinel key or default dimension row unless approved, and do not repair a drop the approved rule reproduces.
- Do not let a staged line vanish: every line is published or listed once with its approved reason, and a null key the legacy allows is not a drop.
- Do not choose the dimension version by assuming a record timestamp; the approved version rule decides, and a late line is not moved or re-dated to fit.
- Do not let a placed line stay in the list or appear twice, and do not change or re-key a row already published when a late line or member arrives.
- Do not claim parity from inputs on which a late line, an unseen member or a line failing two checks cannot occur.
- Do not take the legacy's rows from the model, and do not describe a reconstruction of them as an observed run.
- Do not edit a legacy answer or expected output, or widen the approved precision, to make a comparison pass.
- Do not remove or disable the legacy load before parity is accepted, or let it and the model maintain the consumer-facing table at the same time.
