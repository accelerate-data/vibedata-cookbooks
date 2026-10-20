---
id: move-dbt-project-destination
title: Move a dbt project to a new destination and prove parity before cutover
trigger:
  - A dbt project has to run on a different warehouse or lakehouse, and the dashboards and reports that read it cannot show a different number afterwards.
  - Someone says the migration is done because the build is green on the new destination, but nobody has compared what consumers read.
  - The project uses functions, types, hooks or access rules that may not exist or behave the same on the new destination.
  - The team needs a go or no-go for cutover, with the open items named.
description: Port an existing dbt project to a new destination and compare each relation in the approved scope with the unchanged project over identical inputs, within approved equality rules, with every destination-specific construct accounted for and a cutover recommendation that names what is still open.
pitch: Find out whether a dbt project returns the same results on its new destination, within rules you approve, before anyone cuts over.
job_category: cross-platform
area: transformation
readiness: planned
domain_objects:
  - dbt_model
  - consumer_contract
  - approved_baseline
  - parity_report
  - construct_inventory
  - cutover_recommendation
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
  - Needs a second engine executable from the Intent; a same-engine rehearsal cannot show an engine difference.
related:
  - legacy-sql-to-dbt
  - dbt-refactor-output-identical
  - prove-dbt-change-safe
  - database-tables-to-bronze
evidence:
  features:
    - evaluating-dbt-project
    - running-dbt-in-sandbox
    - dbt-unit-testing
    - verifying
  evals: []
---

## Prompt

Move <dbt_project> to <new_destination> and show, before cutover, whether every relation in <consumer_relations> returns the same results there as the unchanged project does on <current_destination>, within the approved equality rules. Inherit the Intent's repository, Domain, sources and approved requirements, and resolve only the semantics they leave open. Inventory what in the project is specific to the current destination, port each construct or name it as a gap, then compare each in-scope relation with the unchanged project's output over identical, pinned inputs. Deliver the ported project, a comparison report and a go or no-go recommendation with its open items. A defect found, or an output change someone wants, is reported as separate work; moving consumers and retiring the old destination are not part of this move.

## Verified by

- Every relation in the approved scope is named with a verdict of match, difference or not compared; a difference or a "not compared" carries an approved reason, and none is silently absent.
- The ported project is committed and builds each in-scope relation on the destination under test, or the relation is listed with an approved reason it is not built.
- Both destinations read the same inputs, shown identical by per-source row counts and a content check; any comparison input placed on the destination stays apart from consumer-facing relations.
- Each relation's column set, declared types and rows match the unchanged baseline, or differ only where an approved type mapping or tolerance permits; each difference is listed. Rows are compared by key, not order, unless order is part of the consumer contract.
- Each published figure at an approved cut matches the baseline at the approved precision; a baseline figure that disagrees with an independent derivation under the approved rules is reported as a baseline defect, not changed.
- Matches hold in each approved run mode, time zone and calendar; carried history such as snapshots or incremental state is shown moved or listed as a gap.
- A deliberately introduced difference of each approved kind (value beyond tolerance, missing or empty value, row on one side only, changed type) is reported and one within tolerance is not; repeating the comparison on the same files returns the same verdict.
- Every destination-specific construct, including seeds, hooks and access grants, has a verdict (ported, replaced, named gap or unproven) and its cutover consequence; none is inferred from behaviour on another engine.
- The report names the destinations actually compared, makes no claim about one that was not run, and states which engine differences the run could not detect.
- A baseline that returns different output on identical inputs is reported with the affected columns and handled as approved (separate fix, tolerated by the approved comparison, or blocker), never loosened without approval.
- Relations outside the approved scope keep their output against the unchanged baseline except approved differences, and every wanted change is listed as separate work.
- The recommendation is go only when no item approved as cutover-blocking is open or unverified and the approved go evidence is present; each unverified condition is named as an open item.

## Agent guidance

### Instructions

Inherit the Intent's repository, Domain, sources and approved requirements, and resolve only the semantics they leave open. Read the project and every consumer first: marts, serving tables, exposures, semantic models and metrics. Identify which relations consumers read and which internal models are approved interfaces. Inventory everything specific to the current destination: profile and catalog names, functions, types and their precision, text comparison and identifier handling, seeds, hooks and macros that assume local files or a target type, materializations, contracts and access grants. Give each a verdict and port only what the approved scope allows. Pin the inputs both destinations read before comparing. Build the baseline from the unchanged project and compare by key under the approved equality rules, including NULL handling, text, decimals and floating-point values. Show the comparison fails on a seeded difference before trusting a pass. Where the run could not detect a difference, say so. Report defects and wanted changes as separate work, and give a go or no-go with its open items.

### Compose

- evaluating-dbt-project
- running-dbt-in-sandbox
- dbt-unit-testing
- verifying

### Ask first

- If unresolved, which relations, semantic models, metrics and published cuts must match, and which internal models are approved interfaces?
- If unresolved, what does "the same" mean: exact, or a tolerance per column type; the published precision; whether order inside a list or text aggregate counts; and how NULL and empty text, collation, case sensitivity and identifier case or quoting are treated?
- If unresolved, how does the destination get the same inputs, and what counts as identical inputs?
- If unresolved, for each construct with no equivalent on the new destination (functions, types and their mapping, seeds, hooks, grants), is it ported, replaced with an approved equivalent or left as a named gap, and does it block cutover?
- If unresolved, in which time zones, calendars, run modes (full rebuild, incremental) and carried history must results match?
- If unresolved, when the unchanged project returns different output on identical inputs, is that fixed in a separate change, tolerated by the approved comparison, or a blocker?
- If unresolved, who decides go or no-go, what evidence must be present for a go, and which open items block it?
- If unresolved, is any output change wanted? It belongs in a separate change, not in this move.

### Guardrails

- Do not treat a green build or passing tests on the new destination as proof of parity; the proof is the comparison with the unchanged project.
- Do not replace a destination-specific function or type with a look-alike without the approved comparison showing it returns the same results.
- Do not infer a result on one destination from behaviour on another, or claim a destination was compared when it was not run.
- Do not loosen the comparison without approval to turn a failure into a pass; report the cause as a defect, a destination difference or a varying baseline.
- Do not change anything a consumer reads beyond approved differences, even to fix a wrong number; route it to a separate change.
- Do not repoint consumers, retire the old destination or load production data; the only data placed on the destination is the approved comparison input, and production loading and file ingestion belong to their own Recipes.
- Do not recommend a go while an item approved as cutover-blocking is open or unverified.
