---
id: shared-fx-conversion
title: Normalize multi-currency amounts to a reporting currency with as-of rates
trigger:
  - Finance adds amounts held in several currencies as if they were one, or restates old transactions at today's rate, and the total changes every time someone reruns it.
  - A report that must be in one currency cannot show which exchange rate converted each amount, from which date and which source.
  - A rate was corrected after the fact and nobody can say whether a past figure used the old rate or the corrected one.
description: Restate each transaction amount in one reporting currency at the rate the user's approved date basis and rate rules select, keep the original amount and the rate used on every row, set aside what cannot convert with one reason each, and tie converted and set-aside amounts back to what was received in each currency.
pitch: One repeatable reporting-currency figure where every amount shows its rate, date, source and method, and every amount that could not convert shows why.
job_category: build
area: transformation
readiness: supported
domain_objects:
  - transaction_amount
  - currency
  - exchange_rate
  - rate_version
  - currency_conversion
  - conversion_exception
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
  - Needs amounts with a currency code and a date, and rate quotes with a quote date, a source and a recorded time.
  - Takes the quotes as supplied; sourcing a rate feed and checking it against a provider are separate outcomes.
  - Converts to an approved reporting currency; translation, exchange gain or loss, hedging and consolidation are separate.
  - Reproducing a past run needs kept rate versions with their recorded time; without them the outcome says it cannot.
  - Keeps each original currency apart; netting across currencies, pricing and rate forecasting are separate outcomes.
  - Rates are inputs to conversion, not general dated business rules; effective-dated rules are a separate outcome.
related:
  - effective-dated-business-rules
  - customer-historical-ltv
  - finance-trial-balance-close
  - ops-procurement-spend
  - revops-quota-commission
evidence:
  features:
    - capturing-requirements
    - generating-dbt-model
    - verifying
  evals: []
---

## Prompt

Build <conversion_model>, <currency_addback_model> and <unused_rate_model> from <amounts_source>, <currency_list_source> and <rate_source> for the reporting-currency restatement in this Intent. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only the semantics they leave open. Give every amount one disposition, converted or set aside with exactly one reason. For each converted amount publish the original amount and currency as supplied, the rate used with its own date and source, the selection method, whether the rate was carried from an earlier date, and the amount in the reporting currency before and after rounding. Select the rate under the approved date basis, gap rule, quote forms and order, round once under the approved rule, and apply the approved rule that fixes which rate versions count. Publish, per original currency, an add-back of converted and set-aside amounts to what was received, and list the quotes the approved rules left unused with the reason for each. Keep each original currency apart and stop at the converted amounts.

## Verified by

- On a published run every amount has exactly one disposition, converted or set aside with its one reason, and the dispositions add up to the input amounts, so nothing is dropped or counted twice and every set-aside amount stays visible with its original amount and currency.
- Each converted row shows the original amount and currency as supplied, the rate used with its type, date and source, the method, whether the rate was carried, and the converted amount before and after rounding; an amount already in the reporting currency converts at one with no rate lookup.
- Each rate follows the approved date basis, gap rule and edge rule: a row whose date has a quote uses it, a row whose date has none follows the approved out-of-window rule and shows the date of the quote used, and a quote at the window's edge is treated as approved.
- Where several quote forms are allowed, each row follows the approved order and shows its method, a cross shows its oldest leg's date, and a conflicting quote, a zero or negative rate or a same-currency quote is handled as approved, never swapped for an unapproved rate.
- Converted amounts equal the original amount times the rate, worked out in exact decimals with no floating-point error and rounded once under the approved rule and the reporting currency's decimals; a negative amount keeps its sign and follows the approved rounding for negatives.
- Where the approved rule pins a run to an as-of, a rerun on the same inputs reproduces the figures, a later correction does not change that run and a later as-of picks it up; where it does not, the outcome says a past run cannot be reproduced.
- Each code, date, amount, quote or rate problem is handled as approved: matched under the approved code rule, set aside under one approved reason chosen by the approved precedence, or failing the run, and never becomes the reporting currency, zero or a dropped row.
- Each quote the approved rules left unused, such as one superseded, recorded after the as-of, outside the window, outranked or in conflict, is listed for the currencies present with the reason it was unused.
- Per original currency and approved reporting currency, converted plus set-aside original amounts equal what was received with nothing unexplained, unusable amounts are counted beside it, no output adds original amounts of two currencies, and the rounding residual stays within the approved bound.
- Where the approved rule fails a run for an unusable setting, an empty rate table or a stale one, the run names each failing condition and publishes no figures, and an earlier good run's results are untouched.
- Every figure matches values worked out independently of the model for each case the approved rules make relevant, such as a gap day, a quote at the window edge, an inverse or cross quote, an exact half, a refund or a late correction; cases not exercised are named.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile the amounts (currency codes and their case, blanks, dates and time zones, signs, major or minor units, unreadable values, floating-point columns) and the quotes (pairs, direction and units quoted, quote dates, recorded times and versions, sources, duplicates, zero rates, gaps over weekends and holidays) before modelling. Use Ask first only for semantics still open, and record each decision as the user's own answer. Keep the reporting currency, rate window, as-of, decimal counts, declared currencies and the reason list and precedence editable as data where the approved requirements say so. Do rate and amount arithmetic in exact decimals, and check that a division the platform would take as floating point is done exactly. Work out expected results for the agreed cases independently of the models before trusting them, including a correction recorded after the as-of, and say which paths the example did not exercise.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which amounts are converted (payments, refunds, adjustments, test or internal items), which currency codes are accepted and from which dates, are codes matched as supplied or after trimming and case folding, and where do the others go?
- If unresolved, which currency reports (one, or one per entity), how many decimals does each currency carry, and are amounts held in major or minor units?
- If unresolved, which date selects the rate (transaction, posting, period end or fixed) and in which time zone for a timestamp, which rate type and side (spot, average, closing; bid, ask or mid), and which source ranks first?
- If unresolved, when the date has no quote is the latest earlier quote carried, within how many calendar or business days and is the edge day included, is the next quote used, or is the amount set aside?
- If unresolved, which quote forms count (direct, inverse of the reverse, cross through which base), what scale and direction do quotes carry, in what order across forms and sources, and how are conflicts, zero or negative rates and same-currency quotes handled?
- If unresolved, how are amounts rounded (rule, step, negative amounts), what internal precision do derived rates carry, and what bound applies to the rounding residual on the reporting side?
- If unresolved, do corrected rates restate past results or is each run pinned to an as-of using the versions recorded by then, where does the as-of come from, and how are unused quotes shown?
- If unresolved, which set-aside reasons exist and in what precedence, what makes a rate table stale and which settings are unusable, and does such a run fail, publish flagged figures or publish nothing?

### Guardrails

- Do not choose the reporting currency, rate date basis, rate type, gap rule, quote order, rounding rule, versioning or reason list for the user, and take none from the data or common practice; the user may ask for alternatives or a recommendation.
- Never treat a currency code the approved matching rule does not accept as the reporting currency, and never default a missing amount, date or rate to zero or one.
- Never replace a conflicting or invalid quote with a rate the user has not approved, and never use a quote the approved date and gap rules do not allow.
- Never use floating-point arithmetic for rates or amounts, and never round before the approved step.
- Never drop, double count or silently net away an amount; each original currency reconciles on its own, and no output adds original amounts of two currencies.
- Never default the as-of to the clock without approval, and never change a past run's figures when a rate is later corrected unless the approved rule restates them.
- Stop at the converted amounts: do not post conversions, compute exchange gain or loss, translate balances, hedge, consolidate, forecast rates or source rate feeds.
