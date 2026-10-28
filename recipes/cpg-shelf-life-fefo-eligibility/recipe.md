---
id: cpg-shelf-life-fefo-eligibility
title: Shelf-life exposure and first-expiry allocation eligibility by lot, location and open order line
trigger:
  - Planners cannot see which lots are close to expiry, how much of each is still usable, or how much will go unallocated, so stock is written off that a customer could have taken.
  - A customer rejects a delivery because the lot had too little shelf life left on arrival, and nobody can show which lots would have met that customer's minimum.
  - Customer service cannot say why an open order line is not covered when stock exists, because of held lots, short life at receipt or earlier lines taking the lot.
description: At an approved cutoff, publish each lot's shelf-life exposure and usable quantity, a first-expiry allocation of lots to open order lines under each customer's approved minimum life at receipt, a reason for every unmet quantity, and lot and line reconciliations.
pitch: See which lots are ageing out, who each lot can serve and why a line stays short, with every lot and line placed once.
job_category: build
area: transformation
readiness: supported
function:
  - supply-chain-ops
industry:
  - cpg
domain_objects:
  - sku
  - lot
  - location
  - customer
  - order_line
  - shelf_life_rule
  - lane_lead_time
  - allocation
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
  - Needs lot-location stock with expiry and status, open order lines, customer life rules and lane lead times as tables.
  - Life rules, lead times and band edges may be captured as editable data during the run.
  - A batch analytical proposal at one stated cutoff; dispatch, quality release and optimal allocation are separate.
  - Availability across channels is retail-reservation-availability-ledger; stockout risk is retail-sell-through-stockout.
  - Lot genealogy and recall tracing is inventory-lot-traceability; count reconciliation is ops-inventory-reconciliation.
  - Inputs are landed tables; loading files or extracts belongs to file-drop-to-bronze.
  - Reproducing a past cutoff needs kept history of lot stock and open order lines.
related:
  - retail-reservation-availability-ledger
  - retail-sell-through-stockout
  - inventory-lot-traceability
  - ops-inventory-reconciliation
  - inventory-valuation-cogs
  - effective-dated-business-rules
  - file-drop-to-bronze
evidence:
  features:
    - capturing-requirements
    - generating-dbt-model
    - running-dbt-in-sandbox
    - verifying
  evals: []
---

## Prompt

Build <exposure_model>, <allocation_model>, <unmet_line_model>, <lot_reason_model> and the lot and line reconciliations from <lot_stock_source>, <order_line_source>, <shelf_life_rule_source>, <lane_lead_time_source> and <life_band_edges>, as of <cutoff_date>. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only the semantics they leave open. For each lot and location publish the quantity on hand, its status, the usable quantity, the expiry, the remaining days, the share of total life left and the approved life band. For each open order line, find the receipt date, apply the customer's approved minimum remaining life, and allocate eligible lots in the approved order and quantity rules. Publish each line's unmet quantity with one primary reason, each lot that could not serve a line with its reason, and reconcile every lot and every line. Place every input row in a figure or list it with its reason, and keep sources read-only.

## Verified by

