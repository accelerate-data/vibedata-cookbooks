---
id: business-event-fact
title: Build a business-event fact with auditable duplicate handling
trigger:
  - Transaction feeds overlap, and source deliveries may be counted as separate business events.
  - Replayed deliveries change a report's unique event count or additive totals.
  - A trip or consignment fact must preserve valid similar events and explain conflicting records.
description: Build an agreed event-grain fact with an evidence-backed identity rule, deterministic duplicate and correction handling, source lineage, explicit exceptions, and reconciled event counts and additive amounts.
pitch: Count business events with a defensible identity rule and an audit trail for every source row.
job_category: build
area: transformation
readiness: supported
domain_objects:
  - business_event
  - fact_table
  - source_record
works_with:
  platforms:
    - duckdb_local
    - motherduck
    - fabric_lakehouse
    - fabric_warehouse
    - redshift
  tools:
    - dbt
evidence:
  features:
    - profiling-source-data
    - applying-medallion-data-modelling
    - generating-dbt-model
    - dbt-unit-testing
    - running-dbt-in-sandbox
    - verifying
  evals: []
---

## Prompt

Build <fact_name> at the agreed business-event grain for the analytical questions and breakdowns required in this Intent. Inspect approved requirements and source evidence before settling event identity, source delivery identity, duplicate handling, corrections and conflict resolution. Distinguish exact redeliveries, business duplicates, genuinely distinct similar events and conflicting versions. Apply the approved deterministic disposition, preserve source-to-event lineage and expose unresolved, excluded and unknown cases. Validate the reference mappings needed for the agreed questions. Materialize the fact and its audit outputs in the Intent's sandbox, and verify independent duplicate, conflict and valid-repeat cases, source-row disposition closure, event counts and additive amounts.

## Verified by

- The documented grain and identity rule distinguish business events from source deliveries; source evidence supports the chosen keys, and the fact has exactly one row per accepted event at that grain.
- The fact answers the agreed analytical questions and breakdowns; missing attributes, history, mappings or relationship evidence are reported with the questions they prevent from being answered.
- Replaying an identical delivery adds no event and changes no fact amount; each observed source row remains traceable to its disposition and, where resolved, its event.
- Two deliveries proved to describe one business event produce one event under the approved business-duplicate rule, including when their delivery identifiers differ.
- Two distinct event identities with equal timestamps, amounts and descriptive attributes produce two events; valid repeats are retained even when a convenient column subset is identical.
- Conflicting versions and corrections follow the approved precedence and tie rule, independent of input order; unresolved ties remain explicit exceptions with no arbitrary winner. Late corrections meet the agreed update policy.
- Every scoped source row has exactly one auditable disposition: event contributor, redelivery, business duplicate, superseded version, excluded row or unresolved exception. Category counts sum to the source-row count, with no overlap or missing rows.
- Every accepted event links to its contributing source records; duplicate and superseded records link to their resolved event, while exclusions and unresolved cases retain source identity, reason and any candidate event links.
- For each additive measure, source totals reconcile to fact totals plus the approved adjustments for every other disposition at the agreed breakdowns. Independent expected amounts show that redeliveries and superseded values are not counted twice.
- Required reference mappings match approved meanings and cardinalities without event fan-out; unknown, unmapped and ambiguous codes remain visible and reconcile to input counts and amounts rather than disappearing through joins.
- Independent fixtures state expected counts, identities, dispositions and amounts before comparison; synthetic relationships are labelled as synthetic, observed links cite source evidence, and approved allocations cite their rule.
- dbt checks and independent acceptance queries pass on the actual Intent platform after materialization and rerun; every output is read back, and the report records the revision, commands, exits, counts, amounts and unresolved exceptions.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain and sources. Inspect approved requirements, source schemas, key and version semantics, delivery metadata and reference relationships first. Profile candidate identity collisions, nulls, repeats, conflicting payloads and mapping fan-out. Resolve only open business decisions through Ask first; sample values or existing code cannot authorize a policy. Record the event grain, scoped population, keys, precedence, tie and correction rules, dispositions and additive reconciliation equations. Stop if source identity cannot support the agreed distinction. Design the fact and audit outputs at appropriate layers; retain source identities and reasons. Derive expected cases independently of model SQL, including replay, different deliveries of one event, distinct equal-valued events, conflicts, ties, late corrections and unknown mappings. Label synthetic fixtures and any approved allocation. Implement with the composed skills and the current target's dialect and sandbox guidance. Materialize, read back all outputs, rerun and reconcile source rows, events and amounts; capture actual results and unresolved cases. Use only an approved writable fixture area for changed-data scenarios; keep Domain sources read-only. Report any unavailable required evidence as incomplete verification.

### Compose

- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If requirements do not settle them, which analytical questions, breakdowns and additive measures must this fact support, and what source population is in scope?
- If source evidence leaves identity unresolved, what defines one business event, what distinguishes two similar events, and which source identifiers establish delivery identity and legitimate repeats?
- If not already approved, which evidence establishes a business duplicate, which version wins a conflict, how are ties and late corrections treated, and which cases must remain exceptions or exclusions?
- If required reference semantics are unresolved, what do codes and relationships mean, which cardinalities apply, and how must unknown or ambiguous mappings appear in the agreed outputs?
- If not specified, how should each non-contributing disposition adjust additive measures, and are any allocations needed and explicitly approved?

### Guardrails

- Do not invent a natural key, collapse materially distinct rows or discard valid repeats to make uniqueness pass. Missing identity evidence is a blocker to execution.
- Do not treat a loader row as an event or assume exact row equality proves business duplication. Preserve the source's approved repeat semantics.
- This is event identity and disposition modelling, not customer or entity golden-record resolution. Do not require deduplication in bronze for every source.
- Never infer business intent or reference meaning from sample values or convenient existing code. Preserve unknown, unmapped, ambiguous and excluded cases with reasons.
- Do not present synthetic relationships or approved allocations as observed operational facts. Add only attributes and history required by the agreed questions.
- Do not select winners by arrival order or an arbitrary tie-breaker unless that rule is explicitly approved and reproducible; retain conflicting evidence.
- Use the actual Intent platform and provided sandbox. Do not substitute a different engine, synthesize an absent sandbox or mutate Domain sources to manufacture evidence.
- Build success alone does not prove event semantics. Do not claim completed verification while required cases, reconciliation or output read-back remain untested.
