---
id: point-in-time-training-dataset
title: Build a training dataset that uses only information available at prediction time
trigger:
  - A model scores well in training but worse in production because training rows used facts, corrections or labels a real prediction could not have seen.
  - Historical facts are joined by when they happened, not by when they became known, so a late-arriving fact or correction rewrites earlier rows.
  - A data science team wants one row per entity and prediction time with a forward label, and no proof that each feature used only what was known by then.
description: Build one batch table with one row per approved entity and prediction time, features from only the fact versions known by then, a forward label whose unfinished windows are marked or excluded as approved, and every entity-time and fact version accounted for.
pitch: Training rows whose features see only what was known at prediction time, and a check that fails when a join looks ahead.
job_category: build
area: transformation
readiness: supported
domain_objects:
  - prediction_point
  - fact_version
  - availability_record
  - point_in_time_feature
  - outcome_label
  - training_row
  - training_exception
  - fact_accounting_entry
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
  - Entities, facts and outcomes must already be landed as tables; this Recipe does not ingest them.
  - Each fact needs an availability time; absent history is an input gap, never rebuilt from event time.
  - Features and the label follow approved definitions; this Recipe assembles them by availability and defines none.
  - One batch dataset for one prediction target; streaming and online serving are separate outcomes.
  - Stops at the dataset, its exceptions and accounting; training, scoring and a feature store are separate outcomes.
related:
  - customer-retention-churn-features
  - dbt-snapshot-history
  - effective-dated-business-rules
  - identity-golden-record-crosswalk
evidence:
  features:
    - capturing-requirements
    - profiling-source-data
    - applying-medallion-data-modelling
    - generating-dbt-model
    - dbt-unit-testing
    - running-dbt-in-sandbox
    - verifying
  evals: []
---

## Prompt

Build <training_dataset_model>, <exception_model>, <fact_accounting_model> and <coverage_model> from <entity_source>, <fact_source> and <outcome_source>. Inherit the Intent's sources, platform and approved requirements, and settle with the user only the temporal rules they leave open. Publish one row per approved entity and prediction time whose features read only fact versions available by that time under the approved boundary, and whose label looks only at the approved window after it on the approved outcome date, with a window unfinished at the cutoff under the approved maturity rule marked not yet observable or excluded and listed as approved, never labelled negative. List every entity-time without a row with one reason, account for every fact version as read, set aside or counted with its reason as approved, keep the version and availability behind each feature, prove a join that looks ahead fails a check, and report what the inputs cannot prove.

## Verified by

