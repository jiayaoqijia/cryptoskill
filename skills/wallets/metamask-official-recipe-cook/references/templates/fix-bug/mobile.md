---
platforms: [mobile, ios, android]
description: Mobile fix-bug checklist with runtime proof.
---

# Mobile fix-bug checklist

Read and apply `.agents/skills/mms-recipe-cook/references/dev-fix-bug.md` before step 1. Use its matching flow/platform rules at every gate.

## Setup

- [ ] 1. Confirm checklist handoff.
- [ ] 2. Capture task/ACs and bind the recorded harness.
- [ ] 3. Sandbox ready.
- [ ] 4. Local task branch.

## Reproduce

- [ ] 5. AC matrix. Ticket reference screenshots/recordings make an AC visual.
- [ ] 6. Target and rationale. Mark ACs reachable only on an unavailable platform `UNTESTABLE: wrong platform`; never claim them later.
- [ ] 7. Buggy-evidence baseline plan and Mainnet policy.
- [ ] 8. Add `DevLogger.log('[<ticket>] BUG_MARKER: <condition>')` at the bug condition; observe it in `metro.log` and commit it alone as `debug(<ticket>): add reproduction marker`. Retain SHA/log excerpt.
- [ ] 9. Draft buggy-behavior baseline recipe.
- [ ] 10. Recorded baseline run and visual inspection.
- [ ] 11. Early no-change exit if already fixed/not reproduced.
- [ ] 12. Root cause in TASK.md `## Root Cause`: file:line confirmed from marker, `metro.log` and code path.

## Fix

- [ ] 13. Minimal AC-mapped fix.
- [ ] 14. Harness diff check.

## Validate

- [ ] 15. Fixed-behavior after recipe and plan.
- [ ] 16. Recorded after run and before/after evidence gate.
- [ ] 17. Bug-condition tests and changed-file coverage.
- [ ] 18. Commit only marker removal as `chore(<ticket>): remove reproduction marker`, separately from the fix; afterwards `git diff HEAD` shows only the fix.

## Self-review

- [ ] 19. Full-diff self-review.
- [ ] 20. Domain checks with parent step 20.
- [ ] 21. Rerun proof or record no-rerun.

## Report

- [ ] 22. Coverage and per-AC acceptance verdicts.
- [ ] 23. Render PR body, retain terminal artifacts and complete.
