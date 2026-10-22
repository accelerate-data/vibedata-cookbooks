---
id: inventory-lot-traceability
title: Trace a recalled input lot through production to affected shipments and flag lineage that cannot be traced
trigger:
  - A raw material lot is recalled and nobody can say which finished lots and which customer shipments contain it, or how much of it each holds.
  - Lot genealogy lives in spreadsheets or separate receipt, production and shipping systems, and a split or blend makes the same material reach a shipment by several routes.
  - A mock recall must show every affected shipment, and every shipment whose history cannot be followed, within the hour.
description: From observed receipts, production runs that consume and make lots, and shipments, build the lot genealogy with quantities and units on each link, and for a recalled lot list every affected lot and shipment once with the recalled quantity, with unreconciled runs, cycles and untraceable shipments shown.
pitch: Trace a recalled lot to every affected shipment once, and show every shipment whose history cannot be followed.
job_category: build
area: transformation
readiness: supported
function:
  - supply-chain-ops
domain_objects:
  - lot
  - production_run
  - lot_link
  - shipment
  - recall_notice
  - recall_exposure
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
  - Needs observed genealogy, the lots each run consumed and produced; a link is never inferred from dates or numbers.
  - One process and one lot identification scheme per run; other processes or schemes are separate runs.
  - Inputs are landed tables; loading files or extracts belongs to file-drop-to-bronze.
  - Stops at recall exposure evidence; notifying customers and the physical recall are separate outcomes.
  - Stock positions and product hierarchies belong to ops-inventory-reconciliation and master-product-sku-hierarchy.
related:
  - ops-inventory-reconciliation
  - master-product-sku-hierarchy
  - file-drop-to-bronze
  - effective-dated-business-rules
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

Build <lot_lineage_model>, <recall_closure_model>, <affected_shipment_model>, <run_reconciliation_model> and <trace_exception_model> from <receipt_source>, <production_run_source>, <shipment_source> and <recall_notice_source>. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only the semantics they leave open. Hold each recorded link from a parent lot to the lot made from it once, with the run, quantities and unit, never inferring one from dates, adjacent lot numbers or equal quantities. For each recalled lot, list every descendant lot and shipment holding its material once however many routes reach it, with the recalled quantity (and share where the rule gives one) under the approved attribution rule through every split and blend. Reconcile each run's quantity in against quantity out plus declared loss under the approved tolerance and show a run that does not. Detect cycles and handle them as approved, list every shipment with incomplete lineage with the point where it stops and why, never as unaffected or zero, and place every input record. Keep sources read-only and report what the inputs cannot prove.

## Verified by

