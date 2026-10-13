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

- [ ] Write artifacts/review.md with Summary, Criteria outcomes, Findings, Evidence, Limitations and Recommended Action. Include the frozen head, the rule revision and each consumer revision read. Findings need severity, file:line, impact and the smallest correction. Preserve prior findings and their re-review disposition. Follow the host's required verdict/header fields. Distinguish runtime QA requests from static conclusions.
- [ ] Decide APPROVE or REQUEST_CHANGES. APPROVE needs an empty BLOCKERS list; non-blocking nits may come with it. REQUEST_CHANGES names each blocker with a concrete ask. COMMENT is only for a draft PR or an explicitly informational request. A row the reviewer could not check (no reference checkout, no runtime) goes under Limitations as "not verified by this review" and does not block APPROVE. Evidence the author owes, such as runtime behaviour a PR claims without the proof its repository guidelines require, is a NIT or BLOCKER with a concrete ask, never a silent COMMENT. A pass/issues host maps APPROVE to pass and REQUEST_CHANGES to issues. For pass, keep issues empty; retain non-blocking nits in review.md and line-comments.json under the host contract.
- [ ] Write artifacts/line-comments.json using the host contract, or {"pr_number": <number>, "recommendation": "APPROVE|REQUEST_CHANGES|COMMENT", "summary": "...", "comments": [{"path": "...", "line": 1, "body": "...", "severity": "must_fix|suggestion|nitpick"}]} for a PR task. Only attach changed-line findings; retain other findings in review.md. Write artifacts/learnings.md. For a branch-only review, use an empty comments array without inventing a PR number when the terminal contract requires that file.
- [ ] Reconcile the changed-file/acceptance-criteria inventory with the rule outcomes before choosing a verdict. Every applicable rule needs evidence or an explicit gap: a gap the author owes is a finding, a reviewer-side gap is listed as not verified. In a hosted child checklist, return the report to the caller without completing the parent. For a standalone materialized task, satisfy inputs/worker-terminal-contract.json and its completion command. The caller owns publication, retained sessions and cleanup.
