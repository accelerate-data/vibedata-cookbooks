---
id: versioned-data-contract-cutover
title: Add a breaking data contract change as a new version beside the old one
trigger:
  - A required change to a published relation's grain, column meaning or shape cannot keep the old interface.
  - Known consumers cannot all switch on the same day and must keep working while they move.
  - Someone must say what changed, what each reader has to do and when the old version can be retired.
  - A reader that treats the new version as if it had the old grain would quietly get a wrong answer.
description: Build a breaking change to a relation's grain, column meaning or shape as a new version beside an unchanged old one, with a change record, revised queries for a bounded set of named consumers and observable criteria for retiring the old version.
pitch: Build a breaking change as a new version beside the old one, with named consumers revised and checked and retirement left as stated criteria.
job_category: re-engineer
area: transformation
readiness: supported
domain_objects:
  - previous_version
  - new_version
  - change_record
  - named_consumer
  - retirement_criteria
works_with:
  platforms:
    - duckdb_local
    - motherduck
    - fabric_lakehouse
    - fabric_warehouse
    - redshift
  tools:
    - dbt
qualifiers:
  - Assessed end to end on duckdb_local only; the other listed targets rely on dbt support and are unassessed.
  - A compatible type correction or one compatible rename belongs to an existing Feature, not to this Recipe.
  - Consumers are the bounded set the owner names; deployment and retirement belong to the existing harness.
related:
  - dbt-refactor-output-identical
  - incremental-dbt-model-with-contract
  - prove-dbt-change-safe
evidence:
  features:
    - generating-dbt-model
    - evaluating-dbt-project
    - running-dbt-in-sandbox
    - verifying
  evals: []
---

## Prompt

Introduce <breaking_change> to <published_relation> as a new version built beside the unchanged old version, so each named consumer can move on its own schedule. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Deliver the new version, a change record of what changed in grain, meaning and shape and what each named consumer must do, revised queries for the named consumers with the results to expect, and the observable criteria for retiring the old version. Deployment, migration of the consumers' own systems and retirement of the old version are outside this work.

## Verified by

- The old version still exists with its approved name, schema and rows unchanged from a baseline taken from the unchanged code, at the approved precision and in each approved execution environment; nothing was rebuilt into the new shape.
- The new version is built beside it and both are readable together after a build; neither overwrites the other on a rebuild or refresh, and a reference that names no version still resolves to the old one.
- The new version meets its approved contract: key unique at its approved grain, columns with the approved names and meanings, and values equal to those derived independently from the sources and the approved rules.
- Where the old version is derivable from the new one, the two reconcile at the old grain within the approved history and population; each one-sided key or differing measure is listed with its amount and approved reason.
- Records the new contract cannot place are handled as approved: kept under an approved member, set aside and counted with their reason, or the build fails naming them; any approved tie to the old version holds once set-aside amounts are added back, and none is silently dropped, nulled or zeroed.
- For each change a reader could misread without an error, a reader keeping the old grain or meaning on the new version gets a wrong result stated in advance, the revised query gets the right one, and the case fails if the new version reverts; a change that errors instead is stated as such.
- Each named consumer's revised query returns the independently approved expected result on the approved data; where it differs from the old result by design, the difference is stated.
- The change record gives, for each changed grain, column and shape, its old and new meaning, and what each named consumer must do; every figure in it matches the built relations.
- Grants, masking, refresh and history the new version needs are stated as cutover requirements, never as passed checks, and the new version is no more widely readable than approved.
- Retirement is stated as observable criteria with the current state of each, or that it cannot be observed from here and who can; nothing is retired by this work and the old version stays populated.
- Consumers outside the named set are listed as not examined with the reason; no statement says no other consumer exists.
- A defect found in the old version is reported as follow-up, not applied; anything the checks cannot prove is stated.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Confirm the change is breaking: if the old interface can be kept, stop and say so. Find the readers the owner names and the other readers the repository shows, such as downstream models, exposures, semantic-layer and dashboard definitions, grants, orchestration selections, tests and copies, including any that join the old version to other relations at the old key, and decide with the owner which are named, which stay unexamined and why. Fix the new version's contract and its relation to the old one before building it, and write the expected results for the named consumers by hand from the approved dataset before the new version runs over it. Capture a baseline of the old version from the unchanged code. Build the new version beside the old through one shared rule, so a test dataset never runs through a second copy of it, and keep any test relation out of every schema, selection and grant the published relations reach. Compare both versions as approved, revise each named consumer's query, show the wrong result an old-grain reader gets, write the change record, including the cutover requirements for access, refresh and history and the retirement criteria with their current state, and state what the checks cannot prove.

### Compose

- generating-dbt-model
- evaluating-dbt-project
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which relation changes, in what way (grain, column meaning, shape), and is the change truly breaking, or can a compatible change or an existing Feature cover it?
- If unresolved, how do the two versions coexist: what names, schemas or mechanism, and does a column whose meaning changes keep its name or take a new one?
- If unresolved, what does the new contract hold: population, history (from when it is populated, whether it is backfilled, what happens to periods only the old version holds), key, handling of a missing or unplaceable value in the new key, and which measures must tie to the old version?
- If unresolved, what counts as the old version staying identical (precision, execution environments, time zones, run modes), and is any change to its output wanted? If so, that is a separate change.
- If unresolved, which consumers are named and revised, who owns each, and how are other readers found and dispositioned (cleared, to be moved, unexamined)?
- If unresolved, what dataset and independent expected results prove each named consumer, and may a labelled synthetic dataset stand in for real data?
- If unresolved, what must the new version carry that the old one has: which roles may read it, which masking or row filters apply, how often it refreshes, and who applies these through the harness?
- If unresolved, what are the retirement criteria: who must clear which reader, how reads of the old version are observed, and how long the observation window is?

### Guardrails

- Do not change the old version's logic, schema or output, refresh it into the new shape, rename it or alias over it; an approved superseded or deprecation note is allowed, and it stays until the approved retirement criteria are met.
- Do not publish a changed meaning under the old name unless the approved contract says so and the change record names it.
- Do not tell a consumer outside the named set that it is safe, or claim no other consumer exists; unexamined stays unknown.
- Do not retire, drop or restrict the old version, or change deployments, grants or orchestration; the harness owns them.
- Do not copy expected results from the new version's output, and do not run test data through a separate copy of the new version's rule.
- Do not let synthetic or test relations land in a schema, selection or grant that published relations reach.
- Do not fix a defect found in the old version or change output beyond the approved change; report it as follow-up with the output it affects.
