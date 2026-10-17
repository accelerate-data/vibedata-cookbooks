---
id: people-pay-band-gaps
title: Check pay against salary bands and report pay gaps at an aggregate grain
trigger:
  - A pay-equity review is due and worker-level compensation cannot be shared widely.
  - Managers are told people are paid outside the band, but nobody can say how many, where, or on which band version.
  - HR is asked for pay gaps between groups and cannot tell whether publishing a number could reveal a small group.
description: For the approved review date, place each counted worker's pay against the band in force, keep that worker-level result apart from the published outputs, and publish only approved aggregates, such as unadjusted pay gaps, with the approved small-group hiding, while every record is accounted for.
pitch: Check pay against salary bands and publish approved pay gaps by group, with approved small-group hiding and its remaining limits stated.
job_category: build
area: governance-cost
readiness: supported
function:
  - people
domain_objects:
  - worker
  - pay_record
  - salary_band
  - band_placement
  - comparison_group
  - pay_gap
  - suppression_rule
  - pay_exception
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
  - Assessed end to end on duckdb_local only; the other listed targets rely on dbt support and are unassessed.
  - Pay, band and worker records arrive as landed tables; landing them is a separate outcome.
  - Stops at the check and the aggregate report; remediation, adjusted-gap modelling and pay planning are separate outcomes.
  - Restricting worker-level pay needs roles and grants (pii-classification-and-masking); without them it is a label.
  - On fabric_lakehouse, SQL grants do not govern OneLake reads, so restriction cannot be assured there.
  - Statutory report formats and statistical significance are separate outcomes.
  - Hiding small groups alone does not make a figure safe to release; totals and other releases can reveal one.
  - Unless issued reports are frozen, a later correction restates them; frozen ones need kept snapshots.
related:
  - governed-spreadsheet-table
  - pii-classification-and-masking
  - metric-population-and-rollups
  - effective-dated-business-rules
  - dbt-snapshot-history
evidence:
  features:
    - capturing-requirements
    - applying-medallion-data-modelling
    - generating-dbt-model
    - running-dbt-in-sandbox
    - verifying
  evals: []
---

## Prompt

Build <restricted_worker_pay_model>, <published_pay_gap_models> and <accountability_models> from <compensation_source>, <band_source>, <worker_source> and <attributes_in_scope>. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only those they leave open. For each counted unit on <review_date>, take the pay and the band the approved rules put in force, express pay on the approved pay basis, with any approved annualisation and hours scaling, place it against the band as approved, and keep that worker-level result apart from the published outputs, designated restricted to the approved readers. Publish only the approved aggregates at the approved cuts, including any approved pay gap between the approved comparison groups under the approved statistic, hiding every group below <minimum_group_size> as approved and publishing no identifier or pay value the approved hiding withholds. List every record the approved rules leave out or cannot place, with its reason, or name it in the failure where the approved policy fails the run; reconcile every input record, and keep sources read-only. Report what the hiding cannot protect.

## Verified by

