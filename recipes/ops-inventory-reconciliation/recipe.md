---
id: ops-inventory-reconciliation
title: Reconcile inventory positions across warehouse, ERP and physical counts and give every difference a reason
trigger:
  - The warehouse system, the ERP and the last stock count report different quantities for the same item and nobody can say which is right or why.
  - A stock count is due and the variance report is a spreadsheet that cannot tell a counting error from a timing difference or a posting error.
  - Finance asks why book inventory differs from what is on the shelf before the books close.
description: At the approved grain and count date, set warehouse, ERP and count quantities side by side in one unit, give each pair of systems its own difference and reason under approved rules, keep what no rule explains visible, and account for every record of every input.
pitch: Put three inventory systems side by side and give every difference a reason, with nothing quietly absorbed.
job_category: build
area: transformation
readiness: supported
domain_objects:
  - inventory_position
  - stock_count
  - stock_movement
  - item_location
  - unit_of_measure
  - reconciliation_difference
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
  - A timing reason needs a movement log and evidence the approved rule accepts of which system lagged.
  - Quantities only; valuation, availability promising and consignment ownership settlement are separate outcomes.
  - Inputs are landed tables; loading files or extracts belongs to file-drop-to-bronze.
  - Stops at the classified reconciliation; posting adjustments back to a system is a separate outcome.
  - Reproducing a past count date after rule or source changes needs kept history of the sources.
related:
  - finance-gl-subledger-tieout
  - effective-dated-business-rules
  - dbt-snapshot-history
  - file-drop-to-bronze
  - governed-spreadsheet-table
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

Build <reconciliation_model>, <in_transit_model>, <coverage_model> and <completeness_model> from <warehouse_position_source>, <erp_position_source>, <count_source> and <movement_source>. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only the semantics they leave open. At the approved count date or dates and item-and-location grain, or a finer grain where approved, set the warehouse, ERP and count quantities side by side in one unit of measure, give each pair of systems its own signed difference and the reason it differs under the approved rules and precedence, show the amount each reason explains and what is left over, and keep what no rule explains visible. Keep stock the approved rules hold out of on-hand, such as stock in transit, out of the comparison and publish it separately, and place every record of every input as matched, in a difference, left out with a reason or listed as a problem. Keep sources read-only and report what the inputs cannot prove.

## Verified by

