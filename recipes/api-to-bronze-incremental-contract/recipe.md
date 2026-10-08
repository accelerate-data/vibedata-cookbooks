---
id: api-to-bronze-incremental-contract
title: Land a SaaS or REST API into bronze with an incremental cursor and a schema contract
trigger:
  - An API source has to load into bronze incrementally instead of reloading everything on every run.
  - A pipeline breaks whenever the source API adds a field or changes a field's type.
  - The team has to know which of an API's records landed in bronze, which were refused and why, and which it can show were missed.
description: Build a dlt pipeline that lands a SaaS or REST API into bronze incrementally under an approved cursor, enforces an approved schema contract for new fields and changed types, keeps refused records visible, and accounts for each load's records by outcome and by extraction, completely where the API offers an independent view of what it holds.
pitch: Land an API into bronze incrementally, with a schema contract for changed fields and an account of every record it can see.
job_category: build
area: ingestion
readiness: supported
domain_objects:
  - dlt_pipeline
  - dlt_resource
  - bronze_table
  - rejected_records
  - reconciliation_report
works_with:
  platforms:
    - duckdb_local
    - motherduck
    - fabric_lakehouse
    - fabric_warehouse
    - redshift
  tools:
    - dlt
qualifiers:
  - Assessed end to end on duckdb_local only; the other listed targets rely on dlt support and are unassessed.
  - Needs an API that exposes a per-record change cursor; an API without one is outside this Recipe.
  - Studio's rest_api connector is a stub today; read the API with dlt's REST client or a custom resource.
related:
  - managed-connector-to-dlt
evidence:
  features:
    - capturing-requirements
    - add-or-update-source
    - discovering-source-schema
    - generating-dlt-pipeline
    - dlt-unit-testing
    - running-dlt-in-sandbox
    - ingestion-data-testing
    - verifying
  evals: []
---

## Prompt

Build a dlt pipeline in the current Intent that lands <resource_list> from the <source_name> API into bronze. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Load each resource incrementally under the approved cursor, key and write disposition, enforce the approved schema contract for new fields and changed types, keep every refused record visible with its reason, and account for each load's records by outcome (landed, refused or missed) and by extraction (newly read or re-read), completely where the API offers an independent, enumerable view of the records it holds; otherwise account for the records visible through the API and state that unseen misses cannot be proven absent. Report what the load cannot capture.

## Verified by

- Every approved resource lands in bronze under its approved write disposition and, where it has one, business key, and each landed row carries the approved source identifiers and provenance.
- After the first load, each load lands only the records the approved cursor rule selects, including any approved lookback, and a rerun over an unchanged source lands no new record and changes no record's content; re-reads follow the approved re-send rule.
- No record is lost, or re-read beyond the approved lookback, because it shares a cursor value with the stored mark or another record, or writes its cursor with a different offset or format.
- Late, re-sent and corrected records are handled as the approved rules say, and a record the cursor rule cannot reach is reported as missed wherever an independent view of the source shows it.
- Deletes reach bronze as the approved policy says, whether flagged, removed or recorded separately, and the result states which deletes the load cannot see.
- A new field and a changed field type, including on a field the API added after the first load, are handled as the approved contract says, whether the field is added or dropped, the record is refused, the value is kept apart or the load fails.
- Every refused record stays visible where the approved rule puts it, with its reason and the approved identifying detail, a re-read of it keeps its refused outcome, is marked re-read and adds no second refusal, and whether the cursor moves past it follows the approved rule.
- For each load and resource, every relevant source record has one outcome, landed, refused or missed, and every record read is marked newly read or re-read; read records reconcile to what the load requested, outcomes to the relevant source records, by business key and content.
- Where the API offers an independent, enumerable view of its records, such as a full listing, an audit endpoint or a snapshot, every record it holds is accounted for; otherwise the records visible through the API reconcile and the result states that unseen misses cannot be proven absent.
- The result states what the load cannot capture, such as records deleted outright, records later than any approved lookback, or corrections that leave the cursor unchanged.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements. Confirm what the API exposes first: its resources and pagination, each resource's identity, which field marks a change and whether every change moves it, how deletes appear, and whether the API can filter on the cursor. Choose the write disposition, key, cursor and starting point from that evidence and the approved requirements, and state what the choice relies on and what it would miss, such as deletes, corrections that keep their cursor, or records that arrive late. Land each resource with the approved schema contract, keep refused records visible, and carry the approved provenance on every row. Find out whether the API offers an independent, enumerable view of its records, such as a full listing, an audit endpoint or a snapshot. Run the approved loads and give each relevant record one outcome and each record read an extraction status; where such a view exists, reconcile every load against it by business key and content, with each load or periodically over several, and where it does not, reconcile what the API exposes and say that unseen misses cannot be proven absent.

### Compose

- capturing-requirements
- add-or-update-source
- discovering-source-schema
- generating-dlt-pipeline
- dlt-unit-testing
- running-dlt-in-sandbox
- ingestion-data-testing
- verifying

### Ask first

- If unresolved, which API resources are in scope, and are child resources needed?
- If unresolved by the API's evidence, which write disposition, business key, cursor field and starting point each resource uses?
- If unresolved, how a record that arrives with a cursor at or behind what was already loaded is handled: picked up within a bounded lookback (how wide) or missed and reported?
- If unresolved, how the API shows a deleted record, how bronze should show it, and whether records deleted outright must be detected?
- If unresolved, what bronze keeps when a record with a known key is re-sent or corrected: one row per key with the latest copy, every copy, or the copies flagged?
- If unresolved, what the contract does when the API adds a field (add it, drop it, refuse the record or fail the load), and when an existing field, including one added later, changes type (refuse the record, keep the value apart or fail the load)?
- If unresolved, where refused records go and with what reason and payload, whether the cursor moves past them, and how a record with no cursor or no key is treated?
- If unresolved, which source identifiers and provenance every landed row must carry, and whether the reconciliation must list individual keys as well as counts per load?

### Guardrails

- Do not choose or apply a cursor, lookback, delete, identity or schema-contract rule without approval.
- Do not coerce a value the contract refuses into a landed column, or overwrite a landed row with it.
- Do not fall back to a full reload to hide a cursor problem, or re-read records the stored cursor has passed beyond the approved lookback, unless that reload is approved.
- Do not claim deletes, late records or corrections are captured when the chosen cursor cannot see them.
- Do not force business deduplication or transformation into bronze beyond the approved key.
- Do not treat a count match as reconciliation; compare business keys and content.
- Do not claim that no record was missed unless an independent view of the source's records shows it.
