---
id: people-pay-band-gaps
title: Check pay against salary bands and report pay gaps at an aggregate grain
trigger:
  - A pay-equity review is due and compensation data cannot leave HR unmasked.
  - Managers are told people are paid outside the band, but nobody can say how many, where, or on which band version.
  - HR is asked for pay gaps between groups and cannot tell whether a published number exposes a small group.
description: For the approved review date, place each counted worker's pay against the band in force, keep that worker-level result in a separate restricted relation set, and publish only aggregates with the approved small-group hiding, while every record is accounted for.
pitch: Check pay against salary bands and publish pay gaps by group with small groups hidden, keeping worker-level pay in a separate restricted set.
job_category: build
area: governance-cost
readiness: supported
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

Build <restricted_worker_pay_model>, <published_pay_gap_models> and <accountability_models> from <compensation_source>, <band_source>, <worker_source> and <attributes_in_scope>. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only those they leave open. For each counted unit on <review_date>, take the pay and the band the approved rules put in force, express pay on the approved annual and full-time basis, place it against the band as approved, and keep that worker-level result in a separate relation set designated restricted to the approved readers. Publish only the approved aggregates at the approved cuts, including the pay gap between the approved comparison groups under the approved statistic, hiding every group below <minimum_group_size> as approved and publishing nothing that identifies a person. List every record the approved rules leave out or cannot place, with its reason, or name it in the failure where the approved policy fails the run; reconcile every input record, and keep sources read-only. Report what the hiding cannot protect.

## Verified by

- On a run that publishes, every input worker record lands once (or once per counted unit as approved) as counted, out of population, a further record, flagged in its own class, or an exception with reasons, and the classes sum to the input; a failed run names each offending record.
- On a run that publishes, pay and band records the rules do not use, such as orphaned, superseded, ambiguous, out-of-population or other-currency ones, are accounted for with their reasons and never silently dropped.
- Each counted unit's pay and band are the versions in force on the approved review date under the approved effective-dating and tie rules; a version dated after it is never used, and conflicting pay records follow the approved rule rather than row order.
- Annual and full-time-scaled pay follow the approved pay measure, annualisation, hours basis and cap; a record whose pay, currency, frequency or hours cannot be evaluated is listed with its reason, or named in a failure the policy requires, never scaled by one or read as zero.
- Placement follows the approved limits and edges, including workers exactly on each limit and bands with open or unusual limits, and the position against the band follows the approved definition and precision, using the band's stated midpoint where the rules do.
- Each published gap equals an independent recomputation from unit-level values of the approved measure, statistic, direction, reference group and precision; cuts are recomputed from their own workers, never averaged, a zero or absent reference gives a stated null, and no missing value is imputed.
- Distinct legal entities, currencies and jurisdictions are never pooled into one group, band or gap unless an approved rule says so, and any approved conversion states its rate source and date.
- A group is shown or hidden exactly as the approved minimum, counted unit, display rule and any complementary hiding say, the minimum counting distinct people; a hidden group carries no measure, and the number of hidden cells is stated.
- Published relations carry no worker or record identifier and nothing finer than the approved cut and group, only approved measures appear, sub-counts and counts of left-out records follow the approved hiding, and a group the rule hides shows no measure.
- Worker-level pay, exception lists and any list naming workers sit in a separate relation set designated restricted, and the outcome names who must be granted access; build output alone proves no access control.
- The outcome states every disclosure limit the approved rules leave, such as a hidden group derivable from a total, an overlapping cut or a repeated or restated release, and never calls the output safe to release beyond them.
- Each approved rule held as editable data, such as the review date, minimum group size, reference group or band limits, changes the output when its value changes, within the approved rule form.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile the compensation, band and worker records (effective dates, frequencies, currencies, hours, levels, locations, employment types, attribute values and their blanks, duplicate record ids, concurrent jobs and rehires) before proposing rules. Use Ask first only for semantics still open, and record each decision as the user's own answer. Hold each approved date, threshold, list and limit as editable data, keep the worker-level and exception relations apart from the published ones, and derive each published cut from the same group measure so they cannot disagree. Compare each published figure with an independent expectation computed from the inputs, never from the models. Report each exception left open and each disclosure limit the approved hiding leaves.

### Compose

- capturing-requirements
- applying-medallion-data-modelling
- generating-dbt-model
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, what is one counted unit (person, employment or assignment), which workers count on the review date (employment types, contractors, interns, leave, ended or not started), how concurrent jobs, rehires and several ids combine, and how are those left out shown?
- If unresolved, which review date applies, how are the pay and band in force chosen, how are same-date conflicting records treated, and may later corrections restate a published report?
- If unresolved, which pay counts (base, allowances, bonus), how is it annualised and scaled for part-time hours, which currency applies, any cap on the full-time factor, what rate source and date convert, may bands and pay differ in currency, and which records are exceptions instead?
- If unresolved, what defines a band (level, location, job family), are its limits inclusive or open-ended, any tolerance around them, is the midpoint stated or derived, and is position shown as a ratio to midpoint, a quartile or a percentage?
- If unresolved, which attributes, alone or combined, and whether using them is permitted, which groups are compared, which group is the reference, how are missing or undisclosed values handled, are entities or countries compared separately, and is any comparison published at all?
- If unresolved, which measures are published at each cut (counts, out-of-band split, position, gaps), which value the gap compares (pay or position in band), which statistic, direction, unit and precision apply, which cuts are published, and are sub-counts hidden?
- If unresolved, what is the minimum group size (in distinct people, whichever unit is counted), how is a hidden group shown (hidden, omitted, merged), are totals published, is complementary hiding required, and how are overlapping cuts and repeated or restated releases kept from revealing one?
- If unresolved, what happens to records that cannot be placed or evaluated (list and exclude, flag, or fail the run), where are their counts shown, and who may read the worker-level and exception relations?

### Guardrails

- Do not choose the population, counted unit, review date, pay measure, band rule, comparison groups, reference group, gap statistic, minimum size or display rule for the user, nor take them from the data or common practice; the user may ask for options or a recommendation.
- Never publish a worker or record identifier, a pay value for a group the approved rule hides, or any measure that lets one person's pay be read.
- Never impute a missing or undisclosed attribute, and never place such a worker in a comparison group unless the approved rules say so.
- Never read a missing pay, hours or band as zero or as out of band, and never convert a currency the approved rules do not convert; list the record with its reason, or name it in a failure the policy requires, instead.
- Never average cell gaps or medians to make a level or company figure, never present a cross-band figure as a within-band comparison, and publish pooled cuts only as approved.
- Never pool distinct legal entities, currencies or jurisdictions into one group or gap because they share a band or level, unless the approved rules say so.
- Do not describe hiding small groups as anonymisation, and do not claim effective access control from build output alone.
- Stop at the check and the aggregate report: do not propose pay changes, build adjusted-gap models, edit the source records or grant access.
