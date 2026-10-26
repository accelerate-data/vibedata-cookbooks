---
id: fabric-data-pipeline-as-code
title: Author a Fabric Data Pipeline that sequences ingestion, dbt, and downstream refresh as committed code
trigger:
  - The nightly loads, the dbt build and the report refresh are run by hand or live only as a pipeline clicked together in the workspace.
  - Nobody can say what happens to the dbt build and the report refresh when one load fails, times out or is retried.
  - Production runs on Fabric, and the sequence, its retries and its schedule have to be reviewed and deployed from the repository.
description: Author a Fabric Data Pipeline and its schedule as committed code that runs the approved loads, the dbt build and a downstream refresh in order under approved failure, retry and overlap rules, prove its order and failure paths against the committed definition, and run it where an ephemeral Fabric run is approved.
pitch: Turn a clicked-together Fabric pipeline into committed code whose order, failure rules and schedule are proven against its definition.
job_category: build
area: orchestration
readiness: supported
function:
  - cross-functional
domain_objects:
  - fabric_data_pipeline
  - dbt_job
  - schedule
  - pipeline_activity
works_with:
  platforms:
    - fabric_lakehouse
    - fabric_warehouse
  tools:
    - dlt
    - dbt
qualifiers:
  - Not yet assessed end to end on fabric_lakehouse or fabric_warehouse.
  - Sequences existing loads and dbt models; it authors only the pipeline, its schedule and the items that invoke them.
  - Outside a Fabric Domain only the committed definition can be proven; running it needs a Fabric workspace.
  - Needs a Studio route for dlt to read source files; cloud buckets (ADLS, S3) have none today.
  - Scheduling on MotherDuck belongs to motherduck-flight-scheduling.
related:
  - motherduck-flight-scheduling
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

Author a Fabric Data Pipeline named <pipeline_name> that runs <loads>, then the dbt build of <dbt_selection>, then <downstream_refresh>, on <schedule>, as committed code together with its schedule and the execution items it authors. Inherit the Intent's repository, platform, Domain, loads, dbt project and approved requirements, and resolve only the semantics they leave open: order and parallelism, required and optional steps, what runs after each kind of failure, retries and timeouts, the schedule and overlapping runs, run-scoped values, and failure notification. Validate the pipeline statically, prove its order and every approved failure path against the committed definition, run it on demand in an ephemeral Fabric workspace where that is approved, document its steps, failure rules, schedule and deployment prerequisites, and state what the evidence cannot prove.

## Verified by

- The pipeline, its schedule and every execution item this Recipe authors are committed as code, and no committed item holds an environment-specific workspace, item or connection id or a credential.
- The pipeline passes static validation against the platform's pipeline schema with no findings, and every activity invokes either an item this Recipe committed or an approved existing external workload whose reference resolves.
- A workload that is missing, unresolvable or unfinished is reported as a blocker to execution, never as a resolved dependency; recording it as a deployment prerequisite does not count as verification.
- Under the platform's documented dependency, retry, timeout and run-status rules, the committed definition runs steps in parallel only where approved and starts no step before those it depends on reach the state the approved routing requires.
- Each workload step carries the approved retries, retry interval and timeout, any step not safe to retry or run alongside another is named, the schedule carries the approved cadence, time and time zone, and the pipeline or schedule carries the approved overlap behaviour.
- Under those rules, each failure path, one or more steps failing or timing out after their retries, runs or skips exactly the approved later steps and ends with the approved run status and a message naming each failed step the approved rule says to report.
- Under those rules, the refresh starts only after a dbt build the approved rule treats as succeeded; a build it treats as failed, such as a warn-severity test that finds rows where the rule says so, fails a step the refresh depends on, judged by the workload's own result.
- Under those rules, the refresh step succeeds only once the refresh it started completes, and an empty load is routed as approved; that deployed items behave so, and a failing workload fails its activity, is shown only where an on-demand run in an ephemeral Fabric workspace is approved.
- A selected model that needs a run-scoped value receives it as approved, or is left out and reported as needing its own run, with any output that reads it named; any value that would replay, skip or rewind a model's state is reported and used only where approved.
- Where an on-demand run in an ephemeral Fabric workspace is approved, each step's status, the routing and the run status there match the approved rules and each workload's own result agrees with its step; otherwise every run-time claim is reported unproven.
- The approved notification route is committed without its connection; that connection and the other bindings deployment supplies (source routes, secrets, the dbt target) are reported as unverified inputs, and delivery stays unproven unless an approved ephemeral Fabric run delivers it.
- What the evidence cannot prove is reported, including platform behaviour shown only from documentation.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, loads, dbt project and approved requirements, and resolve only the semantics they leave open. Confirm that each load, the dbt selection and the downstream target is either authored here or an approved existing external workload whose reference resolves, report any missing or unfinished one as a blocker to execution, and find which selected models need a run-scoped value and how each behaves without one. Author the pipeline in the platform's native format: activities for the workloads, dependency conditions that express the approved routing, the approved policy on each workload step, routing that gives a run whose optional step failed the approved status and message, and a schedule that only deployment activates. Keep every environment binding out of the committed items. Validate the pipeline statically, then show its order and each approved failure path against the committed definition under the platform's documented dependency, retry, timeout and run-status semantics, judging each step by its own item's exit; run it on demand in an ephemeral workspace where approved. Document the steps, their failure rules, the schedule and the deployment prerequisites, and report what was not proven.

### Compose

- generating-orchestration
- evaluating-orchestration
- running-orchestration-in-sandbox
- documenting-orchestration

### Ask first

- If unresolved, which loads, which dbt selection and which downstream refresh does the pipeline sequence, which of them are existing external workloads, and which steps may run in parallel?
- If unresolved, which steps are required and which optional, what runs after each kind of failure, and what status and message does a run report when an optional step failed?
- If unresolved, does a dbt test that only warns but finds rows fail the build and stop the downstream refresh, and does the build run when a load lands nothing?
- If unresolved, how many retries, how far apart and what timeout apply to each step, and is each step safe to retry or to run alongside another?
- If unresolved, what cadence, time and time zone does the schedule use, and does a trigger that fires during a run queue, skip or start alongside it?
- If unresolved, does a selected model need a run-scoped value such as a run date, and is it supplied by the run, derived from what has landed, or left out of this pipeline?
- If unresolved, who is told of a failure and through what route, given that no connection or credential may be committed?
- If unresolved, may the pipeline run on demand in an ephemeral Fabric workspace, and which source routes, secret store and dbt target does the deployed pipeline use?

### Guardrails

- Do not choose or apply an order, failure route, retry, schedule, overlap or notification rule without approval; explain the alternatives if asked.
- Do not invoke a workload that is neither committed by this Recipe nor an approved existing external workload whose reference resolves.
- Do not commit an environment-specific workspace, item or connection id or a credential; bindings are supplied at deployment.
- Do not deploy, activate the schedule or edit the pipeline in a workspace by hand outside an approved ephemeral run; the committed definition is the only source.
- Do not treat static validation or a succeeded pipeline status as proof that the workloads succeeded.
- Do not choose or supply a run-scoped value without approval; report any value that would replay, skip or rewind a model's state.
- Do not change the loads or dbt models the pipeline invokes; report a defect in them as follow-up work.
- Do not treat a missing or unfinished workload as resolved; it blocks execution until it exists, and listing it as a deployment prerequisite is not verification.
- Do not extend into deployment, environment setup, source freshness gating or another orchestrator.
