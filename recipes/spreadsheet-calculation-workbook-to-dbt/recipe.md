---
id: spreadsheet-calculation-workbook-to-dbt
title: Rebuild a calculation workbook as governed inputs and dbt models compared cell by cell
trigger:
  - A calculation is run in a hand-edited workbook every period, and nobody can prove what it does or why a number came out as it did.
  - The team wants the workbook's lookups, formulas and manual adjustments in governed tables and dbt models, but its consumers need proof of the same results.
  - Manual overrides are typed into the workbook with no record of who changed a number, when or why.
description: Rebuild one frozen workbook version's calculation as governed input tables and dbt models that publish its output range, keep every manual override as its own record, register what was not carried over, and compare it cell by cell with a fresh recalculation, with a written cutover plan.
pitch: Rebuild a hand-edited calculation workbook as governed inputs and models, compared cell by cell with its own recalculation.
job_category: re-engineer
area: transformation
readiness: supported
function:
  - cross-functional
domain_objects:
  - workbook
  - dbt_model
  - consumer_contract
  - manual_override
  - conversion_register
  - parity_report
  - cutover_plan
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
  - Needs the workbook file and a recalculation of its formulas by an evaluator that shares no code with the dbt models.
  - An evaluator the sandbox does not ship must be installable there, which may need network access.
  - Stops at models, a cell comparison, a register and a written cutover plan; the workbook is neither edited nor retired.
  - Ongoing spreadsheet landing belongs to governed-spreadsheet-table; notebook and SQL sources to their own Recipes.
related:
  - governed-spreadsheet-table
  - legacy-sql-to-dbt
  - notebook-transformation-to-dbt
evidence:
  features:
    - capturing-requirements
    - designing
    - planning
    - executing-the-plan
    - generating-dbt-model
    - verifying
  evals: []
---

## Prompt

Replace the calculation in <workbook> with governed input tables and dbt models in the current Intent, so that <consumers> can read a published result equal to the workbook's <output_range>. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and settle only the semantics they leave open. Deliver the inputs, the models, a record for every manual override, a register that names and classes everything in the workbook that was not or could not be carried over, a cell-by-cell comparison against a fresh recalculation of the workbook's formulas on the agreed scenarios, and a written cutover and recovery plan that nothing executes. Reproduce the workbook's own behaviour for repeated lookup keys, unmatched keys, blanks, errors and rounding as approved, report every difference, and leave the workbook unmodified, with its status in the meantime as approved.

## Verified by

- The published result carries the workbook's output range as approved: the same columns, order, row grain, types and scale, with one row for every record of the approved scope unless the approved rule sets one aside or fails the run; each record set aside is listed with its reason.
- Every published cell in the approved compared scope equals the recalculation of the workbook's own formulas, never a saved cell value, at the approved precision, one comparison record per cell; a cell the evaluator cannot reproduce is listed as unverifiable and never counted as matched.
- Expected results derived by hand from the formulas for the agreed scenarios, independently of the models, equal the published values and the recalculation, so the models are never checked only against themselves.
- A saved cell value that disagrees with its own recalculated formula is reported with both values and never accepted as evidence; the published value equals the recalculated one.
- A repeated lookup key, an unmatched key, a blank against a zero, a formula error and a rounding step each follow the approved rule and match the workbook's own result, or appear as a named approved difference; none becomes a silent zero, drop or default, and each is listed with its reason.
- A formula error follows the approved rule: carried with the error kind the recalculation shows, or the run fails naming the cells; every dependent cell, aggregates included, is listed and no unrelated cell changes.
- Every manual override appears once as its own record with the value set, the formula result it replaced, and who, when and why where the workbook or an approved source supplies them, marked missing otherwise, and is applied on its row unless the approved rule holds it.
- An override lacking a reason or approver follows the approved rule, is counted by a completeness check, and is never dropped, hidden or given an invented reason.
- Changing one input moves exactly the cells that depend on it as the approved scope names them in advance, and nothing else; a re-run with no input changed moves no cell, a volatile cell being exempt only as approved.
- A register names every lookup, formula layer, override, pasted-in value, named range, external link, macro and other element as preserved, changed on purpose with its approval, unsupported or out of scope, with the reason; any unsupported element keeps the conversion stated as partial.
- The cutover and recovery plan names the parallel period, who signs off, what counts as matching, the conditions for cutting over and the consumers' step back, which never equates reverting code with reversing data; nothing in it has been run and the workbook stays unmodified.
- The comparison states what it cannot prove, such as behaviours the agreed scenarios never exercise, and equivalence is claimed only for the compared scope.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements. Read the workbook end to end first: every sheet, lookup table, formula layer, pasted-in value, named range, manual override, external link and macro, and which cells the consumers read. Freeze the version being converted, and settle how a reference result is recalculated from its formulas by an evaluator that shares no code with the models; check the evaluator against hand-derived expectations on the workbook's own tricky cases, including its rounding rule, before relying on it, and name where it runs and what it needs. Derive the expected results by hand for the agreed scenarios, independently of the models. Build the inputs as governed tables that keep a blank distinct from a zero and keep lookup rows in the workbook's own order, then the models so that each lookup, error and rounding step has one owner and rounding happens only at the approved places. Publish overrides as their own records, applied after the formula result or held as approved, with the replaced value kept. Run the build in the sandbox, prove equivalence cell by cell, run the changed-input check, write the register and the cutover plan, and state what is not proven.

