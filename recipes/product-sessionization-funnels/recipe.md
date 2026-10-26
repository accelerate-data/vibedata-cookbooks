---
id: product-sessionization-funnels
title: Sessionize event streams and build reproducible funnels from batch exports
trigger:
  - Product analytics numbers cannot be reproduced outside the vendor's screen, and nobody can say why two conversion figures differ.
  - Session or conversion counts change between runs or when a late or overlapping export batch arrives.
  - Teams define a visit or a conversion differently, and a funnel step cannot be traced back to events.
description: Resolve landed batch event exports to identities and visits, build a funnel from configured steps, account for every event, and reproduce a reference figure with each difference attributed to a named cause.
pitch: Rebuild visits and funnels from landed event exports so every conversion figure traces to events and differences from the vendor are explained.
job_category: build
area: transformation
readiness: supported
function:
  - cross-functional
domain_objects:
  - product_event
  - identity
  - visit
  - funnel
  - funnel_step
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
  - Batch-only, reading landed export tables; streaming or real-time sessions are out of scope.
  - Expects the export already landed as tables; ingesting the export is a separate Recipe.
  - Single linear funnel path; branching, optional steps, experiments and attribution are out of scope.
  - Consumes an approved identity map; person resolution across systems belongs to identity-golden-record-crosswalk.
  - Event identity beyond delivered copies belongs to business-event-fact.
  - Edge handling needs each batch's covered range; without it, export-edge completeness is unproven.
  - Complete outcome assessed for duckdb_local only; the other four Studio targets remain unassessed.
related:
  - file-drop-to-bronze
  - business-event-fact
  - identity-golden-record-crosswalk
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

Build <visit_model> and <funnel_model> from the landed batch event exports for the product analytics questions in this Intent. Resolve each event to one identity where the approved rule can, group events into visits by inactivity, and compute reach, step conversion and drop-off for the funnel steps held in configuration, so every figure can be reproduced outside the vendor's tool. Inspect approved requirements and the landed event tables before settling identity, visit ownership and boundaries, the event clock, duplicate and late-batch handling, excluded traffic, step order, unit, conversion window and reporting period. Keep every rule as editable configuration. Account for every event as counted or set aside with a reason, never let visits of one visit owner overlap, and, where <reference_figure> is given, publish a reconciliation in which each difference is attributed to a named cause instead of tuned away.

## Verified by

- Every delivered event row is in exactly one visit, set aside with a reason, held outside visits under an approved disposition, or removed under the approved erasure rule; these populations reconcile to the delivered rows, and the event count follows the approved duplicate rule.
- Each event resolves to an identity under the approved rule; events that rule cannot attribute, and events with no usable identity or time, are listed with reasons and never guessed.
- No two visits of one approved visit owner overlap, and boundaries follow the approved gap, boundary side and any other approved cut rule.
- Events the approved rule says do not keep a visit alive change no visit start, end or count, and none opens a visit; one outside every visit is set aside with a reason or held under another approved disposition, and is listed.
- Late, re-delivered, conflicting and skewed events follow the approved clock and rules, the same batches in give the same visits out, and published periods follow the approved restatement rule when late data or a changed rule arrives.
- Visits near the export edge follow the approved treatment; where held open, each is marked and the mark clears only when later data settles it.
- Funnel steps, their order, the gap and the window are read from configuration; within the approved rule form, changing a configured value changes the dependent figures without editing model logic.
- Each step's reach equals an independent recomputation from the ordered events under the approved order, unit, repeat and window rules, including where those rules distinguish order or window end.
- A configured step or source that matches no events is reported, never read as zero reach, and outputs show only the approved identifiers.
- Each published rate equals its two published counts under the approved definitions and zero-denominator handling; periods follow the approved time zone, week start, grain and placing event, with an empty period shown or omitted as approved.
- Excluded and unusable events stay visible with reasons, recoverable for comparison within approved retention, and appear in the funnel only where approved.
- Where a reference figure is given, per step and period the per-cause differences, applied in the approved order, sum exactly to the reference minus the published figure; each cause is a named approved rule difference, and any residual is shown as unexplained and never folded into a cause.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain and landed event tables. Inspect approved requirements and profile the events first: identifier coverage, duplicate keys, batch overlap and covered ranges, arrival order against event time, clock skew, sources and event names, background or system events, flagged traffic. Use Ask first only for unresolved semantics. Keep every business rule as editable configuration read by the models, never a literal in logic. Fix independent expected visits and funnel counts before implementation and compare to them, with cases at each gap, window and period boundary, each identity path, each late or duplicate path, each exclusion, out-of-order steps and repeat attempts. When no real export exists, use a small synthetic one and label it synthetic everywhere. Publish visits, an event-level accounting relation, the funnel and, where a reference figure is given, a reconciliation that decomposes the difference in a stated order whose per-cause changes sum exactly to it. Materialize in the Intent sandbox, read the outputs back and rerun. Report untested policy branches and any unexplained residual as incomplete verification.

### Compose

- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, how are events resolved to one identity: which ids, how anonymous activity links to an account and in which direction, whether a later merge relinks history, and how shared devices, several devices and unusable identities are treated?
- If unspecified, what owns a visit (identity, device or platform), what is the inactivity gap, which side of it starts a new visit, which events keep a visit alive and where do those outside every visit go, and do any other rules cut a visit?
- If unresolved, which clock orders events, how are missing times, ties, skew and a batch cutoff handled, how are the export edge and expected batches known, and how is a visit near the edge treated?
- If unresolved, which sources and event names feed the steps, which key identifies a delivered copy, how are re-delivered, conflicting and late data handled, and are published periods restated, from all history or an effective date?
- If unresolved, which traffic, test or erased identities leave the population, who owns that rule, where do excluded rows go and how long are they retained, and which identifiers may outputs show?
- If unspecified, what are the funnel steps and conditions, what happens when a step matches no events, is order strict, loose or free, what is the unit, how are repeats and re-entry counted, and how are rates and zero denominators defined?
- If unspecified, what starts the conversion window, how long is it, is its end inclusive, is it elapsed time or calendar days, and which time zone, week start, period grain and placing event define periods?
- If a reference figure is given, which figure, period and definitions does it use, and how should differences be classified and ordered?

### Guardrails

- Never guess identity. An event the approved rule cannot attribute stays listed as unattributed and is not assigned to the nearest or latest identity.
- Do not write the gap, window, steps, event lists, exclusion rules or time zone into model logic; within the approved rule form, they stay editable configuration.
- Do not drop events silently. Duplicate, late, excluded and unusable events are counted or set aside with a reason, and joins must not lose them.
- Do not let delivery or batch order decide visits when the approved clock says otherwise, and keep tie-breaking deterministic.
- Do not let events outside the approved keep-alive rule extend or open a visit, and do not close or drop a visit at the export edge unless approved; mark it instead.
- Do not tune any rule, configuration or reference data so the figures match the vendor's, and never use the vendor figure as the expected result.
- Count each step only in the approved unit, never present one unit's counts as another's, and do not add reach across periods or attempts unless approved.
- Do not place events in periods by the UTC day or the export's own clock unless that is the approved zone, and do not split a visit at midnight unless approved.
- Do not claim streaming or real-time sessions, and do not ingest the export here; hand ingestion to its own Recipe.
- Keep synthetic data labelled and never mixed with real figures.
