---
id: master-b2b-account-hierarchy
title: Resolve B2B account hierarchies and roll measures to the ultimate parent
trigger:
  - Sales and finance cannot see total revenue or pipeline for a whole corporate family because subsidiaries sit as separate accounts.
  - The CRM's parent-account field has gaps, loops and conflicts with a firmographic vendor, and nobody knows which link to trust.
  - After an acquisition or divestiture, reports disagree on which family a past month's revenue belongs to.
  - Named-account or territory rules apply at the ultimate-parent level and need each account mapped to its parent and ultimate parent.
description: Resolve accounts to their parent and ultimate parent under approved precedence and parent rules, keep accounts the rules cannot place explicitly unresolved unless an approved fallback places them, roll measures up every level of each corporate family for the approved periods, and list every hierarchy anomaly with its reason, never double counting an account or inventing hierarchy.
pitch: See every corporate family's total, with every account placed or explicitly unresolved and every broken parent link explained.
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
  - Families as they stood in past periods need dated parent-link history; without it they cannot be rebuilt.
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

Build <account_hierarchy_model> that resolves each account in <account_source> to its parent and ultimate parent from <parent_link_sources> under the approved precedence and parent rules, <family_rollup_model> that rolls <measures> up every level of each corporate family per approved period, and <hierarchy_exceptions_model> for every hierarchy anomaly, unresolved account and unplaced measure. Inherit the Intent's sources, platform and approved requirements, and resolve any hierarchy semantics they leave open. Every account is accounted for: a resolved account has exactly one ultimate parent, and an unresolved one stays explicit unless an approved fallback places it. If an external hierarchy exists and a comparison is wanted, add <comparison_model> explaining each difference without changing ours.

## Verified by

- Each resolved account's parent and ultimate parent follow the approved sources, precedence and parent rules, including where a higher-precedence source offers no usable parent, where an override applies and where a link sits exactly at an approved threshold.
- Every account is accounted for in each period: resolved with exactly one ultimate parent, placed by an approved fallback and marked as such, or explicitly unresolved with its reason. No account is dropped or given an invented parent.
- Hierarchy anomalies such as cycles, missing parents, conflicting or overlapping links and chains past an approved depth cap are handled exactly as the approved rules say, stay visible as exceptions with their reasons, and never make the hierarchy loop.
- Links that start or end on either side of a period boundary place an account in the family the approved rule selects for that period, and where a restated view is approved, its families use only the links in force on the as-of date.
- Past families are rebuilt only from dated link history; where history is missing the output says so instead of projecting current links backward. Restatement changes grouping, never a measure value.
- Each account's own measure counts exactly once in every ancestor's total, never twice through two paths, and measures below an unresolved account roll up only as the approved rule says.
- Per period, each ancestor's total equals its own measure plus its descendants'. Ancestor totals are nested, so only one total per family is summed: the ultimate parents' totals, plus each unresolved account's own measure and unplaced measures, equal the source total at the approved rounding.
- Measures for accounts outside the account list follow the approved rule and are never silently dropped, and the outputs never default a missing measure to zero unless the approved measure semantics explicitly define it as zero.
- Results are identical on every run and under any session time zone.
- If a comparison is in scope, every account shows agreement, a missing external value, an unresolved account on our side, or a difference with an approved explanation or marked unexplained. Our hierarchy is never changed to match the external one.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements. Ask only about hierarchy semantics they leave open; sample data, vendor settings and existing code are evidence, never policy. Profile each parent source: which field names the parent, in which id space, whether links carry ownership shares and validity dates, and whether the source keeps link history or overwrites it, and name any output the available history cannot support. The roll-up, the exceptions and any comparison share one resolved hierarchy, so they never disagree about a family. The approved rules, not model behaviour, decide a source with no usable parent, a link exactly at a threshold, a link starting or ending at a period boundary, cycles, conflicting or overlapping links, chains past a depth cap, and where an unresolved account and the accounts below it belong.

### Compose

- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- verifying

### Ask first

- If unresolved, which sources state a parent (a CRM field, an external registry or vendor, a manual override list), how their ids map to accounts, which source wins when they disagree, and what happens for dates where a higher-precedence source has no usable parent?
- If unresolved, what makes a link a parent, such as an ownership share over a threshold, does a value exactly at the threshold qualify, and do manual overrides follow the same rule?
- If unresolved, are parent links dated and are their start and end dates inclusive, which reporting periods apply, and should a period show the families of its own time, families restated to an as-of date, or both, and which as-of date?
- If unresolved, which measures roll up, is each a balance at period end or a flow within the period, in which currency and rounding, and how are a missing measure and a measure for an account outside the account list handled?
- If unresolved, is there a depth cap, and how are cycles, self-links, missing parents, conflicting or overlapping links and over-deep chains handled: flag and keep the parent, drop the link, or leave the account unresolved?
- If unresolved, does an approved fallback place an account the rules leave without a defensible ultimate parent, where do the accounts below it roll up, and is an exception listed per reason or per account?
- If unresolved and a comparison with an external hierarchy is wanted, at which level and date are the two compared, and which explanations may account for a difference?

### Guardrails

- Do not invent hierarchy policy. Sources, precedence, parent rules, fallbacks, restatement, measure semantics and anomaly handling come from approved requirements or the user; values from another Intent, the sample data or a vendor are not defaults. Do not choose or apply a rule without approval.
- Do not invent hierarchy data. An account the approved rules cannot place stays explicitly unresolved with its reason; never give it a parent, a root or a family unless an approved fallback does.
- Do not fabricate history. Without dated link history past families cannot be rebuilt; say so and never project current links backward.
- Do not treat an external hierarchy as ground truth. Use its links only where the approved precedence includes them, and never change our results to match it.
- Do not double count or default measures. An account's measure counts once in each ancestor's total; never default a missing measure to zero unless the approved measure semantics explicitly define it as zero.
- Do not let outputs disagree about a family. The roll-up, the exceptions and any comparison use the same resolved hierarchy.
- Stop at the hierarchy, the roll-up, the exceptions and the optional comparison. Do not deduplicate accounts, assign territories, apply partial-ownership consolidation or write parents back to source systems.
