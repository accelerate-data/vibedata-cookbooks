---
id: banking-aml-features
title: Build AML monitoring features at account-day grain
trigger:
  - A transaction-monitoring model is fed hand-built features nobody can reproduce, so two runs on the same data disagree.
  - A backtest looks better than live performance because a feature quietly used a transaction recorded after the day being scored.
  - Analysts and model builders each count cash near the reporting threshold, pass-through and velocity differently, and cannot say which transactions were left out.
description: Publish one row per account and day with approved monitoring features computed under an approved time basis so no later transaction changes a published row, every transaction counted, set aside with its reason or listed as not counted, uncomputable features shown as unknown with a reason, and reference data read as now recorded stated as able to restate rows.
pitch: One reproducible feature row per account and day under a stated time basis, with every transaction counted or explained.
job_category: build
area: transformation
readiness: supported
industry:
  - banking
domain_objects:
  - account
  - transaction
  - exchange_rate
  - jurisdiction_risk_list
  - account_day_feature
  - set_aside_transaction
  - coverage_check
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
  - Accounts and transactions must already be landed as tables with the dates the approved time basis needs.
  - Features derive from transactions only; balance-based features need an as-known balance source and are out of scope.
  - Publishes features only; alerts, cases, SAR filing, sanctions screening and risk rating are separate.
  - Account grain only; customer or network roll-ups need entity resolution first.
  - Where a risk-list feature is approved, the list is needed with its effective dates.
  - Reader restriction needs platform roles; DuckDB and MotherDuck have none, so access there is reported unproven.
related:
  - customer-retention-churn-features
  - identity-golden-record-crosswalk
  - pii-classification-and-masking
  - effective-dated-business-rules
  - file-drop-to-bronze
evidence:
  features:
    - capturing-requirements
    - generating-dbt-model
    - verifying
  evals: []
---

## Prompt

Build <account_day_feature_model>, <transaction_accounting_model> and <coverage_model> from <account_source>, <transaction_source>, <exchange_rate_source> and any <jurisdiction_list_source>. Inherit the Intent's sources, platform and approved requirements, and settle with the user only the monitoring semantics they leave open. Publish one row per approved account and day with the approved features, computed under the approved time basis so that no later transaction record changes a published row and reference data read as now recorded is stated as able to restate it, in the approved reporting currency, with a day the source does not cover shown as unknown and never zero, a feature that cannot be computed shown as unknown with its reason, every transaction counted, set aside with its reason or listed as not counted with its state, and what the inputs cannot prove stated.

## Verified by

