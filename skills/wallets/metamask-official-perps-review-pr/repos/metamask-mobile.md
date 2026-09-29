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
- [ ] Mobile Test Layers: Cover every test in its best-fit layer (view, integration, unit); broad mock-heavy unit tests are a review smell. See references/mobile.md#mobile-test-layers

## Verdict and handoff

- [ ] Write artifacts/review.md with Summary, Criteria outcomes, Findings, Evidence, Limitations and Recommended Action. Include the frozen head and rule revision. Findings need severity, file:line, impact and the smallest correction. Preserve prior findings and their re-review disposition. Required NOT_CHECKED items prevent APPROVE; use COMMENT for missing evidence in standalone reports and REQUEST_CHANGES for actionable findings. If the host only accepts pass/issues, missing required evidence must block the task instead of fabricating an issue or passing it. Follow the host's required verdict/header fields. Distinguish runtime QA requests from static conclusions.
- [ ] Write artifacts/line-comments.json using the host contract, or {"pr_number": <number>, "recommendation": "APPROVE|REQUEST_CHANGES|COMMENT", "summary": "...", "comments": [{"path": "...", "line": 1, "body": "...", "severity": "must_fix|suggestion|nitpick"}]} for a PR task. Only attach changed-line findings; retain other findings in review.md. Write artifacts/learnings.md. For a branch-only review, use an empty comments array without inventing a PR number when the terminal contract requires that file.
- [ ] Reconcile the changed-file/acceptance-criteria inventory with the rule outcomes before choosing a verdict. Every applicable rule needs evidence or an explicit gap; required NOT_CHECKED items prevent approval. In a hosted child checklist, return the report to the caller without completing the parent. For a standalone materialized task, satisfy inputs/worker-terminal-contract.json and its completion command. The caller owns publication, retained sessions and cleanup.
