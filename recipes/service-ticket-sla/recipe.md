---
id: service-ticket-sla
title: Track ticket SLA attainment and backlog aging outside the vendor dashboard
trigger:
  - The ticketing vendor's dashboard reports SLA met or breached, but nobody can check how its numbers are calculated.
  - Support leads need the open backlog by age as it stood on a past day, which the vendor dashboard cannot show.
  - SLA attainment must be reported by period, priority and team under the support team's own hours, pauses and reopen rules.
  - The team wants each ticket's own SLA result compared with the vendor's flag, with a reason for every disagreement.
description: Build per-ticket response and resolution SLA outcomes from ticket status, priority, team and reply history under user-approved targets, calendars, pauses, reopens and policy versions, then derive attainment by period, priority and team, a daily open-backlog age view, an exceptions list that reconciles every ticket, and an optional ticket-level vendor comparison.
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
  - vendor_sla_flag
works_with:
  platforms:
    - duckdb_local
  tools:
    - dbt
qualifiers:
  - Complete outcome assessed for duckdb_local only; the other four Studio targets remain unassessed.
  - Assessed with a labelled synthetic 49-ticket fixture and synthetic vendor flags; no real ticket source was read.
  - Past backlog is rebuilt from status, priority and team history; without that history it cannot be reconstructed.
  - No fixture ticket had the lowest priority or one of the three teams; their targets and team hours are unassessed.
  - Only targets were versioned; other policy dates and the priority and team seeds go unread, and 24x7 is a SQL literal.
  - Data tests on frozen seeds only, no unit tests, evaluator skipped; solve-then-close and time zone cases were probes.
  - Vendor flags existed only for stopped clocks; the 24x7 alternative subtracted business-time pauses, not wall-clock.
  - The minute-level business-time expansion ran at fixture scale only; production ticket volume is unassessed.
  - Review was self-review only; equality tests joined on keys, so only uniqueness tests caught duplicate rows.
  - Mart equality tests were written with the SQL, not first; fail-ability came from later deliberate breaks.
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

Build <per_ticket_sla_model> from <ticket_source> with one row per scored ticket and clock, then derive <attainment_model> by period, priority and team, <backlog_model> as the open backlog by age bucket per day, <exceptions_model> for every ticket and clock that cannot be scored or needs a flag, and, only if the vendor's per-ticket flag exists in <vendor_flag_source>, <vendor_comparison_model> per clock. Settle from approved requirements, never supply them: the clocks and what starts and stops each, targets, business hours, time zones, holidays, pause statuses, what a reopen is, its window and effect, which priority and team apply after a change, policy versioning, exclusions, the as-of instant, the met boundary, attainment period and rate, backlog membership, snapshot moment, age and buckets, and any vendor alternatives. Keep policy values in seeds, not SQL. Before model SQL, freeze an approved fixture covering the normal lifecycle and every edge case, with expected results computed independently of the models. Store instants in UTC, never let the session zone decide a result, reconcile every ticket and clock, build under several session zones and report what was not assessed.

## Verified by

- The approved Requirement cites the user's own answer for every clock, calendar, pause, reopen, priority, team, versioning, exclusion, as-of, met-boundary, period, rate, backlog and vendor rule. No rule came from an agent default or from a question that offered a recommended option.
- A hard-coded rule inventory lists every SQL rule, and a grep of the compiled models maps every string, date and number literal to it or to a seed column. Every cited line exists, every user-owned seed column is read by the SQL, and no priority, team or status the policy names is a literal.
- The frozen fixture holds the normal lifecycle through each terminal status in the user's approved list, and a ticket for every priority, team, time zone, holiday calendar, listed status and reply type in the user's policy, or the gap is a stated limitation.
- Each scenario's expected value differs under the approved rule and the likely wrong rule, covering at-target clocks, a reopen exactly at the window edge and one just past it, tickets each side of a policy switch, clocks open at the as-of instant past and within target, and backlog age-bucket edges.
- Expected seeds come from a committed generator that reads only the fixture and policy CSVs, imports no database library, holds no ticket ids or fallback values and reproduces every committed expected seed exactly; an independent recomputation reports 0 differences on every output and row count.
- Every equality test compares multisets (equal row counts and EXCEPT ALL empty both ways) and every model has a grain-uniqueness test on its business key; duplicating one mart row on a database copy makes the equality test itself fail, not only the unique test.
- Reconciliation starts from all source ticket and clock pairs and full-outer-joins results and scoring exceptions; deleting, duplicating or orphaning a row and scoring an excluded clock each fail a committed test. Each reason is in its approved class; accepted_values covers every reason and class.
- A fixture ticket moves from the solve to each post-solve status in the user's list, and its result and reopen count follow the approved rule. An open clock past target lands in the period the approved placement rule names, and its candidate placement instants fall in different periods.
- The tagged dbt build gives identical marts with no session time zone set and under a non-UTC zone with daylight saving; a reopen exactly at the approved window edge across a DST change is scored as the approved unit and zone define. Every instant column loads as timestamp with time zone.
- For every test the log shows a failing run before the passing one, or a recorded deliberate break failing with the expected count. run_results.json of the tagged build lists every planned test by name, all executed, with the node count the plan states.
- If the vendor comparison is in scope, each approved alternative has a case only it explains (under ordered first match, one failing every earlier alternative), plus agreement and missing-flag cases, and disabling one alternative changes only its own case. Our result is never forced to match.
- A Certification artifact exists on the branch at the certified revision before any ship step, with a verdict, a gate table recording unavailable gates as skips, self-review stated as such, and Limitations that the PR body repeats in full.

