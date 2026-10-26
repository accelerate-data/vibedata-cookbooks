---
id: retail-marketplace-settlement
title: Reconcile marketplace orders to net payouts and held reserves by order line and settlement cutoff
trigger:
  - Finance cannot say what each marketplace order settled for or what is still owed, because fees, refunds, chargebacks and reserves are netted into payouts.
  - A fee or refund is deducted on the order and again in the payout, or a held reserve is treated as paid or as lost, and nobody can show which.
  - A payout does not equal the lines and reserve movements it carries, and no one can say which line, currency or timing difference explains the gap.
description: At each approved settlement cutoff, publish each order line's sale, refunds, fees, chargebacks and reserve movements, each order's paid, held and pending amounts, and each payout batch's tie to what it carries, with every difference visible and every unplaceable record listed with its reason.
pitch: What each marketplace order settled for and what is still owed, with every payout tied to its lines and no fee or refund counted twice.
job_category: build
area: transformation
readiness: supported
function:
  - finance
industry:
  - retail
domain_objects:
  - order
  - order_line
  - refund
  - fee
  - chargeback
  - reserve_movement
  - payout_batch
  - statement_line
  - set_aside_record
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
  - Needs order lines, fees, refunds, chargebacks, reserve movements and payout batches with statement lines, landed.
  - A rate table, if conversion is approved, may be captured as editable data; no rate is inferred.
  - Stops at components, balances and the payout tie; margin, bank matching, tax and posting are separate.
  - Margin is order-return-contribution-margin; general bookings, billings and cash is revops-bookings-billings-cash.
  - Reproducing a past cutoff after later or corrected records needs kept source history; a rebuild restates it.
  - Inputs are landed tables; loading statement exports belongs to file-drop-to-bronze.
related:
  - order-return-contribution-margin
  - revops-bookings-billings-cash
  - finance-ar-aging-dso
  - shared-fx-conversion
  - finance-gl-subledger-tieout
  - file-drop-to-bronze
evidence:
  features:
    - capturing-requirements
    - generating-dbt-model
    - dbt-unit-testing
    - running-dbt-in-sandbox
    - verifying
  evals: []
---

## Prompt

Build <line_ledger>, <order_position>, <payout_tie>, <component_model> and <set_aside_model> from <order_line_source>, <fee_source>, <refund_source>, <chargeback_source>, <reserve_source>, <payout_batch_source> and <statement_line_source>. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only the semantics they leave open. At each approved settlement cutoff, publish for each approved marketplace order line the sale, refunds, each fee type, chargebacks, reversals and reserve movements, for each order the paid, held, adjusted and pending amounts, and for each payout batch its declared net against the components it carries and their difference. Count each event once, keep a held reserve owed until the approved rule releases or adjusts it, keep transaction date, settlement period and currency apart, and list every record that cannot be placed with its reason. Keep sources read-only and report what the inputs cannot prove.

## Verified by

