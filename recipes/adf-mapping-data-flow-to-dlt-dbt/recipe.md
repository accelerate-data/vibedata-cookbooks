---
id: adf-mapping-data-flow-to-dlt-dbt
title: Convert an ADF mapping data flow into dlt and dbt and prove parity
trigger:
  - Order or customer reporting still comes from an Azure Data Factory mapping data flow whose logic lives only on the ADF canvas, with no tests or review.
  - The team is leaving Azure Data Factory and needs the data flow's source reads, joins, derived columns, aggregates and splits as dlt and dbt code.
  - Someone has to show the rebuilt output matches what the data flow writes to each sink before the data flow is switched off.
description: Convert one exported ADF mapping data flow into a dlt pipeline for its external source reads and dbt models for its transformation graph, with a verdict for every step and each sink proven against the flow's approved reference output on an agreed slice.
pitch: Rebuild an ADF mapping data flow as dlt and dbt code and prove sink by sink that it returns what the flow wrote.
job_category: re-engineer
area: transformation
readiness: supported
domain_objects:
  - adf_data_flow
  - dlt_pipeline
  - dbt_model
  - sink
  - consumer_contract
  - reference_output
  - conversion_report
  - parity_report
works_with:
  platforms:
    - duckdb_local
  tools:
    - dlt
    - dbt
qualifiers:
  - Needs the exported data flow definition and read access to the sources its reads and sinks name.
  - Needs the flow's own output on the agreed slice, or an approved reference built from its declared semantics.
  - Studio has no ADF connection; the flow is read from its exported definition and never run or edited.
related:
  - legacy-sql-to-dbt
  - spark-ingestion-notebook-to-dlt
  - notebook-transformation-to-dbt
  - stored-procedure-to-dbt
  - managed-connector-to-dlt
evidence:
  features:
    - capturing-requirements
    - add-or-update-source
    - generating-dlt-pipeline
    - ingestion-data-testing
    - generating-dbt-model
    - dbt-unit-testing
    - running-dbt-in-sandbox
    - documenting-dbt-models
    - verifying
  evals: []
---

## Prompt

Convert the <data_flow_name> ADF mapping data flow into code in the current Intent so that <consumers> can review it and later move to it: its source reads that pull from external systems become a dlt pipeline and its transformation graph becomes dbt models. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Give every step of the exported definition one verdict, converted, converted with a stated difference, or not converted, and prove each sink in <sinks> against the data flow's approved reference output on <agreed_slice> at the approved precision. Reproduce what the flow does, including its null handling, its join and split behaviour and its arithmetic where they differ from SQL, and report each behaviour that looks wrong as follow-up work; an output change someone wants belongs in a separate change. Account for every input record, list every difference with its cause, leave the data flow running and consumers unchanged, and state what the comparison cannot prove.

## Verified by

- Every step of the exported definition has one verdict, converted, converted with a stated difference, or not converted, with its reason and the code or gap, and the counts add up to the steps; where the approved policy fails the conversion, the failing step and its reason are named.
- Every source read that pulls from an external system is carried by a dlt pipeline, and each landed source has the row count of its source on the agreed slice under the approved filters or windows.
- Each approved sink's rows equal the approved reference output of the flow, its own run where one exists, on the agreed slice under the approved equality contract, as a multiset in both directions, never by row order; a difference left is listed with its cause and parity is not claimed for it.
- Published results also equal values derived independently from the sources and the flow's declared semantics, including a hand-derived result for each awkward input the approved slice carries, so the comparison does not rest on one calculation agreeing with itself.
- Every input record the flow reads ends in exactly one place, a sink or a drop shown or counted with its reason as approved, the outcome states how many were dropped and why, and the counts add back to the input with no residue.
- For null handling in joins and conditions, a key with several matches, rows matching no split condition or several, date formats, integer and decimal arithmetic, and aggregates over nulls, the flow's construct, the code's construct and the verdict are stated, with the rows where each bites.
- A rerun of the pipeline and models leaves each landed source and sink as the approved load behaviour defines, with no record duplicated, lost or changed beyond load bookkeeping.
- Each behaviour of the flow the code cannot reproduce, or reproduces differently, is listed with its trigger, the rows it affects and its cause; no defect of the flow is corrected in the code, and each is listed as follow-up work.
- The match holds in each approved execution environment and time zone.
- The running data flow is untouched and the conversion adds relations without changing any existing one; a change that reaches an existing relation is named and its parity marked unverified. Consumer cutover and retiring the flow are separate approved work after parity is accepted.
- Anything the comparison cannot prove is stated, including where the reference output is not the data flow's own run.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements. Read the exported definition end to end first: its sources and sinks, every transformation and expression, its parameters, its sink settings and its diagnostic columns, and give each step a stable identifier the report can cite. Settle where the reference output on the agreed slice comes from, and what the awkward inputs are for each ADF and SQL difference named above, including empty or null keys, keys with several matches, rows that match no condition or several, and groups with null measures. Carry each external read into the dlt pipeline and each transformation into models that reproduce the flow's declared expressions and order, and write down what the flow does with every row it reads. Give every step its verdict, compare each sink with the reference output in each approved environment, derive the awkward rows independently, list every difference with its cause and each defect as follow-up work, and state what the comparison cannot prove.

### Compose

- capturing-requirements
- add-or-update-source
- generating-dlt-pipeline
- ingestion-data-testing
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- documenting-dbt-models
- verifying

### Ask first

- If unresolved, which data flow is converted, which parameters it takes, and which input slice forms the comparison?
- If unresolved, where does the flow's own output on that slice come from, a recorded run of the flow or a reference built from its declared semantics, and who approves it?
- If unresolved, what counts as equal at each sink: exact or an approved precision, which decimal scale and rounding, and which names, columns, column order and types must hold?
- If unresolved, what happens to a step the code cannot express: fail the conversion, set it aside and report it, or use a named substitute that is reported as a difference?
- If unresolved, are the rows the flow drops, by a join, a split or an expression error, listed row by row or only counted, and does each carry its reason?
- If unresolved, which of the flow's reads pull from outside the Domain, how is each loaded on a rerun, and which filters or windows must it keep?
- If unresolved, are the flow's sink write policy and its diagnostic or runtime columns reproduced, dropped or only reported?
- If unresolved, in which execution environments and time zones must the result match?

### Guardrails

- Do not edit the data flow, its pipeline or the ADF resource, and do not commit connection strings, linked-service secrets or credentials found in the export.
- Do not correct a defect of the flow, such as a join that drops unmatched rows or a split that lets a null through; reproduce it, report it as follow-up work, and route any wanted output change to a separate change.
- Do not replace the flow's null, ordering or arithmetic behaviour with the SQL default; where the two differ, the flow's declared result is the target and the difference is reported.
- Do not leave a step, an input record or a difference unaccounted for; a step that cannot be converted gets a stated verdict or fails the conversion as approved, never silently dropped.
- Do not compare on row order or widen the precision, narrow the compared slice or change the expected output to make the comparison pass.
- Do not claim parity for a sink, a slice or an environment the comparison did not cover, or equate a reference built from declared semantics with a live factory run.
- Do not treat a green build or passing tests as proof of parity; the proof is the comparison with the approved reference output.
- Do not extend the conversion into orchestration, scheduling, deployment, cutover or retiring the data flow.
