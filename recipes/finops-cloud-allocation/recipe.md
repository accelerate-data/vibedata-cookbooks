---
id: finops-cloud-allocation
title: Allocate cloud and platform spend to teams and flag untagged cost and daily spikes
trigger:
  - The cloud bill grew and nobody can say which team or product drove the increase.
  - Untagged spend is unknown, or is quietly spread across teams so that no one owns it.
  - Shared platform costs are split by a rule nobody can reproduce, and the shares do not add back to the bill.
  - A daily cost spike is noticed only when the invoice arrives.
description: At the approved grain, assign each billing line to a team, product and environment by its tags, split shared pools by an approved method, keep untagged and unallocated cost visible with its reason, flag daily spikes, and close allocated plus unallocated to each invoice.
pitch: Show which team drives the cloud bill, with untagged cost kept as untagged and every allocation closing to the invoice.
job_category: build
area: governance-cost
readiness: supported
domain_objects:
  - billing_line
  - invoice
  - cost_tag
  - team
  - shared_cost_pool
  - cost_allocation
  - cost_exception
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
  - Billing lines, invoices and tag rules arrive as landed tables; landing a provider export is a separate outcome.
  - Stops at the allocation; budgets, forecasts, commitment optimisation and chargeback are separate outcomes.
  - Currency conversion needs an approved rate source; without one, each currency is reported on its own.
  - Allocation is only as good as the tags and drivers supplied; a wrong but valid tag is not detectable.
related:
  - shift-unit-economics
  - finance-gl-subledger-tieout
  - file-drop-to-bronze
  - database-tables-to-bronze
  - managed-connector-to-dlt
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

Build <cost_allocation_model>, <untagged_cost_model>, <shared_pool_model>, <daily_spike_model> and <invoice_closure_model> from <billing_line_source>, <invoice_source>, <tag_rule_source> and, where recorded or approved, <pool_driver_source> and <owner_source>. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only those they leave open. Assign each in-scope billing line to a team, product and environment through its tags under the approved normalisation, keep lines that no tag or approved mapping places as untagged, missing and invalid apart, with the account owner beside them and never spread without approval, split each shared pool by its approved method to the approved precision, flag daily team spikes under the approved rule, and close allocated plus unallocated to each invoice at the approved grain and cost measure, with every gap and every restated, duplicate, unreadable, tax, credit and other-currency line visible with its reason. Materialize the outputs in the Intent's sandbox and verify them against independent expectations.

## Verified by

