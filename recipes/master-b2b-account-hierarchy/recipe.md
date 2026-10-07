---
id: master-b2b-account-hierarchy
title: Resolve B2B account hierarchies and roll measures to the ultimate parent
trigger:
  - Sales and finance cannot see total revenue or pipeline for a whole corporate family because subsidiaries sit as separate accounts.
  - The CRM's parent-account field has gaps, loops and conflicts with a firmographic vendor, and nobody knows which link to trust.
  - After an acquisition or divestiture, reports disagree on which family a past month's revenue belongs to.
  - Named-account or territory rules apply at the ultimate-parent level and need each account mapped to its parent and ultimate parent.
description: Resolve accounts to their parent and ultimate parent under approved precedence, ownership and validity rules, keep accounts the rules cannot place explicitly unresolved, roll measures up every level of each corporate family in each approved view, as it stood at the time where history allows or restated on an approved as-of date, and list every exception with its reason, never double counting.
pitch: See every corporate family's total, as it stood then or as restated, with every broken parent link explained.
job_category: build
area: transformation
readiness: supported
domain_objects:
  - account
  - parent_link
  - account_hierarchy
  - ultimate_parent
  - family_rollup
  - hierarchy_exception
works_with:
  platforms:
    - duckdb_local
  tools:
    - dbt
qualifiers:
  - Complete outcome assessed for duckdb_local only; the other four Studio targets remain unassessed.
  - The as-was view needs dated parent-link history in the source; without it, past families cannot be rebuilt.
  - Accounts must already be one record per company; this Recipe does not deduplicate accounts.
related:
  - metric-population-and-rollups
  - effective-dated-business-rules
  - dbt-snapshot-history
  - identity-golden-record-crosswalk
evidence:
  features:
    - applying-medallion-data-modelling
    - generating-dbt-model
    - dbt-unit-testing
    - verifying
  evals: []
---

## Prompt

Build <account_hierarchy_model> resolving accounts in <account_source> to their parent and ultimate parent from <parent_link_sources> under approved precedence, ownership and validity rules; <family_rollup_model> rolling <measures> up to every ancestor per period for each approved view, as families stood at the time where dated link history allows or restated under those in force on an approved as-of date, counting each account's value once per ancestor; and <hierarchy_exceptions_model> listing every exception, unresolved account and unplaced measure with its reason. Inherit the Intent's sources, platform and approved requirements; resolve only the semantics they leave open. Every account is accounted for: a resolved account has exactly one ultimate parent; an unresolved one stays explicitly unresolved unless an approved fallback places it. Per period and view, family totals plus unresolved accounts' and unplaced measures reconcile to the source total. Approved rule values can change without changing model logic. When <vendor_ultimate_parents> exist and a comparison is requested, build <vendor_comparison_model> explaining each disagreement, never changing our hierarchy.

## Verified by

- Every account is accounted for in each view and period: a resolved account has exactly one ultimate parent under the approved precedence, ownership and validity rules, one placed by an approved fallback is marked as such, and any other is marked unresolved with its reason.
- A resolved account's own measure counts exactly once in each of its ancestors' totals, an unresolved one's rolls up only as the approved rule says, and per period and view the family totals at ultimate parents, plus unresolved accounts' and unplaced measures, equal the source total.
- As-was families use the links the approved as-was rule assigns to each period, and only where dated link history exists; restated families use only the links in force on the approved as-of date, and restatement changes grouping, never a measure value.
- Links on each side of a validity boundary land in the approved periods, and an ownership share exactly at the threshold falls on the approved side.
- Where a source offers no usable parent for some dates, the parent for those dates follows the approved precedence and hand-over rule, and an approved no-parent override, if the rules allow one, applies at its approved rank and dates.
- Cycles, missing parents, self-links, source conflicts, overlapping links, unmapped vendor ids and over-deep chains are each handled as the approved rules say and listed with their approved reasons; an affected account is placed only by an approved rule or fallback, and walking links never loops.
- A chain deeper than the approved cap is handled exactly as the approved depth policy says, whether that only flags it, cuts or invalidates a link, or leaves the account unresolved, and the chain is always listed as an exception.
- A measure for an account outside the account list is handled as the approved rule says, never silently dropped, and is accounted for in the reconciliation; a missing measure follows the approved measure semantics, never defaulted to zero unless they define absence as zero.
- Each approved view's family totals can be read straight from the roll-up without recomputing the hierarchy, and a reader cannot mistake an intermediate ancestor total for a family total or mix totals from different views.
- Changing an approved rule value, such as a precedence order, a threshold or an override, changes the affected outputs without changing model logic.
- The same inputs give the same hierarchy, roll-up and exceptions on every run, in any session time zone.
- When a vendor comparison is requested, each account shows agreement, a missing vendor value, an unresolved account on our side, or a disagreement with its approved reasons or marked unexplained; our hierarchy is never changed to match the vendor.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements, and ask only about hierarchy and roll-up semantics they leave open; sample data, vendor conventions and existing code are evidence, never policy. Confirm what each source states about parents: which field, in which id space, with which ownership share and validity dates, and whether the source keeps history or overwrites links. Decide each source's usable parent per validity interval under the approved ownership and validity rules, then apply the approved precedence once, including where a source offers nothing for some dates. Walk the resolved links once for each date the approved views evaluate, and publish that one hierarchy for every downstream output, so the roll-up, the exceptions and any comparison never disagree about a family. Invalidate only the links the approved rules invalidate, so no published parent comes from an invalidated link. Mark an account unresolved when the approved rules leave it without a defensible ultimate parent, place it only by an approved fallback, such as making it its own root, and mark any fallback placement as such. Roll measures up from the published hierarchy for each approved view, counting each account's own value once per ancestor. Reconcile every period and view: family totals plus unresolved accounts' measures plus unplaced measures equal the source total. Report what the link history cannot answer instead of filling it in.

