---
id: dbt-refactor-output-identical
title: Refactor dbt models without changing consumer output
trigger:
  - A model has grown into one long query with logic packed inline, and nobody dares change it because dashboards and reports depend on its output.
  - The same join, lookup or derived key is written again and again across models, and the copies are starting to drift apart.
  - A mart reads a raw or source table directly instead of going through a staging model.
  - Reviewers need evidence that what consumers see is identical before and after a structural change.
description: Restructure existing dbt models so shared logic has one owner and each model reads as named steps, while every consumer-visible model keeps its approved contract and exact rows, proven by a two-way comparison against a baseline built from the same inputs, with defects found along the way listed rather than silently fixed.
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
  - Parity is proven only on the compared inputs; a rule those inputs never exercise needs its own boundary case.
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

Restructure <target_models> in the current Intent so that each repeated rule, join or derived key has one owner and each model reads as named steps, without changing anything <consumers> rely on. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only what they leave open: which models and repeated logic are in scope, what counts as unchanged consumer output, the comparison inputs and precision, how incremental models are checked, and what to do with a defect that would change output. Build the baseline from the unchanged code on the same inputs and engine, apply the restructuring, and compare every consumer-visible model in both directions under the approved contract. Report every difference row by row with its explanation, handle each defect found under the approved rule, and state what the comparison cannot prove. Change consumer output only under an approved resolution, and add no new marts or outputs as part of the refactor.

## Verified by

- Every consumer-visible model keeps the approved contract after the change, covering whichever of model name, columns, column order, types, materialization and rows the user counts as unchanged output.
- Consumer-visible rows match the baseline as multisets in both directions with equal row counts; any difference is listed row by row with its explanation, never absorbed by a tolerance the user did not approve.
- The baseline is the unchanged code built from the same inputs on the same engine; a gap between a fresh rebuild and the currently deployed tables is reported as a separate finding.
- Each incremental model gives the same output before and after the change under the approved check, whether a full rebuild, an incremental load from an earlier state, or both.
- Each consolidated rule has one owner, every former copy now uses it, and rules that look alike but behave differently, such as as-of versus current-version lookups, keep their distinct results.
- Each consolidated rule behaves the same at its boundaries, such as a record on an effective-date changeover, including boundaries the compared inputs never reach.
- Internal models may be removed, renamed, combined or reshaped; only an internal model the user names as part of an approved interface keeps its contract. Differences the comparison cannot rule out are stated.
- Every semantic defect found is listed with the output it affects, and is either preserved unchanged as a follow-up or changed under an approved resolution that names the contract and baseline change.
- The refactored models match the baseline in each approved execution environment and session time zone; independence from the time zone is required only where the consumer contract already includes it.
- Repeated logic deliberately left in place is listed with its reason.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements. Read the target models, their dependencies and every consumer before changing anything: marts, exposures, documented analysis surfaces and anything downstream that reads them. Find logic that is repeated or packed inline, and check whether copies that look alike really behave alike; two lookups against the same versioned dimension can differ, one as of the record's date and one at the current version. Agree the target set, the consumer contract and the comparison approach before restructuring. Build the baseline from the unchanged code on the same inputs and engine, and check that two unchanged builds agree, so that later differences belong to the change. Restructure one move at a time, giving each shared rule one owner and keeping the approved layering. Rebuild and compare every consumer-visible model in both directions; check incremental models the approved way. Where the compared inputs never reach a rule's boundary, add a case that does. Record each defect found with the output it affects and its approved handling, list repeated logic deliberately left in place, and state what the comparison cannot prove.

### Compose

- refactoring-dbt-models
- evaluating-dbt-project
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which models and which repeated logic are in scope, and does the shared logic extend to every dimension or rule that uses the same pattern, or only the ones named?
- If unresolved, what counts as unchanged consumer output: rows and values only, or also model names, column names, column order, types and materialization?
- If unresolved, which inputs and period form the comparison, and are values compared exactly or within an approved precision for floating-point columns?
- If unresolved, when a defect is found that would change output, is the output preserved and the defect listed as a follow-up, or fixed under an approved contract and baseline change?
- If unresolved, are incremental models checked by a full rebuild, by an incremental load from an earlier state, or both?
- If unresolved, which layering rules must the restructured project keep, for example whether an intermediate model may read from a mart?
- If unresolved, is any internal model part of an approved interface that must keep its contract, and in which execution environments and session time zones must the refactored output match the baseline?

### Guardrails

- Do not change what a consumer sees beyond the approved contract to make the code tidier; a refactor fixes no numbers unless the user approves the change.
- Do not silently fix a defect found during the refactor; preserve the output and list it, or obtain an approved resolution.
- Do not merge rules that look alike but return different results, such as as-of and current-version lookups; give each its own owner or keep both behaviours.
- Do not treat a green build or a passing test suite as proof of unchanged output; the proof is the two-way comparison against the baseline.
- Do not compare against a baseline built from different code, inputs or engine, and do not use deployed tables as the baseline when a rebuild of unchanged code already differs from them.
- Do not widen a tolerance, narrow the compared set or drop a column from the comparison to make it pass.
- Do not reduce required verification coverage; a redundant test may be replaced by one that covers the same behaviour. Do not reverse layer dependencies without approval.
- Do not extend the refactor into incremental conversion, performance tuning, new marts or other model groups outside the agreed target set.
