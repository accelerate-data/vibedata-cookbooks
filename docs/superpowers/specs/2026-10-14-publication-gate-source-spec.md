# Vibedata Cookbook publication gate - implementation specification

**Status:** Approved requirements; ready for implementation
**Date:** 2026-10-14
**Primary repository:** https://github.com/accelerate-data/vibedata-cookbooks
**Target branch:** `pre-prod` (the default contribution branch; `main` receives promotions)
**Existing skill input:** the supplied `vibedata-recipe-review.zip`; update the one `vibedata-recipe-review` skill in place.

## 1. Task for the coding agent

Implement the agreed Cookbook publication review system. Do both workstreams:

1. **Update the existing `vibedata-recipe-review` skill** to apply the complete semantic publication rubric and emit consistent PR findings.
2. **Update `vibedata-cookbooks`** with deterministic CI, the PR template, contributor guidance, tests, and the necessary GitHub review-policy configuration.

Read the current `pre-prod` branch and the attached skill before editing. Use a new feature branch targeting `pre-prod`. Make focused changes; do not rewrite existing Recipes in bulk. If the skill is not in a writable repository, produce the complete updated skill directory and packaged ZIP as a separate deliverable. Do not create a second review skill.

Keep the publication gate independent of any private or separately installed reviewer rubric. The repository's contributor rules must be understandable without installing the skill; the skill must include its own self-contained semantic rules.

### Sources and authority

- **Publication decisions:** this specification is authoritative where existing prose or the attached skill differs.
- **File structure and allowed metadata:** the live `vibedata-cookbooks` schema, template, existing CI, and versioning rules remain authoritative unless an explicit change is required here.
- **Recipe ontology:** https://github.com/accelerate-data/vibedata-gtm/blob/main/docs/gtm/plan/04-demand-inbound/cookbook/README.md
- **PR description:** evidence for the change, not a replacement for the canonical Recipe contract.

If existing Cookbook guidance conflicts with the approved publication decisions, align that guidance. Do not silently invent a new schema or taxonomy.

## 2. Non-negotiable decisions

### 2.1 What is being published

- A Recipe is **one recognizable, bounded data-engineering outcome**, reusable inside a Studio Intent, with an observable acceptance contract and agent guidance.
- A direct atomic operation is a **Feature**, reusable technical knowledge is a **Skill**, a cross-cutting invariant is a **Guarantee**, and a larger bundle of independent outcomes is a **Collection** or multiple Recipes.
- Reject exact or semantic duplicates of existing Recipes or candidate outcomes. Changing source-system nouns, business function, or platform names alone is not enough to justify a clone.
- Prioritize review of the **reusable contract**, not the example that inspired it. The example cannot redefine the contract.
- The Recipe inherits current Intent context: Domain, project, repository, source, platform, and prior approved requirements. Do not require users to resupply known context.

### 2.2 Readiness and implementation evidence

| Readiness | Can be published? | Contract required? | Implementation evidence required? | Invocation? |
| --- | --- | --- | --- | --- |
| `planned` | Yes | Complete reusable contract | No executable example required | Discoverable, but not offered as executable |
| `supported` | Yes | Complete reusable contract | One end-to-end execution showing the defining outcome, with representative verification | Yes |
| `proven` | Yes | Complete reusable contract | `supported` evidence plus a dedicated, repeatable Recipe-level eval/journey, named in `evidence.evals` | Yes |

- An example is expected to run on **one platform**, preferably `duckdb_local` if the outcome can run there. Use another appropriate platform if DuckDB cannot support the outcome.
- **Never require implementation examples for every declared platform**. Untested platforms may remain in `works_with.platforms` when existing product/tool capabilities justify compatibility and the PR records the rationale and limitations.
- A lack of platform-specific example coverage is normally a **warning**, not a blocker. A platform with no viable supported capability path is a **blocker for the claimed readiness/platform metadata**.
- If a `supported` or `proven` example does not demonstrate the **core promised behavior**, that is a readiness/evidence blocker, even if the reusable contract is well written. Do not weaken the Recipe contract to match a faulty example.
- An example that omits a nonessential branch, but whose contract covers it correctly, may pass with a documented limitation.
- `planned` must identify which required capability is missing. Its absence of execution evidence is not a blocker.
- `works_with.platforms` is precise compatibility/discovery metadata; for `planned`, listed platforms are intended targets, not a claim that the Recipe already runs.

