---
id: motherduck-flight-scheduling
title: Schedule a dlt load and a dbt build on MotherDuck as a committed MotherDuck Flight
trigger:
  - The MotherDuck load and the dbt build that follows it run from a cron job on someone's laptop.
  - A dlt load and a dbt build on MotherDuck have to run in order on a schedule without standing up an orchestrator.
  - A scheduled run reports success while the load or the build behind it actually failed.
description: Author a MotherDuck Flight as committed code that runs the approved load and then the dbt build of an approved selection on a schedule, under approved failure, recovery and overlap rules, prove its order, failure paths and carried project against the committed program, and run it in a MotherDuck sandbox where approved.
pitch: Replace the laptop cron with a committed MotherDuck Flight that loads, builds and fails loudly on a schedule.
job_category: build
area: orchestration
readiness: supported
domain_objects:
  - motherduck_flight
  - schedule
  - flight_secret
works_with:
  platforms:
    - motherduck
  tools:
    - dlt
    - dbt
qualifiers:
  - Not yet assessed end to end on motherduck.
  - Schedules the load and build on MotherDuck only; local DuckDB has no scheduler.
  - The dbt project the Flight carries must fit MotherDuck's Flight source-code size limit.
  - A schedule only runs on a MotherDuck plan that offers scheduled Flight runs.
  - The load must reach its source from the Flight runtime, with credentials held as Flight secrets.
  - Scheduling on Fabric belongs to fabric-data-pipeline-as-code.
related:
  - fabric-data-pipeline-as-code
  - readiness-gated-orchestration
  - source-freshness-sla
evidence:
  features:
    - generating-orchestration
    - evaluating-orchestration
    - running-orchestration-in-sandbox
    - documenting-orchestration
  evals: []
---

## Prompt

Author a MotherDuck Flight named <flight_name> that runs <load> and then the dbt build of <dbt_selection> on <schedule>, as committed code with its pinned dependencies, its declared configuration and its secret names. Inherit the Intent's repository, platform, Domain, load, dbt project and approved requirements, and resolve only the semantics they leave open: which models the Flight owns, what runs after each kind of failure, retries, recovery and reruns, the schedule and overlapping runs, run-scoped values, credentials and the source location, and failure notification. Validate the Flight statically, prove its order, its failure paths and the project it carries against the committed program, run it on demand in a MotherDuck sandbox where that is approved, document its steps, failure rules, schedule and deployment prerequisites, and state what the evidence cannot prove.

## Verified by

- The Flight's program, pinned dependencies, declared configuration and schedule are committed, and no Flight id, credential or deployment-specific source location value is committed.
- The Flight passes static Flight validation with no findings, every configuration key it reads is declared, and every workload credential is read from a declared Flight secret under its namespaced name and fails the run when absent.
- One run lands the approved load and then builds the approved selection; a load that still fails after any approved retries, or lands an unfinished package, ends the run failed naming the load, and the build runs or is skipped exactly as approved.
- A build the approved rule treats as failed ends the run failed, naming every node that did not pass and each node skipped because of it; a status the rule treats as not failing, such as a no-op node or an approved warning, is named and does not fail it.
- An empty load is routed as approved, and the run reports the rows that run itself landed, not the totals already held.
- The run builds exactly the approved selection and no excluded node, and the resolved node set changes only as the approved boundary allows; any other change fails packaging, naming the nodes.
- The Flight carries a complete dbt project within the source-code size limit; packaging fails loudly when the carried project is incomplete or over the limit, and the size and its share of the limit are reported.
- A first run into a new destination creates what it writes; a relation the selection reads but does not build or load is a reported prerequisite that fails the run when absent; a model needing a run-scoped value gets it as approved or is left out and reported.
- Retries, reruns and recovery after a failed run follow the approved rule, and overlapping runs follow the approved overlap behaviour; any difference a rerun shows is named with its cause.
- The committed schedule carries the approved cadence as UTC with the local-time conversion and any seasonal drift shown, and it is never activated by this Recipe.
- Where an on-demand MotherDuck sandbox run is approved, its status, exit code and the workload's own result agree with the approved rules; otherwise the behaviour above is shown offline against the committed program, labelled offline, and platform behaviour is reported unproven.
- Every failure path leaves the run failed with a message naming its cause for the approved notification route, whose route, any secret and recipient are reported as deployment prerequisites; delivery stays unproven, and platform behaviour shown only from documentation is reported as such.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, load, dbt project and approved requirements, and resolve only the semantics they leave open. Confirm that the load and every relation the selection reads either exist in the repository or are approved prerequisites, report any missing one as a blocker, and find which selected models need a run-scoped value and how each behaves without one. Author one Flight program from the platform's templates that lands the load, then builds the approved selection, and judges each half by its own result with every status classified explicitly, so that an unknown status fails the run. Carry the dbt project the platform requires, derived at packaging time and never committed; when the whole project exceeds the size limit, carry only what the selection and its macros need. Guard the resolved node set against the approved boundary. If an approved rule, such as a rerun that changes nothing, cannot be met by the inherited load or models, report it as a blocker rather than changing them. Validate the Flight statically, prove its order, failure paths, first run, rerun and carried project against the committed program, run it on demand in a MotherDuck sandbox where approved, document the steps, failure rules, schedule and deployment prerequisites, and report what was not proven.

### Compose

- generating-orchestration
- evaluating-orchestration
- running-orchestration-in-sandbox
- documenting-orchestration

### Ask first

- If unresolved, which load and which dbt models does the Flight own, may models added later downstream of the same source join it, and which belong to other teams?
- If unresolved, what runs after the load or the build fails, does a dbt test that only warns but finds rows fail the run, and does the build run when the load lands nothing?
- If unresolved, does the Flight retry inside a run, how is a failed night recovered, and must a rerun with no new data leave every landed table and model unchanged?
- If unresolved, what cadence, time and time zone does the schedule use, given that it is stored in UTC, and does a run that starts during another one wait, fail or run alongside it, given the plan's concurrent-run limit?
- If unresolved, does a selected model need a run-scoped value such as a run date, and is it supplied by the run, derived from what has landed, or left out of this Flight?
- If unresolved, where does the load read its source in production, and which credentials does it need, given that only secret names may be committed?
- If unresolved, who is told of a failed run and through what route, given that a Flight offers no notification of its own?
- If unresolved, may the Flight run on demand in a MotherDuck sandbox database, and which destination database does the deployed Flight write?

### Guardrails

- Do not choose or apply a selection boundary, failure route, retry, recovery, schedule, overlap or notification rule without approval; explain the alternatives if asked.
- Do not commit a Flight id, a credential, a source location value or the packed dbt project; deployment supplies them and packaging derives the project.
- Do not read a workload credential through an optional lookup or a bare secret alias; a missing credential fails the run.
- Do not treat static validation or a succeeded Flight status as proof that the load and the build succeeded.
- Do not run development-only checks such as dbt unit tests in the scheduled build; some cannot compile in a new destination.
- Do not let the scheduled selection change beyond its approved boundary; any other change fails packaging until it is approved.
- Do not choose or supply a run-scoped value without approval; report any value that would replay, skip or rewind a model's state.
- Do not change the load or the dbt models the Flight invokes; report a defect in them as follow-up work.
- Do not deploy the Flight or activate its schedule; an approved sandbox run executes it on demand only, and the committed Flight is the only source.
- Do not extend into deployment, environment setup, source freshness or readiness gating, or another orchestrator.
