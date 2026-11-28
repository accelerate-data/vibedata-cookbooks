---
id: scd-procedure-to-dbt-snapshot
title: Convert a hand-written history routine into a dbt snapshot and prove history parity
trigger:
  - A Type 2 dimension is kept by a hand-written MERGE procedure or trigger that nobody wants to maintain.
  - The team wants dbt snapshot history, but consumers need proof the versions and dates match, not only today's rows.
  - A migration moves a history table's upkeep into dbt before the old routine can be retired.
description: Move a hand-written Type 2 history routine into a dbt snapshot with a published history relation, and prove after every replayed batch that versions, effective-from and effective-to dates and the current flag match the approved baseline, apart from keys left out as approved.
pitch: Prove a dbt snapshot keeps a hand-rolled history routine's versions and dates after every batch, bar keys left out as approved, before any retirement.
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
  - Needs the tables the routine reads landed in the target; landing them belongs to an ingestion Recipe.
  - Needs the routine's per-run history or an approved rule baseline; history it never kept is not rebuilt.
  - Current-state-only procedures belong to stored-procedure-to-dbt; new history to dbt-snapshot-history.
  - One history table per outcome; its other writers and other tables the routine writes are named, parity unverified.
  - Keys with backdated corrections between closed versions are left out only as approved; a snapshot cannot reproduce them.
  - A snapshot sees only each run's state; keys with versions made between runs are left out of parity only as approved.
  - Complete outcome assessed for duckdb_local only; the other listed platforms remain unassessed.
related:
  - stored-procedure-to-dbt
  - dbt-snapshot-history
  - legacy-sql-to-dbt
  - consolidate-legacy-table-writers-to-dbt
  - split-multi-table-procedure-to-dbt
  - accumulating-snapshot-procedure-to-dbt
  - legacy-periodic-snapshot-to-dbt
  - bitemporal-business-history
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

Convert <history_routine>, which keeps row history in <history_table> by closing and opening versions as tracked attributes change, into a dbt snapshot with a published history relation for <history_consumers> in the current Intent. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Deliver a map from each routine rule that opens, closes, ignores or removes a version to its snapshot equivalent, the snapshot and the published relation, and evidence that after every batch in the agreed replay the published history matches the approved baseline for that batch, apart from keys left out as approved: the same versions, effective-from and effective-to dates and current flag, at the approved precision. Reproduce routine behaviours that look like mistakes, or leave out as approved the keys whose history the snapshot cannot reproduce, and report each as follow-up work. Keep agreement on current rows separate from agreement on history, and keep parity separate from cutover and retirement of the routine.

## Verified by

- Each routine rule that opens, closes, ignores or removes a version maps to a snapshot behaviour or a stated reason none is needed or possible; writes elsewhere are reported out of scope, and what a failed run leaves committed in the history is matched or reported unverified.
- After every replayed batch, not only the last, the published history equals that batch's approved baseline, derived without the snapshot, bar keys left out as approved: same versions, dates and current flag at approved precision, duplicates counted.
- The consumer-facing build shares the replay's snapshot and published-relation definitions, differing only in named inputs and clock; it starts from the existing history as approved, lacks a kept version only as approved and named, and holds no replay batch, constructed key or replay clock time.
- The comparison can fail: a deliberately wrong end date on a closed version fails it while an agreement check on current rows alone would still pass, and one lost or one added duplicate row fails it.
- Within one continuous presence of a key, versions neither overlap nor gap, each closed end follows the approved convention from the next start, and each included key left current by the approved delete rule has one current version; a listed routine behaviour may give another shape.
- A change to one tracked attribute, by the routine's source-engine comparison (null versus empty, sentinels, case, trailing spaces, precision), opens one version, an untracked change none, unless a listed routine behaviour, an approved rule the routine leaves open or an approved left-out key differs.
- Replaying a batch again leaves the published history unchanged and adds no version under the approved effective-time rule; a batch whose rerun changes it, such as several rows for a new key, is named with what the rerun does and kept out of that claim only as approved.
- Null versus empty, unchanged redelivery, same-day changes, duplicate rows, stale changes and rows with no usable key or change time follow approved rules unless a listed routine behaviour or approved left-out key differs; rows a rule ignores or approved scope leaves out are counted with reasons.
- A leaving key follows the approved delete rule with no unapproved version, a returning key the approved return rule, unless a listed routine behaviour or approved left-out key differs; the snapshot never rewrites a closed version, and approved past-version overwrites show in the published relation.
- Each routine behaviour that looks like a defect is listed with the versions it affects and what correcting it would change, and is reproduced or, where the snapshot cannot, left out of parity only as approved; none is silently corrected.
- The published relation keeps the approved consumer contract, relations outside the approved scope are left unchanged, or a change that reaches one only through an approved step is named and its parity marked unverified, and the routine stays in place, and other writers as approved, until cutover.
- What the comparison cannot prove is stated, including a baseline that was not the routine's own output, any replay branch never exercised, and routine history the snapshot cannot reproduce, named per key with the routine's shape and left out of parity only as approved.

