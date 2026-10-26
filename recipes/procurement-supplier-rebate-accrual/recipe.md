---
id: procurement-supplier-rebate-accrual
title: Accrue supplier rebates from purchasing contracts and reconcile settlements
trigger:
  - Procurement cannot say how much supplier rebate has been earned under each purchasing agreement this period, or how much of it suppliers have already credited.
  - Tiered agreements, returns and agreement changes are worked out by hand, so nobody can tell why an accrual moved or whether a supplier credit was counted twice.
  - Finance books a rebate receivable that does not tie to the agreements, because returns, restated agreements or an over-paid credit are missing from it.
description: Place purchases under the approved agreement version, net approved returns, compute each contract period's rebate entitlement under the approved tier method, and publish an accrual and settlement ledger that rolls forward, with every in-scope record that accrues or settles nothing listed and what the scope leaves out shown or counted as approved.
pitch: See what each supplier owes you under each approved contract, how it moved and what suppliers have already credited.
job_category: build
area: transformation
readiness: supported
function:
  - finance
  - supply-chain-ops
domain_objects:
  - supplier
  - supplier_contract
  - agreement_version
  - rebate_tier
  - purchase_line
  - purchase_return
  - vendor_credit
  - rebate_entitlement
  - rebate_accrual_ledger
  - rebate_exception
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
  - Produces evidence for review; it does not post, collect or pay a rebate or write back to a source system.
  - Stops at the contract-based amount; spend cubes, invoice matching, usage charges and forecasts are separate.
  - Accrues the rebate earned on purchases made so far; it does not project where a contract period will end.
  - Returns and credits link to a purchase line or agreement by an explicit reference or an approved linking rule.
  - Agreement terms and credits may be captured as editable data during the run if no source holds them.
  - A rebate term the approved rule form cannot express is listed as unmodelled, never ignored.
  - Without recorded dates on versions, returns or credits, their period placement is reported unproven.
related:
  - ops-procurement-spend
  - procurement-three-way-match
  - finance-duplicate-invoice-detection
  - effective-dated-business-rules
evidence:
  features:
    - capturing-requirements
    - generating-dbt-model
    - verifying
  evals: []
---

## Prompt

Build <contract_period_entitlement_model>, <accrual_ledger_model> and <rebate_exception_model> from <purchase_lines_source>, <return_lines_source>, <supplier_agreements_source>, <agreement_versions_source>, <tier_bands>, <qualifying_products_source>, <rebate_credits_source> and, where approved, <opening_accruals>. Inherit the Intent's established semantics and ask only what it leaves open. Place each purchase under the approved agreement version in force, net the approved returns, compute each contract period's rebate entitlement under the approved tier method, and publish a ledger where opening accrual plus earned rebate plus adjustments minus settlements equals closing accrual. A threshold applies the named tier method, a return lowers qualifying purchases as approved, a change applies as approved with any restatement shown as an adjustment, and one supplier credit reduces the accrual once and never also counts as earned. Keep agreement terms, rates and unit factors as editable data, list every in-scope record that accrues or settles nothing with its amount and reason, show or count what the scope leaves out, and report what the inputs cannot prove.

## Verified by