- Each recorded link appears once with its run, parent and child lots, quantities and units; two lots that share no run have no link, however close their dates, lot numbers or quantities, and a lot beside a recalled lot that shares no run is not listed as affected.
- Each descendant of a recalled lot appears once however many routes reach it, and its recalled quantity counts the material once; the recalled lot itself is reported separately, never as its own descendant.
- Recalled quantity follows the approved attribution rule through every split and blend, never exceeds a lot's produced quantity, and a shipment's recalled quantity follows from its shipped quantity under that rule.
- Each affected shipment appears once at the approved grain however many lots or routes reach it, with its date, customer, recalled quantity, any share the approved rule gives, and one status; a shipment whose figure is a lower bound is labelled so and never reported as fully quantified.
- Each run shows quantity in, quantity out, declared loss, signed residue and a verdict under the approved tolerance; a run outside it stays visible and its downstream quantities are marked provisional, or the run fails, as approved.
- Lots on a cycle of recorded links are detected and never traced through; where the approved rule sets them aside, each is listed once, tracing ends, and a shipment reached through one is listed as incomplete with a cycle reason and unknown recalled quantity, never unaffected and never zero.
- On a run that completes, a shipment whose lot has no observed origin, or whose history stops at a missing quantity, a unit the approved rules do not convert or a lot with no run, is listed with the point where it stops and one reason, with unknown recalled quantity, never unaffected and never zero.
- An unknown quantity stays unknown and a recorded zero stays zero; a recall naming a lot absent from the lot records follows the approved disposition and never returns an empty list as if nothing were affected.
- On a run that completes, every receipt, run, run leg, shipment and shipment line is placed once, as traced, set aside with its reason or listed as a problem, per input the counts sum to the records read, and records the approved scope leaves out are counted with their reason.
- Each output is unique on its declared grain, and changing a rule the approved requirements hold as data, such as the recalled lot, tolerance or unit factors, changes the published figures without a code change within the approved rule form.
- Published links, descendants, recalled quantities, shares and affected shipments equal values derived independently from the sources and approved rules, on cases that include a split, a blend, a lot reached by two routes, an unaffected sibling, a cycle, an unreconciled run and a lot with no origin.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile each input for lot keys, units, quantities, run references and orphan lots before modelling. Derive the expected results independently of the models, by hand from the approved rules and the input data, and include a case for each approved rule at its edge: a lot reached by two routes, a run that is both a split and a blend, a sibling lot beside the recalled one, a run reconciling only through declared loss, a cycle, a lot with no origin and a shipment line mixing a traceable and an untraceable lot. Keep each rule the requirements treat as data (the recalled lots, tolerance, units and factors, scope and reasons) as data that the models and tests read, never as a literal. On a target without recursive queries, expand the links level by level until no new lot appears. Before declaring the outcome complete, check that each shipment is counted once, that every input's records are placed once and that no unknown quantity was published as zero; report what the inputs cannot prove.

### Compose

- capturing-requirements
- applying-medallion-data-modelling
- generating-dbt-model
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which process, sites and lot identification scheme are in scope, which lot number is the key (the company's own or the supplier's), and which records link lots across sources: do the production run's own consumed and produced lines, or something else, define a link?
- If unresolved, how is a recall named and where does it come from (an editable list of lots, a supplier lot, a range), and what happens when it names a lot absent from the lot records: does the run fail or return an empty list that states why?
- If unresolved, how is recalled material attributed through a split or blend (by mass share, by volume, only what was recorded, direct blends only), is there a minimum share below which a shipment is not called affected, and are the recalled lot's own shipments listed as affected?
- If unresolved, which unit applies, what conversion factors and precision are approved, and what happens to a run, link or shipment line with a missing quantity or a unit with no factor: is it set aside as an exception, converted or does the run fail?
- If unresolved, which tolerance applies to a run's quantity in against quantity out plus declared loss, where does the declared loss come from, and is an unreconciled run traced with provisional quantities, held back or a failure?
- If unresolved, how is a cycle handled (set aside and flagged, or a failure), what counts as an observed origin (a receipt or a producing run), and how is a lot with two producing runs treated?
- If unresolved, which shipments are in scope (customer shipments, transfers between sites, samples, returns), what date or time basis applies against the recall, and is rework or a return that re-enters a lot linked, set aside or a problem?
- If unresolved, what grain is published for a shipment with several lots, what does a shipment that is partly traceable show, and is out-of-scope or problem material listed or only counted with its reason?

### Guardrails

- Do not choose the lot key, linking rule, attribution rule, tolerance, units, scope or cycle and bad-record handling for the user, and take none from the data or common practice; the user may ask for alternatives or a recommendation.
- Never infer a link from dates, adjacent lot numbers, equal quantities or the same supplier, and never trace through a link the records do not show.
- Never count a lot, a shipment or recalled material twice because several routes reach it, and never sum quantities across units the approved rules keep apart.
- Never read an unknown, missing or untraceable quantity as zero or a shipment with an unfollowed history as unaffected; keep it visible with its reason.
- Never trace through a lot on a cycle or publish a figure for it; a cycle follows the approved disposition and is never silently dropped.
- On a run that completes, never drop or double count a record: every record of every input stays accounted for, including set-aside and problem records.
- Do not hold a rule the approved requirements treat as data, such as the recalled lot or tolerance, as a literal in the models.
- Stop at the recall exposure: do not notify customers, trigger a recall, adjust stock or hold shipments, and keep sources read-only.
