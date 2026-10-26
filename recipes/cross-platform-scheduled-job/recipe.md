---
id: cross-platform-scheduled-job
title: Convert a scheduled data job to another platform without changing its required behavior
trigger:
  - A scheduled load-and-build job has to move to another platform, and nobody has written down what it must keep doing.
  - An earlier move changed the local hour a job ran, or ran it twice or not at all around a clock change.
  - A failure that used to stop later steps, skip a run or notify someone now passes silently on the new platform.
description: Record the behavior a scheduled data job must keep, rebuild it as committed code on another platform, and show for each required behavior whether it holds, changed, cannot be kept, or not verifiable, with the evidence and any replacement stated.
pitch: Move a scheduled job to a new platform and get a per-behavior answer on what held and what could not.
job_category: cross-platform
area: orchestration
readiness: supported
function:
  - cross-functional
domain_objects:
  - scheduled_job
  - behavior_contract
  - schedule
  - parity_verdict
works_with:
  platforms:
    - motherduck
    - fabric_lakehouse
    - fabric_warehouse
  tools:
    - dlt
    - dbt
qualifiers:
  - Not yet assessed end to end on any listed target.
  - Needs the original job's definition or recorded runs; behavior it never shows is reported unproven.
  - Reports each behavior the target's scheduler or runtime cannot express; it does not add the missing capability.
  - Authors the converted job only; deployment and retiring the original are separate decisions.
  - Converting the workload code the job calls belongs to the Recipe for that source.
  - Readiness gating on upstream feeds belongs to readiness-gated-orchestration; here it is carried or reported.
related:
  - motherduck-flight-scheduling
  - fabric-data-pipeline-as-code
  - readiness-gated-orchestration
evidence:
  features:
    - generating-orchestration
    - evaluating-orchestration
    - running-orchestration-in-sandbox
    - documenting-orchestration
  evals: []
---

## Prompt

Convert the scheduled job <job_name>, run today by <source_scheduler>, to <target_platform> as committed code. Inherit the Intent's repository, platform, Domain, job definition and approved requirements, and resolve only the semantics they leave open: which behaviors are required, how each is judged unchanged, and what happens to one the target cannot express. Record the behavior the job must keep from its definition and recorded runs: its steps (loads, builds or others) and their order, schedule and time zone, failure and skip rules, retries, overlapping runs, runs with nothing new, run-scoped values, notification and outputs. Rebuild it on the target, give every required behavior one verdict (holds, changed with the difference, cannot be kept with its replacement, or not verifiable here) with its evidence, show held behaviors by the same scenarios on both sides, and state what the evidence cannot prove.

## Verified by

- Every required behavior is listed with where it was learned (definition, recorded run or approved requirement) and carries one verdict of holds, changed, cannot be kept or not verifiable, with its evidence beside it and whether that evidence is an on-target run or an offline one.
- The converted job is committed as code with no credential or environment-specific identifier, is never scheduled or activated by this Recipe and is deployed only to an approved ephemeral target, and the original job is left in place and unedited.
- For each behavior judged to hold, the same scenario run on the original definition and on the converted job gives the same observable outcome: which steps ran and in what order, the exit status, what was reported and what landed.
- The expected outcome of each scenario derives from the original job's behavior or the approved rule, never from the converted job's own output.
- The firing instants of the original and converted schedules are shown side by side for ordinary days in each UTC offset and for every local clock change of any zone either uses, and each difference is a changed verdict that names the instants.
- Every failure, skip or quiet-run path the original reacts to (a failing step, a warning-only check, an overlapping start, a run with nothing new) ends on the original as its definition does and on the converted job as the approved rules say, naming its cause; any difference is a changed verdict.
- A behavior the target cannot express is never replaced silently: its verdict names the substitute and the difference it makes, or says it was set aside, as approved; where the approved rule is to fail, the conversion stops naming the behavior and commits no converted job.
- The observable outcomes the approved judgement of unchanged requires are equal on both sides; where it includes landed or built data, rows from the same input are equal as multisets on all columns, or each difference is named with its cause.
- Where a failure notice is a required behavior, the content it carries is kept as approved; the delivery route is a deployment prerequisite unless the target offers one in scope, and delivery stays unproven unless a run delivers it.
- A missed or replayed run, a timeout, and each run-scoped value behave as approved, each with its own verdict; a behavior is not verifiable only where a named missing capability or input prevents it, which the verdict states.
- Where an on-demand run on the target is approved, its status and result agree with the verdicts; otherwise every run-time claim is labelled offline and reported unproven.
- What the evidence cannot prove is reported, including platform behavior shown only from documentation and any source behavior that was inferred because the original never showed it.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, job definition and approved requirements, and resolve only the semantics they leave open. Read the original job as it stands, never as intended: its schedule entry and time zone, its steps and exit handling, its guards against overlap, what it does with nothing new, and what it tells whom on failure; where recorded runs exist, use them to confirm each behavior, and mark any behavior neither shows as inferred. Write each required behavior as a testable statement with the scenario that would tell it apart from a plausible wrong version, and commit its expected outcome before the converted job runs. Author the converted job natively for the target through the platform's own orchestration route, express each behavior with the target's own mechanism, and compute both schedules independently, including every local clock change. Give each behavior one verdict with evidence, never tune the original-side reference toward the converted job, validate the converted job statically, prove held behaviors by the same scenarios on both sides, run it on demand on the target where approved, and report what was not proven.

### Compose

- generating-orchestration
- evaluating-orchestration
- running-orchestration-in-sandbox
- documenting-orchestration

### Ask first

- If unresolved, which job and target are in scope, and which observed behaviors must the target keep: order, schedule, failure rules, retries, overlap, missed-run catch-up, timeouts, late-run alerts, run-scoped values, notification, outputs?
- If unresolved, what must the schedule keep on the target (the same instant, the same local time, or one run per local day), in which time zone, and how are the two clock-change days handled?
- If unresolved, what runs after each failure the original reacts to, does a check that only warns fail the run, how is a start during an active run treated, and does a run with nothing new succeed and still build?
- If unresolved, what does a failure notice carry, who receives it, and may the target send it itself or is the route a deployment prerequisite?
- If unresolved, when the target cannot express a required behavior, should the conversion fail, use a named substitute, or set that behavior aside and report it?
- If unresolved, how is unchanged judged (the same outcomes for a fixed scenario set, the same landed data, or both), and which differences are permitted?
- If unresolved, may the converted job run on demand on the target?
- If unresolved, which source location, secrets and destination does the deployed job use?

### Guardrails

- Do not choose a required behavior, schedule rule, overlap or failure rule, or the substitute for an inexpressible behavior without approval; explain the alternatives if asked.
- Do not edit, disable or retire the original job, deploy the converted one outside an approved ephemeral run, or activate its schedule; cutover is a separate decision.
- Do not tune the original-side reference toward the converted job; a disagreement between them is a verdict.
- Do not report a quiet, skipped or empty run as a plain success; even where success is approved, it states what it did not do.
- Do not treat documentation, static validation or a local stand-in as proof that the target runs the job as stated.
- Do not convert the workload code the job calls; report a defect in it and hand the conversion to the Recipe for that source.
- Do not commit a credential or an environment-specific workspace, item or connection identifier; deployment supplies them.
