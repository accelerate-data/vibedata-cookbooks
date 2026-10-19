---
id: customer-consent-preferences
title: Unify consent and communication preferences with auditable latest-wins logic
trigger:
  - A customer who opted out in one system still gets messages from another, because each source says something different and whichever job ran last wins.
  - Nobody can say why a customer is or is not contactable, which event decided it, or what their state was on a past date.
  - Opt-outs, complaints and STOP replies arrive from several sources and nobody can show which one a decision rests on.
description: Build one contact-permission state per customer, channel and purpose from consent events across sources under the user's approved ordering, scope and no-record rules, with the deciding event, a suppression list and the full event history, and every event applied or set aside with its reasons.
pitch: One auditable answer to whether a customer may be contacted, with the deciding event and a suppression list that never loosens an opt-out.
job_category: build
area: governance-cost
readiness: supported
domain_objects:
  - customer
  - consent_event
  - channel
  - purpose
  - consent_state
  - lawful_basis
  - suppression_entry
  - decision_trace
  - consent_exception
works_with:
  platforms:
    - duckdb_local
    - motherduck
    - fabric_lakehouse
    - fabric_warehouse
    - redshift
  tools:
    - dbt
qualifiers:
  - Assessed end to end on duckdb_local only; the other listed targets rely on dbt support and are unassessed.
  - Needs consent events already landed as tables with source, status, event time, received time and identifier.
  - Takes the customer key and identifier mapping as given; matching and merging customers are separate outcomes.
  - Shows permission to contact only; contact frequency, pressure and send eligibility are separate outcomes.
  - Carries the lawful basis the user approves; deciding lawful basis or regional law is not part of it.
  - Publishes tables only; syncing the state or suppression list into sending tools is a separate outcome.
  - Cannot prove consent given outside the delivered feeds, or a state as known on a past date without received times kept.
related:
  - identity-golden-record-crosswalk
  - effective-dated-business-rules
  - pii-classification-and-masking
  - source-freshness-sla
  - file-drop-to-bronze
evidence:
  features:
    - capturing-requirements
    - profiling-source-data
    - applying-medallion-data-modelling
    - generating-dbt-model
    - dbt-unit-testing
    - running-dbt-in-sandbox
    - verifying
  evals: []
---

## Prompt

Build <consent_state_model>, <suppression_list_model>, <event_history_model>, <decision_trace_model> and <accounting_model> from <consent_sources> on <customer_key>. Inherit the Intent's sources, platform, mapping from source identifiers to the customer key and approved requirements, and settle with the user only the consent semantics they leave open. Normalise each source's events to a permission, an opt-out or another approved effect on an approved channel and purpose scope, order them under the approved clock, and publish one current result per customer, channel and purpose with its basis where the approved scheme has one, the event that decided it and the event it overrode, a suppression list that also holds opt-outs for identifiers matching no customer, the full event history and a trace of every candidate event, with every event applied or set aside with its reasons and the state recomputable for any supplied as-of date, and report what the inputs cannot prove.

## Verified by

