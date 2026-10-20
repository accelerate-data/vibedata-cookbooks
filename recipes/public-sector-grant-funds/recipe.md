---
id: public-sector-grant-funds
title: Track grant funds per award from authorization to drawdown and flag exceptions
trigger:
  - Grants accountants cannot say per award how much is authorized, obligated, spent and drawn, and each report gives a different answer.
  - An amendment, a cancelled commitment, a late posting or a draw ahead of spend changes an award's position and nobody can see why.
  - Program managers and auditors need over-commitment and cash exceptions flagged per award and budget category while every transaction line stays accounted for.
description: For the approved awards, categories and periods, publish authorized, obligated, expended and drawn amounts with unobligated balance, unliquidated obligations and cash position, dated changes applied as approved, exceptions flagged beside the figures, and every source line counted or set aside with a reason.
pitch: Show each award's authorized, obligated, expended and drawn position per budget category and period, with flagged exceptions and every line reconciled.
job_category: build
area: transformation
readiness: supported
function:
  - finance
industry:
  - public-sector
domain_objects:
  - grant_award
  - award_amendment
  - budget_category
  - period_of_performance
  - obligation
  - expenditure
  - drawdown
  - funds_position
  - cash_position
  - funds_exception
  - record_disposition
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
  - Awards, amendments, obligations, expenditures and drawdowns arrive as landed tables; landing them is separate work.
  - A past period as first reported needs kept snapshots or a source arrival date; otherwise it is unproven.
  - Stops at the funds position; allowability, indirect rates, agency reports and budget variance are separate.
  - Tying amounts to the general ledger belongs to finance-gl-subledger-tieout.
  - Commitments come from award records; invoice-to-contract matching belongs to ops-procurement-spend.
related:
  - finance-gl-subledger-tieout
  - finance-budget-forecast-actual
  - effective-dated-business-rules
  - ops-procurement-spend
  - file-drop-to-bronze
evidence:
  features:
    - generating-dbt-model
    - verifying
  evals: []
---

## Prompt

Build the funds position for <grant_awards> from the awards, amendments, obligations, expenditures and drawdowns in <grant_sources>, showing per award, budget category and period the authorized, obligated and expended amounts, and drawn at the grain it is recorded or as an approved allocation gives, with the unobligated balance, unliquidated obligations and cash position as the approved rules define them. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Apply amendments and cancellations under the approved effective-date rule, flag over-commitment, spend without or above its obligation, draws against spend and activity outside the performance period as approved, keep every source line counted, flagged or set aside with its reason so counts, amounts and identities reconcile, show where a late posting lands and what it changes under the approved rule, and report what the checks cannot prove.

## Verified by

- Authorized at each period end follows the approved amendment and performance-period rules and sums across categories to the award plus any authorization the approved rule holds at award level; unless the approved rule restates, a later amendment never changes an earlier period.
- A cancelled commitment counts as obligated through the period the approved rule gives and not after, and appears in a visible de-obligation listing with its date, never silently removed.
- Obligated, expended and drawn accumulate by each line's approved date; unobligated, unliquidated and cash position equal the approved definitions, with any excess shown beside them, and they tie per award and period to the lines.
- Every in-scope award has the rows the approved grid rule gives, quiet periods shown as approved; a figure not recorded at a grain, such as a draw per category, reads as absent, never zero, unless an approved allocation labels it.
- Spend with no obligation or above its obligation, a draw ahead of or behind spend, a draw above authorized and activity outside the performance window in force on its date carry the flags the approved rule gives, in or out of the figures as approved.
- Every source line has exactly one disposition in the approved order: counted, de-obligated, or set aside with its approved reason; counts and amounts add back to the lines landed with no residue, and each set-aside line keeps its reason.
- A re-sent line, reversal, refund or negative line, and a pending, held or returned draw, follow the approved treatment and are never silently dropped or counted twice; a repeat whose values differ is handled as approved and visible.
- A late posting is placed where the approved rule puts it and listed with its arrival and close dates; where a close and arrival signal exists, the affected period's figure before and after is shown, otherwise the restatement is marked unproven.
- Published figures, flags and dispositions equal values derived independently from the source lines and approved rules, including each approved policy branch and the awkward cases present in the sources.
- Amounts in different currencies are never summed or compared unless an approved conversion states its rate source and date.
- A rerun with no new input leaves every figure, flag and disposition unchanged, and a failed run publishes what the approved rule says and names the failure.
- The outcome states what it cannot show, such as allowability, amounts not recorded at a grain and postings not yet received.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain and sources. Inspect the award, amendment, obligation, expenditure and drawdown sources and profile the awkward cases before modelling: amendments and period changes from a date, cancelled and modified commitments, spend with no obligation or above it, draws ahead of spend, dates outside the performance period, re-sent, reversed and unusable lines, unknown awards and categories, mixed currencies and late postings. Use Ask first only for semantics the approved requirements leave open, and record each answer as this Intent's policy, not a default. Resolve each line's disposition in the approved order, apply dated changes as editable rule data, derive the grid and the award figures, attach flags, and build independent expected results from the source lines before comparing the output. Read every output back and record what was not exercised.

### Compose

- generating-dbt-model
- applying-medallion-data-modelling
- verifying

### Ask first

- Which grain, periods (calendar months or the funder's fiscal calendar), budget categories and as-of date are published, are figures cumulative or per period, which periods appear when nothing happened, which currencies apply and are they converted or kept apart, and who may see award-level rows?
- How do dated amendments apply (from their effective date or restated, at award or category level), how do performance-period changes, extensions, a liquidation window, closeout and deobligation of unliquidated balances govern a date?
- What counts as obligated and as expended (subaward commitments, modifications, cancellations), how are unobligated, unliquidated and cash position defined, and which key links an expenditure to its obligation, and what happens to spend with none?
- Which date places a line in a period, how is a late posting shown (own period restated or arrival period), which periods count as closed, and which signal dates a posting's arrival?
- At what grain are drawdowns recorded, is the basis reimbursement or advance, is any allocation across categories approved or left absent, and how are pending, held or returned draws counted?
- Which exceptions are flagged, with what thresholds, may a line carry several flags or one primary flag, and do flagged or out-of-window lines stay in the figures or leave them?
- Which awards, funders, cost share or match, program income, cost types and funding types are in scope, and how are test, closed-out and unknown awards and categories treated, with where out-of-scope and unplaceable lines go?
- What makes two lines the same, how are re-sends with different values, reversals, refunds and negative lines treated, in what order are set-aside reasons applied, are balances signed or floored with an excess column, and what does a failed run publish beside the prior state?

### Guardrails

- Do not restate an earlier period for a dated amendment or cancellation unless the approved rule says so.
- Do not drop or net a line that cannot be placed; give it a disposition and a reason and keep counts and amounts reconciled to the lines landed.
- Do not clamp, floor or net a negative balance, an overrun or an excess draw unless approved; show it beside the figures.
- Do not allocate a draw recorded at one grain to another except under an approved allocation shown as a labelled share, and never read an unrecorded figure as zero.
- Do not link spend to an obligation by guesswork; use the approved key and show spend that has none.
- Do not count a cancelled, reversed or duplicate line beyond what the approved rule gives.
- Do not decide allowability, compute indirect-cost rates or submit agency reports; those are separate work.
- Do not sum or compare amounts across currencies unless an approved conversion states its rate source and date.
- Do not take the as-of date from the run clock, and keep approved category lists, windows, reasons and thresholds as editable data, not code.
- Label synthetic data as synthetic and never land it in a shared Domain relation.
