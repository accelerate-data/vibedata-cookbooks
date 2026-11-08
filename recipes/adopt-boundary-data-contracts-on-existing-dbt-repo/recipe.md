---
id: adopt-boundary-data-contracts-on-existing-dbt-repo
title: Adopt boundary data contracts on an existing dbt repo with a review queue and a CI diff gate
trigger:
  - A dbt repo publishes relations to readers, and loader landings feed them, but nothing states each relation's grain, nulls, allowed values or links to other relations.
  - Consumers cannot tell which column meanings and rules are promised, and a change to a published relation is only noticed when a reader breaks.
  - A contract tool can draft contracts from the data, but the open business questions behind them must be answered and recorded rather than guessed.
description: Draft one data contract per relation in the approved scope, work the review queue so each answer becomes a description, a rule or a written no-rule reason, add dbt enforcement and a CI diff gate, and report every gate that could not run.
pitch: Give every published and landed relation in the approved scope a stated promise, with open questions queued and a gate that flags a contract changing silently.
job_category: build
area: data-quality
readiness: supported
function:
  - cross-functional
domain_objects:
  - boundary_relation
  - data_contract
  - output_contract
  - review_queue_item
  - diff_gate
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
  - Renaming a published relation or file, or versioning a breaking change, belongs to the contract cutover Recipe.
  - The contract tool profiles DuckDB and MotherDuck only; elsewhere rules are measured by direct queries.
  - Semantic model and ontology authoring are outside this Recipe.
related:
  - versioned-data-contract-cutover
  - incremental-dbt-model-with-contract
  - consolidate-duplicate-source-extracts
evidence:
  features:
    - data-contract
    - validating-data-contract
  evals: []
---

## Prompt

Adopt data contracts for <contract_scope> in this repository. Inherit the Intent's repository, platform, Domain, layers, sources and approved requirements, and resolve only the semantics they leave open. Deliver one contract per relation in the approved scope stating its name, grain, key, column meanings, nulls, allowed values and links; a review queue in which every open business question is answered as a description, a rule or a written reason for no rule, or stays open with its owner; dbt enforcement matching the contracts; a CI check that compares contracts against <base_ref>; and a gate report that names each gate that could not run. Published values, names and tests stay as they were.

## Verified by

- Every relation in the approved scope has a contract, and each relation the scope leaves out is listed with its reason.
- Each contract states the relation's published name, grain and key, and for each column its meaning, nullability and allowed values, or a written no-rule reason, or is marked open with its queue item and owner; none is left blank or filled by default.
- Each claimed null, uniqueness, allowed-value, range and link rule is measured on the data independently of the contract tool and holds, or its violation is recorded as a finding with the affected output; no claim is weakened without that record.
- Each review-queue item is closed with a description, a rule, a link or a written no-rule reason by its owner, or stays open with its owner named; no business meaning, failure behaviour or population is chosen by the agent.
- Published relations keep their names, schemas, values and every test they had before; each change adoption makes to a model file is listed, and a test, file or column that existed before still exists.
- Each enforced relation's columns and types equal its contract and it builds with enforcement on in the approved environment, or is reported unbuilt and unproven; each relation left unenforced is listed with its approved reason.
- Relations the approved scope keeps as proposed carry that status and an approved reason, produce no enforcement and no data check, and are counted as not judged, never as passing.
- Against the approved base, a contract change that removes a column or tightens a rule without a version bump is reported and blocks as approved; the check runs on a pull request, or is reported unrun.
- Each gate that read the data reports its result and scope; a gate the platform cannot run, or whose evidence is missing or stale, is reported unrun or unmeasured, never as passing.
- Every finding the checks report is fixed in the contract, attributed to a recorded tool limitation naming the relation, or queued as a data defect or open item with its owner; the count and cause of each remaining finding are stated.
- A data defect found while reviewing, such as a total that does not foot or a type that differs from a reader's, is queued with the output it affects and is not corrected in place.
- A written review gives each relation a verdict, including relations it could not judge and why; claims no gate could check are stated as unproven.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, layers, sources and approved requirements, and resolve only the semantics they leave open. Find which relations the repository declares as boundaries and inputs, which published relations readers use, and which are not built, and settle the scope with the owner before drafting. Draft each contract from the data, then work the review queue in the order the owner sets, publishing the answers as descriptions, rules, links or written reasons. Add the dbt enforcement the contracts call for and the CI comparison against the base. Compare the repository's published names, schemas, values and tests before and after so adoption changes none of them, and write the tool's limits down as queue entries rather than editing published relations to satisfy it. Run each gate the platform allows, report the rest as unrun, measure the claims the gates cannot see directly, and state what remains unproven.

### Compose

- data-contract
- validating-data-contract
- generating-dbt-model
- capturing-requirements
- profiling-source-data
- verifying

### Ask first

- If unresolved, which layers and relations owe a contract, which inputs are in scope, which published or granted relations are left out and why, and are relations not yet built stated as proposed, built first, or left out?
- If unresolved, who answers each business question in the review queue, and in what order are the relations worked?
- If unresolved, what does each contract promise a reader when a rule breaks, and does a broken rule fail the build or warn? Changing a model's output is queued, not built here.
- If unresolved, when the data contradicts a claimed rule, is the claim weakened with a recorded finding, is the data fixed separately, or does it stay open?
- If unresolved, which relations carry dbt enforcement, which are deliberately left unenforced and why, and what happens to existing dbt contracts, contract files or tests that disagree with the data: keep, merge or queue?
- If unresolved, what is the base for the CI comparison, how is a contract version bumped, and which gate results block a merge?
- If unresolved, which environment's data drafts and verifies the contracts, how are per-environment schema names stated, are large relations measured in full or over a window, and may observed values enter committed contracts or are sensitive columns classified?
- If unresolved, how are loader metadata columns described, and which name does a contract carry for a relation published under an alias?

### Guardrails

- Do not change a published relation's name, values, tests or file name to make a contract or gate pass; queue the conflict with the output it affects.
- Do not pick a failure behaviour, a business meaning or a population for a rule; where unanswered, the item stays open with its owner.
- Do not report a gate that did not run, or whose evidence is stale, as passing; state it as unrun or unmeasured.
- Do not keep a rule the data violates without a recorded finding, or drop or weaken one silently to clear a finding.
- Do not build a relation, or draw a conclusion about data, that the approved scope marks as not built.
