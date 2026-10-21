---
id: batch-cdc-current-state
title: Build current-state tables from exported database change events
trigger:
  - A batch export of database change events is available and the current state of its tables has to be rebuilt without reading the source database again.
  - Batches arrive duplicated or out of order, and the rebuilt state must not depend on arrival order.
  - Consumers need to know which tables are trustworthy now, and why one stopped, when part of a transaction is missing or an event cannot be applied.
description: Load exported database change events into a ledger, rebuild each table's current state by source position, and publish every invalid event and incomplete transaction with its reason, with each affected table's state published as approved and checked against independently derived expected tables.
pitch: Rebuild current state from exported change events by source position, with every gap and unusable event listed and affected tables blocked as approved.
job_category: build
area: ingestion
readiness: supported
domain_objects:
  - change_event_ledger
  - current_state_table
  - table_state
  - problem_report
works_with:
  platforms:
    - duckdb_local
    - motherduck
    - fabric_lakehouse
    - fabric_warehouse
    - redshift
  tools:
    - dlt
    - dbt
qualifiers:
  - Finite exported batches only; a live streaming connector is out of scope.
  - Needs a source position on every event and a way to tell that a transaction is complete.
  - Reading the source tables belongs to database-tables-to-bronze; delivering the files belongs to file-drop-to-bronze.
  - Keeping every event as a fact, or history of row versions, belongs to business-event-fact and dbt-snapshot-history.
related:
  - database-tables-to-bronze
  - file-drop-to-bronze
  - business-event-fact
  - dbt-snapshot-history
evidence:
  features:
    - capturing-requirements
    - generating-dlt-pipeline
    - generating-dbt-model
    - verifying
  evals: []
---

## Prompt

Build current-state tables for <table_list> from the <export_location> database change-event export, without reading the source database. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Land every delivered event in a ledger with the file it arrived in kept as provenance only, then rebuild each table's current state from the ledger, ordered by the approved source position and never by arrival. Apply inserts, updates and deletes as approved, treat events covered by the approved bootstrap boundary as approved, and publish each table's state, whether it is blocked and what it leaves out, and one list of every invalid event and every incomplete transaction with its reason. A repeated or reordered load must leave the same accepted state. Check the result against expected tables derived independently by hand, and say what the export cannot show.

## Verified by

- Every delivered event lands in the ledger once under the approved event identity, with arrival file kept as provenance only, and the ledger count equals the distinct events counted independently from the export.
- Order follows the approved source position and tie-break rule; the same events in a different file order, or loaded again, give identical current state and identical problem lists.
- A repeated or duplicated batch changes neither the ledger nor the current state; events sharing an identity but differing in content are handled as approved and never silently merged.
- Each current-state table has one row per live key carrying the last applied event's row values and the approved audit columns; a deleted key appears as the approved delete policy says.
- An older update arriving after a delete does not bring the key back; a later insert of that key, and an update positioned after a delete with no reinsert, are each handled as the approved rules say.
- Events at or below the approved bootstrap boundary are handled as the approved boundary rule says and are still accounted for with that reason.
- Each incomplete transaction is listed per affected table with declared, observed and missing counts, and each affected table's published state follows the approved block rule and states what it leaves out; tables outside the approved block scope are unaffected.
- Each event that cannot be ordered or applied is listed once with one reason, is never applied, and affects its table as the approved rule says.
- Every ledger event ends in exactly one disposition (applied, covered by the boundary, invalid, or withheld by a block), and the counts close.
- Published current state, table state and problem list equal expected tables derived independently by hand from the export and approved rules, compared both ways with nulls as values.
- What the export cannot show, such as events never delivered or a transaction with no end marker, is stated as unproven and not claimed absent.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements. Read the export first: its format, the field that gives each event's source position, transaction, operation and row images, how a transaction's completeness is signalled, whether a snapshot or bootstrap position is marked, and how amounts and timestamps are typed. If the export has no source position or no way to tell a transaction is complete, or no statement of where bootstrap ends, stop and raise it as a blocker; do not order by arrival or invent a position. Land the events through a supported load route without business rules, then decide ordering, completeness, validity, coverage and blocking in the models. Write the expected tables by hand from the export and the approved rules before building, and compare built to expected in both directions. Prove a reordered and a repeated load leave the same state, state which export conditions the example does not exercise, and report what the export cannot show.

### Compose

- capturing-requirements
- generating-dlt-pipeline
- generating-dbt-model
- verifying

### Ask first

- If unresolved, what is the export's format, which fields carry the source position, transaction, operation and before and after images, what does it guarantee about ordering and transaction markers, and how are events at one position ordered?
- If unresolved, which tables are in scope, what key identifies a row in each, and which audit columns should current state carry?
- If unresolved, where does the bootstrap end, and what happens to events at or below it?
- If unresolved, how is a transaction known to be complete, and which tables does an incomplete one block, and what should a blocked table publish: freeze at the last complete point, skip the transaction, or nothing?
- If unresolved, which unusable events are invalid (no position, unknown operation, missing key or image, a change to a key that is not live), and does an invalid event block its table or only get listed?
- If unresolved, what is an event's identity, and how are repeated deliveries and conflicting copies of one event handled?
- If unresolved, how should a deleted row appear, and what happens when its key returns?
- If unresolved, what happens when an update carries a partial image or the images gain a column or change type, and how should timestamps and decimals be typed?

### Guardrails

- Do not order, deduplicate or block by file name, arrival order or load time.
- Do not invent a source position, a transaction boundary or a bootstrap boundary the export does not carry.
- Do not apply an event that is invalid or that the approved boundary or block rule withholds.
- Do not report a blocked or partly applied table as complete, or an event never delivered as absent.
- Do not derive expected tables from the models or pipeline they check.
- Do not read the source database or add a streaming connector as part of this work.
