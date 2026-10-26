---
id: retail-reservation-availability-ledger
title: Reconstruct available-to-promise stock by SKU, location and cutoff from reservation and fulfilment events
trigger:
  - Customer service promises stock that is already reserved, or sells the same units twice because reservations that expired or shipped still count against availability.
  - Planners cannot say why the stock available to promise differs from the physical count, because units are reserved, quarantined, in transit or short-received, and nobody can show which.
  - A split order, a partial shipment or a cancelled and re-sent reservation leaves the reserved quantity wrong, and the error only shows up when a customer is let down.
description: At each approved nightly cutoff, publish for every SKU and location the physical, quarantined, in-transit and validly reserved quantities and the available-to-promise quantity under the approved policy, keep physical and reserved balances reconciling on their own, and place every record or list it with its reason.
pitch: A nightly ledger of what you can still promise, with every reservation released once, every shipment counted once and nothing dropped.
job_category: build
area: transformation
readiness: supported
function:
  - supply-chain-ops
industry:
  - retail
domain_objects:
  - sku
  - location
  - stock_movement
  - reservation
  - order_line
  - shipment
  - stock_transfer
  - available_to_promise
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
  - Needs stock movements, reservations with an expiry, cancellations, shipments and order lines as landed tables.
  - Picks, transfers and quarantine movements are used where the inputs carry them; their absence is reported.
  - A batch analytical ledger; real-time promising, allocation priority, replenishment and safety-stock sizing are separate.
  - Reconciling systems against counts is ops-inventory-reconciliation; stockout exposure is retail-sell-through-stockout.
  - Reproducing a past cutoff after late or corrected records needs kept history of the sources.
  - Inputs are landed tables; loading files or extracts belongs to file-drop-to-bronze.
related:
  - ops-inventory-reconciliation
  - retail-sell-through-stockout
  - master-product-sku-hierarchy
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

Build <ledger_table>, <order_line_model>, <coverage_model> and <set_aside_model> from <stock_movement_source>, <reservation_source>, <cancellation_source>, <shipment_source>, <order_line_source>, <sku_location_master> and any pick or transfer source the approved rules use. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only the semantics they leave open. At each approved cutoff and for each approved SKU and location, publish the physical, quarantined and in-transit quantities, the reserved quantity that is still valid and the available-to-promise quantity under the approved formula, release each reservation once by expiry or cancellation, consume it only as the approved fulfilment rule gives, keep an order line split across locations or shipments at its full quantity, reconcile the physical and reserved balances each on its own, and place every record of every input in a balance or a labelled class or list it with its reason. Keep sources read-only and report what the inputs cannot prove.

## Verified by

