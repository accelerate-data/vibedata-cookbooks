---
id: marketing-contact-pressure-eligibility
title: Build cross-channel contact-pressure and send-eligibility decisions for planned contacts
trigger:
  - The same person is emailed, texted and pushed by several tools in one week, and nobody can say whether the next planned contact is allowed.
  - One delivery reported by two tools is counted twice, or a contact exactly at the edge of the rolling window is counted differently in each report.
  - Two contacts planned for one person at the same moment are ordered by load order, so a different one wins each run.
  - A planned contact has no consent record or no identifiable person, and it is sent or silently dropped with no reason.
description: Decide, for each planned contact at a reporting cutoff, whether it is included or suppressed under the user's approved caps, window, priority and consent rules, with one reason, the contacts already used against each cap, its rank where ranked, and every input row accounted for.
pitch: One auditable send-eligibility table that counts each delivery once, ranks competing contacts the same way every run and says why a contact was held back.
job_category: build
area: transformation
readiness: supported
function:
  - revops
domain_objects:
  - customer
  - planned_contact
  - contact_event
  - channel
  - purpose
  - contact_cap
  - eligibility_decision
  - suppression_reason
  - contact_exception
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
  - Needs planned contacts, reported contact events with times, an identifier-to-person map and a published consent state.
  - Takes consent state and person identity as given; consent derivation and identity resolution are separate outcomes.
  - Publishes eligibility data only; sending, scheduling, quiet hours and journey logic are separate.
  - Gives no legal advice; caps and consent rules are the user's, not a compliance finding.
  - A source with no event-time field stops the run; a row with a missing time follows the approved rule.
related:
  - customer-consent-preferences
  - identity-golden-record-crosswalk
  - effective-dated-business-rules
  - source-freshness-sla
  - pii-classification-and-masking
evidence:
  features:
    - capturing-requirements
    - generating-dbt-model
    - verifying
  evals: []
---

## Prompt

Build <eligibility_model>, <set_aside_model> and <coverage_model> from <planned_contact_source>, <contact_event_source>, <identifier_map_source> and <consent_state_source> for the send-eligibility questions in this Intent. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only the semantics they leave open. For each planned contact at the approved reporting cutoff, count the contacts the person already used under the approved rules with each delivery counted once however many tools report it, rank competing contacts for one person by the approved order, and publish included or suppressed with one reason in the approved order, the contacts used and the room left under each approved cap, the rank where ranked, and the consent verdict where it decided. Set aside every input row that counts nowhere with its reason, reconcile every count to the inputs, and report what the inputs cannot prove. Publish eligibility only: send nothing, decide no consent, resolve no identity.

## Verified by

