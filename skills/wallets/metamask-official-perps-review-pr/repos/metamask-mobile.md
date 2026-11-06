---
repo: metamask-mobile
parent: perps-review-pr
---
## Mobile specifics

Apply these Mobile-specific families in addition to the shared checks. Compare changed counterparts using the parity map; do not apply Extension tooling rules to Mobile.

- [ ] Agentic Testability (testIDs): PRs that touch UI components must include testIDs so agentic recipes and E2E tests can navigate and assert on the app without manual interaction. See references/mobile.md#agentic-testability-testids
- [ ] Navigation Exit Parity: A navigation fix must cover every way the user can leave the screen. See references/mobile.md#navigation-exit-parity
- [ ] Native Modal Layout: Modal wrapper omitted in width-constrained layouts — in the Pro layout, parent columns are width-constrained; bottom sheets must be wrapped in a Modal so they are not clipped. See references/mobile.md#native-modal-layout
- [ ] Mobile Controller Integration Mocks: Controller bump treated as lockfile-only — inspect changed controller `dist` call sites against Mobile's hand-written integration mocks, then run the Perps integration suites. See references/mobile.md#mobile-controller-integration-mocks
- [ ] Mobile Trace Instrumentation: Use `docs/perps/perps-sentry-reference.md` for Mobile trace names and lifecycle. See references/mobile.md#mobile-trace-instrumentation
- [ ] Mobile Reference Paths: Mobile UI constants live in `app/components/UI/Perps/constants/perpsConfig.ts`. See references/mobile.md#mobile-reference-paths
- [ ] Run `domains/testing/skills/mobile-testing` by name for Mobile application behavior or test changes. Use its placement reference to inspect coverage and the applicable unit, component-view or integration reference when tests change. Record NOT_CHECKED if the owning skill or required client guidance is unavailable. Skip this delegation when `perps-review-pr` runs as a capability under `pr-workflow/review-pr`; that router already owns specialist routing.
- [ ] Mobile Test Layers: Controller/provider flow faked with mocks — order/close/flip/validation flows must exercise the real `HyperLiquidProvider` / `TradingService` chain through the Perps harnesses… See references/mobile.md#mobile-test-layers

## Verdict and handoff

- [ ] Write artifacts/review.md from references/report-template.md; full ledger to artifacts/review-ledger.md. Copy this template, replace its content and keep its order and marks. Follow the host's verdict/header fields. Keep findings concise, with only one collapsed Details for agents section; preserve full evidence and prior-round history in the ledger.
- [ ] Choose APPROVE, COMMENT or REQUEST_CHANGES using the policy in references/report-template.md. A confirmed Perps anti-pattern remains blocking. Keep the exact recommendation in the host JSON. For a binary pass/issues host, only APPROVE maps to pass; COMMENT and REQUEST_CHANGES map to issues. On pass, keep issues empty and retain non-blocking nits in line-comments.json. Never report an unchecked claim as passed.
- [ ] Write artifacts/line-comments.json using the host contract, or {"pr_number": <number>, "recommendation": "APPROVE|REQUEST_CHANGES|COMMENT", "summary": "...", "comments": [{"path": "...", "line": 1, "body": "...", "severity": "must_fix|suggestion|nitpick"}]} for a PR task. Every actionable in-diff finding belongs in a line comment with its full problem, evidence and concrete ask; the review body is only its short index. Keep unanchored findings in Details for agents rather than inventing a line. Write artifacts/learnings.md. For a branch-only review, use an empty comments array without inventing a PR number when the terminal contract requires that file.
- [ ] Reconcile the changed-file/acceptance-criteria inventory with the rule outcomes before choosing a verdict. Every applicable rule needs evidence or an explicit gap: a gap the author owes is a finding, a reviewer-side gap is listed as not verified. In a hosted child checklist, return the report to the caller without completing the parent. For a standalone materialized task, satisfy inputs/worker-terminal-contract.json and its completion command. The caller owns publication, retained sessions and cleanup.