- On a run that completes, at each in-scope key the warehouse, ERP and count quantities appear side by side in the approved unit, each pair with both sides present has its own signed difference, and nothing is summed across units, plants or entities the approved rules keep apart.
- An absent position, an uncounted item and a blank or unreadable quantity are never read as zero unless the approved rules define that absence as zero: each is reported with its reason, or fails the run, as approved, and a recorded count of zero stays a count.
- On a run that completes, each pair with a difference, a missing side or a rule-given unit reason carries the approved-precedence reason plus other fitting reasons the rules keep; amounts follow the approved claim order and partial-claim rule, and explained plus left over equals any difference.
- On a run that completes, a difference no approved rule explains stays visible as left over or unexplained, never absorbed into a reason or an adjustment; a difference inside the approved tolerance stays visible and is called matched only where the approved rules say so.
- A timing reason appears only where the approved timing evidence is present and it claims no more than that evidence accounts for; without the evidence the difference falls to the next approved reason.
- Where a count was recounted, the governing record follows the approved rule, superseded and conflicting records stay visible with their reasons, and a recount explains only the amount the approved rule gives it.
- Stock the approved rules keep out of on-hand for a system (such as in transit) is reported separately and adds no on-hand quantity to that system's comparison; a status counted on-hand there is compared as on-hand and never also reported as in transit.
- On a run that completes, every input record is accounted for once: a position or count record as matched, in a difference, left out with its reason or a listed problem, a movement as used as evidence, not used with its reason or a listed problem; per input the counts sum to the records read.
- Records the approved scope leaves out are counted and listed with their reason and move no comparison; a code no cross-reference resolves follows the approved disposition, listed with its reason, and is never dropped or read as an uncounted item.
- A bad record (unresolvable code, disallowed duplicate, unreadable quantity, unit with no factor, or a conversion the approved precision rejects) is listed with its reason and is set aside with a visible count, compared as approved, or fails the run; it never changes another key's result.
- Changing a rule the approved requirements hold as data (count date, tolerance, reference system, unit factors, cross-references, scope, reasons and their precedence) changes the published figures without a code change, within the approved rule form, and the result still reconciles.
- Each output is unique on its declared grain, each published difference traces to the source records behind it, and each pair's difference, reason and explained amounts equal values derived independently from the sources and approved rules.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile each input for keys, units, statuses, dates and posted times, and check the cross-references, unit factors, count scope and movement log before modelling. Derive the expected results independently of the models, from the approved rules and the input data, and include a case for each approved reason at its edge: an absent side beside an observed zero, a recount with a remainder, a movement that explains only part of a difference, and a record that trips two rules at once. Keep every approved rule (date, tolerance, factors, cross-references, scope, reason precedence) as data that the models and tests read, never as a literal. Before declaring the outcome complete, check that each pair's difference, explained amount and leftover add up, that every input's records are placed once, and that a changed rule moves only what it should; report what the inputs cannot prove.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which items, locations, plants and legal entities are in scope, which locations or item types does the count not cover (each left out with a listed reason), and which unit, factors and quantity precision apply: is a fractional conversion exact, rounded or a problem?
- If unresolved, which count date or per-item count dates (cycle counts), cutoff time and time zone, and as-of reading per system apply, which system is the reference, and in which order and sign is each pair taken?
- If unresolved, which reasons exist and how is each identified, which wins when several fit and may a pair carry several, in what order do reasons claim amounts, may a reason claim part of a larger movement or recount, and is a unit-only difference matched or reasoned?
- If unresolved, what makes a difference timing (which movements, including adjustments posted after the count, posting system, posted times, window length, stock in transit across the count date), and which location does an in-transit movement explain?
- If unresolved, which stock statuses and ownership types (own, consigned, third-party) count as on-hand in each system and which stay out (in transit, quarantine, blocked, returns), and is finer stock (status, lot, serial, bin) summed to the location or kept apart?
- If unresolved, is a system's absent position nil stock or missing, how does the count tell a counted zero from a never-counted item, are several count lines summed or recounts, which record governs, and is a negative quantity a value or a problem?
- If unresolved, what tolerance applies (absolute or relative, inclusive edge), may a difference inside it be called matched, and does an unexplained residual or a bad record fail the run or stay listed?
- If unresolved, how does each system's item and location code resolve to one canonical key, and is a code that resolves to none a listed problem, a listed exclusion or a failure?

### Guardrails

- Do not choose reasons, precedence, tolerance, timing evidence, window, unit factors, scope or bad-record handling for the user, and take none from the data or common practice; the user may ask for alternatives or a recommendation.
- Never read an absent position, an uncounted item or a blank or unreadable quantity as zero unless the approved rules define that absence as zero; a recorded zero is a count.
- Never let a reason claim more than it explains, never absorb a leftover into a reason or an adjustment, and keep an unexplained difference visible.
- Never sum or compare quantities across units, plants or entities the approved rules keep apart, never compare unconverted quantities, and never round before comparing unless the user approved it.
- On a run that completes, never drop or double count a record: every record of every input stays accounted for, including superseded, out-of-scope, in-transit and problem records.
- Do not invent timing evidence the inputs do not carry, and do not admit a movement the approved evidence rule does not admit.
- Do not hold a rule the approved requirements treat as data as a literal in the models; keep it as data that the models and tests read.
- Stop at the classified reconciliation: do not post adjustments to the ERP or the warehouse system, value inventory or plan counts, and keep sources read-only.