- Every planned contact has exactly one decision per reporting cutoff, included or suppressed; a suppressed one carries one reason in the approved order and an included one none; rows equal the planned contacts in scope, and none is dropped or duplicated.
- One delivery reported by two tools counts as one contact under the approved delivery key and a conflict between reports is shown; a bounce, an unmapped status or an unreadable event counts only as the approved rule says.
- Contacts used within the window equal a recount from the events under the approved window and edge rules, including a contact at the window edge and one at the planned instant, with what a planned contact or a send counts as following the approved rule.
- A cutoff uses only what the approved time basis lets it see: a later-received report changes that cutoff only if the approved as-known or restated rule allows, a source with no received time reports restatement unproven, and unchanged inputs give the same decisions.
- Caps and windows come from approved rules, each cap with its own window; a plan with no room under an applicable cap is suppressed, with cap reached as its reason when no earlier approved reason applies; changing an approved value changes decisions as the approved rule form allows.
- Contacts for one person are ranked by the approved order; a same-instant tie follows the approved tie-break, rank reproduces from the stated keys regardless of input row order, and plans use up room in rank order where the approved rule lets them.
- An exempt purpose is never blocked by a cap and uses room only as the approved rule says; its deliveries are accounted for as their own class, never as a set-aside error.
- A person with no consent record, a channel without consent coverage, an opt-out, an identifier with no or several owners and an unreadable planned row each follow the approved treatment, with a named reason when suppressed or set aside; none is guessed or dropped.
- Consent and identity are read as given: no verdict is derived, no person is merged or guessed, a person key shows only where the identifier resolves to one owner under the approved rule, and contact values follow the approved protection.
- Every planned row, event and identifier-map row is decided, used, counted in its own approved class (such as exempt deliveries) or set aside with one reason; a plan outside the approved scope is shown or counted with its reason, and counts foot to the inputs with zero residue.
- Results equal values worked out independently of the models for each applicable case the approved rules create, such as a delivery reported twice, a window-edge contact, a same-instant pair, a person at the cap and no consent record; an inapplicable case is stated.
- Where decisions are published the checks above hold; where the approved rule fails or holds a run on missing or stale inputs it names each offending input and publishes none or flags them; an included decision never claims no unreported contact exists, and what the inputs cannot prove is stated.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile the planned contacts (channels, purposes, identifiers, instants, duplicate plan ids, unreadable rows), the contact events (tools, statuses and their frequency, delivery keys reported by several tools, event and received times with time zones, rows with no usable time), the identifier map (unowned and shared identifiers, merged people) and the consent state's coverage before modelling. Use Ask first only for semantics still open, and record each decision as the user's own answer. Keep caps, window, priority order, status meanings and reason order editable as data where the approved requirements say so. Work out expected decisions for the agreed cases and cutoffs independently of the models, check that every count reconciles to the inputs, and say which paths the example did not exercise, such as several windows, caps per purpose or overlapping consent states.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which people and planned contacts are in scope (internal, test, held out), what are the caps (per person across channels, per channel, per purpose, campaign, journey or brand), and which purposes count against them or are exempt?
- If unresolved, is the window rolling or a calendar period, how long is each cap's window, is the far edge inclusive, does a contact at the planned instant count, which time orders events, what time zone applies, and where does the cutoff come from?
- If unresolved, is each cutoff as known then or restated by later reports, which inputs (caps, status meanings, identifier map, plans) are versioned, and what do rows with no received or event time become?
- If unresolved, what counts as one planned contact (duplicate, cancelled, rescheduled, already reported), what consumes room (plan, send, delivery, attempt), how do bounced and unmapped events count, and do included or exempt plans use room?
- If unresolved, what makes two reports one delivery (message id, person, channel, time), which report wins when they disagree, what do events with no key become, and how is a tool with no feed shown?
- If unresolved, how are competing contacts for one person ordered (planned instant, channel precedence, campaign priority), what breaks a same-instant tie, and do suppressed plans keep their rank or use room?
- If unresolved, which consent state and as-of date are read, what do no record, an uncovered channel and a lapsed permission mean, may another channel's consent speak for it, and what follows an identifier with no or several owners or a merged person?
- If unresolved, in which order do reasons apply when several fit, what does an unreadable planned row become, who may read the decisions, in what protected form are contact values published, and should a run on stale inputs fail, flag or hold?

### Guardrails

- Do not choose the caps, window and its edge, what consumes room, delivery key, priority order, tie-break, consent reading, identity treatment, reason order or disclosure for the user, or take them from the data, a vendor default or common practice; the user may ask for a recommendation.
- Never count one delivery twice under the approved delivery key, order contacts by load or row order, or let a report change a cutoff beyond what the approved as-known or restated rule allows.
- Never treat a missing consent record, a channel without consent coverage or an unresolved identity as permission unless an approved rule says so for that case, and never let a cap or rank loosen an opt-out.
- Never drop an input row or a planned contact without a named reason, guess a person for an identifier the approved rule leaves unresolved, or read a missing time as zero.
- Never publish raw email addresses, phone numbers or device handles beyond the approved audience, and never describe a hash of a guessable contact value as anonymisation.
- Never default the reporting cutoff to the run clock without approval.
- Stop at eligibility data: do not send or schedule a contact, collect or decide consent, resolve or merge identities, or push decisions into sending tools.
