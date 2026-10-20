---
id: logistics-lane-on-time-performance
title: Build lane-day on-time transport performance with open trips and exceptions shown as approved
trigger:
  - A TMS dashboard reports on-time performance by lane, but nobody can inspect how it is calculated or reproduce its figure.
  - Trips that were due but never reported an arrival, or lanes that ran nothing on a day, drop out of the on-time figure.
  - A late arrival lands on a different day than planners expect, or time zones and clock changes move a trip's day or verdict.
  - Repeated or corrected events, cancelled trips and trips with no usable plan change the rate with no stated reason.
description: Build, for each approved lane and day, the transport trips due and how many arrived on time, early or late or remain open or overdue, with an on-time rate and lateness derived from trip events under the user's approved rules, and every unmeasurable record listed once with a reason as approved.
pitch: A lane-by-day on-time view built from trip events, with open trips, quiet lanes and unmeasurable records shown as approved.
job_category: build
area: transformation
readiness: supported
function:
  - supply-chain-ops
industry:
  - logistics
domain_objects:
  - transport_trip
  - trip_event
  - lane
  - location
  - planned_arrival
  - on_time_verdict
  - lane_day
  - set_aside_record
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
  - Needs transport trips with a planned arrival and trip events with event times, already in the Domain.
  - Stops at lane-day punctuality; order-line in-full, freight cost, ETA forecasting and dwell are other outcomes.
  - A past as-of time reproduces only where event recorded times are kept; a rebuild restates it.
  - Exported files go to file-drop-to-bronze first.
related:
  - ops-otif
  - logistics-fleet-utilization
  - business-event-fact
  - effective-dated-business-rules
evidence:
  features:
    - capturing-requirements
    - generating-dbt-model
    - verifying
  evals: []
---

## Prompt

Build <lane_day_on_time_model> for the lane and day questions required in this Intent. Inspect approved requirements and source evidence, then settle the trip unit, lane identity, day basis and time zone, governing planned time, arrival event, on-time window, treatment of trips with no arrival, rate and empty-denominator behaviour, as-of time, report window, and duplicate and exception policies. Produce a per-trip verdict relation with exactly one approved status per due trip and a lane-by-day result with the approved status counts, rate and lateness for every approved lane and day, plus, on a completed run, a worklist and coverage accounting in which every landed trip record and event is counted or listed once with one reason. Materialize the outputs in the Intent's sandbox, derive independent expected results for the approved rules before comparing, and read back the published relations. Identify missing plans, events, locations or history that prevent an agreed question from being answered.

## Verified by

- The contract defines the trip unit, lane identity, day basis and time zone, planned time, arrival event, on-time window, no-arrival treatment, rate, empty-denominator value, as-of time, report window and duplicate and exception rules, each approved or inherited, none chosen by the agent.
- Each due trip has exactly one approved status, and on every lane-day the approved status counts add up to the due count; lane-day counts equal the per-trip statuses grouped to lane and day.
- A trip's day follows the approved basis and zone: a trip whose local date differs from its UTC date, and one planned on a clock-change day, land on the approved date and, where the sources carry offsets or zones, are judged by comparing instants, never wall-clock times.
- Window edges follow the approved allowances: an arrival exactly on each approved edge and one just outside it receive the status the approved rule gives, and changing an approved allowance value changes the split.
- A due trip with no arrival stays visible in the approved no-arrival states: one exactly on the approved boundary and one just past it get the approved states, and no such trip leaves the due count.
- The rate is formed on the row from the approved numerator and denominator, never as an average of other rates; a lane-day with an empty denominator shows the approved value beside its due and open counts.
- Rows follow the approved lane-day grid; where the grid is dense, a lane that ran nothing still has a row for every day with zero counts, not null.
- On a completed run every landed trip record and event is counted or listed once with one reason: landed trips equal counted plus each reason and landed events equal used plus each reason, with zero residue, and each reason is reproduced by a labelled case.
- Repeated, duplicate, corrected and late-recorded events and repeated trip ids resolve as approved; an event recorded after the as-of time, or one the approved rule does not treat as the arrival, changes no past status unless the approved rule says so.
- Lateness follows the approved measure, and each lane-day lateness figure the approved rule publishes is recomputed from the per-trip values.
- Published results equal values derived independently from the sources and approved rules by a method that does not reuse the model logic, covering each approved status, window edge, no-arrival boundary, empty-denominator and quiet-lane case.
- Outputs are materialized and read back on the Intent's platform; a missing plan, event or location that blocks a question is an input gap, and partial work is never reported complete; on an approved failing run the offending records and reasons are named.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain and sources. Inspect approved requirements, the trip records, trip events with their event and recorded times, the location zones and the lane list, and profile repeated ids, missing plans and late-recorded events before modelling. Use Ask first only for unresolved semantics; samples, a dashboard or existing SQL cannot approve policy. Resolve each trip and event to counted or one named reason first, admit events by the approved recorded-time rule, then judge each due trip from its approved planned time, arrival and as-of time, and publish the lane-day result over the approved grid. Fix independent expected values before writing model logic, including window edges, the no-arrival boundary, a clock-change day, a late-recorded arrival, tied duplicate trip ids, a quiet lane and an empty denominator. Label any synthetic evidence. Materialize, read back every relation, reconcile the accounting identities and independently recompute the rates. Report unsupported questions and untested required cases as incomplete verification.

