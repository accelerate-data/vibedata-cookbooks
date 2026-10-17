---
id: people-payroll-gl-tieout
title: Tie payroll to the general ledger at every cut-off and classify every break
trigger:
  - Payroll expense in the general ledger does not match the payroll register at close, and the gap is worked out by hand.
  - Finance cannot say which pay run or cost center explains the difference between the register and the ledger.
  - An auditor asks what an accrual, an off-cycle run or a misposting did to a period, and someone has to rebuild the answer.
description: At the approved reconciliation grain, set the payroll register total, mapped to GL accounts, beside what the ledger posted, explain the difference as breaks classed under approved rules, leave any residual visible as unexplained, and account for every register line and ledger posting.
pitch: Reconcile payroll to the ledger at every cut-off with each break classified and nothing quietly absorbed.
job_category: build
area: transformation
readiness: supported
function:
  - people
  - finance
domain_objects:
  - payroll_register
  - pay_run
  - pay_period
  - pay_code_mapping
  - general_ledger
  - ledger_posting
  - reconciliation_break
  - reconciliation_exception
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
  - Assessed end to end on duckdb_local only; the other listed targets rely on dbt support and are unassessed.
  - Linking postings to pay runs needs a run reference on the ledger or an approved matching rule.
  - Needs a pay-code mapping to GL accounts, supplied or agreed; the Recipe never infers one.
  - Reproducing a past tie-out after rule or source changes needs kept history of the tie-out.
  - Stops at the classified tie-out; payroll calculation, correcting journals and sign-off are separate outcomes.
  - Payroll registers keyed by pay run; document-linked control accounts belong to finance-gl-subledger-tieout.
related:
  - finance-gl-subledger-tieout
  - effective-dated-business-rules
evidence:
  features:
    - capturing-requirements
    - domain-modeling
    - designing
    - planning
    - generating-dbt-model
    - executing-the-plan
    - verifying
  evals: []
---

## Prompt

Build <tieout_model>, <breaks_model>, <accountability_model> and <exceptions_model> from <payroll_register_source>, <ledger_postings_source> and <pay_code_mapping>. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only the semantics they leave open. At the approved reconciliation grain (the dimensions both sides carry, or one carries through an approved allocation) and at each approved cut-off, set the mapped register amount beside the ledger amount, explain the difference as classified breaks, leave any residual visible as unexplained, account for every register line and ledger posting, and keep sources read-only. Apply the approved accrual, class, precedence, tolerance, disclosure and failure rules, publish roll-ups beside the rows as approved, and report what the inputs cannot prove.

## Verified by

- On a run that completes, at each in-scope grain and cut-off, the classified break amounts, including any amount within an approved tolerance and shown as such, plus the unexplained residual sum exactly to the difference in the approved direction.
- On a run that completes, every register line and ledger posting in the approved register and ledger extracts, in scope or not, is accounted for once at each grain it affects: in a tie-out row (matched or contributing to a break), left out with its reason, or a problem with its reason.
- At each grain and cut-off, the register and ledger amounts (under the approved accrual basis, allocation and translation), each class's claim and the residual equal values derived from the sources and approved rules independently of the implementation; each record's disposition fits its row.
- A difference that fits several classes is attributed as the approved precedence and attribution rule say, so no amount belongs to two classes and class amounts plus residual equal the difference; an approved rule held as data governs every record it covers, within the approved rule form.
- Where a pay period spans a cut-off, the register side follows the approved accrual basis for each pay code; the approved attribution rule decides what any approved timing class takes, a late or missing posting is never timing unless that rule identifies it, and what no class takes stays unexplained.
- Where an approved class pairs an attribution to another run or cost center with its counterpart row, the paired amounts are equal and opposite and not counted twice; where the approved rule does not pair them, each claim is as that rule says. An approved allocation's shares sum to the posting.
- Records just inside and just outside each approved tolerance edge, cut-off and period boundary are classed as the approved rules say; where carry-forward is approved, an item stays at every later cut-off until the approved settlement rule settles it, so an open break never disappears.
- A pay code the mapping lacks, a posting with no run or an unlisted account, and a duplicate, void, retro, recharged, invalid or foreign-currency record follow the approved policy: visible with reason and amount or suppressed per the disclosure rule, never dropped, zeroed or given a guessed account.
- Where the approved policy fails the run on an unexplained residual, an unmapped pay code or an unprocessable record, the run fails explicitly, names each offending grain or record with its reason and publishes nothing as complete; every other bullet then applies only to published results.
- Roll-ups published beside the rows sum to the rows beneath them, counting any suppressed row at its hidden value, combine entities or currencies only as the approved mapping, rates and rules say, and carry breaks, residual and counts.
- Where a minimum group size is approved, a suppressed figure is shown as approved with its reason and its records stay accounted for; where complementary hiding is approved, no figure in an approved output lets a suppressed figure be recomputed.
- Each break traces to the register and ledger line ids behind it as the approved identifiers allow, each output is unique on its declared grain with required fields populated, and the outcome states open breaks, exceptions and what the inputs cannot prove.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile the register lines (runs, periods, run kinds, pay codes, entities, cost centers, currencies, signs, dates, duplicates), the ledger postings (accounts, run references, posting kinds, dates, cost centers) and the pay-code mapping, and check which postings carry a usable run reference. Use Ask first only for semantics still open, and record each decision as the user's own answer. Keep the mapping, classes, precedence, tolerance, accrual basis, cut-offs and failure policy explicit, and editable where the approved requirements say so. Derive expected results from the inputs independently of the implementation, and collect evidence from a run on one platform before declaring the Recipe complete. The tie-out, breaks, accountability and exceptions must never disagree about a record. Report every open break or exception and what the inputs cannot prove.

