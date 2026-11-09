---
id: legacy-reference-table-to-dbt-seed
title: Move an approved legacy reference table into a dbt seed and prove downstream parity
trigger:
  - A small, static lookup or code list that dbt models read lives in a legacy database, and its owner wants the dbt project to own it.
  - A legacy job still reloads a reference table that dbt models join, and nobody can say who may change it or what a change would do to the reports.
  - A migration plan marks a table as reference data, but nothing records that anyone approved it for seed ownership.
  - A table proposed as a seed may be too large or change too often, and needs a suitability decision before any file is made.
description: Turn one approved small, static legacy reference table into a version-controlled dbt seed from an approved extract with a stated boundary, with typed columns, keys, tests and an ownership record, and prove the dbt consumers' output unchanged; unsuitable tables are reported, not seeded.
pitch: Give a legacy lookup table to the dbt project as a seed, and show the reports that read it do not change.
job_category: re-engineer
area: transformation
readiness: supported
function:
  - cross-functional
domain_objects:
  - reference_table
  - dbt_seed
  - extraction_boundary
  - ownership_record
  - consumer_contract
  - parity_report
works_with:
  platforms:
    - duckdb_local
    - motherduck
    - fabric_lakehouse
    - fabric_warehouse
    - redshift
    - databricks
  tools:
    - dbt
qualifiers:
  - Starts from an approved extract of the table with a stated boundary; it does not read the legacy database.
  - A table that keeps arriving as exports or grows belongs to an ingestion Recipe, not a seed.
  - Large or frequently changing tables are reported unsuitable, not seeded.
  - Retiring the legacy table or its writer is a separate approved step.
  - A table a routine derives from other data belongs to a writer-conversion Recipe, not a seed.
  - Needs the consuming dbt models to exist; moving them is another outcome.
  - History to preserve belongs to dbt-snapshot-history; this seed holds the approved current rows.
related:
  - governed-spreadsheet-table
  - file-drop-to-bronze
  - consolidate-legacy-table-writers-to-dbt
  - inventory-legacy-database-over-mcp
  - plan-legacy-warehouse-layers-to-dbt-intents
  - prove-dbt-change-safe
  - dbt-snapshot-history
evidence:
  features:
    - capturing-requirements
    - generating-dbt-model
    - running-dbt-in-sandbox
    - verifying
  evals: []
---

## Prompt

Move the approved reference table <legacy_table> into a version-controlled dbt seed that the project owns, starting from the approved extract <approved_extract> and its stated extraction boundary, with no ingestion pipeline built. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. First record the owner's approval that this table is suitable for seed ownership, or report it unsuitable with the reason; a table with no writer is not thereby a seed. Deliver the seed file with declared column types, its keys and tests, an ownership record beside it, and the consuming models <consumer_models> reading the seed. Show that the seed holds the approved extract and that what those models publish is unchanged, or changed only as approved. Show what a repeat load does and what an approved update or deleted code does as approved, keep the legacy table maintained or retire it only as approved, and state what the comparison cannot prove.

## Verified by

