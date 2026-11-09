---
id: audit-semantic-model-against-sql-and-warehouse
title: Audit a semantic model against its SQL and warehouse, fix the drift the evidence settles, and report the rest
trigger:
  - A semantic model was written once, the marts behind it have moved on, and nobody can say which declared fields, bindings, metric definitions and contracts still match.
  - A metric's description says it cannot run, or says something other than what it returns, and the claim has not been checked since the model last changed.
  - The model's code checks pass, but nobody has compared what its metrics return with the figures the business already trusts.
description: Check a semantic model against its marts' SQL, the built warehouse and the agreed reference figures, report each finding with its evidence, fix what the evidence settles, move each touched contract's version by the approved rule, and leave findings that change what a number means open with their question; code only.
pitch: Find where a semantic model no longer matches its marts and warehouse, fix what the evidence settles, and put the rest to the owner with its evidence.
job_category: build
area: semantic-layer
readiness: supported
function:
  - cross-functional
domain_objects:
  - semantic_model
  - governed_metric
  - data_contract
  - audit_finding
  - metric_reconciliation
works_with:
  platforms:
    - duckdb_local
    - motherduck
    - fabric_lakehouse
    - fabric_warehouse
    - redshift
    - databricks
  tools:
    - dbt
    - ossie
    - odcs
qualifiers:
  - Needs an existing semantic model and the marts it reads; authoring either from nothing is outside this Recipe.
  - Marts, seeds and published values are never changed to match the model; a wrong mart is reported, not edited.
  - Only existing contracts are touched; relations without one are listed as uncovered for the contract-adoption Recipe.
  - A fix that breaks a published contract's readers is an open finding for versioned-data-contract-cutover.
  - Realigning a metric to its stated meaning is here; changing what it means is an open finding.
  - Code only; publishing to a semantic-layer service or BI tool is outside this Recipe.
related:
  - governed-metrics-in-semantic-model
  - bi-calculations-to-governed-metrics
  - adopt-boundary-data-contracts-on-existing-dbt-repo
  - versioned-data-contract-cutover
evidence:
  features:
    - capturing-requirements
    - designing
    - planning
    - semantic-model
    - validating-semantic-model
    - data-contract
    - validating-data-contract
    - running-dbt-in-sandbox
    - verifying
  evals: []
---

## Prompt

Audit <semantic_model> against the marts it reads and <reference_figures>, then fix the drift the evidence settles. Inherit the Intent's repository, platform, Domain, marts and approved requirements, and resolve only the semantics they leave open. Deliver a findings report in which every declared field, binding, metric and contract in the approved scope is either a finding with its evidence and a class (fixed, accepted as approved, or open with its question) or a stated agreement; the model fixed only where the SQL, the warehouse or the reference settles it; each touched existing contract moved to the version the approved rule requires; the checks re-run after the fixes with every finding shown before and after; and each open finding carrying the question it puts to the owner and what each answer would do to a published number. Deliver the changes as code and publish nothing.

## Verified by

- Every field, binding, dimension, relationship, metric and contract in the approved scope has a finding with the evidence it rests on or a stated agreement naming its supporting check; a part left out is listed with its reason.
- Each finding is classed as the approved rules say, fixed, accepted or open; a fix changes only what the SQL, the warehouse or the agreed reference settles, and a change to what a number means is applied only with the owner's approval.
- Each compilable metric equals a value derived independently from the source records under the approved definition, at the approved precision, with before and after for each moved value; each remaining difference to the reference is named and sized, and a refused shape keeps its independent value.
- Every description or note about what a metric can do, what a key matches or which rule applies agrees with what the model returns and the data holds, or is listed as an accepted or open difference with its reason; none is rewritten to read as settled.
- Every relation the model reads has a contract or is listed as uncovered with its reason; model and contract agree on each key, type, relationship and rule they both state, or the difference is listed as accepted or open.
- Each touched contract carries the version the approved versioning rule requires, with the reason shown; an untouched contract keeps its version, and no published promise is withdrawn to clear a check.
- No mart logic, seed or published value differs from before the audit.
- Each open finding names its owner question, the readings the evidence allows, and the size each reading would change a published number, or states that none shows in the data today.
- Each reported agreement names the check behind it and what would have shown a difference; a check that could not run, such as one needing a catalog or built relation that does not exist, is reported unproven with its reason, never as a pass.
- A failure outside the audited scope is named with evidence that it pre-dates the audit; it is neither fixed nor hidden.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, marts and approved requirements, and resolve only the semantics they leave open. Confirm which model, which marts and which contracts are in scope, which reference figures are the independent expected values, and which relations the warehouse actually holds; where a relation is not built, build it only in the approved environment, or report the check unproven rather than treat it as passed. Run the model's code checks and record each finding with the evidence behind it, then compare every metric the model can compile with an independent computation and the agreed reference figures, and note each description or note that claims more or less than the model returns. Settle with the user which findings the evidence alone decides and which change what a number means. Apply the fixes the evidence settles, update the existing contracts the fixes touch, listing relations without one as uncovered, move each touched contract's version by the approved rule, and re-run every check, showing each finding before and after. Leave open findings open with their question and the effect of each reading.

### Compose

- capturing-requirements
- designing
- planning
- semantic-model
- validating-semantic-model
- data-contract
- validating-data-contract
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which semantic model, marts and warehouse are in scope, which parts are out, and which environment may be built to run a check, with what data window, or is that check reported unproven?
- If unresolved, when the model, the SQL and the agreed reference disagree, which is authoritative for each kind of claim, such as a period, population, type, key or description, and which reference figures, window and as-of date are the expected values?
- If unresolved, which findings may the evidence alone settle, and which change what a number means and wait for an owner answer, such as a metric's period, a population rule, a withdrawn mapping or a member the design promises but the data lacks?
- If unresolved, where a model's type or unit differs from the warehouse column, does the model follow the column or is the difference accepted and listed, with a wrong column reported as a mart finding, and to what precision must values match?
- If unresolved, which versioning rule moves a touched contract's version, which changes count as breaking, and is a fix that breaks a reader's contract reported as an open finding for the cutover Recipe?
- If unresolved, where a name or description promises a meaning the data does not carry, such as a fiscal period holding calendar values, is it a defect to fix, a documented difference to accept or an owner question?
- If unresolved, how is a relationship or key finding treated, such as fan-out, orphans, nulls or a new member of a listed dimension, at any rate or above a tolerance, with unmatched rows kept under an explicit member, excluded and counted, or flagged?
- If unresolved, may a model name, field or metric that other models, queries or reports read be renamed or removed by a fix, or is that an open finding?

### Guardrails

- Do not apply a fix that changes what a published number means without approval; put it to the owner as an open finding with the effect of each reading.
- Do not change a mart, a seed or a published value to make the model and the data agree; report the mart as the finding.
- Do not rewrite a declaration, a description or a note to hide a finding that belongs to the data.
- Do not withdraw a published contract promise to clear a check, or leave a contract at its old version after a change that requires a move.
- Do not count a check that could not run, or a warning that stands in for a failing check, as a pass.
- Do not treat a description, a note or an earlier report as evidence; take the evidence from the SQL, the warehouse relations and the reference.
- Do not accept a zero-finding result without confirming each check was able to raise one.
- Do not fix, mute or hide a failure outside the audited scope; name it and show that it pre-dates the audit.
