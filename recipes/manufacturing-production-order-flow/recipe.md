---
id: manufacturing-production-order-flow
title: Reconcile production-order movements into work in progress by operation, first-pass and final yield, and exceptions
trigger:
  - Yield and work in progress come from a spreadsheet that counts a reworked unit as a second unit produced and cannot keep first-pass yield apart from final yield.
  - Opening work in progress plus what was started never equals closing work in progress, and nobody can say which operation lost the quantity.
  - Split, merge, scrap and finished-goods receipt records lose or double count quantity between operations of a production order.
description: From production orders, material issues and returns, operation completions, scrap, rework, split and merge records and finished-goods receipts, publish a movement ledger, work in progress per order and operation at approved cutoffs that reconciles under the approved identity and tolerance, first-pass and final yield, and every quantity that cannot be placed.
pitch: Reconcile every production-order movement into work in progress and yield, so a reworked unit counts once and no lost quantity hides.
job_category: build
area: transformation
readiness: supported
function:
  - supply-chain-ops
industry:
  - manufacturing
domain_objects:
  - production_order
  - operation
  - material_issue
  - operation_completion
  - scrap_event
  - rework_event
  - goods_receipt
  - unit_conversion
  - wip_position
  - counted_wip
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
  - Needs recorded movements per order and operation; movements are never inferred from plans, schedules or standards.
  - Finding unexplained loss needs an observation such as counted work in progress; without one it is reported unproven.
  - Quantities only; costing, variances and equipment time are separate outcomes.
  - Inputs are landed tables; loading files or extracts belongs to file-drop-to-bronze.
  - Holding a reported cutoff frozen, or showing what a restatement changed, needs kept source history or published rows.
  - Flagging a late movement needs a recorded time on each movement; without one, lateness is reported unproven.
related:
  - manufacturing-oee-downtime
  - inventory-lot-traceability
  - effective-dated-bom-requirements
  - inventory-valuation-cogs
  - ops-inventory-reconciliation
  - file-drop-to-bronze
evidence:
  features:
    - capturing-requirements
    - applying-medallion-data-modelling
    - generating-dbt-model
    - running-dbt-in-sandbox
    - verifying
  evals: []
---

## Prompt

Build <movement_ledger_model>, <wip_position_model>, <order_yield_model>, <flow_exception_model> and <flow_coverage_model> from <production_order_source>, <routing_source>, <material_movement_source>, <operation_event_source>, <goods_receipt_source>, <unit_conversion_source> and, where one exists, <counted_wip_source>. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only the semantics they leave open. Keep one row per recorded movement and place every input record once, counted or set aside with its reason. For each order and operation at each approved cutoff, publish opening work in progress, every flow that enters or leaves it, declared loss and closing work in progress, reconciled under the approved identity and units. Count a unit that returns to an operation as further passes of one unit, never as a second unit produced, and publish first-pass and final yield under the approved definitions. Keep split and merge lineage, convert only through approved factors, and show unexplained, negative or excess quantities and closed orders still holding work as exceptions. Keep sources read-only; report what inputs cannot prove.

## Verified by

