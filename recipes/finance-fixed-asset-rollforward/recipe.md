---
id: finance-fixed-asset-rollforward
title: Build a fixed-asset register and reconcile its net-book-value roll-forward
trigger:
  - Every month someone rebuilds the fixed-asset register and depreciation schedule in a spreadsheet to prove that opening value plus additions less depreciation and disposals equals closing value.
  - A partial disposal, a transfer between entities or a cost adjustment leaves the register, the roll-forward and the ledger disagreeing, and nobody can say which asset moved what.
  - An auditor asks why a class's or an entity's closing net book value, or its difference from the ledger, changed between two periods.
description: Build asset-period movements for cost and accumulated depreciation under the approved policies, roll them up to parent, class, entity and total without counting a component twice, reconcile net book value forward, set closing balances beside the ledger, and keep every unprocessable event or unpoliced asset visible.
pitch: Turn asset events and approved depreciation policies into a register and a net-book-value roll-forward that foot every period and sit beside the ledger.
job_category: build
area: transformation
readiness: supported
function:
  - finance
domain_objects:
  - asset
  - asset_register
  - depreciation_schedule
  - legal_entity
  - general_ledger
  - asset_exception
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
  - Needs dated asset events, approved depreciation policies with their assignments, and ledger balances.
  - Takes capitalisation decisions as given; the depreciation policies may be captured as editable data.
  - Keeps each currency separate; where translation is approved it needs supplied dated rates, else it is unproven.
  - Placing late changes by recorded date needs one on the events; otherwise restatement is reported unproven.
  - One book per run; impairment, revaluation, merges, splits, lease accounting and tax books are separate and set aside.
  - Stops at the register, roll-forward and ledger comparison; break classes, close packs and postings are separate.
related:
  - finance-gl-subledger-tieout
  - finance-trial-balance-close
  - effective-dated-business-rules
  - dbt-snapshot-history
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

Build <register_model>, <rollforward_model>, <ledger_comparison_model>, <movement_model>, <exceptions_model> and <completeness_model> from <asset_events_source>, <depreciation_policy_source>, <policy_assignment_source> and <ledger_balances_source> for <reporting_window>, with <fx_rates_source> only where translation is approved. Inherit the approved requirements and resolve only what they leave open. For each asset or component and period at the approved grain, publish cost and accumulated depreciation as opening, additions, cost adjustments, transfers in and out, depreciation, disposals and closing, with net book value, as the approved policy says. A disposal removes the approved share, and a transfer moves the approved amounts between owners without an addition. Roll up to the parent, class, entity and total at the approved levels, set closing balances beside the ledger at the approved key with every difference shown and none classified, and keep every asset without a policy, outside the approved scope or unprocessable event visible, or fail the run naming it, as approved. Account for every event and amount, keep sources read-only, and report what the inputs cannot prove.

## Verified by

