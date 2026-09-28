---
id: operational-state-duration
title: Build state durations by entity, location and reporting period
trigger:
  - Waiting, idle, available or busy time must be measured by site or zone and hour from operational event histories.
  - State and location change independently, leaving reports unable to explain where an entity spent its time.
  - Vehicle or equipment events have missing closes or observation gaps that could inflate operational duration totals.
description: Build evidence-backed state and location intervals, split them across agreed reporting boundaries, and reconcile durations with explicit unknown periods, missing closes and source lineage.
pitch: Explain how long each entity spent in a state and where, without inventing locations or filling unknown time with activity.
job_category: build
area: transformation
readiness: supported
domain_objects:
  - operational_event
  - entity
  - state_interval
  - location
  - reporting_period
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

Build <duration_model> from operational events to answer the analytical questions and location and time breakdowns required in this Intent. Inspect approved requirements and source evidence, then settle entity and event identity, event meaning, ordering, state and location validity, interval ends, observation coverage and reporting boundaries. Carry state and location independently only while evidence supports each value. Produce traceable intervals and durations by entity, state, applicable location and agreed reporting grain, with explicit unknown periods and missing-close status. Split intervals across required boundaries without duplication; expose ambiguous, unmapped and excluded records with reasons. Materialize the outputs in the Intent's sandbox. Verify independent location-only, state-only, hour/day crossing, equal-timestamp, missing-close and unobserved-gap cases, and reconcile duration at every required grain. Distinguish operational evidence from labelled synthetic demonstrations and report missing inputs that prevent an agreed question from being answered.

## Verified by

- The contract defines entity/event keys, event meaning, ordered identity, state and location validity, interval boundary convention, observation window, missing-close and gap policies, duration units, reporting time zone and output grains.
- Every source event has an auditable disposition and reason; disposition counts close to scoped inputs. Intervals retain contributing event identities, separate state/location evidence and validity limits, end reason, and links to their reporting-period fragments.
- Independent state-only and location-only changes update the relevant attribute while retaining the other only when valid. Unknown, unmapped or expired location stays explicit; a last known site cannot silently supply unsupported location duration.
- A labelled synthetic continuous-observation case has waiting at A at 23:50, location B at 00:10, busy at 00:25 and explicit close at 00:40. Expected durations are waiting/A 20, waiting/B 15 and busy/B 15 minutes; state-only or location-only interval logic fails.
- In that fixed-offset fixture, waiting/A splits into 10 minutes before midnight and 10 after; the two hour/day buckets total 10 and 40 minutes. All required grains reconcile to 50 minutes, with no duplicate boundary instant or lost fragment.
- Independent gap and missing-close cases follow approved validity limits and cutoff rules. A labelled 10-minute unobserved gap with no valid state/location evidence yields 10 minutes unknown, never idle/available or a guessed site; open ends remain identifiable.
- Equal timestamps, duplicate deliveries, out-of-order and late events follow approved identity, ordering and correction rules. Independent expectations prove stable results under input reordering; unresolved conflicting ties stay visible, with no arbitrary winner.
- Boundary cases cover before, at and after interval/reporting edges, zero-length intervals, window clipping and applicable daylight-saving transitions. Durations use elapsed instants; repeated local hours stay distinct and local days are not assumed to be 24 hours.
- Fragments have the agreed unique grain and nonnegative duration without overlap within each entity/state scope. Known, partially known, unknown and approved excluded periods partition the declared observation window; overlaps or uncovered time fail reconciliation.
- Independent elapsed-time totals reconcile intervals, fragments and every required entity/state/location/time rollup within approved precision. Unknown and excluded time remain visible; mapping joins cannot multiply duration or remove unmatched records.
- Each agreed question and breakdown is supported or has an explicit gap tied to missing attributes, history, mappings or relationships. Expected values are fixed independently of model SQL; observed links, approved allocations and synthetic examples are distinguished.
- dbt checks and independent acceptance queries pass on the actual Intent platform after materialization and rerun; every output is read back. The report records revision, commands, exits, interval/fragment counts, duration totals and unresolved exceptions.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain and sources. Inspect approved requirements, event schemas, entity keys, source sequence, state/location semantics and coverage evidence. Profile duplicates, ties, missing values, gaps and mapping cardinality. Use Ask first only for unresolved decisions; samples or existing code cannot authorize policy. Record event grain, independent attribute validity, ordering, interval ends, observation window, gap/cutoff rules, reporting time zone, grains and precision. Distinguish absent updates from explicit clears. Stop an unsupported breakdown and report its missing evidence. Design interval, boundary-fragment and audit outputs with source lineage and unknown statuses; keep independent state scopes explicit. Fix expected results before model SQL, including both one-attribute changes, midnight, gaps, open ends, ties and applicable clock changes. Label synthetic fixtures; cite observed relationships and approved allocation rules. Implement with the composed skills and current target's dialect and sandbox guidance. Split on state, location, validity and reporting boundaries. Materialize, read back every output, rerun and independently reconcile event dispositions and elapsed-time partitions at all required grains. Keep Domain sources read-only; changed-data fixtures need an approved writable area. Record evidence and report required untested cases as incomplete verification.

### Compose

- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If requirements do not settle them, which analytical questions, entity/state scopes, location levels, reporting grains and observation windows must the duration model support?
- If source semantics are unresolved, do events assert state, location or both, which keys and sequence establish identity/order, and does an absent or null attribute mean no update, unknown or an explicit clear?
- If not approved, what evidence permits each attribute to persist, what closes an interval, what marks observation loss or expiry, and how should missing closes, initial unknowns and open-ended intervals be bounded and labelled?
- If still open, how should duplicate deliveries, equal-timestamp changes, conflicting ties, late events and corrections be resolved, and which cases must remain ambiguous or excluded?
- If unspecified, which time zone, daylight-saving rules, interval inclusivity, elapsed-time units, precision and reporting cutoffs apply, and how must unknown and excluded time appear in totals?
- If required spatial meaning is unresolved, which source relationships establish site or zone, when are mappings valid, and are any allocations explicitly approved and distinguishable from observed location?

### Guardrails

- Do not infer idle, available or any other state from silence. Do not carry state or location across an observation gap or past a validity limit without supporting evidence and an approved rule.
- Do not replace missing spatial evidence with a convenient garage/site, hash-selected location or synthetic pattern and claim zone-level operational results. Unknown locations remain explicit even when state is known.
- Do not use only state changes or only location changes to define intervals. Preserve independent changes, explicit clears and separate validity limits; event ordering must not invent unobserved transitions.
- Do not discard materially distinct events to resolve equal timestamps or make duration totals pass. Preserve unresolved conflicts and source lineage; approved tie rules must be reproducible.
- Do not count an open interval indefinitely or double-count boundary instants. A reporting cutoff bounds calculation but is not evidence of an observed close or uninterrupted coverage.
- Do not equate a labelled synthetic fixture with observed operational history. Preserve provenance for observed relationships, approved allocations and demonstrations, including in analytical outputs.
- This is operational duration modelling, not product-session or funnel analysis. Do not create streaming infrastructure or mandate optional attributes unrelated to the agreed questions.
- Use the actual Intent platform and provided sandbox. Do not substitute another engine, synthesize an absent sandbox or mutate Domain sources to manufacture evidence.
- Build success alone does not prove duration semantics. Required independent cases, partition and rollup reconciliation, and output read-back must pass before claiming completed verification.
