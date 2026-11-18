---
id: scd-procedure-to-dbt-snapshot
title: Convert a hand-written history routine into a dbt snapshot and prove history parity
trigger:
  - A Type 2 dimension is kept by a hand-written MERGE procedure or trigger that nobody wants to maintain.
  - The team wants dbt snapshot history, but consumers need proof the versions and dates match, not only today's rows.
  - A migration moves a history table's upkeep into dbt before the old routine can be retired.
description: Move a hand-written Type 2 history routine into a dbt snapshot with a published history relation, and prove after every replayed batch that versions, effective-from and effective-to dates and the current flag match the approved baseline.
pitch: Retire a hand-rolled history routine by proving a dbt snapshot keeps the same versions and dates after every batch.
job_category: re-engineer
area: transformation
readiness: supported
function:
  - cross-functional
domain_objects:
  - history_routine
  - history_table
  - dbt_snapshot
  - published_history
  - replay_batches
  - approved_baseline
  - parity_report
  - follow_up
works_with:
  platforms:
    - duckdb_local
    - motherduck
    - fabric_lakehouse
    - fabric_warehouse
    - redshift
    - databricks
  tools:
    - dbt
qualifiers:
  - Needs the routine's per-run history or an approved rule baseline; history it never kept is not rebuilt.
  - Current-state-only procedures belong to stored-procedure-to-dbt; new history to dbt-snapshot-history.
  - One history table per outcome; its other writers and other tables the routine writes are named, parity unverified.
  - Routines that insert backdated corrections between closed versions are reported; a snapshot cannot reproduce them.
  - Complete outcome assessed for duckdb_local only; the other listed platforms remain unassessed.
related:
  - stored-procedure-to-dbt
  - dbt-snapshot-history
  - legacy-sql-to-dbt
evidence:
  features:
    - capturing-requirements
    - profiling-source-data
    - authoring-dbt-project-artifact
    - generating-dbt-model
    - dbt-unit-testing
    - running-dbt-in-sandbox
    - verifying
  evals: []
---

## Prompt

Convert <history_routine>, which keeps row history in <history_table> by closing and opening versions as tracked attributes change, into a dbt snapshot with a published history relation for <history_consumers> in the current Intent. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Deliver a map from each routine rule that opens, closes, ignores or removes a version to its snapshot equivalent, the snapshot and the published relation, and evidence that after every batch in the agreed replay the published history matches the approved baseline for that batch: the same versions, effective-from and effective-to dates and current flag, at the approved precision. Reproduce routine behaviours that look like mistakes and report each as follow-up work. Keep agreement on current rows separate from agreement on history, and keep parity separate from cutover and retirement of the routine.

## Verified by

- Each routine rule that opens, closes, ignores or removes a version maps to a snapshot behaviour or a stated reason none is needed; writes elsewhere are reported out of scope, and what a failed run leaves committed in the history is matched or reported unverified.
- After every batch in the agreed replay, not only the last, the published history equals the approved baseline for that batch (routine output, or history derived from sources and approved rules without the snapshot): same versions, dates and current flag at the approved precision, duplicates counted.
- The replay build and the consumer-facing build share the snapshot and published-relation definitions and differ only in named inputs and clock, and the consumer-facing history holds no replay batch, constructed key or replay time.
- The comparison can fail: a deliberately wrong end date on a closed version fails it, while an agreement check on current rows alone would still pass.
- Within one continuous presence of a key, versions neither overlap nor gap, each closed end follows the approved convention from the next start, and each included key left current by the approved delete rule has one current version, unless a routine behaviour, listed with its shape, gives another.
- A change to one tracked attribute alone, judged by the routine's own comparison on the source engine (null versus empty, sentinels, case, trailing spaces, precision), opens one version with the new value unless approved rules or a listed defect say otherwise; an untracked change opens none.
- Replaying a batch again leaves the published history unchanged and adds no version under the approved effective-time rule; a batch whose rerun changes it, such as several rows for a new key, is named with what the rerun does and kept out of that claim.
- Null versus empty values, unchanged redelivery, same-day changes, duplicate rows, stale changes and rows with no usable key each follow the approved rule, and rows the rule ignores or the approved scope leaves out are counted with their reason.
- A key that leaves the feed follows the approved delete rule with no unapproved version for the absence, a returning key follows the approved return rule, the snapshot never rewrites a closed version, and any approved overwrite of past versions shows in the published relation.
- Each routine behaviour that looks like a defect is reproduced and listed with the versions it affects and what correcting it would change; none is silently corrected.
- The published relation keeps the approved consumer contract, relations outside the approved scope are left unchanged or any change reaching one is named and its parity marked unverified, and the routine stays in place until cutover is approved.
- What the comparison cannot prove is stated, including a baseline that was not the routine's own output, any replay branch never exercised, and routine history the snapshot cannot reproduce, named per key with the routine's shape and left out of parity only as approved.

