---
id: sales-lead-opportunity-lifecycle
title: Build an auditable lead-to-account-to-opportunity lifecycle that counts deals and new customers once
trigger:
  - Leads, accounts, contacts and opportunities sit in separate CRM tables and the conversion links are patchy, so nobody can show which lead became which customer or deal.
  - Leads are disqualified, recycled and requalified several times, and counting leads, customers or pipeline value per row double counts them.
  - Several leads feed one opportunity and RevOps cannot say how its value is credited or why it is counted once.
  - Missing or conflicting conversion links are guessed or dropped, so the funnel cannot be audited back to its source rows.
description: Derive one row per lead qualification cycle ending in an accepted, recycled, disqualified or unresolved path, link each lead to its account, contact and opportunity, and count opportunity value and new customers once under approved rules.
pitch: Show how each lead cycle ended and count every deal and new customer once, with missing links left visibly unresolved.
job_category: build
area: transformation
readiness: supported
function:
  - revops
domain_objects:
  - lead
  - lead_cycle
  - conversion_link
  - opportunity
  - new_customer
works_with:
  platforms:
    - duckdb_local
  tools:
    - dbt
qualifiers:
  - Stops at the lifecycle and conversion links; stage conversion and slippage belong to revops-pipeline-snapshots.
  - Needs timestamped lead status history and conversion links naming the records the approved accepted test relies on.
related:
  - revops-pipeline-snapshots
  - master-b2b-account-hierarchy
  - business-event-fact
  - effective-dated-business-rules
evidence:
  features:
    - applying-medallion-data-modelling
    - authoring-dbt-project-artifact
    - generating-dbt-model
    - running-dbt-in-sandbox
    - verifying
  evals: []
---

## Prompt

Build a lead lifecycle <lead_cycle_model> with one row per lead qualification cycle from <lead_status_history>, link each cycle through <conversion_link_source> to <account_source>, <contact_source> and <opportunity_source>, and publish <opportunity_link_model> and <account_customer_model>. Settle from approved requirements the cycle boundaries, outcome and unresolved-reason vocabularies, link keys and accepted test, how several leads share one opportunity, the new-customer rule, the opportunity value and the as-of basis. Each cycle ends accepted, recycled, disqualified or unresolved, and missing links stay unresolved. Every delivered row is used, or shown or counted with its reason as approved.

## Verified by

- The approved contract fixes the cycle grain and boundaries, outcome and reason vocabularies, link keys, accepted test, attribution, new-customer rule, value rule and as-of basis, plus a worked scenario with independently derived expected outputs for every published relation.
- The lifecycle holds one row per lead and cycle ordinal, its row count matches the cycle count derived independently from the source rows, and each cycle carries exactly one of accepted, recycled, disqualified or unresolved.
- Every status event the approved rules keep lands in exactly one cycle. Cycles follow the approved event time, not arrival order, so out-of-order delivery gives the same lifecycle, and a re-delivered record counts once under the approved duplicate rule.
- A cycle is accepted only where the approved links resolve and agree. Each unresolved cycle names one reason from the approved vocabulary, and no link is inferred, reassigned or repaired from another.
- Several leads on one opportunity keep their own cycles and links, and each opportunity's value is counted once under the approved attribution. For an opportunity with a credited lead, the credited value adds up to its value once, never once per lead; one with none shows why.
- Each account's new-customer status follows the approved rule and its count matches an independent derivation. A later conversion into the account, from a recycled lead or another, is classified as the approved rule says, with its reason.
- An opportunity's value is the amount the approved rule selects at the approved time and matches an independent derivation. A correction counts as the approved rule says and a record dated after the as-of date is not used. A missing amount stays null with a reason, never zero.
- Running with a different approved as-of basis gives verdicts that match an independent derivation for that date. Records dated after it are shown or counted with their reason as approved and affect no verdict or value.
- Every delivered lead, status event, conversion link, account, contact, opportunity and version lands in a result or is shown or counted once with its reason as approved, and unaccounted residue is zero. The outcome states how many records were excluded and why.
- Published results equal values derived independently from the source rows and approved rules, not from the model's own logic. A reader counting every link, every accepted cycle or every conversion as a customer gets a wrong total.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain and sources. Confirm the status, conversion and opportunity-history references resolve on the target and profile their keys, duplicates, status values, timestamps and amounts. Use Ask first only for unresolved semantics, then record the contract and a hand-worked scenario with expected outputs for every published relation before writing model logic. Cover each case the approved rules distinguish, such as a requalified and a re-engaged lead, an open cycle, each missing link in turn, a contact or opportunity on another account, several opportunities in one cycle, several leads on one opportunity, a repeat conversion into an account, re-delivered and out-of-order events, a conversion or version dated after the as-of date, a corrected amount and a missing amount. Publish the lifecycle, the opportunity links with their attribution, the account new-customer verdicts, the records shown or counted with their reasons and the accounting. Report counts, amounts, expected and actual results and exceptions.

