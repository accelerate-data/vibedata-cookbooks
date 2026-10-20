---
id: healthcare-readmission-cohort
title: Build a thirty-day readmission cohort with explicit exclusions
trigger:
  - The quality team rebuilds a readmission rate from a spreadsheet each quarter, and nobody can say who was left out of the rate or why.
  - Readmissions come from a self-join, so a patient with several returns is counted twice, a planned return counts against the hospital or a return to another facility is missed.
  - Deaths, transfers, discharges against medical advice and discharges too recent to have had a full follow-up window sit in the rate, or vanish from it without a trace.
description: Classify every loaded admission as an eligible index admission, an admission excluded for one named reason, or an admission set aside as unusable, link each eligible index to the admission that readmits it, and publish a readmission rate by facility and month that ties back to the cohort.
pitch: Every admission is an index, excluded for a stated reason or set aside, and the readmission rate ties back to it.
job_category: build
area: transformation
readiness: supported
industry:
  - healthcare
domain_objects:
  - admission
  - index_admission
  - readmission_link
  - exclusion_reason
  - readmission_rate
  - completeness_check
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
  - Admissions with patient, facility, dates, type, outcome and planned flag must already be landed as a table.
  - Stops at the cohort and rate; risk adjustment, cost, root cause and outreach are separate.
  - Readmissions to facilities missing from the data cannot be seen, and are not claimed absent.
related:
  - operational-state-duration
  - business-event-fact
evidence:
  features:
    - capturing-requirements
    - profiling-source-data
    - applying-medallion-data-modelling
    - generating-dbt-model
    - dbt-unit-testing
    - running-dbt-in-sandbox
    - verifying
  evals: []
---

## Prompt

Build <readmission_cohort>, <readmission_rate> and <cohort_coverage> from <admissions> and <exclusion_rules>. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only the semantics they leave open. At one row per admission, give each loaded admission exactly one disposition: an eligible index admission, an admission excluded for one named reason, or an admission set aside as unusable with its reason. Link each eligible index to the admission that readmits it under the approved window and readmission rules, and publish the approved readmission rate by facility and period so that it ties back to the cohort. Keep the window, the exclusion rules and the reason text as data the user can change, within the approved rule form. Publish what the inputs cannot prove.

## Verified by

- Every loaded admission appears once with exactly one disposition and, if it is not an eligible index, one named primary reason; the eligible, excluded and set-aside counts add back to the number of admissions loaded.
- Each eligible index shows whether a readmission followed within the approved window and, if so, which admission, where and after how many days; an admission exactly at the approved window edge counts or not as the approved rule says, and one day past it does not.
- Under the approved linking rule, where several admissions follow an index the rule picks the linked one, and where several indexes precede an admission the rule picks the index that claims it, so no readmission is counted twice unless the rule allows.
- An admission excluded from the index role stays visible with its reason and, where the approved rules allow, can still be the readmission of an earlier index; an admission the approved rules keep out of the readmission role is never linked.
- Where the approved rules let a readmission be the next index, a chain of consecutive admissions is evaluated admission by admission.
- An admission whose follow-up is not fully observed is shown as the approved rules say and is never counted as not readmitted.
- A duplicate, an overlapping pair, an inconsistent date, an unplaceable patient and an excluded visit type each land as approved with their reason: a copy that does not survive or a record set aside is never an index or linked, and none is silently dropped.
- The rate has one row per approved facility and period with its eligible index count, readmission count and rate, empty not zero where none was eligible; before any approved suppression its counts equal the cohort's, and a suppressed row is marked with its reason.
- Changing the window's edge rule or an exclusion in its data changes the cohort and rate with no change to the logic, within the approved rule form.
- The coverage output publishes each accounting check (disposition add-back, each link as the approved linking rule allows, rate ties to cohort) with its residue; a check that does not hold is shown, never hidden.
- The dispositions, links and rates equal figures derived independently from the input admissions, and each rate row traces to the admissions behind it.
- The outcome states the count per reason, which admissions the data cannot place and what the inputs cannot prove, such as a readmission to a facility the data does not hold.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile the admissions (patient and facility keys, admission and discharge dates and their types, admission type, discharge outcome, planned flag, repeats and overlaps) and the exclusion rules before modelling. Use Ask first only for semantics still open, and record each decision as the user's own answer. Keep the window, the inpatient types, the exclusion rules, the reason vocabulary and its precedence explicit and editable where the approved requirements say so. Evaluate the reasons as one ordered chain, so a stay that trips two of them lands on one. Derive independent expected results from the inputs by hand before reading any output, and probe with a repeated copy of an admission that is in a link. The cohort, the rate and the coverage must never disagree about an admission. Publish every set-aside admission, every admission whose follow-up is not observed and what the inputs cannot prove.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which facilities, periods, stay types and admission types are in scope, which key makes two admissions the same patient across facilities, and where do other visits, unplaceable patients and records outside scope go, shown with a reason?
- If unresolved, which date starts the thirty-day window and which ends it, and do a same-day return and the last day count?
- If unresolved, which later admissions count as a readmission (any facility or the same, all causes or related), how is a planned admission treated and a missing planned flag, which one is linked when several follow, and which index claims it?
- If unresolved, which discharge outcomes remove an index (a death, a transfer to another acute hospital, a discharge against medical advice, hospice or others), in what precedence, and can an excluded admission still be a readmission?
- If unresolved, against what date is follow-up complete, does a death or loss of coverage after discharge end it, and where does an index whose window is not fully observed go?
- If unresolved, how are a duplicate admission, an overlapping pair and an admission with a missing or inconsistent date treated, and which copy survives?
- If unresolved, what is the rate's denominator, is it attributed to the index or the readmitting facility, by which period, with what rounding, and is a small denominator suppressed, for which outputs, with complementary hiding?
- If unresolved, who reads the cohort, and may it carry patient identifiers or must they be withheld or pseudonymised?

### Guardrails

- Do not choose the window edges, exclusions and precedence, readmission and planned-admission rules, follow-up reference, duplicate and overlap rules, denominator or attribution for the user, and take none from the data or common practice; the user may ask for alternatives or a recommendation.
- Never drop or double count an admission; every admission that is not an eligible index stays visible with its reason.
- Never count an index as not readmitted when its follow-up is not fully observed.
- Never flatten a chain of admissions to one row per patient.
- Never publish a patient identifier or name in the cohort unless the approved requirements allow it.
- Stop at the cohort and rate: do not risk-adjust, standardise case mix, cost, analyse causes or write back to the admissions source, which stays read-only.
