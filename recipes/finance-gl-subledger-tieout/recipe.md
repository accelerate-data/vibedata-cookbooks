---
id: finance-gl-subledger-tieout
title: Tie the general ledger to its subledgers and classify every break
trigger:
  - Month-end close stalls because control accounts do not agree with their subledgers and the difference is worked out by hand in a spreadsheet.
  - The controller will not sign off until every control-account difference is explained, from late postings to manual journals, with nothing left unexplained.
  - An auditor asks why a control account differed from its subledger at a past period end, and someone has to rebuild the explanation by hand.
description: For each approved control account and period, set the general-ledger balance beside its subledger balance, explain the difference as breaks classed under the user's approved rules, leaving any residual visible as unexplained, and keep every record that cannot be processed visible as an exception, so no amount is lost, counted twice or absorbed to force a tie.
pitch: Reconcile every control account to its subledger with each break classified and nothing quietly absorbed.
job_category: build
area: transformation
readiness: supported
domain_objects:
  - general_ledger
  - journal_line
  - subledger_document
  - control_account
  - reconciliation_break
  - reconciliation_exception
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
  - Linking breaks to documents needs a document reference on ledger lines or an approved matching rule.
  - Reproducing a past tie-out after rule or source changes needs kept history of the tie-out.
  - Stops at the classified tie-out; correcting postings, sign-off and close packs are separate outcomes.
related:
  - effective-dated-business-rules
  - dbt-snapshot-history
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

Build <tieout_model>, <breaks_model> and <exceptions_model> from <general_ledger_source>, <subledger_sources> and <control_account_map>. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only the semantics they leave open. For each control account and period, set the ledger balance beside the subledger balance, explain the difference as classified breaks, leaving any residual visible as unexplained, list every record that cannot be processed as an exception, and keep sources read-only. Where break aging is requested, age each break as the approved rule says. Report what the inputs cannot prove.

## Verified by

- On a run that completes, for each in-scope control account and period, the classified break amounts, including any amount an approved tolerance allows and shown as such, sum exactly to the difference in the approved direction, or the residual is reported as unexplained.
- On a run that completes, in each period it affects, every amount of each in-scope ledger line and subledger record lands once: matched, in a break, or excluded with its record as an exception; none is lost or counted twice.
- Each break carries the class the approved rules and precedence give it, and no amount is attributed to two classes.
- Records just inside and just outside each approved window, tolerance edge and as-of date are classed as the approved rules say, including items still open at the as-of date.
- Netting, reversals, duplicates, sign errors, postings to the wrong account and postings with no document are handled and classed as the approved rules say.
- Where closing balances are compared, they start from the approved opening balances; a missing opening is reported, or fails the run, as the approved policy says, and is never defaulted to zero unless the approved semantics define it as zero.
- On a run that completes, every unprocessable record is listed with its reasons under the approved exception grain, and its effect on the tie-out follows the approved policy; a record left out is counted on the account it is reported on, or listed as unattributed.
- Where the approved policy fails the run on an unexplained residual, a missing opening or an unprocessable record, the run fails explicitly and names each offending account and period, opening or record, with its reason.
- Where break aging is requested, each break's age follows the approved start date and unit.
- Each break traces to the ledger lines and subledger records, or the opening balances, behind it, and each output is unique on its declared business grain with required fields populated.
- The outcome states which breaks and exceptions remain open and what the inputs cannot prove.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile the ledger lines (accounts, periods, posting dates, references, amounts and signs), each subledger's records and document types, and the control-account map, and check which ledger lines carry a usable document reference. Use Ask first only for semantics still open, and record each decision as the user's own answer. Keep the control-account map, break classes, precedence, tolerance and as-of date explicit, and editable where the approved requirements say so, and read opening balances from the approved source. The tie-out, breaks and exceptions must never disagree about a record. Report every break or exception left open and what the inputs cannot prove.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which control accounts, subledgers, legal entities, currencies and periods are in scope, and which period grain and fiscal calendar apply?
- If unresolved, what links a ledger line to a subledger record, which date or period places each side in a period, and are lines netted per record and period before comparing, or compared line by line?
- If unresolved, is the closing balance, the period's movement or both compared, which sign each document type carries on its control account, and which way is the difference taken?
- If unresolved, when is a difference timing rather than a missing posting, how long may it take to clear, and which as-of date judges items still open?
- If unresolved, which break classes exist and how is each identified, which wins when several fit, is there a rounding tolerance with an inclusive edge, may one record carry several breaks, and does an unexplained residual fail the run?
- If unresolved, where do opening balances come from for each control account and each side, how is a difference between the two openings shown, and what happens when one is missing?
- If unresolved, which records are exceptions rather than breaks, one row per reason or one primary reason, which account each is reported on, and is it excluded with a visible count, forcing the period unexplained or failing the run?
- If break aging is requested and unresolved, from which date is each break aged, and in what unit?

### Guardrails

- Do not choose break classes, precedence, tolerance, timing windows or exception handling for the user, and take none from the data or common practice; the user may ask for alternatives or a recommendation.
- Never absorb a residual into a class, an adjustment or a tolerance beyond what the approved rules allow to make a period tie; an amount within tolerance stays visible as such, and an unexplained difference stays visible.
- Never drop or double count a record; every record that cannot be processed stays visible as an exception with its reason.
- Never default a missing opening balance or amount to zero unless the approved semantics define absence as zero.
- Do not invent document links the source does not carry, or match on amount or date alone unless the approved rules say so; report unlinked lines under the approved rule.
- A break records a difference, not which side is wrong; do not assume the subledger or the ledger is correct.
- Stop at the classified tie-out: do not post corrections to the ledger or subledgers, and keep sources read-only.
