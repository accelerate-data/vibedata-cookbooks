---
id: sales-quote-order-price-reconciliation
title: Reconcile accepted quote versions to orders and invoices with a price-exception ledger
trigger:
  - Sales and Finance disagree about the price a customer was promised, and someone reconciles quotes to orders and invoices by hand.
  - A quote was revised, and an order or invoice may be priced from a version the customer never accepted.
  - A quoted line was split across orders, bundled, substituted or ordered in another unit, and nobody can show that quantity and value still add back to the quote.
description: For each accepted quote line, trace the orders and invoice lines that came from it, add quantity and value back to the quote, and publish a ledger of every price that departs from the approved price with its amount and source records.
pitch: Show what became of each accepted quote and every price that departs from the approved one, with no approval inferred from the invoice.
job_category: build
area: transformation
readiness: supported
function:
  - revops
  - finance
domain_objects:
  - sales_quote
  - quote_version
  - quote_line
  - price_approval
  - product_unit_mapping
  - order_line
  - invoice_line
  - price_exception
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
  - Needs quote versions, order lines tied to quote lines and invoice lines tied to orders, or an approved linking rule.
  - Stops at lineage and price exceptions; it does not recommend prices or approvals, or tie bookings to cash.
related:
  - revops-bookings-billings-cash
  - effective-dated-business-rules
  - order-return-contribution-margin
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

Build <lineage_model>, <reconciliation_model>, <exceptions_model> and <coverage_model> from <quote_source>, <approval_source>, <product_mapping_source>, <order_source> and <invoice_source>. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only the semantics they leave open. Identify the accepted version of each quote, take the approved price from it alone, and trace each accepted quote line to its order lines and invoice lines. Per accepted quote line, add quoted, ordered and invoiced quantity and value back to the quote with the open remainder or over-order shown, and publish a ledger of every ordered or invoiced price that departs from the approved price, with signed amount and source records. List every record that cannot be placed, with its reason. Keep sources read-only and report what the inputs cannot prove.

## Verified by

- On a run that completes, every quote version, quote line, order line and invoice line lands in exactly one disposition: reconciled, excepted with a reason, or out of scope with a reason, and counts foot to the inputs.
- Every approved price traces to the approved accepted version of its quote. Any other version never sets a price, whatever its number or date, and an order citing one follows the approved handling, shows the version it cited and is not priced from it.
- A discount counts as approved only to the extent an approval record covers it, and the uncovered excess is shown as its own exception. A discount exactly at its cap and one with no approval record are each handled as approved.
- No approval is inferred from an ordered or invoiced price. On a run that completes, each price departure is a ledger row with signed amount, approved and measured price, quantity and the source records that show it.
- Each published price comparison (ordered or invoiced against approved, invoiced against ordered) is a separate finding, none netted, merged or summed across, and a discount the approval covers raises none.
- Per accepted quote line, quoted quantity equals ordered plus open remainder less any over-order, and value at the approved price adds back the same way. A split line adds back exactly, and a price gap is shown as variance, never as an open remainder.
- A bundle is counted once and its components follow the approved pricing. A substitution or unit conversion counts only through an approved mapping or factor, and a missing one is an exception that adds nothing to totals.
- Order lines with no quote reference, a currency other than the quote's, or an unavailable factor follow the approved handling, stay visible with reason and own amount, and are never attributed to a guessed quote line. No amount converts between currencies unless approved.
- Expected lineage and ledger rows are derived independently from the sources and approved rules, and published results equal them, including each boundary and adverse case the approved rules allow.
- Each output is unique on its declared grain, and a rerun on unchanged inputs gives identical results.
- The outcome states which exceptions and open remainders remain and what the inputs cannot prove.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask again. Profile the quote versions, approvals, product mappings, order lines and invoice lines: keys, versions, statuses, units, currencies, dates and which references the sources actually carry. Use Ask first only for semantics still open, and record each answer as the user's own decision. Keep rules such as approval caps, tolerances, unit factors and bundle or substitution mappings as editable data where the approved requirements say so. Resolve the accepted version before pricing, attribute only through stated references and mappings, and keep the lineage, reconciliation, exception and coverage outputs agreeing about every record. Write expected rows by hand from the sources and approved rules before any model, including the boundary cases, and compare published rows with them in both directions. Report every exception left open and what the inputs cannot prove.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which quotes, customers, statuses, entities, order and invoice lines and dates are in scope, is the result as of a date, and are the records left out listed with their reason?
- If unresolved, what makes a quote version the accepted one (a status, an acceptance record, an effective date), which wins when several were accepted, do quote expiry or the order date relative to acceptance matter, and what happens to an order citing another version?
- If unresolved, what is the approved price (quoted, list less approved discount, net of what discounts), what does an approval cover and how is a cap stated, and which tolerance and rounding apply?
- If unresolved, what ties an order line to a quote line and an invoice line to an order line, may one order span several quotes, and what happens to a missing, unknown or conflicting reference?
- If unresolved, how are bundles priced and quantified, which substitutions are allowed and by what mapping, and which unit factors apply to a quantity and a price?
- If unresolved, how are partial, split, over-ordered, cancelled and amended quantities shown, and what counts as an open remainder or an over-order?
- If unresolved, which currencies are compared, is any conversion approved and under which rates, and are tax, freight and rebates inside or outside the compared price?
- If unresolved, which price comparisons are published, in what sign and order, and does an exception stay visible or fail the run?

### Guardrails

- Do not choose the accepted version, approval coverage, tolerance, population, linking, bundle, substitution or unit rules for the user, and take none from the data or common practice; the user may ask for alternatives or a recommendation.
- Never infer an approval, an accepted version or a quote link from the price that was ordered or invoiced, or match on product, customer or amount alone unless the approved rules say so.
- Never price from a version other than the approved accepted one, and never let a later version number or creation date decide acceptance unless the approved rule says so.
- Never default a missing factor, approval, price or reference to a convenient value unless an approved rule defines it; an unknown stays visible with its reason.
- Never net or convert across currencies, units or entities because they share a quote or customer; convert only under approved rates and factors.
- Never drop, double count, clamp or merge an amount: a split, bundle or substitution adds back exactly, an over-order stays visible, and findings are not summed across comparisons.
- Stop at lineage and price exceptions: do not recommend a price, discount or approval, tie bookings to billings or cash, or change the sources.
