---
id: finance-duplicate-invoice-detection
title: Detect duplicate invoice candidates from explicit matching rules before payment
trigger:
  - Accounts payable paid the same supplier invoice twice and only found out when the supplier returned the money.
  - Before each payment run, accounts payable wants the suspected duplicate invoices to hold for review, with the rule that flagged each one.
  - The payables system only catches an exact repeat of the invoice number, so re-keyed numbers and invoices entered under a second supplier record slip through.
description: Compare in-scope supplier invoices under the user's approved matching rules, list every candidate duplicate pair with the rules that matched, list every invoice once with whether it is a candidate and whether it is held for review and why, and keep every record that cannot be checked visible, as an exception or in an explicit run failure, so no invoice is lost, counted twice or silently cleared.
pitch: Catch suspected duplicate supplier invoices before they are paid, with the rule behind every match and a hold list the team can act on.
job_category: build
area: data-quality
readiness: supported
domain_objects:
  - accounts_payable
  - supplier_invoice
  - supplier
  - payment
  - duplicate_candidate
  - matching_rule
  - payment_hold
  - review_decision
  - invoice_exception
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
  - Produces a candidate and hold list; it does not block, release or post anything in the payables or payment system.
  - Stops at duplicate candidates; purchase order matching, recovering paid duplicates and supplier clean-up are separate.
  - Results as known on a past date need entry timestamps or kept snapshots of the results.
  - Past hold lists are not kept; a rule or list change restates every result.
related:
  - finance-ap-aging
  - identity-golden-record-crosswalk
  - identity-standardize-names-addresses
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

Build <candidate_pairs_model>, <invoice_register_model> and <exceptions_model> from <supplier_invoices_source>, <matching_rules>, <review_decisions> and, where recorded separately, <payments_source>. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only the semantics they leave open. For the approved as-of date, compare in-scope invoices under the approved matching rules at the approved grain (legal entity and currency wherever they apply), list every candidate pair as approved, with every rule that matched and its primary rule, list every register record once with whether it was checked, left out or excepted, whether it is a candidate and whether it is held for review and why, apply reviewer decisions as approved, and list every record that cannot be checked as an exception, or fail the run naming it, as the approved policy says. Keep the matching rules, lists and reviewer decisions as editable data. Keep sources read-only. Report what the inputs cannot prove.

## Verified by

- On a run that completes, every input record, including those the scope leaves out or whose identity cannot be resolved, appears once in the register as checked, left out with its reason, or excepted with its reasons; counts at the approved grain, with entity and currency, equal the input's.
- Each pair an enabled rule matches appears once in either order unless approved rules flag or omit it, listing every matching rule and the primary one by priority; other pairs only where approved, via named linking records; no record pairs with itself or a copy the repeat rule deems the same.
- Records are compared only within the approved grain; records of different legal entities or currencies never pair unless an approved consolidation or translation rule says so, and then under that rule.
- Number and supplier normalisation, amount tolerance, date gap and lookback follow the approved rules, including records exactly on each edge and one step beyond it.
- Records the approved rules leave out (by type, status or date) are never compared, and records that cannot be checked are compared only as far as the approved rules allow.
- On a run that completes, every invoice the approved hold rule names is held once with every reason that applies, no other invoice is held, and paid or settled status and pairs with paid sides affect holds and reporting only as approved.
- Reviewer decisions apply as approved; each decision the approved policy does not apply (stale, conflicting or unknown) is reported with its reason and changes no hold.
- Repeated deliveries of one record are treated as approved; beyond what that rule keeps as separate records, no invoice is counted twice or held twice for one reason.
- Changing an approved rule's values, its fields within the approved rule form, its priority or enablement, an approved scope list entry, a reviewer decision or the as-of date changes the result accordingly without a code change.
- Where the approved policy fails the run on a record that cannot be checked, the run fails explicitly and names each offending record with its reason; other outputs need not be produced, and the other conditions apply to runs that complete.
- On a run that completes, the candidate list, the invoice register and the exceptions agree about every record, and each output is unique on its declared business grain with required fields populated.
- The outcome states which candidates, holds and exceptions remain open and what the inputs cannot prove, including that no hold was applied in the payment system.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile the invoice register first: document types, statuses, entities, currencies, supplier ids, how invoice numbers are written, amounts, the dates present (invoice, entry, payment) and whether one record can arrive more than once. Use Ask first only for semantics still open, and record each decision as the user's own answer. Hold each matching rule as editable data (which fields it compares and how, its tolerance, date gap, lookback and priority) so the team can add or change a rule without code, and keep the in-scope lists and reviewer decisions editable too. Where the register is too large to compare every pair, narrow each rule's comparisons only on fields that rule requires to be equal, so no pair a rule would match is dropped, and confirm on a representative sample that the result equals the full comparison. Keep each record's placement consistent across the candidate list, the register and the exceptions; derive pair results and holds only for the record that was actually compared. Test each rule's edges and each placement on records that fail several checks at once, and recompute the expected results independently of the models. Report every candidate, hold and exception left open and what the inputs cannot prove.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which document types, statuses, legal entities, currencies and suppliers are in scope, at what grain records are compared, and is any cross-entity or cross-currency match wanted, under which mapping or rates?
- If unresolved, which matching rules apply (fields compared, which amount: gross, net or tax, in document or ledger currency; number and supplier normalisation; tolerance, date gap, lookback), in what priority, and is a pair reported only when a rule matches it directly?
- If unresolved, which records are compared (unpaid only, paid as well, voided or cancelled), and are duplicates already paid on both sides reported, flagged on the register or left out?
- If unresolved, what makes an invoice paid or settled at the as-of (a payment date, a status, payment records, partial payments, credit notes or reversals applied), which as-of date applies, and are results from business dates or as known then?
- If unresolved, which invoices go on the hold list: every unpaid side of a candidate, only the later-entered one, or by rule; and what do cleared and confirmed reviewer decisions change?
- If unresolved, which records cannot be checked, are they still compared by the rules their fields allow, and are they held, only listed as exceptions, or does the run fail naming them?
- If unresolved, what identifies one register record (document id, header or line, and how lines roll up), and how is a record delivered more than once treated, both when the copies are identical and when they differ?
- If unresolved, how are reviewer decisions keyed, and what happens to a decision that no longer matches a pair, conflicts with another or carries an unknown value?

### Guardrails

- Do not choose the matching rules, normalisation, tolerances, windows, compared population, hold rule or exception handling for the user, and take none from the data, a vendor default or common practice; the user may ask for alternatives or a recommendation.
- Never compare or pair records across legal entities or currencies, or link supplier records as one supplier, unless an approved rule or source says so.
- Never drop, double count or silently clear an input record; records the approved scope leaves out stay visible with their reason, and every record that cannot be checked stays visible, as an exception or in an explicit run failure, with its reasons.
- Never report a record that cannot be checked as checked and clear, and never let a paid status, a reviewer decision or a repeated copy release a hold the approved rules keep.
- Never default a missing amount to zero, or fill a missing supplier, invoice number or date, unless the approved semantics say so; otherwise a record missing a field a rule compares cannot be checked by that rule.
- Do not claim results as known on a past date unless the source carries entry timestamps or kept snapshots; otherwise compute from business dates only with the user's approval and report that backdated entries restate results.
- Do not hard-code a rule value, list entry or the as-of date in the models; a change to them must change the result without a code change.
- Do not block, release or edit invoices or payments in the source or payment systems; the hold list is a report for the team.
- Stop at duplicate candidates and holds: do not recover money already paid, match purchase orders and receipts, or merge supplier master records.
