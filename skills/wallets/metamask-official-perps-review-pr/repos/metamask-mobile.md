---
repo: metamask-mobile
parent: perps-review-pr
---
## Mobile specifics

Mobile is the reference implementation for Perps. When a changed screen, hook or formatter has an Extension counterpart, report the divergence against Mobile and never carry an Extension pattern back into Mobile. Extension-only and Core-only families are out of scope for this review.

## Verdict and handoff

- [ ] Write artifacts/review.md with Summary, Criteria outcomes, Findings, Evidence, Limitations and Recommended Action. Include the frozen head and rule revision. Findings need severity, file:line, impact and the smallest correction. Preserve prior findings and their re-review disposition. Required NOT_CHECKED items prevent APPROVE; use COMMENT for missing evidence in standalone reports and REQUEST_CHANGES for actionable findings. If the host only accepts pass/issues, missing required evidence must block the task instead of fabricating an issue or passing it. Follow the host's required verdict/header fields. Distinguish runtime QA requests from static conclusions.
- [ ] Write artifacts/line-comments.json using the host contract, or {"pr_number": <number>, "recommendation": "APPROVE|REQUEST_CHANGES|COMMENT", "summary": "...", "comments": [{"path": "...", "line": 1, "body": "...", "severity": "must_fix|suggestion|nitpick"}]} for a PR task. Only attach changed-line findings; retain other findings in review.md. Write artifacts/learnings.md. For a branch-only review, use an empty comments array without inventing a PR number when the terminal contract requires that file.
- [ ] Confirm every applicable criterion has an outcome and evidence. For a materialized task, satisfy inputs/worker-terminal-contract.json and run the task-local mark complete --mark-last. A blocked review uses mark blocked with its reason. Without a task runtime, return the report and criteria ledger. The caller owns publication, retained sessions and cleanup; stop after handing back the result.