### Compose

- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- verifying

### Ask first

- If unresolved, which sources state a parent (a CRM field, a firmographic vendor, a manual override list), how vendor ids map to accounts, which source wins when they disagree, does a source with no usable parent for some dates hand over to the next, and can an override declare no parent?
- If unresolved, what makes a link a parent: which ownership share, does a share exactly at the threshold qualify, does the rule apply to every source, and how is an account whose links all fall short shown?
- If unresolved, are parent links dated, are their start and end dates inclusive, which reporting periods apply (calendar or fiscal, what grain), are the as-was view, the restated view or both needed, which links define a period's family as-was, and which as-of date defines the restated families?
- If unresolved, which measures roll up, is each a balance at period end or a flow within the period, in which currency and rounding, what happens when an account has no measure for a period, and how is a measure for an account not in the account list handled?
- If unresolved, is there a depth cap, at what depth, and how are cycles, self-links, missing parents, two parents from one source for overlapping dates, unmapped vendor ids and over-deep chains handled: flag only (keeping which parent), cut or invalidate a link, treat as a root, or leave unresolved?
- If unresolved, when do sources count as conflicting: which sources take part, does a manual override take part, and must each named parent pass the ownership rule?
- If unresolved, is an account left without a defensible ultimate parent placed by a fallback, such as becoming its own root, or left unresolved, where do accounts below it roll up, and is an exception listed per reason or per account, per period or once at the as-of date?
- If unresolved and a vendor comparison is requested, which level and date are compared, which reasons can explain a disagreement (another source winning, a vendor link below the threshold, an exception in the chain), and does a disagreement list every applicable reason or one?

### Guardrails

- Do not invent ownership, precedence, fallback, restatement, measure or exception policy. Values from another Intent, the sample data or the vendor are not defaults; ask for a missing rule without recommending one.
- Do not treat the vendor's parent or ultimate parent as ground truth. A vendor link enters our hierarchy only where the approved precedence includes it, and a comparison never changes our hierarchy to match the vendor.
- Do not count an account's measure twice in any ancestor's total, such as through two paths to one ancestor, and never default a missing measure to zero unless the approved measure semantics explicitly define absence as zero.
- Do not drop an account or invent an ultimate parent for it because its links cannot be resolved; keep it explicitly unresolved with its reason, and place it only under an approved fallback rule.
- Handle an over-deep chain or a cycle only as the approved rules say, whether that flags it, cuts or invalidates a link, treats an account as a root or leaves accounts unresolved, and never let walking the links loop forever.
- Do not rebuild past families from current links when the source lacks dated link history; state what the history cannot answer.
- Do not let the hierarchy, roll-up, exceptions and any vendor comparison disagree about a family; derive them all from one published hierarchy.
- Keep Domain sources read-only and use the Intent's actual platform; do not write parents back to the CRM or the vendor.
- Stop at the hierarchy, the roll-up, the exceptions and an optional vendor comparison. Do not deduplicate accounts, assign territories or apply partial-ownership consolidation.
