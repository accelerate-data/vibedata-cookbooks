---
id: api-to-bronze-incremental-contract
title: Land a SaaS or REST API into bronze with an incremental cursor and a schema contract
trigger:
  - An API source has to load into bronze incrementally instead of reloading everything on every run.
  - A pipeline breaks whenever the source API adds or changes a field.
description: Build a dlt pipeline that lands a SaaS or REST API into bronze with cursor-based incremental loading and a schema contract that decides how new or changed columns are handled, with pytest coverage of both and a sandbox load that proves the landed row counts.
pitch: Land an API into bronze incrementally, with a schema contract that decides what happens when a field changes.
job_category: build
area: ingestion
readiness: supported
domain_objects:
  - dlt_pipeline
  - dlt_resource
  - bronze_table
works_with:
  platforms:
    - duckdb_local
    - motherduck
    - fabric_lakehouse
    - fabric_warehouse
    - redshift
  tools:
    - dlt
evidence:
  features:
    - discovering-source-schema
    - generating-dlt-pipeline
    - running-dlt-in-sandbox
    - dlt-unit-testing
    - ingestion-data-testing
  evals: []
---

## Prompt

Build a dlt pipeline that lands <source_name> into bronze. Load <resource_list> incrementally on the <cursor_field> cursor, starting from <initial_value>. Handle new columns with the <new_column_policy> schema contract (evolve, freeze or discard_row), and freeze type changes. Add pytest coverage for the cursor and the contract, run the pipeline in the sandbox, and report the landed row count for each resource.

## Verified by

- A sandbox load lands every requested resource in bronze, and the landed row count of each resource is reported.
- A second run loads only rows newer than the persisted cursor value.
- A fixture that adds a column is handled exactly as the agreed new-column policy states.
- A fixture that changes a column's type fails the schema contract test.
- The pytest suite covers the cursor and both contract cases, and it passes.
- The connector and dlt versions are pinned in the pipeline's requirements.

## Agent guidance

### Instructions

Confirm the source connection resolves and discover its resources before writing pipeline code. Settle the cursor field, write disposition and primary key of each resource from the request and the source's evidence, and record each choice. Build the pipeline on the vendored connector, cover the cursor and both contract cases in pytest, then run it in the sandbox twice and collect the row counts and the second-run evidence before declaring the Recipe complete.

### Compose

- discovering-source-schema
- generating-dlt-pipeline
- running-dlt-in-sandbox
- dlt-unit-testing
- ingestion-data-testing

### Ask first

- Ask for the write disposition of a resource (append, replace or merge) only if neither the request nor the source's evidence settles it.
- Ask for the primary key of a merge resource only if the source exposes no defensible one.
- Ask whether child resources are needed only if the source exposes them and the request does not say.

### Guardrails

- Pin the connector and dlt versions in the pipeline's requirements.
- Do not fall back silently from MotherDuck to local DuckDB.
- Do not report the contract as tested until a fixture with a changed type has turned its test red.
- Do not reload rows the persisted cursor has already passed.
