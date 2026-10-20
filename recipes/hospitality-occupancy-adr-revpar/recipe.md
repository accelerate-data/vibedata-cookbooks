---
id: hospitality-occupancy-adr-revpar
title: Build nightly occupancy, ADR and RevPAR by property with closed-night restatements
trigger:
  - Occupancy, ADR and RevPAR differ between reports because each one counts stays, comps, out-of-order rooms and cancellations its own way.
  - A multi-night stay lands on its check-in day, the checkout day is counted as a night, or a month's ADR is an average of daily ADRs.
  - A reservation amended after a night closed quietly changes a morning figure that revenue management already acted on.
description: Publish rooms available, sold and occupied, room revenue, occupancy, ADR and RevPAR per property and night from reservation lines and room inventory, with every line counted or set aside with a reason and amendments to closed nights handled visibly as approved.
pitch: One nightly table of occupancy, ADR and RevPAR that reconciles to every reservation line and rolls up from sums.
job_category: build
area: transformation
readiness: supported
industry:
  - hospitality
domain_objects:
  - property
  - reservation_line
  - room_inventory
  - stay_night
  - rooms_available
  - rooms_sold
  - room_revenue
  - occupancy
  - adr
  - revpar
  - night_close
  - restatement
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
  - Needs reservation lines with a nightly rate and a room inventory per property and night already landed as tables.
  - Stops at the nightly table; forecasting, pace, comp-set index, channel mix and profit measures are separate work.
  - Judging a later amendment needs a close per night, from the source or an approved rule.
related:
  - shared-calendar-fiscal-periods
  - metric-population-and-rollups
  - business-event-fact
  - metricflow-semantic-model
  - shared-fx-conversion
evidence:
  features:
    - capturing-requirements
    - profiling-source-data
    - generating-dbt-model
    - running-dbt-in-sandbox
    - verifying
  evals: []
---

## Prompt

Build <nightly_kpi_model> with one row per property and night from <reservation_lines> and <room_inventory>, so revenue management and property owners read occupancy, ADR and RevPAR that agree at a night and at any week or month. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Count a stay on every night slept and never on its checkout day, publish rooms available, sold and occupied, room revenue, occupancy, ADR and RevPAR under the approved rules for comp and house-use rooms, out-of-order rooms, cancellations, no-shows, taxes and fees, and nights with nothing sold or available, and recompute any period's ratios from summed components. Count each reservation line once or set it aside with one approved reason so counts and revenue tie back to the lines landed, show how an amendment after a night closed is restated or adjusted as approved, and report what the checks cannot prove.

## Verified by

- The table holds exactly one row per property and night under the approved population rule, keys unique and not null, and the row count equals the count of property-nights that rule names.
- A stay counts on every night from check-in through the night before check-out and never on its checkout day, including a stay that crosses a week or month boundary.
- Rooms available follow the approved out-of-order rule, the out-of-order count is published beside them where the source carries it, and a night with every room out of order reads as the approved rule shows, not as a missing row.
- Comp and house-use rooms enter rooms sold, rooms occupied and room revenue as the approved rule says, each published as its own count, and the approved ratio bases are stated.
- Room revenue is the approved nightly amount per counted room and night, in one approved currency, holds only the amounts the approved rule names as room revenue with every other amount kept apart, and a rate that changes mid-stay is taken per night.
- Occupancy, ADR and RevPAR recompute from the published components each night, a zero denominator reads as the approved value and never an unstated zero, and a week or month ratio divides summed components, never averaged nightly ratios.
- Lines whose status the approved rules exclude, and any line they call unusable, are set aside once each with their reason and appear in no count or revenue figure; any fee on them goes where the approved rule says.
- A stayed night with no inventory row, a night where occupied rooms exceed available rooms, and a reservation delivered twice are each handled as approved and visible, never silently dropped, capped or double counted.
- Every reservation line is counted or set aside exactly once, any stayed night set aside is listed with its reason, and counts add back to the lines landed with rooms and revenue tying to the counted nights and no residue.
- An amendment after its night's close is handled as the approved rule says, restated with previous and new figures or posted as an approved adjustment, never silently rewritten; with no kept published state or amendment dates, the change is reported as unproven.
- Published figures, set-asides and restatements match expected results derived independently from the delivered lines, including each approved policy branch and the awkward cases present in the data.
- Changing an approved rule value, such as the set-aside reasons or a close date, moves the figures with no code change, within the approved rule form.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain and sources. Inspect the reservation lines, rate fields, room inventory, any close or amendment records and the calendar, and profile the awkward cases before modelling: multi-night and boundary-crossing stays, comp and house-use rooms, cancellations and no-shows, out-of-order rooms, unknown properties, unreadable dates, zero-night stays, negative rates, repeated lines and nights with no inventory. Use Ask first only for semantics the approved requirements leave open, and record each answer as this Intent's policy, not a default. Decide each line's disposition before expanding it to nights, expand to nights from the approved calendar, join inventory by property and night, and keep rule values as data. Build independent expected results from the delivered lines before comparing the output, replay an amendment before and after a close to show a restatement, and read every output back. Record what was not exercised.

### Compose

- capturing-requirements
- profiling-source-data
- generating-dbt-model
- running-dbt-in-sandbox
- verifying

### Ask first

- Is a night the property's night-audit date in its local zone or the calendar date, does the table cover every inventory property-night or every calendar night, and how is a night with no inventory shown?
- Which rooms are available (physical less out-of-order, or as recorded), and how are long-term, day-use and permanently closed rooms treated?
- How do comp and house-use rooms count in rooms sold, rooms occupied, revenue, ADR and occupancy, is a line one room or a room count, and how are sharers and room moves counted?
- Which statuses count (tentative, waitlist, guaranteed, unpicked group block), what are cancelled, no-show and early-departure lines worth, is departure booked or actual, and is any fee room revenue?
- Which amounts are room revenue (rate before tax, service charge, resort fee, packages, incidentals) and in which currency, and is conversion needed?
- Which properties are in scope (test, closed, managed), which lines are unusable (unknown property, unreadable or backwards dates, zero nights, negative rate) and in what order, and what makes two lines the same reservation and which counts?
- When does a night close, what happens to a reservation amended afterwards, and where is the published state kept so a restatement can show previous and new figures?
- Which ratios read null or zero when nothing was sold or available, how is an over-capacity night shown, and which week and calendar do the roll-ups use?

### Guardrails

- Do not count a stay on its check-in day only, and do not count the checkout day as a night.
- Do not average nightly occupancy, ADR or RevPAR to a period; recompute from summed components.
- Do not show a zero denominator as zero unless the approved rule says so, and state the rule beside the figure.
- Do not include tax, service charge, fees or incidentals in room revenue unless the approved rule says so.
- Do not let a comp, house-use, cancelled or no-show room dilute ADR or enter sold counts unless the approved rule says so.
- Do not silently rewrite a closed night when a reservation changes; restate or adjust as approved, and report an unprovable change as unproven.
- Do not drop, cap or silently correct a line or night that cannot be placed or exceeds capacity; give it a reason and keep the counts reconciled.
- Do not hard-code approved rule values such as set-aside reasons or close dates in code; keep them as editable data.
- Do not forecast, compute pace or comp-set index, or report channel mix or profit; those are separate work.
- Label synthetic data as synthetic and never land it in a shared Domain relation.
