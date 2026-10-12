---
id: readiness-gated-orchestration
title: Gate a consumer pipeline on upstream data readiness instead of a clock
trigger:
  - A consumer build runs at a fixed time and, on runs where an upstream load is late, builds on partial data without anyone noticing.
  - The schedule was pushed later to be safe, so in an ordinary period the consumers wait hours for no reason.
  - Several upstream teams land data at different times, and the build must start only when the feeds it needs are ready, and fail loudly when one misses its deadline.
description: Author a consumer pipeline as committed code that starts each period's build only when the required upstream feeds meet the approved readiness signal, handles missed, late and republished periods as the approved rules say, and fails explicitly without building when a required feed misses its deadline.
pitch: Start the build when the data is ready, not when the clock says so, and fail loudly instead of building on partial data.
job_category: build
area: orchestration
readiness: supported
domain_objects:
  - orchestration_pipeline
  - readiness_signal
  - schedule
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
  - Needs each required upstream feed to expose an approved readiness signal per period.
  - Assessed only as a Fabric pipeline on a local stand-in runtime; no listed target was run end to end.
  - Needs an orchestrator that can wait, check and fail a run; Studio authors one only for some targets today.
  - Checks readiness by polling within an approved window; event-triggered starts are out of scope.
related:
  - source-freshness-sla
  - fabric-data-pipeline-as-code
evidence:
  features:
    - generating-orchestration
    - evaluating-orchestration
    - running-orchestration-in-sandbox
    - documenting-orchestration
  evals: []
---

## Prompt

Author a pipeline named <pipeline_name> that builds <consumer_selection> for each period only once <required_feeds> meet the approved readiness signal for that period, treats <optional_feeds> as the approved policy says, checks readiness within <readiness_window> until <deadline>, and fails explicitly, naming the late feed, when the deadline passes. Commit the pipeline, its schedule and the definition of a pipeline-owned record of what was built as code, inherit the Intent's repository, platform, sources and approved requirements, and resolve only the semantics they leave open.

## Verified by

- A period's consumer build never starts before every required feed's approved readiness signal for that period holds, including any approved agreement check against the landed data; a feed that fails the check is reported not ready with the reason.
- A required feed not ready by the approved deadline produces an explicit failure whose message names each late feed, the period and the last status seen; no build runs for that period, and later periods are held or built as the approved rule says.
- A required feed that exposes no signal for a period is treated as not ready, so the period reaches its deadline rather than being skipped, unless the approved calendar excludes it.
- Pending periods are caught up, ordered and held back as the approved catch-up rule says; no period is skipped unless that rule allows it.
- A newer readiness signal for a period already built is handled as the approved restatement rule says, and every rebuild records the versions it replaced; a republished identical signal changes nothing.
- An optional feed not ready by its approved cut-off is handled and reported as the approved policy says, never as a clean success.
- A failed consumer build is recorded as failed with its cause, its period is not counted as built, and it is retried as the approved rule says.
- Overlapping runs are handled as the approved rule says, and no period is ever built by two runs at once.
- The pipeline-owned record of what was built holds, per period, the signal versions the gate accepted, when each feed was seen ready, the build start and end, the outcome and any flags, and survives rebuilds of the consumer models.
- Window, cut-off and deadline instants and the target period follow the approved business time zone and calendar, with ambiguous or skipped local times resolved as approved.
- The committed pipeline passes the validation its orchestrator offers; where deploying and running it is in scope, the behaviours above are shown in platform runs, otherwise they are shown against the committed definition's control flow and reported unproven on the platform.

## Agent guidance

### Instructions

Confirm which upstream feeds the consumer build reads and what each exposes when its load commits, and resolve any readiness semantics the Intent's approved requirements leave open. Define readiness per feed as the approved signal, derive the periods still to build from the approved calendar and the record of what was built rather than from the signals present, and keep that record where rebuilding the consumer models cannot change it. Make every failure path end the run as failed with its cause.

### Compose

- generating-orchestration
- evaluating-orchestration
- running-orchestration-in-sandbox
- documenting-orchestration

### Ask first

- If unresolved, ask which upstream feeds the consumer build needs, which are required and which optional, and how a build that proceeds without an optional feed must be reported.
- If unresolved, ask what signals that a feed has finished a period (a published completion record, the loader's own log, or a data condition), whether it must agree with the rows actually landed, and what a failed signal means.
- If unresolved, ask when checking starts, how often readiness is checked, the deadline for required feeds and any cut-off for optional ones, whether a feed ready exactly at the deadline counts, the time zone, and how ambiguous or skipped local times resolve.
- If unresolved, ask which period a run targets, which calendar defines periods, whether missed periods are caught up and in what order, and where the first period comes from on a fresh deployment.
- If unresolved, ask what happens to later periods when a period misses its deadline or its build fails, and when a failed build is retried.
- If unresolved, ask what a newer signal for a period already built means (which statuses count as a restatement), and whether overlapping runs wait, are skipped or fail.
- If unresolved, ask who is alerted when a deadline passes or a build fails, through which platform alert, and whether deploying and running the pipeline is in scope or only authoring and validating it.

### Guardrails

- Do not start a build on a schedule alone; a clock may only open the readiness window.
- Do not choose readiness signals, deadlines, cut-offs, check intervals, catch-up order, retry or restatement rules without approval.
- Do not skip a period because no feed has exposed a signal for it, unless the approved calendar excludes it.
- Do not report a run that proceeded without an optional feed, or that missed a deadline, as a clean success.
- Do not change or re-run the upstream feeds' own loads; they are outside this pipeline.
- Do not commit workspace, item or connection identifiers, credentials or an activated schedule.
- Do not claim runtime behaviour on the platform from static validation or a local stand-in.
