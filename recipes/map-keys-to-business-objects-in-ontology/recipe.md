---
id: map-keys-to-business-objects-in-ontology
title: Map each key to the business object it identifies across a Domain and find datasets keyed by an unmapped object
trigger:
  - Several datasets carry customer, product or order keys, and nobody can say which business object a key identifies or whether two keys name the same one.
  - A key holds a version, a hash or a code and nothing records which, so a join on it counts a changed member twice or matches nothing.
  - A dataset is keyed by an object that no mapping names, and the gap shows only when someone asks where that object lives.
description: Declare the business objects behind the keys of the approved Ossie documents, each identified by its natural code, and map each key to the object it identifies. Leave version surrogates and derived hashes unmapped and named, and report every dataset keyed by an object no mapping names. Declaration only; no model changes.
pitch: Say which object every key identifies, and name every dataset keyed by an object nothing maps.
job_category: explain
area: semantic-layer
readiness: supported
function:
  - cross-functional
domain_objects:
  - ontology
  - business_object
  - business_key
  - semantic_model
  - glossary_term
works_with:
  platforms:
    - duckdb_local
    - motherduck
  tools:
    - ossie
qualifiers:
  - Needs Ossie documents already in the repository; writing them is the semantic-model Recipes' job.
  - A declaration only, so no mapping is executed and it stays unproven as a query until a consumer runs it.
  - Runs where Ossie documents exist and the semantic-model checks execute, today DuckDB-dialect targets.
  - Resolving one customer across systems is identity-golden-record-crosswalk, not this Recipe.
  - The ontology has no construct for a version of an object, so a key that names only a version stays unmapped.
related:
  - identity-golden-record-crosswalk
  - metricflow-semantic-model
  - bi-calculations-to-governed-metrics
evidence:
  features:
    - capturing-requirements
    - designing
    - planning
    - ontology
    - domain-modeling
    - validating-ontology
    - verifying
  evals: []
---

## Prompt

Declare the business objects behind the keys of <ossie_documents> in the Domain ontology and map each key to the object it identifies, so a reader can tell which object a key names and whether two datasets are keyed by the same one. Inherit the Intent's repository, platform, Domain, Ossie documents, glossary and approved requirements, and resolve only the semantics they leave open. Deliver one ontology of the approved business objects, each identified by its natural code; one mapping per Ossie document; a glossary term per object; every key left unmapped, named with its reason; and a report naming every dataset keyed by an object no mapping names, with the decision taken for each. Change no model, dataset, contract or published relation.

## Verified by

- Every business object in the approved scope is declared once, has a glossary term and is identified by its natural code, never by a surrogate, a version or a code invented for it; the structural, reference and glossary checks end with zero errors.
- Every key of every approved document is accounted for: mapped to the object it identifies, or left unmapped and named with its reason, such as a version, a derived hash with no natural code, members held elsewhere or not an object. No key is silently omitted.
- A key that names one version of a member, or a derived value with no natural code beside it, identifies no object in any mapping; a mapping that names one is reported as an error.
- An object keyed in several documents has one declaration and a mapping in each, the same key names the same real-world object in all of them, and a difference in the population each covers is stated, not hidden.
- Roles of one object, such as two dates on a line or a pickup and a drop-off, are separate named relationships to that one object, never one relationship used for both and never a second object.
- Every document is mapped or its description says why no object reaches it, and every object reaches a dataset or its description says it is declared ahead of its data.
- Every dataset keyed by an object no mapping names is listed with the decision taken, mapped or kept out with its reason; each warning the identity checks raise is cleared by a mapping or left standing with its reason.
- Each identity check is shown to report a defect introduced on a copy, such as a dropped mapping or a key mapped on a version surrogate, and a check that reports nothing is not read as a pass; a result from a copy is never evidence about the committed ontology.
- Every statement about members, versions or placeholder members matches what the served relation holds; a description that omits a member the relation carries, or names one it does not, is a finding.
- A key value that names no member of its own dimension, such as a placeholder key on a fact, is reported as a finding about the model, never mapped around or repaired here.
- The outcome says plainly that the ontology is a declaration: no mapping is described as proven against a built relation unless a consumer has run it.
- No model, dataset, seed, contract or Ossie document changes; only the ontology, its mappings, the glossary and the decision record change.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, Ossie documents, glossary and approved requirements, and resolve only the semantics they leave open. Read the glossary, every Ossie document in scope and the source and staging SQL of every dataset a key could reach, never names alone. Classify each table, then route each key by what the data holds: the natural code of an object, a version surrogate, a derived hash, a placeholder member, or a foreign key to members held elsewhere. Declare objects from glossary terms, map each key in its own document's mapping, state the roles of repeated keys, and name every unmapped key, dataset and document with its reason inside the artifacts. Describe each object's members as the served relation holds them, placeholder members included, reading the served relation and not only its source. Run the structural, reference and glossary checks, confirm each can fail by introducing a defect on a copy, and report the datasets keyed by an object no mapping names with the decision for each. Report a model defect as a finding, never a fix.

### Compose

- capturing-requirements
- profiling-source-data
- domain-modeling
- designing
- ontology
- validating-ontology
- planning
- verifying

### Ask first

- If unresolved, which documents and datasets are in scope, and which kinds of table, such as dimension, fact, snapshot or reference, get an object and which are exempt with a reason?
- If unresolved, which object does each key identify, and where one word names several things, such as a customer as order party, a resolved customer or a source record, which distinct objects exist and are they ever asserted equal?
- If unresolved, is an object carried by two documents with different coverage, such as two calendars, one object or two, and where is the difference in coverage stated?
- If unresolved, how is a key handled that holds a version, or a derived hash with no natural code: left unmapped and reported, or does the owner supply a natural code or change the model?
- If unresolved, which keys are placeholder members, such as unknown, unassigned or unmapped, do they stay inside the object's population, and how is a fact key that matches no member handled?
- If unresolved, is a dataset keyed by an object no mapping names mapped or kept out with its reason, is an identity warning cleared or left standing, and who owns the answer when the members are held elsewhere?
- If unresolved, which terms may be added to the glossary, and which identity decisions need a decision record?

### Guardrails

- Do not give an object an identity that is a surrogate, a version or an invented code; report the key as a surrogate with no natural code.
- Do not declare an object the glossary does not name, and do not add glossary vocabulary without approval.
- Do not clone an object per document, and do not merge two objects because their keys share a name.
- Do not map a key to an object whose members the dataset does not hold; declare the object ahead of its data instead.
- Do not map a dataset only to silence an identity warning; map it where it holds the object's members.
- Do not change a model, seed, contract or Ossie document to make a mapping resolve; report the defect with its evidence.
- Do not describe a declaration as proven; no mapping is executed unless a consumer runs it.
- Do not stage a dataset or fixture to make an identity check fire, or present a result from a copy as evidence about the committed ontology.
- Do not choose the object set, whether two objects are the same, or the disposition of an unmapped dataset without approval.
