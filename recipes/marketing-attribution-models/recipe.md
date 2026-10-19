---
id: marketing-attribution-models
title: Attribute conversions to touchpoints under several models side by side
trigger:
  - Marketing and Sales each have a spreadsheet crediting their channel with the same revenue, and together they claim more than was booked.
  - Channel credit differs between tools or reports and nobody can show which rule explains the gap.
  - A lookback, conversion or model setting is about to change and the owner must see which channels gain or lose, and why, before the numbers move.
description: Split the value of each qualifying conversion across the marketing touches before it under several approved attribution models side by side, with each model's credit adding back to the conversion value, every touch and conversion accounted for, and channels compared across models.
pitch: One reproducible attribution whose credit under every model adds back to booked value, so teams can see exactly where they differ.
job_category: build
area: transformation
readiness: supported
domain_objects:
  - touchpoint
  - conversion
  - identity_link
  - channel_map
  - attribution_model
  - attribution_setting
  - credit_line
  - unattributed_amount
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
  - Touchpoint, conversion and any adjustment records must already be landed as tables; this Recipe does not ingest them.
  - Who converted is resolved through the identity the Intent supplies; this Recipe does not build identity.
  - Visits or sessions used as touches must already be built; this Recipe does not sessionize events.
  - Rule-based models only; data-driven models, incrementality, spend and payback are out of scope.
related:
  - business-event-fact
  - identity-golden-record-crosswalk
  - customer-historical-ltv
  - effective-dated-business-rules
  - metric-population-and-rollups
evidence:
  features:
    - capturing-requirements
    - generating-dbt-model
    - verifying
  evals: []
---

## Prompt

Build <attribution_model_set> that splits the value of each qualifying conversion in <conversion_sources> across the approved marketing touches in <touchpoint_sources> that came before it, under the approved attribution models side by side. Inherit the Intent's sources, platform and approved requirements, and settle only what they leave open: what a conversion is and which value is split, how a touch is tied to who converted, which touches are eligible and over what lookback, and how each model weights them. Under every model a conversion's credit plus its explicit unattributed amount equals its value exactly. Account for every touch and every conversion candidate as credited, given no credit with a reason, set aside with a reason, or out of scope, publish credit per conversion, touch and model, roll it up by channel and compare the models. Keep each window, weight and mapping as editable data. Nothing is guessed, dropped or defaulted to make a touch count or a conversion attribute.

## Verified by

- For every conversion under every published model, the credit on its touches plus its unattributed amount equals its approved value exactly, to each currency's approved rounding unit, including when the value does not divide evenly, with no credit created or lost.
- A conversion with no creditable touch carries its whole value as one explicit unattributed amount under each model, and per approved reporting currency each model's credited plus unattributed total equals the in-scope total, with other currencies translated or kept apart as approved.
- A touch is credited only when it is tied to the approved conversion entity under the approved identity rule, falls inside the approved lookback for its touch type with the approved handling at both edges, and precedes the conversion under the approved ordering and journey rule.
- Every touch is credited, given no credit with a reason, or set aside with a reason, and every conversion candidate is a conversion, out of scope with a reason or an exception; each source row sits in one place (a touch used by several conversions by its highest outcome) and the counts add up.
- A touch the approved eligibility policy withholds credit from, such as excluded traffic or a visit that yields to another touch, stays visible with its reason and the touches it yielded to, and is never removed silently.
- Credit under each model equals an independent recomputation of that model's approved weighting, and touches at the same instant are ordered by the approved stable rule, never by row order or run order.
- A rerun on unchanged input gives identical rows, and changing a window, weight, model parameter or mapping in its approved data changes the dependent credit with no logic edit, within the approved rule form.
- The roll-up at the approved level equals the per-touch credit summed to it, and the comparison shows each approved channel's credit under every model with its spread, a channel with no credit under a model reading zero.
- Each conversion carries its date on the approved reporting clock, so a conversion near a day boundary lands on its local date and every figure can be cut by period.
- Gross value, any adjustment and the split value sit beside each other under the approved value rule, and a conversion that fails the approved value rule is out of scope or reversed as approved, with its reason.
- A touch, conversion or adjustment arriving late changes only the conversions it affects, or leaves figures as of the approved date, as approved, and the difference is visible and never silent.
- Independent expected results for a labelled case set cover each applicable approved rule: edges, ties, uneven rounding, repeats, identity conflicts, excluded traffic, no touch, adjustments, currencies, late input, shared touches and models differing; an inapplicable case is stated as such.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements. Ask only about attribution semantics they leave open; sample data, existing code and any vendor tool's defaults are evidence, never policy. Profile touches and conversions first: touch types and channels, how identity keys behave, devices shared by several people, timestamp precision and clocks, repeated touches, refunds and late arrivals. Whether one touch may count for several conversions follows the approved journey rule; credit is decided per conversion, and each touch is accounted for once by its highest outcome. Keep every window, weight, mapping and rule as editable data and only the choice of model formulas as code. If no real data exists, build a small labelled fixture that carries every situation the approved rules name, and compute its expected results from the rules in a separate generator before any model exists. Before declaring complete, show the add-back and coverage for every model, the rule-as-data change, an identical rerun and the hand-calculated cases, and state what the fixture could not exercise.

