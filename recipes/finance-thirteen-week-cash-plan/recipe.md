---
id: finance-thirteen-week-cash-plan
title: Build a thirteen-week cash plan with traceable scenario assumptions
trigger:
  - The weekly cash view is a spreadsheet rebuilt by hand each week, and nobody can say which receipt, payment or assumption moved a week's balance.
  - Treasury needs a weekly roll-forward for each approved scenario, with the date and rule behind every expected movement, before the cash review.
  - Overdue invoices, disputed items, undated obligations and invoices listed in two inputs are handled differently by each person who builds the plan.
description: For each approved scenario version, roll cash forward over thirteen weeks from opening balances and approved open items, payroll and commitments, keeping the date and rule behind every movement and every item left out of the weeks visible with its reason and amount.
pitch: Roll cash forward week by week for each approved scenario, with the date and rule behind every movement and nothing quietly dropped.
job_category: build
area: transformation
readiness: supported
function:
  - finance
domain_objects:
  - cash_plan
  - plan_week
  - opening_cash_balance
  - receivable
  - payable
  - payroll_schedule
  - commitment
  - scenario_version
  - scenario_rule
  - expected_movement
  - set_aside_item
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
  - Open items arrive as landed tables; aging them is a separate outcome.
  - Uses approved assumptions only; it is not a forecasting model or a recommendation to borrow or invest.
  - Stops at the plan; budget comparison, revaluation and ledger posting are separate outcomes.
  - A past plan as issued needs kept snapshots; a rebuild restates it.
  - Rates, calendars and rules are inputs; sourcing rates and detecting duplicate invoices are separate outcomes.
related:
  - finance-ar-aging-dso
  - finance-ap-aging
  - finance-budget-forecast-actual
  - finance-duplicate-invoice-detection
  - revops-bookings-billings-cash
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

Build <weekly_plan_model>, <movement_model>, <set_aside_model> and <coverage_model> from <opening_cash_source>, <receivables_source>, <payables_source>, <payroll_schedule_source>, <commitments_source> and <scenario_rules_source>. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only the semantics they leave open. For each approved scenario version, place each open item on an expected date under the version's approved rules, publish thirteen consecutive weeks with opening balance, receipts, payments and closing balance, and keep for every movement its direction, expected date, week, amount, currency, source item, version and the rule or dating basis that placed it. Account for every item's amount as movements or set-asides, each with one reason. Keep sources read-only and report what the inputs cannot prove.

## Verified by

- At the approved grain, each version publishes exactly thirteen consecutive weeks where opening plus receipts minus payments equals closing, up to any approved rounding shown where it arises; week one opens from the approved opening balance and each later week from the prior closing.
- An expected weekly table derived independently from the sources and approved rules agrees with the published one, and receipts and payments recomputed from the movement rows equal the weekly figures, so a check never repeats the implementation's own calculation.
- Every movement carries its expected date, week, version and the approved rule, or the approved dating basis where no rule shifts it, never an invented rule; the date follows the approved calendar rule and falls inside its own week.
- A rule that moves an item changes only its week; a move past the last week makes it a set-aside at its full amount, so plan plus set-aside is unchanged and no cash is created or lost; cash already in the opening balance never moves again.
- An item referenced by two inputs under the approved match key moves cash once; the other copy is listed as a duplicate with its amount, never counted as cash or as an unscheduled claim, and conflicting amounts or dates resolve as approved.
- Each item's open amount is fully accounted for across movements and set-asides, each part with one approved reason and parts summing to the open amount; a partly settled item moves its open remainder, and credits and unapplied items land as approved, visible with their amounts.
- Items outside the approved scope, and counts and amounts per version, reconcile to the inputs with zero residue: every input item is a movement, a set-aside or shown as out of scope with its reason.
- Overdue, disputed, undated and beyond-horizon items follow the approved handling per version and are visible with their amounts; no scenario lowers its own outflow by setting a payment aside unless the approved rules say so.
- Amounts in a currency other than the plan currency are never summed into the plan; they are converted only under an approved rate rule, or set aside in their own currency and amount.
- Only approved scenario versions and rules are planned; an unapproved version is never published as approved, and an unapproved rule changes no movement.
- A missing opening balance, unknown scenario or unplaceable item is never read as zero or hidden: affected weeks are shown as unproven or the run fails naming the item, and a partial plan is never reported complete.
- Unscheduled receipts and payments are published separately per version, direction and currency beside the plan, never netted or summed across currencies; identical inputs, as-of date, version and rules give identical output, unique on its declared grain.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile the opening balances and their date, the open receivables and payables (due dates, open amounts, dispute and currency fields, document keys), the payroll schedule, the commitments and the scenario rules. Use Ask first only for semantics still open, and record each decision as the user's own answer. Keep the plan start, week boundaries, calendars, scenario versions, delays, overdue handling and approval flags as editable data rather than constants in model code, and fail the build on a value outside an allowed set. Derive the expected weekly table independently from the sources and approved rules before any model exists, and never edit it to make a build pass. Report every item left out of the weeks and what the inputs cannot prove.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which date starts week one, where weeks start and end, which entities, accounts and currency are covered, whether it is published per account, entity or consolidated, how own-account transfers, intercompany items and restricted cash are treated, and the opening balance and as-of date.
- If unresolved, which date places a receipt and a payment, whether a rule shifts it by customer, supplier or payment method, which business-day and holiday calendar and payment-run days apply, and whether payroll and commitments move with a scenario.
- If unresolved, what overdue receipts and payments, disputed items or the disputed part of an item, undated obligations and items dated after the last week do per scenario: move cash in a stated week, or stay out and be listed with their amount.
- If unresolved, what identifies an item in two inputs, including an order and its later invoice across payables and commitments, which copy and amount counts, and how partly settled items, instalments, credits, offsets and unapplied payments are treated, aligned to the opening balance date.
- If unresolved, which commitment classes and statuses count, how recurring schedules expand inside the window, which payroll components are included, and whether non-invoice receipts such as refunds or financing enter as approved inputs.
- If unresolved, which currency the plan uses and whether other currencies are converted (which rate, as of which date, rounded where), shown in their own plan, or set aside.
- If unresolved, which scenario versions exist, what each changes (delays, or a share collected or paid and where the remainder goes), who approves versions and rules, which versions a default run publishes, and what an unapproved selection does.
- If unresolved, how items left out are shown beside the plan, what happens when the plan cannot be computed (fail naming it, or publish flagged as unproven), and whether a restated input restates past plans or past plans are kept.

### Guardrails

- Do not choose week boundaries, grain, timing rules, calendars, overdue or dispute handling, duplicate precedence, currency treatment or scenario rules for the user, nor take them from the data or common practice; the user may ask for options or a recommendation.
- Never show an item as moved cash without an approved date and rule or dating basis behind it, and never let a delay create or remove cash.
- Never count one document twice because two inputs list it, never add a duplicate copy to any unscheduled figure, and never move cash already in the opening balance again.
- Never drop, round away or silently absorb an amount: each part moves once or is listed with one reason and its amount.
- Never net money in with money out in one figure unless an approved offset rule says so, nor sum currencies without an approved rate rule.
- Never run an unapproved scenario version or rule, never read a missing input as zero, and never read a clock, random value or build timestamp into a figure.
- Do not present the plan as a forecast, a budget comparison or advice to borrow or invest.
- Do not edit a source, post to a ledger or write the plan back to a planning tool.