- On a run that completes, every input record is placed once, counted under its movement type or set aside with one reason, and line counts and quantities per record type and native unit foot to the input; records the approved scope leaves out are shown or counted with their reason as approved.
- At each approved cutoff, each order and operation satisfies the approved identity: opening plus work entering, minus work leaving, scrap and declared loss, with any labelled late adjustment, equals closing exactly or within the approved tolerance, and each opening equals the previous closing.
- A unit sent back to an operation is introduced once and counted at most once as completed output of each operation and once as receipted; each return and later pass is its own visible movement, and between passes it sits in work in progress where the approved rule places it.
- First-pass and final yield follow the approved definitions and denominators at every published level, with numerator and denominator shown; a unit that fails a pass at that level and finally passes counts in final good and not first-pass good, and open work in progress is never counted as lost.
- Every output of a split and every input of a merge keeps its own movement and its lineage; quantity is conserved with the declared loss under the approved rules, and a difference beyond it is published as an exception.
- Declared loss follows the approved definition and stays apart from scrap; where a counted work in progress or another approved observation disagrees with the computed position, the signed difference is published as unexplained, never folded into scrap, loss or work in progress.
- Every converted quantity is traceable to an approved factor, or a chain approved rules allow, in force at its approved date; a quantity with no such path is never converted at one, it stays in its native unit under the approved disposition, and no roll-up needing it is published as reconciled.
- A position below zero, a receipt or reversal beyond the balance it meets, and a closed or cancelled order still holding work are each published, or named in a run failure, with their quantity under the approved disposition; none is clamped, netted away at a higher level or written off silently.
- Positions count movements by the approved time basis; a movement dated before a cutoff but recorded after it is restated into that cutoff or entered as a labelled adjustment in the next, as approved, never dropped; a frozen cutoff keeps its published values.
- Each output is unique on its approved grain, and orders, operations or units from different plants or sources are never merged because their identifiers match.
- Published movements, positions, yields and exceptions equal values derived independently from the sources and approved rules, on cases including a rework loop that finally passes, a later-pass scrap, a split, a merge, an unconvertible quantity, an excess receipt and two cutoffs.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile each input for order, operation and unit keys, movement types, units of measure, dates, routing coverage and repeated records before modelling. Write the expected ledger, positions, yields, exceptions and coverage by hand from the approved rules and the input data before any model, and include a case for each rule at its edge, such as a unit reworked across several operations, a pass scrapped late, a split with and without declared loss, a merge of units with different histories, a transfer between operations in different units, a receipt larger than what is waiting, a late-recorded movement and an operation that goes negative. Keep each rule the requirements treat as data (factors, reasons, cutoffs, routings, tolerances) as data that the models and tests read, never as a literal. Before declaring the outcome complete, recompute the identity on every published position independently of the models, check that a reworked unit is counted once, that every input is placed once and that no unexplained, negative or excess quantity was hidden; report what the inputs cannot prove.

### Compose

- capturing-requirements
- applying-medallion-data-modelling
- generating-dbt-model
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which plants, orders, order types and statuses, operations and record types are in scope, which keys link a movement to its order, operation and unit, and are out-of-scope records listed or only counted with their reason?
- If unresolved, in which unit is each operation counted (its output unit, the finished-goods unit, the recorded unit), which conversion factors and effective dates are approved, and is an order-level roll-up published when any operation lacks a factor?
- If unresolved, what is a unit (piece, lot or batch key), how is a returning unit identified and where does it sit between passes (the operation it returns to, a rework step or a linked rework order), how do split or merge outputs inherit history, and how is a mixed-fate lot judged?
- If unresolved, what counts as declared loss (only stated scrap and loss, or a routing allowance), what tolerance applies to the identity, and which observation, such as counted work in progress, reveals an unexplained difference?
- If unresolved, is first-pass judged per operation or across the whole route, what makes a unit final good, and is the yield denominator resolved units or units introduced, with work in progress inside or beside it?
- If unresolved, which cutoffs are published, which date places a movement (event or recorded), and is a cutoff already reported frozen, restated or adjusted when a movement arrives late, including a missing recorded time?
- If unresolved, where does work in progress start and end (release, material issue or first move; completion or receipt), and how are a receipt or reversal beyond its balance, a negative position and a closed or cancelled order holding work treated: set aside, split, flagged or failed?
- If unresolved, what identifies a duplicate record, how are conflicting copies, an operation or rework target outside the routing and an unknown order or unit treated, and does the run fail or set them aside?

### Guardrails

- Do not choose the counting unit, unit identity, declared loss, yield definitions, cutoffs, scope or exception handling for the user, and take none from the data, the routing standard or common practice; the user may ask for alternatives or a recommendation.
- Never count a reworked or returning unit as a second unit introduced, completed or receipted, and never count a pass as production.
- Never infer a quantity, a link between units or a conversion factor from plans, standards, dates or equal quantities unless an approved rule, such as a routing allowance, says so; keep such loss labelled apart, and never sum across units the approved rules keep apart.
- Never close an identity by plugging, rounding beyond the approved tolerance or absorbing an unexplained difference into scrap, declared loss or work in progress.
- Never clamp a negative position, net it away at order level or write off work held by a closed order; keep it visible with its quantity.
- On a run that completes, never drop or double count a record: every record of every input stays accounted for, including duplicates, conflicts and set-aside records.
- Do not hold a rule the approved requirements treat as data, such as a factor, reason, cutoff or tolerance, as a literal in the models.
- Stop at quantities: do not value movements, post to a ledger or change the production system, and keep sources read-only.
