---
id: profile-api-source-from-docs
title: Read a new API's docs, add it as a source and profile a sample before you build on it
trigger:
  - A new API source is being considered and the team has to understand it before building a pipeline on it.
  - The API's documentation is current in Context7 but nobody has seen real data from the source yet.
  - A build is blocked because nobody knows the API's grain, field behaviour or data quirks.
description: Read an API's current documentation through Context7 or the approved documentation, add it as a source, land a bounded sample and profile it, so the team knows what the source offers, how it behaves and what to watch before any build. Stops before loading, modelling or scheduling.
pitch: Read a new API's docs, sample it and profile the sample before you build on it.
job_category: explain
area: ingestion
readiness: supported
function:
  - cross-functional
domain_objects:
  - api_source
  - source_connection
  - dlt_pipeline
  - sample_table
  - source_profile
works_with:
  platforms:
    - duckdb_local
    - motherduck
    - fabric_lakehouse
    - fabric_warehouse
    - redshift
    - databricks
  tools:
    - dlt
qualifiers:
  - Needs the API's documentation in Context7 or supplied by the user; unreadable docs stop the run.
  - Stops at a profiled sample; loading, cursors and schema contracts belong to the API ingestion Recipe.
  - An API with no mounted connector is declared by hand; add-or-update-source cannot configure it.
  - A sample shows only its own slice; behaviour outside it stays unproven.
  - Assessed end to end on duckdb_local only; the other listed targets rely on dlt support and are unassessed.
related:
  - api-to-bronze-incremental-contract
evidence:
  features:
    - capturing-requirements
    - configuring-dlt-destination
    - generating-dlt-pipeline
    - verifying
  evals: []
---

## Prompt

Read the current documentation for <api_name> through Context7, or the approved documentation where Context7 lacks it, add it as a source in the current Intent, pull a sample of <resource_list> within the approved scope, and profile the landed sample so the team knows what the source offers and what to watch before building on it. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Keep the API's own values, time labels and units unless approval says otherwise, record every place a live response differs from the documentation, and report what the sample cannot show. Build nothing beyond the sample and its profile.

## Verified by

- The documentation is read from Context7, or from the approved alternative where Context7 lacks it, and the result states what the API offers, what a request needs and which of these a live response confirmed rather than the documentation alone, including any paging and rate limits the run met.
- The source is a named connection whose files and outputs hold no secret value, and any credential it needs is referenced by name from the approved store.
- The sample covers exactly the approved scope: landed rows reconcile element for element to the response the load received, and records the API shows beyond it are counted with their reason, or the result says it cannot see them.
- Each landed row carries the approved key; keys are checked at the approved grain, any missing or duplicate key is counted and reported in the profile, never dropped or merged silently, and re-running the load follows the approved re-run rule.
- Landed time labels, time zone, units and value representations are as approved, and without an approved conversion each value equals the source's own value in the response the load received.
- The profile reports row count, null count, distinct count and range or common values per landed column, and these equal values computed independently from the sample.
- The profile names constant columns, categorical codes held as numbers and any summary value that misleads, so no code or constant is read as a measure.
- Every difference between the documentation and a live response, such as the place or time answered versus requested, units, or how recent values behave, is listed with evidence and none is resolved silently.
- The result states what the sample cannot show, such as other windows, entities or volumes and how recent values settle, and claims no understanding beyond the sample.
- A failed request or unusable response stops the run or is recorded, as the approved rule says, with its reason; documentation no approved source supplies stops the run; no partial sample is presented as the complete profile.
- The result states whether the sample is adequate to build on under the approved adequacy rule, naming the fields that are not, with the evidence.
- Nothing beyond the sample and its profile is built or changed: no transformation, contract, schedule or existing table.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements. Read the documentation first and note what each claim relies on, then add the source through the connector route the runtime offers, declaring the connection by hand where no connector can be configured, and never handling a secret value. Request only the approved scope, land it as approved, and compare the landed rows to the response the load received, kept as evidence, before profiling; a later read can confirm only values that the approved data version treats as settled. Profile every landed column, check each documentation claim against the live response, and record every difference, constant column, coded value and misleading summary. Finish with what the sample cannot show and an adequacy verdict with its evidence.

### Compose

- capturing-requirements
- add-or-update-source
- configuring-dlt-destination
- generating-dlt-pipeline
- profiling-source-data
- verifying

### Ask first

- If unresolved, which resources, entities, places or filters of the API are in scope, and which request parameters they use?
- If unresolved, which version of the data the sample takes when the API serves settled and current or forecast values, and which it must exclude?
- If unresolved, how large the sample is, which window or slice it covers, how that slice is chosen, and within what request or cost budget?
- If unresolved, which fields are landed, at what row grain and under what key?
- If unresolved, how time labels, time zone, units and value representations are stored: as the API returns them or converted?
- If unresolved, where the sample lands and what a re-run does to an existing sample: replace, merge or refuse?
- If unresolved, which documentation to use where Context7 does not hold the API's?
- If unresolved, what makes a sample adequate to build on, and whether a failure or a difference from the documentation stops the run or is only recorded?

### Guardrails

- Do not choose or apply any Ask first answer without approval, such as scope, data version, sample slice, budget, key, time zone, units, re-run, documentation source, failure or adequacy rule.
- Do not put a secret value in any file, config or output, or ask for one in chat.
- Do not present documentation as confirmed behaviour, or a live response as documented behaviour, without evidence.
- Do not read a categorical code or a constant column as a measure.
- Do not extend the sample into a load, transformation, contract or schedule, or change an existing table.
- Do not claim the sample shows behaviour outside the slice it covers.
- Do not exceed the approved request or cost budget, including on retries.
