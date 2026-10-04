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

Build <credited_bookings_model>, <credit_exceptions_model>, <commission_bookings_model> and <quota_attainment_model> from <bookings_source>, <credit_split_source>, <rep_assignment_source>, <quota_source> and <plan_rules_source>. Settle every plan rule with the user before design: what counts as a booking, its key, credited amount and currency, the date, time zone and period that place it, eligibility for commission and for quota separately, credit roles and splits, owner changes and partly unassigned deals, cancellations and plan changes, quota grain and proration, and how exceptions are reported. Take every answer from the user, never from a default. Hold rule versions as data and list each rule left in SQL. Before any model SQL, fix a labelled fixture where each rule has a case that fails if the rule is wrong, plus hand-calculated expected outputs; freeze both. Keep Domain sources read-only. Prove each rule with committed unit and equality tests, test every key and required column, reconcile every booking, and report what the inputs cannot prove.

## Verified by

- The contract records the user's answer to every Ask first question, the fixture, hand-calculated expected rows and row counts for every output, all written and approved before model SQL; later changes to any of them carry the user's explicit approval.
- Every approved rule has a fixture case whose expected result would differ if the rule were wrong, such as boundary-date deals of the type the rule changes, reassignment around the placement date, a joiner, a leaver and a deal with several problems.
- Every in-scope booking appears in credited output or exceptions as the approved policy says, counted by distinct booking, with none lost, none in both and no join fan-out.
- Credited rows are unique on their declared business grain, including a credit event type when cancellations post separately. Per booking, credit equals the approved split; roles credited beyond the booking amount stay in their own columns and never inflate booking totals.
- Boundary-date bookings land in the approved period and plan version, and reassignment, departed-rep and partly unassigned cases are credited or excepted exactly as approved.
- A cancellation or plan change alters only the periods the approved policy names, and a rerun leaves closed periods unchanged.
- Attainment equals the credit approved for each quota holder divided by quota at the approved grain, after the approved proration for joiners and leavers. A rep-month with credit but no quota follows the approved handling and never shows zero or infinite attainment.
- Each exception reason has its approved key pattern, per booking or per rep and month, enforced by tests that required keys are filled and the others are empty.
- Committed tests compare every output with its hand-calculated expected rows in both directions using null-safe comparison. No expected value was copied from model output.
- Every model and seed has not-null tests on required columns, conditional null tests, unique tests on each business key and range checks on amounts and percentages; no key is a generated or hashed id.
- The report records revision, tool versions, commands, an independently re-run full test count with every test passing, expected and actual results, the rules left in SQL and what the inputs could not prove.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain and sources, and run dbt only on this Intent's models. Profile keys, amounts, currencies, dates, assignment intervals, quota grain and rule versions. Ask every unresolved Ask first question; never recommend a rule or record an approval the user did not give. If the Domain lacks the data, build a labelled synthetic fixture in its own schema with explicit column types, and keep expected-result seeds in a separate schema. Write the contract, fixture and hand-calculated expected rows, and get them approved before SQL. Hold versioned rules as data keyed by version and effective date, and list every rule left in SQL in the Requirement. Build staging, then a credited-bookings intermediate at the approved grain, a deal and rep-month exceptions model, a commission model with one column per credit role, and attainment over every quota row and every credited rep-month. Work test-first: unit tests from the hand calculation, then SQL, then committed equality, uniqueness, coverage, not-null, conditional-null and range tests. When a staging view changes, rebuild it and rerun its tests. Never edit fixtures or expected values to make a test pass; show the failing rows and ask. Commit and push after each task, and confirm the push.

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

- Do not decide compensation policy for the user. Take no rule from data, CRM fields, spreadsheets or common practice, never offer a recommended rule, and record approvals only from the user's own words.
- Credit for a booking may not exceed or fall short of the approved split. Keep each extra credit role in its own column so booking totals are never inflated.
- Whatever the approved handling, unassigned bookings, missing quotas, quotas without assignments, unmatched rules and unconverted currencies stay visible; never default them to zero or drop them silently.
- A cancellation, late edit or plan change alters only the periods the approved policy names. Never silently rewrite a closed period.
- Stop at commission-eligible bookings and attainment. Payout rates, tiers, accelerators and draws are a separate outcome.
- Freeze the approved fixture and expected results. Never change seeds or expected values to make a test pass, never copy model output into expected results, and report mismatches with their rows.
- A ticked plan step, a summary or a one-off query is not verification. Every check is a committed test, and the full count is re-run independently before certification.
- Keep Domain sources read-only, keep the fixture and expected results in their own schemas, and use business keys only, never generated, hashed or dbt-run ids.
- Run dbt only on this Intent's models. Report failures in models outside its scope instead of fixing them, and execute on the actual Intent target; support covers duckdb_local only.
