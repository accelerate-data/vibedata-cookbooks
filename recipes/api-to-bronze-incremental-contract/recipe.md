---
id: api-to-bronze-incremental-contract
title: Land a SaaS or REST API into bronze with an incremental cursor and a schema contract
trigger:
  - An API source has to load into bronze incrementally instead of reloading everything on every run.
  - A pipeline breaks whenever the source API adds or changes a field.
  - A logistics API repeats shipment events across source rows that must remain traceable for downstream modelling.
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

Build a dlt pipeline that lands <source_name> into bronze in the current Intent. Load <resource_list> incrementally on the <cursor_field> cursor, starting from <initial_value>, using the agreed write disposition and keys. Handle new columns with the <new_column_policy> schema contract (evolve, freeze or discard_row), and freeze type changes. Preserve the agreed source identifiers and provenance needed for downstream conformance. Add pytest coverage for the cursor and the contract, run the pipeline in the sandbox twice, and report landed source-row counts for each resource separately from any evidenced business-event counts. Retain approved source, cursor and late-arrival semantics; do not impose business deduplication in bronze.

## Verified by

- A sandbox load lands every requested resource in bronze, and the landed row count of each resource is reported.
- A second run loads only rows newer than the persisted cursor value.
- A fixture that adds a column is handled exactly as the agreed new-column policy states.
- A fixture that changes a column's type fails the schema contract test.
- The pytest suite covers the cursor and both contract cases, and it passes.
- The connector and dlt versions are pinned in the pipeline's requirements.
- Each resource records its approved write disposition, keys, cursor and late-arrival policy; loaded rows, destination counts and contract exclusions reconcile to source/audit evidence with explicit count definitions.
- Agreed source identifiers and provenance survive landing and trace output rows to the source. Missing or ambiguous identifiers, unknown values and unmapped cases are exposed for downstream conformance.
- An append fixture with three distinct source rows, two referencing one event and one a distinct event with equal measures, lands three rows with all agreed identifiers. Expectations are fixed independently; loader identity is not reported as event identity.
- The assigned destination and mandatory shipped bronze gate pass. Any unavailable custom remote bronze pytest is recorded as deferred, not passed; local mocked cursor and contract tests still pass.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain and sources. Inspect approved requirements, confirm the source connection and discover resources. Establish required questions and breakdowns; expose missing identifiers, history or relationship evidence needed downstream. Record each resource's approved cursor, initial value, late-arrival policy, write disposition and primary key; source evidence informs choices but does not authorize semantic changes. Agree which source identifiers and provenance must survive landing, distinguishing observed relationships from approved allocations or synthetic fixtures. Build on the vendored connector without bronze business transformations. Use independent mocked responses to test cursor wiring, repeated-event rows and distinct events with equal measures. Enforce new-column and changed-type cases against an established schema in isolated local pytest. The append fixture tests source-row preservation; also test the actual approved disposition and its expected counts. Run two real sandbox loads, assert the assigned destination, run the mandatory shipped bronze gate and collect load packages, source/audit counts and second-run evidence. Reconcile extracted/loaded rows, destination changes and exclusions under the contract, keeping source rows separate from business events. Retain source-to-bronze traceability. Record custom remote bronze tests as deferred when credentials are unavailable; do not waive local pytest or the shipped gate.

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
- Ask which analytical questions and breakdowns, source identifiers and provenance must be supported downstream only if approved requirements leave them unresolved.
- Ask for the cursor, initial value, late-arrival or schema policy only if approved requirements do not settle it; expose conflicts without changing existing policy.

### Guardrails

- Pin the connector and dlt versions in the pipeline's requirements.
- Do not fall back silently from MotherDuck to local DuckDB.
- Do not report the contract as tested until a fixture with a changed type has turned its test red.
- Do not reload rows the persisted cursor has already passed.
- Do not call landed rows or unique _dlt_id values unique business events without independent evidence of business grain.
- Do not force business deduplication into bronze, discard distinct source rows to pass a test, or change approved source, cursor, write-disposition or late-arrival semantics.
- Preserve agreed source identifiers alongside loader identity; report missing evidence instead of inventing keys or operational relationships.
- Synthetic fixtures prove the stated cases, not observed source relationships; report contract exclusions explicitly.