## Agent guidance

### Instructions

Read the routine end to end first: its key, tracked columns and comparison rule, how effective-from, effective-to and the current flag are set, what it does with deletes, returning keys and several rows for one key in a batch, and every other writer and consumer of the history table. Report behaviour the history cannot show as out of scope. Measure whether the existing history was written by the routine; if not, it is the starting history, not a batch result. Settle where the routine's history after each batch comes from, check the snapshot options the installed dbt and adapter support, and author the snapshot and a published relation that maps its internal dates to the approved convention. Build the expected history per batch with a committed builder that never reads the snapshot and starts from the same approved starting history, replay the agreed batches in order from it, compare after each one, run a negative control that proves the comparison can fail, and prove reruns on a disposable copy. Before the snapshot runs, in every build that writes the history, check each batch for several rows per key and match what the routine leaves, including after a failure; adapters differ on such rows. Apply batches in order; where versions take their time from the incoming row, an older batch backdates or reverts them. Leave a key out of comparison only as approved, named with its reason and its divergence measured. Record which replay branches were exercised and which were not.

### Compose

- capturing-requirements
- profiling-source-data
- authoring-dbt-project-artifact
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which timestamp sets a version's effective-from (a source change time, a load date or the run time), at what precision and time zone, how are effective-to and the current flag shown, and is the comparison exact or within a stated precision?
- If unresolved, which attributes open a version, which are overwritten on past versions, which are ignored, and are null and empty values equal or different?
- If unresolved, what happens with several rows for one key in a batch, existing or new, several changes on one day, stale or out-of-order changes, unchanged redelivery, rows with no usable key or change time, and a batch the routine fails on partway?
- If unresolved, is a key deleted by its absence from a complete batch or by a source delete flag, what happens to its current version and its closing date, and how does a returning key reopen?
- If unresolved, where does each batch's routine history come from (the routine run live or on an approved copy, or approved extracts or rules), who approves it, where may the replay's source or history copies live and how long, which batches form the replay, and how does existing history enter?
- If unresolved, may a key whose history the snapshot cannot reproduce be left out of parity, or a batch whose rerun changes the published history be left out of the rerun claim, each named, and how is a rerun of such a batch prevented in production?
- If unresolved, which entities or records belong in the history, which key identifies one entity, and how are excluded ones listed with their reasons?
- If unresolved, what counts as unchanged output (name, columns, types, order), must surrogate version keys keep the routine's values and assignment, does the snapshot take over the table's name or do consumers move later, and what happens to the routine and the table's other writers after parity?

### Guardrails

- Do not edit the routine or its captured per-batch output to make the comparison pass, or widen a tolerance, shorten the replay or narrow the approved contract to do so.
- Do not accept agreement on current rows as history parity; a history that matches only after the last batch has not been shown to match the batches consumers read in between.
- Do not rebuild history the routine never kept; a version dated before the approved starting history or otherwise backdated appears only where the routine's rules make one, and a snapshot cannot rewrite a closed version.
- Do not use the run clock as a version time unless the approved effective-time rule says so; a replay must not depend on when it ran.
- Do not normalise, trim or default values the approved comparison keeps distinct, or let a column outside the approved tracked list open a version, unless a listed routine behaviour does.
- Do not correct a routine defect, even under an approved rule; reproduce it or, where the snapshot cannot, leave its keys out of parity only as approved, report it as follow-up work and route any wanted change to a separate change.
- Do not let the routine and the snapshot both maintain the consumer-facing history at once, or retire the routine before parity is accepted and consumers have moved.
- Do not present a synthetic or rule-built baseline as the routine's real output; label it and state that cutover needs validation against the real routine.
- Run the replay, its constructed batches and any fixed clock in a separately named test build of the same snapshot and published-relation definitions; the consumer-facing history reads only the approved source, and the replay writes neither it nor, unless approved, the routine's live table.
- Keep Domain sources read-only bar an approved write to the routine's live table; keep output within the approved contract, use a labelled synthetic or approved writable fixture, commit no copy of source or history rows unless approved, and change other relations only by an approved, named step.
