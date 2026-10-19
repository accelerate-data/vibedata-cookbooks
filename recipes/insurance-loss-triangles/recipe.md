---
id: insurance-loss-triangles
title: Build paid and incurred claims loss triangles by accident and development period
trigger:
  - Reserving analysts rebuild loss triangles by hand in spreadsheets, and a late payment or reserve change pushes back into cells that were already reported.
  - Two runs of the same claims data give different older diagonals, so development methods run on numbers nobody can reproduce.
  - Incurred is read with today's case reserve instead of the reserve as it stood at each evaluation date, and nobody can say which claim transactions a triangle left out.
description: Publish paid and incurred loss triangles by accident period and development age, one per segment, each cell as known at its evaluation date, with every claim transaction counted in a cell or set aside with its reason and the totals tied back to the inputs.
pitch: Reproducible paid and incurred triangles whose older diagonals never move, with every claim transaction counted or explained.
job_category: build
area: transformation
readiness: supported
industry:
  - insurance
domain_objects:
  - claim
  - claim_transaction
  - line_of_business_map
  - loss_triangle
  - expense_total
  - set_aside_transaction
  - coverage_check
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
  - Claims and claim transactions must already be landed as tables with the dates the approved time basis needs.
  - Publishes triangles only; development factors, projections, IBNR, ultimates, reserving and reinsurance are separate.
  - Results are only as complete as the transaction history the source carries; earlier history is not recoverable here.
related:
  - dbt-snapshot-history
  - effective-dated-business-rules
  - revops-pipeline-snapshots
  - finance-gl-subledger-tieout
evidence:
  features:
    - capturing-requirements
    - profiling-source-data
    - applying-medallion-data-modelling
    - generating-dbt-model
    - dbt-unit-testing
    - running-dbt-in-sandbox
    - verifying
  evals: []
---

## Prompt

Build <triangle_model>, <expense_model>, <transaction_accounting_model> and <coverage_model> from <claim_source>, <claim_transaction_source> and <line_of_business_map_source>. Inherit the Intent's sources, platform and approved requirements, and settle with the user only the triangle semantics they leave open. Publish, for each approved segment, cumulative and incremental paid and incurred loss by accident period and development age, each cell as known at its evaluation date under the approved time basis so that a later or backdated posting never changes an older diagonal, cells after the approved cutoff shown as blank and never zero, expense payments handled as approved, periods not yet fully observed marked as approved, and every claim transaction counted in a cell or set aside with exactly one reason, with totals tied back to the inputs and what the inputs cannot prove stated.

## Verified by

