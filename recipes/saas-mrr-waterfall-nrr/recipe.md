---
id: saas-mrr-waterfall-nrr
title: Build the MRR waterfall and net revenue retention
trigger:
  - Finance, RevOps and the board each quote a different net revenue retention because each turns subscriptions into monthly recurring revenue its own way.
  - A monthly revenue bridge never foots, or shows a plan switch as a lost customer beside a new one.
  - Nobody can say how much of a month's change came from new customers, upgrades, downgrades, losses and returns.
description: Turn subscription records into monthly recurring revenue per customer under approved rules, a monthly waterfall of new, expansion, contraction, churn and reactivation that foots, and net and gross revenue retention, with every record counted or set aside.
pitch: One agreed definition of monthly recurring revenue, a waterfall that foots, and retention figures the board can trace.
job_category: build
area: transformation
readiness: supported
function:
  - finance
  - revops
industry:
  - saas
domain_objects:
  - customer
  - subscription_record
  - monthly_recurring_revenue
  - revenue_movement
  - mrr_waterfall
  - revenue_retention
  - subscription_exception
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
  - Subscription records must already be landed as tables; this Recipe does not ingest them.
  - Keeps each currency separate; conversion is a separate outcome.
  - Counts recurring subscription revenue only; usage, one-off and recognised revenue are separate outcomes.
  - Needs dated, priced subscription terms; past results after backdated changes need kept history.
  - Stops at MRR, waterfall and retention; forecasting, customer-count churn and billing ties are separate outcomes.
  - Restricting customer-level rows needs roles and grants; without them the restriction is a label only.
related:
  - customer-retention-churn-features
  - finance-revenue-recognition
  - customer-historical-ltv
  - revops-bookings-billings-cash
  - shared-fx-conversion
  - shared-calendar-fiscal-periods
  - effective-dated-business-rules
  - database-tables-to-bronze
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

Build <customer_month_model>, <waterfall_model>, <retention_model>, <exceptions_model> and <accounting_model> from <subscription_source> and any <plan_source>, <term_source> or <currency_source>. Inherit the Intent's sources, platform and approved requirements, and settle with the user only the revenue semantics they leave open. Turn each in-scope subscription record into its monthly equivalent under the approved rules, publish recurring revenue per customer, currency and approved month with its movement from the approved classes, publish a waterfall per currency and month whose opening plus movements equals its closing, publish net and gross revenue retention over the approved base with no ratio where the base is empty, leave months the data has not reached absent or unknown rather than zero, account for every subscription record as counted or set aside with its reason, and report what the inputs cannot prove.

## Verified by

- Every subscription record is counted or set aside with its reason as the approved rule shows, counted plus set aside equals the input, the outcome states how many were left out and why, and a failed or held run names the offending records.
- Each counted record contributes its monthly equivalent under the approved interval, quantity, discount and rounding rules; charges the approved rules leave out contribute nothing and stay visible with their reason.
- Each customer-month figure equals the sum of the customer's in-force subscriptions under the approved measurement basis, per currency, before any approved suppression, and equals a recomputation from the source records and approved rules done independently of the models.
- Each movement is of one approved class at the approved level, and where movements are decided per customer a customer-month has at most one; a plan switch or seat move is then never a loss beside a new customer, and a return reads as approved.
- Each currency-month waterfall shows opening, each approved movement with its count, and closing; before any approved suppression, opening plus movements equals closing, closing equals the sum of the customer figures, and movements equal those behind them.
- Retention for a month uses only the approved base, equals values derived independently by hand from the approved rules, leaves out customers outside the base, and shows no ratio, never 0 or 100%, where the base is empty.
- Months after the approved as-of date, or outside a source's covered range, are absent or marked unknown with a reason, never zero, and moving the as-of changes only which months appear.
- Amounts in different currencies are never added or blended in any figure, movement or ratio, and a customer billed in two currencies appears once per currency.
- Duplicate, superseded and conflicting records follow the approved rule, a pair the rule cannot resolve is named, and a customer is never shown as lost for a record that was only superseded.
- Customer-level rows reach only the approved readers, or the outcome states that restriction is not enforced.
- A result that needs history the inputs do not keep, such as a past as-of after a backdated change, is labelled as known today, not presented as it stood then.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile the subscription records (customer key, plan, interval, price, quantity, currency, start and end dates, status, load or version date), the line types, and the covered date range, and check that each record has a customer and a usable term. Use Ask first only for semantics still open, and record each decision as the user's own answer. Keep line-type rules, interval lengths, the retention window, the as-of date and the movement and reason vocabularies as editable data, not literals. Derive each case's expected result independently of the models, from the records and the rule tables, before comparing: an annual and a quarterly plan, a mid-month start or end, a plan switch, a seat move between two subscriptions, a churn, a return after a gap, a customer in two currencies, a duplicate or superseded record, a zero or negative price and a record outside the reported months. Keep every setting that bounds the published months consistent with the others, and refuse an inconsistent set rather than publish a partial month. State what the inputs cannot prove.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which customers and billing entities are in scope (internal, test, trial, free, merged), what is the customer key, which line types count as recurring (one-off, usage, setup, paused, negative), how recurring discounts and credit memos enter, and how left-out records are shown?
- If unresolved, how a billing interval becomes a monthly amount, how quantity, rounding and a term the rules do not cover are treated, and which term applies when several are dated?
- If unresolved, is the figure a month-end rate, any-day overlap or day-prorated, which months (calendar or fiscal) and as-of date apply, and does a dormant month between a loss and a return get a row, a zero or nothing?
- If unresolved, from which date to which date is each source complete, where does opening revenue for customers older than the sources come from, and what does a month outside that range show?
- If unresolved, at what level are movements decided (customer or subscription), how are plan switches, seat moves, price changes, a start or end inside one month and a fall to zero classed, and when is a returning customer a reactivation rather than new (does a gap length matter)?
- If unresolved, how are net and gross retention defined (window length or month over month, the base, gross capped at the starting amount, a customer who left and returned inside the window), and what shows where no base exists?
- If unresolved, how are a repeated record id, a later version, a conflicting pair, a late or backdated change and an unplaceable record handled (counted, set aside with one reason or every reason, flagged or the run failed), and does a restated month show its prior figure?
- If unresolved, who may read customer-level rows, what minimum group size is published and for which outputs, and is complementary hiding required?

### Guardrails

- Do not choose the recurring line types, discount treatment, interval conversion, rounding, measurement basis, movement classes, reactivation rule, retention definition, window, duplicate rule or disclosure for the user, and take none from sample data, a vendor default or common practice.
- Never decide movements at a level or in classes other than the approved ones; where they are decided per customer, never show a plan switch or seat move as a loss beside a new customer, and never show a returning customer as new unless the approved rule says so.
- Never include in recurring revenue a charge the approved rules leave out, and never sum, blend or convert currencies; conversion is a separate outcome.
- Never publish a month the data has not reached or a source does not cover as zero, and never publish a ratio over an empty base as 0 or 100%.
- Never publish customer-level rows beyond the approved readers or a group below the approved minimum, and never let a hidden group be worked back from published totals where the approved policy forbids it.
- Never drop or double count a record; every record that cannot be placed stays visible with its reason, and a conflict the approved rule cannot resolve is named, not guessed.
- Never let a waterfall disagree with the customer figures behind it, or restate a published month silently when a later or backdated change arrives.
- Stop at recurring revenue, the waterfall and retention: do not forecast, recognise revenue, value or predict churn of customers, tie to billing or cash, or write back to the source systems.
