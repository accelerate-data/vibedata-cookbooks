---
# Copy to recipes/<recipe_id>/recipe.md and replace every value. CONTRIBUTING.md describes each key.
id: <recipe_id>
title: <literal_deliverable_title>
trigger:
  - <situation_that_calls_for_this_recipe>
description: <one_line_outcome_and_scope>
pitch: <one_sentence_for_the_hero_card>
job_category: build  # get-running, re-engineer, build, prove, explain or cross-platform
area: transformation  # kebab-case, for example ingestion, transformation, orchestration
readiness: supported  # proven, supported or planned; proven needs at least one evidence.evals entry
domain_objects:
  - <domain_object>
works_with:
  platforms:  # one or more of duckdb_local, motherduck, fabric_lakehouse, fabric_warehouse, redshift
    - duckdb_local
  tools:
    - dbt
evidence:
  features:
    - <skill_name>
  evals: []
---

## Prompt

Replace this line with the task as one paragraph on one line, and mark each value the engineer adapts as a placeholder such as <model_name>.

## Verified by

- Replace with one independently checkable acceptance condition.
- Add one bullet per further condition.

## Agent guidance

### Instructions

Replace with one paragraph on how the agent should approach the work and what evidence it must collect before declaring the Recipe complete.

### Compose

- <skill_name>

### Ask first

- Ask for <decision> only if it cannot be inferred from approved requirements or repository evidence.

### Guardrails

- Do not <unsafe_shortcut>.
