# Modelling Recipes: approved materialization plan and execution tracker

**Batch ID:** `2026-09-28-modelling-recipes`
**Decision status:** Approved by SS on 2026-09-28. Execute; do not restart requirements discovery.
**Execution status at this checkpoint:** In execution. See the batch tracker and Codex checkpoint below; the original planning baseline is historical.
**Repository:** `accelerate-data/vibedata-cookbooks` (the only repository writable for this work).
**Target branch:** `pre-prod`. Promotion to `main` is outside scope.
**Plan path:** `docs/plans/2026-09-28-modelling-recipes-materialization.md`.
**Linear project:** [Content - Recipes](https://linear.app/acceleratedata/project/content-recipes-fb2483d9868a/overview), team `GTM`.
**Owner:** SS. Resolve the current Linear account before writing; do not infer the owner from the executing account.

This is the complete handoff for a new ChatGPT session using connected GitHub and Linear tools, plus ChatGPT's temporary container. It is also the running plan and tracker. It replaces a Linear project document. The new session must prepare the issue batch and then execute it, not return another proposal.

## 1. Objective and meaning of completion

Materialize reusable Vibedata Recipes that prompt engineers to settle modelling semantics before producing plausible but unsupported analytical outputs. Cover business-event grain, duplicate handling, metric populations and rollups, relationship provenance, usable history, operational state durations, availability, unit economics and effective-dated rules.

Write requirements that apply across data platforms. A motivating Fabric example does not make the outcomes Fabric-specific. Do not require NYC taxi data, specific source counts, fixed dates or a particular customer's policies.

A Recipe is a requirement-sized outcome with a concrete deliverable, an observable acceptance contract and execution guidance. It is not a small SQL operation, a general tutorial or a bundle of unrelated deliverables. A Collection is a non-executable discovery view. Every Recipe must prove its own result; it must not require a second Recipe simply for verification.

**This batch authors Recipe definitions. It does not execute the Recipes against customer/test warehouses or create new runtime evaluation infrastructure.** The future Recipe executor must inspect the Intent, ask about genuinely unresolved semantics, implement the agreed outcome and run the checks described in the Recipe.

A Recipe materialization/change ticket is Done only when all of these are true:

1. Its full approved content scope is implemented and substantively reviewed.
2. Current capability evidence supports execution of the complete outcome on at least one declared platform. Each Recipe in a grouped change ticket must pass this condition.
3. The repository's generator and required checks pass, including required PR CI for the actual head being merged.
4. Its PR is merged into `pre-prod`, and the required post-merge checks pass for the merge result.
5. Linear contains the canonical Recipe link, PR, tested head/merge SHAs, CI evidence, readiness rationale and an accurate completion comment. The local tracker is updated.

Done means materialized and verified in `pre-prod`, not published on `main` and not runtime-proven. Apply this batch-specific completion rule in the issues; do not change the project's general description or workflow.

If no supported platform can be established, do not merge a `planned` definition during this batch. Keep authored work on its branch or draft PR, leave the ticket unfinished, document the blocker, assign/notify SS and continue independent work. Distinguish a known missing capability from insufficient evidence. Neither is a supported compatibility claim.

## 2. Authorized actions and strict boundaries

SS has approved the scope, issue preparation, sequential execution, PR creation, CI repair within scope, merges to `pre-prod`, status updates and blocker handling. Do not seek repeated approval for these actions. This authorization does not override tool permissions, branch protections or additional platform confirmation requirements.

### Allowed

- Read and update the approved existing Linear candidates; create or reuse the approved new issues in this project.
- Assign every batch issue to SS. Create new issues in Backlog; use Todo when selected and In Progress when authoring starts.
- Use connected GitHub and Linear tools for remote operations. Use a temporary local copy of this repository for structured edits, the existing generator and tests.
- Create a fresh branch and PR per ticket from the latest verified `pre-prod`. Merge only after the required checks and content review pass.
- Modify the scoped `recipes/<id>/recipe.md` files, the two approved Collections, generated `catalog.json`, this plan and directly necessary cookbook documentation or additive tests.
- Make an initial plan-only PR if this plan has not already landed. Include checkpoints in content PRs. Make a final tracker-only PR when needed. These are not additional Linear tickets.
- Use a corrective branch/PR under the same ticket if a defect attributable to that work is found after merge.
- Inspect other repositories read-only to substantiate capability claims. Keep their private content out of public artifacts.

### Not allowed

- Write to any repository other than `accelerate-data/vibedata-cookbooks`, including through local checkouts, remote tools or delegated work.
- Modify Studio, plugins, product implementations, websites, infrastructure or customer data. Do not use the user's Mac or Ubuntu server.
- Change Recipe/Collection/catalog schemas, schema versions, validators, generator behaviour, CI workflows, branch protections, dependency pins or security settings to make this batch pass.
- Disable, skip or weaken checks; lower acceptance criteria merely to obtain green CI; invent compatibility, evaluations or evidence.
- Push directly to `pre-prod` or `main`, promote to `main`, force-push shared branches, dismiss required reviews or bypass protections.
- Create new project documents, statuses, labels, cycles, milestones, deadlines, estimates, extra Recipe candidates or out-of-project capability tickets.
- Publish the original engineer comparison, personal details, private source excerpts, customer examples, credentials or tokens in the public repository or PRs.

No new milestone or cycle is required for this batch. Preserve existing issue metadata not explicitly changed by this plan, including provenance, priority, labels, links and discussion. New issues have no priority, cycle, milestone, estimate or due date. Existing completed/in-progress work discovered on resume must be reconciled, not reset mechanically to Backlog.

## 3. Sources and preflight

### Source precedence

User-approved decisions in this plan define scope and authorization. Live repository contracts define valid artifact shape. Linear owns candidate lifecycle; canonical Recipe files own materialized definitions. The GTM seed catalog is historical context, not the current registry. When current facts conflict materially with the approved scope, record the conflict and block that item rather than changing scope silently.

Read before editing:

- This plan, its tracker and any linked execution comments/PRs.
- Repository `README.md`, `CONTRIBUTING.md`, `templates/recipe.md`, all three files under `schema/`, `.github/workflows/ci.yml`, and the relevant files under `docs/adr/`.
- Current `catalog.json`, `recipes/`, `collections/` and relevant tests/scripts.
- The actual Linear project, GTM statuses, SS account, approved existing issues and their comments/relations.
- [Cookbook model](https://github.com/accelerate-data/vibedata-gtm/tree/main/docs/gtm/plan/04-demand-inbound/cookbook), especially its README and Feature/Recipe boundary. Read only.
- Relevant current implementation/capability evidence in [Studio](https://github.com/accelerate-data/studio) and [data-engineering capabilities](https://github.com/accelerate-data/vibedata-data-engineering), as needed. Read only; discover paths rather than inventing them.

Planning baseline, not a substitute for refresh: `pre-prod` was inspected at `8ba32b65344c36dc63463f5144f52fccb8fef227`. It contained four materialized Recipes: incremental dbt conversion, API-to-bronze ingestion, Fabric pipeline authoring and MotherDuck scheduling. GTM-187, GTM-241 and GTM-243 existed as backlog candidates. Recheck all of this at execution time.

### Environment preflight

Discover available connected tool actions before declaring them unavailable. Verify read/write access to the cookbook repository and the selected Linear project. Resolve actual IDs; retain them locally. Verify tools for creating branches/files/PRs, inspecting workflows/jobs/logs, merging with an expected head SHA, and updating/commenting on Linear issues.

Inspect the repository's scripts before running them. Verify that the temporary container can run Python, its pinned dependencies, tests and the existing catalog generator. Do not assume the container has network access or GitHub credentials merely because the connector works.

Use a normal temporary checkout when available. If direct Git/network access is unavailable, retrieve repository files through the GitHub connector at a pinned commit and reconstruct the required local snapshot from those exact bytes. Verify the manifest and blob hashes; do not substitute snippets, missing files or hand-written implementations. For a Git-dependent check, fetch sufficient source/history through supported tools or let unchanged remote CI perform that check, explicitly recording which local checks did not run. Never report an unrun check as passed. Catalog generation must actually run; do not construct `catalog.json` manually.

All persistent GitHub writes must still use the connector. A local snapshot need not have remote credentials. If the generator or required dependencies cannot run through the permitted environment, treat that as a tooling blocker. Continue only work that does not depend on that prerequisite.

Read paginated results completely using returned cursors/pages. A partial or truncated tool response is not proof that a file, issue, check or failure does not exist.

### Support and readiness evidence

Keep each new Recipe's business requirement platform-neutral. Use platform-specific details only for compatibility or real execution differences. Preserve an essential technique such as dbt snapshots rather than renaming it as a generic capability.

At planning time, allowed execution targets were `duckdb_local`, `motherduck`, `fabric_lakehouse`, `fabric_warehouse` and `redshift`. Refresh the schema, but do not add targets or schemas. Consider all current relevant targets; do not stop discovery simply because the motivating example used Fabric. Declare only those supported by complete evidence. One supported target is sufficient for completion.

For each Recipe, record the required operations, current Feature/Skill implementation references, source revision, supported target(s), restrictions and unresolved gaps in Linear. Link evidence at a precise revision. Do not infer Vibedata support solely because an engine can express the SQL. Do not cite the Recipe being authored as proof of its own availability.

Use `supported` where current capabilities establish end-to-end executability without a dedicated Recipe evaluation. Use `proven` only with an existing qualifying evaluation for the exact shape and targets; identify it. A schema-valid string in `Compose` is not evidence that a capability exists. A generic SQL Feature may implement several steps, but its scope must actually cover them. Unknown runtime support must remain unknown.

## 4. Approved batch and order

There are **11 logical work items**: update three existing candidates, create six new candidates, create one combined change issue for two materialized Recipes, and create one Collection issue. Normally this means eight new Linear issues and three updated issues. Reuse matching work discovered at execution time rather than forcing duplicate issue counts.

| Order | Key | Linear action | Canonical identity / outcome |
| --- | --- | --- | --- |
| 1 | B01 | Create or reuse | `business-event-fact` - business-event fact and auditable duplicate handling |
| 2 | B02 | Create or reuse | `metric-population-and-rollups` - metric eligibility and reconcilable aggregation |
| 3 | B03 | Create or reuse | `event-resource-attribution` - auditable event-to-person/asset attribution |
| 4 | B04 | Update GTM-187 | `dbt-snapshot-history` - useful history and historical consumption |
| 5 | B05 | Create or reuse | `operational-state-duration` - location-aware operational state durations |
| 6 | B06 | Update GTM-241 | `logistics-fleet-utilization` - explicit availability and utilisation rules |
| 7 | B07 | Create or reuse | `shift-unit-economics` - shift revenue, cost, margin and rollups |
| 8 | B08 | Create or reuse | `effective-dated-business-rules` - historical rates and applicability |
| 9 | B09 | Update GTM-243 | `prove-dbt-change-safe` - independent assurance of an existing change |
| 10 | B10 | One new combined change issue | Strengthen `dbt-full-refresh-to-incremental` and `api-to-bronze-incremental-contract` |
| 11 | B11 | One new Collection issue | General modelling Collection and logistics/fleet Collection |

This yields nine newly materialized Recipe definitions, changes to two existing definitions, and two Collections if all work is supported and completed. It does not change the other materialized orchestration Recipes.

The order is a useful progression, not an automatic blocking graph. A Recipe's source/model prerequisites are not a requirement that another Recipe be invoked first. Define its own verification. Keep B01-B10 independently authorable where possible. Omit optional `related` links to definitions that do not yet exist. B11 depends on its specified member definitions being present in `pre-prod`.

Out of scope: GTM-245 / destination migration; GTM-223 / sessionization funnels; extra logistics outcomes; standalone Recipes for a lookup join, adding one test, choosing a key, enriching a weather table, adding an already-specified ratio, or creating a convenience mart. Use their relevant Features within the approved outcomes.

## 5. Common authoring contract

For every Recipe:

- Use a literal deliverable title and recognisable engineer situations in `trigger`, not only technique names.
- Write the bounded task in `Prompt`, observable future execution results in `Verified by`, and the approach in `Agent guidance`.
- Inherit the existing Intent's repository, platform, Domain and sources. Do not ask the user to restate known context.
- Inspect approved requirements and source evidence first. Put only unresolved semantic decisions in `Ask first`. Do not silently infer business intent from sample values or from convenient existing code.
- Ask which analytical questions and breakdowns are actually required. Missing Reference-style features are not universally mandatory. Expose missing attributes, history, mappings or relationship evidence that prevent the agreed question from being answered.
- Distinguish observed source relationships, approved allocations and synthetic examples. An internally consistent synthetic fixture is permitted; presenting an invented relationship as an observed operational fact is not.
- Define at least one discriminating case: an example where an attractive but incorrect implementation fails. Specify expected results independently of the implementation being tested.
- Preserve source-to-output traceability and reconcile counts/amounts where relevant. Expose unmapped, ambiguous, excluded and unknown cases. Never discard materially distinct data to satisfy a test.
- Keep domain-specific acceptance where it materially changes grain, policies, inputs or outputs. Add logistics triggers to generic Recipes without restricting all generic discovery to logistics.
- Compose real supported Features/Skills. Follow current schema, section order, length limits and formatting. Do not add a new artifact type, fixture directory or runtime evaluation framework.

Tests and scenarios below are **required future Recipe-execution evidence**. Materialization must encode them, not claim to have run them. The ticket's authoring acceptance is that these requirements are accurately represented, supported by current capabilities, content-reviewed and repository-validated.

## 6. Per-item specifications

The title, problem, outcome, semantic questions, future proof and exclusions in each section are the approved issue specification. Put product-level scope in Linear; keep implementation sequencing here. For existing candidates preserve their provenance and discussion and add the strengthened contract. Source references and canonical deliverable links belong in the issue for traceability.

### B01 - Build a business-event fact with auditable duplicate handling

**Identity:** `business-event-fact`. **Category/area:** `build` / `transformation`. **Treatment:** new candidate.

**Problem and outcome:** A loader row can be mistaken for a real business event. Deliver an agreed event-grain fact, a defensible identity rule, traceability to source records, and explicit treatment of duplicate deliveries, conflicts and exceptions.

**Recognition:** Combining transaction feeds, replaying deliveries, counting unique events, or building a trip/consignment fact.

**Question to surface:** Does one row mean one business event or one source delivery? What makes two otherwise similar events distinct? How should corrections and conflicting versions be resolved?

**Required scope:** Establish grain and source identity evidence; distinguish exact redelivery, business duplicates, valid similar events and conflicting records; apply an approved deterministic disposition; retain lineage and expose unresolved cases. Validate relevant reference mappings without inventing their meaning.

**Future proof:** Repeated delivery does not add an event. Two genuinely distinct similar events remain distinct. Conflicting versions follow the approved rule or remain explicit exceptions. Source rows reconcile to events and all other dispositions. Additive amounts reconcile, and unknown reference codes are visible rather than silently dropped.

**Boundaries:** Not customer/entity golden-record resolution. Do not demand deduplication at bronze for every source. Do not invent a natural key merely to make uniqueness pass. Source semantics that permit repeats must remain valid.

### B02 - Build a metric with explicit eligibility and reconcilable rollups

**Identity:** `metric-population-and-rollups`. **Category/area:** `build` / `transformation`. **Treatment:** new candidate.

**Problem and outcome:** A correct formula over the wrong population can produce a misleading metric. Deliver an implemented metric with defined eligibility, components, missing-value treatment, weighting and valid aggregation grains.

**Recognition:** Adding a percentage, rate or average; reconciling daily/monthly metrics; measuring trip tips, occupancy or service rates.

**Question to surface:** Who is eligible? Is an unobserved value zero, excluded or unknown? What should a zero denominator mean? Which dimensions and higher-grain totals must reconcile?

**Required scope:** Define numerator, denominator, eligibility, unknown/unmeasurable cases, weighting and supported rollups. Retain calculation components. Validate eligibility mappings and dimension coverage. State additive/non-additive restrictions rather than claiming every metric aggregates in the same way.

**Future proof:** An independently specified small example verifies inclusion and exclusion. An unknown/unobserved case distinguishes absence from zero. Unequal group sizes expose inappropriate averaging of rates. Requested rollups reconcile to the approved calculation from underlying components. Zero denominators follow the explicit policy.

**Boundaries:** Do not mandate ratio-of-sums for metrics whose approved definition requires something else. A fully specified simple ratio remains a Feature, not a new Recipe. Missing optional analytical breakdowns are reported, not invented.

### B03 - Attribute events to people and assets through auditable relationships

**Identity:** `event-resource-attribution`. **Category/area:** `build` / `transformation`. **Treatment:** new candidate.

**Problem and outcome:** A deterministic possible match is not necessarily a factual assignment. Deliver an attribution model with provenance, valid relationship cardinality, temporal applicability and explicit unresolved cases.

**Recognition:** Reporting event revenue or productivity by employee, driver, asset, vehicle, team or garage.

**Question to surface:** What establishes responsibility for the event? Is there an observed assignment source, an explicitly modelled synthetic relationship, or an approved allocation policy? How are ambiguous/unmatched events treated?

**Required scope:** Inspect source-of-truth assignments; establish keys, cardinality and applicable times; prevent join fan-out; separate observed assignments from estimates/allocations; preserve lineage and unresolved relationships. Allow approved allocation only when labelled and governed by explicit rules.

**Future proof:** Each assignment is traceable. Ambiguous and unmatched events stay visible. Counts and additive amounts reconcile through joins. Applicable temporal assignments are selected correctly. Approved many-to-many allocation conserves the required totals. A deterministic arbitrary hash cannot masquerade as observed assignment.

**Boundaries:** Do not fabricate attribution to enable rankings or economic outputs. Synthetic examples remain permitted when explicitly synthetic and internally consistent. Do not mutate source operational systems.

### B04 - Add history to a slowly changing dimension and prove historical use

**Identity:** `dbt-snapshot-history`. **Existing issue:** [GTM-187](https://linear.app/acceleratedata/issue/GTM-187). **Category/area:** retain `build` / `transformation` unless the live candidate contains a justified equivalent.

**Problem and outcome:** Snapshot/as-of syntax is not useful proof when no record changes. Strengthen the existing candidate to deliver recorded history with correct, demonstrated historical consumption, not merely snapshot creation.

**Recognition:** A master attribute changes and historical events need an agreed classification; changes in customer, asset, vendor or zone attributes.

**Question to surface:** Preserve the historical classification or restate history? Which attributes change? Does validity refer to source effective time or observation time? What are the approved boundary, late-change and deletion policies where relevant?

**Required scope:** Establish dimension identity and historical policy, capture history with supported dbt snapshot behaviour, and specify how a consuming fact selects its version. Do not imply that snapshots of present-state data can reconstruct unknown past history.

**Future proof:** A controlled entity actually changes between versions. Facts before, exactly at and after the change resolve to expected versions. A current-row join and an incorrect boundary rule fail at least one test. The historical join does not multiply fact rows. Unchanged reruns do not generate spurious versions. Overlaps/gaps are surfaced under the agreed policy.

**Boundaries:** Keep snapshot history as this existing candidate. Do not create a second SCD2-testing Recipe or bundle an unrelated full fact warehouse into it. Retain exact platform support rather than assuming all dbt adapters support the same behaviour.

### B05 - Build location-aware state durations from operational events

**Identity:** `operational-state-duration`. **Category/area:** `build` / `transformation`. **Treatment:** new candidate.

**Problem and outcome:** State intervals without location evidence cannot answer where an entity was in a state. Deliver durations by entity, state, applicable location and agreed time grain, with explicit unknown periods.

**Recognition:** Measuring waiting, idle, available or busy time by site/zone and hour; reconstructing operational state from event histories.

**Question to surface:** Do events describe state changes, location changes, or both? What establishes interval ends? How should unknown gaps, equal timestamps and open-ended intervals be handled? What time zone/reporting boundaries apply?

**Required scope:** Establish event meaning and ordered identity; carry state and location only as evidence permits; build intervals; split them across required reporting boundaries; handle missing closes and observation gaps explicitly. Separate operational evidence from synthetic demonstration patterns.

**Future proof:** Include a location change without a state change, a state change without a location change, an hour/day boundary crossing, a missing close and an unobserved gap. Durations reconcile at required grains without duplication. Unknown gaps are not automatically idle/available, and missing locations are not invented.

**Boundaries:** This is not GTM-223's product-session/funnel outcome. Do not replace missing spatial data with a convenient garage/site and call the result zone-level. Do not create streaming infrastructure.

### B06 - Build fleet utilisation from explicit availability rules

**Identity:** `logistics-fleet-utilization`. **Existing issue:** [GTM-241](https://linear.app/acceleratedata/issue/GTM-241). **Category/area:** `build` / `transformation`; logistics context is intentional.

**Problem and outcome:** Occupancy while observed and utilisation against available asset time are different measures. Strengthen the existing candidate to implement utilisation with explicit availability, downtime and rollup semantics.

**Recognition:** Fleet capacity, vehicle utilisation, maintenance-adjusted availability, or a dashboard containing ambiguous utilisation rates.

**Question to surface:** Utilisation of which resource, over which available time? Do calendar, rostered, online and observed time differ? What removes an asset from availability? How are maintenance intervals and missing observations handled?

**Required scope:** Separate driver occupancy, asset utilisation and availability when relevant. Establish an authoritative asset/time denominator, operational observation coverage and maintenance downtime policy. Handle interval overlaps/reporting boundaries and distinguish missing maintenance evidence from zero downtime.

**Future proof:** Contrast an available but never-online asset with a maintenance-unavailable asset. Include downtime crossing a reporting boundary and overlapping intervals without double subtraction. Distinguish calendar availability from observed time. Reconcile daily and monthly numerator/denominator components and enforce approved zero-denominator behaviour.

**Boundaries:** Maintenance-adjusted availability belongs here, not in a separate subtraction Recipe. Do not infer downtime duration from a single date unless an approved policy and evidence justify it. Do not duplicate B02 as a separate fleet-ratio tutorial.

### B07 - Build shift revenue, cost and margin with reconciled rollups

**Identity:** `shift-unit-economics`. **Category/area:** `build` / `transformation`; logistics/fleet context is intentional. **Treatment:** new candidate.

**Problem and outcome:** Revenue-only metrics do not establish profitability. Deliver shift-grain economics from defensible event assignments, applicable costs and explicit allocation, with driver/vehicle/period reconciliation.

**Recognition:** Margin per shift, cost-adjusted driver performance or vehicle/shift economics.

**Question to surface:** What is the economic unit? Which revenue and costs belong to it? How are shared costs allocated? Are all required costs observed? Which comparisons require minimum exposure or hours?

**Required scope:** Establish shift identity and assignment provenance, attribute supported revenue, identify applicable cost sources, allocate costs recorded at other grains under approved rules, and produce revenue/cost/margin components with required rollups. Surface currency/unit mismatches or missing upstream conversions instead of adding unapproved FX scope.

**Future proof:** Shift revenue reconciles to attributed events. Cost components reconcile to source totals. Allocation neither loses nor duplicates costs. Driver, vehicle and period totals reconcile. Missing costs are visible, not zero-filled. If rankings are requested, approved exposure/eligibility conditions are applied and evidenced.

**Boundaries:** Do not claim profit from incomplete costs or invented relationships. Not an entire fleet analytics bundle, payroll engine or accounting-policy design. Input modelling prerequisites need not be implemented by invoking B03.

### B08 - Apply effective-dated business rules to historical events

**Identity:** `effective-dated-business-rules`. **Category/area:** `build` / `transformation`. **Treatment:** new candidate.

**Problem and outcome:** Current rates may not be the rates applicable to historical events. Deliver a model that selects the applicable historical rate/rule and calculates the required expected amount.

**Recognition:** Historical fees, surcharges, tariffs, fare components or other effective-dated business rates.

**Question to surface:** Which event timestamp determines applicability? Which dimensions qualify a rule? How do rules compose or take precedence? What happens at validity boundaries, overlaps and missing rules? How are retroactive corrections handled?

**Required scope:** Define rule identity, applicability, relevant timestamps, validity intervals, precedence/composition where needed, calculation units and no-match behaviour. Keep descriptive reference codes distinct from dated calculation rules.

**Future proof:** Cases before, exactly at and after a change select the expected rule. Applicable resource/fleet/customer distinctions are respected. Overlaps and gaps are visible or resolved by the approved policy. An independently calculated example verifies the amount. Adding a future rate does not unintentionally alter historical amounts.

**Boundaries:** Not a generic policy-engine platform. Capturing dimension history is B04's outcome; this Recipe applies business rules. Do not infer real legal/tariff policy from fixture values.

### B09 - Prove an existing dbt change is safe to merge without modifying it

**Identity:** `prove-dbt-change-safe`. **Existing issue:** [GTM-243](https://linear.app/acceleratedata/issue/GTM-243). **Category/area:** `prove` / `data-quality`.

**Problem and outcome:** A successful build does not prove that an existing change preserves the required analytical meaning. Deliver an independent evidence-backed assessment against agreed requirements and baselines without changing the reviewed implementation.

**Recognition:** An existing dbt change needs assurance before merge; reviewers need to establish whether its business answers are supported.

**Question to surface:** What questions, populations, grain, relationships and historical behaviour must remain valid? Which baseline is approved? Which differences are intentional? What constitutes adequate evidence?

**Required scope:** Preserve the candidate's existing assurance requirements. Add conditional examination of grain/keys, mappings, relationship provenance, history, metric populations, aggregation, required dimensions and enrichment grain. Cover incremental idempotency, unique-key integrity and late-arriving behaviour when applicable. Distinguish missing convenience views from unavailable source information or relationships.

**Future proof:** Findings cite actual evidence and are classified as implemented-and-demonstrated, implemented-but-insufficiently-exercised, unsupported, or explicitly out of scope. Discriminating cases cover the relevant semantic risks. The report identifies limitations and unproven claims. The assessed implementation remains unchanged; evidence collection may use appropriate isolated runs.

**Boundaries:** Its future runtime may inspect/test a dbt change, but this batch only authors that instruction. It must not automatically repair the assessed code. Other Build Recipes do not depend on invoking this Recipe to complete their own proof.

### B10 - Strengthen business-grain safeguards in materialized Recipes

**Treatment:** One new combined change issue, one normal PR, two existing Recipe definitions. Do not create one issue per definition or re-purpose unrelated old seed issues.

**Title:** Strengthen business-grain safeguards in incremental conversion and API-to-bronze Recipes.

**Outcome A - `dbt-full-refresh-to-incremental`:** Preserve its existing output-parity, idempotency, late-arriving and measured-runtime requirements. Add a check for disagreement between declared business grain and loader-row identity. When an existing semantic defect is discovered, expose the conflict with output parity and require an approved resolution or separate follow-up. Do not silently redesign the grain while claiming unchanged semantics. Do not assume that idempotency alone proves business-event identity.

**Outcome B - `api-to-bronze-incremental-contract`:** Preserve cursor, write-disposition, contract and landed-count requirements. Explicitly distinguish landed source rows from unique business events and preserve the source identifiers/provenance needed for downstream conformance. Do not force all business deduplication into bronze or change approved source semantics. Do not change existing cursor/late-arrival policies opportunistically.

**Future proof to encode:** Conversion preserves the approved contract and flags unresolved semantic conflicts. Ingestion reports source-row counts accurately and retains agreed identifiers. Neither Recipe calls loader counts unique business events without evidence. Existing acceptance is retained, not replaced by the new safeguards.

**Authoring acceptance:** Both definitions meet the common review, support and repository checks. Regenerate the catalog. A failure affecting either definition leaves this combined ticket unfinished. Do not modify the other materialized orchestration Recipes.

### B11 - Add modelling and logistics/fleet discovery Collections

**Treatment:** One new issue for two non-executable curated Collections; execute last.

**Title:** Add modelling correctness and logistics/fleet Recipe Collections.

**Collection 1:** `modelling-correctness`, title `Build models that answer the right questions`. Intended members: B01-B09's nine canonical Recipe IDs.

**Collection 2:** `logistics-and-fleet-analytics`, title `Logistics and fleet analytics`. Intended members: B01-B08's eight canonical Recipe IDs. This includes generic patterns with relevant logistics triggers and the two domain-specific outcomes.

**Required outcome:** Discovery reuses canonical definitions. Generic Recipes remain broadly discoverable; a logistics Collection does not make them logistics-only. Choose `curated` under the current schema; do not invent a Collection type. Both Collections must meet current publication thresholds using supported/proven materialized members. No website or Studio code is required.

**Acceptance:** Both files validate; each referenced member exists in the target branch and has the expected supported scope; the generated catalog resolves the intended membership and visibility. No copied Recipe bodies, nonexistent IDs, duplicate definitions or metadata-only promises of unsupported execution.

**Dependencies:** B01-B09 are required for the full approved membership. If a required member is blocked, keep B11 unfinished and record the dependency. A smaller temporary draft may help preserve work, but do not merge a silently reduced Collection and call the approved task Done. Do not add more Recipes to resolve the dependency.

## 7. Linear preparation before materialization

Prepare the complete issue batch first, without moving all issues into active work.

1. Read the project's issues, the three known candidates and relevant comments. Search candidate IDs and outcome synonyms. Search materialized definitions and relevant open/closed PRs as well. Do not assume that a Backlog issue means its Recipe is absent.
2. Map each B-key to one issue. Update GTM-187, GTM-241 and GTM-243 instead of duplicating them. Create new candidates only when no equivalent authorized issue exists. Keep B10 combined and B11 combined.
3. Preserve existing issue content and provenance. Use structural edits or a clearly bounded batch section, not blind full-description replacement. If an exact patch cannot safely match, reread and reconcile first.
4. Assign all mapped issues to SS. Put new issues in Backlog and leave unstarted existing candidates in Backlog. Preserve legitimate active/completed state on resume. Use no new priority, cycle, milestone or deadline.
5. Add the specification, canonical identity, this plan's section link, the batch-specific completion rule and explicit exclusions. Keep implementation steps in this plan, not in the issue body. Keep private capability/source analysis in Linear rather than copying it into public files.
6. Record each returned issue ID/URL in the local tracker immediately. Cross-link related batch issues only where useful. Add a blocking relation only for a real prerequisite, not merely the suggested order.
7. Read back each changed issue to verify the title/scope, project, owner and state. Record any deviation caused by pre-existing work. Do not duplicate an issue after an ambiguous write response: search and read first.

Use the issue classification `feature` for new outcomes/Collections and an enhancement for the combined change; these are conceptual classifications, not permission to create labels. GTM does not require Studio/Roadmap/Utilities User Flow labels. Preserve any existing selected metadata.

If an equivalent issue is found outside the authorized project, do not move or modify it silently or create a known duplicate. Record the conflict against the batch item and notify SS through an authorized batch issue or the current-session handoff.

## 8. Per-ticket execution loop

Execute serially so generated catalog changes do not compete. Do not dispatch parallel writers or start unrelated work while a shared verification prerequisite is broken.

1. **Reconcile:** Read the issue, live plan and any existing branch/PR. Check whether the exact approved scope is already satisfied. Reuse work and evidence; do not reset finished work or create a redundant PR. Missing/insufficient evidence is not completion.
2. **Select:** Move Backlog to Todo when selected, then In Progress when authoring begins. Keep SS assigned. Add a concise start comment and update the local tracker.
3. **Pin:** Read the latest verified `pre-prod` head and its CI state. Create `recipes/<linear-id-lowercase>-<short-slug>` or use a compatible existing branch. Record the actual base SHA. Do not stack work on an unmerged ticket branch.
4. **Establish support:** Inspect the current required capabilities and targets. Record the evidence matrix in Linear. If no target is supported, preserve any draft, block the item and continue independently; do not invent a schema-compatible platform just to save it.
5. **Author:** Use the existing template and approved scope. Make structured edits. Use Recipe-local constraints to condense the instructions without losing semantic decisions. Do not add scaffolding, code samples or tests that imply runtime execution occurred.
6. **Review:** Check the Feature/Recipe boundary, scope, business questions, discriminating cases, acceptance, missing-context behaviour, source trust, platform breadth and evidence. Confirm no technical operation is substituted for the requested outcome. Check every approved requirement is represented somewhere in the contract.
7. **Generate and validate:** Run the unchanged catalog generator and applicable tests. Review the diff against the pinned base and allowed paths. Commit the scoped files, generated catalog and truthful tracker checkpoint together. Verify source bytes/hashes when transferring local changes through connector writes.
8. **Open PR:** Target `pre-prod`, link the issue and this plan, state materialization-only scope, support evidence, content-review result and checks actually run. Avoid closing keywords that could mark Linear Done before post-merge checks. Do not expose private source details.
9. **Repair CI:** Inspect the actual required jobs and failing steps/logs for this PR head. Correct failures caused by this change, regenerate and rerun. Do not treat queued/pending/neutral/skipped required work or an empty status set as success. An intentionally inapplicable promotion-only job is not a missing cookbook-contract result.
10. **Revalidate merge:** Refresh PR head, base, diff and review state. If the base or content moved, synchronize without destructive overwrites, regenerate as necessary and obtain fresh applicable checks. Ensure no unresolved required review/protection conflict remains. Merge normally with the expected head SHA; do not bypass protections.
11. **Verify merge result:** Inspect post-merge checks on the actual resulting commit in `pre-prod`. A prior PR check alone is insufficient. On a caused failure, use a corrective branch/PR under this ticket; leave the issue unfinished until corrected post-merge checks pass.
12. **Close:** Add an evidence-backed completion comment and canonical `pre-prod` link; mark Done only after all gates pass. Read back the issue. Update the local tracker immediately, then checkpoint the post-merge facts in the next content PR or final tracker PR.

At planning time the repository documented:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -q
.venv/bin/python scripts/build_catalog.py
.venv/bin/python scripts/build_catalog.py --check
.venv/bin/python scripts/check_schema_versions.py --base "$(git merge-base origin/pre-prod HEAD)"
```

Re-read the live commands. Do not change dependency pins or scripts if setup fails. Capture command exits and actual output; a predicted result is not evidence. Schema checks must compare the actual change with a valid base, not the same modified tree on both sides.

### Connected-tool CI cautions

Discover and use the current tool schemas. A commit's legacy combined status may omit modern Check Runs. Inspect actual workflow jobs/check runs and required protections.

The GitHub connector's `fetch_commit_workflow_runs` wrapper may return only pull-request-triggered runs. Do not use absence there to conclude that post-merge push CI passed or does not exist. Use the connector's approved GitHub GET support to inspect repository workflow runs for the merge SHA and `event=push`, then its jobs/logs. Match head SHA, event and target branch. Follow pagination.

For example, the approved GET endpoint shape is `https://api.github.com/repos/accelerate-data/vibedata-cookbooks/actions/runs?head_sha=<merge_sha>&event=push`. Check runs can also be inspected under `commits/<sha>/check-runs`. These are read routes through the GitHub connector, not a reason to extract credentials.

## 9. Blockers, retries and safe stopping

For a blocker, keep the ticket unfinished and In Progress if work has started, assign SS, add a prominent blocker section and a comment mentioning the resolved SS account. Do not create a new workflow state. Record:

- Blocker class: missing capability, insufficient support evidence, missing tool/permission, scoped CI failure, unrelated baseline failure, dependency or conflicting prior work.
- Exact affected requirement, target(s), branch/PR/commit and failing check or source evidence.
- What was attempted, what changed, and what remains unverified.
- The specific external decision/capability/action needed to resume.
- Whether independent items can continue and which dependents are skipped.

A failed write gets one safe retry after reading back the current state. For CI repairs, continue while a concrete new diagnosis supports a scoped correction. Stop repeating the same attempt without new evidence. Distinguish external outages or access failures from bad Recipe content. Do not resolve capability gaps by weakening the desired outcome.

Keep unsupported Recipe drafts unmerged. Keep B11 blocked when a required member is unavailable. Continue other independent items. Stop the whole batch only when a shared prerequisite makes safe progress impossible. If a session/resource limit is reached, checkpoint truthful progress and return the updated Markdown; do not claim unattended work will continue after the session ends.

If Linear is unavailable, do not perform untracked ticket work or mark it Done. Record the failed action locally and restore tracking first. If a Linear/GitHub integration auto-closes a ticket early, restore an unfinished state and document why the batch's completion gate is not met.

## 10. Tracking, persistence and resumption

Maintain this same Markdown file locally throughout execution. Do not create a separate Linear project document or an unrelated plan. The approved specifications remain stable; update the tracker and execution log rather than rewriting decisions to match partial results.

Update the local record immediately after issue creation/update, start, support decision, branch/PR creation, CI repair/result, merge, post-merge result, blocker and completion. Do not persist fabricated IDs or predicted success. Use `not started`, `not created`, `not assessed` and `pending verification` literally when appropriate.

Commit the latest checkpoint in each ticket PR. Post-merge results necessarily occur after that PR's last content commit, so persist them in the next content PR or a final tracker-only PR. At the end, reconcile all ticket facts and raise the final tracker PR if needed. No additional Linear ticket is required.

A tracker commit cannot truthfully contain its own future merge result. Do not create an endless sequence of tracker PRs to solve that. Record the final checkpoint PR's closure in its PR conversation and the final downloadable Markdown, with a clear checkpoint boundary if that final local record is newer than the committed copy.

On resume, read this file, then actual Linear state and GitHub branches/PRs/CI. External observed state takes precedence over stale tracker cells. Reconcile discrepancies before continuing. Reuse the same B-key and issue, preserve completed steps, and do not reopen settled requirements or blindly recreate resources.

### Batch tracker

`not started` below describes the execution of this plan, not a claim about the current issue owner or status. Validate live state before mutation.

| Key | Issue | Preparation | Execution | Branch / PR | Support | Merge / post-merge CI | Blocker / next action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| B01 | [GTM-296](https://linear.app/acceleratedata/issue/GTM-296) | Verified; SS; Backlog | Done; read back | recipes/gtm-296-business-event-fact; [PR #10](https://github.com/accelerate-data/vibedata-cookbooks/pull/10) | All 5 targets (supported) | d297804b462c50118d4d9076ac6e9d84d1d1eec8; [push CI passed](https://github.com/accelerate-data/vibedata-cookbooks/actions/runs/36395516309) | Complete; checkpoint in next content PR |
| B02 | [GTM-297](https://linear.app/acceleratedata/issue/GTM-297) | Verified; SS; Backlog | Done; read back | recipes/gtm-297-metric-population-and-rollups; [PR #11](https://github.com/accelerate-data/vibedata-cookbooks/pull/11) | All 5 targets (supported) | 23f4e906424cd0dc3ce260dea982897fa836cb9c; [push CI passed](https://github.com/accelerate-data/vibedata-cookbooks/actions/runs/36397194772) | Complete; checkpoint in next content PR |
| B03 | [GTM-298](https://linear.app/acceleratedata/issue/GTM-298) | Verified; SS; Backlog | Authoring; In Progress | recipes/gtm-298-event-resource-attribution; PR not created | All 5 targets (supported) | None | Author and review full scope |
| B04 | [GTM-187](https://linear.app/acceleratedata/issue/GTM-187) | Verified; SS; Backlog | Not started | None | duckdb_local (supported); others unassessed | None | Select sequentially |
| B05 | [GTM-299](https://linear.app/acceleratedata/issue/GTM-299) | Verified; SS; Backlog | Not started | None | All 5 targets (supported) | None | Select sequentially |
| B06 | [GTM-241](https://linear.app/acceleratedata/issue/GTM-241) | Verified; SS; Backlog | Not started | None | All 5 targets (supported) | None | Select sequentially |
| B07 | [GTM-300](https://linear.app/acceleratedata/issue/GTM-300) | Verified; SS; Backlog | Not started | None | All 5 targets (supported) | None | Select sequentially |
| B08 | [GTM-301](https://linear.app/acceleratedata/issue/GTM-301) | Verified; SS; Backlog | Not started | None | All 5 targets (supported) | None | Select sequentially |
| B09 | [GTM-243](https://linear.app/acceleratedata/issue/GTM-243) | Verified; SS; Backlog | Not started | None | All 5 targets (supported) | None | Select sequentially |
| B10 | [GTM-302](https://linear.app/acceleratedata/issue/GTM-302) | Verified; SS; Backlog | Not started | None | Existing 4 dbt / 5 ingestion targets | None | Select sequentially |
| B11 | [GTM-303](https://linear.app/acceleratedata/issue/GTM-303) | Verified; SS; Backlog | Not started | None | Non-executable; member-dependent | None | Wait for B01-B09 membership |

### Evidence record for each item

Extend below as work occurs. Keep private evidence details in the issue and public references/summaries here.

```text
Batch key and issue URL:
Last observed issue owner/state and observation time:
Preparation outcome and source-preserving edits:
Canonical Recipe/Collection path(s):
Support decision, declared platforms and evidence reference:
Unsupported/unassessed targets and reason:
Base SHA; authored/tested PR head SHA:
Branch; PR URL; corrective PRs if any:
Content-review result and scope-diff check:
Local commands actually run, exits and limitations:
Required PR jobs, run URLs, head SHA and outcomes:
Merge commit; post-merge run URL and outcome:
Completion/blocker comment reference and verified issue state:
Next action and dependencies:
```

### Execution log

- 2026-09-28: Scope and execution rules approved. Initial plan prepared for a separate execution session. No Linear batch mutations or Recipe/Collection materialization performed by the planning session. Discover the plan-initialization PR and verify its live merge/CI status before considering it complete.

## 11. Final delivery and suggested skills

Return a brief status report plus a downloadable updated copy of this Markdown. Include completed, blocked and not-started items; actual ticket/PR links; supported platforms per Recipe; the last verified `pre-prod` commit; CI results; exact resumption actions; and whether the local final checkpoint is newer than the committed one. State explicitly that `main` promotion and runtime Recipe evaluations were not performed.

Suggested skills, when available and applicable:

- **creating-linear-issue:** Prepare precise, source-backed issue scopes and preserve existing content. The user has already approved the field defaults, bounded batch and autonomous execution; do not repeat resolved questions. Do not use this skill for PR/merge execution.
- **handoff:** Reconcile the final tracker and produce the updated session handoff without duplicating canonical definitions or exposing private data.
- Repository-provided contribution and validation guidance is mandatory. Do not restart brainstorming/grilling for settled decisions. If new information makes an approved decision impossible, record a blocker rather than expanding scope.

No additional product design, website implementation or data-analysis dashboard work is authorized by this plan.

### Codex execution checkpoint

User amendment: execute in the local cookbook repository with GitHub CLI and connected Linear tools. This supersedes the original temporary-container, connector-only and no-Mac clauses. Repository scope, definition-only scope and completion gates remain unchanged. Mechanical work uses Luna xhigh; substantive authoring and capability assessment use Astra high.

- 2026-09-28 11:50 GST: Reconciled initialization PR #9 as merged at 4003b0244113b91003de27dfd7524469f2611f5e. Verified push CI https://github.com/accelerate-data/vibedata-cookbooks/actions/runs/36387593499: Cookbook contract succeeded; promotion-only job intentionally inapplicable. Local exact pinned dependencies present; 284 tests passed; catalog --check and schema-version check passed. ENV-01 from the previous temporary environment is resolved for this authorized checkout. Reuse GTM-296/297/298; GTM-187/241/243 retain original provenance. No Recipe runtime evaluation performed.
- 2026-09-28 11:56 GST: B01: reused/updated GTM-296; preserved original provenance and unrelated metadata. SS assigned; unstarted Backlog.
- 2026-09-28 11:56 GST: B02: reused/updated GTM-297; preserved original provenance and unrelated metadata. SS assigned; unstarted Backlog.
- 2026-09-28 11:56 GST: B03: reused/updated GTM-298; preserved original provenance and unrelated metadata. SS assigned; unstarted Backlog.
- 2026-09-28 11:56 GST: B04: reused/updated GTM-187; preserved original provenance and unrelated metadata. SS assigned; unstarted Backlog.
- 2026-09-28 11:56 GST: B05: created GTM-299; preserved original provenance and unrelated metadata. SS assigned; unstarted Backlog.
- 2026-09-28 11:56 GST: B06: reused/updated GTM-241; preserved original provenance and unrelated metadata. SS assigned; unstarted Backlog.
- 2026-09-28 11:56 GST: B07: created GTM-300; preserved original provenance and unrelated metadata. SS assigned; unstarted Backlog.
- 2026-09-28 11:56 GST: B08: created GTM-301; preserved original provenance and unrelated metadata. SS assigned; unstarted Backlog.
- 2026-09-28 11:56 GST: B09: reused/updated GTM-243; preserved original provenance and unrelated metadata. SS assigned; unstarted Backlog.
- 2026-09-28 11:56 GST: B10: created GTM-302; preserved original provenance and unrelated metadata. SS assigned; unstarted Backlog.
- 2026-09-28 11:56 GST: B11: created GTM-303; preserved original provenance and unrelated metadata. SS assigned; unstarted Backlog.
- 2026-09-28 11:58 GST: Reconciled initialization PR #9 as merged at 4003b0244113b91003de27dfd7524469f2611f5e. Verified push CI https://github.com/accelerate-data/vibedata-cookbooks/actions/runs/36387593499: Cookbook contract succeeded; promotion-only job intentionally inapplicable. Local exact pinned dependencies present; 284 tests passed; catalog --check and schema-version check passed. ENV-01 from the previous temporary environment is resolved for this authorized checkout. Reuse GTM-296/297/298; GTM-187/241/243 retain original provenance. No Recipe runtime evaluation performed.
- 2026-09-28 11:58 GST: Complete 11-ticket batch prepared, read back and assigned to SS; five additional tickets GTM-299 through GTM-303 created, six existing tickets reused. Capability evidence recorded privately in each Linear issue. B01 selected through Todo to In Progress; base 4003b0244113b91003de27dfd7524469f2611f5e. B04 supported on duckdb_local only; other four snapshot targets unassessed; no runtime-proven claims.
- 2026-09-28 12:07 GST: B01 / GTM-296 authored at 9b032fea01b03159543dc0620aebe74631d11ef8; independent spec compliance and task quality both approved with no findings. 285 tests, unchanged generator/freshness, schema-version and whitespace checks passed. PR #10 opened to pre-prod; required CI pending. No runtime evaluation.
- 2026-09-28 12:08 GST: B01 PR #10 merged after Cookbook contract succeeded for head 9b032fea01b03159543dc0620aebe74631d11ef8 (PR run 36395446333). Merge d297804b462c50118d4d9076ac6e9d84d1d1eec8; post-merge push run 36395516309 pending. Issue remains unfinished.
- 2026-09-28 12:09 GST: B01 / GTM-296 Done and read back after post-merge Cookbook contract passed on d297804b462c50118d4d9076ac6e9d84d1d1eec8 (push run 36395516309). Canonical link and full evidence posted to Linear; definition supported on all five targets, not runtime-proven.
- 2026-09-28 12:09 GST: B02 / GTM-297 selected through Todo to In Progress on fresh branch from verified pre-prod d297804b462c50118d4d9076ac6e9d84d1d1eec8.
- 2026-09-28 12:23 GST: B02 authored at437b4e6; independent review found one missing-value-policy conflict. Scoped correction5beba6d passed re-review with no new findings. 286 repository tests and unchanged catalog/freshness/schema/whitespace checks passed; PR #11 opened to pre-prod. No runtime evaluation.
- 2026-09-28 12:25 GST: B02 PR #11 merged at 23f4e906424cd0dc3ce260dea982897fa836cb9c after required PR Cookbook contract passed for corrected head 5beba6da83e3390f8b20551130b9394aacb215f4 (run 36397089724). Post-merge push run 36397194772 pending; issue unfinished.
- 2026-09-28 12:26 GST: B02 / GTM-297 Done and read back after push Cookbook contract succeeded at23f4e906424cd0dc3ce260dea982897fa836cb9c (run36397194772). Full evidence and canonical link recorded; all five targets supported, no runtime evaluation.
- 2026-09-28 12:26 GST: B03 / GTM-298 selected through Todo to In Progress; fresh branch from verified pre-prod23f4e906424cd0dc3ce260dea982897fa836cb9c.