### 2.3 Correctness, semantic decisions, and execution

- Define material inputs, bounded outputs, scope, grain/identity, and the observable success condition where applicable.
- `Verified by` states **properties of correct outcomes**, not merely instructions to run tools or check that tests pass.
- For defining business logic, require **independent expected results or checks**. A test that repeats the implementation's possibly incorrect calculation is not sufficient. A fixed fixture need not live in the Recipe; the contract must describe what needs proving.
- Acceptance criteria must cover defining behavior and material edge/failure modes. Do not insist that the single example exhaustively exercises all branches.
- Address relevant risks: silent exclusion/data loss, unintended deduplication, duplicate counts or join fan-out, wrong grain/aggregation, null/unknown handling, late or changed records, deletes, reruns/recovery, partial/unobservable verification, unsafe mutations, and consumer contract changes. Do not add irrelevant boilerplate.
- Every material record should have an explainable disposition **where the outcome requires completeness/accountability**. Do not force population accounting onto unrelated Recipes.
- The Recipe must name the **types of business decisions** the agent may need to settle in `Ask first`, without inventing their answers. Examples: eligibility, time boundaries, fiscal conventions, precedence, account classifications, missing-value rules, tolerances, effective dates, and exception policy.
- The agent may propose alternatives, but must not silently choose or apply customer policy. Inherit approved decisions first and ask only unresolved semantic questions.
- Partial work may be retained, but **never reported as completed**. Block publication of unsafe or misleading outputs when required meaning, approval, or verification is missing.
- Keep `Prompt` (outcome), `Verified by` (acceptance), and `Agent guidance` (approach, genuine questions, and risk-specific guardrails) distinct and mutually consistent.
- Verify that actual Vibedata capabilities and named Skills/Features can accomplish what a `supported` Recipe promises, using public Cookbook and PR evidence (including authoritative capability references supplied in the PR). Do not accept unsupported claims based on generic LLM ability. An unsupported dependency implies `planned` unless another supported path exists.
- Require quantitative before/after measurements **only where the Recipe outcome calls for them**, such as performance or cost optimization. If it promises equivalence, require an observable comparison, not an unrelated numerical benchmark. Do not turn every Recipe into a benchmark.

### 2.4 Scope and security

- Public-repository material must not expose credentials, tokens, customer data, or other unauthorized confidential information. Check public Recipe/Collection files, templates, examples, and PR content.
- **Do not read, audit, or scan Google Drive/Domain Bundles** as part of this gate. They are outside both functional review evidence and security review scope.
- Use public Cookbook content and PR description/evidence for review. Record missing evidence; do not claim to have verified Drive artifacts.
- Do not auto-edit an author's Recipe in CI or during semantic review. Return failures and specific corrections to the author.
- Preserve the current post-merge `catalog.json` generation workflow; the no-rewrite rule applies to PR validation, Recipe source, and reviewer behavior, **not** the existing catalog regeneration after merge.

## 3. Semantic review skill changes

Edit these files within the existing skill archive:

- `vibedata-recipe-review/SKILL.md`
- `vibedata-recipe-review/references/review-rubric.md`
- `vibedata-recipe-review/references/output-format.md`

Preserve the skill name, entrypoint, `agents/openai.yaml`, and existing icon unless a change is technically required. Prefer a short entrypoint and a focused supporting rubric; remove obsolete/duplicated prose rather than appending another parallel rubric.

### 3.1 Required workflow

1. Identify new PR, existing PR, PR set, pre-PR draft, or re-review. Use GitHub to read current head/base, PR description, changed `recipe.md` files, and directly relevant existing Recipes. On re-review, compare with the previously assessed head/findings.
2. Confirm correct Recipe/Feature/Skill/Guarantee/Collection boundary and distinctness. Compare published Recipes **and Linear Recipe candidates** when connector access is available. If Linear is unavailable, state the scope of the comparison; do not invent a complete duplicate check.
3. Review the contract across frontmatter, `Prompt`, `Verified by`, `Instructions`, `Compose`, `Ask first`, `Guardrails`, `qualifiers`, and `related`. Check internal consistency and neighboring Recipe boundaries.
4. Check input/output expectations, relevant semantic policy types, absence of invented policy, completeness/exception disposition where relevant, and independent acceptance criteria that distinguish correct from plausible-but-wrong behavior.
5. Check material edge cases and risk-specific guardrails. No generic checklist padding in the Recipe.
6. Check product feasibility and `planned`/`supported`/`proven` classification against concrete capability evidence provided in the PR and public Cookbook. Public authoritative product references may be cited in the PR. If sufficient evidence is absent, request it; do not inspect private Studio bundles or treat generic LLM ability as product support.
7. Check the implementation **only for the platform demonstrated** and the core outcome/representative cases. For `planned`, do not demand executable evidence. Use the public PR evidence; do not open Drive.
8. Assess untested platform claims by documented capability/compatibility, not by demanding one example per platform. Compatibility rationale belongs in the PR description; no separate per-platform artifact.
9. Scan changed public-repo text for evident sensitive data or secrets, in addition to any deterministic secret scan result. Do not inspect external/private archives.
10. Report blockers, warnings, and suggestions; provide paste-ready review comments. **Do not write fixes, merge, or post reviews automatically** unless separately requested.

