---
id: effective-dated-business-rules
title: Build historical event amounts from effective-dated business rules
trigger:
  - Historical fees or surcharges change when a current rate is applied to past events.
  - Fleet tariffs or fare components vary by resource, customer or service date and need traceable historical calculations.
  - Overlapping rate versions or retroactive corrections make historical amounts ambiguous.
description: Build an event calculation model that selects applicable dated rules, calculates expected amounts and exposes missing or ambiguous matches under approved precedence and correction policies.
pitch: Calculate historical amounts from the rules that apply to each event, with visible exceptions and independent amount checks.
job_category: build
area: transformation
readiness: supported
domain_objects:
  - business_event
  - effective_dated_rule
  - rate_component
  - expected_amount
works_with:
  platforms:
    - duckdb_local
    - motherduck
    - fabric_lakehouse
    - fabric_warehouse
    - redshift
  tools:
    - dbt
evidence:
  features:
    - profiling-source-data
    - applying-medallion-data-modelling
    - generating-dbt-model
    - dbt-unit-testing
    - running-dbt-in-sandbox
    - verifying
  evals: []
---

## Prompt

Build <historical_amount_model> for the historical calculation questions and breakdowns required in this Intent. Inspect approved requirements, event inputs and governed dated rules; settle unresolved applicability timestamps, qualifying dimensions, validity boundaries, rule composition, precedence and correction policy. Select applicable rule versions and calculate expected amounts with explicit units, currency and rounding. Preserve event and rule lineage, and expose missing, ambiguous, excluded or invalid cases. Keep descriptive reference codes separate from dated calculation rules. Materialize the model in the Intent's sandbox and verify independent before/at/after, dimension, overlap, gap, composition and amount cases. Prove that a future rate leaves earlier amounts unchanged and that retroactive corrections affect only their approved scope. Identify missing attributes, history, mappings or relationship evidence that prevent an agreed question from being answered.

## Verified by

- The contract fixes event/output grain, scoped population, rule identity/version, applicability timestamp and timezone, validity boundaries, qualifying dimensions, precedence/composition, units, currency, rounding, no-match and retroactive-correction policy, plus required questions and breakdowns.
- Each scoped event retains source identity, calculation inputs, selected rule versions and a calculated, excluded or unresolved disposition. Invalid intervals, missing inputs, unmapped qualifiers and ambiguous matches remain visible; input counts close without event loss or unintended join fan-out.
- A labelled synthetic fixture uses one currency, quantity 4 and half-open validity: A has rate 2 before boundary T and rate 3 from T. Events just before, exactly at and just after T select the old/new/new versions and independently yield 8/12/12, rejecting a current-rate join.
- Under that fixture's explicit exclusive policy, B has rate 7 across T: its event yields 28. Separate resource, fleet and customer cases vary one qualifying dimension at a time and select the approved version or no-match outcome; unrelated rates cannot leak across qualifiers.
- Boundary cases cover open-ended validity, null timestamps, timezone conversion and source precision. Duplicate or overlapping candidates, equal-priority ties and gaps produce the approved resolution or visible unresolved status; arbitrary row selection and silent zero defaults fail.
- Component rules have independent expectations for eligibility, composition order, precedence and rounding. A labelled additive fixture at rate 3 with quantity 4 and fixed fee 1 yields 13; an exclusive override of 5 per unit yields 20, not 25 or 33. Only approved policies apply to real inputs.
- Independent calculations cover required formulas, zero/null quantities, negative adjustments, unit scales, currencies and rounding edges. Each component and total matches approved precision; incompatible inputs remain unresolved until an approved conversion is available.
- A future version effective at U after T leaves all earlier rule selections and amounts unchanged on rerun; a case at U selects the new version. Expected results are fixed before model SQL and compared at event/component grain, not only as grand totals.
- Retroactive corrections follow the approved restatement or as-known policy. A controlled corrected version changes only eligible events, or preserves prior as-known results as specified; late events use the approved time basis. Original/corrected lineage and differences remain auditable.
- Event/component uniqueness and permitted cardinalities hold. Calculated totals reconcile to independent component sums and required breakdowns; excluded and unresolved counts and any known amounts reconcile separately, with unknown amounts never presented as complete totals.
- Every agreed question has supporting attributes and relationship evidence or an explicit input gap. Observed source relationships, approved rule policies and synthetic examples remain distinguishable; descriptive code mappings cannot substitute for evidence of dated calculation rules.
- dbt checks and independent acceptance queries pass on the actual Intent platform after materialization and rerun; every output is read back. The report records revision, commands, exits, rule selections, amounts, reconciliation balances, correction/future-rate comparisons and unresolved exceptions.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain and sources. Inspect approved questions, authoritative dated rules and event evidence first. Profile identities, versions, qualifying dimensions, cardinalities, time precision, units and interval quality. Use Ask first only for unresolved semantics; sample values or existing SQL cannot approve policy. Record effective time separately from recorded/correction time and choose the approved restatement or as-known basis. Confirm required history exists. Specify component grain, composition order, precedence, tie handling, gaps, conversions and rounding. Keep code descriptions separate from governed calculation rules. Fix expected rule selections, amounts and exceptions independently before model SQL, including before/at/after boundaries, qualifying dimensions, overlaps, gaps, component interactions and rounding. Build dated joins and calculations with the composed skills and current target dialect/sandbox guidance; preserve event-to-rule lineage and exception balances. Materialize, read back and rerun, then reconcile counts, components and required breakdowns. Compare future versions, late events and retroactive corrections in an approved writable fixture area while keeping Domain read-only. Use existing governed rule inputs; surface missing authoritative inputs without inventing policy. Report missing evidence and any untested required case as incomplete verification.

### Compose

- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which historical amounts, analytical questions and breakdowns are required, and what event population and output/component grain belong in scope?
- If not established, which authoritative rules and version identities apply, which event timestamp determines applicability, and what timezone, precision and interval boundary conventions govern selection?
- If incomplete, which resource, fleet, customer or other dimensions qualify each rule, and what source evidence supplies their values at the relevant event time?
- If not approved, which components add, compound or override, in what order, with what precedence and tie policy; what must happen for overlaps, gaps, invalid rules and missing inputs?
- If unresolved, which quantity units, currencies, formulas, conversions, rounding stages and precision apply, including zero quantities, credits and negative adjustments?
- If not decided, do retroactive corrections restate history or preserve an as-known result, which recorded/correction timestamp defines that view, and how should late events and corrected outputs be identified and reprocessed?

### Guardrails

- Do not infer legal, tariff or commercial policy from synthetic fixtures, current rates, sample values or convenient existing code. Fixtures demonstrate approved semantics; they do not authorize real policy.
- Do not select the newest rule without the event's applicability time and qualifiers, hide overlaps with arbitrary deduplication, or discard unresolved events to make totals reconcile.
- Missing rules or required inputs are not zero amounts. Apply only approved fallback or no-match behavior and retain the reason, source event and candidate rule evidence.
- Keep descriptive reference codes distinct from dated calculation rules. Do not invent historical dimension assignments, missing rule versions, unit conversions or relationships to complete an amount.
- Keep this outcome to applying dated rules to events. Do not build a generic policy engine or expand into dimension-history capture; surface missing history and evidence without requiring another Recipe for verification.
- Use the actual Intent platform and provided sandbox. Do not substitute another engine, synthesize an absent sandbox or mutate Domain sources to manufacture correction or future-rate evidence.
- Build success does not prove rule applicability or amount correctness. Required independent selections, calculations, exception balances and future/correction comparisons must pass before claiming completed verification.
