---
id: fabric-data-pipeline-as-code
title: Author a Fabric Data Pipeline that sequences ingestion, dbt, and downstream refresh as committed code
trigger:
  - A Fabric Data Pipeline was built by clicking and lives only in the workspace.
  - Ingestion, the dbt build and a downstream refresh have to run in order on a schedule in Fabric.
description: Author a Fabric Data Pipeline and its schedule as committed code that runs ingestion, the dbt job and a downstream step in order, validate its dependency graph statically, run it once on demand, and document its schedule and dependency order.
pitch: Turn a clicked-together Fabric pipeline into committed code that runs ingestion, dbt and the downstream refresh in order.
job_category: build
area: orchestration
readiness: supported
domain_objects:
  - fabric_data_pipeline
  - dbt_job
  - schedule
works_with:
  platforms:
    - fabric_lakehouse
    - fabric_warehouse
  tools:
    - dlt
    - dbt
evidence:
  features:
    - generating-orchestration
    - evaluating-orchestration
    - running-orchestration-in-sandbox
    - documenting-orchestration
  evals: []
---

## Prompt

Author a Fabric Data Pipeline named <pipeline_name> that runs <ingestion_pipeline>, then the dbt job, then <downstream_step>, on a <cadence> schedule with <retry_policy>. Commit the pipeline and its schedule as code, validate its dependency graph, run it once on demand in the sandbox, and document the schedule and the dependency order.

## Verified by

- The pipeline definition and its schedule are committed to the repository as code.
- Every artifact the pipeline invokes exists in the repository.
- Static validation of the pipeline's dependency graph passes with no findings.
- An on-demand sandbox run of the pipeline completes, and its run evidence is recorded.
- The schedule, the retry policy and the step order are documented.

## Agent guidance

### Instructions

Inventory the ingestion pipeline, the dbt job and the downstream step the pipeline will invoke, and confirm each exists in the repository before referencing it. Generate the pipeline and its schedule as code, validate the dependency graph statically, run the pipeline once on demand in the sandbox, and document its schedule and dependency order before declaring the Recipe complete.

### Compose

- generating-orchestration
- evaluating-orchestration
- running-orchestration-in-sandbox
- documenting-orchestration

### Ask first

- Ask for the failure notification target only if no approved requirement or project convention names one.
- Ask whether a step is optional only if the request does not say how its failure affects the steps after it.

### Guardrails

- Do not reference an artifact the repository does not contain.
- Do not edit the pipeline by hand in the workspace; the committed definition is the only source.
- Do not treat static validation as proof that the pipeline runs; record an on-demand run.
