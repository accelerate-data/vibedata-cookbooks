---
id: cpg-gross-to-net-revenue
title: Build manufacturer gross-to-net revenue with trade accruals and settlements
trigger:
  - Revenue accounting closes the month by working gross to net in spreadsheets, nobody can audit them, and the trade accrual never ties to what customers claim.
  - Off-invoice discounts, returns, accrued trade spend and settlements are mixed in one number, so net revenue cannot be traced to the invoice, credit, deduction or agreement behind it.
  - Deductions and paid claims arrive without a clear agreement, and nobody can say which ones reduced the liability, which are disputed and which were quietly booked as promotion cost.
  - A trade agreement ends with a balance nobody released or expensed, or a customer is settled beyond what was accrued, and the liability no longer rolls forward.
description: For an approved cutoff, build a gross-to-net waterfall by customer, product and fiscal month and a trade-liability roll-forward by agreement and month, both exact under the user's approved rules, every amount traceable, every input row placed once or set aside with one reason.
pitch: Net revenue and the trade liability that tie exactly, with every amount traced to its invoice, credit, claim and agreement.
job_category: build
area: transformation
readiness: supported
function:
  - finance
industry:
  - cpg
domain_objects:
  - billing_line
  - credit_memo
  - trade_agreement
  - agreement_version
  - deduction
  - paid_claim
  - fiscal_calendar
  - gross_to_net_waterfall
  - trade_liability_rollforward
  - disputed_deduction
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
  - Needs billing lines, credit memos, trade agreements, deductions, claims and a fiscal calendar.
  - Stops at revenue reduction and trade liability; lift, margin, rebates and recognition are separate.
  - Applies the approved accrual, matching and close rules; it does not decide them.
  - Tables already in the Domain; exported files go to file-drop-to-bronze first.
related:
  - cpg-promotion-lift
  - effective-dated-business-rules
  - master-product-sku-hierarchy
evidence:
  features:
    - capturing-requirements
    - generating-dbt-model
    - verifying
  evals: []
---

## Prompt

Build <waterfall_model>, <rollforward_model>, <disputed_model>, <set_aside_model> and <coverage_model> from <billing_source>, <credit_memo_source>, <trade_agreement_source>, <deduction_and_claim_source> and <fiscal_calendar_source>. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only the semantics they leave open. For the approved cutoff, publish a gross-to-net waterfall at the approved customer, product and period grain and a trade-liability roll-forward per agreement and period, with every adjustment categorised, accrued, reversed, settled or trued up under the approved rules, every amount carrying its source document and agreement, and every input row placed once or set aside with one reason. Keep sources read-only and state what the inputs cannot prove.

## Verified by

- Gross sales less each approved adjustment category, plus any approved reversal or release shown beside them, equals net revenue to the approved rounding on every row and the total, with no plug, and rows equal values derived independently from the sources and approved rules.
- The roll-forward holds on every agreement and period: opening plus accrued, less reversed and settled, plus or minus trued up, equals closing, each closing is the next opening, and each opening comes from the approved opening-balance source.
- Every published amount names the source document it came from and the agreement behind it, or states that none exists; per source document the published amounts sum back to that document's own amount.
- Every input row is counted in a published figure or listed with exactly one reason, never both, and the coverage output reports each population, its counted and set-aside counts and amounts and the unaccounted residue, which is zero.
- Each agreement's adjustment category and accrual follow the approved classification and accrual rules; an agreement type with no approved category is handled as approved, never netted by default, and stays visible with its reason.
- A settlement reduces the agreement's liability under the approved match rule and reaches revenue only through an approved over-settlement or close rule, as a labelled amount; a deduction or claim the rule does not match stays on the disputed list with one reason.
- A settlement larger than the accrual available, and an agreement that reaches its close with a balance, follow the approved over-settlement and close rules; the amount is named, and a later document never reopens a closed liability unless the rules say so.
- Each return and any accrual reversal follow the approved return rules and appear as their own labelled amounts; a reversal never exceeds what the original line accrued, and an unlinked or over-quantity return is flagged and shown.
- Documents after the cutoff, in another currency, duplicated, or pointing at an unknown customer, product, invoice or agreement follow the approved rules and are shown with their reason; none is silently dropped, doubled or defaulted.
- Rebuilding on the same inputs gives identical outputs, and every output is unique on its declared grain with amounts at the approved precision.
- The outcome states what the inputs cannot prove, such as tiers, restated agreement terms or settlements the data does not carry.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile billing lines, credit memos, agreements and versions, deductions, claims and the fiscal calendar first: keys, grains, status values, duplicates, unlinked or unreferenced rows, currencies and the dates they cover. Use Ask first only for semantics still open, and record each answer as the user's own decision. Keep the classification map, accrual rules, cutoff and opening balances as editable data where the approved requirements say so. Make the waterfall, roll-forward, disputed list, set-asides and coverage agree about every document. Prove each stated behaviour on the source records, including cases the inputs do not exercise, such as an agreement with several products or an amendment mid-window, with constructed rows kept out of the sources.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, how gross sales is defined, how an agreement type becomes an adjustment category (including a type with none), and how an off-invoice discount with no agreement reference is shown.
- If unresolved, how each agreement type accrues: per unit, share of gross or lump sum, the basis, rounding, tiers, and for a lump sum its timing and allocation across products, including months with no sales.
- If unresolved, which agreement terms apply to a billing line: the version date, window edges, and whether a later amendment restates earlier accruals or only later lines.
- If unresolved, how a deduction or paid claim links to an agreement and what makes it matched: the reference fields, customer check, period and status rules, and what it needs when the agreement is closed.
- If unresolved, how an over-settlement, a balance at agreement close and a document dated after the close are treated, and whether a disputed amount is ever released or expensed.
- If unresolved, how a return affects accruals: linked or unlinked, pricing of the reversal, a quantity above what was billed, and where the reversal appears.
- If unresolved, which customers, products, agreements and document statuses are in scope, and the fiscal calendar, cutoff, partial months, documents after the cutoff, opening-liability source and whether quiet months are carried.
- If unresolved, how exceptional input is handled: currency, duplicates, unknown keys, conflicting rows, and whether a restated source row changes closed periods.

### Guardrails

- Do not choose the classification map, accrual method, version rule, match rule, close rule or cutoff for the user, and take none from the data or common practice; the user may ask for alternatives or a recommendation.
- Never let a settlement reduce revenue as well as liability except as an approved, labelled over-settlement or close amount, and never turn an unmatched deduction or claim into promotion cost or a true-up.
- Never hide a balancing amount in an unlabelled plug, and never silently round, floor or clip a figure; show the unclipped amount and any approved treatment.
- Never drop, double count or default an input row; each is counted, or set aside with one reason and counts that close.
- Never publish an amount without its source document and agreement, or an invented reference where none exists.
- Never reopen a closed liability or restate a published period unless the approved rules say so, and then as a separate labelled movement.
- Keep sources read-only, and state what the inputs cannot prove instead of presenting rules as facts.
- Stop at revenue reduction and trade liability: do not compute promotion lift, margin, supplier rebates, revenue recognition timing or GL postings, and do not manage collection.