### 3.2 Decision rules and verdicts

| Classification | Meaning | Gate |
| --- | --- | --- |
| **Blocker** | Reusable-contract defect, unsafe behavior, misleading readiness/capability, unsupported promise, failure to demonstrate the core outcome for `supported`/`proven`, or missing material public PR evidence | Changes required |
| **Warning** | Valid disclosed limit, justified but untested compatible platform, or optional case missing from the example without invalidating the contract | May publish |
| **Suggestion** | Nonmaterial editorial improvement | May publish |

Use exactly these reader-facing verdicts:

- **PASS:** No blockers or material warnings.
- **PASS WITH WARNINGS:** No blockers; disclose residual limitations.
- **CHANGES REQUIRED:** One or more blockers.

For GitHub review recommendations, `PASS` and `PASS WITH WARNINGS` map to a human `Approve`; `CHANGES REQUIRED` maps to `Request changes`. The skill produces a recommendation, not the human approval itself.

Every blocker must have:

1. Relevant file/section or PR evidence location.
2. The specific reusable-contract, safety, evidence, or metadata requirement violated.
3. A concrete counterexample or failure mode where useful.
4. The **smallest sufficient correction**, as a paste-ready comment for the author.

Keep implementation-example limitations separate from reusable-contract defects. When an example defect disproves the readiness claim, explicitly classify it as **readiness/evidence**, not as a reason to weaken the Recipe specification.

### 3.3 Replace obsolete skill assumptions

The attached skill currently says to `APPROVE` only when a Recipe can execute through current product capabilities and normally treats example bugs as nonblocking. Update that logic:

- `planned` may pass with no runnable implementation if its full contract and missing capabilities are explicit.
- `supported` requires a demonstrated defining outcome; an unsuccessful or unsubstantiated core example is not a mere optional limitation.
- `proven` requires an identified, repeatable Recipe-level evaluation.
- Missing untested **optional** branches are normally nonblocking; unproven **defining** outcomes are not.
- Replace its two-way `APPROVE`/`CHANGES REQUESTED` output with the three verdicts above.
- Preserve the distinction between contract and example, the inheritance of Intent context, and the no-policy-invention rule.

### 3.4 Skill validation cases

Validate the updated skill against at least these review fixtures or controlled dry runs:

- Well-specified `planned`, explicit missing capability, no execution example: **PASS** or **PASS WITH WARNINGS**.
- `supported`, DuckDB example proves the defining outcome, four other platforms justified but untested: **PASS WITH WARNINGS** at most; not blocked merely for missing examples.
- `supported`, claimed but no demonstrated core execution in PR evidence: **CHANGES REQUIRED** for readiness evidence.
- `proven`, no identifiable repeatable Recipe eval: **CHANGES REQUIRED**.
- Contract silently excludes statistical or consolidation-only accounts without approved eligibility policy: **CHANGES REQUIRED**.
- Implementation example omits one valid optional semantic branch, while the contract correctly covers it: **warning**, not a blocker.
- Contract's acceptance checks are satisfied by an incorrect result because they reuse the implementation's business rule: **CHANGES REQUIRED**.
- Only editorial cleanup remains: **PASS** with suggestions; do not invent blockers.
- Re-review resolves original blocker with no regression: old blocker disappears; report only outstanding/new issues.

## 4. Cookbook repository changes

Work against the latest `pre-prod`, not a stale `main` snapshot. The following paths exist as of 2026-10-14:

| Path | Required action |
| --- | --- |
| `.github/workflows/ci.yml` | Keep existing contract CI and add narrowly scoped deterministic checks |
| `.github/workflows/catalog.yml` | Preserve post-merge catalog generation |
| `.github/pull_request_template.md` | Replace the current sparse template with review-evidence sections |
| `CONTRIBUTING.md` | State author self-check and publication policy; clarify Drive separation |
| `README.md` | Clarify `planned` publication/readiness and invocation semantics |
| `tests/test_published_recipes.py` | Fix the incorrect unconditional `evidence.evals == []` assumption |
| `schema/recipe.schema.json` | Prefer **no change**; already supports `planned` and requires evals for `proven` |
| `tests/` and `scripts/` | Add focused tests/scripts for new deterministic rules as needed |

### 4.1 Deterministic CI (blocking, read-only)

Preserve existing checks: Python tests, Recipe/Collection schema and format validation, ID/reference checks, generated catalog validation, and schema-version discipline.

Add or correct these **objectively testable** checks:

1. **Fix `proven` support:** `tests/test_published_recipes.py` currently asserts `entry["evidence"]["evals"] == []` for every Recipe. Remove this unconditional assertion. A `proven` Recipe must be allowed and required (by the existing schema) to have nonempty `evidence.evals`. Do not reject legal `planned` Recipes.
2. **New/changed Recipe PR body structure:** On PRs targeting `pre-prod` that change `recipes/**/recipe.md`, require the PR description to contain the evidence headings in Section 4.2. Validate **presence/structure only**, not whether their prose is persuasive. Treat `Not applicable: planned` as valid for implementation execution sections. Do not require these fields for documentation-only, collection-only, or `pre-prod` -> `main` promotion PRs. Trigger validation when the PR description is edited as well as when commits change.
3. **Generated catalog policy:** Reject contribution PRs to `pre-prod` that edit `catalog.json`; authors must not regenerate and commit it in their PR. Keep the existing workflow that regenerates it **after merge** to `pre-prod` and checks freshness on promotion to `main`.
4. **Public-repo secret scan:** Add a maintained scanner (for example, Gitleaks), pinned to a specific release/commit, covering changed public-repo/PR content. Provide a documented, narrow false-positive process. Do not run the scanner against Google Drive or other private evidence. Keep the scanner read-only.
5. **Tests for all checks:** Positive and negative tests, including PRs with no Recipe changes, `planned` N/A evidence, catalog-edit detection, PR edits, and a safe synthetic secret fixture.

Implementation safety:

- Parse the GitHub event payload or trusted file input; never interpolate an untrusted PR body into a shell command.
- Use least-privilege GitHub Action permissions. Emit actionable failures naming the missing section or offending path.
- Ensure deterministic steps do not write back to PR branches or edit Recipe source files.
- Keep semantic policy checks out of deterministic CI: do not fail builds based on keyword searches for `late`, `null`, `proof`, `qualifier`, `ask first`, or `guardrail`.
- `Compose` references are currently advisory. Validate their usefulness and existence semantically unless a **reliable machine-readable registry** already exists. Do not create a fake capability registry or a hardcoded list to make CI appear comprehensive.
- Do not add an external LLM call to required CI for semantic grading. The updated review skill and human PR review own that judgment.

### 4.2 PR template

Update `.github/pull_request_template.md` to include a concise template, using these headings (names may be refined, but CI and template must agree):

```markdown
## Summary
<!-- Recipe IDs and what changed. -->

## Distinct outcome and overlap
<!-- Why is this a Recipe, not a Feature or a duplicate? Links to related Recipes or Linear candidates. -->

## Readiness and required capabilities
<!-- planned/supported/proven; current support or exactly what is missing. -->

## Platform compatibility
<!-- For every declared platform, give the supported execution path/rationale, whether assessed, and any limitations. No per-platform example required. -->

## Implementation example and execution evidence
<!-- One platform only, preferably DuckDB where appropriate. State the example's platform, core scenario, checks/results, and known untested cases. For planned: 'Not applicable: planned'. No Google Drive links required. -->

## Limitations and material risks
<!-- Key assumptions, open semantic choices, safety boundaries, and unverified behavior. -->

## Author checklist
- [ ] Contract describes a distinct bounded outcome and contains observable acceptance criteria.
- [ ] Material business decisions remain user-approved; known Intent context is inherited.
- [ ] Defining risks and representative correctness cases are covered.
- [ ] Readiness and platform claims match current capabilities and available PR evidence.
- [ ] Public repo changes and this PR do not expose secrets or unauthorized sensitive data.
- [ ] Local deterministic tests and validation pass; `catalog.json` is not edited.
```