- Exposure has one row per approved lot and location at the cutoff, unique on that grain, with on-hand, status, usable quantity, expiry, remaining days, life share and band as the approved rules give; a lot with no expiry shows no usable quantity unless an approved rule derives one.
- Every allocated unit comes from a lot that meets the line's approved minimum remaining life at that line's receipt date; a lot that fails is skipped even when it expires first, and one exactly on the approved boundary follows the approved rule.
- Only lots in an approved allocatable status are allocated; a lot outside it, such as a held, quarantined or unknown-status one, or an expired lot, carries its reason and stays in exposure, and no lot gives more than its usable quantity or a line more than its open quantity.
- A line's rule and receipt date follow the approved precedence and dating; a line with no usable rule or lead time is blocked at line level with a named reason and never read as zero days, no minimum or immediate receipt unless an approved rule says so.
- Competing lines claim lots in the approved order, a lot used by an earlier line shows as consumed for later ones, and the published result does not change when the input rows arrive in a different order, given the approved tie-break.
- Each open line not fully allocated is shown, or counted with its reason as approved, with its unmet quantity and one primary reason by the approved precedence; allocated plus unmet equals open quantity, and each lot that could not serve a covered line shows one reason.
- Lot reconciliation: quantity on hand equals allocated plus unallocated usable plus excluded by named reason, for every lot, and the quantity left unallocated and near expiry stays visible rather than being folded into one catch-all cause.
- Every input lot row and order line is placed once or set aside with one reason (duplicate, conflicting, non-positive or non-whole quantity, closed or over-closed line), counted per input, and a set-aside row changes no exposure, allocation or reconciliation figure.
- Every published row states the cutoff it was computed at, and moving the cutoff or an approved rule changes the figures consistently; rules, lead times and band edges are read as data and never held as literals.
- Published figures equal values derived independently from the sources and approved rules, including a lot on the boundary day, an early-expiry lot that fails a customer's minimum, a line split across lots, two lines competing for one lot and an expired lot.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile each input for keys, expiry and manufacture dates, quantity signs and whole units, status values, duplicate lot rows and how a rule and a lead time resolve for a line, before modelling. Derive the expected exposure, allocation, unmet reasons and reconciliations independently of the models, by hand from the approved rules and the input data, and include cases at each edge: a boundary-day lot, a lot that fails one customer and serves another, a line that needs several lots, competing lines, a held lot, a missing expiry, a missing rule or lead time, a conflicting duplicate and a line with no stock at its location. Keep every rule the requirements treat as data as data that the models and tests read. Make the allocation independent of input row order. Before declaring the outcome complete, check each reconciliation, that every input row is placed once, that no set-aside row builds a figure, and that a changed cutoff or rule moves only what it should; report what the inputs cannot prove.

### Compose

- capturing-requirements
- applying-medallion-data-modelling
- generating-dbt-model
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which products, locations, lots and order lines are in scope, which products are shelf-life managed, what is the cutoff, what makes a line open (and how is an over-shipped or non-positive one treated), and how is an out-of-scope row listed or counted?
- If unresolved, in what form does a customer state the minimum life (days or share of total life, one or either), which rule wins among customer, customer and product, and dated rules, and what does a missing, invalid or ambiguous rule do?
- If unresolved, what makes the receipt date (ship date plus lane lead time, or a given delivery date), what happens to a line whose requested date is before the cutoff, and how is a missing or invalid lead time treated?
- If unresolved, how is remaining life counted (is the expiry day included, what is the boundary day), how is a missing expiry or manufacture date treated, and what are the life band edges?
- If unresolved, which lot statuses may be allocated, how are duplicate or conflicting lot rows, negative or non-whole quantities and a unit mismatch treated, and may stock at another location serve a line?
- If unresolved, in which order do competing lines claim lots, how are ties broken, in which order are a line's eligible lots taken, are partial and multi-lot allocations allowed in which units, and is a greedy sequence acceptable or is a better allocation wanted?
- If unresolved, what is the precedence of the primary unmet reason and of the reason a lot could not serve a line, and do blocked lines and lines with no stock appear in the unmet output and the lot reasons?
- If unresolved, are lots, lines, rules and lead times taken as latest or as known at the cutoff, how is a late or corrected record treated, and does a rule change from a date?

### Guardrails

- Do not choose rule form, rule precedence, receipt date, boundary day, allocatable statuses, claim order, location scope, reason precedence or exception handling for the user, and take none from the data or common practice; the user may ask for alternatives or a recommendation.
- Never read a missing, invalid or ambiguous rule or lead time as zero days, no minimum or immediate receipt, and never derive an expiry the sources do not carry, unless an approved rule says so.
- Never allocate a lot beyond its usable quantity or a line beyond its open quantity, and never allocate a lot that fails the line's approved minimum life or is not in an approved status.
- Never let the result depend on input row order, floor a negative quantity or double count a lot or a line; a set-aside row builds no figure.
- Do not hold a rule the approved requirements treat as data as a literal in the models; keep it as data that the models and tests read.
- Stop at the analytical proposal: do not release pick or dispatch, approve quality release, reserve or write back stock, forecast, or claim the allocation is optimal, and keep sources read-only.
