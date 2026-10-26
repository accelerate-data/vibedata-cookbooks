---
id: procurement-supplier-rebate-accrual
title: Accrue supplier rebates from purchasing contracts and reconcile settlements
trigger:
  - Procurement cannot say how much supplier rebate has been earned under each purchasing agreement this period, or how much of it suppliers have already credited.
  - Tiered agreements, returns and agreement changes are worked out by hand, so nobody can tell why an accrual moved or whether a supplier credit was counted twice.
  - Finance books a rebate receivable that does not tie to the agreements, because returns, restated agreements or an over-paid credit are missing from it.
description: For the approved as-of date, qualify purchases under the approved agreement version, net approved returns, compute each contract period's rebate entitlement under the approved tier method, and publish an accrual and settlement ledger that rolls forward, with every excluded purchase, return and credit listed.
pitch: See what each supplier owes you under every contract, how it moved and what suppliers have already credited.
job_category: build
area: transformation
readiness: supported
function:
  - finance
  - supply-chain-ops
domain_objects:
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
  - Accrues only purchases made up to the as-of date and does not project where a contract period will end.
  - Returns and credits link to a purchase line or agreement by an explicit reference or an approved linking rule.
  - Agreement terms and credits may be captured as editable data during the run if no source holds them.
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

Build <contract_period_entitlement_model>, <accrual_ledger_model> and <rebate_exception_model> from <purchase_lines_source>, <return_lines_source>, <supplier_agreements_source>, <agreement_versions_source>, <tier_bands>, <qualifying_products_source> and <rebate_credits_source>. Inherit the semantics the Intent already establishes, and resolve with the user only what it leaves open. For the approved as-of date, qualify each purchase under the one approved agreement version in force, net the approved returns, compute each contract period's rebate entitlement under the approved tier method, and publish a ledger where opening accrual plus earned rebate plus adjustments minus settlements equals closing accrual. A threshold applies the named tier method, a return lowers qualifying purchases as approved, an agreement change applies as approved with any restatement shown as an adjustment, and one supplier credit reduces the accrual once and never also counts as earned. Keep tiers, versions, qualifying products and periods as editable data, list every purchase, return and credit that accrues or settles nothing with its amount and reason, and report what the inputs cannot prove.

## Verified by

- Every purchase, return and credit in the approved scope is accrued or applied once, or listed once with its amount and one reason; records the scope leaves out are shown or counted with their reason as approved, and a repeated record is never counted twice.
- Published entitlements equal values derived independently from the sources and the approved rules, to the approved rounding, and no purchase is accrued that the approved rules do not qualify.
- A base that crosses a threshold, and one exactly on it, earns what the approved tier method and edge rule give, and the same base earns what each approved method gives where agreements differ.
- A return lowers qualifying purchases in the approved period, can pull a base back under a threshold, and its effect posts as approved; a settled period's earlier rows are not rewritten unless an approved rule restates them.
- An agreement change applies only to what the approved version rule says, and a restatement shows its difference as a labelled adjustment in the approved period; earlier periods keep their rows unless approved.
- One supplier credit reduces the accrual once and never also counts as earned rebate or as a second benefit; a credit seen twice, or repeated with a different amount, follows the approved identity rule.
- For every ledger row, opening accrual plus earned rebate plus adjustments minus settlements equals closing accrual up to the approved rounding, plus any over-settlement the approved rule shows beside it, and each opening equals the prior closing.
- A credit larger than the accrual follows the approved disposition, and the uncovered amount stays visible, never hidden in a balance or netted across agreements unless approved.
- A purchase under no agreement, under more than one, of a non-qualifying product or outside every contract period follows the approved rule and is accrued at most once; any not accrued is listed with its amount and reason, and no listed amount enters an accrued figure.
- Each contract period's entitlement equals the earned rebate plus the adjustments the ledger attributes to it, wherever they post, and a ledger period with no activity keeps its balance carried.
- Changing an approved tier band, qualifying product, agreement version or as-of date changes the result accordingly without a code change, within the approved rule form, and the same inputs give the same ledger on a rerun.
- On a run that completes, each output is unique on its declared grain with required fields populated, every figure carries the as-of date it describes, the outcome states what the inputs cannot prove, and no output posts, collects or pays anything.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile the sources first: how returns cite their purchase line, how credits cite an agreement and whether the same credit arrives in more than one input, how agreement versions carry effective and recorded dates, which products each agreement covers, and the units, currencies and dates present. Use Ask first only for semantics still open, and record each decision as the user's own answer. Keep tier bands, versions, qualifying products and contract periods as editable data. Compute the expected entitlements and ledger by hand from the source rows and the approved rules before building, so no check repeats the implementation, and test a base exactly on a threshold edge, a threshold crossing under each approved tier method, a return that pulls a base under a threshold, a return for an already settled period, each approved version mode, a credit seen twice and one that conflicts, a credit larger than the accrual, a purchase under no agreement or under two, a non-qualifying product, another currency and a period with no activity. Report every exception and what the inputs cannot prove.

