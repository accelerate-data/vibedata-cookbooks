---
id: fabric-direct-lake-semantic-model
title: Author a Direct Lake semantic model as code over governed gold tables
trigger:
  - The gold marts exist and the Power BI team is about to rebuild the star schema by hand in every report.
  - Report authors import copies of the gold tables into each report, so data lags and each report redefines the same KPI in its own DAX.
  - A Direct Lake model built straight on the gold tables shows blank members, missing dates or totals that disagree with the gold layer.
description: Author a Fabric Direct Lake semantic model as code over the governed gold tables, make the gold layer fit for it, define each approved KPI once as a measure, and prove its tables and relationships on the gold data and in the platform's model parser, with each measure's expected values computed independently over gold and checked against the deployed model where deploying it is approved.
pitch: Author one Direct Lake model as code over governed gold, every KPI defined once with independently computed expected values.
job_category: build
area: semantic-layer
readiness: supported
domain_objects:
  - semantic_model
  - governed_measure
  - dimension
  - date_table
  - gold_table
  - serving_table
  - acceptance_query
works_with:
  platforms:
    - fabric_lakehouse
    - fabric_warehouse
  tools:
    - dbt
qualifiers:
  - Not yet assessed end to end on fabric_lakehouse or fabric_warehouse.
  - Needs the gold layer in a Fabric lakehouse or warehouse that Direct Lake can read through OneLake.
  - Studio authors the model offline; deploying it and running its acceptance queries need a Fabric workspace.
  - A MetricFlow semantic model of the same metrics belongs to metricflow-semantic-model.
  - Reports and security roles are outside this Recipe.
related:
  - metric-population-and-rollups
evidence:
  features:
    - capturing-requirements
    - profiling-source-data
    - generating-dbt-model
    - dbt-unit-testing
    - running-dbt-in-sandbox
    - verifying
  evals: []
---

## Prompt

Author a Fabric Direct Lake semantic model over <gold_tables> with <measures>, so report authors in <workspace> read the governed gold data directly with each KPI defined once. Inherit the Intent's repository, platform, Domain, gold tables and approved requirements, and resolve only the semantics they leave open. Deliver the model as code: tables over the gold tables in Direct Lake mode, relationships from the declared keys, the approved date table, and the approved measures with their descriptions and formats; whatever the gold layer needs to be fit for the model, made as approved; and evidence that the model definition is valid for the target platform, that its tables and relationships hold on the gold data, and that each measure's expected values at the approved grains and slices are computed independently over gold at the approved precision, checked against the deployed model where deploying and refreshing it is approved and otherwise delivered as acceptance queries for its first deployment. State what the evidence cannot prove.

## Verified by

- The model definition loads in the platform's own semantic-model parser.
- Every table the approved design serves in Direct Lake is bound to a physical table, never a view, with columns mapped to source columns of compatible types, and the model's behaviour when Direct Lake cannot serve a query is set as the approved policy says.
- Every relationship has the approved cardinality and direction, each one side unique on the gold data, with the same type on both sides, and each role-playing dimension relates to the fact as the approved design exposes it.
- Every fact row resolves to a member of each related dimension, or, where its key does not resolve, is shown under an explicit member, excluded and counted, or fails the run with the offending rows identified, as the approved policy says; none is left silently on a blank member.
- The date table covers every fact date without gaps under the approved calendar and week start, and no table or measure filters to a reporting window unless the approved rules say so.
- Each measure's definition follows the approved population, ratio, missing-value, zero-denominator and period-to-date rules, and its expected values are computed independently over gold from those rules at every approved grain and slice, at the approved precision.
- Where deploying and refreshing the model in a workspace is approved, it deploys, frames successfully, serves its tables as the approved fallback policy says and returns the expected values at the approved precision at every approved grain and slice; otherwise each is reported as unproven.
- Published gold tables and their consumers are unchanged, or change only by the approved differences with each affected consumer identified, and any serving table is a physical table that reconciles to its source with only the approved differences.
- Every measure and visible column carries the approved name, description, format and any approved synonyms, and columns are hidden or visible as approved.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, gold tables and approved requirements, and resolve only the semantics they leave open. Profile the gold tables for what a Direct Lake model needs: key uniqueness on the one side of each relationship, fact keys that are null or do not resolve, the key types on both sides, date coverage of every fact date, attributes that exist only in views or would need calculated columns, and role-playing dimensions. Agree the measure definitions and member policies still open with the user. Make the gold layer fit where it is not, through approved changes to it or through physical serving tables reconciled to their sources. Then author the model as code with the skill that covers the format: tables over the physical gold tables, the relationships, the date table, the measures and their metadata, and load it in the platform's own model parser. Compute each measure's expected values independently over gold at the approved precision, and deliver acceptance queries that compare the model's results with them; run them against the deployed model where deploying and refreshing it is approved.

### Compose

- capturing-requirements
- profiling-source-data
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which measures are governed, over which gold tables, and which column, aggregation and population, such as billable, refunded, voided or unmapped records, does each one use?
- If unresolved, is each ratio a ratio of sums or an average of per-record ratios, what does a zero denominator or a missing value show, and to what precision must values match?
- If unresolved, which date places a fact in a period, which calendar and week start apply, which period-to-date measures are needed, and does any reporting window apply?
- If unresolved, which dimensions slice each measure, is a role-playing dimension exposed as separate tables or inactive relationships, and which version of a changing dimension applies?
- If unresolved, is a fact whose dimension key does not resolve shown under an explicit member, excluded and counted, or failed, and how is that member labelled?
- If unresolved, may the published gold tables change to fit the model, or must fixes go into separate physical serving tables?
- If unresolved, which Direct Lake source and workspace apply, may queries fall back to DirectQuery or must they fail, and are deployment and refresh in scope?
- If unresolved, which grains and slices form the acceptance evidence, and which names, descriptions, formats, synonyms and hidden columns do report authors need?

### Guardrails

- Do not choose or apply a measure definition, population, ratio, calendar or unresolved-member policy without approval; explain the alternatives if asked.
- Do not leave a fact on a blank dimension member, or drop it, because its key does not resolve, unless the approved policy excludes and counts it.
- Do not bind a Direct Lake table to a view or rely on calculated columns where Direct Lake needs physical columns; put derived attributes in the gold layer.
- Do not change published gold tables or their consumers to fit the model unless approved.
- Do not treat a checklist review or a green build as proof that the model loads.
- Do not claim the model's numbers are proven in the target engine until its acceptance queries have run against the deployed model.
- Do not widen the approved precision or tolerance to make values match.
- Do not extend into reports, security roles or a MetricFlow semantic model, or into deployment or refresh unless approved.
