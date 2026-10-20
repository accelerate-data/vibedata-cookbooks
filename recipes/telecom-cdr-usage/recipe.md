---
id: telecom-cdr-usage
title: Land call-detail batches and aggregate them into subscriber-day usage with manifest completeness
trigger:
  - Monthly subscriber usage differs by who ran it, because nobody can say which call-detail batches had landed or whether each arrived complete.
  - A batch is re-sent, cut short, missing its manifest or delivered late, and the usage numbers change or hold a quiet day that was really a gap.
  - Billing or network analytics need usage per subscriber per day with every record accounted for and each day marked as backed by complete batches or not.
description: Land switch call-detail batches with their manifests, report every expected batch against its declared count, and publish usage per subscriber and day with each day's backing stated, every record counted, set aside or unusable with a reason, and late batches restated visibly.
pitch: Land call-detail batches and publish subscriber-day usage with batch completeness, day backing and visible restatement of late batches.
job_category: build
area: ingestion
readiness: supported
industry:
  - telecom
domain_objects:
  - cdr_batch
  - batch_manifest
  - expected_batch_schedule
  - delivery_completeness
  - record_disposition
  - subscriber_day_usage
  - usage_restatement
works_with:
  platforms:
    - duckdb_local
    - motherduck
    - fabric_lakehouse
    - fabric_warehouse
    - redshift
  tools:
    - dlt
    - dbt
qualifiers:
  - Assessed end to end on duckdb_local only; other listed targets rely on dlt and dbt support and are unassessed.
  - Needs a Studio route for dlt to read the drop; cloud buckets (ADLS, S3) have none today.
  - Needs each batch to arrive with a manifest stating its declared record count, or the batch cannot be judged.
  - Needs a source of expected batches; a batch neither expected nor delivered cannot be seen.
  - Covers delimited text batches such as CSV; other layouts are out of scope.
  - Stops at subscriber-day usage; rating, billing, churn, ARPU, fraud and network quality are separate work.
  - Landing controls for layout, rescans and part-way failure follow file-drop-to-bronze.
  - A generic file drop with no usage rollup belongs to file-drop-to-bronze.
related:
  - file-drop-to-bronze
  - business-event-fact
  - customer-retention-churn-features
evidence:
  features:
    - add-or-update-source
    - generating-dlt-pipeline
    - generating-dbt-model
    - verifying
  evals: []
---

## Prompt

Land the call-detail record batches from <cdr_drop_location>, with the manifest delivered beside each batch and the expected batches from <expected_batch_source>, then publish usage per <subscriber_identifier> and usage day. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Report every expected batch and every delivery against its manifest's declared count, state for every day whether it rests on complete batches so an incomplete batch never reads as a quiet day, and count each landed record once, set it aside as a duplicate, or set it aside with its approved reason so the counts add back to the records landed. Show how a late batch changes a day already reported, leave a rerun with no new input unchanged, and report what the checks cannot prove.

## Verified by

