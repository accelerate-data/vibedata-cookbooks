---
id: life-sciences-enrollment
title: Build clinical-trial enrollment and site-performance models with every screened subject accounted for
trigger:
  - Clinical operations rebuilds enrollment and site performance in a spreadsheet each month, and nobody can say who was left out of the enrolled count or why a site looks slow.
  - Re-screens and people screened for more than one study are counted inconsistently, so enrolled counts and screen-failure rates cannot be defended.
  - Randomizations before a site was activated or after it closed, bad dates and subjects at unlisted sites sit in the counts or vanish from them without a trace.
  - A site that enrolled nobody in a month has no row, and a changed enrollment target is applied in the wrong period.
description: Classify every loaded screening record as an enrolled subject, a screen failure with one named reason or a record set aside or left out of scope with its reason, and publish study, site and month enrollment against the target in force, with screen-failure rate and time to first enrollment, tied back to the subjects.
pitch: Every screening record is enrolled, failed for a stated reason or set aside, and site performance ties back to the subjects.
job_category: build
area: transformation
readiness: supported
industry:
  - life-sciences
domain_objects:
  - screening_record
  - study_subject
  - enrollment_disposition
  - screen_failure_reason
  - site_month
  - enrollment_target
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
  - Screening records and the site list with dates must be landed; reasons and targets may be captured as data.
  - Stops at enrollment and site performance; forecasting, site selection and monitoring are separate.
  - Screenings at sites missing from the data cannot be seen, and are not claimed absent.
related:
  - effective-dated-business-rules
  - metric-population-and-rollups
  - business-event-fact
  - operational-state-duration
  - healthcare-readmission-cohort
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

Build <subject_dispositions>, <site_performance> and <enrollment_coverage> from <screening_records>, <site_list>, <enrollment_targets> and <screen_failure_reasons>. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only the semantics they leave open. At one row per screening record, give each loaded record exactly one disposition: an enrolled subject, a screen failure with one named reason, or a record set aside or left out of scope with its reason, such as an unusable or pending one. Publish the approved site performance by study, site and month, with subjects screened, screen failures, enrolled, cumulative enrolled against the target in force, screen-failure rate and days from activation to first enrollment, so that it ties back to the subjects. Keep the enrolled definition, the reasons, the rate definition and the target history as data the user can change, within the approved rule form. Publish what the inputs cannot prove.

## Verified by

- Every loaded screening record appears once with exactly one disposition and, if it did not enroll, one named reason; the enrolled, screen-failure and set-aside or out-of-scope counts add back to the number of records loaded.
- Under the approved subject identity and re-screening rules, a subject is enrolled at most once per study; a repeat screening is handled as approved and shown with its reason, and a person in two studies counts in each only where the rules say so.
- A record that is unusable by itself (duplicate, impossible or inconsistent date, site not on the list, unknown reason code) lands as approved with its reason and never hides or replaces a usable screening of the same subject.
- Enrolled follows the approved definition: a later withdrawal or status change does not un-enroll where the rules say so, and an enrolling event outside the site's activation and closure dates lands as approved with its reason.
- The site table has one row per approved study, site and month, including quiet months within the approved span of the site's life; every count lands in the month the approved date rule names.
- Cumulative enrolled is the running total through each month, shown with the target in force for that month under the approved target rule.
- The screen-failure rate uses the approved numerator and denominator and shows the approved value, never an unmarked zero, where nothing was screened; days to first enrollment shows the approved value until the study-site has enrolled someone.
- Before any approved suppression, the site table's counts equal the subjects' dispositions for the approved subject placement, and a subject with records at several sites counts where the rule places them; a suppressed figure is marked with its reason.
- Changing the enrolled definition, a screen-failure reason, the rate definition or a target in its data changes the outputs with no change to the logic, within the approved rule form.
- The coverage output publishes each accounting check (disposition add-back, one disposition per record, site table ties to subjects) with its residue; a check that does not hold is shown, never hidden.
- The dispositions and site figures equal results derived independently from the input records, and each site figure traces to the subjects behind it.
- The outcome states the count per reason, which subjects the data cannot place and what the inputs cannot prove, such as screenings at a site the data does not hold.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile the screening records (subject, study and site keys, consent, screening and randomization dates, outcome and reason codes, withdrawal), the site list with its dates and targets and the reason table before modelling. Use Ask first only for semantics still open, and record each decision as the user's own answer. Keep the enrolled definition, the reasons and their precedence, the rate definition, the month rule and the target history explicit and editable where the approved requirements say so. Evaluate the unusable checks as one ordered chain, so a record that trips two of them lands on one. Build the fixture with the awkward cases (re-screens, a person in two studies, duplicates, bad dates, a randomization outside a site's dates, an unlisted site, a site with a quiet month, a changed target) and derive independent expected results by hand before reading any output. The dispositions, the site table and the coverage must never disagree about a subject. Publish every set-aside record and what the inputs cannot prove.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which studies, sites and months are in scope, which key makes two screening records the same subject (within one study or across studies), and where do records outside scope, such as test or training subjects, go, shown with a reason?
- If unresolved, when a subject is screened more than once, is a later screening a re-screen or a new subject, which record represents them (an enrolled one, the earliest, the latest), and what happens to the others?
- If unresolved, which event makes a subject enrolled (randomization, consent, first dose), does a later withdrawal or status change un-enroll, and which wins when the outcome and the dates disagree?
- If unresolved, how are a duplicate row, an impossible or inconsistent date, a screening at a site not on the list, an unknown reason code, a screening with no outcome yet and an enrolling event outside the site's dates treated, and do set-aside subjects count as screened?
- If unresolved, what starts and ends a site's life, which months get a row, which date places each count in a month, what is each target set for (study, site, country, arm or cohort), how does a study cap or close apply, and how does a changed target apply?
- If unresolved, where does a subject with records at several sites count, what is the rate's numerator, denominator and rounding, and what shows for a month with nothing screened?
- If unresolved, what is the screen-failure vocabulary, which reason wins when several apply, and where does a failure with no reason go?
- If unresolved, who reads the outputs, may they carry subject identifiers, and is a small site or month suppressed, for which outputs, with complementary hiding?

### Guardrails

- Do not choose the subject identity, re-screening, enrolled definition, unusable-record, month, target and rate rules for the user, and take none from the data or common practice; the user may ask for alternatives or a recommendation.
- Never drop or double count a screening record or a subject; every record that is not enrolled stays visible with its reason.
- Never let a record that is unusable by itself replace or hide a usable screening of the same subject.
- Never merge a person across studies, or split a subject within one study, unless the approved identity rule says so.
- Never publish a subject identifier or name unless the approved requirements allow it.
- Stop at enrollment and site performance: do not forecast, select sites, monitor, manage data queries, analyse safety or write back to the source, which stays read-only.
