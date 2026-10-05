---
id: service-ticket-sla
title: Track ticket SLA attainment and backlog aging outside the vendor dashboard
trigger:
  - The ticketing vendor's dashboard reports SLA met or breached, but nobody can check how its numbers are calculated.
  - Support leads need the open backlog by age as it stood on a past day, which the vendor dashboard cannot show.
  - SLA attainment must be reported by period, priority and team under the support team's own hours, pauses and reopen rules.
  - A breach must be traceable to the business hours, pauses and policy version that applied to that ticket.
description: Build per-ticket response and resolution SLA outcomes from ticket status, priority, team and reply history under approved targets, calendars, pauses, reopens and policy versions, then derive attainment by period, priority and team, a daily open-backlog age view and an exceptions list that accounts for every ticket, with an optional vendor comparison when ticket-level vendor results exist.
pitch: See how every SLA number is computed and how old the open backlog was on any past day.
job_category: build
area: transformation
readiness: supported
domain_objects:
  - ticket
  - sla_clock
  - sla_policy_version
  - business_calendar
  - state_interval
  - sla_exception
  - backlog_snapshot
  - reporting_period
works_with:
  platforms:
    - duckdb_local
  tools:
    - dbt
qualifiers:
  - Complete outcome assessed for duckdb_local only; the other four Studio targets remain unassessed.
  - Past backlog needs retained status, priority and team history; without it, backlog starts at the first captured day.
  - The vendor comparison needs the vendor's per-ticket, per-clock result; without that export it is left out.
related:
  - operational-state-duration
  - effective-dated-business-rules
  - metric-population-and-rollups
  - business-event-fact
  - dbt-snapshot-history
evidence:
  features:
    - capturing-requirements
    - designing
    - domain-modeling
    - applying-medallion-data-modelling
    - planning
    - executing-the-plan
    - generating-dbt-model
    - verifying
    - shipping
  evals: []
---

## Prompt

Build <per_ticket_sla_model> from <ticket_source> with one row per eligible ticket and SLA clock, then derive <attainment_model> by reporting period, priority and team, <backlog_model> as the open backlog by age bucket per day, and <exceptions_model> for every ticket and clock that cannot be scored or carries a flag. Inherit the Intent's sources, platform and approved requirements, and resolve only the SLA semantics they leave open: what starts, pauses, stops and reopens each clock, targets and policy versions, business hours, time zones and holidays, priority and team changes, exclusions, the as-of instant, the met boundary, attainment periods, and backlog membership and age. Keep policy values as data the user can change. Every eligible clock ends in one outcome or one explicit exception, attainment reconciles to ticket-level results, and no result depends on the session time zone. Rebuild past backlog only where history supports it. If ticket-level vendor results exist and a comparison is wanted, add <vendor_comparison_model> that reconciles and explains each difference.

## Verified by

- Tickets that are answered, paused, solved, reopened inside and outside the approved window and solved again have each clock start, pause, stop and resume exactly as the approved rules say, counting only approved business time.
- Tickets created just before and just after a policy change, and tickets whose priority or team changes while a clock runs, are scored against the target and calendar the approved rules select. A ticket with no applicable policy is an exception, not a default.
- Every eligible ticket and clock appears exactly once, as a scored outcome or as an exception. Source tickets reconcile to outcomes plus exceptions, with no duplicates and no silent drops.
- Merged, excluded, no-policy and missing-value tickets appear in the exceptions output with an approved reason, and none is counted as met or breached.
- A clock that finishes exactly at its target is scored by the approved met boundary. A clock still open at the as-of instant is classed and placed in a period by the approved rule, not by the run time.
- Daily backlog rows reflect each ticket's status, priority and team as they stood at the approved snapshot moment, with ages and buckets on the approved start, unit and edges. Where history is missing, the output says so instead of projecting today's state backward.
- Results are identical under any session time zone. Business hours, holidays and local-day windows follow each approved zone, including across daylight-saving changes, and fixed-length durations neither gain nor lose an hour.
- For every period, priority and team, met plus breached equals the scored clocks in the per-ticket output, the rate follows the approved formula including a zero total, and group totals add up to the ticket-level totals.
- Expected outcomes for the cases above are fixed from the approved rules, independently of the model logic, and every built output matches them.
- If the vendor comparison is in scope, every vendor result matches a ticket clock or is listed as unmatched, and each disagreement carries an approved explanation or stays visibly unexplained. Our results are never changed to match the vendor.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements. Ask only about SLA semantics they leave open; sample data, vendor settings and existing code are evidence, never policy. Profile the ticket source for status, priority, team and reply history, timestamps and time zones, and name any output the available history cannot support. Hold approved targets, policy versions, calendars, holidays, pause statuses, reopen windows and exclusions as data the user can change. Build state intervals from the history first, then compute each clock's elapsed business time, stop instant and breach instant once, and derive attainment, backlog, exceptions and any vendor comparison from those per-ticket results. Keep every instant in UTC and convert to a local zone only where an approved rule names one. Cover at-target clocks, reopens at and just past the window edge, policy-version switches, mid-clock priority and team changes, holidays and daylight-saving changes, with expected outcomes fixed from the approved rules. Reconcile tickets to outcomes and exceptions, and attainment to ticket-level results. Add the vendor comparison only when ticket-level vendor results exist and the user wants it.

