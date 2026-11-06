---
repo: va-mmcx-terminal
parent: perps-review-pr
---
## Terminal criteria

Required for Terminal changes, in addition to the Perps families above.

- [ ] Provider-Agnostic Perps Code: Hyperliquid-specific logic stays behind the `@metamask/perps-controller` provider interface, never in UI or feature code. See references/terminal.md#provider-agnostic-perps-code
- [ ] Mobile Parity: Before implementation, MetaMask Mobile's matching flow, validation, copy and controller use are checked and matched unless the ticket explicitly requires a difference, which the PR explains. See references/terminal.md#mobile-parity
- [ ] Reuse and Types: Controller and shared utilities, and Mobile's controller selectors, actions and state shape, are reused with no parallel state or copied logic. See references/terminal.md#reuse-and-types

## Verdict and handoff

- [ ] Write artifacts/review.md with Summary, Criteria outcomes, Findings, Evidence, Limitations and Recommended Action. Include the frozen head, the rule revision and each consumer revision read. Findings need severity, file:line, impact and the smallest correction. Preserve prior findings and their re-review disposition. Follow the host's required verdict/header fields. Distinguish runtime QA requests from static conclusions.
- [ ] Decide APPROVE or REQUEST_CHANGES. APPROVE needs an empty BLOCKERS list; non-blocking nits may come with it. REQUEST_CHANGES names each blocker with a concrete ask. COMMENT is only for a draft PR or an explicitly informational request. A row the reviewer could not check (no reference checkout, no runtime) goes under Limitations as "not verified by this review" and does not block APPROVE. Evidence the author owes, such as runtime behaviour a PR claims without the proof its repository guidelines require, is a NIT or BLOCKER with a concrete ask, never a silent COMMENT. A pass/issues host maps APPROVE to pass and REQUEST_CHANGES to issues. For pass, keep issues empty; retain non-blocking nits in review.md and line-comments.json under the host contract.
- [ ] Write artifacts/line-comments.json using the host contract, or {"pr_number": <number>, "recommendation": "APPROVE|REQUEST_CHANGES|COMMENT", "summary": "...", "comments": [{"path": "...", "line": 1, "body": "...", "severity": "must_fix|suggestion|nitpick"}]} for a PR task. Only attach changed-line findings; retain other findings in review.md. Write artifacts/learnings.md. For a branch-only review, use an empty comments array without inventing a PR number when the terminal contract requires that file.
- [ ] Reconcile the changed-file/acceptance-criteria inventory with the rule outcomes before choosing a verdict. Every applicable rule needs evidence or an explicit gap: a gap the author owes is a finding, a reviewer-side gap is listed as not verified. In a hosted child checklist, return the report to the caller without completing the parent. For a standalone materialized task, satisfy inputs/worker-terminal-contract.json and its completion command. The caller owns publication, retained sessions and cleanup.