### Compose

- capturing-requirements
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which movements are trips (leg, shipment or order; multi-leg movements; cancelled, test or rescheduled), what identifies a lane (ordered or unordered location pair, any mode or carrier split), and which lanes belong in the list?
- If unspecified, which day a trip belongs to (due, arrival or other), in which time zone and calendar, which report window and as-of time apply, does a later change restate a past as-of time, and are rows shown for every listed lane on every day or only active ones?
- If not approved, which planned time governs (original, latest agreed or in force at the as-of time), is it an instant or a window, who may move it, and may a move excuse a miss?
- If unresolved, which event is the arrival (arrived, delivered, proof of delivery), what links an event to a trip (trip, leg or stop id), which wins when events repeat or are corrected, how are duplicate, unknown-trip and unrecognised events treated, and which recorded time admits an event?
- If not established, what makes a trip on time, early or late (allowances in minutes or days, by customer or lane), does early count as on time, and how is lateness measured and summarised per lane-day?
- If still open, how is a due trip with no arrival treated (open versus overdue boundary, in or out of the rate, lateness measure) and is departure state shown?
- If unspecified, which statuses form the rate's numerator and denominator, which roll-ups beyond lane-day are needed, and what does an empty denominator show (null, zero or other) at what precision?
- If unresolved, how are repeated trip ids, cancelled trips, trips outside the window, unknown locations, lanes outside the list and missing or unparseable timestamps treated, and does an unplaceable record fail the run or stay listed?

### Guardrails

- Do not choose the trip unit, lane identity, day basis, planned-time basis, window, arrival event, no-arrival treatment, rate rule or population for the user, and take none from the data, a dashboard or common practice; the user may ask for alternatives or a recommendation.
- Never judge a trip on wall-clock time across a clock change or on a date assumed to be UTC; compare instants and place the day in the approved zone.
- Never let a due trip with no arrival leave the due count or default to on time; its no-arrival state follows the approved rule.
- Never average rates across lanes or days; recompute every figure from the approved components.
- Never drop, merge or default a record that cannot be placed; a missing plan, event or location is not zero, on time or late unless the approved semantics define it so.
- Never apply a later plan change, event, cancellation or resend to an earlier as-of time unless an approved restatement rule says so.
- Never treat a departed, delivered or other event as the arrival unless the approved arrival event names it.
- Stop at lane-day punctuality: do not compute freight cost or penalties, forecast arrivals, judge order lines in full, or change source trips and events, and keep sources read-only.
- Build success alone does not prove punctuality semantics; independent expected cases, accounting identities and read-back of every published relation must pass before claiming completed verification.
