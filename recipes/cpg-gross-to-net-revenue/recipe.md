---
id: cpg-gross-to-net-revenue
title: Build manufacturer gross-to-net revenue with trade accruals and settlements
trigger:
  - Revenue accounting closes the month by working gross to net in spreadsheets, nobody can audit them, and the trade accrual never ties to what customers claim.
  - Off-invoice discounts, returns, accrued trade spend and settlements are mixed in one number, so net revenue cannot be traced to the invoice, credit, deduction or agreement behind it.
  - Deductions and paid claims arrive without a clear agreement, and nobody can say which ones reduced the liability, which are disputed and which were quietly booked as promotion cost.
  - A trade agreement ends with a balance nobody released or expensed, or a customer is settled beyond what was accrued, and the liability no longer rolls forward.
description: For an approved cutoff, build a gross-to-net waterfall at the approved customer, product and period grain and a trade-liability roll-forward by agreement and period, both tying under the user's approved rules and rounding, every amount traceable, every input amount placed once or set aside with one reason.
pitch: Net revenue and the trade liability that tie to the approved rounding, with every amount traced to its invoice, credit, claim and agreement.
job_category: build
area: transformation
readiness: supported
function:
  - finance
  - revops
industry:
  - cpg
domain_objects:
  - customer
  - product
  - billing_line
  - credit_memo
  - trade_agreement
  - agreement_version
  - deduction
  - paid_claim
  - fiscal_calendar
  - disputed_deduction
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
  - Stops at revenue reduction and trade liability; lift, margin, supplier rebates and recognition are separate.
  - Applies the approved accrual, matching and close rules; it does not decide them.
  - Tables already in the Domain; exported files go to file-drop-to-bronze first.
  - A source with no recorded time cannot show late changes; restatement then reads unproven.
related:
  - cpg-promotion-lift
  - effective-dated-business-rules
  - master-product-sku-hierarchy
  - procurement-supplier-rebate-accrual
  - finance-revenue-recognition
  - order-return-contribution-margin
  - finance-ar-aging-dso
  - file-drop-to-bronze
evidence:
  features:
    - capturing-requirements
    - generating-dbt-model
    - dbt-unit-testing
    - verifying
  evals: []
---

## Prompt

Build <waterfall_model>, <rollforward_model>, <disputed_model>, <set_aside_model> and <coverage_model> from <billing_source>, <credit_memo_source>, <trade_agreement_source>, <deduction_and_claim_source>, <customer_and_product_source>, <fiscal_calendar_source>, <opening_liability_source> where approved, and <volume_source> where accruals use scanned or estimated volume. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only the semantics they leave open. For the approved cutoff, entity scope and currency, publish a gross-to-net waterfall at the approved customer, product and period grain and a trade-liability roll-forward per agreement and period, with every adjustment categorised, accrued, reversed, settled or trued up under the approved rules, every amount carrying its source document and agreement, and every input amount placed once, part by part where an approved rule splits a row, or set aside with one reason. Keep sources read-only and state what the inputs cannot prove.

## Verified by