- On a run that completes, every input billing line lands once as allocated, pooled, untagged, tax or set aside with its reason, counts and per-currency amounts sum to the input, and nothing counts twice; the properties below hold on published outputs, and a failed run names each bad record.
- Equivalent tag spellings resolve to one team, product and environment under the approved normalisation, and a changed rule value changes the output where the data reaches it, within the approved rule form.
- Lines left without a team after tags and approved mappings are untagged, missing and invalid kept apart, each with its account owner; untagged cost always shows as untagged and reaches a team only as a separate, labelled share under approved redistribution; conflicting tag values are never guessed.
- Credits, refunds, discounts and tax follow the approved treatment and are shown with it; a credit with no usable tag stays visible and reaches no team unless the approved treatment distributes it.
- Each shared pool's shares add back to its total at the approved precision under the approved method, and a pool with no usable basis follows the approved no-basis treatment and stays visible with its reason.
- At the approved grain and cost measure, allocated plus unallocated equals the invoice, or the gap is within the approved tolerance and shown; a gap, a line month with no invoice or an unreadable invoice is flagged, or fails the run naming each item, as approved, and is never plugged.
- Amounts in different currencies are never summed or netted unless an approved conversion states its rate source and date; each currency ties out on its own.
- A restated line counts once under the approved revision rule with earlier revisions visible, and an exact duplicate counts once; where the source gives no approved revision signal, restatement is stated as unproven, and late tag fixes and adjustments follow the approved restatement basis.
- A value that cannot be read, such as a date, an amount, a revision time or an invoice figure, and an account, charge type or service with no mapping, follow the approved disposition: excepted with the raw text visible, or the run fails naming it; none is coerced to a default or dropped.
- Spike flags follow the approved basis, day boundary, threshold, floor and zero-prior-day rule, including a day exactly on each edge; period-level pool shares and a still-incomplete newest day create no flags unless approved.
- The untagged percentage states its numerator, denominator and approved basis and mixes currencies only under an approved conversion; every share, closure figure and flag equals an independent recomputation against invoice figures not derived from the lines.
- The outcome states what the inputs cannot prove, such as a wrong but valid tag, cost with no billing line or amortisation the export hides, and owner names and cost appear only at the approved audience and grain.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile the billing lines (dates, amounts, currencies, charge types, credits, discounts, tax, tag keys and values, restated and duplicate lines), the invoices and the pool definitions before proposing rules. Use Ask first only for semantics still open, and record each decision as the user's own answer. Keep tag vocabularies, aliases, mappings, charge-type treatment, pool membership and method, thresholds and reasons as data a reader can change. Fix expected results independently before model SQL, with invoice figures that are not derived from the lines, and one named case for each tag spelling, untagged kind, partial tag, credit, tax line, restatement, duplicate, pool with a remainder, pool with no basis, other currency, invoice mismatch, line month with no invoice, unreadable value, spike and below-floor jump, and compute shares, closure, percentage and flags in a separate script. Build line attribution, pool shares, invoice closure and the spike series using composed skills and current target dialect and sandbox guidance. Materialize, read back and rerun, compare every output row for row with the expectations, and show that a changed rule value moves the output. Keep the Domain read-only. Report untested cases as incomplete verification.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, the cost measure (billed, net of credits or discounts, amortised), the treatment of each charge type, credit, refund, discount and tax, the accounts, currencies and window, any approved rate source, date and type, and the handling of an unmapped account, charge type or service.
- If unresolved, which tag keys define team, product and environment, which values are registered, which aliases, synonyms and case rule apply, and what counts as invalid: an unregistered value, a blank, or conflicting values for one key, and the precedence for conflicts.
- If unresolved, whether account, project or service mappings or inherited parent tags allocate lines without tags of their own, their precedence over line tags, who owns each billing account, who may see owners and cost, and whether such lines count as tagged.
- If unresolved, whether untagged or unallocated cost stays unallocated or is redistributed, to whom and on what basis, whether a team without a product counts as tagged and what label a missing part carries, and whether the untagged percentage is net or gross of credits.
- If unresolved, which services or accounts form each shared pool, its eligible recipients and driver source and period, the split method (even, by usage, by headcount, by share of direct cost), the rounding and remainder rule, and the no-basis treatment.
- If unresolved, at what grain and cost measure allocated plus unallocated must equal the invoice, what gap tolerance applies, and whether a gap, a line month with no invoice or an unreadable invoice is published and flagged or fails the run.
- If unresolved, which measure the spike rule uses (directly attributed cost or with pool shares), the day boundary and time zone, how the newest incomplete day is handled, the comparison basis, threshold, floor, zero-base rule, series scope and currency.
- If unresolved, how revisions of a line, reissued invoices and additive adjustment lines are identified and treated, how exact duplicates and tied revisions are recognised, whether an unreadable value is excepted or fails the run, and whether a late tag fix restates past periods.

### Guardrails

- Do not spread untagged cost, assign it to a default owner or merge it into a team's direct cost without approval; it always stays visible as untagged with its reason.
- Do not guess a tag when keys conflict without an approved precedence or a value fails the approved validity rule, and do not coerce an unreadable date, amount, revision time or invoice figure to a default.
- Do not charge a shared pool in full to each recipient, drop its remainder, invent recipients, or use a basis the user has not approved; shares reconcile to the pool.
- Do not sum, net or convert across currencies without an approved rate source, date and type, and do not let a credit or refund lower a team's cost beyond what the approved treatment names.
- Do not force allocated plus unallocated to equal an invoice by dropping, plugging or netting; every gap stays an exception with its amount and reason.
- Do not count superseded, duplicate or unreadable lines in any total, and do not drop them from the record.
- Do not let monthly pool shares or period-start effects create daily spikes, and do not flag a rise from a zero base without the approved floor.
- Do not present a synthetic or sample billing set as real cost, or read a tag as proof of who actually consumed the resource.
- Do not publish account owner names or cost below the approved audience and grain.