## Agent guidance

### Instructions

Confirm the ticket source keeps status, priority and team history and typed reply events with timestamps; if not, state which questions cannot be answered and leave those outputs out. If there is no real source, ask whether a labelled synthetic fixture may be built and ask for every policy value instead of inventing one. Ask each open semantic in Ask first as its own question with no recommended option, map every answer to a requirement clause, and make any later change a new revision the user approves. Hold the approved as-of instant as data, never the run clock; for a fixture it falls after every fixture event. Before model SQL, freeze the approved fixture, a rule-to-ticket coverage table, the hard-coded rule inventory and expected seeds from a committed standalone generator. Declare column_types for every seed column, write every instant with an offset and tag every seed, model and test with one selector. Build staging views, a state-interval model, one clock model that computes elapsed time, clock stop and breach instant once for every mart, then the marts. Write each test and record its failure before the SQL it tests. Run dbt parse and the tagged build before each commit. Run heavy probes singly on a database copy outside the build sandbox, after pushing. After any context compaction, re-read the plan, approvals and frozen commits. Quote evidence only from commands run in the same turn, and write the Certification artifact with honest limitations before shipping.

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

- If unresolved, which clocks are scored per ticket (first response, next response, resolution), which event starts each, which reply types and authors stop the response clock, which status stops resolution, first or final solve after a reopen, and what if a ticket is solved with no qualifying reply?
- If unresolved, what are the response and resolution targets per priority, do they vary by team, customer or contract, which priority sets a target after a change or while a clock runs, which policy elements are versioned, which instant picks the version, and what happens before the first version?
- If unresolved, which hours and days apply per priority, team or customer, which priorities run around the clock or through holidays, whose IANA zone and holiday calendar set each ticket's hours, do hours follow each interval, which statuses pause which clock, and is off-hours pause subtracted?
- If unresolved, which post-solve transitions are a reopen or mean done, how long is the window, in 24-hour periods or local days in whose zone, is the edge inclusive, does a reopen resume the clock, start one or exclude the ticket, does the gap count, is response restarted, what does a late one do?
- If unresolved, which tickets are excluded and from which clock (merged, split, spam, deleted, closed unsolved, test), does a merge survivor take on merged events, how are no-policy, unknown and missing values handled, even for part of its life, and which reasons remove a clock or only flag it?
- If unresolved, what as-of instant judges open clocks, are those within target left out, counted or shown apart, is elapsed at target met, at what precision, which period, zone and instant place a result, which priority and team label it, what is the rate with a zero total, and may periods restate?
- If unresolved, which statuses count as open backlog, at what moment and zone is each day taken, over which range, which priority and team label a row, are empty groups shown, do excluded or undated tickets appear, and what are the age start, unit (24 hours or local days), rounding and buckets?
- If unresolved, can the vendor's per-ticket met or breached flag be exported per clock, how are a missing flag, our exclusion, an open clock and an agreement reported, are disagreements explained by recomputing with alternative rules, which, singly or combined, first or every match, in what order?

### Guardrails

- Values a user chose in another Intent are not defaults. Never ask a catch-all question, mark an option recommended or put a sample value in a question. Ask for a missing value instead of inventing it.
- Never infer which post-solve transitions are reopens or how a reopen affects the clock; apply only the approved list and rule. Compute the clock stop, approved reopen exclusions and breach instant once, on the clock the approved hours set for each interval, and reuse them in every mart.
- Store every instant as UTC timestamptz with explicit UTC casts; convert to a local zone only where an approved rule names one. Never let the session time zone decide a result: use epoch seconds for fixed-length durations and explicit conversion to the approved zone for local-calendar windows.
- Never copy, export or refresh expected seeds from model output, reorder approved rules to fit values, or default unknown values. A self-check reads the frozen fixture and seeds with git show, writes to a temp folder and compares parsed rows on values.
- The fixture and expected seeds are frozen after approval. An added ticket needs the user's approval and an independently regenerated expected set; keep line endings, quoting and row order so the diff from the frozen commit shows only approved rows.
- Keep user-owned values in seeds, SQL rules in the inventory. SQL reads every user-owned seed column, such as an effective date or which priorities run around the clock, and never names a policy priority, team or status as a literal. A changed grain, column, reason or exclusion needs a new revision.
- Keep Domain sources read-only and write the fixture and models only to the sandbox's own database. Run heavy rebuilds and probes one at a time on a database copy outside the build sandbox, and size the per-minute expansion before running at real volume.
- Use only installed test macros or singular tests, record an unavailable gate such as a project evaluator without packages as a skip, never a pass, and drop relations left by abandoned builds.
- Tick a plan step only with honest text about what happened, quote evidence in full from commands run in the same turn, and list every deviation, probe-only case and untested path under Limitations in both the Certification artifact and the PR body.
- Without status history a past backlog cannot be rebuilt: capture snapshots from now on and say so. Stop at per-ticket outcomes, attainment, backlog aging, exceptions and the vendor comparison; build no agent productivity, CSAT or staffing model. Skip the vendor comparison if no flag export exists.
