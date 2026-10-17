---
id: master-product-sku-hierarchy
title: Conform product and SKU hierarchies across systems
trigger:
  - The same product carries different SKUs and category trees in the ERP, the web shop and the point of sale, so sales by category disagree between reports.
  - A new system or an acquisition brings another catalog and nobody can say which of its items are already known.
  - Category reporting needs one taxonomy with each product in exactly one place, and duplicate or reused SKUs and GTINs make product counts untrustworthy.
description: Bind every source item to at most one conformed product and SKU or list why not, map each source category into the approved conformed hierarchy with each product placed at most once per view or listed unplaced, and tie item counts and units to each source at every level with every difference explained or marked not tied.
pitch: One conformed catalog, every item bound or explained, every product rolled up once, and totals that tie back to each source.
job_category: build
area: transformation
readiness: supported
domain_objects:
  - source_item
  - product_binding
  - conformed_sku
  - conformed_product
  - category_mapping
  - conformed_hierarchy
  - product_placement
  - catalog_tieout
  - product_exception
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
  - Item records, category trees and any sale lines must already be landed as tables; this Recipe does not ingest catalogs.
  - An item no approved rule can bind stays unbound unless an approved cross-reference binds it.
  - Units tie out only for systems that supply sale lines.
  - Earlier taxonomy versions can be rebuilt only from dated mapping history; without it they cannot be restated.
related:
  - master-b2b-account-hierarchy
  - identity-golden-record-crosswalk
  - effective-dated-business-rules
  - file-drop-to-bronze
evidence:
  features:
    - capturing-requirements
    - generating-dbt-model
    - verifying
  evals: []
---

## Prompt

Build <item_binding_model> that ties every item in <source_item_sources> to exactly one conformed product and SKU under the approved identifier rules, or lists it as ambiguous, unmatched, out of scope or a problem with its reason and the candidates it saw, <conformed_catalog_models> for the conformed products and SKUs with each attribute taken from the approved owning system, <category_hierarchy_models> that map every source category into the approved conformed hierarchy and place each conformed product under at most one node per hierarchy view or list it unplaced, and <tieout_model> that ties item counts and, where <sale_line_sources> exist, units for each source system to the conformed totals at every node and level with every difference explained by an approved reason or marked not tied. Inherit the Intent's sources, platform and approved requirements, and resolve any product semantics they leave open. Every record is accounted for once, bound and placed or set aside with its reason, and nothing is merged, repaired or invented to make a total tie.

## Verified by

