---
id: order-return-contribution-margin
title: Build order-line contribution margin with order and period rollups after refunds and returns
trigger:
  - Gross sales minus original item cost overstates order margin because refunds and returns arrive after the order.
  - Finance cannot explain a margin because refund value, returned stock, recovered inventory cost, fees and return handling are mixed or missing.
  - A refund is delivered twice, a return is partial, or a refund has no physical return, and the order margin moves the wrong way.
description: Build order-line economics that separate refund value, returned quantity, recoverable goods cost, fees, fulfilment and return handling into a margin, with order and period rollups that reconcile to the lines and show where margin is unknown.
pitch: Show what an order actually earned after refunds, returns and recovered stock, with every adjustment counted once and no missing cost hidden as zero.
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
  - return
  - recoverable_goods_cost
  - fee
  - contribution_margin
  - period_rollup
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
  - Needs order-line, refund and return records; costs may be captured as approved editable data.
related:
  - shift-unit-economics
  - revops-bookings-billings-cash
  - retail-sell-through-stockout
evidence:
  features:
    - profiling-source-data
    - applying-medallion-data-modelling
    - generating-dbt-model
    - dbt-unit-testing
    - running-dbt-in-sandbox
    - verifying
  evals: []
---

## Prompt

Build <order_contribution_model> for the order margin questions in this Intent. Inspect the approved requirements, order-line, refund, return and cost sources, then settle the unresolved period, revenue, recovery, fee, completeness and linking rules. Produce order-line revenue, refund value, returned quantity, recoverable goods cost, original goods cost, fees, fulfilment, return handling and contribution margin, plus order and period rollups that reconcile to the lines. Count each refund and return once, recover stock cost only for physically returned stock the approved rule accepts, and leave margin unknown with a reason when a required cost is missing. Show refunds, returns and costs that cannot be placed. Materialize in the Intent's sandbox and verify against independently derived expected values.

## Verified by

- The contract fixes the line grain, scoped population, period basis, revenue and refund basis, cost components and which are required, currency, rounding and every published output, each as approved.
- Each in-scope order line, refund, return and cost record has lineage and an applied, superseded, excluded or set-aside disposition with a reason. Delivered refund amounts and returned units equal what the lines carry plus redelivered, conflicting and unplaceable records.
- A refund or return delivered again counts once. A conflicting delivery follows the approved handling and stays visible. One line with several refunds and returns carries each amount once, never their cross product.
- In a labelled single-currency case where these are the line's approved components, revenue 100, refund 30, original goods cost 40, recovered goods cost 8, fees 5 and return cost 4 yield margin 29. Independent expectations catch swapped or doubled adjustments.
- A refund without a physical return recovers no goods cost. A partial return recovers only the returned quantity the approved condition and valuation rule accept, and refund value stays separate from returned quantity.
- A missing required cost leaves margin unknown with a named reason, distinct from a source-confirmed zero and an approved not-applicable cost. Known subtotals are labelled, and no unknown becomes zero.
- An over-refund, a return above the ordered quantity and a refund or return naming no known line follow the approved handling, with their flag or reason visible. None is silently capped, dropped or attached to another line.
- Each refund and return lands in the approved period, and the outcome states whether it restates the order period or adjusts the return period. Boundary events land per the approved time zone and cutoff.
- Order and period rollups reconcile to the lines on every component with no fan-out. A margin is never presented as complete while any contributing line is unknown, and the unknown-line count shows beside it.
- Margins recompute from their components, and ratios use approved denominators, not averages of line ratios. Currencies or units outside the approved set are set aside, not summed.
- Expected lines, orders and periods are derived independently of the model from the sources and approved rules before comparison, including duplicate delivery, refund-only, partial return, missing cost, over-refund and boundary cases.
- Outputs are read back after materialization and rerun with identical results. The report states counts, margins, exceptions and unresolved inputs.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain and sources. Inspect approved requirements and the order, refund, return and cost sources first, and profile keys, timing, cardinalities, duplicates, missing costs and currencies. Use Ask first only for unresolved semantics; samples or existing SQL cannot approve economic policy. Fix the line grain, period basis, revenue and refund basis, recovery rule, fee treatment, required costs and linking keys. Resolve each refund and return to one governing record before joining, so a line with many refunds and returns cannot multiply either side. Keep refund value, returned quantity and recovered cost as separate components, and keep unknown, confirmed-zero and not-applicable costs apart. Fix expected lines, rollups and exceptions independently before model SQL, including adverse cases. Build line economics, then order and period rollups from them, materialize, read back, rerun and reconcile every record to a line or an exception. Report absent inputs and untested cases as incomplete verification.

### Compose

- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, what is one economic order line, which margin questions, breakdowns and ratio denominators are required, and which orders, line types, statuses and periods are in scope or excluded?
- If not approved, which period basis applies: restate the order period or record the adjustment in the return period; and which time zone, cutoffs and treatment of late refunds and returns?
- If unspecified, what is revenue and refund value: discounts, tax, shipping, gift cards and other tenders, and how are tax and shipping amounts treated in refunds?
- If recovery is unresolved, which return conditions are recoverable, how is recovered stock valued, how are restocking, write-downs, returns in transit and refunds where the item is kept treated, and what limits recovery?
- If fees and charges are not defined, are processor fee, fulfilment and return handling recorded, derived or allocated from an order, does a refund reverse any of them, and which are required?
- If linking is unresolved, which keys tie a refund or return to a line, how are redelivered or conflicting records, over-refunds, returns above the ordered quantity and unplaceable records handled?
- If completeness is unspecified, what proves a cost complete, missing, confirmed zero or not applicable, and how should rollups present margin and counts when lines are unknown?
- If other currencies or units appear, which currency, unit and rounding precision are in scope, and what happens to lines outside them?

### Guardrails

- Do not zero-fill a missing required cost or claim a margin from incomplete costs. Label known subtotals and keep unknown, confirmed-zero and not-applicable costs distinct.
- Do not recover goods cost for a refund without an accepted physical return, or count a redelivered refund or return twice. Do not let a line with several refunds and returns multiply either side.
- Do not cap, drop or reassign an over-refund, an over-return or an unplaceable record to make totals close. Keep each visible with its reason.
- Do not choose the period basis, valuation, fee treatment or linking keys from the sample. Do not mix periods or sum incompatible currencies or units.
- Keep this outcome to order-line margin and its order and period rollups. Do not expand it into bookings-to-cash reconciliation, stockout analysis, tax or ledger posting, or require another Recipe to implement or verify it.
- Use the actual Intent platform and sandbox. Do not substitute another engine, synthesize an absent sandbox or mutate Domain sources to manufacture evidence. Build success alone does not prove the economics.