- Every transaction record is counted (flagged where approved), shown as an internal transfer, listed as not counted with its type or state, or set aside with its reason as approved; the classes sum to the input by count and by source amount per currency, and a failed run names the offending items.
- The published accounts and days equal an independently derived set under the approved population and row rule, an excluded class has no row and its records are listed, and a day that gets a row and has no activity reads zero while a day the source does not cover reads unknown with its reason.
- Deleting or changing every transaction known after a day, under the approved time basis, leaves that day's row unchanged, as does a later rate, list or account change where those are read as known; a late record counts only as the approved rule places it; two builds on one input and as-of match.
- Only counted items, and internal transfers in the features the approved rule names, move any feature; items not counted are listed with their type or state as approved; a reversal, return or approved correction nets as approved on the day it became known without changing any earlier row.
- Every converted amount equals an independent conversion at the approved rate rule, no total contains an unconverted amount, and a transaction with no usable rate is handled as approved with that reason.
- Each approved feature equals a value derived independently from the inputs and approved rule values, such as channel flows, cash near the approved threshold with its edges, round-amount share, counterparties, risk-list share, pass-through and velocity against the account's own baseline.
- An internal transfer between accounts the approved rule treats as one holder enters only the features the approved rule names, is shown separately from external flows, and never reads as an external counterparty.
- Where an approved pass-through rule pairs amounts, no amount is matched twice and each match names the inflow it used; under any rule an outflow is judged only against inflows counted by its own day.
- Where velocity or a share cannot be computed because history is short, the baseline is empty or nothing was counted, it reads a named unknown with its reason, never zero and never a division by zero.
- A transaction is judged against the list version the approved rule selects; a version effective later changes no earlier day, and where versions are read as known, a version recorded later changes no earlier day.
- Changing an approved rule held as data, such as the threshold, band, windows or list, changes the dependent features from its approved effective day, or on every day where restating is approved, without a code change within the approved rule form; the as-of is a stated input, never the run clock.
- Where the platform enforces access and applying it is approved, querying as each role shows account-level rows only to the approved readers; otherwise, where publishing is approved, access is reported unproven. The outcome states what the inputs cannot prove, such as when a record became known.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements; ask only about monitoring semantics they leave open. Sample data, vendor defaults, regulatory examples and existing code are evidence, never policy. Profile the accounts first (classes, open and close dates, holders, lifecycle changes), then the transactions (feeds and the range each covers, states, reversals, duplicates and amended deliveries, malformed fields, which date shows when a record became known, time zones), then the rates and the reference list. Keep every rule value, window, threshold, band, vocabulary, reason precedence, list version, coverage window and as-of date as editable data. Derive each case's expected result independently of the models, from the inputs and the rule data, before comparing: a day-boundary or threshold edge, a later reversal, a late record, a pending item that posts later, a duplicate or amended delivery, an account opened, closed or reclassified mid-period, a new account, a dormant day, an uncovered day, a missing rate, an own-account transfer, a list change and an excluded account. Make every window and baseline read only what the approved time basis lets the day see. Refuse inconsistent coverage and as-of settings, and publish a partly covered day only as the approved rule allows. State what the inputs cannot prove, including reference data read as now recorded rather than as known.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which accounts get rows (customer, ledger, suspense, test, frozen, closed, joint, omnibus or virtual sub-accounts), what is the account key, how is an account that changes class or id or reopens handled, which days get a row, and how are excluded accounts and their records shown?
- If unresolved, which date is a record's activity date (business, posting or value), which field shows when it became known and what stands in where none does, what time zone, day boundary and as-of apply, and does a late record count on the day it became known, get set aside or get flagged?
- If unresolved, which transaction types (fees, interest, adjustments) and states count, how reversals, returns and chargebacks net on the day each is known, what makes records duplicates and which delivery counts, and is a later change to a counted record a duplicate, counted when known or set aside?
- If unresolved, which amount is converted (original or booked account-currency amount), which reporting currency, rate source, rate date, carry-forward window, method order and rounding apply, and is a transaction with no usable rate set aside, counted with its amounts unknown, or the run failed?
- If unresolved, which source codes map to which channel and what counts as cash, who is the same holder, which features an internal transfer enters, how counterparty identity is taken (account, name, token), and how a missing counterparty, channel or jurisdiction is handled?
- If unresolved, which features are published; is the near-threshold band judged per item or on a day total, in which directions, currency and jurisdictions; and which round unit and currency, windows, minimum history, baseline basis and pass-through rule (exact, tolerance, proportional, ratio) apply?
- If unresolved, which high-risk list applies, which jurisdiction a transaction carries, which date picks a list version, are list versions, rates and account attributes read as known on each day or as now recorded, and does a changed rule value restate earlier days or apply from its effective date?
- If unresolved, how are unknown accounts, malformed fields and records outside open dates or after the as-of handled (which reasons and precedence, flagged or run failed), what does a partly covered day read, who may read account-level rows, and may they be published where roles cannot restrict them?

### Guardrails

- Do not choose the population, time basis, counted states, reversal rule, currency rule, thresholds, windows, matching rule, list or disposition for the user, and take none from sample data, a vendor default, a regulation example or common practice.
- Never let a feature, window or baseline read a record the approved time basis does not let that day see, and never rewrite a published row when a later record arrives.
- Never treat unknown as zero: a day the source does not cover, a missing rate, a short history or an empty baseline stays unknown with its reason.
- Never drop or double count a transaction; every record is counted once, shown as an internal transfer, listed as not counted or set aside with its reason, and records no rule can place are listed, not repaired.
- Never sum amounts across currencies without the approved conversion, and never let a failed conversion contribute a raw amount.
- Never judge a transaction against a reference list version approved for a different date.
- Never claim account-level rows are limited to the approved readers unless querying as each role shows it, never grant wider access than approved, and never put real customer data in a fixture, a PR or a Recipe.
- Stop at the feature table and its accounting: do not raise alerts, run scenarios, open cases, file reports, screen against sanctions, rate customer risk, merge customers, apply access controls beyond what is approved, or train, score or serve a model.