- Every in-scope purchase, return and credit is accrued or applied, or listed with its amount and the reason or reasons the approved rules give, and applied plus listed amounts add back to the record; an approved-identity repeat is never counted twice, and left-out records are shown or counted.
- Published entitlements, ledger rows and exceptions equal values derived independently from the sources and the approved rules, to the approved rounding, and no purchase is accrued that the approved rules do not qualify.
- A base that crosses a threshold, and one exactly on it, earns what the approved tier method and edge rule give, and the same base earns what each approved method gives where agreements differ.
- An approved return lowers qualifying purchases in the approved period and can pull a base under a threshold; one set aside is listed. A closed or settled period's rows are not rewritten unless an approved rule restates them, and a late or revised record follows the same rule.
- An agreement change applies only to what the approved version rule says, and a restatement shows its difference, as a labelled adjustment where the rule posts one; earlier periods keep their rows unless approved.
- Each credit amount appears once, in settlements, and in no earned or adjustment figure; a credit that is not a rebate settlement is listed or counted as approved, and one seen twice or repeated with a different amount follows the approved identity rule.
- For every ledger row, opening accrual plus earned rebate plus adjustments minus settlements applied equals closing up to the approved rounding; an excess the approved rule keeps out of the balance is shown beside it. Each opening equals the prior closing, and the first equals the approved opening.
- A credit larger than the accrual follows the approved disposition, and the uncovered amount stays visible, never hidden in a balance or netted across agreements unless approved.
- A purchase under no agreement, under several, of a non-qualifying product or in no contract period follows the approved rule and accrues under an agreement only as that rule allows, never twice under one; an in-scope one not accrued is listed with amount and reason.
- Each contract period's entitlement equals the earned rebate plus the adjustments the ledger attributes to it, wherever they post, and a ledger period with no activity carries its balance as approved.
- Changing an approved tier band, qualifying product, agreement version, contract period, rate or unit factor changes the result accordingly without a code change, within the approved rule form, and the same inputs give the same ledger on a rerun.
- Each output is unique on its approved grain (for the ledger, such as agreement, ledger period, currency and, where approved, entity); shares of a base spanning entities or currencies are allocated as approved; each output names its period, states what is unproven, and posts or pays nothing.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile the sources first: how purchases, returns and credits cite an agreement or purchase line, whether the same record arrives twice, how versions carry effective and recorded dates, which products each agreement covers, and the units, currencies and dates present. Use Ask first only for semantics still open, and record each decision as the user's own answer. Keep tier bands, versions, qualifying products, contract periods, rates and unit factors as editable data. Compute expected entitlements, ledger rows and exceptions independently of the models from the source rows and the approved rules, and test a base exactly on a threshold edge, a crossing under each approved tier method, a return that pulls a base under a threshold, a return for a closed period, a late purchase, each approved version mode, a purchase under no or several agreements, a credit seen twice or conflicting or above the accrual, a non-qualifying product, another currency, a volume base with converted units, a period with no activity and an opening balance. Report every exception and what the inputs cannot prove.

### Compose

- capturing-requirements
- profiling-source-data
- generating-dbt-model
- verifying

### Ask first

- If unresolved, which suppliers, entities and purchase types are in scope, which fields place a purchase under an agreement, what one under none, several or outside its period does (set aside, accrue under each, or by priority), and are left-out records listed or counted?
- If unresolved, how a contract period and a ledger period are defined, whether the base is spend or volume, which date, time zone and amount (order, receipt, invoice) place a purchase, the ledger grain with any entity split, and where the first opening accrual comes from?
- If unresolved, which tier method each agreement uses (the rate on each slice or the reached tier's rate on the whole base), how a base on a threshold is treated, whether tiers accumulate over the contract period, and whether a baseline, cap or floor applies?
- If unresolved, which agreement version applies (by effective or recorded date), whether a change is prospective or restates the period, how far and where its difference posts, what closes or settles a period, and what a late or revised record does after it?
- If unresolved, which reference links a return to its purchase line, which returns reduce the base, which period they reduce, where the adjustment posts, and what a return larger than its purchase or naming no purchase does?
- If unresolved, which credit types settle a rebate (credit note, cash, deduction, goods), what links a credit to an agreement and sets its month, and what identifies a purchase, return or credit sent twice, which copy counts and how a conflicting one is treated?
- If unresolved, how a credit larger than the accrual is treated (a negative balance, a carry forward, or a cap with the excess listed), and how a record with several reasons, or a zero, missing or negative amount, is listed?
- If unresolved, is the outcome in one currency (and how another is treated) or converted at an approved rate and date, how units convert for a volume base and a quantity with no factor is treated, and at what point and mode an amount is rounded?

### Guardrails

- Do not choose the tier method, boundary rule, linking rule, version, return, credit or over-settlement treatment, opening accrual or period closing for the user, and take none from the data, a vendor default or common practice; the user may ask for alternatives or a recommendation.
- Never hard-code a rate, band, boundary rule, qualifying product, agreement version or unit factor in the models; a change to them must change the result without a code change, within the approved rule form.
- Never place a purchase under an agreement by a key the user has not approved, or accrue a purchase under no agreement, a non-qualifying product or one in no contract period unless an approved rule says so, or twice under one agreement; list or count the rest as approved.
- Never let one credit reduce the accrual twice, count as earned rebate or apply to a different agreement than the one it names unless approved.
- Never rewrite a closed or settled period's rows silently; a change to an earlier figure posts as a labelled adjustment unless an approved rule restates it, and an over-settlement or negative balance is shown, never hidden or netted across agreements unless approved.
- Never project where a contract period will end or accrue a tier the purchases so far have not reached.
- Never convert a currency or unit without an approved rate or factor, or equate a missing amount with zero.
- Do not post, collect, claim or pay a rebate or write back to any purchasing, ledger or payment system; the output is evidence for a reviewer.
- Stop at the contract-based amount: do not build the spend cube, verify invoices against orders and receipts, compute customer usage charges or detect duplicate invoices.
