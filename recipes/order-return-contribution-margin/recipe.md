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
  - customer-historical-ltv
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

Build <order_contribution_model> for the order margin questions in this Intent. Inspect the approved requirements, order-line, refund, return and cost sources, then settle the unresolved scope, period, amount, quantity, cost, recovery, fee, linking and completeness rules. Produce order-line revenue, refund value, returned quantity, recoverable goods cost, original goods cost, fees, fulfilment, return handling and contribution margin, plus order and period rollups that reconcile to the lines. Count each refund and return once, recover stock cost only for physically returned stock the approved rule accepts, and leave margin unknown with a reason when a required cost is missing. Show refunds, returns and costs that cannot be placed or that the scope leaves out. Materialize in the Intent's sandbox and verify against independently derived expected values.

## Verified by

- The contract fixes the line grain, scoped population, period basis, amount basis, quantity basis, cost components and which are required, and every published output, each as approved.
- Each in-scope order line, refund, return and cost record ends on a line or with a set-aside reason. Records the approved scope leaves out are shown or counted with their reason, and the outcome states how many were excluded and why.
- Delivered refund amounts and returned units equal what the lines carry plus any redelivered, conflicting, unplaceable, order-level, other-currency or approved-excluded component, each shown with its reason.
- A refund or return delivered again counts once under the approved identity rule. A conflicting delivery follows the approved handling and stays visible. One line with several refunds and returns carries each once, never their cross product.
- In a labelled single-currency case where these are the line's approved components, revenue 100, refund 30, original goods cost 40, recovered goods cost 8, fees 5 and return cost 4 yield margin 29. Margin equals the approved components plus any approved fee reversal.
- A refund without a physical return recovers no goods cost. A partial return recovers only the returned quantity the approved condition and valuation rule accept, and refund value stays separate from returned quantity.
- A missing required cost leaves margin unknown with a named reason, distinct from a source-confirmed zero and an approved not-applicable cost, unless an approved rule supplies a labelled estimate. Known subtotals are labelled, and no unknown becomes zero.
- An over-refund, a return above the approved quantity basis and a refund or return naming no known line follow the approved handling, with their flag or reason visible. None is silently capped, dropped or attached to another line.
- Each refund and return lands in the approved period by the approved event date and status, and the outcome states whether it restates the order period or adjusts the return period. Boundary events land per the approved time zone and cutoff.
- Rollups reconcile to the lines, or to their approved period adjustments, on every component with no fan-out. A margin is never shown as complete while any contributing line is unknown, the unknown-line count shows beside it, and margins recompute from components.
- Expected lines, orders and periods are derived independently of the model from the sources and approved rules before comparison, covering each duplicate, refund-only, partial, missing-cost, over-refund and boundary case the approved rules make possible.
- Outputs are read back after materialization and a rerun on unchanged inputs gives identical results. The report states counts, margins, exceptions and unresolved inputs.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain and sources. Inspect approved requirements and the order, refund, return and cost sources first, and profile keys, timing, cardinalities, duplicates, statuses, missing costs and currencies. Use Ask first only for unresolved semantics; samples or existing SQL cannot approve economic policy. Fix the line grain, period basis, amount basis, quantity basis, cost basis, recovery rule, fee treatment, record identity and linking keys. Resolve each refund and return to one governing record before joining, so a line with many refunds and returns cannot multiply either side. Keep refund value, returned quantity and recovered cost as separate components, and keep unknown, confirmed-zero and not-applicable costs apart. Fix expected lines, rollups and exceptions independently before model SQL, including adverse cases. Build line economics, then order and period rollups from them, materialize, read back, rerun and reconcile every record to a line or an exception. Report absent inputs and untested cases as incomplete verification.

### Compose

- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, what is one economic order line, which margin questions, breakdowns and ratio denominators are required, which orders, line types and statuses are in scope, and are excluded records listed or only counted?
- If not approved, does a refund restate the order period or adjust the return period (as its own row or not), which event date and status make it count, and which time zone, cutoffs and late-record treatment apply?
- If unspecified, what counts as revenue and refund value (discounts, tax, shipping, gift cards, tenders), and which currency, unit and rounding apply, with what done to lines outside them?
- If the basis is unresolved, which quantity governs over-return (ordered, shipped, net of cancellation) and what is original goods cost (method, timing, warehouse, bundle parts), and which cost applies when it changes?
- If recovery is unresolved, which return conditions recover stock, how is it valued, how are restocking fees, write-downs, returns in transit and kept-item refunds treated, and what limits recovery?
- If fees are undefined, are processor fee, fulfilment and return handling recorded, derived or allocated from the order, does a refund reverse any, and which are required?
- If linking is unresolved, what makes a refund or return the same across deliveries, which delivery governs, which keys tie it to a line, and how are order-level, conflicting, orphan and over-refunded ones, chargebacks, exchanges and store credit treated?
- If completeness is unspecified, what proves a cost complete, missing, confirmed zero, not applicable or estimated, and how do rollups show margin and counts when lines are unknown?

### Guardrails

- Do not zero-fill a missing required cost or claim a margin from incomplete costs unless an approved rule supplies a labelled estimate. Label known subtotals and keep unknown, confirmed-zero and not-applicable costs distinct.
- Do not recover goods cost for a refund without an accepted physical return, or count a redelivered refund or return twice. Do not let a line with several refunds and returns multiply either side.
- Do not silently cap, drop or reassign an over-refund, an over-return, an order-level amount or an unplaceable record. Handle each as approved and keep it visible with its reason.
- Do not choose the period basis, valuation, cost basis, fee treatment, record identity or linking keys from the sample. Do not mix periods or sum incompatible currencies or units.
- Keep this outcome to order-line margin and its order and period rollups. Currency conversion, tax or ledger posting, customer or product margin cuts, bookings-to-cash reconciliation and stockout analysis belong to other outcomes; do not require another Recipe to implement or verify this one.
- Use the actual Intent platform and sandbox. Do not substitute another engine, synthesize an absent sandbox or mutate Domain sources to manufacture evidence. Build success alone does not prove the economics.
