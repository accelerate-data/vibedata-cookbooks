---
id: customer-rfm-segmentation
title: Score customers with RFM and maintain segments incrementally
trigger:
  - Marketing segment lists come from a spreadsheet or BI export nobody can reproduce, and the same customer lands in different segments depending on who pulled the list.
  - Segments must stay current as transactions arrive without rescoring everyone from scratch, yet match a rebuild from zero for the same date.
  - A cut-off or segment definition is about to change and the owner must see who moves, and why, before it goes live.
description: Score each customer's recency, frequency and spend as of a date from approved transactions, assign one approved segment or an explicit reason, keep every as-of's cut-offs and definitions, and maintain it so each result equals a rebuild for that date, with every segment move explained.
pitch: Repeatable RFM segments that stay current as data arrives, equal a rebuild from zero, and say why a customer moved.
job_category: build
area: transformation
readiness: supported
domain_objects:
  - customer
  - qualifying_transaction
  - rfm_score
  - score_cutoff
  - segment_map
  - customer_segment
  - segment_move
  - definition_version
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
  - Customer, transaction, refund and correction records must already be landed as tables; this Recipe does not ingest them.
  - Customers are scored under the key the Intent supplies; resolving who a customer is belongs to the identity Recipes.
  - Amounts must already be in one reporting currency; other currencies follow the approved handling, never converted here.
  - Rebuilding a past as-of as first published needs recorded dates and detectable deletes on inputs; else it is unproven.
related:
  - identity-golden-record-crosswalk
  - effective-dated-business-rules
  - metric-population-and-rollups
  - incremental-dbt-model-with-contract
  - dbt-full-refresh-to-incremental
  - revops-pipeline-snapshots
evidence:
  features:
    - capturing-requirements
    - generating-dbt-model
    - verifying
  evals: []
---

## Prompt

Build <rfm_model> that scores each customer in <customer_sources> as of each as-of date: recency, frequency and spend from the qualifying transactions in <transaction_sources>, scores cut by the approved method, and one named segment under the approved rules, or an explicit reason the customer is not scored. Inherit the Intent's sources, platform and approved requirements, and resolve any customer semantics they leave open. Account for every customer in exactly one class and every transaction as counted, set aside with its reason, or outside the approved window. Store the cut-offs and definition versions each as-of used, publish each as-of under the approved history rule for late and corrected input, and make a rebuild from zero for any as-of reproduce its maintained result under that rule. For every customer that moved, show where it moved from and to and every approved reason that applies, so a move that time, shifted cut-offs or a definition edit caused is never credited to the customer's behaviour. Nothing is converted, imputed or defaulted to make a customer score unless an approved rule places it.

## Verified by

