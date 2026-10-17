---
id: ops-procurement-spend
title: Build the procurement spend cube and flag invoice lines on or off contract
trigger:
  - Procurement, Finance and the business units each quote a different spend total, and nobody can say how much was bought outside a contract.
  - Procurement is asked which suppliers and categories are bought off contract and why, and cannot show the invoice lines behind the number.
  - A contract expires or is renegotiated and the team cannot see how much spend still flows to it after the end date, above its price or beyond its cap.
description: For the approved periods, roll invoice lines up to a spend cube, match each line to the contract that governs it and flag it on or off contract with the approved reason, keeping every line, credit and unmatched record visible so no spend is lost, counted twice or silently cleared.
pitch: Build one defensible monthly spend cube and see which lines were bought off contract, and why, line by line.
job_category: build
area: transformation
readiness: supported
function:
  - supply-chain-ops
  - finance
domain_objects:
  - invoice_line
  - purchase_order_line
  - supplier_contract
  - contract_line
  - spend_cube
  - off_contract_reason
  - spend_exception
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
  - Invoice lines, purchase-order lines and contracts arrive as landed tables; landing them is a separate outcome.
  - Supplier identity and item categories arrive conformed; matching suppliers and mapping items are separate outcomes.
  - Stops at the cube and contract flags; aging, duplicates, three-way match, rebates and savings are separate outcomes.
  - Without an approved contract-exempt list, spend with no contract on file is unproven, not non-compliant.
  - Currency conversion needs an approved rate source; without one, other-currency lines are shown apart from the totals.
related:
  - finance-ap-aging
  - finance-duplicate-invoice-detection
  - identity-golden-record-crosswalk
  - effective-dated-business-rules
  - metric-population-and-rollups
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

Build <flagged_invoice_line_model>, <spend_cube_model> and <spend_exception_models> from <invoice_line_source>, <contract_source>, <contract_line_source> and, where recorded or approved, <purchase_order_line_source>, <category_mapping_source> and <business_unit_source>. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only those they leave open. Count in the approved spend measure and period, match each in-scope invoice line to the contract the approved rules say governs it, and flag it on contract, or off contract with the approved reason or reasons for each approved breach, such as no contract, outside its dates, outside its scope, above its price or over a cap. Roll the lines up to the approved cube grain, such as period, supplier, category and business unit, from the lines alone, net credits as approved, and list every record the approved rules leave out, cannot place or cannot match, with its reason, or name it in the failure where the approved policy fails the run. Keep sources read-only. Report what the inputs cannot prove.

## Verified by

- On a run that completes, every input invoice line, credit note included, lands once in the cube's totals or once in a left-out list with its reason, and the counts, and the amounts per currency, sum to the input; a failed run names each bad record.
- Spend follows the approved measure, sign convention and period basis, including lines on each period edge; each cube figure equals an independent recomputation from the lines, never an average, a document total or a purchase-order total.
- A line's contract and reason equal an independent recomputation from the inputs, with every candidate contract visible; overlaps and ties follow the approved rule, never a silent pick, and dates apply at the approved edges, including the end date.
- Each line, or part of a line the approved cap rule splits, is on contract, off contract or in an approved unflagged class with its reason; an off-contract line carries the approved reason and any other breach as the approved rule says, so no breach is hidden unless approved.
- Where a price check is approved it follows the approved basis, tolerance and edge, including a price exactly on the edge; a price that cannot be compared without an approved conversion of currency, unit or price form shows as unchecked and is never reported compliant.
- Where a cap is approved it follows the approved measure, order and period: a line exactly at the cap, the line that crosses it and later lines are treated as approved, and credits reduce the running total only as approved.
- Credit notes net as approved: one naming an original line takes the approved treatment, and one naming none, or naming a line not in the input, is shown with that status and never silently dropped.
- Lines with no purchase order, category, contract or business unit follow the approved handling, appear as explicit members or as left-out records with their reason, and are never silently dropped or counted twice; a missing purchase order is an off-contract reason only where approved.
- Other-currency lines are never summed with the reporting currency unless an approved conversion states its rate source and date; any left-out amount is shown beside the totals with its own currency and amount.
- At every published cut, off-contract spend by primary reason sums to the cube's off-contract spend, with other breaches shown beside it and not added, and on-contract, off-contract and any approved unflagged spend sum to the net spend of each row.
- Each approved rule value, such as a tolerance, a cap, a contract date or a precedence, changes the output where the data reaches it, within the approved rule form.
- The outcome states what the inputs cannot prove, such as suppliers with no contract on file, amended contracts, spend recorded elsewhere, or whether a later change restates past periods.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile the invoice lines (dates, amounts, currencies, quantities, credits and their references, missing purchase orders and categories), the contracts and their lines (windows, scope, prices, caps, overlaps) before proposing rules. Use Ask first only for semantics still open, and record each decision as the user's own answer. Keep each approved tolerance, cap, date window, currency flag and reason precedence as data a reader can change, state the matching and reason rules once and check them against an independent expectation computed from the inputs, never from the models. Derive the cube and every breakdown from the same flagged lines so they cannot disagree. Report every exception left open and what the inputs cannot prove.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, what counts as spend (invoiced, paid or committed), which date sets the period, which calendar applies, and which dimensions the cube carries?
- If unresolved, which suppliers, entities, spend types and invoice statuses (voided, held, disputed) are in scope, do tax and freight count and follow their parent line's match, and how are left-out lines shown?
- If unresolved, which currency reports, are other currencies converted (rate source and date), excluded and shown apart, or reported separately, and may prices and quantities convert across units and price forms (fixed, discount, tiered, indexed)?
- If unresolved, what does a contract cover (item, category, supplier, entity, business unit), does a contract or PO reference override inferred matching, which versions count (draft, terminated, amended, renewed, open-ended), and are dates inclusive?
- If unresolved, how are overlapping or tied contracts resolved, which breaches make a line off contract (no contract, outside dates, outside scope, price above, over a cap), what price tolerance applies, and is a missing PO a reason or a flag?
- If unresolved, how is a cap measured (quantity or value; per contract, item or period), in what order are lines counted, is the crossing line wholly off contract or split, do credits reduce it, and how many reasons does a line carry, in what precedence?
- If unresolved, which in-scope spend needs no contract (categories, spend types, suppliers or a value threshold), how is it shown in the cube, and is a line whose price stays unchecked on contract, off contract or in its own unflagged class?
- If unresolved, how are credit notes treated (own or original's period, inherit the original's flag or judged alone), what happens to an unplaceable record (exclude and list, flag and keep, or fail), how is a split line attributed, and may later contract changes restate past periods?

### Guardrails

- Do not choose the spend measure, period basis, population, contract match or overlap rule, price tolerance, cap basis, reason precedence or credit treatment for the user, nor take them from the data or common practice; the user may ask for options or a recommendation.
- Never sum, net or compare amounts across currencies, or prices across units, unless the approved rules convert them and state the rate source and date.
- Never silently drop, zero-fill or double-count a line because it has no contract, purchase order, category, business unit or original invoice; follow the approved handling and keep its reason.
- Never pick silently among overlapping or tied contracts, and never let a single reason hide another breach unless the approved rule says so.
- Never build a cube figure from a total, an average or a document header; build every cut from the lines alone.
- Do not read a missing contract or purchase order as proof of non-compliance, nor call a line on contract on a contract the inputs do not show; report what the inputs cannot prove.
- Never restate a reported period silently when a contract or line changes later.
- Stop at the cube and the contract flags: do not resolve supplier identity, age payables, detect duplicate invoices, match receipts, accrue rebates, measure savings, set conversion rates or edit the source records.