- In a published result, each source item record is bound to one conformed product and SKU or listed ambiguous, unmatched, out of scope or a problem, with its rule or reason and any candidates, none missing or twice; a failed or held run names the items and reasons that stopped it.
- Binding follows the approved identifier rules and any approved cross-reference in their approved order, and no binding rests on evidence those rules do not accept.
- Identifiers claimed by several SKUs, listed twice, or disagreeing between items bound together are bound only as the approved conflict rule says, never merged on their own, and stay listed with the reason.
- In a published result, units convert only as the approved rule says, recorded units stay visible beside base units, units sum only within one approved unit of measure, and a line that cannot convert is listed and never summed or assumed to be one.
- Each conformed attribute comes from the approved owning system by the approved precedence with the supplier published beside it, a different value elsewhere is handled as approved and stays visible, never silently combined, and an item that is not bound supplies no value and is not counted as bound.
- In a published result, every source category at every approved level maps to a node in each approved view or is listed unmapped, each product sits under at most one node per view by the approved basis or is listed unplaced, and another system's different node is shown without moving it.
- In a published result, category cycles, orphans, chains past an approved depth and nodes no category maps into are listed with their reasons, never loop the build, and never leave an item under a node the rules cannot reach.
- In a published tie-out, each source, view, node and level shows source and conformed item counts and, where sale lines exist, units, with the signed difference, each explained part carries an approved named reason, and a row with any unexplained part reads as not tied, never as tied.
- In a published result, per source the items and (where sale lines exist) units at its nodes plus those set aside under each named reason add back to its own total per approved unit, and per view a node's total equals its own plus its children's, so nothing counts twice and ancestors are not summed.
- Where sale lines exist, returns follow the approved rule and are never clamped or dropped silently, a duplicate sale counts once only as the approved rule says, out-of-window sales are listed with the reason, and absent sales read as unknown units unless the approved rules define zero.
- Published bindings, placements and tie-out figures equal values derived independently from the sources and the approved rules, not from the models' own outputs.
- Conformed identifiers are identical on every run for the same inputs, and a change to an approved rule held as data changes the results without a code change within the approved rule form.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements. Ask only about product semantics they leave open; sample data, vendor defaults and existing code are evidence, never policy. Profile each source first: which identifiers exist and in which forms, whether check digits validate, which item types appear, whether ids repeat across or within systems, how deep each category tree runs, and which systems report sales. Name any output the available inputs cannot support. The binding, the conformed catalog, the placement and the tie-out share one resolved identity, so they never disagree about an item. The approved rules, not model behaviour, decide ambiguity, ownership, fallback placement, unmapped categories, depth caps and what a difference is called. Derive each case's expected result independently of the models, from the inputs and the rule tables, before comparing.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which identifiers may bind an item (which GTIN forms are one key, brand with part number, vendor code, system SKU), in what order, where a maintained cross-reference ranks, whether a title may ever bind, and what an invalid identifier does?
- If unresolved, what unit and precision is each item and sale line recorded in, what is a SKU versus a variant, pack or bundle, whether and how units convert, may different units be summed at a node, and what does a line that cannot convert do?
- If unresolved, how are an identifier claimed by several SKUs, an item id listed twice, a reused key, a superseded item, a bad cross-reference and items bound together with disagreeing identifiers handled: ambiguous, fail, bound to a successor, or kept under a precedence?
- If unresolved, how are conformed products and SKUs established (an authored list or derived from matches) and kept stable across reruns, which system owns each attribute by what precedence, and what does a missing or differing value do?
- If unresolved, is the hierarchy authored or adopted, which views, how do categories map in (leaf only, split by attribute), which category counts for an item or category with several parents, and where do disagreeing, unmapped, orphan, cyclic or too-deep cases go?
- If unresolved, what is one source item record (per system, company, store, storefront or locale), which items are in scope (item types, discontinued), and what stays visible as out of scope?
- If unresolved and units are wanted, which systems report sales, what is a sale, over what window, cutoff time, time zone and as-of date, does an item with no sale lines mean nil or unknown, how do returns net, and when are two lines one sale?
- If unresolved, which named reasons may explain a tie-out difference, which wins when several fit and may one explain only part, do unbound items, a sale line naming an unknown item or an unexplained difference publish and flag, fail or hold, and is history restated when rules or taxonomy change?

### Guardrails

- Do not invent product policy. Identifier order, variant and pack meaning, ownership, mappings, fallbacks, windows and the handling of conflicts come from approved requirements or the user; values from another Intent, the sample data or a vendor are not defaults.
- Do not merge items on a name, a similarity score or a precedence the approved rules do not state; an item the rules cannot decide stays unbound and listed.
- Do not invent hierarchy data. An unmapped, orphan or cyclic category and a product the rules cannot place stay listed with their reasons and get no node, no default category and no catch-all bucket unless an approved fallback says so.
- Do not let an unbound item supply attribute values to a conformed product or SKU or count as bound to it.
- Do not double count or default measures: a product counts at most once per view, a node's total includes each descendant once, a missing unit is unknown unless the approved rules define absence as zero, and a return is never clamped silently.
- Do not sum quantities recorded in different units, or assume a conversion the approved rules do not state; a line that cannot convert stays listed.
- Do not absorb a tie-out difference: it is either explained by an approved named reason or the row is not tied.
- Stop at conformed identity, hierarchy, placement and the tie-out. Do not ingest catalogs, match customers or accounts, explode bills of materials, trace lots, price, cost or value stock, tie sales amounts or currencies, or write conformed ids back to source systems.