### Compose

- capturing-requirements
- profiling-source-data
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, what counts as a conversion and which value is split: statuses, first or every one, gross or net of refunds, minimum value or zero-value and count conversions, whether a later refund restates credit, and the reporting currency, translation and rounding unit?
- If unresolved, how is a touch tied to who converted: person or account level, identity keys, whether other people's touches at the same account count, how a shared device is treated, whether a link covers earlier touches, and what an untied or conflicting touch gets?
- If unresolved, which touch types count (view-through, direct, referral, offline and where a date-only touch sits), whether direct or untagged visits earn credit or yield, how source, medium or campaign maps to channel, what an unmapped touch gets, and which level rolls up?
- If unresolved, what is the lookback per touch type, in elapsed time or calendar days, do both edges and a touch at the conversion instant count, how do repeated touches from one channel count, and does an earlier conversion end the journey for later ones?
- If unresolved, which models are published and with what parameters: time-decay half-life, position-based weights, a rule for one or two touches, and any other model the teams already use?
- If unresolved, how is a value that does not divide evenly rounded, which touch takes the leftover, and how are touches at the same instant ordered?
- If unresolved, which reporting clock and source time zone cut the results, which periods, what is the unattributed amount called, and does it appear among channels in roll-ups?
- If unresolved, which records are excluded or exceptions (test, internal, bot, consent-withheld, duplicate touches or conversions, other statuses) and how is each shown, and how is late data handled: restate the conversions affected, or fix by as-of?

### Guardrails

- Do not invent attribution policy: lookback, weights, conversion rules, channel mapping and tie order come from approved requirements or the user, and a vendor's defaults or another Intent's choices are not defaults.
- Do not let any model credit more or less than a conversion's value; keep the remainder, rounding and unattributed amount explicit and never round away or create value.
- Do not drop an untied, excluded, unmapped or out-of-window touch, or a conversion with no touch; show it with its reason.
- Do not guess who a touch belongs to; an untied or conflicting touch gets no credit and keeps its reason.
- Do not let row order, arrival order or a run clock decide a tie or a figure; same input must give same rows.
- Do not hardcode a window, weight, threshold, status list, mapping or time zone; read each from approved data or configuration.
- Do not count one touch's credit twice within a conversion, or treat sums of credit across conversions as counts of distinct touches.
- Do not carry personal data beyond the identifiers the Intent already holds into attribution outputs.
- Stop at attribution credit and comparison. Do not build identity, sessions, ingestion, spend or payback, incrementality or data-driven models, or push credit into ad platforms.
