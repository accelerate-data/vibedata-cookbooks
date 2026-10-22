---
id: sales-commission-payout-ledger
title: Build a sales commission payout ledger with accelerator tiers, caps and clawbacks
trigger:
  - Finance cannot say what each rep is owed because tier rates, caps, holds, payments and cancellations are applied by hand in a spreadsheet.
  - A deal crossed an accelerator tier, a rep hit the cap, or a deal was cancelled after it was paid, and nobody can show how the payable balance moved.
  - Plan rates changed mid-year and the team cannot say which version priced which booking.
description: Price each rep's approved booking credit under the plan version, tier and cap rules the user approves, apply holds, cancellations and payments, and publish an earned, held, payable, paid and clawed-back ledger per rep and period that rolls forward and keeps every unpriced input visible.
pitch: Turn approved booking credit and plan rules into a rep-period payout ledger that rolls forward and shows every clawback.
job_category: build
area: transformation
readiness: supported
function:
  - revops
  - finance
domain_objects:
  - commission_plan_version
  - attainment_tier
  - commission_payout_ledger
  - clawback
  - payment
works_with:
  platforms:
    - duckdb_local
  tools:
    - dbt
qualifiers:
  - Complete outcome assessed for duckdb_local only; the other four Studio targets remain unassessed.
  - Needs approved eligible credit; plan rules may be captured as data. Eligibility belongs to the quota Recipe.
  - Calculates obligations only; it never executes payroll or payment.
related:
  - revops-quota-commission
  - effective-dated-business-rules
evidence:
  features:
    - capturing-requirements
    - applying-medallion-data-modelling
    - generating-dbt-model
    - dbt-unit-testing
    - running-dbt-in-sandbox
    - verifying
  evals: []
---

## Prompt

Build <payout_ledger_model> and <payout_exceptions_model> from <approved_credit_source>, <plan_rules_source>, <quota_source>, <payment_source>, <cancellation_source> and <hold_source>. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only what is still open: which credit is priced and in which currency, how a plan version is chosen, how attainment places a deal in a tier, the cap, what a cancellation reverses and when, holds and releases, how a payment is applied, and the period, rounding and exception rules. Price each deal under the approved rules, split a deal that crosses a tier as approved, apply the cap, holds, cancellations and payments, and publish per rep and period what was earned, held, payable, paid and clawed back, with an opening and closing payable that roll forward. Keep money owed back visible, keep every input that cannot be priced or applied as an exception with its reason, never move money between reps, and keep Domain sources read-only. Calculate obligations only: do not pay anyone or decide which bookings are eligible, and use quota only to place deals in tiers. Report what the inputs cannot prove.

## Verified by

- Published earnings, held, paid, clawed-back and closing amounts equal values derived independently from the approved credit, plan rules and events, including a deal that crosses a tier and a deal that ends exactly on a tier threshold or on an approved cap.
- For every rep and period, opening payable plus earned and approved adjustments, minus payments, equals closing payable, with holds, releases and clawbacks shown as their own approved movements, and each closing is the next period's opening.
- Each booking is priced under the plan version and tier the approved rules give for its placement, and a deal that crosses a tier is priced as the approved method says; closed periods change only where approved.
- Where a cap applies, capped-away earnings are published beside payable earnings, uncapped equals payable plus reduction on every row, and nothing disappears.
- A cancellation reverses what the approved rule names, once per deal, even when delivered more than once; periods the policy does not restate stay unchanged.
- Clawed-back money already paid, a payment above what is owed and any negative payable show the approved owed-back treatment with its amount, and are never silently set to zero.
- Held amounts stay visible and carried until the approved release, and are never counted as payable.
- A payment applies only to its own rep; a payment for no known rep is listed with its reason and applied to nobody, and no amount is netted across reps.
- Every in-scope input row is in the ledger or appears once in the exceptions with one reason and its amount and contributes to no measure; rows the approved scope leaves out are counted with their reason.
- Each output is unique on its declared grain, shows no duplicated or fanned-out amounts, and a rerun on unchanged inputs leaves the ledger and its closed periods identical.
- The outcome states which plan rules are explicit data and which live only in model logic, which exceptions remain open, what the inputs cannot prove, and that no payment was made.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile the approved credit, plan versions and tier rules, quotas, payments, cancellations and holds first; use quota only to place deals in tiers. Use Ask first only for semantics still open, and record each decision as the user's own answer; sample data, a compensation spreadsheet or common practice cannot approve payout policy. Keep tier rates, cap and quotas as editable data, never literals in model code. Model deal pricing at deal grain with its tier pieces traceable, the ledger at one row per rep and period, and exceptions per input row with one reason. Write the expected ledger by hand from the approved rules before the models exist, and compare in both directions. Report any approved rule the inputs cannot prove.

### Compose

- capturing-requirements
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which approved credit is priced, which currencies are in scope and what happens to credit in another currency, such as converting at an approved rate, a separate ledger or listing it unpriced?
- If unspecified, which date selects the plan version for a booking, and does a version change apply from its effective date or restate earlier bookings?
- If unresolved, what base places a deal in a tier, such as year-to-date or plan-year credit against quota, how are deals ordered on one date, is a deal that crosses a tier priced marginally or retroactively, and which tier owns the boundary dollar?
- If unresolved, whether a cap applies, what it limits, at what period, and how capped-away money is shown?
- If unresolved, what does a cancellation reverse, in which period, and does it rewind attainment or the cap; how are partial, repeated and unknown-deal cancellations handled, and is a clawback of paid money offset against later payables, carried as owed back or written off?
- If unresolved, what places a hold, what releases it, and does a hold tied to a cancelled deal stand?
- If unresolved, how is a payment applied, and what happens to a payment above what is owed, a payment for no known rep or before it is payable, and unreleased amounts of a departed rep?
- If unspecified, which time zone and period grain define the ledger, do quiet periods carry, how is money rounded, and does an input with several problems get one exception per reason or one primary reason?

### Guardrails

- Do not decide compensation policy for the user. Take no rule from data, spreadsheets or common practice, and record approvals only from the user's own words or the Intent's approved requirements.
- Calculate obligations only. Never create a payment instruction, decide which bookings are commission-eligible or republish attainment as a result; use credit against quota only to place deals in tiers.
- Never pay, net or move money across reps, and never floor a negative payable to zero without an approved rule.
- Money capped away, held, clawed back or owed back stays visible; it is never dropped or merged into a direct figure.
- Unpriced credit, unmatched payments, unknown-deal cancellations and unsupported currencies stay visible with a reason; never default them to zero.
- A cancellation, late edit or plan change alters only the periods the approved policy names. Never silently rewrite a closed period.
- Synthetic or sample data can illustrate approved semantics but never authorizes real payout policy.
- Keep Domain sources read-only.