- In a published result, each customer in the approved population has one row per as-of date it existed on, in exactly one approved class; a customer with no qualifying transaction carries its approved class and reason and no score, and a segment only where the approved placement gives one.
- Each transaction recorded for an as-of under the approved time basis is counted, set aside under one approved reason, or outside the approved window; the three add up to the transactions recorded, with none counted twice or missing.
- Recency, frequency and spend equal independent recomputations from the transactions under the approved window, day basis, amount and refund rules, counting only input the approved time basis allows for that as-of.
- Each score equals a recomputation from that as-of's stored cut-offs or the approved fixed bands; ties are placed as approved and never by row order or run order, and when values are too few for the approved bins the effective bin count is recorded and no split is invented.
- Every scored customer has exactly one segment from the approved map; the map is data under which every score combination resolves to one segment by the approved priority, and a gap or an unresolved priority follows the approved failure rule and never drops a customer.
- Unscored customers appear with their approved reason and stay out of the cut-off population unless approved otherwise; their transactions are still accounted for.
- A rerun on unchanged input changes no published row, an as-of earlier than one already published is refused or handled as approved, and input recorded later changes only later as-of dates and is flagged with the as-of it concerns, unless restatement is approved.
- A rebuild from zero for an as-of, under the same rules and the input the approved time basis allows, reproduces its maintained rows, and any difference the approved policy permits is reported, never hidden.
- Each as-of stores the cut-offs and the version of each definition it used (bands, map, window, time zone); an edit applies from its approved effective as-of and rewrites no earlier published row unless approved.
- A moved customer shows its from and to, every approved reason that applies and a primary by the approved precedence; a reason is set only where its approved definition holds (a definition change only where the new definitions change the segment), and an unexplained move is reported, never defaulted.
- A run that cannot score (absent input, incomplete map, invalid definition) follows the approved failure rule and never publishes a partly scored as-of silently.
- Independent expected results for a labelled case set cover each approved rule that applies (ties, window edges, refunds and corrections, late input, ageing, cut-off shift, definition change, each unscored, excluded or set-aside class); a case an approved rule makes inapplicable is stated as such.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements. Ask only about customer semantics they leave open; sample data and existing code are evidence, never policy. Profile transactions first: statuses, amount and refund shapes, currencies, how dates and recorded dates behave, late and corrected input, ties and skew in each measure, and customers with no qualifying history. Recency ages with the as-of date and quantile cut-offs move with the population, so each as-of is a full recompute of the approved rules over the input it may see, and an incremental model is correct only when it equals that rebuild. Keep windows, bands, scoring methods, segment maps and the time zone as versioned data, so any as-of can be rebuilt with what applied then. Derive expected results independently of the models first, run as-ofs in date order, and prove maintenance by publishing the first as-ofs, appending the next without rebuilding earlier ones and comparing with a rebuild. A later key merge or erasure restates history only as approved.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which supplied customer key a row is for (account, person, company; no matching here), per brand, entity or region, which customers are excluded (staff, test, internal, closed, guest, erased or key removed), and what one with no qualifying transaction gets: no score or a named class?
- If unresolved, which transactions count (statuses, types), whether amounts net discounts, refunds, corrections and exclude tips or tax, which date places a refund, whether a fully refunded line counts, how zero, negative, other-currency and unmatched lines go, and which reason wins (window too)?
- If unresolved, which date places a transaction, in which time zone (one or per customer) and with what day cutoff, and what window (trailing days, all history)?
- If unresolved, how are recency (days since last), frequency (transactions, days or lines) and spend measured, and where do customers whose qualifying history lies wholly outside the window go: a lapsed class, unscored, or lowest?
- If unresolved, how is each measure scored: population quantiles, fixed cut-offs or day bands, how many bins and which direction, where tied values land, which population sets the cut-offs, and what a thin or degenerate distribution does?
- If unresolved, what are the segments, which rules over the scores assign them in what priority, what catches a combination no rule names, where unscored, lapsed and excluded customers sit, and who may read customer-level output with which attributes?
- If unresolved, which as-of dates and how often, may an as-of see only input recorded by it or all now known, does late or corrected input restate history or correct forward, what does an out-of-order as-of do, when does a definition edit apply, and what does a run that cannot score do?
- If unresolved, what counts as a move (segment change, entry, class change), what each reason beyond time, cut-off shift and definition change means, how interacting causes rank, and which is primary?

### Guardrails

- Do not invent customer or segment policy: windows, methods, tie placement, segment names and rules come from approved requirements or the user, and sample data, vendor tools or another Intent's choices are not defaults.
- Do not give an unscored, lapsed, closed or excluded customer a score or segment unless an approved rule places it there, and do not count them in the cut-off population unless approved.
- Do not let row order or arrival order decide a tied customer's score, or fill an empty score band with an invented split; record the effective bin count.
- Do not lose the cut-offs and definition versions an as-of used: every published as-of keeps them, so its scores can be recomputed without re-reading the population.
- Do not rewrite a published as-of unless restatement is approved; new, late or corrected input changes later as-of dates and is flagged.
- Do not credit a move to the customer when time, shifted cut-offs or a definition edit caused it; every approved reason that applies is shown and an unexplained move is reported, never defaulted.
- Do not divide in floating point or round where a score boundary can be exact; use exact arithmetic so equal values tie.
- Do not convert currencies, merge or link customers, or infer missing transactions; set aside what the approved rules cannot count, with the reason.
- Do not carry contact attributes or more customer detail than the approved audience may read.
- Stop at scores, segments and move reasons. Do not activate segments in a campaign or CRM tool, build churn or lifetime-value models, gate contact on consent, or claim runtime savings from incremental runs.