### Compose

- capturing-requirements
- designing
- domain-modeling
- applying-medallion-data-modelling
- planning
- executing-the-plan
- generating-dbt-model
- verifying
- shipping

### Ask first

- If unresolved, which clocks are scored per ticket (first response, next response, resolution), which event starts each, which replies stop a response clock, which status stops resolution, and what happens when a ticket is solved with no qualifying reply?
- If unresolved, what are the response and resolution targets, do they vary by priority, team, customer or contract, which priority and team apply after a change while a clock runs, which policy elements are versioned and which instant selects the version?
- If unresolved, which business hours, time zones and holiday calendars apply to each ticket, which priorities run around the clock, which statuses pause which clock, and is time outside business hours excluded?
- If unresolved, which post-solve transitions count as a reopen, how long is the reopen window and in what unit and zone, and does a reopen resume the clock, start a new one or exclude the ticket?
- If unresolved, which tickets are excluded from which clock (merged, split, spam, deleted, test), and how are tickets with no applicable policy or unknown priority, team or status reported?
- If unresolved, what as-of instant judges open clocks, is elapsed exactly at target met, which period, zone and instant place a result, and how is the attainment rate defined, including a zero total?
- If unresolved, which statuses count as open backlog, at what moment and zone is each day taken, and what are the age start, unit and buckets?
- If a vendor comparison is wanted and ticket-level vendor results exist, how do they map to our clocks, how are missing results, our exclusions and open clocks shown, and which alternative rules may explain a disagreement?

### Guardrails

- Do not invent SLA policy. Targets, hours, calendars, pauses, versions and exclusions come from approved requirements or the user; values from another Intent or the vendor's settings are not defaults. Ask for a missing value without recommending one.
- Do not infer reopen semantics. Apply only the approved list of post-solve transitions and the approved effect of a reopen on each clock.
- Do not fabricate historical backlog. Without status, priority and team history a past backlog cannot be rebuilt; start from the first captured day, say so and never project today's state backward.
- Do not treat vendor results as ground truth. Never adjust our rules or results to agree with the vendor; report each disagreement with its approved explanation or as unexplained.
- Do not drop or default unscorable tickets. No policy, unknown priority or team, merged and excluded tickets stay visible as exceptions with reasons and are never counted as met or breached.
- Do not let the session time zone or local calendar arithmetic decide a result. Fixed-length durations are elapsed time between instants; local-day windows, hours and holidays use the approved zone, including across daylight-saving changes.
- Do not compute a clock separately in each output. Attainment, backlog aging, exceptions and any vendor comparison all derive from one set of per-ticket results.
- Keep Domain sources read-only and use the Intent's actual platform; do not modify source data to manufacture evidence.
- Stop at per-ticket outcomes, attainment, backlog aging, exceptions and the optional vendor comparison. Do not extend into agent productivity, CSAT or staffing models.