### Compose

- profiling-source-data
- applying-medallion-data-modelling
- authoring-dbt-project-artifact
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- evaluating-dbt-project
- verifying

### Ask first

- If the approved requirements do not settle it, which statuses end a cycle and map to accepted, recycled and disqualified, what opens a new cycle after one ends, and which reason a cycle still open at the as-of date carries within unresolved.
- If evidence does not settle it, which keys link a lead's cycle to its conversion, account, contact and opportunity, and which links an accepted cycle needs to resolve and agree, such as a contact on the account or an opportunity on the account.
- If unspecified, what each unresolved reason is called, which precedence applies when several apply to one cycle, and how a conversion recorded on a cycle that did not qualify, or naming several opportunities, is reported.
- If several leads feed one opportunity, how its value is attributed (first, last or primary lead, an equal or weighted split, or the opportunity alone), how ties break, and what a non-credited lead carries.
- If unresolved, what makes an account a new customer, how a recycled lead, a second lead into the same account or a lead into a different account counts, and how customers that predate the history are treated.
- If unspecified, which opportunity amount is the value (in force at the as-of date, at conversion or only when won), its currency, how a correction or a missing amount is handled, and whether stage affects any count.
- Unless the user has confirmed it, where the as-of date comes from, how records dated after it are shown, which time orders events and breaks ties, and which delivered record wins when an id is repeated.
- If unresolved, which leads, accounts and opportunities are in scope (test, internal, partner, merged or deleted records), whether excluded records are listed or only counted, and whether any aggregate cut beyond the detail is wanted.

### Guardrails

- Do not infer or repair a link by name, email, domain or proximity, or reassign a conversion to another account or opportunity. A link that cannot be shown stays unresolved with its reason.
- Do not copy an opportunity's full value onto every lead, and do not sum amounts across lead rows as if each opportunity landed once per lead. Keep leads, cycles, opportunities and accounts at their own grains.
- Do not count a recycled or re-engaged lead's later conversion, or a second lead into an existing account, as a new customer unless the approved rule says so. Never count customers per cycle or per lead unless approved.
- Do not use the run date as the as-of date unless approved, order cycles by arrival, or back-date a record that was delivered late. Report records dated after the as-of date instead of dropping them.
- Do not turn a missing amount into zero, add amounts in different currencies, or let a later opportunity stage change an accepted cycle unless approved.
- Do not build stage snapshots, conversion rates, forecasts, win rates, account hierarchies or contact identity resolution. Keep to the lifecycle, links, attribution, new-customer verdicts and accounting.
- Keep Domain sources read-only. Use only an approved, labelled synthetic fixture or a writable fixture with a verified reset, isolated by schema in every layer, and say that it stands in for the CRM.
- Execute on the actual supported Intent target and sandbox; support covers duckdb_local only.
