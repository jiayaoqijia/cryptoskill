---
repo: core
parent: perps-review-pr
---
## Core criteria

Required for changes to the controller package or its public contract, in addition to the Perps families above.

- [ ] Public Controller Contracts Must Be Versioned and Migration-Aware
  A change to controller state shape, method signatures, event names or payloads, or package exports ships with a client migration plan and package-level consumer-style tests. See references/core.md#public-controller-contracts-must-be-versioned-and-migration-aware
- [ ] Package Release Metadata Must Match Contract Impact
  The changelog entry and the semver bump match the contract impact, and a bump PR names the package version and the consumers it was checked against. See references/core.md#package-release-metadata-must-match-contract-impact
- [ ] HyperLiquid Multi-Sig Account Handling in HyperLiquidProvider
  Every user-scoped exchange write in `HyperLiquidProvider` needs both a proactive info probe placed right before the write and a message classifier in its `catch`; HyperLiquid rejects every… See references/core.md#hyperliquid-multi-sig-account-handling-in-hyperliquidprovider
- [ ] `#ensureUnifiedAccountEnabled` — Retry vs Permanent-Failure Cache Semantics
  An attempted unified-account setup that fails either sets the retry flag (`#unifiedAccountSetupNeedsRetry`, transient) or caches `{ attempted: true, enabled: false }` in `TradingReadinessCache`… See references/core.md#ensureunifiedaccountenabled-retry-vs-permanent-failure-cache-semantics
- [ ] Metered Benefits Need a Strict Improvement
  A winning fee source and an actual reduction in the charged fee are separate conditions. See references/core.md#metered-benefits-need-a-strict-improvement
- [ ] Read-only Account Guards Cover Every Write
  Inventory exchange calls, transfers, cancellation, withdrawals and registered venue-key paths before claiming an account is read-only. See references/core.md#read-only-account-guards-cover-every-write
- [ ] One Formatter Surface in the Controller
  Display formatting lives in `src/utils/perpsFormatters.ts` as a few reusable formatters configured by an options object, not one exported function per screen or value. See references/core.md#one-formatter-surface-in-the-controller
- [ ] Provider Rejections Have Two Shapes
  A venue call fails either by throwing or by returning a non-`ok` status result that the caller wraps. See references/core.md#provider-rejections-have-two-shapes
- [ ] Evidence Expected Before Core Perps Review
  The PR carries a contract impact matrix (state, methods, events, exports, constants), a Mobile, Extension and Terminal compatibility note or paired PR links, provider abstraction and fallback tests,… See references/core.md#evidence-expected-before-core-perps-review

## Verdict and handoff

- [ ] Write the review report
  Write artifacts/review.md from references/report-template.md; full ledger to artifacts/review-ledger.md. Copy this template, replace its content and keep its order and marks. Follow the host's verdict/header fields. Keep findings concise, with only one collapsed Details for agents section; preserve full evidence and prior-round history in the ledger.
- [ ] Choose the recommendation
  Choose APPROVE, COMMENT or REQUEST_CHANGES using the policy in references/report-template.md. A confirmed Perps anti-pattern remains blocking. Keep the exact recommendation in the host JSON. For a binary pass/issues host, only APPROVE maps to pass; COMMENT and REQUEST_CHANGES map to issues. On pass, keep issues empty and retain non-blocking nits in line-comments.json. Never report an unchecked claim as passed.
- [ ] Write line comments and learnings
  Write artifacts/line-comments.json using the host contract, or {"pr_number": <number>, "recommendation": "APPROVE|REQUEST_CHANGES|COMMENT", "summary": "...", "comments": [{"path": "...", "line": 1, "body": "...", "severity": "must_fix|suggestion|nitpick"}]} for a PR task. Every actionable in-diff finding belongs in a line comment with its full problem, evidence and concrete ask; the review body is only its short index. Keep unanchored findings in Details for agents rather than inventing a line. Write artifacts/learnings.md. For a branch-only review, use an empty comments array without inventing a PR number when the terminal contract requires that file.
- [ ] Reconcile outcomes before the verdict
  Reconcile the changed-file/acceptance-criteria inventory with the rule outcomes before choosing a verdict. Every applicable rule needs evidence or an explicit gap: a gap the author owes is a finding, a reviewer-side gap is listed as not verified. In a hosted child checklist, return the report to the caller without completing the parent. For a standalone materialized task, satisfy inputs/worker-terminal-contract.json and its completion command. The caller owns publication, retained sessions and cleanup.