- Every entity and prediction time in the approved population, with eligibility judged on what was known by that time, is a training row or a listed exception with one reason; rows plus exceptions equal the population at each time, none in both.
- Entities the approved scope leaves out are shown or counted with their reason as approved, and the outcome states how many were excluded and why.
- Every fact version delivered is read by at least one row or set aside with one reason (never available, available before it happened, superseded before any row read it, conflicting, belonging to an entity left out) or counted or flagged as approved; per-source counts equal the input.
- A row reads only versions available by its prediction time under the approved boundary; a fact that happened earlier but became available later is absent from earlier rows and, in an approved window, present at the approved version from its availability on.
- A correction changes only rows at or after its availability; changing or deleting any fact available after a row's prediction time leaves that row's features unchanged.
- Each feature equals a value derived independently from the visible versions under the approved windows, with window boundaries holding on both sides and an empty window reading as approved.
- The label reads outcomes only in the approved window after the prediction time, on the approved outcome date; boundary outcomes follow the approved rule, and a window unfinished under the approved maturity rule is marked or excluded and listed as approved, never negative.
- There is exactly one row per approved entity and prediction time under the approved entity link, and a duplicate or ambiguous key is reported with its offending items, never merged silently.
- Each row keeps or links the fact version and availability time behind each feature, so any value traces to the evidence that made it visible.
- Where the inputs hold a fact whose availability follows its event, a deliberately future-looking join (event time alone, or a later-available version) fails a check the approved join passes, naming the leaking fact; where none does, the check is stated unproven.
- Changing an approved rule held as data, such as a window, horizon, boundary or cutoff, changes dependent results without a code change within the approved rule form, and the cutoff is a stated input, never the run clock.
- Rerunning on unchanged inputs gives identical rows; published rows, labels, exceptions and accounting equal values derived independently from the inputs and approved rules, with what the inputs and platform cannot prove stated, including effective reader access.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements; ask only about temporal rules they leave open. Sample data, vendor defaults and existing code are evidence, never policy. Profile the entities first, then each fact source: which timestamp says when a fact became knowable, its grain and time zone, versions, corrections and merges, and how far back availability is recorded. Treat absent availability history as an input gap and say so. Keep windows, horizon, boundaries, calendar, maturity rule and cutoff as editable data. Write the expected rows by hand from the inputs and the approved rules before the models exist, never from the models, and compare both directions: a fact that happened before the prediction time but became available after it, a correction that arrives later, two versions with one availability time, a version available before its own event, an entity with nothing known, an outcome exactly on a window end or recorded after its window closed, an event exactly on the prediction time and a window still open at the cutoff. Prove the leak check by running a deliberately future-looking join and recording that it fails and the approved join passes. State what the inputs cannot prove.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which entities are in scope, how eligibility is judged from what was known at each prediction time (entities the source no longer lists, not yet eligible or already past their outcome), and what each gets: a row, a listed exception or an exclusion counted with its reason.
- If unresolved, the prediction times (calendar, frequency, time zone, first eligible time, cutoff) and the grain and time zone at which each source's availability stamp is compared with them.
- If unresolved, which timestamp says when each source's fact became known, whether the prediction-time boundary is inclusive, and what a fact with no availability time, one available before it happened or one dated after the cutoff gets: read if approved as known ahead, set aside, or fail.
- If unresolved, which version a row reads, what two versions with the same availability time do (pick one by a stated rule, set aside as conflicting or fail), and how a backfilled or late-loaded version is treated.
- If unresolved, which keys link each fact and outcome to an entity, how a merged, re-keyed or parent entity's facts reach rows (the merge has its own availability), and how a duplicate or unknown entity key is handled.
- If unresolved, which features and trailing windows are published, which date places a fact in a window (event or availability), which fact types count, how an empty window reads, and which attributes count as known at the prediction time, including values held without history.
- If unresolved, what the label measures, its outcome event, window start, length and boundary, the date outcomes are read on (also deciding an outcome is already past), when a window counts as finished given reporting delay, and how already-past and unfinished-window rows are labelled or listed.
- If unresolved, how a duplicate fact, a record outside the cutoff and an unplaceable record are handled and what publishes then, who may read entity-level rows, and whether version and availability evidence stays on the row or in a linked relation.

### Guardrails

- Do not choose the availability timestamp, boundary, version rule, windows, label definition, outcome date, cutoff, entity link, exception handling or disclosure for the user, and take none from sample data, a vendor default or common practice.
- Never let a feature read a fact version available after its prediction time, a fact dated after it unless the approved rule treats it as known ahead, or a correction later than the row, and never silently rebuild availability from event time.
- Never let a feature read a fact recorded because of the outcome, and never label a row whose window the data has not finished as negative; mark it not yet observable or list it as excluded as approved, never drop it silently.
- Never edit a fixture, rule or expected row to make a check pass, and never generate expected rows from the models under test.
- Never drop or double count an entity-time or fact version; every one is a row or a listed exception, or set aside or counted with its reason as approved.
- Never treat unknown as zero unless the approved rule says so, and never merge duplicate keys, conflicting versions or entities without the approved rule.
- Stop at the dataset, its exceptions, accounting and checks: follow approved feature and label definitions, and do not train or score a model, serve a feature store, or build a general two-axis history store.
