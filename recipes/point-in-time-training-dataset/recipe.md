---
id: point-in-time-training-dataset
title: Build a training dataset that uses only information available at prediction time
trigger:
  - A model scores well in training but worse in production because training rows used facts, corrections or labels a real prediction could not have seen.
  - Historical facts are joined by when they happened, not by when they became known, so a late-arriving fact or correction rewrites earlier rows.
  - A data science team wants one row per entity and prediction time with a forward label, and no proof that the features cannot see the future.
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
  - Features and the label follow definitions approved with the user; this Recipe does not choose what predicts.
  - One batch dataset for one prediction target; streaming and online serving are separate outcomes.
  - Stops at the dataset, its exceptions and accounting; training, scoring and a feature store are separate outcomes.
related:
  - customer-retention-churn-features
  - dbt-snapshot-history
  - effective-dated-business-rules
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

Build <training_dataset_model>, <exception_model>, <fact_accounting_model> and <coverage_model> from <entity_source>, <fact_source> and <outcome_source>. Inherit the Intent's sources, platform and approved requirements, and settle with the user only the temporal rules they leave open. Publish one row per approved entity and prediction time whose features read only fact versions available by that time under the approved boundary, and whose label looks only at the approved window after it, keeping rows whose window is unfinished at the cutoff, marked not yet observable or excluded and listed as approved, never labelled negative. List every entity-time without a row with one reason, account for every fact version as read or set aside with its reason, keep the version and availability behind each feature, prove a join that looks ahead fails a check, and report what the inputs cannot prove.

## Verified by

- Every entity and prediction time in the approved population is a training row or a listed exception with one reason; rows plus exceptions equal the population at each prediction time, and none sits in both.
- Every fact version delivered is read by a row or set aside with one reason, such as not yet available, available before it happened, superseded or conflicting; counts per source equal the input.
- A row reads only versions available by its prediction time under the approved boundary, and a fact that happened earlier but became available later is absent from that row and, where its event falls in an approved window, present at its own version in the first row at or after its availability.
- A correction changes only rows at or after its availability, never an earlier row, so changing or deleting any fact available after a row's time leaves that row unchanged.
- Each feature equals a value derived independently from the visible versions under the approved windows, with window boundaries holding on both sides and an empty window reading as approved.
- The label reads outcomes only inside the approved window after the prediction time, boundary outcomes follow the approved rule, and a row whose window is not finished at the cutoff is marked not yet observable or excluded and listed as approved, never negative.
- There is exactly one row per approved entity and prediction time, and a duplicate or ambiguous key is reported with its offending items, never merged silently.
- Each row keeps or links the fact version and availability time behind each feature, so any value traces to the evidence that made it visible.
- A deliberately future-looking join, matching on event time alone or reading a later-available version, fails a check the approved join passes, and the failure names the leaking fact.
- Changing an approved rule held as data, such as a window, horizon, boundary or cutoff, changes dependent results without a code change within the approved rule form, and the cutoff is a stated input, never the run clock.
- Rerunning on unchanged inputs gives identical rows, and published rows, labels, exceptions and accounting equal values derived independently from the inputs and approved rules, with what the inputs cannot prove stated.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements; ask only about temporal rules they leave open. Sample data, vendor defaults and existing code are evidence, never policy. Profile the entities first, then each fact source: which timestamp says when a fact became knowable, its grain, versions and corrections, and how far back availability is recorded. Treat absent availability history as an input gap and say so. Keep windows, horizon, boundaries, calendar and cutoff as editable data. Write the expected rows by hand from the inputs and the approved rules before the models exist, never from the models, and compare both directions: a fact that happened before the prediction time but became available after it, a correction that arrives later, two versions with one availability time, a version available before its own event, an entity with nothing known, an outcome exactly on a window end, an event exactly on the prediction time and a window still open at the cutoff. Prove the leak check by running a deliberately future-looking join and recording that it fails and the approved join passes. State what the inputs cannot prove.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which entities are in scope, what the prediction times are (calendar, time zone, first eligible time, cutoff), and what an entity not yet eligible or already past its outcome gets: a row, a listed exception or exclusion.
- If unresolved, which timestamp says when each source's fact became known, whether a boundary at the prediction time is inclusive, and what a fact with no availability time, one available before it happened or one dated after the cutoff is handled (set aside with its reason or the run failed).
- If unresolved, which version of a fact a row reads, what two versions with the same availability time do (pick one by a stated rule, set aside as conflicting or fail), and whether a correction may ever restate an earlier row.
- If unresolved, which features and trailing windows are published, which fact types count, how an empty window reads (zero or unknown), and which attributes are taken as known at the prediction time.
- If unresolved, what outcome event the label uses, the window start, length and boundary, which date the outcome is read on (event or availability), and how an outcome already past at the prediction time is labelled.
- If unresolved, whether a row whose window is unfinished at the cutoff is kept and marked or excluded and listed, and where an entity with nothing known at a prediction time is listed: a separate exception list, a row with a reason or both.
- If unresolved, how an unknown entity, a duplicate fact or key, a record outside the cutoff and an unplaceable record are handled: counted, set aside with a reason, flagged or the run failed, and what publishes then.
- If unresolved, who may read entity-level rows, and whether the source version and availability evidence behind each feature is kept on the row or in a linked relation.

### Guardrails

- Do not choose the availability timestamp, boundary, version rule, windows, label definition, cutoff, exception handling or disclosure for the user, and take none from sample data, a vendor default or common practice.
- Never let a feature read a fact version available after its prediction time, a fact dated after it, or a correction that arrives later than the row, and never rebuild availability from event time.
- Never label a row whose window the data has not finished as negative, and never drop it silently; mark it not yet observable or list it as excluded as approved.
- Never edit a fixture, rule or expected row to make a check pass, and never generate expected rows from the models under test.
- Never drop or double count an entity-time or fact version; every one is a row, or set aside with its reason.
- Never treat unknown as zero unless the approved rule says so, and never merge duplicate keys or conflicting versions without the approved rule.
- Stop at the dataset, its exceptions, accounting and checks: do not train or score a model, serve a feature store, define new features or labels, or build a general two-axis history store.
