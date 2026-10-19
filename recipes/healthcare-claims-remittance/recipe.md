---
id: healthcare-claims-remittance
title: Reconcile billed claims to payer remittances and denials by payer
trigger:
  - The revenue cycle team matches payer remittances to billed claims by hand, and nobody can say, payer by payer, how much of what was billed was paid, adjusted, denied or is still open.
  - A payer's denial rate or top denial reasons are quoted from a spreadsheet that mixes claim-level and line-level amounts, counts a resent remittance twice or reads patient responsibility as a denial.
  - A remittance batch does not match the payment it carries, a remittance names a claim nobody holds, or a billed claim has no remittance yet, and the gap is found only at month end.
description: Explain every billed claim line as paid, adjusted, patient responsibility, denied or open so the pieces add up to the billed amount, summarise the same by payer with denial rate and denial reasons, account for every remittance line as applied or set aside with its reason, and tie each remittance batch to its payment.
pitch: Billed to paid, adjusted, denied and open for every claim line and payer, with every remittance line applied or explained.
job_category: build
area: transformation
readiness: supported
industry:
  - healthcare
domain_objects:
  - claim
  - claim_line
  - remittance_line
  - remittance_batch
  - reason_code_map
  - payer_summary
  - set_aside_remittance_line
  - completeness_check
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
  - Claims, remittance lines, batch payments and reason-code rules must already be landed as tables.
  - Stops at the reconciliation; appeals, resubmission, underpayment checks, patient billing and bank matching are separate.
  - Only as complete as the remittances received; claims not yet remitted are shown as approved.
related:
  - finance-gl-subledger-tieout
  - finance-duplicate-invoice-detection
  - finance-ar-aging-dso
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

Build <claim_line_reconciliation>, <claim_reconciliation>, <payer_summary>, <remittance_line_coverage> and <batch_tieout> from <billed_claims>, <remittance_lines>, <remittance_batch_payments> and <reason_code_rules>. Inherit the semantics the Intent or its approved requirements already establish, and resolve with the user only the semantics they leave open. At the approved grains, explain each billed amount, with a code the rules do not place kept visible, as paid, contractual adjustment, patient responsibility, denied, any other approved class, and open, so the pieces add up to the billed amount, publish the same by payer with the approved denial rate and denial reasons, account for every remittance line as applied to a claim line or set aside with its reason, and set each remittance batch beside the payment it carries. Keep the denial and adjustment classes and the reason-code rules as data the user can change. Publish what the inputs cannot prove.

## Verified by

- At each published grain, the pieces of every row plus any residue shown add up to its billed amount; a claim with no remittance appears as the approved rule says.
- On a run that completes, every input remittance line is either applied to a claim line or set aside with its approved reason, and the applied plus set-aside amounts equal the input total.
- A remittance line the approved rules cannot link to a claim, line or payer is set aside with its approved identifying keys, amount and reason, never attached elsewhere; claims left out of scope stay visible with their reason.
- A resent line is not paid twice under the approved duplicate rule, the line of record follows it and each set-aside copy names the line it duplicates; several remittances on one claim combine as approved, and a negative amount reduces paid.
- A line paid above its billed amount shows the excess as the approved rule says, and a code the approved rules do not place lands where they say, visible and never silently classed; the pieces still add up to the billed amount.
- The class of an amount comes from the approved reason-code rules and not from the payer's own label; changing a rule changes the published pieces with no change to the logic.
- Where the approved rule spreads a claim-level remittance over the claim's lines, the shares sum exactly to the remitted amount, each spread row is marked and the claim-level original stays visible.
- The payer summary has one row per approved payer, with a payer seen only in remittances shown as approved; its pieces equal the sum over its claims, and its denial rate follows the approved definition and is empty, not zero, where nothing was billed.
- The denial reasons and amounts on the payer summary equal the ranking recomputed independently from the published breakdown by payer and reason code.
- Each remittance batch shows its carried payment, the approved sum of its amounts and the difference; a difference follows the approved disposition and changes no claim's pieces.
- The pieces, payer rows and batch differences equal figures derived independently from the inputs, and each tie back to the input totals (billed, remitted, batch payments) is published with its residue, zero except an explained break.
- Each output is unique on its declared grain with required fields populated, and each row traces to the claim lines and remittance lines behind it; the outcome states what is set aside, which batches do not tie, which claims have no remittance and what the inputs cannot prove.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and every semantic decision its approved requirements already record; do not ask the user to confirm them again. Profile the billed claims (payers, claim and service-line keys, dates, amounts, currencies), the remittance lines (the grain each carries, payer, batch, claim, line, amounts by kind, reason codes, received time and repeats), the batch payments and the reason-code rules. Use Ask first only for semantics still open, and record each decision as the user's own answer. Keep the classes, the reason-code rules, the set-aside reasons and the spreading and rounding rule explicit and editable where the approved requirements say so. Derive independent expected results from the inputs by hand before reading any output. The claim and line outputs, the payer summary, the coverage and the batch tie-out must never disagree about a remittance line. Publish every remittance left set aside, every batch that does not tie and what the inputs cannot prove.

### Compose

- capturing-requirements
- profiling-source-data
- applying-medallion-data-modelling
- generating-dbt-model
- dbt-unit-testing
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which payers (including one seen only in remittances), periods and currencies are in scope, which date places a claim in a period, how are corrected, replacement, voided or resubmitted claim versions treated, and are excluded claims shown with a reason?
- If unresolved, which classes divide a billed amount, how does a rule map a code to a class (by reason code and adjustment group, per payer or global, with what default), is there a class for other adjustments, and where does a code the rules do not place go?
- If unresolved, how are several remittances on one claim combined, what makes a line a resend, which copy is the line of record, and how are a reversal, a correction, a recovery and a replacement treated?
- If unresolved, how is a remittance that names a claim but no service line attributed to the claim's lines, spread by what weight and rounding, or kept at claim grain?
- If unresolved, how is open defined, and how are a claim with no remittance yet and a line paid above its billed amount shown, signed and flagged or limited?
- If unresolved, which remittance lines are set aside rather than applied (unknown claim or line, another payer including a secondary payer under coordination of benefits), under which reasons, and at which grain is each reported?
- If unresolved, how is denial rate defined (by amount, line count or claim count), how many top denial reasons are published, ranked by what, and how are ties broken?
- If unresolved, which amounts count toward a batch total (including provider-level adjustments, interest and withholds), is a resent line counted once, and does a difference fail the run or only flag?

### Guardrails

- Do not choose classes, reason-code rules, resend and combination rules, the spreading rule, the open definition, the denial-rate definition, the set-aside reasons or the batch total for the user, and take none from the data or common practice; the user may ask for alternatives or a recommendation.
- Never mix claim-level and line-level amounts at one grain; when a claim-level amount is spread, keep the original and mark the spread.
- Never drop or double count a remittance line; every line that cannot be applied stays visible with its reason.
- Never clamp, floor or absorb a difference to make a row tie unless the approved rule says so; an overpayment, an unmapped amount and an untied batch stay visible.
- Never classify an amount by the payer's label when the approved reason-code rules say otherwise, and never place an unknown code in a class the approved rules do not give it.
- Never attach a remittance to a claim, line or payer the approved rules do not link it to.
- Never publish a patient identifier or name in a reconciliation output unless the approved requirements require it.
- Stop at the reconciliation: do not appeal, resubmit, rework or write back to the claims or remittance sources, which stay read-only.
