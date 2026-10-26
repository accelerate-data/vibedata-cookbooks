---
id: readiness-gated-orchestration
title: Gate a consumer pipeline on upstream data readiness instead of a clock
trigger:
  - A consumer build runs at a fixed time and, on runs where an upstream load is late, builds on partial data without anyone noticing.
  - The schedule was pushed later to be safe, so in an ordinary period the consumers wait hours for no reason.
  - Several upstream teams land data at different times, and the build must start only when the feeds it needs are ready, and fail loudly when one misses its deadline.
description: Author a consumer pipeline as committed code that starts each period's build only when the required upstream feeds meet the approved readiness signal, handles missed, late and restated periods as the approved rules say, and fails explicitly without building when a required feed misses its deadline.
pitch: Start the build when the data is ready, not when the clock says so, and fail loudly instead of building on partial data.
job_category: build
area: orchestration
readiness: supported
function:
  - cross-functional
domain_objects:
  - orchestration_pipeline
  - readiness_signal
  - schedule
works_with:
  platforms:
    - motherduck
    - fabric_lakehouse
    - fabric_warehouse
  tools:
    - dbt
qualifiers:
  - Needs each required upstream feed to expose an approved readiness signal per period.
  - Not yet assessed end to end on any listed target.
  - Needs an orchestrator that can wait for readiness, check it and fail a run.
  - Studio's orchestration templates do not yet include a readiness gate for every listed target.
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

Author a pipeline named <pipeline_name> that builds <consumer_selection> for each period only once <required_feeds> meet the approved readiness signal for that period, treats <optional_feeds> as the approved policy says, checks readiness within <readiness_window> until <deadline>, and fails explicitly, naming the late feed, when the deadline passes. Commit the pipeline, its schedule and every execution item this Recipe authors as code, inherit the Intent's repository, platform, sources and approved requirements, and resolve only the semantics they leave open.

## Verified by

- A period's consumer build never starts before every required feed's approved readiness signal for that period holds, including any approved agreement check against the landed data; a feed that fails the check is reported not ready with the reason.
- A required feed not ready by the approved deadline produces an explicit failure whose message names each late feed, the period and the last status seen; no build runs for that period, and later periods are held or built as the approved rule says.
- A required feed that exposes no signal for a period is treated as not ready, so the period reaches its deadline rather than being skipped, unless the approved calendar excludes it.
- Pending periods are caught up, ordered and held back as the approved catch-up rule says; no period is skipped unless that rule allows it.
- Where automatic restatement is required, a change to a built period is detected through the approved change identifier and rebuilt as the approved rule says, recording the identifiers replaced; without such an identifier, automatic restatement detection is reported unproven.
- An optional feed not ready by its approved cut-off is handled as the approved policy says and reported with the flag it names, never as an unflagged success.
- A failed consumer build is reported failed with its cause, is not counted as built, and is retried as the approved rule says; overlapping runs follow the approved rule and never build one period twice at once.
- A record of what was built, kept where the approved rule says, shows per period the readiness evidence the gate accepted (with the approved change identifiers where they exist), the outcome and any flags, and is not changed by rebuilding the consumer models.
- Window, cut-off and deadline instants and the target period follow the approved business time zone and calendar, with ambiguous or skipped local times resolved as approved.
- Everything this Recipe authors is committed; any other workload, signal or binding it needs exists and resolves, or is reported as a blocker to execution, and listing it as a deployment prerequisite does not count as verification.
- Each deadline miss and build failure ends the run failed with a message naming its cause, routed to the approved alert with no connection committed; delivery is reported unproven unless deploying and running it is in scope and a platform run shows it.
- The pipeline passes its orchestrator's validation; where deploying and running it is in scope the behaviours above are shown in platform runs, otherwise against the committed definition under the orchestrator's documented semantics, and reported unproven on the platform.

## Agent guidance

### Instructions

Confirm which upstream feeds the consumer build reads, what each exposes when its load commits, and that each workload the pipeline invokes is either authored here or an approved existing one whose reference resolves, and resolve any readiness semantics the Intent's approved requirements leave open. Define readiness per feed as the approved signal, derive the periods still to build from the approved calendar and the record of what was built rather than from the signals present, and keep that record where the approved rule says, out of reach of the consumer models' rebuilds. Make every failure path end the run as failed with its cause.

### Compose

- generating-orchestration
- evaluating-orchestration
- running-orchestration-in-sandbox
- documenting-orchestration

### Ask first

- If unresolved, ask which upstream feeds the consumer build needs, which are required and which optional, which workloads it invokes already exist, and how a build that proceeds without an optional feed must be reported.
- If unresolved, ask what signals that a feed has finished a period (a published completion record, the loader's own log, or a data condition), whether it must agree with the rows actually landed, and what a failed signal means.
- If unresolved, ask when checking starts, how often readiness is checked, the deadline for required feeds and any cut-off for optional ones, whether a feed ready exactly at the deadline counts, the time zone, and how ambiguous or skipped local times resolve.
- If unresolved, ask which period a run targets, which calendar defines periods, whether missed periods are caught up and in what order, where the first period comes from on a fresh deployment, and where the record of what was built is kept.
- If unresolved, ask what happens to later periods when a period misses its deadline or its build fails, and when a failed build is retried.
- If unresolved, ask whether a change to a period already built must trigger a rebuild, which observable change identifier marks it (a publication revision, load ID, source snapshot or reliable fingerprint) and which statuses count, and whether overlapping runs wait, are skipped or fail.
- If unresolved, ask who is alerted when a deadline passes or a build fails, through which platform alert, and whether deploying and running the pipeline is in scope or only authoring and validating it.

### Guardrails

- Do not start a build on a schedule alone; a clock may only open the readiness window.
- Do not choose readiness signals, deadlines, cut-offs, check intervals, catch-up order, retry or restatement rules without approval.
- Do not invent version lineage; where no approved change identifier exists, report that automatic restatement detection cannot be proven.
- Do not skip a period because no feed has exposed a signal for it, unless the approved calendar excludes it.
- Do not report a run that proceeded without an optional feed as an unflagged success, or a run that missed a deadline as a success.
- Do not change or re-run the upstream feeds' own loads; they are outside this pipeline.
- Do not treat a feed for which the approved signal does not exist yet, or a missing or unfinished workload or binding, as resolved; it blocks execution, and listing it as a deployment prerequisite is not verification.
- Do not commit workspace, item or connection identifiers, credentials or an activated schedule.
- Do not claim runtime behaviour on the platform from static validation or a local stand-in.
