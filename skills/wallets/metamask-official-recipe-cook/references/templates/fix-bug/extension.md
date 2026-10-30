---
platforms: [extension, chrome-extension]
description: Extension fix-bug checklist with runtime proof.
---

# Extension fix-bug checklist

Read and apply `.agents/skills/mms-recipe-cook/references/dev-fix-bug.md` before step 1. Use its matching flow/platform rules at every gate.

## Setup

- [ ] 1. Confirm checklist handoff.
- [ ] 2. Capture task/ACs and bind the recorded harness.
- [ ] 3. Sandbox ready.
- [ ] 4. Local task branch.

## Reproduce

- [ ] 5. AC matrix.
- [ ] 6. Target and rationale. Open sidepanels through the harness helper; mark dependent ACs UNTESTABLE only if still unreachable.
- [ ] 7. Buggy-evidence baseline plan and Mainnet policy.
- [ ] 8. Draft buggy-behavior baseline recipe. Pair ordering, portal or z-index screenshots with a bounding-box read.
- [ ] 9. Recorded baseline run and visual inspection.
- [ ] 10. Early no-change exit if already fixed/not reproduced.
- [ ] 11. Root cause in TASK.md `## Root Cause`: file:line traced from symptom to source.

## Fix

- [ ] 12. Minimal AC-mapped fix.
- [ ] 13. Harness diff check.

## Validate

- [ ] 14. Fixed-behavior after recipe and plan.
- [ ] 15. Recorded after run and before/after evidence gate.
- [ ] 16. Bug-condition tests and changed-file coverage.

## Self-review

- [ ] 17. Full-diff self-review.
- [ ] 18. Domain checks with parent step 18.
- [ ] 19. Rerun proof or record no-rerun.

## Report

- [ ] 20. Coverage and per-AC acceptance verdicts.
- [ ] 21. Render PR body, retain terminal artifacts and complete.
