---
repo: va-mmcx-terminal
parent: perps-review-pr
---
## Terminal criteria

Required for Terminal changes, in addition to the Perps families above.

- [ ] Provider-Agnostic Perps Code
  Hyperliquid-specific logic stays behind the `@metamask/perps-controller` provider interface, never in UI or feature code. See references/terminal.md#provider-agnostic-perps-code
- [ ] Mobile Parity
  Before implementation, MetaMask Mobile's matching flow, validation, copy and controller use are checked and matched unless the ticket explicitly requires a difference, which the PR explains. See references/terminal.md#mobile-parity
- [ ] Reuse and Types
  Controller and shared utilities, and Mobile's controller selectors, actions and state shape, are reused with no parallel state or copied logic. See references/terminal.md#reuse-and-types
- [ ] Legacy Local Formatters
  Terminal's `formatFee`, `formatPercentage`, `formatSize`, `formatTablePrice` and `formatUsd` (`src/features/perpetuals/utils/`) are legacy copies: a PR that uses, extends or calls one migrates that… See references/terminal.md#legacy-local-formatters
- [ ] Forced Testnet
  `config.hyperliquid.forceTestnet` (`src/features/perpetuals/config/hyperliquid.config.ts`) is authoritative: code that reads network state respects it (for example `client-factory.ts`,… See references/terminal.md#forced-testnet

## Verdict and handoff

- [ ] Write the review report
  Write artifacts/review.md from references/report-template.md; full ledger to artifacts/review-ledger.md. Copy this template, replace its content and keep its order and marks. Follow the host's verdict/header fields. Keep findings concise, with only one collapsed Details for agents section; preserve full evidence and prior-round history in the ledger.
- [ ] Choose the recommendation
  Choose APPROVE, COMMENT or REQUEST_CHANGES using the policy in references/report-template.md. A confirmed Perps anti-pattern remains blocking. Keep the exact recommendation in the host JSON. For a binary pass/issues host, only APPROVE maps to pass; COMMENT and REQUEST_CHANGES map to issues. On pass, keep issues empty and retain non-blocking nits in line-comments.json. Never report an unchecked claim as passed.
- [ ] Write line comments and learnings
  Write artifacts/line-comments.json using the host contract, or {"pr_number": <number>, "recommendation": "APPROVE|REQUEST_CHANGES|COMMENT", "summary": "...", "comments": [{"path": "...", "line": 1, "body": "...", "severity": "must_fix|suggestion|nitpick"}]} for a PR task. Every actionable in-diff finding belongs in a line comment with its full problem, evidence and concrete ask; the review body is only its short index. Keep unanchored findings in Details for agents rather than inventing a line. Write artifacts/learnings.md. For a branch-only review, use an empty comments array without inventing a PR number when the terminal contract requires that file.
- [ ] Reconcile outcomes before the verdict
  Reconcile the changed-file/acceptance-criteria inventory with the rule outcomes before choosing a verdict. Every applicable rule needs evidence or an explicit gap: a gap the author owes is a finding, a reviewer-side gap is listed as not verified. In a hosted child checklist, return the report to the caller without completing the parent. For a standalone materialized task, satisfy inputs/worker-terminal-contract.json and its completion command. The caller owns publication, retained sessions and cleanup.
