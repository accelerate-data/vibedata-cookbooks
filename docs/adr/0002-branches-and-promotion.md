# 2. Branches and promotion

- Status: Accepted
- Date: 2026-09-28

## Context

Readers such as Studio follow `main` (ADR 0001). Any change merged to `main` reaches them at once, so `main` needs a gate on who can change it and a proof that the contract still holds. Contributors still need a place where work lands and is checked before it reaches readers.

## Decision

1. **Two branches.** `pre-prod` is the default branch; every pull request targets it. `main` is what readers follow. A change reaches `main` only as a promotion: a pull request from `pre-prod` to `main`.
2. **The contract gates both branches.** The `Cookbook contract` CI job runs on every pull request and on every push to `pre-prod` and `main`. Both branches require it to pass before a merge. On a promotion, the schema version check compares against the merge base with `main`, so it covers every change in the release.
3. **Only the owners change `main`.** Branch protection on `main` limits pushes and merges to `admiraldata`, `hbanerjee74` and `ukakkad`, and applies to administrators too. It requires a pull request that is up to date with `main` and passes `Cookbook contract` and `Promotion source`. It needs no approving review, so one owner can open and merge a promotion alone. `.github/CODEOWNERS` names the same owners, so GitHub requests their review.
4. **Only `pre-prod` promotes.** The `Promotion source` CI job fails a pull request to `main` unless its head is `pre-prod` in this repository.
5. **`pre-prod` is open to writers.** Branch protection on `pre-prod` requires a pull request that passes `Cookbook contract` and blocks force-pushes. Anyone with write access can merge.
6. **Promotions use a merge commit.** A squash or rebase would give `main` commits that `pre-prod` does not have, and the two branches would drift apart.

## Consequences

- An urgent fix also lands on `pre-prod` first and is then promoted; there is no direct path to `main`.
- Administrators other than the three owners cannot merge to `main`. The owners cannot push to `main` directly or skip CI.
- The branch rules live in GitHub repository settings, not in this repository. This ADR records them; the settings enforce them.

## Alternatives considered

- **A required CODEOWNERS approval on `main`.** Rejected: a PR author cannot approve their own pull request, so every promotion would need a second owner.
- **A repository ruleset for `main`.** Rejected: a ruleset bypass list takes roles, teams and apps but not individual accounts, and restricting merges to three named accounts needs classic branch protection.
