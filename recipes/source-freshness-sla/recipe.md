---
id: source-freshness-sla
title: Declare source freshness SLAs and make stale data fail before downstream work
trigger:
  - A load stopped and nothing failed; downstream models rebuilt on old data and the reports still looked current.
  - Only some sources have a freshness check, often one blanket threshold, and nobody can say which tables are checked or against what.
  - A stale source must stop the work that depends on it before it rebuilds, and say which source is late, by how much and against what limit.
description: Give every source table a dbt project declares a freshness limit, or a recorded exemption, and gate the builds that run the check so a source past its fail limit holds back the work that depends on it before it rebuilds, with a report of each table's age, its limit and the work held back.
pitch: Give every source a freshness limit and stop stale data before downstream models rebuild on it.
job_category: build
area: data-quality
readiness: supported
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
  - Protects only work whose source is judged in the same build; the run report names a build that judged none.
  - Each checked table needs a load time, from a landing column, the loader's load log or an approved proxy.
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

Give every source table that the Intent's dbt project declares a freshness expectation, its approved limits, such as warn and fail, with the measure its age is taken from, or a recorded exemption with its reason, and make a source past its fail limit hold back the work the approved failure policy names before that work rebuilds on stale data. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Choose each table's measure from the load-time evidence the source actually carries, and state what each measure relies on and what it would miss. Deliver the per-table declarations, the gate, where the approved policy allows overrides a recorded way to apply one, a coverage report that names every declared source table with its limit or exemption, and a run report that names each late table, its age, its limit and the work it held back.

## Verified by

- Every source table the project declares is either checked, with its approved limits and the measure its age is taken from, or exempt with a stated reason; the coverage report lists every one of them, and a declared table with neither is caught as uncovered rather than passing unnoticed.
- The limits and measure the coverage report shows for a table are the ones the gate judges it by; relations in a declared source's schema that no source declares, other than the project's own outputs and the loader's bookkeeping, are listed apart from checked and exempt tables.
- In a build that judges a table, its age is judged at the approved point in the run, before the work that depends on it builds; a timestamp without a zone is read in the approved time zone, and an age exactly on a limit is treated as the approved rule says.
- In a build that judges the late source, a source past its fail limit with no override in force holds back the work the approved failure policy names before it rebuilds, and nothing else; the run report names the late table, its age, its limit and each model held back with its cause.
- Work that cannot keep its previous contents while a source is late, such as a view that reads the source live, is handled as the approved policy says and is reported as unprotected, never as protected.
- A table past its warn limit, an empty table and a declared table missing from the warehouse are each handled as the approved rules say and reported with their own message.
- A business-day limit counts only the approved calendar's business days, and a date the calendar does not cover is handled as the approved rule says and named in the result, never silently counted or skipped.
- Where the approved policy allows overrides, an override applies only within its approved terms, such as approver and expiry, an override recorded before a run applies in that run, and every override used is named in the run report; an expired or missing override never lets a late source pass.
- A table measured by an event-time proxy is labelled as a proxy wherever its age appears, a table with no measurable load time is never shown as checked or fresh, and a build that judged no table is recorded as having judged none.
- The result states what a normal build on the current data will do under the new limits: which sources are already past their limits and that the work depending on them would be held back.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Inventory every declared source table and the load-time evidence it carries: a landing column, the loader's own load log, only business timestamps, or nothing. Propose a measure per table from that evidence and, where the approved requirements leave them open, agree the arrival cadence, limits, calendars and exemptions with the user. Declare each table's limits and measure once, where the gate and the coverage report both read them. Judge each table at the approved point in the run, before the work that depends on it builds; a check that fails without holding anything back does not count. Report each run's verdicts, the work held back and its cause, and any build that ran no gate. Run the gate against the current data and report what it would hold back before release.

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
- If unresolved, what counts as loaded for each table: a landing column, the loader's own load log, or the newest business timestamp as a labelled proxy, and which time zone do timestamps without one hold?
- If unresolved, does any feed arrive only on business days, which calendar defines them, and what happens when the calendar does not cover a date in the period being counted?
- If unresolved, when a source fails, is only its dependents' work held back, keeping their previous contents, or is the whole run stopped, and how is a view that reads the source live treated?
- If unresolved, does a warning only report or also stop work, and is an empty table or a declared table missing from the warehouse a failure?
- If unresolved, may an operator run past a failed source, who approves it, how long it lasts, and where is it recorded?
- If unresolved, is freshness judged once at the start of a run or again before each dependent step?

### Guardrails

- Do not choose or apply a limit, exemption, measure, calendar or failure policy without approval; explain the alternatives if asked.
- Do not leave a declared source table unchecked without a recorded exemption, and do not treat a table with no measurable load time as fresh.
- Do not present an event-time proxy as load recency, or a quiet feed as a stopped one, without saying so.
- Do not call a source protected until a deliberately late source has been shown to hold back the work the approved policy names.
- Do not add a way past a late source other than the approved override, if any, such as a flag or a setting that moves the instant ages are judged against.
- Do not extend into scheduling consumer pipelines, alert delivery, volume or distribution checks, or fixing the loaders that run late.
