---
id: identity-golden-record-crosswalk
title: Deduplicate customers into a golden record with a source crosswalk
trigger:
  - The same customer exists in several systems under different ids, so customer counts and per-customer revenue are inflated.
  - Analysts need to trace a golden customer to every source record behind it, and any source record to its golden customer.
  - Source systems disagree on a customer's name, address or contact details and nobody can say which value wins or why.
  - Customer ids change from one run to the next when a later record turns out to belong to an existing customer.
description: Resolve customer records from several source systems into one golden record per customer, with a two-way crosswalk, approved match and survivorship rules held as data, golden ids that stay stable across runs, an unresolved list that accounts for every source record, and an optional comparison with a source system's own merge pointers.
pitch: One customer, one stable id, every source record traced to it and every unresolved one explained.
job_category: build
area: transformation
readiness: supported
domain_objects:
  - customer
  - golden_record
  - source_record
  - crosswalk
  - match_rule
  - survivorship_rule
  - golden_id_register
  - unresolved_record
works_with:
  platforms:
    - duckdb_local
  tools:
    - dbt
qualifiers:
  - Complete outcome assessed for duckdb_local only; the other four Studio targets remain unassessed.
  - Expects names and addresses already standardized, with a match key, by an earlier standardization step.
  - Stable golden ids need the id register to persist between runs; a rebuild from scratch reissues them.
  - Without retained crosswalk history, the crosswalk as it stood on a past run cannot be reconstructed.
related:
  - business-event-fact
  - dbt-snapshot-history
evidence:
  features:
    - profiling-source-data
    - identifying-data-slice
    - domain-modeling
    - applying-medallion-data-modelling
    - authoring-dbt-project-artifact
    - dbt-unit-testing
    - verifying
  evals: []
---

## Prompt

Build <golden_customer_model> with one row per resolved customer from <customer_sources>, <crosswalk_model> linking every source record to its golden customer and back, and <unresolved_model> listing every source record that cannot be resolved cleanly with its reason. Inherit the Intent's sources, platform and approved requirements, and resolve only the identity semantics they leave open: which records and signals can link two records, normalization, never-link values, removed records, manual merge and split overrides, group limits, which value survives for each attribute, how golden ids stay stable across merges and splits, repeated deliveries, and the unresolved reasons. Match lists, rankings and limits can change without changing model logic. Every source record lands in the crosswalk or the unresolved list as the approved rules say, never lost and never counted twice, and golden ids never change except as the approved merge and split rules allow. If a source carries its own merge pointer and a comparison is wanted, add <source_merge_comparison_model> that reports each agreement and disagreement.

## Verified by

