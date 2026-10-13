---
id: finance-trial-balance-close
title: Produce the trial balance and close pack as code
trigger:
  - The close pack is rebuilt by hand every period and last quarter's trial balance cannot be reproduced as it was when the period closed.
  - Auditors ask what a closed period showed at its hard close and whether anything was posted into it afterwards.
  - Controllers need the journals posted after the soft close listed, and a hard stop when a closed period changes.
description: Build the trial balance by account and fiscal period with opening, debits, credits and closing, roll it up to statement lines, list late postings and invalid journals, and record each period at hard close so any later change to it is handled as the approved lock policy says.
pitch: Rebuild the trial balance and close pack from the ledger every period, with closed periods locked and every journal accounted for.
job_category: build
area: transformation
readiness: supported
function:
  - finance
domain_objects:
  - general_ledger
  - journal_entry
  - journal_line
  - chart_of_accounts
  - fiscal_period
  - trial_balance
  - period_close
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
  - Detecting a change to a closed period needs state that later builds and full refreshes do not rewrite.
  - Naming a changed line needs stable line ids; lateness and recording state at hard close need posting instants.
  - Stops at the close pack; subledger tie-out, consolidation, FX and posting corrections are separate outcomes.
related:
  - dbt-snapshot-history
  - effective-dated-business-rules
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

Build <trial_balance_model>, <statement_rollup_model>, <late_posting_model>, <invalid_journal_model> and <close_status_model> from <journal_source>, <chart_of_accounts>, <fiscal_calendar> and <close_calendar>. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only the semantics they leave open. At the approved grain (account and fiscal period, plus legal entity and currency wherever more than one is in scope), show opening, debits, credits and closing, roll the accounts up to the approved statement lines, apply the approved fiscal-year-end treatment, list journals posted after the soft close, and list every invalid journal with its reasons. Record each period's state when it passes its hard close, keep that record where later builds do not rewrite it, and handle any later change to a closed period as the approved lock policy says. Where the user asks for it, rebuild the trial balance as at a past instant. Keep sources read-only and report what the inputs cannot prove.

## Verified by

- On a run that completes, at each in-scope grain, closing equals opening plus debits minus credits, and each account in the approved chart appears in every in-scope period unless the approved semantics omit it, shown as they say when it has no balance.
- On a run that completes, within each period at each approved balancing grain, debits equal credits, closings net to zero and statement lines and the balance-sheet identity hold as approved, apart from any approved opening imbalance or flagged journal, each shown with its amount.
- Each period's closing becomes the next period's opening, except at a fiscal-year boundary, where the opening follows the approved year-end treatment.
- Each journal lands in the period the approved placement rule gives it; under an approved as-at instant, only lines the approved as-at rule places by then count, and later lines are reported as outside that run.
- Where lines carry a posting instant, journals posted after a period's soft close, up to its hard close, are listed as late with how late they were, honouring each boundary's approved inclusivity; otherwise lateness is reported as unproven.
- On a run that completes, every in-scope journal line lands once: in the trial balance (flagged where the approved policy includes its invalid journal) or excluded with its journal, listed with every reason; each period and grain shows what was excluded or flagged.
- Where the approved policy fails the run on an invalid journal, the run fails explicitly and names each offending journal and reason.
- Each period's record is taken as at its hard close where lines carry posting instants, otherwise as first observed after it and labelled so; it survives later builds and full refreshes, and where an approved reopen replaces it the earlier record is kept.
- A change to a closed period, as the approved definition counts one, is detected against its record; under a fail policy the run fails naming each period and grain, each line where line ids are stable, recorded and current figures, and publishes no close pack.
- Under a flag policy a changed closed period is published visibly flagged with the same change detail; under either policy, no close-pack output is published from data the closed-period check has not checked, and each period shows its close status.
- A requested past as-at rebuild counts only lines the approved as-at rule places by that instant, writes no closed-period record, and states which later in-place edits or deletions neither the source nor kept history lets it recover.
- Results do not change with the session time zone, each output is unique on its declared grain, and the outcome states what remains open and what the inputs cannot prove.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile the journal source (journal and line ids, types, periods, accounting dates, posting instants, accounts, debit and credit amounts, reversal links), the chart of accounts and its statement mapping, the fiscal and close calendars and any opening balances, and check whether posted lines can be edited or deleted in place. Use Ask first only for semantics still open, and record each decision as the user's own answer. Keep the chart, statement mapping, calendars, journal types, openings and the year-end rule explicit, and editable where the approved requirements say so. Keep the closed-period records and any approved reopen records where later builds and full refreshes cannot rewrite them, and never publish close-pack output from data the closed-period check has not checked. The trial balance, the invalid journals and the closed-period checks must never disagree about a line. Report every invalid journal, late posting or closed-period change left open and what the inputs cannot prove.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which ledger, legal entities, currencies and periods are in scope, which amount (ledger or transaction currency) is balanced, and does the grain include entity and currency (it must where more than one is in scope)?
- If unresolved, which fiscal calendar applies (year start, period grain, any adjustment period), which field places a journal in a period, and which instant does a run judge against, including rebuilds as at a past instant?
- If unresolved, when does each period soft-close and hard-close, for each entity if they differ, in which time zone, and is a posting exactly at a close instant on time or late?
- If unresolved, what are the chart of accounts, each account's type, normal balance and statement line, where do opening balances come from, must they balance, and how is an account with no balance or a missing opening shown?
- If unresolved, how are revenue and expense closed at fiscal-year end (a computed roll into a named retained-earnings account, or a closing journal already in the ledger), and how are reversals linked to their originals?
- If unresolved, which journal types exist, which journals are invalid, one row per reason or per journal, and is an invalid journal excluded with a visible count, failing the run, or, if it can be placed by account, period and amount, included and flagged?
- If unresolved, what is recorded at hard close, what counts as a change (a period's own postings, or also openings carried from earlier periods), does a change fail the run or flag the period (showing recorded or current figures), and can a period reopen, approved by whom, for how long?
- If unresolved, can the source edit or delete posted lines in place, are line ids stable, and does each line carry a posting instant?

### Guardrails

- Do not choose the calendar, close instants, year-end treatment, invalid-journal handling or lock policy for the user, and take none from the data or common practice; the user may ask for alternatives or a recommendation.
- Never let a build rewrite a closed period's record except through the approved reopen rule, and never downgrade an approved fail-on-change policy to a warning.
- Never drop or double count a journal line; an invalid journal stays visible with every reason.
- Never default a missing opening balance or amount to zero unless the approved semantics define absence as zero.
- Never net distinct legal entities or currencies together; consolidation and currency translation are separate outcomes.
- Do not infer an edit, deletion or posting time the source does not carry; report it as unproven.
- Stop at the close pack: do not post corrections or closing journals to the ledger, and keep sources read-only.