- Gross sales less each approved adjustment category, plus any approved reversal or release shown beside them, equals net revenue to the approved rounding on every row and the total, with no plug, and rows equal values derived independently from the sources and approved rules.
- Per agreement and period, opening plus accrued, less reversed and settled, plus or minus trued up and any other movement approved rules show as its own class (such as an expensed over-settlement or a restatement), equals closing; each closing is the next opening, the first from the approved opening.
- Every published amount names the source document and agreement it traces to, or states that none exists; amounts taken from a document (gross, credits, deductions, claims) sum back to its own amount, and each accrual traces to the line, volume record or agreement term that drove it.
- Every input amount is counted in published figures or set aside with one reason, part by part where an approved split, partial match or stacking divides a row, never both for one part; a flag on a counted row sets nothing aside; coverage shows counted and set-aside counts and amounts, zero residue.
- Each agreement's adjustment category and accrual follow the approved classification and accrual rules; an agreement type with no approved category is handled as approved, never netted by default, and stays visible with its reason.
- A settlement reduces the agreement's liability under the approved match rule and reaches revenue only through an approved over-settlement, close or write-off rule, as a labelled amount; an unmatched deduction or claim, or part of one, stays disputed with one reason until an approved rule clears it.
- A settlement larger than the accrual available, and an agreement that reaches its close with a balance, follow the approved over-settlement and close rules; the amount is named, and a later document never reopens a closed liability unless the rules say so.
- Each return and any accrual reversal follow the approved return rules and appear as their own labelled amounts; a reversal beyond what the original line accrued, and an unlinked or over-quantity return, follow the approved rules and are flagged and shown.
- Documents after the cutoff, in another currency, duplicated, or pointing at an unknown customer, product, invoice or agreement follow the approved rules and are shown with their reason; none is silently dropped, doubled or defaulted.
- Rebuilding on the same inputs gives identical outputs, and every output is unique on its declared grain with amounts at the approved precision.
- The outcome states what the inputs cannot prove, such as tiers, restated agreement terms, settlements the data does not carry, or late changes where no recorded time exists.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile billing lines, credit memos, agreements and versions, deductions, claims, customer and product masters, any volume records and the fiscal calendar first: keys, grains, status values, duplicates, unlinked or unreferenced rows, currencies and the dates they cover. Use Ask first only for semantics still open, and record each answer as the user's own decision. Keep the classification map, accrual rules, cutoff and opening balances as editable data where the approved requirements say so. Make the waterfall, roll-forward, disputed list, set-asides and coverage agree about every document. Prove each stated behaviour on the source records, including cases the inputs do not exercise, such as overlapping agreements or a partly matched deduction, with constructed rows kept out of the sources.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, how gross sales is defined, how an agreement type becomes an adjustment category (including a type with none), how an off-invoice discount with no agreement reference is shown, and where and how amounts are rounded.
- If unresolved, how each agreement type accrues: per unit, share of gross or lump sum, the volume basis (billed, shipped, scanned or estimated), tiers, and for a lump sum its timing and allocation across products, including months with no sales.
- If unresolved, which agreements and terms apply to a billing line: the customer and product level they cover, whether overlapping agreements stack or one wins, which document date places a line in a window and picks the version, and whether an amendment restates earlier accruals or only later lines.
- If unresolved, how a deduction or paid claim links to agreements and what makes it matched: the reference fields, customer check, period and status rules, how one spanning several agreements or matching only in part is split, and what it needs when the agreement is closed.
- If unresolved, how an over-settlement, a balance at agreement close and a document dated after the close are treated, how a close amount is spread across the agreement's products, and whether a disputed amount is ever written off, released or expensed.
- If unresolved, which credit memos are returns, price corrections or trade settlements, and how a return affects accruals: linked or unlinked, pricing of the reversal, a quantity above what was billed, and where the reversal appears.
- If unresolved, which entities, currency, customers, products, agreements, deduction types and statuses are in scope; the published customer, product and period levels and hierarchy version; the fiscal calendar, cutoff, partial months, late documents, opening liability and quiet months.
- If unresolved, how exceptional input is handled: another entity, another currency (set aside, failed or converted at an approved rate), duplicates, unknown keys, conflicting rows, a missing recorded time, and whether a restated source row changes closed periods.

### Guardrails

- Do not choose the classification map, accrual method, version or stacking rule, match or split rule, close rule, scope or cutoff for the user, and take none from the data or common practice; the user may ask for alternatives or a recommendation.
- Never let a settlement reduce revenue as well as liability, and never turn an unmatched deduction or claim into promotion cost, a true-up or revenue except under an approved over-settlement, close or write-off rule, as a labelled amount that keeps its reason.
- Never hide a balancing amount in an unlabelled plug, and never silently round, floor or clip a figure; show the unclipped amount and any approved treatment.
- Never drop, double count or default an input amount; each is counted or set aside with one reason, part by part where an approved rule splits a row, and the counts close.
- Never publish an amount without its source document and agreement, or a statement that none exists, and never invent a reference.
- Never reopen a closed liability or change a published period unless the approved rules say so, and then only where they place the change, labelled and never silent.
- Never sum or net amounts in different currencies unless converted under an approved rate rule, and keep entities apart unless the approved scope combines them.
- Keep sources read-only, and state what the inputs cannot prove instead of presenting rules as facts.
- Stop at revenue reduction and trade liability: do not compute promotion lift, margin, supplier rebates, revenue recognition timing or GL postings, and do not manage collection.
