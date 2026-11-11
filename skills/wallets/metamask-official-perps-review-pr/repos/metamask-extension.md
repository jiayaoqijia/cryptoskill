---
repo: metamask-extension
parent: perps-review-pr
---
## Extension criteria

Required for Extension changes, in addition to the Perps families above.

- [ ] Extension Must Consume the Published Controller Contract
  A controller bump or a `perps-events.ts` merge is proven against the shipped `@metamask/perps-controller` bundle and its `.d.cts`, not against manifests or Mobile assumptions. See references/extension.md#extension-must-consume-the-published-controller-contract
- [ ] Controller Mock Must Be Kept Current
  Every new contract value that product code reads is added to the hand-maintained `test/mocks/metamask-perps-controller.js` in the same PR, otherwise tests silently see `undefined`. See references/extension.md#controller-mock-must-be-kept-current
- [ ] Analytics Wiring Patterns
  Tracker outlives the rendered form: Gate screen-view, abandonment and adjacent subscriptions on the same valid subject and render condition. See references/extension.md#analytics-wiring-patterns
- [ ] Hook Import Boundaries
  Shared perps hooks are imported from their module file, not the `hooks/perps` barrel, stream-module mocks list every hook a component uses, and no hook mutates a caller's ref. See references/extension.md#hook-import-boundaries
- [ ] Market Data Source and Provider Behavior Must Be Consistent Across Paths
  A preferred market data source or provider applies to every fetch path (stream, market detail, order form, charts, fallback) through a typed, visible selection with tested fallback. See references/extension.md#market-data-source-and-provider-behavior-must-be-consistent-across-paths
- [ ] Backend Routing and Controller Preload Caches
  A backend route or provider endpoint change updates the preload and cache-prime paths (`cachedMarketDataByProvider`, `PerpsStreamBridge`'s `startMarketDataPreload`) and the reconnect fallback, not… See references/extension.md#backend-routing-and-controller-preload-caches
- [ ] Order Forms Must Preserve User Input Across Toggles
  A TP/SL sign or percent toggle transforms the existing value, and the submitted order params equal what the form displays. See references/extension.md#order-forms-must-preserve-user-input-across-toggles
- [ ] Charts and CTAs Need Feature-Parity Evidence
  Loading and loaded section order differ: Reserve space for every conditional section above stable controls, including a populated watchlist. See references/extension.md#charts-and-ctas-need-feature-parity-evidence
- [ ] Batch-Action and Analytics Error-Path Parity
  Sibling batch-action handlers (`handleCloseAllPositions`, `handleCancelAllOrders`) share one error contract: the same catch and soft-failure analytics in every sibling, each new branch covered by a… See references/extension.md#batch-action-and-analytics-error-path-parity
- [ ] CDP / E2E Proof Surfaces
  A Perps tab screenshot proves market data only when a non-zero price or position value is visible or a CDP state assertion confirms live data; a navigated route over a loading skeleton is not proof. See references/extension.md#cdp-e2e-proof-surfaces
- [ ] Evidence Expected Before Extension Perps Review
  The PR carries a controller package version and contract compatibility note, a state-flow matrix for the selectors and hooks touched, a market data source matrix across stream, detail, order, chart… See references/extension.md#evidence-expected-before-extension-perps-review
- [ ] Run the extension-testing skill
  Run `domains/testing/skills/extension-testing` by name for Extension application behavior or test changes. Record NOT_CHECKED if the owning skill or required client guidance is unavailable. Skip this delegation when `perps-review-pr` runs as a capability under `pr-workflow/review-pr`; that router already owns specialist routing.

## Verdict and handoff

- [ ] Write the review report
  Write artifacts/review.md from references/report-template.md; full ledger to artifacts/review-ledger.md. Copy this template, replace its content and keep its order and marks. Follow the host's verdict/header fields. Keep findings concise, with only one collapsed Details for agents section; preserve full evidence and prior-round history in the ledger.
- [ ] Choose the recommendation
  Choose APPROVE, COMMENT or REQUEST_CHANGES using the policy in references/report-template.md. A confirmed Perps anti-pattern remains blocking. Keep the exact recommendation in the host JSON. For a binary pass/issues host, only APPROVE maps to pass; COMMENT and REQUEST_CHANGES map to issues. On pass, keep issues empty and retain non-blocking nits in line-comments.json. Never report an unchecked claim as passed.
- [ ] Write line comments and learnings
  Write artifacts/line-comments.json using the host contract, or {"pr_number": <number>, "recommendation": "APPROVE|REQUEST_CHANGES|COMMENT", "summary": "...", "comments": [{"path": "...", "line": 1, "body": "...", "severity": "must_fix|suggestion|nitpick"}]} for a PR task. Every actionable in-diff finding belongs in a line comment with its full problem, evidence and concrete ask; the review body is only its short index. Keep unanchored findings in Details for agents rather than inventing a line. Write artifacts/learnings.md. For a branch-only review, use an empty comments array without inventing a PR number when the terminal contract requires that file.
- [ ] Reconcile outcomes before the verdict
  Reconcile the changed-file/acceptance-criteria inventory with the rule outcomes before choosing a verdict. Every applicable rule needs evidence or an explicit gap: a gap the author owes is a finding, a reviewer-side gap is listed as not verified. In a hosted child checklist, return the report to the caller without completing the parent. For a standalone materialized task, satisfy inputs/worker-terminal-contract.json and its completion command. The caller owns publication, retained sessions and cleanup.
