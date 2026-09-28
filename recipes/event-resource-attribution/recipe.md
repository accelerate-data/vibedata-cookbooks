---
id: event-resource-attribution
title: Build auditable event-to-resource attribution
trigger:
  - Revenue or productivity must be reported by employee, asset or team, but responsibility for each event is unclear.
  - Joining events to resource assignments duplicates amounts or assigns events outside the relationship's valid time.
  - Trip or delivery reporting needs defensible driver, vehicle or garage attribution, including shared responsibility.
description: Build event-to-resource relationships with source provenance, approved cardinality and temporal rules, visible unresolved cases, and count and amount reconciliation for observed assignments or approved allocations.
pitch: Explain who or what is responsible for each event, with evidence and totals that survive attribution joins.
job_category: build
area: transformation
readiness: supported
domain_objects:
  - business_event
  - resource
  - assignment
  - allocation
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

Build <attribution_model> to relate events to people or assets for the analytical questions and breakdowns required in this Intent. Inspect approved requirements and source-of-truth assignments before settling event and resource keys, responsibility roles, relationship cardinality, event time and temporal applicability. Separate observed assignments, approved allocations and explicitly synthetic examples. Preserve source-to-output lineage and expose unmatched, ambiguous, unknown and excluded cases with reasons. Implement approved allocation rules only where needed, retaining weights and policy provenance. Materialize attribution and audit outputs in the Intent's sandbox. Verify independent wrong-resource, temporal-boundary, overlap, missing-assignment and fan-out cases; reconcile event counts and additive amounts through joins, including conservation under any many-to-many allocation. Report missing evidence that prevents an agreed question from being answered.

## Verified by

- The contract defines event and resource keys, source and output grains, responsibility roles, cardinality, applicable event time, interval boundaries and time zone rules; observed assignments are supported by authoritative source evidence.
- Every resolved relationship retains event, resource and assignment lineage plus its provenance class: observed, approved allocation or synthetic. Allocations cite the approved policy/version and weights; synthetic outputs and fixtures are explicitly labelled.
- Accepted links satisfy the approved keys, roles, cardinality and temporal rules. Duplicate or overlapping assignment candidates cannot silently multiply event rows; legitimate multiple resources remain represented at the declared bridge grain.
- Independent temporal cases cover before, at and after assignment boundaries, gaps and overlaps. A synthetic resource handover assigns events to the expected resource on each side; current-only joins and arbitrary overlap winners fail the expected results.
- Every scoped event has one auditable resolved, unmatched, ambiguous, unknown or excluded status per attribution scope, with reasons and candidate links where present. Status counts close to input events; missing or conflicting relationships remain visible.
- Distinct event counts and additive amounts reconcile before and after joins, including unresolved and excluded populations, at every required breakdown. Raw bridge-row counts or repeated full event amounts are never passed off as conserved event totals.
- Approved many-to-many allocation conserves each event's count contribution and additive amounts within each policy scope, then reconciles aggregate totals. Weights, rounding, residuals and unallocated balances follow the approved rule and tolerance.
- When allocation is required, an independent synthetic event of amount 100 split 25/75 yields amounts 25 and 75 and count contributions 0.25 and 0.75; totals remain 100 and 1. Equivalent cases cover the approved rule and multiple events sharing resources.
- An independently specified wrong-resource case fails even when event counts and amounts reconcile. Missing assignments produce unresolved output, never a hash-selected resource; ambiguous candidates stay unresolved unless an approved rule resolves them.
- Every agreed question and breakdown is supported or has an explicit gap tied to missing attributes, history, mappings or relationship evidence. Observed responsibility and estimated allocations remain distinguishable in analytical outputs.
- Expected links, statuses, counts and amounts are fixed independently of model SQL before comparison; cases cover valid multi-resource links, duplicate candidates, null keys, unknown resources and every meaningful policy branch.
- dbt checks and independent acceptance queries pass on the actual Intent platform after materialization and rerun; all outputs are read back, and the report records revision, commands, exits, counts, amounts, lineage and unresolved exceptions.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain and sources. Inspect approved requirements, authoritative assignments, event/resource keys, relationship meanings and available history first. Profile nulls, duplicates, orphan keys, candidate multiplicity, gaps and overlaps. Use Ask first only for unresolved semantics; samples or convenient SQL cannot authorize responsibility. Document attribution scopes, grains, roles, cardinality, event time, interval boundaries, time zones, status precedence and any approved allocation policy, weights, precision and tolerance. Retain source identities, assignment evidence, policy versions and unresolved candidates. Design event-level audit outputs and relationship bridges so multiple links do not inflate additive totals. Fix expected fixtures independently before implementation: wrong-resource links, missing assignments, temporal handovers, overlaps, valid multiple links and allocation conservation. Label synthetic data and distinguish allocated from observed responsibility. Implement with the composed skills and current target's dialect and sandbox guidance. Materialize, read back all outputs and rerun; reconcile status populations, event counts and amounts within each scope and at required breakdowns. Use only an approved writable fixture area and keep Domain sources read-only. Report missing relationship evidence and untested required cases as incomplete verification.

### Compose

- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which analytical questions, resource roles, breakdowns and additive measures must attribution support, and which event population is in scope?
- If source evidence does not settle it, what establishes responsibility: which authoritative assignment, explicitly synthetic relationship or approved allocation policy, and which keys and cardinalities apply?
- If unspecified, which event time selects an assignment, how do time zones and interval endpoints work, and how must gaps, overlaps, missing keys and conflicting candidates be treated?
- If allocation is needed but not approved, what policy and scope govern weights, event-count contributions, amount measures, rounding, residuals and unallocated balances, and what tolerance applies?
- If unresolved, how should unmatched, ambiguous, unknown and excluded events appear in outputs and totals, and can any approved evidence-based precedence resolve competing assignments?

### Guardrails

- Never fabricate a relationship to enable rankings or economic outputs. A deterministic arbitrary hash, nearest candidate or convenient join key is not evidence of observed responsibility.
- Keep synthetic examples explicitly synthetic and internally consistent; do not mix them into observed totals. Approved allocations remain labelled estimates with policy provenance, not operational facts.
- Do not resolve ambiguous responsibility by arbitrary row selection, drop unmatched events through inner joins or deduplicate away legitimate multiple resources to force uniqueness.
- Do not infer temporal applicability from today's assignment or fill missing history without approval. Expose questions that absent relationship evidence prevents from being answered.
- Never sum repeated full event values across a many-to-many bridge. Separate distinct-event reporting from allocated count contributions; reconcile each independent role or policy scope without adding scopes together.
- Add only relationships and attributes needed for the agreed questions. Missing optional mappings do not authorize invented inputs or unrelated modelling work.
- Use the actual Intent platform and provided sandbox. Do not substitute another engine, synthesize an absent sandbox or mutate operational systems or Domain sources to manufacture evidence.
- Build success and balanced totals alone do not prove attribution. Required independent link, temporal, cardinality and allocation checks must pass before claiming completed verification.