- Every source record, identified by source system and source record id, is in the crosswalk once, on the unresolved list, or both, exactly as the approved removing and flagging reasons say. No record is lost, duplicated or assigned to two golden customers.
- Records linked by an approved signal resolve to one golden customer, and chains of links behave as the approved rule says; records with no approved link stay separate. Formatting variants match or not exactly as the approved normalization says.
- A never-link value never joins two customers, and the record still links on its other signals. A removed record, such as a test account or a deleted one, never bridges two customers.
- A linked group larger than the approved limit is not merged, and its records are listed with a reason; a group exactly at the limit merges as the approved rule says.
- Manual merges and splits are applied as approved: a split pair never shares a golden customer, and a merge or split that conflicts with another rule is listed with a reason, never applied silently.
- Each golden attribute carries the value the approved survivorship rule selects, including ties and missing values, and names the source record that supplied it. Values the approved rules exclude never become golden values.
- Rerunning with no new data reproduces every golden id. When a later record links existing customers, the id the approved rule selects survives and each retired id still resolves to it; a split keeps the id on the side the approved rule names.
- A golden id changes only through an approved merge or split. When a customer's records change in any other way, including losing the record its id was first issued for, its id follows the approved rule rather than being reissued by default.
- Repeated deliveries of one source record are resolved by the approved rule; each extra copy is listed, and differing copies the rule cannot rank never pick an arbitrary winner.
- A record with nothing to match on is handled as approved and is never dropped; the golden record count equals the distinct golden ids in the crosswalk.
- Results are identical under any session time zone, and changing an approved list, ranking or limit changes the results without changing model logic.
- If the source merge comparison is in scope, every pointer appears once as an agreement or a disagreement with a reason, and the golden grouping is never changed to match it.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements. Ask only about identity semantics they leave open; sample values, a source's own merge pointers and existing code are evidence, never policy. Profile each source's record identity, repeated deliveries, statuses, contact formats, standardized fields and match keys, and name any rule the available data cannot support. If names and addresses are not yet standardized, standardize them first rather than inside this work. Hold match signals and their order, normalization, never-link values, test accounts, status meanings, overrides, group limits, survivorship rankings and validity patterns as data. Decide removal, validity and repeated deliveries once per source record, resolve groups under the approved linking and override rules, then issue golden ids from a register that persists between runs and resolves retired ids to their survivors. Derive the golden record, crosswalk and unresolved list from that one resolution, so they cannot disagree about a record. The approved rules, not model behaviour, decide chains, group limits, override conflicts, ties, missing values, repeated copies and which id survives a merge or split. Add the source merge comparison only when a source carries merge pointers and the user wants it.

### Compose

- profiling-source-data
- identifying-data-slice
- domain-modeling
- applying-medallion-data-modelling
- authoring-dbt-project-artifact
- dbt-unit-testing
- verifying

### Ask first

- If unresolved, which source systems and which customers (people, organisations or both) are in scope, which field identifies a record in each source, can a source hold duplicates of itself, and are names and addresses already standardized with a match key?
- If unresolved, which signals link two records, after what normalization, in what order, by exact match only or by similarity too, is linking transitive across signals, and is there a largest group that may merge?
- If unresolved, which values must never link records (shared or role addresses, placeholder numbers), how are test accounts identified, which statuses mean deleted or inactive, and what makes an email or phone invalid?
- If unresolved, is there a manual force-merge or force-split list, and what happens when an override conflicts with a never-link value, another override or a chain that keeps the split pair connected?
- If unresolved, which value wins for each golden attribute (source ranking, most recent, most complete), how are ties broken, are excluded or invalid values eligible, and are values published as typed or normalized?
- If unresolved, how are golden ids issued, which id survives a merge, which side keeps it on a split, what happens to a retired id, and what happens when the record an id was first issued for leaves its customer?
- If unresolved, how is a source record delivered more than once resolved, including copies that differ but share the latest time, and how is a record with nothing to match on handled?
- If unresolved, what are the unresolved reasons, does each remove the record from the crosswalk or only flag it, is the list one row per record and reason, and must any past crosswalk state be reconstructable?

### Guardrails

- Do not invent matching or survivorship policy. Signals, normalization, rankings, limits and overrides come from approved requirements or the user; values from another Intent are not defaults. Ask for a missing rule without recommending one.
- Do not merge records on approximate similarity, or on a value the user has said must never link records, unless an approved rule allows it.
- Do not let a removed, deleted or test record join two customers, or contribute a golden value, unless an approved rule allows it.
- Do not silently drop, default or double-count a source record. Every record is in the crosswalk or on the unresolved list with a reason, and conflicts stay visible instead of being resolved arbitrarily.
- Do not derive or recompute golden ids from the current group contents. Ids are issued once and persist; a later merge must not renumber existing customers.
- Do not treat a source system's own merge pointers as ground truth. Report agreement and disagreement; never change the grouping to match them.
- Do not let the golden record, crosswalk and unresolved list disagree about a record; derive all three from one resolution.
- Keep source systems and Domain sources read-only; resolve identity in the warehouse and never write back to a source.
- Stop at the golden record, crosswalk, unresolved list and optional source merge comparison. Do not build account hierarchies, consent merging, address standardization or a steward review tool here.