- The owner's approval as a seed, with size, rate of change and storage permission, is recorded before any seed exists; a table whose values may not be stored in the repository, above the approved size or rate, derived by a routine, or seeded only because nothing writes it, is reported unsuitable.
- The extraction boundary (rows, as-of time or version, how taken) is stated and rows it leaves out are counted with their reason as approved. The seed equals the current approved extract value for value, apart from approved corrections and set-aside rows, each listed, shown by count and checksum.
- Each column holds its approved type, read back from the target rather than guessed from the file; the approved key is unique and never null in the seed, or each exception is named under its approved disposition, and keys are compared under the approved case, whitespace and collation rule.
- Values that file formats alter survive on cases the shipped data may not hold: a leading-zero code keeps its zeros, numeric text its precision, and delimiters, quotes, accents and long text are unchanged. Empty and missing stay distinct under the approved encoding, or the gap is reported unproven.
- A duplicate key or missing key in the extract, and a consumer key the seed lacks, each follow the approved disposition, with offending items named and any set-aside row counted with its reason; none is dropped, collapsed or defaulted outside it.
- Every key the consuming models carry resolves to the seed, or follows its approved disposition and is counted; references from the seed to other tables and from other tables to it are checked as approved, and consumer rows with an empty key are counted, not lost.
- What each consuming model publishes equals what it published before, on the same consumer inputs with the baseline taken at the approved boundary, compared on values against an expectation held outside the model, or differs only as an approved update or correction explains, with the rows shown.
- A repeat load of the unchanged seed changes neither content nor consumer output. An approved update follows the approved replacement and deletion rules with each consumer's effect shown first; deleting or rewording a code consumers match on fails a check or changes output only as approved.
- Where the table carries validity ranges, overlaps and gaps follow the approved rule and each consumer selects the row as approved.
- The seed, its metadata and an ownership record (owner, approver, date, boundary, change procedure, which copy consumers read, whether the other is still maintained) are committed together, and loading on the Intent's target reads back the approved rows.
- Proof cases stay outside the seed paths. After the approved cutover one process alone writes the relation consumers read, and the legacy table and its writer change only as approved; retirement is not done here.
- What the comparison cannot prove, such as consumers or writers outside the project, is stated.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. From the extract, the project's lineage and the owner's statement, find who reads the table and judge its size and rate of change; state consumers and writers outside the project as unknown. Profile the extract for keys, types, nulls and text edge cases. Record what the extract is, how it was taken and checked, so the seed is never both the copy and its own proof. Declare column types rather than letting the loader infer them, and check what the target stores. Prove content, type, key and relationship rules with inputs that separate a faithful load from a lossy one: leading-zero codes, empty versus missing values, trailing-zero decimals, delimiters, quotes, accents, a duplicate code, a missing code, a reworded code and a deleted code. Run them on throwaway copies outside the seed paths, restore the seed after each, and record what was observed. Compare consumer output with an expectation held outside the model. Keep the owner, approval, boundary, change procedure and measured effect of a change beside the seed. Report how other platforms would load the seed and what was not assessed.

### Compose

- capturing-requirements
- profiling-source-data
- generating-dbt-model
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, is this table suitable to be a seed, who approves that, what size or rate of change makes it unsuitable, may its values be stored in the repository and read by whom, and is it derived by a routine rather than maintained directly?
- If unresolved, what is the extraction boundary: which rows, as of what time or version, taken how, which rows it leaves out, such as inactive or deleted ones, and which count and checksum stand for it?
- If unresolved, what is the key, how are keys compared for case, whitespace and collation, what are the column types, and how are leading zeros, empty versus missing values, precision, length and encoding kept?
- If unresolved, how are a duplicate key, a missing key, a consumer row with an empty key, a consumer key absent from the seed, and references to or from other tables treated: failed, set aside, kept as today or flagged?
- If unresolved, does the table carry validity ranges or effective dates, and how are overlaps, gaps and each consumer's as-of rule handled?
- If unresolved, which consuming models and breakdowns are compared, on which inputs and at what precision, and which differences are approved?
- If unresolved, what are the replacement and deletion rules for a reload and an approved update, which value corrections and which new extract revision are approved, who approves a change to a value consumers match on, and who owns the seed?
- If unresolved, after the move does the legacy table stay maintained, get marked retired or get removed, when do consumers outside the project move, and who approves retirement?

### Guardrails

- Do not make a table a seed because it has no writer; suitability is approved, and an unsuitable table is reported, not converted.
- Do not build the seed from the dbt project's own output or prove it against itself.
- Do not let the loader infer types, or change, reorder or add a row or value that is not an approved named correction.
- Do not drop, collapse or default a duplicate, missing or unmatched key outside an approved disposition.
- Do not edit the expected consumer output or widen the approved precision to make a comparison pass.
- Do not leave probe or fixture data in the seed paths.
- Do not write to the legacy database or retire its table or writer unless approved.
- Do not let two processes maintain the relation consumers read after cutover, or give the seed the name of a relation another load maintains.