### Compose

- capturing-requirements
- designing
- generating-dbt-model
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which workbook version and period is converted, which rows and sheets count as records (hidden, filtered, total, blank and note rows) and which are set aside with reasons, and what counts as unchanged output: columns, order, row grain, types and scale?
- If unresolved, how lookup keys are matched (exact or approximate, case, trailing spaces, wildcards), how a repeated key and an unmatched key are treated, such as first match, last match, set aside or fail, and which are listed as exceptions?
- If unresolved, how a blank and a zero flow through each formula, how text that looks like a number and the date system are read, and how a formula error reaches the output and its dependents: carried with its kind, or the run fails?
- If unresolved, where rounding is applied and by which rule, whether arithmetic is binary or decimal, and whether the comparison is exact or within an approved tolerance?
- If unresolved, how a manual override is identified (typed constant, pasted value, adjustment column), where its who, when and why come from, and what happens to one without a reason or approver: apply and flag it, or hold it and flag it?
- If unresolved, how the reference result is obtained, which scenarios and changed inputs are compared, which cells must match, and what happens to cells the evaluator cannot reproduce, such as volatile, circular, array or user-defined ones: frozen, held out and listed, or fail?
- If unresolved, how each pasted-in value, named range and other workbook element is classed: carried, changed on purpose with whose approval, unsupported or out of scope; an external link or macro is listed and never run unless the owner widens the scope?
- If unresolved, how consumers cut over and go back: the parallel period, who signs off, what counts as matching, and the workbook's status in the meantime?

### Guardrails

- Do not read a value saved in a workbook cell as evidence of what its formulas return; the reference is a recalculation, and a saved value that disagrees is reported, not accepted.
- Do not edit, rewrite or retire the workbook, and do not let any model write to it; it stays the system of record until the owner decides otherwise.
- Do not fill a blank with a zero, an error with a number or an unmatched lookup with a default; carry each as the approved rule says and keep it visible.
- Do not drop, hide or reorder a manual override, and do not invent its reason or approver; an incomplete one is applied or held only as approved, and always counted.
- Do not round at a step the approved rule does not name, and do not widen a tolerance or narrow the compared cells, scenarios or range to make the comparison pass.
- Do not run a macro or follow an external link unless the owner widens the scope; list each with what it does and class it, so the conversion is never called fully equivalent while one stays unsupported.
- Do not change the workbook's behaviour silently: a deliberate change needs its recorded approval, and a defect found is reported as follow-up, not corrected in the rebuild.
- Do not treat a green build or a passing test suite as proof of equivalence; the proof is the comparison against the recalculated workbook.
- Do not execute any step of the cutover plan, load the workbook on a schedule, or extend the work into eligibility, payout or other rules the workbook does not compute.