### Compose

- capturing-requirements
- generating-dbt-model
- verifying

### Ask first

- If unresolved, which suppliers, entities and purchase types are in scope, which products qualify and what the base includes (tax, freight, discount), are left-out records listed or counted, and what happens to a purchase under no, overlapping or out-of-period agreements?
- If unresolved, how a contract period and a ledger period (such as a month) are defined for each agreement, whether the base is spend or volume, which date places a purchase in a period (order, receipt, invoice or posting), and which as-of date, cutoff time and zone apply?
- If unresolved, which tier method each agreement uses (the rate on each slice or the reached tier's rate on the whole base), how a base exactly on a threshold is treated, whether tiers accumulate across the contract period, and how a gap or overlap between bands is handled?
- If unresolved, which agreement version applies to a purchase (by effective or recorded date), whether a change is prospective or restates the period, how far a restatement reaches, and in which period its difference posts?
- If unresolved, which reference links a return to its purchase line, which period it reduces, where its adjustment posts, and what happens to a return larger than its purchase, one for a settled period or one that names no known purchase?
- If unresolved, which reference links a credit to an agreement and period, in which month it settles, what identifies a duplicate and which row counts, and what happens to a credit with a conflicting amount or an unknown agreement?
- If unresolved, how is a credit larger than the accrual treated (a negative balance, a carry forward, or a cap with the excess listed), and how is the uncovered amount published and described?
- If unresolved, is the outcome in one currency (and how another currency is treated) or converted at an approved rate and date, and at what point and by what mode is an amount rounded?

### Guardrails

- Do not choose the tier method, boundary rule, version treatment, return or credit handling, over-settlement treatment, linking rule or as-of date for the user, and take none from the data, a vendor default or common practice; the user may ask for alternatives or a recommendation.
- Never hard-code a rate, band, boundary rule, qualifying product, agreement version or as-of date in the models; a change to them must change the result without a code change, within the approved rule form.
- Never accrue a purchase under no agreement, a non-qualifying product or one outside a contract period unless an approved rule says so, or one purchase under more than one agreement; list what is not accrued with its amount and reason.
- Never let one credit reduce the accrual twice, count as earned rebate or apply to a different agreement than the one it names unless approved.
- Never rewrite a settled period's rows silently; a change to an earlier figure posts as a labelled adjustment unless an approved rule restates it, and an over-settlement or negative balance is shown, never hidden or netted across agreements unless approved.
- Never project where a contract period will end or accrue a tier the purchases to the as-of date have not reached.
- Never convert a currency without an approved rate, or equate a missing amount with zero.
- Do not post, collect, claim or pay a rebate or write back to any purchasing, ledger or payment system; the output is evidence for a reviewer.
- Stop at the contract-based amount: do not build the spend cube, verify invoices against orders and receipts, compute customer usage charges or detect duplicate invoices.