- Landing keeps every delivered record and manifest as delivered, merging and removing nothing, so a re-sent batch's records stay present as evidence for the duplicate rule.
- Each expected batch reports its declared count, received count and signed difference with a status under the approved completeness rule; a batch with no delivery, a file with no manifest, a manifest with no file, an over-count and an unexpected batch each get that rule's status, never complete.
- A re-delivery of an already-received batch is flagged as one and affects the batch verdict and day backing as the approved rule says; the report says what it cannot see, such as a batch neither expected nor delivered.
- Every landed record has exactly one disposition, applied in the approved order: counted, duplicate, or set aside with its approved reason (unusable, or outside the approved scope); the three add back to the records landed with no residue, and each set-aside record keeps its reason.
- Each subscriber-day's measures recompute exactly from its own counted records under the approved day, unit and rounding rules, and every counted record sits in one subscriber-day unless an approved split sums back to the record.
- A call crossing midnight and a call whose local day differs from its UTC day each land on the day the approved day rule gives, using the approved reporting zone.
- Every subscriber-day states whether its day is fully backed under the approved backing rule; a subscriber with no counted records on a day not fully backed reads as the approved rule shows it, always marked not fully backed and never as a backed zero.
- A repeated record id is handled as the approved duplicate rule says, and a repeat whose values differ is flagged rather than silently dropped or counted twice.
- A late batch changes reported days only as the approved rule says, each change showing previous and new usage and backing, and usage it does not restate appears in its approved adjustment, never lost.
- Changes are compared with the last successfully published state; a failed run does not move that state or hide the next restatement, the first run reports none, and a rerun with no new input leaves every figure unchanged.
- Published figures, verdicts and backing match expected results derived independently from the delivered files, including each approved policy branch and the awkward cases present in the delivered files.
- Changing an approved rule value, such as the reporting zone, a subscriber list or a reason list, moves the figures with no code change, within the approved rule form.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain and sources. Inspect the delivered batches, manifests, the expected-batch source and any subscriber or test-number reference, and profile the awkward cases before modelling: re-sends, short and over-count batches, files without manifests, calls across midnight and zone boundaries, bad subscriber, time or duration values. Use Ask first only for semantics the approved requirements leave open, and record each answer as this Intent's policy, not a default. Land the batches append-only with a delivery order, judge each delivery against its own manifest, then derive the expected-batch verdicts, record dispositions, day backing and the subscriber-day grid, and keep rule values as data. Build independent expected results from the delivered files before comparing the output, replay deliveries with a build between them to show a restatement, and read every output back. Landing controls for layout, encoding, malformed rows, rescans and part-way failure follow file-drop-to-bronze's contract. Where a re-send cannot be paired with its own manifest, say so. Record what was not exercised.

### Compose

- add-or-update-source
- generating-dlt-pipeline
- generating-dbt-model
- applying-medallion-data-modelling
- verifying

### Ask first

- Which zone do source timestamps carry, which reporting zone and day own a record, is a record ever split, and how are daylight-saving days and skewed switch clocks handled?
- Whose usage is reported (originating, terminating, forwarded, roaming or interconnect legs), which record types count, and who may see subscriber-level rows?
- Which measures and units are required, do switches report different units, and is any rounding or per-type rule approved?
- Where does the expected set come from, when is a batch due or missing, how is a file paired with its manifest, what makes it complete (count, checksum, sequence), and how are over-count, no manifest, an unexpected batch and re-delivery treated?
- What makes two records the same, which instance counts, and how are differing repeats, reversals and partial records of one call treated?
- Which records are unusable or excluded (no subscriber, test, unknown, unreadable time, non-positive duration), in what order, what is a known subscriber, and who owns a ported or reused number on a date?
- When is a day fully backed, which subscribers and days appear when there is no usage, and how is an unbacked day with no records shown?
- How does a late batch change a reported day (restate or adjust later), how is it shown, where is prior state kept, and what does a failed run publish?

### Guardrails

- Do not de-duplicate, filter or merge records at landing; a duplicate and an unusable record are evidence to report, not rows to remove.
- Do not report a short, over-count, missing or unpaired batch as complete, and do not show a day resting on one as a quiet day or as a backed zero.
- Do not derive the expected set only from what arrived; a batch that never arrived has to be visible, and the report states what it cannot see.
- Do not pair a re-sent file with a manifest by assumption; report a delivery that cannot be paired with the approved status, never complete.
- Do not let a later duplicate silently replace the counted record, and do not split, round or reassign days unless the approved rule says so.
- Do not drop a record that cannot be placed; give it a disposition and a reason, and keep the counts reconciled to the records landed.
- Do not hard-code the reporting zone, subscriber lists, test numbers or reason and status lists in code; keep them as data.
- Take reported days and due batches from the approved expected set and as-of rule, never implicitly from the run clock.
- Do not rate or bill usage, or compute churn, ARPU, fraud or network quality; those are separate work.
- Label synthetic data as synthetic and never land it in a shared Domain relation or claim an unseen batch is absent.