The example and compatibility narrative belong in the PR description. **Do not require new permanent JSON/YAML evidence artifacts**, a separate implementation example per platform, or any Drive inspection. A PR may link to public evidence, but links must not substitute for the core justification in the PR body.

The existing PR template has a mandatory Domain Bundle/Google Drive checkbox. **Remove it from the publication review checklist**. If the organization still requires an internal Domain Bundle archive, describe that as a separate author-side archival process, not something CI or the reviewer verifies. Do not remove the broader internal archival policy without authorization.

### 4.3 Contributing and documentation

Update `CONTRIBUTING.md` and related public docs to explain, concisely:

- What counts as a Recipe vs Feature, Skill, Guarantee, or Collection.
- The three readiness states. `planned` **can publish**, but is not executable. `supported` requires one demonstrated defining outcome. `proven` adds a repeatable named Recipe eval.
- One implementation example is sufficient; prefer DuckDB unless unavailable. Other platform declarations need compatibility reasoning in the PR, not separate examples.
- The contract must specify relevant acceptance properties and independent expected results, material policy-decision types, honest exceptional states, and risk-specific guardrails.
- An author should run deterministic checks **and** the semantic self-review before requesting human review. Do not require installing a private skill to understand the checklist.
- Reviewer classifications (blocker/warning/suggestion) and the three verdicts.
- The public-repo and PR-evidence-only review scope. Domain Bundle storage, if retained, is **not a publication-review dependency**.
- New and changed Recipes get review; re-reviews focus on changes and regressions.
- CI is read-only; only the existing post-merge catalog job regenerates `catalog.json`.

Do not duplicate the full current JSON schema or its length limits in multiple documents. Point authors to the canonical schema/template for file-level rules.

### 4.4 GitHub review protections (configuration, not just documentation)

The current docs say any user with write access can merge into `pre-prod`; this is not the approved publication policy. Inspect the actual repo rulesets/branch protection and configure, if authorized:

- PR required for changes to `pre-prod`.
- At least **one approving review from someone other than the author** before merge to `pre-prod`.
- Required deterministic CI statuses, including the new PR-structure and secret-scan checks as applicable.
- Prevent an approval from counting after materially new, unreviewed commits (use the appropriate stale-review/last-push controls).
- Do **not** require founder/CODEOWNER approval for routine `pre-prod` changes unless that is already an explicit higher-level policy. The authorized independent reviewer is sufficient.
- Keep the existing controlled `pre-prod` -> `main` promotion flow and owner restrictions. Do not weaken protections on `main`.

A `.github/CODEOWNERS` file by itself is not approval enforcement. If branch/ruleset configuration cannot be changed with available rights, do **not** claim enforcement. Supply exact settings and mark that step as outstanding. Align `CONTRIBUTING.md` with the actual configured policy.

### 4.5 Consumer behavior for planned Recipes (cross-repository follow-up)

The existing Recipe contract needs **no new field** to represent `planned`. Consumers already receive `readiness` through the metadata catalog.

Required behavior for the website/Studio consumers:

- A `planned` Recipe may be discoverable and readable.
- Label it clearly as `planned`, identify missing capabilities, and disable/hide the executable **Use Recipe** invocation action.
- Do not infer executable support simply because `works_with.platforms` has entries.
- Only `supported` and `proven` contribute to Collection publication thresholds; preserve the existing logic.

This is a **consumer UI/product follow-up**, not a reason to alter the Cookbook schema or block the repository changes. If the coding agent has those consumer repositories explicitly in scope, implement and test there as a separate change. Otherwise document the gap and the exact consumer changes needed; do not silently declare the UI behavior complete.

## 5. Human review process

1. Author runs deterministic validation and the updated semantic skill's **pre-PR self-review**. Correct blockers before requesting review.
2. Author opens a PR to `pre-prod` using the evidence template.
3. Deterministic CI checks run and produce read-only failures if needed.
4. Reviewer runs the semantic skill against the PR, inspects **public Recipe content and PR evidence only**, and leaves the verdict and paste-ready comments on the PR. Do not inspect Drive.
5. An independent human reviewer approves only a `PASS` or `PASS WITH WARNINGS`; a `CHANGES REQUIRED` verdict returns to the author.
6. On changes, review fixed blockers, changed text, and resulting regressions. Do not re-audit unaffected content without cause.
7. Merge to `pre-prod` after required status checks and human approval; let the existing catalog workflow regenerate `catalog.json`; then use the protected promotion flow to `main`.

