---
id: finance-gross-margin-variance-bridge
title: Explain gross-margin change with a reconciled price, volume, mix, and cost bridge
trigger:
  - Finance subtracts one period's gross margin from another and writes the explanation by hand, and the story changes with whoever builds it.
  - Price, volume, mix and cost effects do not add up to the margin change, or an unlabelled line absorbs the difference.
  - New products, discontinued products, returns or a zero base quantity distort the volume and mix effect and nobody can see by how much.
description: Explain the gross-margin change between two periods under the user's approved method as price, unit cost, volume and mix components plus any new, discontinued, no-quantity, interaction, translation or period-length components the approved rules define, closing to the observed change with any rounding shown and every line left out accounted for.
pitch: Show why gross margin moved between two periods, with every component adding up to the change when it closes and nothing hidden in a plug.
job_category: build
area: transformation
readiness: supported
function:
  - finance
domain_objects:
  - gross_margin
  - sales_line
  - product
  - customer
  - margin_bridge
  - price_effect
  - unit_cost_effect
  - volume_effect
  - mix_effect
  - new_product
  - discontinued_product
  - rounding_remainder
  - bridge_exception
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
  - Needs sales lines for two comparable periods; lines lacking quantity or cost follow the approved disposition.
  - Takes line revenue and cost as given; allocating shared charges to lines is a separate outcome.
  - Keeps each currency and unit of measure separate unless an approved rule applies.
  - Explains a change between two periods; plan versus actual and forecasting are separate.
  - Needs dated line, rate and mapping versions to prove a restatement; without them it reads unproven.
  - Stops at the bridge; commentary, charts and repricing advice are separate outcomes.
related:
  - finance-budget-forecast-actual
  - order-return-contribution-margin
  - shift-unit-economics
  - shared-calendar-fiscal-periods
  - shared-fx-conversion
evidence:
  features:
    - capturing-requirements
    - generating-dbt-model
    - verifying
  evals: []
---

## Prompt

Build <bridge_model>, <bridge_total_model>, <exceptions_model> and <coverage_model> from <sales_line_source> for this Intent's margin-change questions. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only the semantics they leave open. For the two approved periods, place each in-scope sales line at the approved grain, currency, unit and entity, value margin as approved, classify each cell as continuing, new, discontinued or without quantity under the approved rule, and split its margin change into the approved price, unit cost, volume and mix components plus any new, discontinued, no-quantity, interaction, translation or period-length components the approved rules define, so that, on a run that closes, the components and any approved rounding remainder equal the observed change exactly at the approved precision. Total the rows and recompute the total independently. List every line that cannot be placed with its reason and amount, show or count lines outside the approved periods or scope as approved, and reconcile all lines to the input by count, revenue and cost. Keep sources read-only. Report what the inputs cannot prove.

## Verified by

