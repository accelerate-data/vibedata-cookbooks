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
  - Prices approved credit against plan and quota data; payments, holds and cancellations are separate inputs.
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

Build <payout_ledger_model> and <payout_exceptions_model> from <approved_credit_source>, <plan_rules_source>, <quota_source>, <payment_source>, <cancellation_source> and <hold_source>. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only what is still open: which credit is priced and in which currency, how a plan version is chosen, how attainment places a deal in a tier, the cap, what a cancellation reverses and when, holds and releases, how a payment is applied, and the period, rounding and exception rules. Price each deal under the approved rules, split a deal that crosses a tier as approved, apply the cap, holds, cancellations and payments, and publish per rep and period what was earned, held, payable, paid and clawed back, with an opening and closing payable that roll forward. Keep money owed back visible, keep every input that cannot be priced or applied as an exception with its reason, never net money across reps, and keep Domain sources read-only. Calculate obligations only: do not pay anyone or decide which bookings are eligible, and use quota only to place deals in tiers. Report what the inputs cannot prove.

## Verified by

- Published earnings, held, paid, clawed-back and closing amounts equal values derived independently from the approved credit, plan rules and events, including any deal that crosses a tier or ends exactly on a tier threshold or an applicable cap.
- For every rep and period, opening payable plus earned and approved adjustments, minus payments applied, equals closing payable, with holds, releases, clawbacks and any unapplied payment excess shown as their own approved movements; each closing is the next opening.
- Each booking is priced under the plan version and tier the approved rules give for its placement, and a deal that crosses a tier is priced as the approved method says; closed periods change only where approved.
- Where a cap applies, capped-away earnings are published beside payable earnings, uncapped equals payable plus reduction on every row, and nothing disappears.
- A cancellation reverses what the approved rule names; the same cancellation delivered twice reverses once; partial, repeated and out-of-window cancellations follow the approved handling, and periods the policy does not restate stay unchanged.
- Clawed-back money already paid, a payment above what is owed and any negative payable show the approved owed-back treatment with its amount, and are never silently set to zero.
- Held amounts stay visible and carried until the approved release, and are never counted as payable.
- A payment applies as the approved linking rule and handling say; no amount is netted across reps; a payment for no known rep, an excess and any approved reassignment appear with their reason.
- Every in-scope input amount is in the ledger or in the exceptions as the approved rule says, each exception carrying its reason and amount and adding to no ledger measure; a partly applied row is accounted per amount; rows the approved scope leaves out are shown or counted with their reason.
- Each output is unique on its declared grain, shows no duplicated or fanned-out amounts, and a rerun on unchanged inputs leaves the ledger and its closed periods identical.
- The outcome states which plan rules are explicit versioned data and which, if any, live only in model logic, which exceptions remain open, what the inputs cannot prove, and that no payment was made.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile the approved credit, plan versions and tier rules, quotas, payments, cancellations and holds first; use quota only to place deals in tiers. Use Ask first only for semantics still open, and record each decision as the user's own answer; sample data, a compensation spreadsheet or common practice cannot approve payout policy. Keep tier rates, cap and quotas as editable data where the approved design allows, and list any rule left only in model logic. Model deal pricing at deal grain with its tier pieces traceable, the ledger at one row per rep and period, and exceptions per input row with one reason. Report any approved rule the inputs cannot prove.

### Compose

- capturing-requirements
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which credit is priced, which currencies apply to credit, quota, payments and payout, which rate and date convert them, and what happens to credit in another currency?
- If unspecified, which date selects the plan version, does a version change apply from its effective date or restate earlier bookings, and do product, deal type, role or overlay credit change the rate?
- If unresolved, what base and reset period place a deal in a tier, how is quota prorated, changed or missing, how are same-date deals ordered, is a crossing deal priced marginally or retroactively, and which tier owns the boundary dollar?
- If unresolved, whether a cap applies, what it limits, over which reset period, and how capped-away money is shown?
- If unresolved, what does a cancellation reverse and when, within what clawback window, for a leaver; does it rewind attainment or the cap; how are partial, repeated and unknown-deal cancellations handled; is paid money offset, carried as owed back or written off?
- If unresolved, what places a hold, what releases it (a record, a date, a customer payment, a holdback percentage), and does a hold tied to a cancelled deal stand?
- If unresolved, which keys link a payment, hold or release to rep, period and deal; how is a payment above what is owed, for no known rep or early handled; and which leaver amounts, draws, guarantees, manual adjustments or reassignments to another rep are in scope?
- If unspecified, which time zone and period grain define the ledger, do quiet periods carry, how is money rounded, is there one exception per reason or one primary reason, and is invalid plan data, such as a tier gap or missing cap row, set aside or a failed run?

### Guardrails

- Do not decide compensation policy for the user. Take no rule from data, spreadsheets or common practice, and record approvals only from the user's own words or the Intent's approved requirements.
- Calculate obligations only. Never create a payment instruction, decide which bookings are commission-eligible or republish attainment as a result; use credit against quota only to place deals in tiers.
- Never pay or net money across reps; an approved reassignment is its own labelled movement. Never floor a negative payable to zero without an approved rule.
- Never sum different currencies except under an approved rate rule.
- Money capped away, held, clawed back or owed back stays visible; it is never dropped or merged into a direct figure.
- Unpriced credit, unmatched payments, unknown-deal cancellations and unsupported currencies stay visible with a reason; never default them to zero.
- A cancellation, late edit or plan change alters only the periods the approved policy names. Never silently rewrite a closed period.
- Synthetic or sample data can illustrate approved semantics but never authorizes real payout policy.
- Keep Domain sources read-only.
