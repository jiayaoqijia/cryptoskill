---
repo: core
parent: perps-review-pr
---
## Core criteria

Required for changes to the controller package or its public contract, in addition to the Perps families above.

- [ ] Public Controller Contracts Must Be Versioned and Migration-Aware: A change to controller state shape, method signatures, event names or payloads, or package exports ships with a client migration plan and package-level consumer-style tests. See references/criteria/core/public-controller-contracts-must-be-versioned-and-migration-aware.md
- [ ] Package Release Metadata Must Match Contract Impact: The changelog entry and the semver bump match the contract impact, and a bump PR names the package version and the consumers it was checked against. See references/criteria/core/package-release-metadata-must-match-contract-impact.md
- [ ] HyperLiquid Multi-Sig Account Handling in HyperLiquidProvider: Every user-scoped exchange write in `HyperLiquidProvider` needs both a proactive info probe placed right before the write and a message classifier in its `catch`; HyperLiquid rejects every… See references/criteria/core/hyperliquid-multi-sig-account-handling-in-hyperliquidprovider.md
- [ ] `#ensureUnifiedAccountEnabled` — Retry vs Permanent-Failure Cache Semantics: An attempted unified-account setup that fails either sets the retry flag (`#unifiedAccountSetupNeedsRetry`, transient) or caches `{ attempted: true, enabled: false }` in `TradingReadinessCache`… See references/criteria/core/ensureunifiedaccountenabled-retry-vs-permanent-failure-cache-semantics.md
- [ ] Evidence Expected Before Core Perps Review: The PR carries a contract impact matrix (state, methods, events, exports, constants), a Mobile/Extension compatibility note or paired PR links, provider abstraction and fallback tests, and grep… See references/criteria/core/evidence-expected-before-core-perps-review.md

## Verdict and handoff

- [ ] Write artifacts/review.md with Summary, Criteria outcomes, Findings, Evidence, Limitations and Recommended Action. Include the frozen head and rule revision. Findings need severity, file:line, impact and the smallest correction. Preserve prior findings and their re-review disposition. Required NOT_CHECKED items prevent APPROVE; use COMMENT for missing evidence in standalone reports and REQUEST_CHANGES for actionable findings. If the host only accepts pass/issues, missing required evidence must block the task instead of fabricating an issue or passing it. Follow the host's required verdict/header fields. Distinguish runtime QA requests from static conclusions.
- [ ] Write artifacts/line-comments.json using the host contract, or {"pr_number": <number>, "recommendation": "APPROVE|REQUEST_CHANGES|COMMENT", "summary": "...", "comments": [{"path": "...", "line": 1, "body": "...", "severity": "must_fix|suggestion|nitpick"}]} for a PR task. Only attach changed-line findings; retain other findings in review.md. Write artifacts/learnings.md. For a branch-only review, use an empty comments array without inventing a PR number when the terminal contract requires that file.
- [ ] Confirm every applicable criterion has an outcome and evidence. For a materialized task, satisfy inputs/worker-terminal-contract.json and run the task-local mark complete --mark-last. A blocked review uses mark blocked with its reason. Without a task runtime, return the report and criteria ledger. The caller owns publication, retained sessions and cleanup; stop after handing back the result.