- On a run that completes, there is one line row per approved order line and cutoff and one order row per approved order, currency and cutoff, quiet cutoffs included and each output unique on its grain; the same order number on two marketplaces is two orders.
- A record counts at the cutoff the approved placing date gives; transaction date, settlement period and cutoff stay separate columns; one on the boundary follows the approved rule; a rerun on unchanged inputs gives the same rows, and a later record restates a published cutoff only as approved.
- Each economic event is counted once: a fee or refund carried on an order and in a payout is deducted once, a repeated statement line follows the approved duplicate rule, and a chargeback settled from a reserve is deducted once, in one place, never also as a payout deduction.
- A held reserve stays owed until the approved rule releases or adjusts it; a release adds no sale, an adjustment is shown as adjusted and never as collected, and a release or adjustment beyond what is held follows the approved treatment with the excess visible.
- Per line and per order and currency, net earned equals paid plus held plus adjusted plus pending, plus any excess the approved rule shows; pending keeps its sign, so a deduction in no paid batch behind a paid sale stays visible, and is checked against an independently derived value.
- A chargeback deducts once, a reversal credits once and is not a sale, a chargeback after a refund is flagged as the approved rule gives with every deduction kept, and a refund or chargeback with no sale behind it follows the approved treatment.
- Each payout batch publishes its declared net, the components it carries, their sum and the difference, never plugged, corrected or allocated away and exact to the approved rounding; every counted component traces to one batch, and a failed or returned batch pays nothing.
- A batch that does not tie, is failed or carries a line with no rate stays published with its status, difference and named lines; the orders it carries follow the approved rule and are flagged, never silently corrected.
- Amounts stay in their own currency and no total spans currencies; a payout-currency amount exists only where an approved rate gives it, and a line with no rate is listed with its reason and kept out of the tie as approved, never converted at a guessed rate.
- On a run that completes, every record of every input is counted in a measure, a labelled class or listed with its reason as approved; per-input counts sum to the records read, a set-aside record changes no balance, and the outcome states how many were excluded and why.
- A cutoff or payout that cannot be trusted follows the approved behaviour (fail naming the items, publish flagged, or keep the prior cutoff) and is never published as complete.
- Published figures equal values derived independently from the sources and approved rules, including a reserve held then released, a refund after the payout, a later deduction in no paid batch, a batch that does not tie and a foreign-currency order; the outcome states what the inputs cannot prove.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile each input for keys, signs, currencies, the three dates a record can carry, how a statement line links to its batch and source record, and the grain each reserve movement arrives at, before modelling. Derive the expected results independently of the models, from the approved rules and the inputs, before any model exists, and include cases at each edge: a reserve held and released later, a release larger than the hold, a refund after the payout with its commission credited back, a chargeback lost, reversed, after a refund and settled from a reserve, a failed batch, a batch that does not tie, a line in another currency or with no rate, a repeated and a conflicting statement line, an order-level fee, and the same order number on two marketplaces. Keep approved rules as data the models and tests read, never as literals. Before declaring the outcome complete, check that each identity holds at every cutoff, every input's records are placed once and no set-aside record changes a balance; report what the inputs cannot prove.

### Compose

- capturing-requirements
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which marketplaces, seller accounts, order lines and statuses are in scope (cancelled, test, zero value), which cutoffs run and from when, and how is a record outside scope handled (listed or counted)?
- If unresolved, which date places a statement line at a cutoff (its own or its batch's), what is the cutoff and its time zone, and does a later or corrected record restate a published cutoff or enter the next one?
- If unresolved, what links a fee, refund, chargeback and reserve movement to its order line, and a statement line to its batch and source record, and how are an order-level amount, an account-level amount, an unknown line and a repeated or conflicting event treated?
- If unresolved, which fee types stay apart, how is a commission credit on a refund shown, and how are a chargeback after a refund, a reversal, a refund or chargeback with no sale, and a pass-through such as tax or a shipping credit treated?
- If unresolved, at what grain are reserves held, what do a release, an adjustment and a chargeback settled from the reserve do to the held balance, and how is a release or adjustment beyond what is held treated?
- If unresolved, when does an event count as paid, what do a failed or returned batch and a batch that does not tie do to the orders they carry, and how is a deduction in no paid batch behind a paid sale shown?
- If unresolved, which rate converts a line to the payout currency (source, effective date, direction), where does rounding occur and may it show as a difference, and how is a line with no rate treated in the tie?
- If unresolved, how are a payout that does not tie beyond tolerance, a negative net payout, a reissued batch and an input missing for a cutoff treated (list, flag, fail or keep the prior cutoff)?

### Guardrails

- Do not choose placing date, cutoff, links, reserve treatment, paid rule, rounding, rate source, tie behaviour or exception handling for the user, and take none from the data or common practice; the user may ask for alternatives or a recommendation.
- Never deduct a fee, refund or chargeback twice, on the order and again in a payout or in two components; each event counts once under the approved duplicate rule.
- Never treat a held reserve as paid or lost or a release as a sale; it stays owed until the approved rule releases or adjusts it, and an adjustment is never reported as collected.
- Never plug, correct or allocate away a payout difference, or absorb it into a line, a tolerance or an adjustment; it stays published with its batch and status.
- Never add or convert across currencies except under an approved rate, and never invent, infer or look up a rate or default a missing rate to one.
- Never allocate an order-level or account-level amount to lines, or merge the same order number across marketplaces or seller accounts.
- Never drop, double count or silently net a record; a set-aside record changes no balance, and a flagged case such as a chargeback after a refund keeps every deduction.
- Never default a missing amount, date or key to zero unless the approved semantics define it so.
- Stop at the settlement ledger: do not compute margin, match bank statements, recognise revenue, post to a ledger, work out tax, set rates or forecast reserve releases, and keep sources read-only.
