---
id: pii-classification-and-masking
title: Tag personal-data columns, mask them by kind for a lower-privilege audience and prove the masked outputs
trigger:
  - Analysts need tables that carry names, addresses, emails, phone numbers or ID numbers they must not see.
  - Nobody can say which published columns hold personal data, so a new column can leak it unnoticed.
  - An auditor asks to see exactly what a lower-privilege user can read, and whether the clear values can be reached another way.
description: Classify every column of the governed relations as a kind of personal data or as not personal, serve a lower-privilege audience each kind masked as approved, limit that audience to the approved access, prove the masked outputs correct whether or not grants are applied, and, where applying the grants is approved, verify each role's effective access, including whether clear values can be recovered.
pitch: Classify personal data by column, mask it by kind for a lower-privilege audience, and verify that audience's access where grants are applied.
job_category: build
area: governance-cost
readiness: supported
domain_objects:
  - personal_data_classification
  - masking_treatment
  - access_role
  - masked_column
  - discovery_candidate
works_with:
  platforms:
    - fabric_warehouse
    - redshift
  tools:
    - dbt
qualifiers:
  - Not yet assessed end to end on fabric_warehouse or redshift.
  - Needs database roles and per-object grants on the target; DuckDB and MotherDuck have neither.
  - Applying the roles and grants and running the role checks need a live warehouse and approval to change access.
  - Fabric Lakehouse is excluded because its SQL endpoint grants do not govern OneLake or Spark reads.
  - Assumes the lower-privilege audience has no storage-level read path that bypasses database grants.
  - Finds personal data inside free text only as far as the approved discovery rules reach.
  - Row-level security, sensitivity labels, encryption, erasure and access auditing are outside this Recipe.
related:
  - identity-standardize-names-addresses
  - identity-golden-record-crosswalk
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

Classify every column of <governed_relations> as an approved kind of personal data or as not personal, serve <lower_privilege_audience> each kind masked as approved within <approved_access_scope>, and keep <privileged_audience> reading the clear values. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Deliver the classification, the masking for each kind and the access scope, held in the project where they can be reviewed and changed; the platform's roles and grants, authored so the lower-privilege role never reads a relation, or a version of one, the checks have not cleared; a check that handles a column nobody classified, a stale classification entry or an unclassified discovery candidate as the approved policy says; and evidence that the masked outputs are correct whether or not grants are applied and, where applying the grants is approved, of each role's effective access queried as that role, including attempts to reach clear values outside the approved scope, with audience access otherwise reported unproven. State what the evidence cannot prove.

## Verified by

- Every governed column's classification, an approved kind or not personal, is held in the project where a reviewer can read it, and a column without one is handled as the approved policy says.
- Where the approved policy fails the build, the failure names each unclassified column or candidate and stale entry; otherwise each such column is hidden, or masked with a warning naming it, and each stale entry is reported, as approved; none appears in the clear in a masked output.
- On a build that runs the classification checks and passes, each authored masked output holds its governed relation's rows, not-personal values unchanged and personal values exactly as the approved treatment renders them, nulls and blanks included, whether or not grants are applied.
- Where masked data must stay countable or joinable, counts and joins through the approved identifiers give the same results on the masked outputs as on the governed relations.
- No candidate found by the approved discovery rules in a masked output or other relation in the approved access scope appears in the clear until it is classified, or cleared with a recorded reason by an approved clearer.
- Read without applying them, the authored roles and grants give the lower-privilege role exactly the approved access scope, per relation or per schema as approved, and no build plans it a grant on a relation with clear personal columns or one it wrote that its checks did not clear.
- Where applying the grants is approved, querying as each role on the warehouse after a build whose checks pass shows the privileged role reads every clear value and the lower-privilege role reads exactly the approved access scope, with attempts to reach clear values outside it refused.
- Where applying the grants is approved and clear values must be unrecoverable by query, routes outside the approved access scope that were not attempted are reported unproven, and a known clear value finds nothing beyond what the treatment reveals.
- Where masking what is displayed is approved as enough, the ways a filter or join can still infer a masked value on that platform are reported.
- Where applying the grants is approved, after any build the lower-privilege role can read no relation, or version of one, that the checks have not cleared; access to cleared relations stays in force, and each relation withheld is named.
- Where grants remain unapplied, each audience's effective access is reported unproven, never as a completed acceptance condition, and the unapplied access rules are reported as blockers to granting the lower-privilege audience access.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Enumerate the governed relations and the columns each one actually has, and profile their names and values for personal data before classifying them with the user. Choose the enforcement the target platform offers that renders each kind as approved and meets the approved recoverability requirement, and record what it relies on and what it would miss. Author the roles and grants for the target so that, across rebuilds, the lower-privilege role never reads a relation or a version of one the checks have not cleared. Prove the masked outputs against the approved treatments, including their edge forms, and where applying the grants is approved query as each role, attempting the routes to the clear values the platform offers and reporting any not attempted. Report the checks that could not run.

### Compose

- capturing-requirements
- profiling-source-data
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which relations are governed, which audience is privileged, which is the lower-privilege audience, and is applying the roles and grants to the warehouse approved?
- If unresolved, which kinds of personal data does the organisation recognise, and which kind, or not personal, is each column of the governed relations?
- If unresolved, what is the lower-privilege audience served for each kind (removed, a fixed mask, a partial value, a token), how are nulls and blanks shown, and must masked data stay countable or joinable, through which identifiers?
- If unresolved, must the lower-privilege audience be unable to recover clear values by any query (filters, joins, base relations), or is masking what it displays enough?
- If unresolved, what happens to a column nobody classified, a discovery candidate not yet classified or cleared, and a classification entry whose column no longer exists: fail the build, or hide the column or mask it and warn?
- If unresolved, which relations beyond the governed ones may the lower-privilege audience read, and is access granted per relation or per schema (a per-schema grant reaches every relation in it unless the platform can withhold one)?
- If unresolved, how are unclassified personal data found (name terms, value shapes or other rules), over which relations, and who may clear a candidate?

### Guardrails

- Do not choose a kind, a treatment, an audience or the access scope without approval; recommending one is fine.
- Do not treat a column nobody classified as not personal, and do not clear a discovery candidate without a recorded reason.
- Do not serve the lower-privilege audience a personal column in the clear.
- Do not grant or restore the lower-privilege role's access to a relation, or a version of one, the classification checks have not cleared.
- Do not rely on masking what is displayed where clear values must be unrecoverable by query.
- Do not claim the roles and grants are proven on the warehouse from a local stand-in.
- Do not change what the privileged audience or existing consumers read beyond the approved access changes.
- Do not extend this Recipe to row-level security, sensitivity labels, encryption, erasure or access auditing.