- Where a row closes within the approved bound, its components plus its rounding remainder equal its observed margin change exactly at the approved precision and rounding point; the remainder appears where the approved rule puts it, with its amount, never as an unlabelled plug.
- Components equal values worked out independently of the model for each agreed case: price-only lands in price alone, cost-only in unit cost alone, quantity-only in volume and mix (price and cost zero unless an approved translation moves them), mixed per the approved interaction rule.
- Volume and mix are measured against the approved benchmark; new and discontinued cells stay out of it unless the approved rule says otherwise, and where the benchmark cannot be measured they read as the approved rule says.
- A cell with no sales in one period, a zero base quantity or netted sales and returns follows the approved classification, and no rate is divided by zero; new, discontinued and no-quantity amounts are shown as approved, separately identifiable, never folded into volume or mix unless approved.
- A return or credit note is valued and shown as the approved rule says; a return priced differently from its sale moves price or unit cost only as that rule says.
- Where the total closes within the approved bound it equals the placed rows' components and remainders and, over placed lines, an independent comparison margin less base margin; set-aside margin shows beside it where computable, and a roll-up holds each member once, never summed across levels.
- On a run that completes, every input line is placed once, set aside with its reason and amount, or shown or counted as outside the approved periods or scope, and counts, revenue and cost equal the input; a missing, null or malformed cost or amount is listed, never read as zero unless approved.
- Currencies, units and entities are never netted unless an approved translation, conversion or consolidation rule is stated; each reconciles on its own, is bridged separately or is set aside with its reason, and a translation effect appears as the approved rule says, never silently as price or cost.
- The periods compared are exactly the approved ones and each line sits in the period the approved date basis gives it; a difference in length follows the approved rule (kept in the components, normalised, or the run rejected or flagged), never silently.
- A cell whose product matches across the two periods under the approved rule and grain is never also new or discontinued; each unmatched product follows the approved classification, and a renamed, merged or split product is not reported as a false new-plus-discontinued pair.
- A late or backdated posting, or a changed amount on a valued line (credit, rebate, cost revision), follows the approved time basis; a change the rule does not restate appears as its own labelled movement, and a source without dated versions reports restatement as unproven.
- Where a bridge does not close within the approved bound and the approved rule publishes it, the gap amount and reason stay visible and closure reads failed or unverified for that row or total, never passed; otherwise the run fails or publishes nothing, naming each offending line or row.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile the sales lines (periods, products, customers, quantities, prices, costs, currencies, units, returns, lines with an amount but no quantity, null costs) before modelling. Use Ask first only for semantics still open, and record each decision as the user's own answer. Keep the periods, benchmark, precision and bound, and the reason lists editable as data where the approved requirements say so. Work out expected results for the agreed cases independently of the models, from the source lines, before trusting them, including the cases an example does not carry, check that each row and the total close, and say which paths the example did not exercise.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, how is gross margin defined (which revenue and cost lines count, such as discounts, rebates, freight, fees and landed cost), and which records are in scope (intercompany, samples, free goods, test or statistical lines)?
- If unresolved, which currency, unit of measure and legal entity are the basis, are lines in another one set aside, bridged separately, or translated, converted or consolidated under approved rates and factors, and is a translation effect its own component?
- If unresolved, which two periods are compared and how are length and calendar handled, which date places a line in a period, is the time basis as known or restated, how does a late posting or changed amount reach published figures, and are lines outside both shown or counted?
- If unresolved, at what grain is the bridge built (product, customer, segment or a pair), how is a product matched across periods (renames, merges, splits, bundles), are roll-ups summed from pairs or recomputed, and how is a customer in several groups shared?
- If unresolved, at what quantity are price and unit cost valued (comparison, base or midpoint), where does any remaining interaction with quantity go, and how are volume and mix separated (which benchmark, period and cells)?
- If unresolved, how is a cell classified when one side has no sales, a zero quantity, or netted sales and returns, how are new, discontinued and no-quantity amounts shown, and are returns negative quantity or separate, at their own price or the sale's?
- If unresolved, what precision applies, is each component rounded on its own, where does any rounding remainder go (a named line or an approved component), and what bound is allowed?
- If unresolved, which lines can't be placed (missing cost, unknown key, malformed amounts), are they set aside and flagged, excluded or does the run fail, and should a bridge that cannot close fail, publish flagged or publish nothing?

### Guardrails

- Do not choose the margin definition, basis, periods, grain, valuation quantity, interaction, benchmark, classification, return treatment, precision or exception handling for the user, or take them from the data, a reporting tool or common practice; the user may ask for options or a recommendation.
- Never absorb a difference in an unlabelled line or an unapproved component so the bridge closes; a remainder is shown where the approved rule puts it.
- Never read a missing cost as zero cost or a line with revenue and no cost as full margin, unless the approved rule says so.
- Never fold new, discontinued or no-quantity amounts into volume or mix unless the approved rule says so.
- Never net two currencies, units of measure or entities into one figure unless an approved rule and rate or factor say so.
- Never drop, double count or silently net away a sales line or an amount; lines left out stay visible with their reasons.
- Never treat a renamed, merged or split product as new plus discontinued, or default the compared periods, date basis or length treatment, without approval.
- Stop at the bridge: do not compare with plan, forecast, reprice, recommend, or write commentary or charts.
