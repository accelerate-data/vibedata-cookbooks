---
id: revops-quota-commission
title: Build commission-eligible bookings and quota attainment from explicit plan rules
trigger:
  - Reps, managers and finance disagree on attainment because each team credits bookings with its own spreadsheet logic.
  - Compensation plan rules for eligibility, crediting splits and timing live in documents, not in tested models.
  - A rep moved territory, a deal was cancelled or a plan changed mid-year, and nobody can say which bookings counted in a closed period.
description: Credit each booking to the reps and periods the user's approved plan rules name, flag commission eligibility, roll credit against quota, and keep every booking or quota that cannot be credited visible as an exception.
pitch: Turn written compensation plan rules into tested, traceable commission-eligible bookings and quota attainment.
job_category: build
area: transformation
readiness: supported
domain_objects:
  - booking
  - compensation_plan_rule
  - credit_assignment
  - quota
  - quota_attainment
works_with:
  platforms:
    - duckdb_local
  tools:
    - dbt
qualifiers:
  - Complete outcome assessed for duckdb_local only; the other four Studio targets remain unassessed.
  - Stops at commission-eligible bookings and attainment; payout amounts are a separate outcome.
  - Assessed with a labelled synthetic fixture standing in for CRM bookings, rep assignments, quotas and plan rules.
  - Credit ignoring today's owner needs owner history in the source; the assessed fixture had none.
related:
  - effective-dated-business-rules
  - metric-population-and-rollups
  - business-event-fact
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

Build <credited_bookings_model>, <credit_exceptions_model>, <commission_bookings_model> and <quota_attainment_model> from <bookings_source>, <credit_assignment_source>, <quota_source> and <plan_rules_source>. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only what is still open: booking identity, credited amount and currency, the date, time zone and period that place a booking, commission and quota eligibility, credit roles and splits, owner changes and unassigned deals, cancellations and plan changes, quota grain and proration, and exception reporting. Credit each in-scope booking to the reps and periods the approved rules name, flag commission eligibility separately from quota credit, and roll credit against quota. Keep each result traceable to its plan-rule version, keep every booking or quota that cannot be credited visible as an exception, and keep Domain sources read-only. Report what the inputs cannot prove.

## Verified by

- Every in-scope source booking is either credited or excepted as the approved policy says, never both and never lost; booking counts and amounts reconcile to the source with no duplication or join fan-out.
- Per booking, credited amount equals the approved split. Credit types granted beyond the booking amount, such as overlay credit, stay distinguishable and never inflate booking totals.
- Each booking lands in the period, plan version and eligibility the approved rules give for its placement date, including bookings on period and plan-version boundaries.
- Commission eligibility and quota credit follow their own approved rules, so a booking counts toward quota without being commission-eligible exactly when the plan says so.
- Owner changes, departed reps and unassigned or partly unassigned bookings are credited or excepted exactly as approved, and credit never follows today's owner unless that is the approved rule.
- Cancellations, downgrades and plan changes alter only the periods the approved policy names, and a rerun leaves closed periods unchanged.
- Attainment for each quota holder and period equals approved credit divided by quota after approved proration. Credit without a quota and quota without an assignment follow the approved handling and never show zero or infinite attainment.
- Every exception names its reason and the booking or rep-period it concerns. Unassigned bookings, missing quotas, unmatched rules and unconverted currencies are never defaulted to zero or dropped.
- Each output is unique on its declared business grain, required fields are populated, and amounts and percentages stay within approved ranges.
- Every credited row traces to the source booking, credit assignment, quota and plan-rule version that produced it.
- The outcome states which plan rules are held as data, which are expressed only in model logic, which exceptions remain open and what the inputs cannot prove.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile booking keys, amounts, currencies, dates, credit assignments and their effective intervals, quota grain and plan-rule versions. Use Ask first only for semantics still open, and record each decision as the user's own answer; sample data, CRM fields and spreadsheets cannot approve compensation policy. Keep plan rules explicit and versioned by effective date, and list any rule expressed only in model logic. Model credited bookings at an explicit business grain, exceptions per booking or per rep-period as approved, commission-eligible bookings with credit types kept distinguishable, and attainment over every quota and every credited rep-period. Report any approved rule the inputs cannot prove and any open exception.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which periods, teams, products and booking types are in scope, which bookings are eligible for commission, which count toward quota, and are those the same set?
- If not established, what counts as a booking, which field identifies it, which amount and currency are credited, such as ACV, TCV or net new ARR, which exchange rate applies, and how are split amounts rounded?
- If unresolved, which date, time zone and period grain place a booking, such as close date and calendar month or fiscal quarter, and when does a period close to change?
- If unresolved, who receives credit, how are splits set and checked, may a role such as an overlay be credited beyond the booking amount, and is that credit commission-eligible?
- If unspecified, when an owner changes, does credit go to the rep assigned on the placement date or the current owner, and what happens to unassigned, departed-rep and partly unassigned split bookings?
- If unresolved, are cancellations, downgrades and clawbacks in scope, do they post when they happen or restate, and does a plan change apply from its effective date or restate earlier bookings?
- If unresolved, at what grain and period are quotas set, which credit counts toward each quota, are joiners and leavers prorated, and what happens to credit without a quota or a quota without an assignment?
- If unspecified, does a booking with several problems get one exception per reason or one primary reason, and which exceptions are keyed per booking or per rep and month?

### Guardrails

- Do not decide compensation policy for the user. Take no rule from data, CRM fields, spreadsheets or common practice, never offer a recommended rule, and record approvals only from the user's own words or the Intent's approved requirements.
- Credit for a booking may not exceed or fall short of the approved split, and credit types granted beyond the booking amount must never inflate booking totals.
- Whatever the approved handling, unassigned bookings, missing quotas, quotas without assignments, unmatched rules and unconverted currencies stay visible; never default them to zero or drop them silently.
- A cancellation, late edit or plan change alters only the periods the approved policy names. Never silently rewrite a closed period.
- Do not credit by today's owner when the approved rule needs the owner at the placement date, and do not invent assignment history the source lacks; report the gap instead.
- Stop at commission-eligible bookings and attainment. Payout rates, tiers, accelerators and draws are a separate outcome.
- Synthetic or sample data can illustrate approved semantics but never authorizes real compensation policy.
- Keep Domain sources read-only.