- On a run that completes, there is one row per approved SKU, location and cutoff from the approved first row to the last cutoff, quiet nights included, none for a pair the approved scope leaves out, and each output is unique on its declared grain.
- A record counts at the cutoff the approved governing timestamp gives; one exactly on the boundary follows the approved rule; a rerun on unchanged inputs reproduces the same rows, and a late or corrected record changes a published cutoff only where the approved rule restates it.
- Physical stock reconciles on its own: from the approved opening at the first cutoff, opening plus the approved movements equals closing at every cutoff, a negative closing follows the approved treatment and is never silently floored, and a unit is never in two physical balances at once.
- The reserved quantity reconciles on its own: from the approved opening, opening plus newly reserved and any amendment or reinstatement the approved rule shows, less released and consumed, equals closing, is never negative, and is not derived from physical stock or availability.
- No reservation releases more than its remaining quantity or releases the same quantity twice: a repeated cancellation and a cancellation after expiry or full fulfilment release nothing further, and one after partial fulfilment releases only the remainder, as the approved rule gives.
- Physical stock falls once per fulfilled unit at the approved point; its reservation is consumed up to its reserved quantity and as the approved rule gives after release, never lowering available stock twice; unreserved, excess or other-location quantity is labelled and follows the approved rule.
- An order line split across locations or shipments keeps its ordered quantity: reserved, fulfilled and released quantities foot to it, or the line carries one named reason that it does not.
- Stock in transit and quarantined stock are published as the approved rules place them and never promised unless approved; a transfer joins its destination as approved, and a short or over receipt follows the approved treatment with its variance visible and is never silently dropped.
- Available-to-promise equals the approved formula over the row's own components, and where reservations and held stock exceed physical stock the unfloored deficit stays observable, as a shortfall or as the approved negative figure.
- On a run that completes, every record of every input is counted in a balance, a labelled class, or listed or counted with its reason as approved; per-input counts sum to the records read, the outcome says how many were excluded and why, and a set-aside record changes no balance or ledger row.
- A cutoff that cannot be trusted, such as an input missing for the night, follows the approved behaviour (fail naming the items, publish flagged, or publish nothing) and is never published as complete.
- Published figures equal values derived independently from the sources and approved rules, including an expiry on the boundary, an expiry and a fulfilment within one cutoff in each order, a split line and a short receipt; the outcome states what the inputs cannot prove.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile each input for keys, quantity signs, units, timestamps and their time zone, and for how a shipment, a pick and a cancellation link to a reservation, before modelling. Derive the expected results independently of the models, from the approved rules and the input data, and include cases at each edge: a reservation expiring on the boundary and one just after it, an expiry and a fulfilment within one cutoff in each order, a repeated cancellation, a cancellation after partial fulfilment, a fulfilment after release, an unreserved shipment, a split order, a short receipt and a record whose keys do not resolve. Keep each approved rule the requirements treat as data as data that the models and tests read, never as a literal. Before declaring the outcome complete, check that each balance reconciles on its own, that every input's records are placed once, that no set-aside record builds a row, and that a changed rule moves only what it should; report what the inputs cannot prove.

### Compose

- capturing-requirements
- applying-medallion-data-modelling
- generating-dbt-model
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which SKUs, locations and sales channels are in scope, is a channel a stock location or an attribute of the order, which pairs get a row, from when and from what opening balance, in which unit are quantities held, and how is a record outside scope handled?
- If unresolved, what instant is each cutoff and in which time zone, does a record or an expiry exactly on it count, which timestamp governs, and is a late or corrected record applied at the next cutoff or does it restate a published one?
- If unresolved, how is available-to-promise defined: which quantities it subtracts (reservations, quarantine, other held stock), is quarantined stock part of physical, and may it be negative or is it floored with the deficit shown?
- If unresolved, which reservation states count as valid, how is the expiry edge read, what does a cancellation release, what do a repeated cancellation and a shipment after release do, and how does an amended reservation reach the balance?
- If unresolved, when does physical stock fall and a reservation get consumed (at pick or at shipment), what does a pick change, and how does a shipment link to its reservations (by reservation, or by order line, SKU and location)?
- If unresolved, how are a partial shipment, a shipment without a reservation, one above the reservation's remainder, one from another location than reserved, and links that sum above the shipped quantity treated?
- If unresolved, when does a transfer leave its source and join its destination, where is stock in transit shown and may it be promised, how is a short or over receipt treated, and how does stock enter and leave quarantine?
- If unresolved, how are an unknown SKU or location, a duplicate event, a non-positive quantity, an order line whose reservations differ from its ordered quantity, a negative physical balance and a cutoff that cannot be trusted treated (list, flag, fail or publish nothing)?

### Guardrails

- Do not choose cutoff, boundary, availability formula, reservation validity, fulfilment point, linking keys, transfer timing or exception handling for the user, and take none from the data or common practice; the user may ask for alternatives or a recommendation.
- Never release or consume the same reserved quantity twice or beyond its reserved quantity, and never let a shipment lower available stock through both the physical movement and the reservation.
- Never derive the reserved balance from physical stock or availability, or the reverse; each reconciles from its own inputs.
- Never hide a deficit: a floored or clipped available figure needs an approved rule and the unfloored amount stays observable.
- Never drop or double count a record; a set-aside record changes no balance and builds no ledger row.
- Do not hold a rule the approved requirements treat as data as a literal in the models; keep it as data that the models and tests read.
- Stop at the nightly ledger: do not promise stock in real time, allocate or rebalance stock, size safety stock, value inventory or write back to a source, and keep sources read-only.
