---
id: finance-gross-margin-variance-bridge
title: Explain gross-margin change with a reconciled price, volume, mix, and cost bridge
trigger:
  - Finance subtracts one period's gross margin from another and writes the explanation by hand, and the story changes with whoever builds it.
  - Price, volume, mix and cost effects do not add up to the margin change, or an unlabelled line absorbs the difference.
  - New products, discontinued products, returns or a zero base quantity distort the volume and mix effect and nobody can see by how much.
description: Explain the gross-margin change between two comparable periods under the user's approved method as price, unit cost, volume, mix, new, discontinued and no-quantity components that add up to the observed change exactly, with any rounding shown and every line left out accounted for.
pitch: Show why gross margin moved between two periods, with every component adding up to the change and nothing hidden in a plug.
job_category: build
area: transformation
readiness: supported
function:
  - finance
domain_objects:
  - gross_margin
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
  - Needs sales lines with quantity, revenue and cost for two comparable periods.
  - Takes revenue and cost as given; cost assignment and allocation are separate outcomes.
  - Keeps each currency and unit of measure separate unless an approved rule applies.
  - Explains a change between two periods; plan versus actual and forecasting are separate.
  - Stops at the bridge; commentary, charts and repricing advice are separate outcomes.
related:
  - finance-budget-forecast-actual
  - order-return-contribution-margin
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

Build <bridge_model>, <bridge_total_model>, <exceptions_model> and <coverage_model> from <sales_line_source> for the margin-change questions in this Intent. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only the semantics they leave open. For the two approved periods, place each in-scope sales line at the approved grain, value margin as the approved rules define it, classify each cell as continuing, new, discontinued or without quantity under the approved rule, and split its margin change into the approved price, unit cost, volume and mix components plus new, discontinued and no-quantity components, with the price and cost interaction assigned as approved, so that the components and any named rounding remainder equal the observed change exactly at the approved precision. Total the rows and recompute the total change independently. List every line that cannot be placed or falls outside the approved periods or scope with its reason and amount, and reconcile placed, set-aside and outside lines to the input by count, revenue and cost. Keep sources read-only. Report what the inputs cannot prove.

## Verified by

- On a run that completes, each row's components plus its rounding remainder equal its observed margin change exactly at the approved precision; the remainder sits where the approved rule puts it, within the approved bound, and is never hidden inside a component.
- Components equal values worked out independently of the model for each agreed case: a price-only case lands in price alone, a cost-only case in unit cost alone, a quantity-only case in volume and mix with price and cost at zero, and a mixed case follows the approved interaction rule.
- Volume and mix are measured against the approved benchmark; new and discontinued cells stay out of it unless the approved rule says otherwise, and where the benchmark cannot be measured they read as the approved rule says.
- A cell with no sales in one period, a zero base quantity, or sales and returns that net to zero follows the approved classification; new, discontinued and no-quantity amounts are explicit components, never folded into volume or mix.
- No rate is divided by a zero or undefined quantity: a zero base never yields an infinite or zero price effect, and the cell reads as the approved classification with its reason.
- A return or credit note is treated as the approved rule says and is never read as a price or cost change unless that rule says so.
- The total's components equal the sum of its rows, its change equals the sum of the row changes and an independent comparison margin less base margin, and any total remainder equals the sum of the row remainders.
- Every input line is placed once, set aside with its reason and amount, or listed as outside the approved periods or scope; placed, set-aside and outside counts, revenue and cost equal the input, with any difference shown.
- A missing, null or malformed cost or amount is listed with its reason and never read as zero cost or zero revenue; a cell touched by a set-aside line is flagged as the approved rule says.
- Currencies, units of measure and entities are never netted together unless an approved translation or conversion rule is stated; otherwise each reconciles on its own.
- The periods compared are exactly the approved ones, and a difference in their length stays in the components or is normalised as the approved rule says, never silently.
- Where the approved rule fails a run, or a bridge that cannot close, the output names each offending line or row and publishes no figures, or flags them; each output is unique on its declared grain and states what the inputs cannot prove.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile the sales lines (periods, products, customers, quantities, prices, costs, currencies, units, returns, lines with an amount but no quantity, null costs) before modelling. Use Ask first only for semantics still open, and record each decision as the user's own answer. Keep the periods, benchmark, precision and bound, and the reason lists editable as data where the approved requirements say so. Work out expected results for the agreed cases independently of the models, from the source lines, before trusting them, including the cases an example does not carry, check that each row and the total close, and say which paths the example did not exercise.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, how is gross margin defined (which revenue and cost lines count, such as discounts, rebates, freight, fees and landed cost), which currency and unit of measure are the basis, and are lines in another currency or unit set aside or translated under approved rates and factors?
- If unresolved, which two periods are compared, how are their length and calendar handled (equal shape required, a length difference left in the components or normalised), and where do sales dated outside both periods go?
- If unresolved, at what grain is the bridge built (product, customer, segment or a pair), which roll-ups are published, and which records are in scope (intercompany, samples, free goods, test or statistical lines)?
- If unresolved, at what quantity are price and unit cost valued (comparison, base or the midpoint), and does the price and quantity interaction go into price and cost, into volume or into its own component?
- If unresolved, how are volume and mix separated (a book-wide average margin, an average within a customer or other group, by quantity or by revenue, over which cells), and what do volume and mix read when no benchmark can be measured?
- If unresolved, how is a cell classified when one side has no sales, a zero quantity, or sales and returns that net to zero, how are new, discontinued and no-quantity amounts shown, and are returns and credit notes negative quantity or separate?
- If unresolved, what precision applies, is each component rounded on its own, where does any rounding remainder go (a named remainder or an approved component), and what bound is allowed?
- If unresolved, which lines can't be placed (missing cost, unknown key, another currency or unit, malformed amounts), is each set aside and flagged on its cell, excluded from both periods or does the run fail, and should a bridge that cannot close fail, publish flagged or publish nothing?

### Guardrails

- Do not choose the margin definition, basis, periods, grain, valuation quantity, interaction, benchmark, classification, return treatment, precision or exception handling for the user, or take them from the data, a reporting tool or common practice; the user may ask for options or a recommendation.
- Never absorb a difference in a component or an unlabelled line so the bridge closes; a remainder is shown where the approved rule puts it.
- Never read a missing cost as zero cost or a line with revenue and no cost as full margin.
- Never fold new, discontinued or no-quantity amounts into volume or mix unless the approved rule says so.
- Never net two currencies, units of measure or entities into one figure unless an approved rule and rate or factor say so.
- Never drop, double count or silently net away a sales line or an amount; lines left out stay visible with their reasons.
- Never default the compared periods or their length treatment without approval.
- Stop at the bridge: do not compare with plan, forecast, reprice, recommend, or write commentary or charts.
