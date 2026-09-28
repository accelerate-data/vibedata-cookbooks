---
id: prove-dbt-change-safe
title: Assess an existing dbt change for safe merge without modifying it
trigger:
  - An existing dbt change builds successfully but reviewers still need evidence that its business answers remain valid.
  - A change to fleet, shipment or financial models needs independent checks against agreed requirements and an approved baseline.
  - A reviewer must distinguish an implementation defect from missing data, missing relationships or insufficient test coverage.
description: Produce an independent assessment of an existing dbt change against approved requirements and baselines, with semantic checks, evidence gaps and a merge recommendation while preserving the reviewed implementation.
pitch: Review the business answers behind a dbt change with independent evidence and leave its implementation unchanged.
job_category: prove
area: data-quality
readiness: supported
domain_objects:
  - dbt_change
  - assurance_requirement
  - approved_baseline
  - assessment_report
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
    - evaluating-dbt-project
    - dbt-unit-testing
    - running-dbt-in-sandbox
    - verifying
  evals: []
---

## Prompt

Assess <reviewed_change> for safe merge against this Intent's approved assurance requirements and <approved_baseline>, without modifying the reviewed implementation. Inspect the change, dependencies, source evidence and required analytical questions first. Preserve existing acceptance criteria and settle only unresolved scope, intentional differences and evidence thresholds. Independently examine applicable grain, keys, mappings, relationship provenance, history, metric populations, aggregation, required dimensions and enrichment grain. Include incremental idempotency, unique-key integrity and late-arriving cases when relevant. Run checks on the actual Intent platform using isolated test and evidence locations. Deliver an evidence-backed report that classifies every requirement, records limitations and unproven claims, and gives a bounded merge recommendation. Distinguish a missing convenience view from unavailable source information or relationships. Do not repair failures or change the candidate to obtain passing evidence.

## Verified by

- The assessment fixes the candidate revision and implementation hashes, approved requirements, impacted dependencies and consumers, required questions/breakdowns, population, grain, baseline identity/slice, intentional differences and evidence thresholds; existing assurance criteria remain in scope.
- Before/after revision and hash checks confirm the reviewed implementation is unchanged. Tests, fixtures, logs and the report reside only in an isolated evidence workspace; execution uses the provided sandbox on the actual Intent platform and keeps Domain sources read-only.
- Each requirement is classified as implemented-and-demonstrated, implemented-but-insufficiently-exercised, unsupported, or explicitly out of scope, with evidence and rationale. Scope exclusions require approval; missing evidence never counts as a pass.
- Build and existing-test results, read-only project audit findings, impacted lineage and downstream contracts are recorded. Missing packages, sources, fixtures or evaluators and failing baselines remain visible; the report identifies which claims these gaps prevent from being demonstrated.
- Applicable grain/key, deduplication, mapping, relationship and enrichment checks establish permitted cardinalities and source-to-output traceability. Unmapped, ambiguous, excluded and unknown cases stay visible; scoped counts and amounts reconcile without unexplained loss or multiplication.
- A labelled synthetic fan-out case has one event of amount 10 and two matching reference rows: at approved event grain, the expected result is one event and amount 10, or an explicit ambiguity. A two-row result totalling 20 fails; expectations are fixed independently before executing candidate SQL.
- Applicable population, formula and aggregation cases independently recompute inclusion, null/zero handling, numerators, denominators and rollups at required dimensions. Unequal group sizes expose averages of averages; grand-total agreement cannot mask offsetting errors or wrong subgroup answers.
- Where history matters, independent cases cover changed/unchanged entities, validity boundaries, gaps/overlaps, event-time attribution and late corrections under approved policy. Required historical attributes and relationship provenance exist, or their absence limits the supported questions.
- Incremental changes are exercised with repeated identical inputs, unique-key checks and an approved late-arriving insert/update case. The rerun has no unintended row or value changes; late data affects exactly the independently expected keys and values, with all unexercised cases disclosed.
- Candidate output is compared to the approved baseline on the agreed scope, keys, dimensions and precision. Baseline provenance and inherited assumptions are disclosed separately from independent recomputation; every difference is explained as approved, a defect or unresolved evidence.
- Each agreed question has the necessary attributes, mappings, history and observed relationship evidence or an explicit gap. Missing convenience views are distinguished from unavailable information; approved allocations and synthetic fixtures are labelled and cannot prove real source relationships.
- The report records revision, platform/target, commands, exits, input slice, expected/actual results and artifact locations; materialized outputs are read back. Its merge recommendation cites unresolved findings, limitations and unproven claims, without equating build success with semantic safety.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain and sources. Read approved requirements and source evidence before evaluating code. Freeze the candidate revision/bytes, baseline, acceptance criteria and isolated test/evidence locations. Trace changed paths through dependencies and consumers; use the read-only project audit and direct dbt testing operations against the unchanged candidate. Establish independent expected answers before tests, including a case that defeats a plausible wrong implementation. Select relevant key, population, relationship, history, enrichment and incremental cases from the agreed questions; disclose every unexercised requirement. Use current target dialect and sandbox guidance, materialize and read back outputs, compare the approved baseline and reconcile independent results. Use only approved writable fixtures for history or late-data experiments; keep Domain read-only. Run verifying only for assurance evidence and reporting with fixed locations; its stage bookkeeping or failure routes must not alter the candidate. Failed audits, builds or tests produce findings, never repair steps. Record revision, commands, exits and limitations, classify each requirement, and recheck candidate hashes before the recommendation. An unavailable sandbox, package, fixture or baseline blocks affected evidence rather than authorizing a substitute engine, invented data or implementation changes.

### Compose

- evaluating-dbt-project
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which analytical questions, populations, output grain, required dimensions and downstream contracts must this change preserve, beyond its existing assurance requirements?
- If not approved, which baseline revision, input slice, keys, comparison precision and evidence thresholds apply, and which differences are intentional?
- If unclear, what grain, duplicate, mapping, relationship, allocation and enrichment policies govern ambiguous or missing cases, and which source evidence supports them?
- If history or incremental behavior is relevant but unresolved, what event-time, validity, correction and late-arriving policies must hold, and which writable isolated fixtures are approved to exercise them?
- If scope is disputed, which requirements are explicitly out of scope, and who can approve that exclusion or accept the report's remaining limitations?

### Guardrails

- Do not change reviewed models, macros, configuration, dependencies or existing tests. Preserve implementation bytes and revision; place new tests, fixtures, run artifacts and reports only in the isolated evidence workspace.
- No audit, test, sandbox or verification failure authorizes refactoring, repair, dependency changes, shipping or merge. A recommendation is an assessment outcome; fixes and release actions need a separate task.
- Do not infer business intent from convenient SQL or sample values, weaken existing assurance requirements, lower evidence thresholds or discard materially distinct records to make checks pass.
- Do not treat an approved baseline as independent truth. Disclose shared assumptions and stale evidence, and test agreed semantics independently; a failing or unavailable baseline is an explicit evidence limitation.
- Do not invent operational relationships, history or mappings. Synthetic fixtures prove behavior on stated examples only; approved allocations remain distinguishable from observed source facts.
- Do not add convenience views merely because they are absent. Establish whether the required answer is possible from available sources and relationships; report a real information gap without repairing it.
- Use only the actual Intent platform and provided sandbox. Do not synthesize an absent sandbox, mutate Domain sources, substitute an easier engine or claim an unexecuted check passed.
- Keep assessment classifications in the report and preserve the verification evidence contract. No Skill wrapper overrides the no-repair boundary, and no second Recipe is required to complete this assessment.
