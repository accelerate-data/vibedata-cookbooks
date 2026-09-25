---
id: motherduck-flight-scheduling
title: Schedule a dlt load and a dbt build on MotherDuck as a committed MotherDuck Flight
trigger:
  - The MotherDuck load and build run from a cron job on someone's laptop.
  - A dlt load and a dbt build on MotherDuck have to run in order on a schedule without standing up an orchestrator.
description: Author a MotherDuck Flight as committed code that runs a dlt load and then a dbt build in order on a schedule, with every credential declared as a secret, and prove one on-demand run succeeded on the workload's own result as well as the Flight's status.
pitch: Replace the laptop cron with a committed MotherDuck Flight that loads and builds on a schedule.
job_category: build
area: orchestration
readiness: supported
domain_objects:
  - motherduck_flight
  - schedule
works_with:
  platforms:
    - motherduck
  tools:
    - dlt
    - dbt
evidence:
  features:
    - generating-orchestration
    - evaluating-orchestration
    - running-orchestration-in-sandbox
    - documenting-orchestration
  evals: []
---

## Prompt

Schedule <dlt_pipeline> and then the dbt build of <dbt_selector> to run every <cadence> on MotherDuck as a MotherDuck Flight named <flight_name>. Commit the Flight as code with every credential it reads declared as a secret, run it once on demand in the sandbox, and report its run status, its exit code and the workload's own result.

## Verified by

- The Flight is committed to the repository with its schedule, and no Flight id or credential value appears in the repository.
- The Flight passes static Flight validation with no findings.
- An on-demand sandbox run reaches a succeeded status with exit code 0.
- The run's own dlt and dbt results show that the load and the build both succeeded.
- The Flight name, version, run number, status and exit code are recorded as run evidence.

## Agent guidance

### Instructions

Confirm the dlt pipeline and the dbt selection the Flight will run exist in the repository before authoring it. Author the Flight from the canonical template and adapt it only through its configuration, declaring every credential as a secret and committing the Flight's name, never its generated id. Validate it statically, run it once on demand in the sandbox, and judge success on the workload's own result as well as the Flight's status before declaring the Recipe complete.

### Compose

- generating-orchestration
- evaluating-orchestration
- running-orchestration-in-sandbox
- documenting-orchestration

### Ask first

- Ask for the schedule cadence only if neither the request nor the approved requirements state one.
- Ask whether the dbt build should run when the load lands no new rows only if the approved requirements do not say.

### Guardrails

- Do not create, apply or schedule the Flight directly on the platform; the committed item is the only deploy path.
- Do not treat a succeeded Flight status alone as proof; a failed dbt graph can still report success.
- Do not offer this Recipe for local DuckDB, which has no scheduling capability.
