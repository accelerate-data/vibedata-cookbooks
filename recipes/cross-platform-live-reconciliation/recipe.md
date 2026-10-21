---
id: cross-platform-live-reconciliation
title: Reconcile equivalent data across two live systems before cutover
trigger:
  - A table or model has been rebuilt on another platform or database while the original is still running, and the owner needs evidence the two hold the same data before cutting over.
  - Both sides keep changing, so a one-off or count-only comparison is not sign-off evidence.
  - A cutover decision needs a ready, blocked or unproven verdict per table, with the differences behind it listed.
description: Compare each approved table across two live systems in place, read-only, and give per-table and overall cutover verdicts with every difference counted exactly and examples shown as approved.
pitch: Show that the old and the rebuilt table hold the same data, read live from both, before you cut over.
job_category: cross-platform
area: data-quality
readiness: supported
domain_objects:
  - comparison_pair
  - business_key
  - reconciliation_finding
  - cutover_verdict
works_with:
  platforms:
    - duckdb_local
qualifiers:
  - Each side must be readable live and read-only from the Intent; a side that is not stays unproven.
  - A baseline of the same project's unchanged dbt code belongs to dbt-refactor-output-identical.
related:
  - dbt-refactor-output-identical
  - prove-dbt-change-safe
evidence:
  features:
    - verifying
  evals: []
---

## Prompt

Show that <comparison_tables> hold the same data in <old_system> and <new_system> before cutover, reading both live and in place, read-only. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. For each table, show which business keys are on both sides, only on one side, duplicated or null, how each column compares under the approved correspondence, type normalisation and tolerance, and every difference with its exact count and examples as approved. Hold each side still as approved, and show or count the rows that leaves out. Deliver per-table and overall cutover verdicts with typed blockers. A difference is reported, not repaired, and the verdict does not perform or authorise the cutover.

## Verified by

- Each side is read live and in place, read-only: neither is repaired or written, no copy of either side persists beyond findings and approved examples, and no credential or connection secret appears in the output.
- Each table has an approved way of holding the comparison still (pinned instant, closed-date cutoff or settling window), or is unproven. A change during the read leaves the table unproven, reported as inconsistent rather than as a value difference; a change outside the compared records does not.
- Rows the comparison leaves out (past the comparison point, outside the approved population) are shown or counted with their reason as approved and treated as the policy says; on each side compared plus left-out rows equal total rows.
- Each distinct key falls in exactly one class: matched, only-old, only-new, duplicate, or null or partly null. The classes add up to the union of keys, set-aside keys are counted with their reason, and equal row counts never hide a missing key paired with an extra one.
- Every column on either side is listed with both types, its mapping and an approved compatibility verdict. A column outside the compared scope, on one side only or incompatible is listed and counted with its reason, never silently skipped.
- Matched rows are compared column by column under the approved normalisation and tolerance, with agree and differ counts per column. A value within tolerance is not a difference, and one beyond it always is.
- Each finding names the table, difference type and, where it applies, the column and business key. Its count is exact within the compared scope and never capped, and examples up to the approved number can be re-read from the sources.
- Each table and the whole get one verdict, ready, blocked or unproven, from the approved policy, with typed blockers naming the findings behind it and any budget rule applied. Equal totals never pass, and an unreadable, unnormalisable or unproven item is never ready.
- Published counts and verdicts equal values recomputed independently from the two sources with a separate method, and no check reuses the comparison's own calculation. A pair differing only by permitted type drift is ready.
- A labelled pair with planted differences reports each as a finding, blocking unless policy permits it: offsetting missing and extra keys, a duplicate key, a null key, NULL against empty text, a missing column, an out-of-tolerance value. A planted row past the comparison point is left out, counted.
- A rerun at the same comparison point on unchanged sides reproduces counts and verdicts. A sampled or partial table's verdict states its scope, is exact only within it and leaves the rest unproven unless the policy says otherwise, and its draw can be reproduced.
- The result names the engine of each side. Where the approved cutover target differs from what was compared, that difference stays an open blocker.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Establish how each side can be read live and read-only before designing anything; if a side cannot be read live from the Intent, say so and mark its tables unproven. Fix the business key, the key and column correspondence, the population and the way each side is held still per table, then settle key presence before values: classify every key as matched, only on one side, duplicated or null, and show the classes add up to the union of keys. Compare column by column under the approved normalisation, record exact counts, and keep examples as approved. Hold each side still as approved or detect change during the read, and record where neither is possible. Derive expected counts independently, prove the comparison can fail on a labelled pair with planted differences, then run it on the real pair and rerun it at the same comparison point. Write findings to a workspace apart from both sides, and leave both sides untouched.

### Compose

- verifying

### Ask first

- Ask which two systems and tables are compared, which side is the reference, and how each side can be read live and read-only, only if the Intent does not already name them.
- Ask for each table's business key and how key values and columns correspond across the sides (renames, derived and technical columns, casing, collation, type).
- Ask which records count (closed periods, record classes, soft-deleted or test rows) and whether left-out records are listed or only counted.
- Ask how each side is held still: a pinned instant, a closed-date cutoff or a settling window, or neither, and how rows written after it, or lagging on one side, are treated.
- Ask which type normalisation applies per column (integer width, decimal scale, timestamp precision and zone, text trim and case, NULL against empty text or another sentinel) and what tolerance, absolute or relative, if any.
- Ask how duplicate keys, null keys, records on one side only, and columns on one side only or with a type that cannot be normalised are treated: a blocker, a permitted difference, or a set-aside with a reason.
- Ask what makes a table ready for cutover: zero differences, a stated mismatch budget, or a subset of blocking difference types, and whether overall readiness needs every table.
- Ask whether the whole table or an approved sample or column subset is compared, how a sample is drawn, how many examples per finding to show and whether sensitive values may appear in them or must be masked.

### Guardrails

- Do not repair a difference, or change either side, to reach a ready verdict.
- Do not treat equal row counts, totals or checksums at table level as proof of equal content; compare keys and values.
- Do not join on a key with duplicate or null values without reporting them.
- Do not coerce types, trim text, fold case or equate NULL with empty text beyond the approved normalisation.
- Do not compare data that is still changing as if it were settled; hold it still as approved, or mark the table unproven.
- Do not present a sample, a stand-in or a result between the same kind of system as proof about a different production system.
- Do not put credentials, connection strings or unmasked sensitive values in the output.
- Do not treat a ready verdict as performing or authorising the cutover, or retiring the old side.