Keep the semantic skill and human review **outside deterministic CI**. A semantic review can be posted manually by the reviewer; do not build a new review bot as a prerequisite.

## 6. Acceptance tests and completion criteria

### Repository tests

- [ ] Existing unit tests and `python scripts/build_catalog.py --validate` pass on `pre-prod`-based code.
- [ ] A valid `planned` Recipe passes structural CI with no implementation example, while its readiness limitations remain a semantic requirement.
- [ ] A valid `proven` Recipe with named `evidence.evals` is accepted; the old `evals == []` test no longer rejects it.
- [ ] `proven` without eval evidence is still rejected by the canonical schema.
- [ ] Adding/changing a Recipe without required PR-description headings fails with an actionable CI message.
- [ ] PR description edits are revalidated; `planned`'s execution-evidence N/A is permitted.
- [ ] Docs/Collection-only PRs and main promotion PRs do not incorrectly require a Recipe-evidence template.
- [ ] Contribution PRs attempting to commit `catalog.json` fail; the existing post-merge catalog job remains functional.
- [ ] A synthetic leaked secret in changed public content fails the scanner; ordinary placeholders do not create unresolved false positives.
- [ ] CI does not alter PR content or source files.
- [ ] At least one independent human approval is enforced on `pre-prod`, or the missing permissions/settings are explicitly reported as outstanding.

### Skill review examples

- [ ] Planned but contract-complete: publishable without a runnable example.
- [ ] One-platform example with justified untested target platforms: not automatically blocked.
- [ ] Unsupported mandatory capability with `readiness: supported`: blocker / reclassify as `planned` or narrow scope.
- [ ] Missing evidence of the core outcome for `supported`: blocker.
- [ ] Material acceptance gap (wrong account classification, silent dropped records, invalid rollup, etc.): blocker.
- [ ] Irrelevant or untested optional example branch: warning at most.
- [ ] Specific, paste-ready comments and correctly categorized verdicts.
- [ ] Re-review drops resolved findings and catches regressions.

### Deliverables

1. A branch and PR against `accelerate-data/vibedata-cookbooks:pre-prod` containing focused CI, tests, template, and documentation changes. **Do not merge automatically.**
2. The complete updated `vibedata-recipe-review` skill, including supporting references, packaged as one validated ZIP (or an equivalent PR if its source repository exists and is writable).
3. Test/validation results and a short mapping from each requirement to changed files.
4. A record of GitHub ruleset/approval settings that were actually enforced, or a precise manual configuration checklist for those that could not be changed.
5. A clearly separated follow-up for disabling Recipe invocation on website/Studio when `readiness: planned`, if not implemented in the same authorized scope.

## 7. Explicit non-goals

- No bulk re-authoring of existing Recipe definitions.
- No requirement to prove every supported platform using a separate implementation example.
- No new Recipe schema field merely to describe `planned` readiness or implementation history.
- No new persistent evidence registry or extra artifact for compatibility assessments.
- No Google Drive/Domain Bundle review, validation, secret scanning, or dependency for publication approval.
- No probabilistic/LLM grading as a required deterministic CI status.
- No automatic fixing, rewriting, or merging of author-submitted Recipes.
- No change to existing catalog post-merge generation or the protected promotion model.

## 8. Coding-agent execution order

1. Compare this spec with current `pre-prod`, inspect the attached skill, and note any current-file drift.
2. Update and validate the semantic skill; run its controlled review cases.
3. Change the Cookbook PR template and contributor documentation.
4. Implement the smallest deterministic CI additions and regression tests; fix the `proven` test contradiction.
5. Run the full test suite and prove PR CI remains read-only.
6. Check/configure GitHub review protections; report unavailable admin changes accurately.
7. Prepare the Cookbook PR and the updated skill package; document the separate consumer-readiness follow-up.

**Decision rule:** If a proposed implementation cannot be enforced deterministically from trusted repository/PR data, keep it in the semantic skill and human review. Do not replace judgment with a keyword-based CI approximation.
