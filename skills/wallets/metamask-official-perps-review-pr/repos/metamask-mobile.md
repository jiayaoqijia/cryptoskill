---
repo: metamask-mobile
parent: perps-review-pr
---
## Mobile specifics

Apply these Mobile-specific families in addition to the shared checks. Compare changed counterparts using the parity map; do not apply Extension tooling rules to Mobile.

- [ ] Gate Pro screens on both flags
  Prevents: Pro screens silently not showing, or showing when off. See references/shared.md#pro-mode-ui-gating
- [ ] Bound and close every trace
  Prevents: A flood of traces, or traces that never end. See references/shared.md#sentry-tracing
- [ ] Cover every way in and out of a screen
  Prevents: A back button that works from one entry and not another. See references/shared.md#navigation-entry-and-exit-parity
- [ ] Add testIDs to controls
  Prevents: Buttons our recipes cannot press. See references/mobile.md#agentic-testability-testids
- [ ] Handle Android back
  Prevents: Android hardware back skipping a dialog. See references/mobile.md#android-back-paths
- [ ] Keep logic out of components
  Prevents: Logic buried in components where tests cannot reach it. See references/mobile.md#mobile-ui-structure
- [ ] Wrap Pro bottom sheets in a Modal
  Prevents: A bottom sheet clipped in the Pro layout. See references/mobile.md#native-modal-layout
- [ ] Keep the controller mocks current
  Prevents: A controller bump that breaks hand-written mocks unnoticed. See references/mobile.md#mobile-controller-integration-mocks
- [ ] Trace every Mobile screen
  Prevents: Screens with no performance trace, or traces that never end. See references/mobile.md#mobile-trace-instrumentation
- [ ] Mobile Reference Paths
  Mobile UI constants live in `app/components/UI/Perps/constants/perpsConfig.ts`. See references/mobile.md#mobile-reference-paths
- [ ] Run the mobile-testing skill
  Run the installed `mms-mobile-testing` skill by name (`domains/testing/skills/mobile-testing` in a MetaMask/skills checkout) for Mobile application behavior or test changes. Use its placement reference to inspect coverage and the applicable unit, component-view or integration reference when tests change. Record NOT_CHECKED if the owning skill or required client guidance is unavailable. Skip this delegation when `perps-review-pr` runs as a capability under `pr-workflow/review-pr`; that router already owns specialist routing.
- [ ] Exercise the real order flow in tests
  Prevents: Order flows tested with everything mocked. See references/mobile.md#mobile-test-layers

## Verdict and handoff

- [ ] Reconcile outcomes, then choose the verdict
  Prevents: An unchecked rule reported as passed, or a verdict that does not match the findings.
  Reconcile the changed-file/acceptance-criteria inventory with the rule outcomes before choosing a verdict. Every applicable rule needs evidence or an explicit gap: a gap the author owes is a finding, a reviewer-side gap is listed as not verified.
  Choose APPROVE, COMMENT or REQUEST_CHANGES using the policy in references/report-template.md. A confirmed Perps anti-pattern remains blocking. Keep the exact recommendation in the host JSON. For a binary pass/issues host, only APPROVE maps to pass; COMMENT and REQUEST_CHANGES map to issues. On pass, keep issues empty and retain non-blocking nits in line-comments.json. Never report an unchecked claim as passed.
  See references/shared.md#blocking-review-checks
- [ ] Write the review report
  Prevents: A posted review nobody can scan.
  Write artifacts/review.md from references/report-template.md; full ledger to artifacts/review-ledger.md. Copy this template, replace its content and keep its order and marks. Follow the host's verdict/header fields. Keep findings concise, with only one collapsed Details for agents section; preserve full evidence and prior-round history in the ledger.
- [ ] Write line comments and learnings
  Prevents: Findings with no line to act on.
  Write artifacts/line-comments.json using the host contract, or {"pr_number": <number>, "recommendation": "APPROVE|REQUEST_CHANGES|COMMENT", "summary": "...", "comments": [{"path": "...", "line": 1, "body": "...", "severity": "must_fix|suggestion|nitpick"}]} for a PR task. Every actionable in-diff finding belongs in a line comment with its full problem, evidence and concrete ask; the review body is only its short index. Keep unanchored findings in Details for agents rather than inventing a line. Write artifacts/learnings.md. For a branch-only review, use an empty comments array without inventing a PR number when the terminal contract requires that file.
  Mark this row and run the finish command that start printed. The caller owns publication, retained sessions and cleanup.
