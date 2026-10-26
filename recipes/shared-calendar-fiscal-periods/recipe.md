---
id: shared-calendar-fiscal-periods
title: Build one shared calendar and fiscal-period date table
trigger:
  - Two reports put the same day in different weeks, months, quarters or fiscal periods because each mart builds its own date logic.
  - Last year's comparison drifts whenever a fiscal year carries an extra week, or a business-day count ignores the holiday list.
  - Facts dated outside the date table, or with no date, silently drop out of the reports that join it.
description: Publish one date table, one row per day without gaps over an approved window, carrying calendar attributes, fiscal year, period, quarter and week, a business-day flag and a prior-year pointer under approved rules, with unplaceable dates handled as approved.
pitch: One date table every mart joins, so a day lands in the same fiscal period in every report.
job_category: build
area: transformation
readiness: supported
function:
  - cross-functional
domain_objects:
  - calendar_date
  - fiscal_calendar
  - fiscal_period
  - fiscal_week
  - holiday_calendar
  - business_day
  - prior_year_pointer
  - unknown_date_member
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
  - Where a holiday list applies, it must already be landed as a table; sourcing it is a separate outcome.
  - Does not convert time zones; the date basis each fact uses is approved per mart.
  - Stops at the date table; close, lock, period-to-date measures and mart rewiring are separate outcomes.
  - Once published, consumers take their periods from this table instead of rebuilding calendars.
related:
  - effective-dated-business-rules
  - finance-trial-balance-close
  - metric-population-and-rollups
  - customer-retention-churn-features
  - finance-budget-forecast-actual
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

Build <date_table_model> as the one governed date table every mart joins, from <fiscal_calendar_rules>, <holiday_source> and the <fact_date_columns> of the marts that join it. Inherit the Intent's platform, sources and approved requirements, and settle with the user only the calendar semantics they leave open. Publish one row per calendar day over the approved window, held as data and without gaps, carrying the approved calendar attributes and, for each approved fiscal calendar, the approved fiscal attributes (year, period, quarter, week) so each date has exactly one of each per calendar, a business-day flag and any approved number under the approved holiday rules with an indicator that tells a date the holiday list does not reach from one it covers, and the approved same-period-last-year pointer, showing the approved value with its reason where no counterpart exists. Account for every joining mart's fact dates as placed, handled as approved when missing or outside the window, or failed, keep every published column of any existing date relation unchanged unless approved, state which date basis each joining mart uses, and report what the inputs cannot prove.

## Verified by

- The table holds one row per calendar day from the approved window start to its end, each calendar-day key unique and not null with no day missing, and the window follows the approved rule, stated values or a stated derivation, never an unstated one derived from the facts at run time.
- Every fact date of every joining mart has a row or is handled as approved; a date outside the window or a null date is never placed on another day, and the count of each per mart is reported.
- Each date carries exactly one of each published fiscal year, period, quarter and week per approved fiscal calendar, agreeing as the approved week and period rules define, and fiscal identifiers equal those of any fiscal calendar the Domain already publishes, or each approved difference is stated.
- Where fiscal weeks are published, each fiscal year has the week count a hand-worked expectation states, including a year with an extra week and a first or last week cut short by the year boundary or window edge, computed under the approved week rule and never forced to a number it does not set.
- The business-day flag follows the approved weekday and holiday rules; a date the list does not reach shows the approved value and never false by default, the coverage indicator tells it from a covered date, and each approved business-day number restarts where approved counting only flagged days.
- The prior-year pointer names the counterpart under the approved alignment, which may fall in another period where the alignment is by week, and shows the approved value with its reason where none exists, such as the first year of the window.
- Extending the window adds rows and never changes a key; an existing date's attribute changes only where it depends on the window edge or on holiday coverage, and each such change is stated; a rebuild over identical inputs reproduces every row.
- Every column an existing date relation published keeps its name, type and value on the dates it already had unless an approved change says otherwise and is listed; a wider range, a new reader or a downstream value that changes on its next build is stated and its readers named.
- The documentation names which joining marts place a fact by which date basis, so a reader knows the table does not make different bases agree.
- Published identifiers, week counts, pointers, business-day numbers and window edges equal values derived independently from the approved rules, not from the table's own output.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements; ask only about calendar semantics they leave open. Sample data, vendor defaults and existing code are evidence, never policy. Profile first the existing date relations and every mart that joins or should join one (which date column each uses and the date range each covers), then any fiscal calendar the finance area already publishes, then the holiday list and the dates it reaches. Keep the window, fiscal calendar rules and holiday list as editable data, and extend an existing date relation in place unless the user approves a separate one. Write the expected week counts, identifiers and boundary dates by hand from the approved rules before building, covering each weekday a fiscal year can start on and each extra-week or leap case the approved calendar can produce. Compare the new table with the old one on the rows both hold, check that no unknown value became known by an expression that treats unknown as false, and probe the downstream models that read the table for a value that would change on their next build. State what the inputs cannot prove.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which fiscal calendars apply (one, or one per entity or region, with the key that identifies each) and for each: the year start, month or week-group periods (such as 4-4-5 or 13) and when an extra week is added, naming, any adjustment period, and any change over time.
- If unresolved, which fiscal and calendar attributes are published and how weeks are defined: week start day, week 1 (the year's first day, first full week or a majority-of-days rule), which year a straddling week belongs to, the week-year rule, weekend days and name language.
- If unresolved, what window the table covers and how it is bounded (stated start, end and forward horizon, whole fiscal years or not, or a stated derivation), and who extends it.
- If unresolved, which holiday list applies and the dates it covers, what makes a working day (weekdays, observed holidays, local days off, half days), and what a date outside the list's coverage shows.
- If unresolved, which business-day numbers are published and where each restarts, and how same-period-last-year aligns (same date, same week index and weekday, or same period) and what is shown where no counterpart exists.
- If unresolved, how a null, unparseable, out-of-window or not-yet-occurred fact date is handled (unknown member, set aside, flagged or the run failed), how that member is keyed and how it is kept out of day counts.
- If unresolved, which existing date relations and consumers join the table, whether it extends one in place or stands alone, and whether a published column may be added, changed or widened.
- If unresolved, which date or time zone places each joining mart's facts, and whether any mart is restated or only documented.

### Guardrails

- Do not choose the fiscal calendar, week construction, calendar attributes, year naming, window, holiday rules, business-day numbering, prior-year alignment, unknown-date handling or calendar grain for the user, and take none from sample data, a vendor default or existing code.
- Never derive the window from the facts at run time by an unstated rule, or hard-code a date in the model; extending the window adds rows and changes no key.
- Never place a null, unparseable or out-of-window fact date on another real day; it follows the approved handling and its count is reported.
- Never force a fiscal year's week count to a number the approved week rule does not set; a year with an extra or partial week is computed and checked against the hand-worked expectation.
- Never show a holiday or non-working answer the list does not support as known unless the user approves that value for uncovered dates; the coverage indicator shows which dates the list reaches.
- Never let an expression turn an unknown into a known value on rows an existing date relation published as unknown unless the user approves that change; compare those rows with the old table before accepting.
- Never count the unknown-date member as a day: it stays out of day counts, gap checks and any serving date list.
- Never change a published value of an existing date relation or restate a mart without approval; a downstream value that changes on its next build is stated, not hidden.
- Stop at the date table: do not convert timestamps between time zones, source a holiday list, close or lock periods, build period-to-date measures or rewire marts.
