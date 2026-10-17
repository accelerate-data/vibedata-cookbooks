---
id: finops-saas-license-utilization
title: Measure SaaS licence utilisation and shelfware against contracts and invoices
trigger:
  - A SaaS renewal is due and nobody can say how many of the paid seats are actually used.
  - The vendor console, the contract and the invoice show different seat counts for the same application.
  - Finance is asked what the unused seats cost and which applications are shelfware before the renewal date.
description: For each application and period, compare the seats the contract entitles, the invoice bills and the console assigns with the seats used under an approved activity rule, publish utilisation, unused-seat cost, shelfware and renewal timing, keep person-level idle seats restricted, and account for every record.
pitch: Measure paid SaaS seats against real use, flag shelfware before renewal, and keep the idle-user list restricted.
job_category: build
area: governance-cost
readiness: supported
function:
  - it-finops
  - finance
domain_objects:
  - application
  - license_contract
  - contract_version
  - invoice_line
  - seat_assignment
  - activity_event
  - seat_identity
  - utilisation_period
  - shelfware_flag
  - idle_seat_list
  - seat_problem
  - suppression_rule
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
  - Contract, invoice, assignment and activity records arrive as landed tables; landing them is a separate outcome.
  - Stops at the utilisation report; renewal terms, deprovisioning and seat reclaim are separate outcomes.
  - Other plan models (usage-based, unlimited, pooled) need an approved treatment before they count as seats.
  - Past periods need assignment history of an approved form; a current-only export leaves them unproven.
  - Restricting the person-level lists needs roles and grants; without them the restriction is a label only.
  - On fabric_lakehouse, SQL grants do not govern OneLake reads, so restriction cannot be assured there.
  - Hiding small groups alone does not make a figure safe to release; totals and sibling cells can reveal one.
  - Unless issued periods are kept as retained copies, a late or backdated event restates the periods it affects.
  - Vendor activity feeds differ; unless approved otherwise, no feed or a declared gap reads unknown, not inactive.
related:
  - people-pay-band-gaps
  - metric-population-and-rollups
  - effective-dated-business-rules
  - pii-classification-and-masking
  - identity-golden-record-crosswalk
  - file-drop-to-bronze
  - database-tables-to-bronze
  - managed-connector-to-dlt
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

Build <licence_utilisation_models>, <seat_tie_out_models> and <restricted_person_models> from <contract_source>, <invoice_source>, <assignment_source>, <activity_source> and <account_source> for <applications_in_scope>. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only those they leave open. For each application and approved period, take the entitlement of record and the price in force, the invoiced seats the invoice lines cover, the assigned seats and the seats active under the approved activity rule, and publish utilisation, unused seats and their cost, shelfware and renewal timing at the approved grain. Compare contract, invoice and console seat counts and publish each difference with its reason under the approved disposition. Keep person-level idle seats, identity exceptions and excluded accounts in restricted relations apart from published aggregates, and hide small groups as approved. Account for every contract line, invoice line, assignment and sign-in identity, show unknown where evidence is missing, and keep sources read-only.

## Verified by

- On a run that publishes, each application and approved period has one row at the approved grain and every figure equals an independent recomputation from the source records; roll-ups use seat-type components, never averaged percentages, and person counts are distinct per cut.
- Entitlement and price are the contract version in force on the approved judging date; lines the approved rules exclude land out of population with a reason; overlaps or gaps the rule cannot resolve read unknown, never silently summed or picked; no contract means zero entitlement only if approved.
- Assigned seats for each period follow the approved way past assignments are known (dates, snapshots or a log); where the source cannot show them the period reads unknown or unproven unless an approved, labelled rule says otherwise; seats in an approved grace period are shown as such.
- Active seats follow the approved activity rule and window; unless the approved rule defines otherwise, a seat whose activity cannot be judged reads unknown, never inactive or idle, and a ratio built on it follows the approved unknown rule (null with a reason, or a labelled partial figure).
- Seats are measured only for approved seat-based licence models; unlimited, usage-based, concurrent, pooled, committed-minimum, trial and free lines land as approved with their reason, never as zero seats; a missing price reads unknown, an approved zero price is zero.
- Unused seats are never negative and over-assignment is shown as approved, never netted into unused seats; unused cost multiplies each seat type's unused seats by its approved price on the approved base, annual converted as approved, and is never summed across currencies.
- Shelfware, days to renewal and renewal due follow the approved threshold, lookahead and renewal date (term end, auto-renewal roll or notice deadline); a missing renewal date reads unknown, never far away.
- On a run that publishes, contract, invoice and console seat counts, where each exists, are compared per application and period with counts and any reason; a difference follows the approved disposition, no count is silently chosen, and a period with no invoice line follows the approved rule.
- Every contract line, invoice line, assignment and sign-in identity is accounted for per affected application and period (once where the rule judges it once) as counted, out of population with its reason, or a listed problem, summing to the input; a failed run names each offending item and reason.
- Seat measures and person measures are stated apart; whether non-person accounts count in seat measures or reach person counts follows the approved rule, and a cut with no entitlement (such as department) shows person measures only unless an approved allocation exists.
- Person-level lists, identity exceptions and excluded accounts sit in separate relations marked restricted and named to the approved readers; where grants are approved a role limited to the published relations cannot read them, otherwise access is reported unproven, not protected.
- Published relations carry no login id, name or identity-derived column; a group is hidden as the approved minimum, outputs, rounding and display say, totals computed before hiding, each disclosure left is stated, and a late or backdated event restates or stays out of an issued period as approved.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile the contract versions, invoice periods and currencies, assignment and removal dates, activity feeds, identities and aliases before proposing rules, and note which applications report no activity or carry licence models other than named seats. Use Ask first only for semantics still open, and record each decision as the user's own answer. Keep the restricted relations apart from the published ones and derive every published cut from the same seat components so they cannot disagree. Fix independent expectations from the source records, including boundary days, overlapping contracts, a feed gap and a month with no contract, and compare every published column with them. Report each exception left open and each disclosure limit the approved hiding leaves.

