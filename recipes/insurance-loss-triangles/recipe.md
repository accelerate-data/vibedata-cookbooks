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
  - segment_map
  - loss_triangle
  - expense_total
  - set_aside_transaction
  - completeness_check
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
  - Claims and claim transactions must already be landed as tables with the dates the approved time basis needs.
  - Amount triangles only; claim counts, factors, IBNR, ultimates, reserving and reinsurance cessions are separate.
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

Build <triangle_model>, <transaction_accounting_model>, <completeness_model> and, where expense is kept separate, <expense_model> from <claim_source>, <claim_transaction_source>, <segment_map_source> and any <policy_source> the approved period basis needs. Inherit the Intent's sources, platform and approved requirements, and settle with the user only the triangle semantics they leave open. Publish, for each approved segment, cumulative and incremental paid and incurred loss by accident period and development age, each cell as known at its evaluation date under the approved time basis so that a later or backdated posting never changes an older diagonal, cells after the approved cutoff blank where published and never zero, expense payments handled as approved, periods not yet fully observed marked as approved, and every claim transaction counted in a cell or set aside with exactly one reason, with totals tied back to the inputs and what the inputs cannot prove stated.

## Verified by

- Every claim transaction is in a cell or set aside with exactly one reason, counted plus set aside equals the input by count and by amount per type and currency before any approved cap, floor, adjustment or conversion, and a row failing several checks shows the approved reason.
- Each cell equals an independently derived value under the approved rules, with the accident period from the approved date, each transaction counted once in the incremental cell of the age it first appears in, cumulative equal to the running sum, and no cell before its accident period begins.
- A posting counts only from the date the approved rule says it became known, so a late or backdated posting changes no cell at an earlier evaluation date, a corrected claim date, segment or status applies as approved, and two builds over unchanged inputs are identical.
- A cell after the approved cutoff is never zero and reads blank where published, and an in-scope cell with no movement reads zero under the approved grid shape.
- Incurred equals paid plus the case reserve as it stood at that evaluation date under the approved reserve rule, never the current reserve, and a result below paid or negative is published as approved, not silently clamped.
- Recoveries and reversals net as approved, and expense payments are handled as approved, where kept outside loss paid they are published in their own total at the same grain and separation.
- Each approved segment is its own triangle, no cell mixes currencies or segments except as an approved conversion states with its rate and restatement treatment, and the segments equal an independently derived in-scope set.
- Accident periods between the earliest and latest claim are present or absent as the approved grid shape says, and under a dense grid a segment with no claim in a period reads zero, never missing.
- The latest evaluation date at or before the cutoff ties claim by claim to each in-scope claim's paid and incurred as known then, before any approved cap, floor, adjustment or conversion shown as its own amount, and postings known by the cutoff but after it carry the approved disposition.
- The not-fully-developed marker follows the approved rule and is carried on every row of the period it describes.
- Changing an approved parameter held as data, such as period length, step, evaluation dates or cutoff, changes the triangles, and changing the reason order changes only the reason given to a set-aside transaction, with no code change within the approved rule form.
- A failed run names the offending rows, and the outcome states what the inputs cannot prove, such as when a posting became known where the source holds only an effective date, or when a claim's date, segment or status last changed.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements; ask only about triangle semantics they leave open. Sample data, vendor defaults, convention and existing code are evidence, never policy. Profile the claims first (dates, statuses, segment codes, currencies, test and void marks, reopenings, and whether their history is kept), then the transactions (types and signs, offsetting or voided entries, posting and effective dates, which date shows when a record became known, duplicates, currencies, missing keys, and the history range), then the segment map. Keep every rule value, period, step, evaluation date, cutoff, status vocabulary and reason order as editable data. Derive each case's expected result independently of the models, from the inputs and rule data, before comparing: a loss on a period boundary, a posting on an evaluation date, a backdated posting, a recovery larger than the payments, a reserve released below zero, a reopened claim, a claim closed with no payment, a duplicate id, a posting before the loss date, a posting after the cutoff, a posting between the last evaluation date and the cutoff, a reversed or voided payment, a corrected claim date or status, a currency held on the transaction instead of the claim, a test claim, a claim with no loss date, an unmapped code, a missing currency and a segment with no claim in a period. Make every cell read only what was posted by its evaluation date. State what the inputs cannot prove.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which date and source place a claim in an accident period (loss, report or policy), how long is a period, what is the development step, which evaluation dates and cutoff apply, which cells are published, and how is a period not yet fully observed marked?
- If unresolved, which date shows when a transaction became known, how are backdated, late and reopened postings dated, does a corrected claim date, segment or status apply to all history or only from its correction, and what source proves when each changed?
- If unresolved, which transaction types and expense classes make up loss paid, how do recoveries, reversals and voids net, on which date and by which source field, are amounts gross or net of reinsurance, and does any cap or adjustment apply?
- If unresolved, how is the case reserve at a date derived (signed changes or stated levels), which reserve entry types count as case reserve (bulk, IBNER and IBNR stay separate), and is a negative or below-paid result kept, flagged or floored?
- If unresolved, which claim or coverage attributes define a segment (line, coverage, peril, currency), does each sit on the claim or the transaction, how is an unmapped value treated, and is a currency conversion approved with its rate source, rate date and restatement treatment?
- If unresolved, which claims count (open, closed, reopened, test, void, closed without payment), what is the exempt population and where do its transactions go, and how are claims missing a value the approved period or segment needs treated?
- If unresolved, what makes two transactions duplicates, which wins, in what order do set-aside reasons apply, and how are postings before the approved period date, missing the date the basis needs, after the cutoff, or between the last evaluation date and the cutoff handled?
- If unresolved, is the grid dense or observed-only, how are missing periods between claims shown, what happens when a check fails (set aside, flag or fail the run), and who may read claim-level listings?

### Guardrails

- Do not choose the accident period basis, time basis, paid and incurred definitions, segments, population, duplicate rule, reason order, cutoff or disposition for the user, and take none from sample data, a vendor default or actuarial convention.
- Never let a cell read a posting made after its evaluation date, and never rewrite a published diagonal when a later or backdated posting arrives.
- Never treat blank as zero: a cell after the cutoff stays blank, and an in-scope empty cell is zero only where the approved grid says so.
- Never drop or double count a transaction; every record sits in a cell or in the set-aside listing with one reason, and records no rule can place are listed, not repaired.
- Never sum amounts across currencies or segments without the approved rule, and never floor, clamp or hide a negative paid or incurred cell unless the user approved it.
- Never put expense payments inside loss paid, or recoveries on the loss date, unless the user approved it.
- Never publish claim-level listings beyond the approved readers, and never put real claims data in a fixture, a PR or a Recipe.
- Stop at the triangles and their accounting: do not build claim-count triangles, compute development factors, project, estimate IBNR or ultimates, set reserves, price, cede to reinsurance or file regulatory schedules.
