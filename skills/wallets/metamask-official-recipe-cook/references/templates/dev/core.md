---
platforms: [core, cli]
description: Core dev checklist with runtime proof.
---

# Core dev checklist

Read and apply `.agents/skills/mms-recipe-cook/references/dev-fix-bug.md` before step 1. Use its matching flow/platform rules at every gate.

## Setup

- [ ] 1. Confirm checklist handoff.
- [ ] 2. Capture task/ACs and bind the recorded harness.
- [ ] 3. Sandbox ready.
- [ ] 4. Local task branch.

## Plan

- [ ] 5. Approach. Include a real commit subject when the task title is empty or generic; use it for any requested product commit.
- [ ] 6. AC matrix.
- [ ] 7. Target and rationale.
- [ ] 8. Proof plan: the recipe drives the controller through its public API as Mobile or Extension do (real messenger, mocked only at the network boundary) and asserts the observable state or event; a Jest or unit-test probe is never the proof. Apply the shared Mainnet policy.
  - Sign real testnet orders only with a testnet-wallet fixture; otherwise use read paths and record why.
- [ ] 9. Recipe drafted and pre-implementation proof.

## Implement

- [ ] 10. Implement the gated, AC-mapped change.
- [ ] 11. Harness diff check.

## Validate

- [ ] 12. Focused tests and required build/export checks.
- [ ] 13. Recipe run and state/log inspection.

## Self-review

- [ ] 14. Full-diff self-review.
- [ ] 15. Domain checks with parent step 15.
- [ ] 16. Rerun proof or record no-rerun.

## Report

- [ ] 17. Coverage and per-AC acceptance verdicts.
- [ ] 18. Render PR body, retain terminal artifacts and complete.

When the frozen terminal contract requires `artifacts/recipe-decision.json`, use the shared proof-decision fields; diagnose and repair missing runtime prerequisites first.