### Compose

- capturing-requirements
- profiling-source-data
- domain-modeling
- designing
- planning
- generating-dbt-model
- executing-the-plan
- verifying

### Ask first

- If unresolved, which pay runs, entities, currencies, cost centers and pay codes are in scope, and which ledger accounts and posting kinds count as payroll (statistical, summary, memorandum, remittance and cash accounts are a user decision)?
- If unresolved, what maps each pay code to a GL account and a debit or credit direction, does it vary by entity or time, which dimensions form the grain, what happens where a side lacks one (reconcile coarser, or allocate under an approved rule), and which roll-ups are published?
- If unresolved, what links a posting to a pay run, may one posting cover several runs or one run several postings (summary journals) and under which allocation, which date places each side, does a past cut-off restate for late postings, and what happens to an unlinked posting?
- If unresolved, which cut-offs are reported, what basis splits a spanning period (calendar or working days, ratable or on pay date or earned period, by pay code), when is an accrual expected and reversed, and does a difference carry forward until what settles it?
- If unresolved, which break classes exist and how is each identified, which wins when several fit and does it take the whole difference or only the part it explains, what tolerance applies (inclusive edge, per row or run), and which way is the difference taken?
- If unresolved, is an unmapped pay code, an unexplained residual or an unprocessable record counted and flagged, excluded with a visible count and amount, or a failure of the run, and is it reported once per reason or once overall?
- If unresolved, how are duplicates, voids, retro adjustments, intercompany recharges and split cost centers treated, and is consolidation or translation across entities or currencies approved, under which mapping and rates?
- If unresolved, which identifiers and amounts may drill-down rows carry, is a minimum group size applied and what counts as a group, how is a suppressed figure shown (marked, merged, omitted), and is complementary hiding required, over which outputs?

### Guardrails

- Do not choose the pay-code mapping, accrual basis, break classes, precedence, tolerance, failure or disclosure policy or population for the user, and take none from the data or common practice; the user may ask for alternatives or a recommendation.
- Never absorb a residual into a class, an adjustment or a tolerance beyond what the approved rules allow, or label a late or missing posting as timing by default; amounts within tolerance and unexplained differences stay visible as such.
- Never net separate runs, entities or currencies together because they share an account, cost center or period, unless the approved grain or rules say so.
- Never drop or double count a record; every unprocessable or left-out record stays visible with its reason and amount, or suppressed under the approved disclosure rule, and an unmapped pay code is never given a guessed account.
- Do not link a posting to a run by amount or date alone, or spread one posting across runs, unless the approved rules say so; report unlinked postings under the approved rule.
- Where differences carry forward, do not drop a run from later cut-offs before the approved settlement rule says it is settled.
- Register lines are personal data: publish names, pay amounts or keys only as the approved disclosure rule allows; where a minimum group size is approved a small group's figure is suppressed as approved, and where complementary hiding is approved it is not exposed through the approved outputs.
- A break records a difference, not which side is wrong; do not assume the register or the ledger is correct.
- Stop at the classified tie-out: do not calculate payroll, post corrections or accruals, or sign off, and keep sources read-only.