- Every claim transaction is in a triangle cell or set aside with exactly one reason, counted plus set aside equals the input by count and by amount for each transaction type, a transaction failing several checks shows the approved winning reason, and a failed run names the offending items.
- Each cell equals an independently derived value from the claim transactions under the approved rules, with the accident period taken from the approved date, cumulative equal to the running sum of the incremental cells, and no cell existing before its accident period begins.
- A posting counts only from the date the approved rule says it became known, so a late or backdated posting changes no cell at an earlier evaluation date, and two builds over unchanged inputs are identical.
- A cell whose evaluation date is after the approved cutoff reads blank and never zero, and an in-scope cell with no movement reads zero under the approved grid shape.
- Incurred equals paid plus the case reserve as it stood at that evaluation date under the approved reserve rule, never the current reserve, and a release or recovery that takes a cell below paid or negative is published as the approved rule says, not silently clamped.
- Recoveries net on the approved date, and expense payments are handled as approved, where they are kept outside loss paid they are published in their own total at the same grain and separation.
- Each approved segment is its own triangle, no cell mixes two currencies or two segments, and the set of segments equals an independently derived in-scope set.
- Accident periods between the earliest and latest claim are present or absent as the approved grid shape says, and under a dense grid a segment with no claim in a period reads zero, never missing.
- The latest evaluation date at or before the cutoff ties claim by claim to each in-scope claim's paid and incurred as known then, and postings known by the cutoff but after that date are listed with the approved disposition.
- The not-fully-developed marker follows the approved rule and is carried on every row of the period it describes.
- Changing an approved parameter held as data, such as the period length, step, evaluation dates, cutoff or reason order, changes the triangles without a code change within the approved rule form.
- The outcome states what the inputs cannot prove, such as when a posting became known where the source holds only an effective date.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements; ask only about triangle semantics they leave open. Sample data, vendor defaults, actuarial convention and existing code are evidence, never policy. Profile the claims first (loss dates, statuses, segment codes, currencies, test and void marks, reopenings), then the transactions (types and signs, posting and effective dates, which date shows when a record became known, duplicates, amounts, missing keys, and the history range the source carries), then the segment map. Keep every rule value, period length, step, evaluation date, cutoff, status vocabulary and reason precedence as editable data. Derive each case's expected result independently of the models, from the inputs and the rule data, before comparing: a loss on a period boundary, a posting on an evaluation date, a backdated posting, a recovery larger than the payments, a reserve released below zero, a reopened claim, a claim closed with no payment, a duplicate id, a posting before the loss date, a posting after the cutoff, a posting between the last evaluation date and the cutoff, a test claim, a claim with no loss date, an unmapped segment code, a missing currency and a segment with no claim in a period. Make every cell read only what was posted by its evaluation date. State what the inputs cannot prove.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which date places a claim in an accident period (loss, report or policy), how long is a period, what is the development step, how is age counted and labelled, which evaluation dates and cutoff apply, and how is a period not yet observed as far as the oldest marked?
- If unresolved, which date shows when a transaction became known (posting or effective), how are backdated, late and reopened claims' postings dated, and what does the source carry that proves when each became known?
- If unresolved, which transaction types make up loss paid, how recoveries net and on which date, whether expense payments are separate or included, whether amounts are gross or net of reinsurance, and whether any capping or adjustment applies?
- If unresolved, how is the case reserve at a date derived (signed changes or stated levels), is incurred shown with or without IBNR, and is a negative or below-paid result kept, flagged or floored?
- If unresolved, how are segments defined (line of business, currency or both), how is the segment map applied to an unmapped code, and is any conversion between currencies approved or never done?
- If unresolved, which claims count (open, closed, reopened, test, void, closed without payment), what is the exempt population and where do its transactions go, and how are claims with no loss date or no currency treated?
- If unresolved, what makes two transactions duplicates, which wins, in what order do the set-aside reasons apply, and how are postings before the loss date, after the cutoff, or between the last evaluation date and the cutoff handled?
- If unresolved, is the grid dense or observed-only, how are missing periods between claims shown, what happens when a check fails (set aside, flag or fail the run), and who may read claim-level listings?

### Guardrails

- Do not choose the accident period basis, time basis, paid and incurred definitions, segments, population, duplicate rule, reason order, cutoff or disposition for the user, and take none from sample data, a vendor default or actuarial convention.
- Never let a cell read a posting made after its evaluation date, and never rewrite a published diagonal when a later or backdated posting arrives.
- Never treat blank as zero: a cell after the cutoff stays blank, and an in-scope empty cell is zero only where the approved grid says so.
- Never drop or double count a transaction; every record sits in a cell or in the set-aside listing with one reason, and records no rule can place are listed, not repaired.
- Never sum amounts across currencies or segments without the approved rule, and never floor, clamp or hide a negative paid or incurred cell unless the user approved it.
- Never put expense payments inside loss paid, or recoveries on the loss date, unless the user approved it.
- Never publish claim-level listings beyond the approved readers, and never put real claims data in a fixture, a PR or a Recipe.
- Stop at the triangles and their accounting: do not compute development factors, project, estimate IBNR or ultimates, set reserves, price, cede to reinsurance or file regulatory schedules.
