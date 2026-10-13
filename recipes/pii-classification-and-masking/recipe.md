---
id: pii-classification-and-masking
title: Tag personal-data columns, mask them by kind and prove what a lower-privilege audience is served
trigger:
  - Analysts need tables that carry names, addresses, emails, phone numbers or ID numbers they must not see.
  - Nobody can say which published columns hold personal data, so a new column can leak it unnoticed.
  - An auditor asks to see exactly what a lower-privilege user can read, and whether the clear values can be reached another way.
description: Classify every column of the governed relations as a kind of personal data or as not personal, serve a lower-privilege audience each kind masked as approved, limit that audience to the approved access, and prove what each audience is served, run as each role where applying the roles and grants is in scope, including whether clear values can be recovered where that is required.
pitch: Classify personal data by column, mask it by kind for a lower-privilege audience, and prove what that audience is served.
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
  - Fabric Lakehouse is excluded because OneLake and Spark reads bypass its SQL endpoint grants.
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

Classify every column of <governed_relations> as an approved kind of personal data or as not personal, serve <lower_privilege_audience> each kind masked as approved within <approved_access_scope>, and keep <privileged_audience> reading the clear values. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Deliver the classification, the masking for each kind and the access scope, held in the project where they can be reviewed and changed; the platform's roles and grants, authored to stay in force across rebuilds; a check that handles a column nobody classified, a stale classification entry or an unclassified discovery candidate as the approved policy says; and evidence of what each audience reads and, where the approved requirement says so, that clear values cannot be recovered by query, run as the roles on the warehouse where applying them is in scope and otherwise reported unproven. State what the evidence cannot prove.

## Verified by

- On a build that runs the classification checks and passes, every governed column is classified as an approved kind or as not personal, in the project where a reviewer can read it.
- Where the approved policy fails the build, the failure names each unclassified column or candidate and stale entry; otherwise each is hidden, or masked with a warning naming it, as approved, and none is served in the clear.
- On a build that runs the classification checks and passes, the lower-privilege audience is served each governed relation's rows as the privileged audience reads them, not-personal values unchanged and personal values exactly as the approved treatment renders them, nulls and blanks included.
- Where masked data must stay countable or joinable, counts and joins through the approved identifiers give the lower-privilege audience the same results as the privileged audience.
- No candidate found by the approved discovery rules in a relation the lower-privilege audience is served is served in the clear until it is classified, or cleared with a recorded reason by an approved clearer.
- Where applying the roles and grants is in scope, run as each role on the warehouse, the privileged role reads every clear value and the lower-privilege role reads exactly the approved access scope with no personal column in the clear.
- Where clear values must be unrecoverable by query and the roles are applied, every route outside the approved access scope is refused to the lower-privilege role, and a filter or join on a known clear value finds nothing beyond what the approved treatment reveals.
- Where masking what is displayed is approved as enough, the platform's documented inference risk is reported.
- Where the roles and grants are applied, a rebuild leaves each role's access as approved: grants the platform drops when it recreates a relation are restored, and nothing outside the approved access scope becomes readable.
- Where applying the roles and grants is not in scope, the role checks above are reported unproven, and the unapplied access rules are reported as blockers to granting the lower-privilege audience access, never as a passed check.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Enumerate the governed relations and the columns each one actually has, and profile their names and values for personal data before classifying them with the user. Choose the enforcement the target platform offers that renders each kind as approved and meets the approved recoverability requirement, and record what it relies on and what it would miss. Author the roles and grants for the target, and keep them in force when a build recreates a relation. Prove what each audience is served against the approved treatments, including their edge forms, and where the roles are applied run the checks as each role with every other route to the clear values attempted. Report the checks that could not run.

### Compose

- capturing-requirements
- profiling-source-data
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which relations are governed, which audience is privileged, which is the lower-privilege audience, and is applying the roles and grants to the warehouse in scope?
- If unresolved, which kinds of personal data does the organisation recognise, and which kind, or not personal, is each column of the governed relations?
- If unresolved, what is the lower-privilege audience served for each kind (removed, a fixed mask, a partial value, a token), how are nulls and blanks shown, and must masked data stay countable or joinable, through which identifiers?
- If unresolved, must the lower-privilege audience be unable to recover clear values by any query (filters, joins, base relations), or is masking what it displays enough?
- If unresolved, what happens to a column nobody classified, a discovery candidate not yet classified or cleared, and a classification entry whose column no longer exists: fail the build, or hide the column or mask it and warn?
- If unresolved, which relations beyond the governed ones may the lower-privilege audience read, and is access granted per relation or per schema?
- If unresolved, how are unclassified personal data found (name terms, value shapes or other rules), over which relations, and who may clear a candidate?

### Guardrails

- Do not choose a kind, a treatment, an audience or the access scope without approval; recommending one is fine.
- Do not treat a column nobody classified as not personal, and do not clear a discovery candidate without a recorded reason.
- Do not serve the lower-privilege audience a personal column in the clear.
- Do not rely on masking what is displayed where clear values must be unrecoverable by query.
- Do not claim the roles and grants are proven on the warehouse from a local stand-in.
- Do not change what the privileged audience or existing consumers read beyond the approved access changes.
- Do not extend this Recipe to row-level security, sensitivity labels, encryption, erasure or access auditing.
