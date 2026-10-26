---
id: finance-fixed-asset-rollforward
title: Build a fixed-asset register and reconcile its net-book-value roll-forward
trigger:
  - Every month someone rebuilds the fixed-asset register and depreciation schedule in a spreadsheet to prove that opening value plus additions less depreciation and disposals equals closing value.
  - A partial disposal, a transfer between entities or a cost adjustment leaves the register, the roll-forward and the ledger disagreeing, and nobody can say which asset moved what.
  - An auditor asks why a class's or an entity's closing net book value, or its difference from the ledger, changed between two periods.
description: Build asset-period movements for cost and accumulated depreciation under the approved policies, roll them up to parent, class, entity and total without counting a component twice, reconcile net book value forward, set closing balances beside the ledger, and keep every unprocessable event or unpoliced asset visible.
pitch: Turn asset events and approved depreciation policies into a register and a net-book-value roll-forward that foot every period and tie to the ledger.
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
  - Needs dated asset events, approved depreciation policies and their assignments, and ledger balances by class and entity.
  - Takes capitalisation, useful life and residual decisions as given; the policies may be captured as editable data.
  - Keeps each currency separate unless an approved translation rule applies; rate sourcing is separate.
  - Recomputes from the supplied events; reproducing a past register after late changes needs kept history.
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

Build <asset_register_model>, <nbv_rollforward_model>, <ledger_comparison_model>, <asset_movement_model>, <asset_exceptions_model> and <asset_completeness_model> from <asset_events_source>, <depreciation_policy_source>, <policy_assignment_source> and <ledger_balances_source> for <reporting_window>. Inherit the semantics the approved requirements establish and resolve only those left open. For each asset or component and period at the approved grain, publish cost and accumulated depreciation as opening, additions, cost adjustments, transfers in and out, depreciation, disposals and closing, with net book value, charging depreciation as the approved policy says. A disposal removes the approved share, and a transfer changes the owner only. Roll up to the parent, class, entity and total at the approved levels, set closing balances beside the ledger at the approved key with every difference shown and none classified, and keep every asset without a policy, every asset outside the reporting scope and every unprocessable event visible, or fail the run naming it, as approved. Account for every event and amount, keep sources read-only, and report what the inputs cannot prove.

## Verified by

- On a completed run, for every asset and period, opening plus movements equals closing for cost, accumulated depreciation and net book value, and each period opens from the prior closing, within the approved rounding shown where it arises.
- Published results equal values derived independently from the sources and approved rules: each period's charge, accumulated balance, disposal and transfer recomputed for every kind of asset the inputs exercise.
- Depreciation follows the approved method, life, residual, start and stop rules; an asset at its approved residual is charged as approved, and a cost adjustment changes charges only as its approved treatment says.
- A partial disposal removes the approved share of cost and of accumulated depreciation and the remainder continues as approved; a full disposal leaves nothing and no later charge; neither shows a gain or loss.
- A transfer moves the same cost and accumulated depreciation from one owner to another in one period with no addition, and the total across owners is unchanged by it.
- A parent equals the sum of its components, each component counts once at every roll-up level, and rows of different levels are never summed into each other.
- An asset with no policy assignment stays visible every period with its amounts and a named state, and takes no charge the approved rules do not give it.
- An asset outside the approved scope or reporting currency is shown or counted with its reason as approved, converted only under an approved rate rule and never added to another currency's totals, and each total states how many assets and what amount it leaves out.
- Closing cost and accumulated depreciation sit beside the ledger at the approved key with signed differences; a key on one side only still appears, and no difference is hidden by a tolerance, reclassified or posted away.
- On a completed run, every source event ends once applied or listed with one reason; counts and amounts add up to the source, listed events move no figure, and where the approved policy fails the run it names each offending item.
- Every movement traces to the event or computed charge behind it, and the detail sums to each published movement column.
- The outcome states which exceptions and ledger differences remain open and what the inputs cannot prove, such as whether a late change restates earlier periods.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile the asset events (types, dates, amounts, shares, owners, currencies), the parent and component links, the policies and their assignments, and the ledger balances (classes, entities, currencies, periods, signs), and check that every event names a known asset and that each asset's policy can be found. Use Ask first only for semantics still open, and record each decision as the user's own answer. Keep policies, assignments, the reporting window and the ledger key map explicit and editable where the approved rules allow. Derive the expected register and roll-forward independently of the models from the rules and the inputs before trusting them, and cover partial and full disposals, a transfer, a cost adjustment, an asset at its residual and an asset without a policy where the inputs allow; prove a branch the inputs do not exercise on a small labelled set. The register, roll-forward, ledger comparison, movement detail, exceptions and completeness must never disagree about an asset or an amount. Report every exception left open and what the inputs cannot prove.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which assets, classes, entities and currencies are in scope, is the register published per component, per parent or both, and is an asset in another currency converted under an approved rate rule, shown in its own currency or set aside?
- If unresolved, which period calendar and window apply, where do opening balances for assets older than the window come from, and are late or backdated events restated or applied in the period they are recorded?
- If unresolved, which depreciation method, useful life, residual and start and stop rule apply to each class, how are part-periods and rounding treated, where does rounding residue land, what does an asset at its residual show, and is a cost adjustment applied prospectively, by catch-up or restated?
- If unresolved, is a partial disposal share taken from the original or the remaining cost, how is accumulated depreciation removed with it, what does the remainder depreciate on, and what happens to a share above what remains?
- If unresolved, what links an event to an asset and a component to its parent, when does a transfer take effect, how is accumulated depreciation split between the owners, and which policy applies when an assignment changes?
- If unresolved, what shows for an asset with no policy assignment (a charge-free visible state, a failure or another approved treatment)?
- If unresolved, which ledger accounts map to cost and accumulated depreciation, with which sign, difference direction and key, and what shows when one side has no balance?
- If unresolved, which events are exceptions (unknown asset, duplicate event, share outside range, event outside the life of the asset), one row per reason or one primary reason, and are they excluded with a visible count or does the run fail?

### Guardrails

- Do not choose the method, life, residual, start or stop rule, adjustment treatment, disposal basis, transfer attribution, ledger mapping or exception handling for the user, and take none from the data or common practice; the user may ask for alternatives or a recommendation.
- Never depreciate an asset at a policy the approved assignments do not give it, and never default a missing policy, cost or date to zero or to another value.
- Never net or translate distinct entities or currencies together, and never add a parent row to the components it summarises.
- Never create an addition from a transfer or a cost adjustment, and never remove more than the approved share of cost and accumulated depreciation together.
- Never drop or double count an event or an amount; every event or asset that cannot be processed stays visible as an exception or in an explicit run failure, with its reason.
- Never absorb a ledger difference into a movement, a tolerance or a class beyond what the approved rules allow; it stays visible and unclassified.
- Stop at the register, roll-forward and ledger comparison: do not post journals, work out gain or loss, or change the source events or the ledger.
