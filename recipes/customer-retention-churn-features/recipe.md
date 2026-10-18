---
id: customer-retention-churn-features
title: Build retention cohorts and a churn feature table
trigger:
  - Marketing, finance and product each quote a different churn rate because each defines an active and a lost customer differently.
  - Nobody can say whether newer customer cohorts keep their customers better or worse than older ones.
  - A data science team wants a customer-by-period table of features and a churn label, but has no agreed definition and no way to show the features cannot see the future.
description: Place each customer in one cohort, publish a retention table by cohort and elapsed period, and a customer-by-period feature table with a forward churn label under approved definitions, with every record counted or set aside and labels the data cannot yet settle marked unobservable.
pitch: One agreed definition of active and lost, a cohort retention table, and features with a churn label that only looks forward.
job_category: build
area: transformation
readiness: supported
domain_objects:
  - customer
  - signup_cohort
  - activity_event
  - churn_event
  - retention_cell
  - customer_period_feature
  - churn_label
  - retention_exception
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
  - Customer and activity records must already be landed as tables; this Recipe does not ingest them.
  - Assessed end to end on duckdb_local only; the other listed targets rely on dbt support and are unassessed.
  - Counts customers, not revenue; revenue retention and lifetime value are separate outcomes.
  - Features use event time under an approved as-of date; facts known only later or later corrected are not separated.
  - Churn inferred from silence cannot tell a lost customer from one who has not returned yet.
  - Stops at cohorts, retention, features and the label; training, scoring and serving are separate outcomes.
related:
  - people-attrition-tenure
  - identity-golden-record-crosswalk
  - metric-population-and-rollups
  - file-drop-to-bronze
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

Build <customer_period_status_model>, <cohort_assignment_model>, <retention_table_model>, <feature_table_model> and <accounting_model> from <customer_source>, <activity_source> and any <support_source> or <plan_change_source>. Inherit the Intent's sources, platform and approved requirements, and settle with the user only the churn semantics they leave open. Place each customer in one cohort, mark each customer-period active or lost under the approved activity and churn rules, publish a retention table by cohort and elapsed period with periods a cohort has not reached left empty with a reason and never zero, publish one row per approved customer-period with look-back features from events on or before its end and a churn label that looks only at the approved horizon after it, saying not yet observable where that window is incomplete, account for every customer and event as counted or set aside with its reason, and report what the inputs cannot prove.

## Verified by

- Every customer record and event row is counted or set aside with its reason, counted plus set aside equals the input per source, a row failing several checks shows each reason, and a failed or held run names the offending items.
- Each customer in scope sits in exactly one cohort under the approved anchor and period, one with no usable anchor is handled as approved and listed with its reason, and cohort sizes plus those left out equal the customers in scope.
- Which events count as activity, the churn definition and the date a churn is recognised follow the approved rules, an event that does not count stays visible with its reason, and each churn date equals one recomputed independently from the inputs and rules.
- A customer's status and features in a period use only events dated on or before its end, so changing or deleting any later event leaves that row unchanged.
- Where churn needs a silent window, a customer whose window is not complete at the as-of date reads not churned yet, never lost.
- A retention cell is the retained customers over the cohort size under the approved retained rule, cells past the as-of are empty with a reason and never zero, and any return the approved rule allows is shown as a return.
- A blended figure for an elapsed period is the sum of retained over the sum of sizes for the cohorts that reached it, never an average of shares, and a recorded churn date is not rewritten by a later return.
- The feature table has one row per approved customer-period, none before the anchor or after the as-of, and each feature equals a value recomputed independently from the inputs under the approved features and windows.
- A feature whose source or window the data does not fully cover reads unknown with its reason, never zero and never a partial count.
- The label looks only at events after the period end within the approved horizon, reads lost, stayed, not yet observable or the approved state for an already lost customer, and reads stayed only when the whole window is at or before the as-of.
- Changing an approved rule held as data, such as the silent window, a feature window, the horizon or the calendar, changes the dependent results without a code change within the approved rule form, and the as-of is a stated input, never the run clock.
- Customer-level rows are readable only by the approved readers, a group below the approved minimum is hidden as approved with sums holding before hiding, and the outcome states what the inputs cannot prove, such as when a fact became known.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements; ask only about churn semantics they leave open. Sample data, vendor defaults and existing code are evidence, never policy. Profile the customers first (anchor dates, duplicates, internal or test accounts, merged records), then the activity (event types and statuses, duplicates, out-of-order arrival, time zones, and the date each source begins to cover), then any subscription, plan or support data, and decide with the user whether churn is recorded or inferred from silence. Keep the activity rules, windows, horizon, calendar and as-of date as editable data. Derive each case's expected result independently of the models, from the inputs and the rule tables, before comparing: an event exactly on a window boundary, a return, a customer with no activity, one anchored near the as-of, a cohort of one, a window that starts before a source's coverage, and a duplicate or late event. Keep every setting that bounds the published periods (as-of date, calendar) consistent with the others, and refuse an inconsistent set rather than publish a partial period. State what the inputs cannot prove.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which customers are in scope (internal, test, trial, free, merged or duplicate customers, several accounts under one customer), what is the customer key, and how are customers left out shown?
- If unresolved, what anchors a cohort (signup, first purchase, first activity, subscription start), which period grain, calendar, time zone and as-of date apply, and what happens to a customer with no usable anchor?
- If unresolved, which events keep a customer active, is churn a silent window (how long, from which day, boundary inclusive), an explicit end or either, is there a grace delay before a loss is recognised, which date is it dated on, and when is a customer with no activity lost?
- If unresolved, what happens when a lost customer returns (stays lost, returns to the original cohort, starts a new entry), what counts as retained in a cell, and how are cohorts blended?
- If unresolved, which periods get a feature row (every period from the anchor or only those at risk), how far forward does the label look, and how is a customer already lost at a period end labelled?
- If unresolved, which features and trailing windows are published, such as recency, frequency, tenure, support contacts and plan changes, and what does a window a source does not cover show?
- If unresolved, how are an unknown customer, a duplicate event, an event before the anchor or after the as-of, a late arrival and an unplaceable record handled: counted, set aside with a reason, flagged or the run failed, and what publishes then?
- If unresolved, who may read customer-level rows, what minimum cohort size is published and for which outputs, and is complementary hiding required?

### Guardrails

- Do not choose the active events, churn definition, grace, anchor, calendar, return rule, retained rule, horizon, features, row rule, exception handling or disclosure for the user, and take none from sample data, a vendor default or common practice.
- Never let a feature or a status read an event dated after its period end, and never let the label use anything past its approved horizon or the as-of.
- Never settle a label as stayed, or a cohort cell as zero, for a window or period the data has not reached; mark it not yet observable or empty with its reason.
- Never rewrite a recorded churn date when the customer returns, and never place a returning customer in a second cohort unless the approved rule starts a new entry.
- Never average cohort shares or sum retention across periods; a blended figure is a sum over a sum.
- Never treat unknown as zero: a source or window the data does not cover, or an absent event the approved rules define no value for, stays unknown with its reason.
- Never drop or double count a customer or event; every row is counted once or set aside with its reason, and rows no rule can place are listed, not repaired.
- Never publish customer-level rows beyond the approved readers or a group below the approved minimum, and never let a hidden group be worked back from published totals where the approved policy forbids it.
- Stop at cohorts, retention, the feature table and the label: do not train or score a model, serve a feature store, segment or value customers, measure revenue retention, merge customers or write flags back to source systems.
