---
id: visual-etl-mapping-to-dlt-dbt
title: Rebuild an exported visual ETL mapping as dlt and dbt and prove parity
trigger:
  - A load into a fact or reporting table still runs from a mapping built in a visual ETL tool, and its lookups, filters, routing and insert-update-delete rules are visible only on the tool's canvas.
  - The team is leaving the visual ETL tool and needs the mapping's reads, transformations, reject path and outputs as dlt and dbt code that can be reviewed and tested.
  - Someone has to show the rebuilt outputs match what the mapping writes, including its rejects, before consumers are moved off it.
description: Rebuild one exported visual ETL mapping as a dlt pipeline for its source reads and dbt models for its transformation graph, with a verdict for every step, every output including rejects compared with the mapping's reference run, and a specified cutover and recovery path that keeps the old path available.
pitch: Rebuild a visual ETL mapping as dlt and dbt code, prove each output and reject path against its reference run, and specify the cutover.
job_category: re-engineer
area: transformation
readiness: supported
function:
  - cross-functional
domain_objects:
  - etl_mapping
  - dlt_pipeline
  - dbt_model
  - sink
  - reject_path
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
  - Needs a readable export of the mapping, its resolved parameters and read access to its sources.
  - Needs the mapping's own output on the agreed slice, or an approved reference built from its declared semantics.
  - Studio has no connection to the visual ETL tool; the mapping is read from its export and never run or edited.
related:
  - adf-mapping-data-flow-to-dlt-dbt
  - legacy-sql-to-dbt
  - stored-procedure-to-dbt
  - notebook-transformation-to-dbt
  - spark-ingestion-notebook-to-dlt
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

Rebuild the <mapping_name> visual ETL mapping in the current Intent so that <consumers> can review it and later move to it: its source reads become a dlt pipeline and its transformation graph becomes dbt models. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Give every input, lookup, transformation, router or filter branch, reject path and output of the export one verdict, converted, converted with a stated difference, or not converted, with its reason. Reproduce what the mapping does, including its lookup match rules, null and error treatment, branch conditions, the insert, update or delete decision per row and what a rerun does, and prove every output in <outputs>, rejects included, against the mapping's reference run on <agreed_slice> and independently from the sources. List each node the code cannot express as an explicit blocker, specify a bounded cutover and recovery method without performing it, keep the old path available, and state what the comparison cannot prove.

## Verified by

- Every input, lookup, transformation, branch, reject path and output of the export has one verdict, converted, converted with a stated difference, or not converted, with its reason and the code or gap, and the counts add up to the steps; an unsupported node is a named blocker, never a silent drop.
- Every source read is carried by a dlt pipeline, and each landed source has the row count of its source on the agreed slice under the approved filters.
- Every output, rejects included, equals the mapping's reference run on the agreed slice under the approved equality contract, as a multiset in both directions, never by row order; a difference left is listed with its cause and parity is not claimed for it.
- Published results equal values derived independently from the sources and the mapping's declared semantics, with a hand-derived result for each awkward input on the slice, such as a key with several lookup matches, a null key, a row in several branches or none, or a delete for a row never loaded.
- Each input record is accounted for: it reaches each output it belongs to or an explicit drop with its reason, and per-output contributions add back to the input with no residue.
- For lookup multiplicity, null and error treatment, branch conditions that overlap or leave rows out, update and delete disposition, and arithmetic or date handling, the mapping's construct, the code's construct and the verdict are stated, with the rows where each bites.
- A rerun of the pipeline and models leaves each output as the approved load behaviour defines, with no record duplicated, lost or changed beyond load bookkeeping.
- Each behaviour the code cannot reproduce, or reproduces differently, is listed with its trigger, the rows it affects and its cause; no defect of the mapping is corrected in the code, and each is listed as follow-up work.
- A cutover and recovery method is specified, with the parallel-run comparison it needs, the approval it waits for and how to return to the old path; the mapping keeps running and no consumer changes in this work.
- Anything the comparison cannot prove is stated, including where the reference run is not the mapping's own.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements. Read the export end to end first: its sources, lookups, expressions, branch conditions, update rules, reject outputs, parameters and runtime settings, and give each step a stable identifier the report can cite. Settle where the reference run on the agreed slice comes from, and what the awkward inputs are for each behaviour above, including null and unmatched keys, keys with several matches, rows in several branches or none, and deletes for rows never loaded. Carry each source read into the dlt pipeline and each transformation, branch and update rule into models that reproduce the mapping's declared behaviour, and trace each input record to every output it reaches or to its drop. Give every step its verdict, compare every output with the reference run, derive the awkward rows independently, list every difference with its cause, and state what the comparison cannot prove. Write the cutover and recovery method as a specification only.

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

- If unresolved, which mapping is rebuilt, which resolved parameters and connections it runs with, and which input slice forms the comparison?
- If unresolved, where does the mapping's reference run on that slice come from, a recorded run or a reference built from its declared semantics, and who approves it?
- If unresolved, what counts as equal at each output: exact or an approved precision, which names, columns and types must hold, and which generated keys and runtime columns are reproduced, dropped or only reported?
- If unresolved, which lookup match wins when several rows match a key, and what happens to a row whose lookup finds nothing or whose key is null?
- If unresolved, what happens to a row that fits no branch or several: set aside, rejected or sent to each, and does each reject carry its reason?
- If unresolved, how does a rerun treat rows already loaded (merge, append or overwrite), and are a delete for a row never loaded and an update that changes nothing reported or counted?
- If unresolved, what happens to a node the code cannot express: fail the conversion, set it aside and report it, or use a named substitute reported as a difference?
- If unresolved, who approves the cutover, how long the parallel run lasts, and what returns consumers to the old path?

### Guardrails

- Do not edit the mapping, its workflow, its schedule or the visual ETL tool, and do not commit connection strings, passwords or credentials found in the export.
- Do not correct a defect of the mapping, such as a lookup that hides duplicate keys; reproduce it, report it as follow-up work, and route any wanted output change to a separate change.
- Do not replace the mapping's null, error, ordering or arithmetic behaviour with the SQL default; where the two differ, the mapping's declared result is the target and the difference is reported.
- Do not leave a step, an input record or a difference unaccounted for; a node that cannot be converted gets a stated verdict or fails the conversion as approved.
- Do not compare on row order or widen the precision, narrow the compared slice or change the expected output to make the comparison pass.
- Do not claim parity for an output, slice or environment the comparison did not cover, or equate a reference built from declared semantics with a live run of the mapping.
- Do not treat a green build or passing tests as proof of parity; the proof is the comparison with the reference run.
- Do not perform the cutover, retire the old path, change a schedule or repoint consumers; this work specifies them only. Control flow and orchestration of the workflow belong to separate work.
