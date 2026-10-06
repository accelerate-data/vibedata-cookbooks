---
id: identity-standardize-names-addresses
title: Standardize names and addresses and mint deterministic match keys
trigger:
  - The same customer is written differently across CRM, billing and support, so joins on name or address miss.
  - A deduplication or golden-record step needs stable, explainable match keys before any fuzzy matching.
  - Addresses arrive in mixed formats across countries, so reports group the same address several ways.
  - Match results must be reproducible from run to run, without depending on run order or an external service.
description: Standardize every source record's name and postal address under approved, editable rules, keep the original values beside the standardized ones, mint deterministic match keys that agree exactly when the standardized values agree, and account for every record as standardized or excluded with a reason, without merging records.
pitch: Give every customer record a clean name, a clean address and a match key you can explain.
job_category: build
area: transformation
readiness: supported
domain_objects:
  - customer_record
  - party_name
  - postal_address
  - match_key
  - standardization_exception
  - rule_list
works_with:
  platforms:
    - duckdb_local
  tools:
    - dbt
qualifiers:
  - Complete outcome assessed for duckdb_local only; the other four Studio targets remain unassessed.
  - Addresses are standardized by rule, not verified against a postal service, so deliverability is not checked.
related:
  - business-event-fact
evidence:
  features:
    - applying-medallion-data-modelling
    - generating-dbt-model
    - dbt-unit-testing
    - verifying
  evals: []
---

## Prompt

Build <standardized_records_model> from <customer_source> with one row per source record at the approved grain, holding the standardized name, the standardized postal address in components, the original values beside them, and <match_key_columns> derived only from standardized values. Build <exceptions_model> listing every record that is excluded or flagged, with one row per reason. Inherit the Intent's sources, platform and approved requirements, and resolve only the semantics they leave open: party types, countries and fields in scope, name and business-name rules, address rules per country, which keys to mint and from which components, what a missing component does, and which records are excluded or only flagged. Rule lists such as honorifics, suffixes, abbreviations, country spellings and transliterations are editable data, so a rule change needs no model change. Two records get the same key exactly when the approved key components agree. Every source record is either standardized or excluded with a reason, never both and never neither. Do not merge, link or deduplicate records.

## Verified by

- Every source record is either standardized or excluded with an approved reason at the approved grain, never both and never neither; source records reconcile to standardized plus excluded records with no duplicates or silent drops.
- Records whose standardized key components agree get identical keys, and records that differ in an approved key component, such as a generational suffix or a unit, get different keys.
- Differences the approved rules ignore, such as case, spacing, punctuation, abbreviation spelling, accents, approved transliterations and an excluded legal suffix, never split one key into two.
- Names follow the approved rules for honorifics, generational suffixes, name order including a comma form and a single word, kept punctuation, nicknames, and how a business is told apart from a person.
- Addresses follow the approved per-country rules for house-number form and position, units, PO boxes, care-of lines, postal codes, regions and cities, and every written form of an in-scope country resolves to one country.
- A record missing a component that a key needs is handled by the approved rule, never gets a key built from a silently defaulted value, and stays visible in the outputs with its reason.
- Original name and address values sit unchanged beside the standardized values, and the standardized name keeps the original characters the approved rules preserve.
- Excluded and flagged records are visible in the exceptions output with one row per approved reason; a flagged record still has its standardized row and keys.
- Changing an editable rule list changes the affected outputs without a model change, and where a rule-set version is approved, every output row shows the version that produced it.
- The same records and rule lists produce the same standardized values and keys on every run, regardless of run order or environment.
- No records are merged, linked or collapsed, and nothing in the output claims that two records describe the same party.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements. Ask only about standardization semantics they leave open; sample data, vendor conventions and existing code are evidence, never policy. Profile the source for name and address fields, record types, address roles, countries and how each country is written, and name any rule the data cannot support. Standardize names and addresses once, in one place, so the standardized output, the keys and the exceptions all share one result. Keep the original values unchanged beside the standardized ones. Hold every approved list as editable data, including honorifics, suffixes, legal forms, abbreviations, unit and PO box markers, region codes, country spellings, house-number positions, transliterations and test markers, and stamp each row with the rule-set version when one is approved. Build each key only from standardized components the user approved, in a fixed order, so equal components give equal keys, and apply the approved rule when a component is missing. Decide edge cases by the approved rules, not by model behaviour: comma names, single-word names, business suffixes, units in several forms, PO boxes, care-of lines, house numbers with letters or ranges, and characters such as umlauts or sharp s. Every source record reconciles to a standardized row or an excluded exception. Stop before matching: keys prepare records for linking but do not link them.

### Compose

- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- verifying

### Ask first

- If unresolved, which party types, source systems and fields are in scope, which countries and address formats apply, and what happens to a record from a country outside that list?
- If unresolved, what identifies one source record, can a record carry several addresses such as billing and shipping, and are current values enough or must earlier names and addresses be kept?
- If unresolved, how are names cased and punctuated, are accents and characters such as umlauts or sharp s kept, folded or transliterated, and in the standardized name, the keys or both?
- If unresolved, how are honorifics, generational suffixes and nicknames treated, how are names split or ordered, including a comma form and a single word, and how is a business told apart from a person?
- If unresolved, how are business names standardized: legal forms such as Inc or GmbH, connecting words such as ampersands, and leading articles, and do legal forms count in the keys?
- If unresolved, which abbreviation standard and direction applies per country, and how are units, PO boxes, care-of lines, house numbers with letters or ranges, house-number position, postal codes, regions, cities and country spellings written?
- If unresolved, which match keys are minted from which standardized components, are they readable or hashed, and what happens when a key component is missing?
- If unresolved, which records are excluded and which are only flagged, such as blank names, test records, out-of-scope countries, non-Latin names or PO boxes, which rule lists does the user keep as editable data, and must outputs carry a rule-set version?

### Guardrails

- Do not invent standardization policy. Abbreviations, name and business rules, key components and exclusions come from approved requirements or the user; values from another Intent or a vendor convention are not defaults. Ask for a missing rule without recommending one.
- Do not treat equal keys as proof that two records are the same party. Do not merge, link, cluster, score similarity or pick surviving values.
- Do not drop or blank records that cannot be standardized. Excluded and flagged records stay visible with their reasons, and a flagged record keeps its standardized row.
- Do not overwrite or lose the original values; the standardized values sit beside them.
- Do not guess a country, region, house number or name part the data does not support; apply the approved rule and keep the record visible.
- Do not call an external address-verification or geocoding service, and do not claim an address is deliverable.
- Keep Domain sources read-only and use the Intent's actual platform; do not modify source data to manufacture evidence.
- Stop at standardized records, match keys and exceptions. Do not extend into matching, deduplication, golden records or geographic enrichment.
