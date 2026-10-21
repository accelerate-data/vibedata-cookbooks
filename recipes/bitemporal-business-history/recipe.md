---
id: bitemporal-business-history
title: Preserve business-effective history and what was known at each reporting cutoff
trigger:
  - A backdated correction must change today's reading of the past, yet a report issued earlier has to stay reproducible as it was published.
  - Finance or regulators ask both what was in force on a date and what was known at a reporting cutoff, and a single history table answers only one of them.
  - Corrections arrive late or overlap an earlier version, and nobody can say which version applied or when it became known.
description: Keep each business version with its own valid interval and recorded interval, never overwriting history, and answer bounded questions by effective date and by knowledge cutoff, with correction lineage, flagged unresolved overlaps and stable reruns.
pitch: Answer what applied on a date and what we knew at a cutoff, from one preserved version ledger.
job_category: build
area: transformation
readiness: supported
related:
  - dbt-snapshot-history
  - scd-procedure-to-dbt-snapshot
  - effective-dated-business-rules
domain_objects:
  - dimension
  - history
  - business_event
  - version_ledger
works_with:
  platforms:
    - duckdb_local
  tools:
    - dbt
qualifiers:
  - Complete outcome assessed for duckdb_local only; the other four Studio targets remain unassessed.
  - Needs a recorded time on each change; knowledge is never rebuilt from a present snapshot.
  - Both time axes at once; business-axis history alone belongs to the dimension history Recipe.
evidence:
  features:
    - profiling-source-data
    - authoring-dbt-project-artifact
    - generating-dbt-model
    - dbt-unit-testing
    - running-dbt-in-sandbox
    - verifying
  evals: []
---

## Prompt

Build a two-axis version history for <tracked_attribute> of <entity_name> and two bounded consumers for the questions required in this Intent: what applied on <effective_date> and what was known at <reporting_cutoff>. Inspect approved requirements and source evidence first, and confirm that every change carries a recorded time before building anything. Keep each version with its own business-valid interval and recorded interval, keep correction lineage, never overwrite or delete a version, and expose overlaps the rules cannot resolve. Keep Domain sources read-only; use a labelled synthetic fixture or an approved writable fixture with reset when the Domain has no such feed. Prove the discriminating case where a backdated correction changes the corrected period for later cutoffs while an earlier cutoff keeps the earlier answer, both axes at their boundaries, unresolved overlaps, and an unchanged rerun that leaves the ledger identical.

## Verified by

- The approved contract defines the entity, version key, tracked attribute, interval ends, precision, time zone, what a cutoff includes, each consumer's grain, the dates and cutoffs answered, and how corrections, overlaps and unusable changes are treated.
- Source evidence shows a recorded time carried by each change. A change without one is listed with its reason, never given a load time, run time or inferred time.
- Every usable change exists as its own version with both intervals. After a correction the superseded version remains with its own keys and lineage, and no version is overwritten, merged or deleted.
- Both consumers' published answers equal expected answers derived independently from sources and approved rules, fixed before the consumers exist, for a grid of dates and cutoffs. A correction recorded after an early cutoff leaves that cutoff's answer unchanged and changes a later cutoff's.
- Both axes are pinned at their boundaries by expected results that differ from their neighbours: an effective date at a version's start, just before its end and at its end, and a cutoff just before, at and after a correction's recording and a series' first recording, per the approved rules.
- Deliberately wrong consumers, such as one ignoring the cutoff, one ignoring the effective date and one using the wrong end bound, each fail at least one expected case against the same expectations.
- A date or cutoff with no applicable answer gets the approved disposition, and an unknown at that cutoff stays distinguishable from a date no version ever covered; a missing result never reads as zero or as a broken build.
- An overlap the correction rules cannot resolve is flagged with the versions and recorded times involved, and the contested dates carry no chosen winner; any wider withholding than the contested dates is the approved policy and is stated, and dates outside it keep answering.
- Every change delivered is accounted for once, as a version, an approved retraction or a set-aside with exactly one reason; counts reconcile at each stage.
- A rerun on unchanged input leaves versions, keys and intervals identical, and a larger input adding a later correction changes only what that correction governs, with earlier versions and keys unchanged.
- Results are read back on the actual supported Intent target, with expected and actual answers, the wrong consumers' failures and any unresolved exceptions reported, and the fixture reset verified.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain and sources. Inspect approved requirements and source evidence, and decide from the data whether each change carries a recorded time; stop and report when it does not. Use Ask first only for unresolved semantics, and record the entity, version key, intervals, cutoff meaning and dispositions before building. Check installed dbt and adapter versions. Derive the version key from the change's own identity so it survives rebuilds and reordering. Author expected answers by hand from the fixture before the consumers exist. Build the version ledger once with both axes, resolve corrections only by the agreed rule, and have the two consumers differ only by the cutoff filter so they cannot drift. Run the rerun and larger-input comparisons and the wrong-consumer checks against the same expectations, read the outputs back and verify fixture reset. Report missing recorded time, missing history or unexecuted required cases as incomplete verification.

### Compose

- profiling-source-data
- authoring-dbt-project-artifact
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which entity, attribute, changes and analytical questions must this history answer, at which effective dates and cutoffs, and which source supplies each change's identity and recorded time?
- If unspecified, how is a correction identified and resolved: by an explicit link, by period or by another rule, may it cover only part of the version it corrects, and what happens with competing corrections of one version?
- If unresolved, what do the consumers return for dates contested by an unresolvable overlap, and what do they return for a date with no applicable version or a cutoff before the first recording?
- If unspecified, what do the interval ends include, what precision and time zone apply, what does a cutoff include, and which knowledge does the effective-date question read when no cutoff is given?
- If unresolved, how are unusable changes, retractions, deletions and reappearing entities handled in the ledger and in the consumers?

### Guardrails

- Never reconstruct what was known from a present-state snapshot, a load stamp or a file time, and never backdate an observation; periods before the first recording stay unknown at earlier cutoffs.
- Valid time and recorded time are distinct axes. Do not collapse them into one validity interval, and do not let an observation boundary stand in for when a change took effect.
- Never overwrite, merge or delete a version to apply a correction. Do not infer a correction from equal periods or recording order unless that rule was approved.
- Do not pick a winner for an unresolvable overlap, deduplicate it away or drop the contested rows through an inner join.
- Keep Domain sources read-only. Mutate only an independently authored synthetic fixture or an approved writable fixture with a verified reset, and never mix synthetic rows into observed results.
- Execute on the actual supported Intent target and supplied sandbox without switching engines; support here covers duckdb_local only.
- Keep the deliverable to the version ledger, its two consumers and necessary checks. Single-axis dimension history, converting an existing slowly changing procedure and source ingestion belong to their own Recipes.
- A build that compiles or reruns cleanly does not prove the outcome; the changed case, boundary results, wrong-consumer failures and reconciliation are required execution evidence.
