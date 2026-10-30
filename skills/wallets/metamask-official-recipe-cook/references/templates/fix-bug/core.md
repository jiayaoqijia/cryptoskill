---
platforms: [core, cli]
description: Core fix-bug checklist with runtime proof.
---

# Core fix-bug checklist

Read and apply `.agents/skills/mms-recipe-cook/references/dev-fix-bug.md` before step 1. Use its matching flow/platform rules at every gate.

## Setup

- [ ] 1. Confirm checklist handoff.
- [ ] 2. Capture task/ACs and bind the recorded harness.
- [ ] 3. Sandbox ready.
- [ ] 4. Local task branch.

## Reproduce

- [ ] 5. AC matrix.
- [ ] 6. Package/controller target and fixtures.
- [ ] 7. Discover actions/recipes; record proof decision and Mainnet policy.
- [ ] 8. Draft fixed-behavior baseline recipe when required.
- [ ] 9. Probe setup and retain failing baseline run.
- [ ] 10. Root cause: file:line, affected files and fix plan in `artifacts/approach.md`.
- [ ] 11. Early no-change exit if already fixed/not reproduced.

## Fix

- [ ] 12. Minimal AC-mapped fix.
- [ ] 13. Tests and required build/export checks.
- [ ] 14. Harness fast-profile diff check.

## Validate

- [ ] 15. Required recipe run.
- [ ] 16. Domain smoke when applicable.

## Self-review

- [ ] 17. Full-diff self-review.
- [ ] 18. Domain checks with parent step 18.
- [ ] 19. Rerun proof or record no-rerun.

## Report

- [ ] 20. Recipe coverage when applicable; all AC acceptance verdicts.
- [ ] 21. Render PR body, retain terminal artifacts and complete.