- On a run that publishes, every input worker record lands once (or once per counted unit as approved) as counted (any approved flag shown), out of population, a further record of a counted unit, or an exception, and the classes sum to the input before hiding; a failed run names each bad record.
- On a run that publishes, pay and band records the rules do not use, such as orphaned, superseded, ambiguous, out-of-population or other-currency ones, are accounted for with their reasons and never silently dropped.
- Each counted unit's pay and band are the versions in force on the approved review date, or the approved earnings window ending on it, under the approved effective-dating and tie rules; later versions are never used, as-known only where the source shows entry times, and ties follow the approved rule.
- Pay follows the approved measure, annualisation, hours scaling and cap; a record whose pay, currency, frequency or hours cannot be evaluated follows the approved missing-value rule, is listed with its reason or named in a required failure, and is never silently read as zero or scaled by one.
- Placement follows the approved limits and edges, including workers exactly on each limit and bands with open or unusual limits, and the position against the band follows the approved definition and precision, using the band's stated midpoint where the rules do.
- Each published gap equals an independent recomputation from unit-level values under the approved measure, statistic, reference and precision; cuts are recomputed from their own workers, never averaged; a zero or absent reference gives a null with a reason; nothing missing is imputed unless approved.
- Distinct legal entities, currencies and jurisdictions are never pooled into one group, band or gap unless an approved rule says so, and any approved conversion states its rate source and date.
- A group is shown or hidden exactly as the approved minimum (distinct people unless another unit is approved), display rule and complementary hiding say; a hidden group carries no measure, a merged one only a combined measure that meets the minimum, and a gap needs the approved sides at the minimum.
- Published relations carry no worker or record identifier and nothing finer than the approved cut and group, only approved measures appear, sub-counts and counts of left-out records follow the approved hiding, and a group the rule hides shows no measure.
- Worker-level pay, exception lists and any list naming workers sit in separate relations marked restricted and named to the approved readers; where grants are approved, a role limited to the published relations cannot read them, otherwise access is reported unproven, not protected.
- The outcome states each disclosure limit the approved rules leave, and the hidden-cell count where the rule shows it, such as a hidden group derivable from a total, an overlapping cut, a restated release or a group whose members share a value or status, and never calls the output safe beyond them.
- Each approved rule value, such as the review date, minimum group size, reference group or band limits, changes the output where the data reaches it, within the approved rule form.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile the compensation, band and worker records (effective dates, frequencies, currencies, hours, levels, locations, employment types, attribute values and their blanks, duplicate record ids, concurrent jobs and rehires) before proposing rules. Use Ask first only for semantics still open, and record each decision as the user's own answer. Keep each approved date, threshold, list and limit as data a reader can change, keep the worker-level and exception relations apart from the published ones, and derive each published cut from the same group measure so they cannot disagree. Compare each published figure with an independent expectation computed from the inputs, never from the models. Report each exception left open and each disclosure limit the approved hiding leaves.

### Compose

- capturing-requirements
- applying-medallion-data-modelling
- generating-dbt-model
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, what is one counted unit (person, employment or assignment), which workers count on the review date (employment types, contractors, interns, leave, ended or not started), how concurrent jobs, rehires and several ids combine, and how are those left out shown?
- If unresolved, which review date, any earnings window ending on it, and time basis (as of, or as known) apply, how are the pay and band in force chosen, how are same-date conflicting records treated, and may later corrections restate a published report?
- If unresolved, which pay counts (base, allowances, bonus; contracted rate or actual earnings), how is it annualised and scaled for part-time hours with any cap, which currency applies, what rate source and date convert, may bands and pay differ in currency, and which records are exceptions instead?
- If unresolved, what defines a band (level, location, job family), are its limits inclusive or open-ended, any tolerance around them, is the midpoint stated or derived, and is position shown as a ratio to midpoint, a quartile or a percentage?
- If unresolved, which attributes (alone or combined, and on what lawful basis) and groups are compared, which is the reference, how are missing or undisclosed values handled, are entities or countries compared separately, is a statutory format needed (separate), and is any comparison published?
- If unresolved, which measures are published at each cut (counts, out-of-band split, position, gaps), which value the gap compares (pay or position in band), which statistic, headcount or FTE weighting, direction, unit and precision apply, which cuts are published, and are sub-counts hidden?
- If unresolved, what is the minimum group size (in distinct people), which outputs does it cover, is rounding applied, how is a hidden group shown (hidden, omitted, merged) and its count stated, are totals published, and is complementary hiding needed against overlapping cuts or restated releases?
- If unresolved, what happens to records that cannot be placed or evaluated (list and exclude, flag and keep, or fail the run), where are their counts shown, who may read the worker-level and exception relations, and are access grants applied?

### Guardrails

- Do not choose the population, counted unit, review date, pay measure, band rule, comparison groups, reference group, gap statistic, minimum size or display rule for the user, nor take them from the data or common practice; the user may ask for options or a recommendation.
- Never publish a worker or record identifier or a pay value for a group the approved rule hides, and report any disclosure the approved rules leave.
- Never impute a missing or undisclosed attribute, and never place such a worker in a comparison group unless the approved rules say so.
- Never silently read a missing pay, hours or band as zero or as out of band, and never convert a currency the approved rules do not convert; follow the approved rule, or list the record with its reason or name it in a required failure.
- Never average cell gaps or medians to make a level or company figure, never present a cross-band figure as a within-band comparison, and publish pooled cuts only as approved.
- Never pool distinct legal entities, currencies or jurisdictions into one group or gap because they share a band or level, unless the approved rules say so.
- Do not describe hiding small groups as anonymisation or aggregates as anonymous, and do not claim effective access control from build output alone.
- Stop at the check and the aggregate report: do not propose pay changes, build adjusted-gap models, edit the source records or grant access.
