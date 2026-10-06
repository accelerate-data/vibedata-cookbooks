---
id: master-b2b-account-hierarchy
title: Resolve B2B account hierarchies and roll measures to the ultimate parent
trigger:
  - Sales and finance cannot see total revenue or pipeline for a whole corporate family because subsidiaries sit as separate accounts.
  - The CRM's parent-account field has gaps, loops and conflicts with a firmographic vendor, and nobody knows which link to trust.
  - After an acquisition or divestiture, reports disagree on which family a past month's revenue belongs to.
  - Named-account or territory rules apply at the ultimate-parent level and need a flat account to parent to ultimate parent table.
description: Resolve every account to its parent and ultimate parent under approved, editable precedence, ownership and validity rules, roll measures up every level of each corporate family both as the families stood at the time and restated under the families on an approved as-of date, and list every unresolvable link with a reason, without counting anything twice.
pitch: See every corporate family's total, as it stood then and as it stands now, with every broken parent link explained.
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

Build <account_hierarchy_model> resolving every account in <account_source> to its parent and ultimate parent from <parent_link_sources> under approved, editable precedence, ownership and validity rules; <family_rollup_model> rolling <measures> up to every ancestor and ultimate parent per period, both as the families stood at the time and restated under the families in force on an approved as-of date, with each account's own value counted once; and <hierarchy_exceptions_model> listing every unresolvable link or unplaced measure with one row per reason. Inherit the Intent's sources, platform and approved requirements, and resolve only the semantics they leave open. Every account keeps an ultimate parent even when flagged, and per period and view the family totals reconcile to the total of all accounts' own measures. Hold source precedence, ownership thresholds, the depth cap, the as-of date and manual overrides as editable data. When <vendor_ultimate_parents> exist and a comparison is requested, build <vendor_comparison_model> explaining each disagreement without changing our hierarchy. Do not deduplicate accounts.

## Verified by

- Every account has exactly one ultimate parent per view and period, and each reported parent follows the approved source precedence, ownership rule and link validity dates.
- Each account's own measure is counted once at each of its ancestors, and per period and view the family totals at ultimate parents equal the total of all listed accounts' own measures.
- As-was families use the links in force at the approved point in each period; restated families use only the links in force on the approved as-of date, and restatement changes grouping, never a measure value.
- Links on each side of a validity boundary land in the approved periods, and an ownership share exactly at the threshold falls on the approved side.
- A source that offers no usable parent for some dates lets the next source in precedence supply one, and an approved no-parent override removes the parent for its dates even when another source names one.
- Cycles, missing parents, self-links, source conflicts, overlapping links, unmapped vendor ids and over-deep chains each appear as exceptions with their approved reasons, no flagged account loses its family, and walking the parent links never loops.
- A chain deeper than the approved cap keeps its true ultimate parent and is only flagged.
- Measures for accounts outside the account list are kept out of families, listed with a reason and accounted for in the reconciliation, and a missing measure follows the approved rule, never shown as zero.
- Family-total rows are marked separately for each view, so each view's family totals can be read without recomputing the hierarchy.
- Changing an editable rule such as precedence, a threshold, the depth cap, the as-of date or an override changes the affected outputs without a model change.
- The same inputs give the same hierarchy, roll-up and exceptions on every run, in any session time zone.
- When a vendor comparison is requested, each account shows agreement, a missing vendor value, or disagreement with every applicable approved reason, and our hierarchy is never changed to match the vendor.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements, and ask only about hierarchy and roll-up semantics they leave open; sample data, vendor conventions and existing code are evidence, never policy. Confirm what each source states about parents: which field, in which id space, with which ownership share and validity dates, and whether the source keeps history or overwrites links. Resolve each source's usable parent per validity interval first, then apply precedence once, so a source that offers nothing for some dates hands over to the next. Walk the resolved links once per evaluation date, the approved period points and the approved as-of date, and publish that one hierarchy for every downstream output, so the roll-up, the exceptions and any comparison can never disagree about a family. Drop only the links the approved rules drop, so the published parent never points at a link that was discarded. Roll measures up from the published hierarchy for both views, counting each account's own value once per ancestor. Reconcile every period and view to the total of all accounts' own measures, and account for measures that cannot be placed. Report what the link history cannot answer instead of filling it in.

### Compose

- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- verifying

### Ask first

- If unresolved, which sources state a parent, such as a CRM field, a firmographic vendor or a manual override list, how vendor ids map to accounts, which source wins when they disagree, and can an override declare that an account has no parent?
- If unresolved, what makes a link a parent: an ownership share above which threshold, on which side the boundary falls, whether it applies to every source, and how an account whose links all fall below it is shown?
- If unresolved, are parent links dated, are start and end dates inclusive, which links define a period's families for the as-was view, and which fixed as-of date defines today's families for the restated view?
- If unresolved, which measures roll up, whether each is a balance at period end or a flow within the period, in which currency and rounding, and what happens when an account has no measure for a period?
- If unresolved, how are cycles, self-links, missing parents, one source naming two parents for overlapping dates, unmapped vendor ids and chains deeper than a cap handled, and which only flag the account versus remove the link?
- If unresolved, when do sources count as conflicting: which sources take part, does a manual override, and must each named parent pass the ownership rule?
- If unresolved, is an exception one row per reason or per account, listed for every period it holds in the as-was view, and only once at the as-of date for the restated view?
- If unresolved and a vendor comparison is requested, at which date is it made, and which reasons explain a disagreement, such as another source winning, a vendor link below the threshold or an exception in the chain, listed every one that applies?

### Guardrails

- Do not invent ownership, precedence, restatement or exception policy. Values from another Intent, the sample data or the vendor are not defaults; ask for a missing rule without recommending one.
- Do not treat the vendor's parent or ultimate parent as ground truth; compare and explain, never adopt it into our hierarchy.
- Do not count an account's measure twice within a family, and do not show a missing measure as zero.
- Do not drop an account or silently re-parent it because its links cannot be resolved; keep it in a family and list the reason.
- Do not cut a chain at the depth cap or let a cycle loop forever; apply the approved rules and flag them.
- Do not rebuild past families from current links when the source lacks dated link history; state what the history cannot answer.
- Keep Domain sources read-only and use the Intent's actual platform; do not write parents back to the CRM or the vendor.
- Stop at the hierarchy, the roll-up, the exceptions and an optional vendor comparison. Do not deduplicate accounts, assign territories or apply partial-ownership consolidation.
