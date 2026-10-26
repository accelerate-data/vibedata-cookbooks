---
id: source-freshness-sla
title: Declare source freshness SLAs and make stale data fail before downstream work
trigger:
  - A load stopped and nothing failed; downstream models rebuilt on old data and the reports still looked current.
  - Only some sources have a freshness check, often one blanket threshold, and nobody can say which tables are checked or against what.
  - A stale source must stop the work that depends on it before it rebuilds, and say which source is late, by how much and against what limit.
description: Give every source table a dbt project declares a freshness limit, or a recorded exemption, and gate the builds that run the check so a source past its fail limit holds back the work the approved failure policy names before it rebuilds, with a report of each table's age, its limit and the work held back.
pitch: Give every source a freshness limit and stop stale data before downstream models rebuild on it.
job_category: build
area: data-quality
readiness: supported
function:
  - cross-functional
domain_objects:
  - source_freshness_sla
  - freshness_exemption
  - freshness_gate
  - freshness_override
  - freshness_coverage_report
  - freshness_run_report
works_with:
  platforms:
    - duckdb_local
    - motherduck
    - fabric_lakehouse
    - fabric_warehouse
    - redshift
  tools:
    - dbt
qualifiers:
  - Assessed end to end on duckdb_local only; the other listed targets rely on dbt support and are unassessed.
  - Protects only work whose source is judged in the same build; how often builds run is outside this Recipe.
  - Each checked table needs a measurable load time, such as a landing column, a load log, table metadata or a proxy.
  - Gating consumer pipelines on upstream readiness belongs to the readiness-gated-orchestration Recipe.
evidence:
  features:
    - registering-dbt-sources
    - authoring-dbt-project-artifact
    - generating-dbt-model
    - dbt-unit-testing
    - running-dbt-in-sandbox
    - verifying
  evals: []
---

## Prompt

Give every source table that the Intent's dbt project declares a freshness expectation, its approved limits, such as warn and fail, with the measure its age is taken from, or a recorded exemption with its reason, and make a source past its fail limit hold back, in every build that judges it, the work the approved failure policy names before that work rebuilds on stale data. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Choose each table's measure from the load-time evidence the source actually carries, and state what each measure relies on and what it would miss. Deliver the per-table declarations, the gate, where the approved policy allows overrides a recorded way to apply one, a coverage report that names every declared source table with its limit or exemption and lists apart the relations in the sources' schemas that no source declares, and a run report that names each late table, its age, its limit and the work it held back.

## Verified by

- Every source table the project declares is either checked, with its approved limits and the measure its age is taken from, or exempt with a stated reason; the coverage report lists every one of them, and a declared table with neither is caught as uncovered rather than passing unnoticed.
- The limits and measure the coverage report shows for a table are the ones the gate judges it by; relations in a declared source's schema that no source declares, other than the project's own outputs and the loader's bookkeeping, are listed apart from checked and exempt tables.
- In a build that judges a table, its age is judged at the approved point in the build, before the work that depends on it builds; a timestamp without a zone is read in the approved time zone, and an age exactly on a limit is treated as the approved rule says.
- A source past its fail limit with no override in force, in a build that judges it, holds back the work the approved failure policy names before it rebuilds, and nothing else; the run report names the late table, its age and limit, and each model held back with every late source that caused it.
- Work that cannot keep its previous contents while a source is late, such as a view that reads the source live, is handled as the approved policy says and is never reported as protected unless that handling protects it.
- A table past its warn limit, an empty table and a declared table missing from the warehouse are each handled as the approved rules say and reported with their own message.
- A business-day limit counts only the approved calendar's business days, and a date the calendar does not cover is handled as the approved rule says and named in the check's result, never silently counted or skipped.
- Where the approved policy allows overrides, an override applies only within its approved terms, such as approver and expiry, an override recorded before a run applies in that run, and every override used is named in the run report; an expired or missing override never lets a late source pass.
- A table measured by an event-time proxy is labelled as a proxy wherever its age appears, a table with no load-time measure is never shown as checked, one whose age cannot be measured is never shown as fresh, and a build that judged no table is recorded as having judged none.
- The result states what a normal build on the current data will do under the new limits: which sources are already past their limits and which work the approved failure policy would hold back.
- Which builds must judge the sources, and how often they run, are stated; where the run definition is in scope its builds judge the sources, otherwise this is recorded as a cutover or unverified requirement, and a late source is caught when such a build runs, not when its limit passes.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Inventory every declared source table and the load-time evidence it carries: a landing column, the loader's own load log, warehouse load metadata, only business timestamps, or nothing. Propose a measure per table from that evidence and, where the approved requirements leave them open, agree the arrival cadence, limits, calendars and exemptions with the user. Keep the limits and measure the coverage report shows identical to those the gate judges. Judge each table at the approved point in the build, before the work that depends on it builds; a check that fails without holding anything back does not count. Report each run's verdicts, the work held back and its cause, and any build that ran no gate. State which builds must judge the sources and how often they run, and run the gate against the current data to report what it would hold back before release.

### Compose

- registering-dbt-sources
- authoring-dbt-project-artifact
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which source tables get a limit and which are exempt, and why: static code lists, reject or ledger tables, tables the project itself builds, tables with no load-time evidence?
- If unresolved, what is each feed's expected arrival cadence, what limits apply, such as a warn and a fail limit, and is an age exactly on a limit still inside it or already a breach?
- If unresolved, what counts as loaded for each table, such as a landing column, the loader's own load log, warehouse load metadata or the newest business timestamp as a labelled proxy, and which time zone do timestamps without one hold?
- If unresolved, does any feed arrive only on business days, which calendar and time zone define them, and what happens when the calendar does not cover a date in the period being counted?
- If unresolved, when a source fails, is only its dependents' work held back, keeping their previous contents, or is the whole run stopped, and how is a view that reads the source live treated?
- If unresolved, does a warning only report or also stop work, and is an empty table or a declared table missing from the warehouse a failure?
- If unresolved, may an operator run past a failed source, who approves it, how long it lasts, and where is it recorded?
- If unresolved, which builds must judge the sources and how often, is that run definition part of this work or a cutover requirement, and is freshness judged once at the start of a build or before each dependent step?

### Guardrails

- Do not choose or apply a limit, exemption, measure, calendar or failure policy without approval; explain the alternatives if asked.
- Do not leave a declared source table unchecked without a recorded exemption, and do not treat a table with no measurable load time as fresh.
- Do not present an event-time proxy as load recency, or a quiet feed as a stopped one, without saying so.
- Do not report a source as protected when its lateness would not hold back the work the approved policy names, such as a check that only warns or a build that skips it.
- Do not add a way past a late source other than the approved override, if any, such as a flag or a setting that moves the instant ages are judged against.
- Do not extend into scheduling consumer pipelines, alert delivery, volume or distribution checks, or fixing the loaders that run late.