### Compose

- capturing-requirements
- applying-medallion-data-modelling
- generating-dbt-model
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which contract and invoice lines count (status, credit notes, reversals, non-seat items), which source is the entitlement of record, how amendments, add-ons and overlaps combine, and which date of a period (end, average, peak) judges entitlement, assignment and price?
- If unresolved, what is one seat type (edition, tier, add-on) and how lines map to it, which applications and licence models are measured in seats (named, concurrent, usage-based, unlimited, pooled, committed minimum, trial, free), and how do suite or reseller lines map?
- If unresolved, what counts as active per application (sign-in or named events), over which window, as-of date and time zone, which system supplies activity, how is a gap or missing feed declared and treated, and which key links a sign-in identity to a seat and credits aliases?
- If unresolved, which source classifies accounts and which count as seat-holders (employees, contractors, guests, service accounts, shared mailboxes, offboarded holders), do non-person seats count in seat measures, and how are duplicates and activity with no seat shown?
- If unresolved, which base is the headline and which prices unused cost (entitled, invoiced or assigned), is utilisation capped, how are over-assignment and unknown inputs shown in roll-ups, and is there a grace period for new assignments and how do its seats count?
- If unresolved, what threshold makes an application shelfware, which renewal date applies when several contracts exist (term end, auto-renewal, notice deadline), what lookahead sets renewal due, and does shelfware wait for a renewal date?
- If unresolved, how is the tie-out judged, what happens to a difference (publish and flag, or fail the run), how are periods with no invoice line, several lines or other currencies treated, how are past assignments known, and what rate source and date convert, if any?
- If unresolved, what period and grain are reported, which cuts are published, is entitlement or cost allocated to a cut and how is department assigned, who reads the restricted lists and are grants applied, and what are the minimum group size, rounding, display rule, totals rule and late-event rule?

### Guardrails

- Do not choose the activity rule, window, population, entitlement source, price, threshold, grace, currency treatment, minimum group size or display rule for the user, nor take them from vendor defaults, the data or common practice; the user may ask for options or a recommendation.
- Unless an approved rule says so, never read missing activity, entitlement, price or invoice evidence as zero, inactive or unused; keep unknown with its reason, and never sum or pick between conflicting contracts or counts the approved rules do not resolve.
- Never average percentages, an average price or cell values to build an application, seat-type or company figure; build every roll-up from seat and cost components, and never let unused seats or their cost go negative.
- Never publish a login id, person name or identity-derived value in a published relation, and never publish a measure for a group the approved rule hides.
- Do not describe hiding small groups as anonymisation, and do not claim effective access control from build output alone.
- Do not silently drop a contract line, invoice line, assignment or sign-in identity, merge two accounts into one person without an approved rule, or convert a currency the approved rules do not convert.
- Do not infer an activity-feed gap from silence unless the approved rule defines one; a gap, or an application with no feed, is declared by evidence and reads unknown.
- Do not invent an allocation of entitlement, price or cost to a department or other cut that carries none, or present today's assignments as a past period's unless approved and labelled.
- Stop at the utilisation report: do not propose renewal terms, deprovision or reclaim seats, edit source records or grant access.