## Agent guidance

### Instructions

Read the routine end to end first: its key, tracked columns and comparison rule, how effective-from, effective-to and the current flag are set, what it does with deletes, returning keys and several rows for one key in a batch, and every consumer of the history table. Report behaviour the history cannot show as out of scope. Measure whether the existing history was written by the routine; if not, it is the starting history, not a batch result. Settle where the routine's history after each batch comes from, check the snapshot options the installed dbt and adapter support, and author the snapshot and a published relation that maps its internal dates to the approved convention. Build the expected history per batch with a committed builder that never reads the snapshot, replay the agreed batches in order from the approved starting history, compare after each one, and run a negative control that proves the comparison can fail. Before the snapshot runs, in every build that writes the history, check each batch for several rows per key and match what the routine leaves, including after a failure; adapters differ on such rows. Apply batches in order; where versions take their time from the incoming row, an older batch backdates or reverts them. Leave a key out of comparison only as approved, named with its reason and its divergence measured. Record which replay branches were exercised and which were not.

### Compose

- capturing-requirements
- profiling-source-data
- authoring-dbt-project-artifact
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which timestamp sets a version's effective-from (a source change time, a load date or the run time), at what date or time precision and time zone, and how effective-to and the current flag are shown?
- If unresolved, which attributes open a version, which are overwritten on past versions, which are ignored, and are null and empty values equal or different?
- If unresolved, what happens with several rows for one key in a batch, existing or new, several changes on one day, stale or out-of-order changes, unchanged redelivery, rows with no usable key, and a batch the routine fails on partway?
- If unresolved, is a key deleted by its absence from a complete batch or by a source delete flag, what happens to its current version and its closing date, and how does a returning key reopen?
- If unresolved, where does the routine's history after each batch come from, such as running it beside the snapshot, approved extracts or approved rules, and who approves that baseline?
- If unresolved, which batch sequence forms the replay, how does existing history enter the snapshot at its start, is the comparison exact or within a stated precision, and may a key whose history the snapshot cannot reproduce be left out of parity, named?
- If unresolved, which entities or records belong in the history, which key identifies one entity, and how are excluded ones listed with their reasons?
- If unresolved, what counts as unchanged output (name, columns, types, order), does the snapshot take over the history table's name or do consumers move later, and is the routine kept or removed after parity?

### Guardrails

- Do not edit the routine or its captured per-batch output to make the comparison pass, or widen a tolerance, shorten the replay or narrow the approved contract to do so.
- Do not accept agreement on current rows as history parity; a history that matches only after the last batch has not been shown to match the batches consumers read in between.
- Do not rebuild history the routine never kept or backdate versions; coverage starts where the approved starting history does, and a snapshot cannot rewrite a closed version.
- Do not use the run clock as a version time unless the approved effective-time rule says so; a replay must not depend on when it ran.
- Do not normalise, trim or default values the approved comparison keeps distinct, and do not let a column outside the approved tracked list open a version.
- Do not correct a routine defect; reproduce it, report it as follow-up work and route any wanted change to a separate change.
- Do not let the routine and the snapshot both maintain the consumer-facing history at once, or retire the routine before parity is accepted and consumers have moved.
- Do not present a synthetic or rule-built baseline as the routine's real output; label it and state that cutover needs validation against the real routine.
- Run the replay, its constructed batches and any fixed clock in a separately named test build of the same snapshot and published-relation definitions; the consumer-facing history reads only the approved source and is never written by the replay.
- Keep Domain sources read-only and the published relation's output within the approved contract; use a labelled synthetic fixture or an approved writable one, and do not change relations outside the conversion.
