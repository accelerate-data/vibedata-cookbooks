---
id: trace-governed-metric-to-sql-and-sources
title: Trace a governed metric to the SQL and source tables behind it
trigger:
  - A number is reported under a business metric name and nobody can say how it is computed or which tables it comes from.
  - Two reports carry the same metric name with different figures, and neither owner can show the SQL or sources behind theirs.
  - A reviewer or auditor asks which source tables sit behind a governed metric before relying on it.
  - A data team inherits a governed metric and needs to see what the semantic layer really runs, in the Domain and in the workspace being built.
description: Show, for one governed metric named by its business name, the SQL the semantic layer compiles it to and the lineage from that SQL back to the source tables, from the Domain and from the Intent's workspace, with the chosen source, the rejected sources and every gap named; read-only.
pitch: Name a governed metric and see the SQL it compiles to and the source tables behind it, with every gap in the trace named.
job_category: explain
area: semantic-layer
readiness: supported
function:
  - cross-functional
domain_objects:
  - governed_metric
  - semantic_model
  - compiled_sql
  - data_lineage
  - source_table
works_with:
  platforms:
    - duckdb_local
    - motherduck
    - redshift
    - databricks
  tools:
    - dbt
qualifiers:
  - Assessed end to end on duckdb_local only; the other listed targets are unassessed.
  - Needs the Domain's semantic model to exist and validate; this Recipe does not author, audit or fix one.
  - Explains one metric; reconciling two sources that disagree is the reconciliation Recipes' work.
related:
  - metricflow-semantic-model
evidence:
  features:
    - querying-semantic-model
    - running-dbt-in-sandbox
  evals: []
---

## Prompt

Show how <metric> is built: the SQL the semantic layer compiles it to for <grouping>, and the lineage from that SQL back to the source tables, from the Domain and from the Intent's workspace, as approved. Inherit the Intent's repository, platform, Domain, semantic model and approved requirements, and resolve only the semantics they leave open. Deliver, for each approved target, the compiled SQL with the source the semantic layer chose, the sources it rejected with their reasons and the model revision; the lineage from each relation the SQL reads back to the source tables, ending where the evidence ends, with every gap named; and, where both targets are approved, what differs between them. Change no model, semantic document, test or Domain relation and publish nothing; the only writes are approved builds of existing definitions in the workspace, each named.

## Verified by

- The SQL shown is the SQL the semantic layer returns for the approved metric and grouping on each approved target, never hand-written; the chosen source, the rejected sources with their reasons, the model revision and any uncommitted model change are stated.
- Every definition carrying the metric's business name is listed and the traced one named; the metric is stated as its definition says, including any filter or population rule it carries or lacks; a filter added at query time is reported as a constraint on it, not part of it.
- Every relation the compiled SQL reads is traced upstream to source tables with each hop named, and the trace says where it stops and why, such as an external landing relation, an unlinked loader or an unreadable artifact; no gap is filled by guess.
- A relation the SQL reads that is not a source table, such as a time spine or dimension, is shown as what it is.
- A relation the reader may not access or disclose is shown as restricted, never skipped, guessed or exposed.
- Where the query was run, each total equals an independent computation of the metric as its definition says, from the relations the lineage names for each of its inputs, within floating-point rounding; a metric type the layer cannot compile or run is reported with its refusal.
- Any refusal or failed run is quoted with its error and the metric is reported as not run there; no figure is presented as the semantic layer's answer when the layer did not produce it.
- A relation outside the semantic layer is stated as not governed, never presented as an answer from it.
- A relation that fails to build is reported with its error and the cause is classed as a stale built upstream, a defect in its definition or a missing capability, never blamed on the definition without checking its upstream first.
- Where both targets are approved they are compared: identical SQL, source and revision, or each difference named, and a relation present in one and absent from the other is a finding; with one target, the report says the other was not traced.
- No model, semantic document, test or Domain relation is changed to make the trace work; each relation built in the workspace to run the query is approved, named and an existing definition.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, semantic model and approved requirements, and resolve only the semantics they leave open. Resolve the business name to the model's metric and agree the grouping. Ask the semantic layer for the SQL on each approved target and report the chosen source, the rejected sources with their reasons and the revision. Run it only where the relations exist, and compare any result with an independent computation from the fact relation the lineage names. When a target lacks relations, quote the refusal and take the approved route. Trace each relation the SQL reads upstream with the lineage tool and name the point and reason where it ends. Compare the two targets and report every difference, a failed build included, with its classified cause. Report anything that would need changing as work outside this Recipe.

### Compose

- querying-semantic-model
- running-dbt-in-sandbox

### Ask first

- If unresolved, which metric, named by its business name, and over which grouping and filter, is to be traced, and which definition when the name resolves to more than one?
- If unresolved, which targets are traced, the production Domain, the workspace or both?
- If unresolved, when a target lacks relations the SQL reads, is the metric run on a target that has them, is the SQL shown without running it, or are the existing models built in the workspace first?
- If unresolved, when the semantic layer can serve the metric from more than one source, does the trace follow the source it chooses or a named one?
- If unresolved, how far must the lineage go, to the first external relation, to the loader that fills it or to the originating system, which relations count as source tables rather than spine or dimensions, and which tables or columns may be named or read, a restricted one shown as restricted?
- If unresolved, which model revision is traced, a committed branch or the working tree with its uncommitted changes?

### Guardrails

- Do not write SQL around the semantic layer to produce a governed metric's number or to show its SQL, and do not present a hand-computed figure as the semantic layer's answer.
- Do not edit a model, semantic document, test or warehouse relation to make the trace work; build in the workspace only existing definitions, and only as approved.
- Do not fill a lineage gap by guess; name where the trace stops and why.
- Do not describe a relation outside the semantic layer as governed, or a refusal as an answer.
- Do not extend into authoring, auditing or fixing the semantic model, defining a new metric, reconciling sources that disagree, or publishing lineage to a catalog.