- On a completed run, for every asset and period, opening plus movements equals closing for cost, accumulated depreciation and net book value within approved rounding shown where it arises, plus any approved translation as its own movement; each later period opens from the prior closing.
- Published results equal values derived independently from the sources and approved rules: each period's charge, accumulated balance, disposal and transfer recomputed for every kind of asset the inputs exercise.
- Depreciation follows the approved method, life, residual, start and stop rules; an asset at its approved residual is charged as approved, and a cost adjustment changes charges only as its approved treatment says.
- A partial disposal removes the approved share of cost and of accumulated depreciation and the remainder continues as approved; a full disposal leaves nothing and no later charge; no gain or loss is computed.
- A transfer moves cost and accumulated depreciation between owners as the approved attribution says, in one period, with no addition and no net-book-value change within a currency beyond approved translation.
- Within each entity and currency, a parent equals the sum of its components, each component counts once at every roll-up level, and rows of different levels are never summed into each other.
- On a completed run, an asset with no policy assignment stays visible every period with its amounts and a named state as approved, and takes no charge the approved rules do not give it; under a fail policy the run names it.
- An asset outside the approved scope or reporting currency is shown or counted with its reason as approved, converted only under an approved rate rule and never added to another currency's totals, and each total states how many assets and what amount it leaves out.
- Closing cost and accumulated depreciation sit beside the ledger at the approved key with signed differences; a key on one side only still appears, and no difference is hidden by a tolerance, reclassified or posted away.
- On a completed run, every source event is applied or set aside as approved, shown or counted with its reasons; counts and amounts add up to the source by event and amount (a part-applied event shows both parts), set-aside amounts move no figure, and a fail policy names each offender.
- Every movement traces to the event, rate or computed charge behind it, and the detail sums to each published movement column.
- The outcome states which exceptions and ledger differences remain open and what the inputs cannot prove, such as whether a late change restates earlier periods.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile the asset events (types, dates, amounts, shares, owners, currencies), the parent and component links, the policies and their assignments, and the ledger balances (classes, entities, currencies, periods, signs), and check that every event names a known asset and that each asset's policy can be found. Use Ask first only for semantics still open, and record each decision as the user's own answer. Keep policies, assignments, the reporting window and the ledger key map explicit and editable where the approved rules allow. Derive the expected register and roll-forward independently of the models from the rules and the inputs before trusting them, and cover disposals, transfers, cost adjustments, assets at their residual or without a policy, and each exceptional event kind the inputs carry; prove a branch the inputs do not exercise on a small labelled set. The register, roll-forward, ledger comparison, movement detail, exceptions and completeness must never disagree about an asset or an amount. Report every exception left open and what the inputs cannot prove.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which assets (land, assets under construction, leased or expensed items), classes, entities and currencies are in scope, which roll-up levels are published, and is a foreign-currency asset converted (which rate and date), shown in its own currency or set aside?
- If unresolved, which period calendar and window apply, where do opening balances for assets older than the window come from, which date (event or recorded) places a late or backdated event, and is it restated or applied in the period it is recorded?
- If unresolved, which method, life, residual, start and stop rule apply to each class (no-charge classes, assets at residual), how are part-periods and rounding handled, how is a cost adjustment applied (prospectively, by catch-up or restated), and when does a life or method change apply?
- If unresolved, is a partial disposal share taken from the original or the remaining cost, how is accumulated depreciation removed with it, what does the remainder depreciate on, and what happens to a share above what remains?
- If unresolved, what links an event to an asset and a component to its parent, when does a transfer take effect, how is accumulated depreciation split between the owners, which policy applies when an assignment changes, and how is a class change handled?
- If unresolved, what shows for an asset with no policy assignment (a charge-free visible state, a failure or another approved treatment)?
- If unresolved, which ledger accounts map to cost and accumulated depreciation, with which sign, difference direction and key, and what shows when one side has no balance?
- If unresolved, which events are exceptions (unknown asset or event type, duplicate, share out of range, outside the asset's life), how is a reversal or correction applied, one row per reason or one primary, and is an exception counted or listed, or does the run fail?

### Guardrails

- Do not choose the method, life, residual, start or stop rule, adjustment treatment, disposal basis, transfer attribution, ledger mapping or exception handling for the user, and take none from the data or common practice; the user may ask for alternatives or a recommendation.
- Never depreciate an asset at a policy the approved assignments do not give it, and never default a missing policy, cost or date to zero or to another value unless an approved rule says so.
- Never net or translate distinct entities or currencies together, and never add a parent row to the components it summarises.
- Never create an addition from a transfer or a cost adjustment, and never remove more than the approved share of cost and accumulated depreciation together.
- Never drop or double count an event or an amount; every event or asset that cannot be processed stays visible or counted with its reason as approved, or in an explicit run failure.
- Never absorb a ledger difference into a movement, a tolerance or a class; it stays visible and unclassified.
- Stop at the register, roll-forward and ledger comparison: do not post journals, work out gain or loss, or change the source events or the ledger.
