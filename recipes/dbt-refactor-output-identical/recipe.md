---
id: dbt-refactor-output-identical
title: Refactor dbt models without changing consumer output
trigger:
  - A model has grown into one long query with logic packed inline, and nobody dares change it because dashboards and reports depend on its output.
  - The same join, lookup or derived key is written again and again across models, and the copies are starting to drift apart.
  - A mart reads a raw or source table directly instead of going through a staging model.
  - Reviewers need evidence that what consumers see is identical before and after a structural change.
description: Restructure existing dbt models so that, within an approved scope, repeated logic has one owner and long models read as named steps, with evidence that every relation a consumer reads keeps its approved contract against a baseline of the unchanged code.
pitch: Clean up tangled dbt models and prove that nothing your consumers read has changed.
job_category: re-engineer
area: transformation
readiness: supported
domain_objects:
  - dbt_model
  - consumer_contract
  - approved_baseline
  - parity_report
  - follow_up
works_with:
  platforms:
    - duckdb_local
  tools:
    - dbt
qualifiers:
  - Complete outcome assessed for duckdb_local only; the other four Studio targets remain unassessed.
related:
  - dbt-full-refresh-to-incremental
  - prove-dbt-change-safe
evidence:
  features:
    - refactoring-dbt-models
    - evaluating-dbt-project
    - dbt-unit-testing
    - running-dbt-in-sandbox
    - verifying
  evals: []
---

## Prompt

Refactor <target_models> so that, as the approved scope requires, repeated logic has one owner and long models read as named steps, without changing anything a consumer reads. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Propose the restructure before editing. Deliver the restructured models and evidence that every consumer-visible relation, and any internal model that is part of an approved interface, keeps its approved contract and matches a baseline of the unchanged code in each approved execution environment. A defect found along the way, or an output change someone wants, is reported as separate work; it is not part of this refactor.

## Verified by

- Every relation a consumer reads keeps its approved contract after the refactor, and its name, schema and rows match the baseline of the unchanged code at the approved precision.
- The match holds in each approved execution environment and time zone; independence from the time zone is required only where the consumer contract already includes it.
- Internal models that are not part of an approved interface may be removed, renamed, combined or reshaped; an internal model that is part of an approved interface keeps its contract.
- Repeated logic in scope has one owner, and rules that look alike but return different results keep their distinct behaviour.
- Each restructured rule gives the same result as the logic it replaced, including at boundaries the compared data never reaches.
- Defects found and output changes requested during the refactor are reported as follow-up work, with the output they affect, and are not applied.
- Anything the comparison cannot prove is stated.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements. Read the target models, their dependencies and every consumer before changing anything: marts, exposures, semantic models, documented analysis surfaces and anything downstream that reads them. Identify which relations are consumer-visible and which internal models, if any, are approved interfaces. Find logic that is repeated or packed inline, and check whether copies that look alike really behave alike; two lookups against the same versioned dimension can differ, one as of the record's date and one at its current version. Propose the restructure, then build a baseline from the unchanged code. Restructure within the approved scope, following the project's approved structure and layering. Compare every consumer-visible relation and approved interface with the baseline in each approved environment; for an incremental model, compare after an incremental run as well as a full rebuild. Where the compared data never exercises a restructured rule's boundary, cover that boundary another way. Report defects and wanted output changes as follow-up work, and state what the comparison cannot prove.

### Compose

- refactoring-dbt-models
- evaluating-dbt-project
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which models and which repeated logic are in scope?
- If unresolved, what is the consumer contract: which relations count as consumer-visible, which internal models are approved interfaces, and must rows match exactly or within an approved precision?
- If unresolved, in which execution environments and time zones must the output match the baseline, and does the consumer contract already promise the same result in every time zone?
- If unresolved, is any output change actually wanted? If so, it belongs in a separate change, not in this refactor.
- If unresolved, which project structure and layering conventions must the restructured models follow?

### Guardrails

- Do not change anything a consumer reads, even to fix a wrong number; route any output change to a separate change.
- Do not merge rules that look alike but return different results; keep each behaviour.
- Do not treat a green build or a passing test suite as proof of unchanged output; the proof is the comparison with the baseline.
- Do not claim exact preservation when the baseline itself varies from run to run; report what cannot be proven.
- Do not reduce required verification coverage; a refactor may replace or remove redundant tests.
- Do not extend the refactor into incremental conversion, performance tuning, new marts or model groups outside the agreed scope.