- Every event row has one disposition (applied to a cell, superseded everywhere, duplicate, set aside with each reason, or corrected or erased under the approved rule); counts equal input rows per source, the trace holds per-cell outcomes, and an unreadable row is named, never guessed or dropped.
- Every customer in scope has one current-state row per approved channel and purpose, including customers with no events, showing a result, the basis where the scheme has one, the deciding event and the event it overrides where one exists; customers outside scope stay listed with their reason.
- Each cell's deciding event is the one the approved clock, supersession and tie rules select, derived independently from the inputs; ordering never follows load order, an event the clock places after the as-of changes nothing at it, and a tie names the rule that broke it.
- An event changes exactly the cells its approved channel and purpose scope names, wildcard words such as STOP-all or a global unsubscribe included, and leaves every other cell as it was; an event whose status or scope has no approved meaning changes no cell and is listed.
- A cell with nothing on record shows the approved result as its own state, distinct from an opt-out and from an identifier suppression; a lapsed permission shows the approved state naming it and its expiry, and an opt-out ends only as the approved supersession rule or its status meaning allows.
- A cell that reads as permitted shows the approved basis where the scheme has one, and never reads as permitted from a source whose coverage does not reach the as-of, a channel no source declares, or an unreadable event, unless the approved rule says otherwise.
- The suppression list holds, per opted-out cell, every identifier the approved identifier rule covers for the customer, plus each opt-out matching no customer; no permitted cell has a covering row except under that rule, a cell only partly covered shows so, and an unmatched permission lifts nothing.
- Where customers merged, each event keeps the identifier it arrived under, the combined result follows the approved merge rule, no opt-out on either customer is lost without the rule naming the superseding permission, and a past as-of follows the approved mapping basis.
- Each source's and channel's supplied coverage is published; a source behind the as-of or a channel with none declared is shown, a stale source never loosens an opt-out, and where the approved rule fails or holds the run it names the sources and events and publishes nothing held as current.
- The result at any supplied as-of date equals an independent recomputation from the kept events and the rule data under the approved rule-version basis, and a rerun on unchanged inputs and rules changes no recorded decision; the as-of is an input, defaulting to the run clock only if approved.
- Changing an approved rule held as data, such as precedence, the scope of a status word, a lifetime or a source's coverage, changes the results for the dates the approved rule-version basis applies it to, without changing the logic, within the approved rule form.
- No published relation carries a raw email address, phone number or postal address beyond the approved audience, and the outcome states what the inputs cannot prove, such as consent given outside the delivered feeds or when a fact became known.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile each source first (status words and their frequency, how an identifier is written, event and received times with their time zones and precision, duplicates, redeliveries, rows with no usable time, identifiers that match no customer or several, merged customers, and the dates each source starts and stops covering), then settle with the user only what is still open and record each decision as the user's own answer. Keep the status meanings, scope map, precedence, lifetime, coverage, normalisation and as-of date as editable data where the approved requirements say so. Derive each case's expected result independently of the models before comparing: a tie, a late arrival, a wildcard against a later specific event, a pending status, an expired permission, a timed opt-out, a merged pair, a shared identifier, an unmatched opt-out, a correction and a stale source. Say which paths the example did not exercise.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which customers are in scope (internal, test, minors, guest, merged), how are identifiers normalised, what happens to an unmatched opt-out or permission, and does an opt-out cover all a customer's identifiers of a kind or only the one it arrived on, shared or reassigned ones included?
- If unresolved, which channels and purposes are published, which identifier kinds each channel uses, whether any lawful basis applies and, if so, which for each purpose and where it comes from, and are service purposes treated differently from marketing and research?
- If unresolved, which time orders events (the person's act or the time received), what time zone and precision apply, how are late, date-only, duplicate and redelivered events and the as-of date handled, what breaks a tie, and do past dates use the rules then in force?
- If unresolved, what does each status word mean (permission, opt-out, pending confirmation or no effect, and which channels and purposes it covers), can a pending state, opt-out or pause end by itself, and what happens to a status or scope no rule maps?
- If unresolved, what does nothing on record mean for each purpose (and customer region where schemes differ), does a permission expire after how long and what restarts it, and what state does a lapsed permission show?
- If unresolved, can a later permission supersede an earlier opt-out, for one customer or after a merge, and under what conditions, how do merged customers combine, does a past as-of use the mapping then or now, and what does a later-matched suppressed identifier carry over?
- If unresolved, what coverage and cadence does each source have, what does a source behind the as-of or an unreadable event do to cells that would read as permitted, and should a run with missing or stale inputs fail, publish flagged results or hold them?
- If unresolved, who may read the state, the suppression list and the history, in what protected form are contact values published, how long are events kept, and how are corrections, retractions and erasure requests handled?

### Guardrails

- Do not choose the ordering clock, tie rule, status meanings, scope map, no-record result, lifetime, merge rule, coverage and failure rules or disclosure for the user, and take none from the data, a vendor default or common practice; the user may ask for a recommendation.
- Never let a stale, missing, unreadable or unmatched piece of evidence loosen an opt-out, and never drop an opt-out because its identifier maps to no customer.
- Never order events by load or run order, and never apply an event the approved clock places after the as-of date.
- Never let a wildcard or an unnamed scope change a cell outside its approved scope, and never guess the meaning of a status or scope no approved rule maps.
- Never treat nothing on record as a permission or as an opt-out unless the approved rule says so for that purpose; show it as its own state.
- Never publish raw email addresses, phone numbers or postal addresses beyond the approved audience, and never describe a hash of a guessable contact value as anonymisation.
- Never overwrite history except as the approved correction and erasure rule allows, never let a redaction or erasure loosen an opt-out, and never let a rerun on unchanged inputs and rules change a recorded decision.
- Never let a merge or an identifier correction silently drop or resurrect a suppression.
- Stop at the state, the suppression list, the history and the trace: do not collect consent, decide lawful basis or regional law, resolve or merge customers, apply contact frequency or send eligibility rules, or push the list into sending tools.
