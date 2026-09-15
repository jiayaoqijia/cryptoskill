---
repo: metamask-extension
parent: performance-attribution
---

## Source & Project

Primary source is Sentry **Trace Explorer** (not Dashboard 219877): <https://metamask.sentry.io/explore/traces/>

- Project `metamask` (ID `273505`), `environment:production`
- Mode `Aggregates`, **Group By** `release`, **Visualize** `p75(span.duration)` and `p95(span.duration)`
- Time `90d` (primary). Dashboard 219877 (30d) is legacy/context only.

## Key Transactions

| Transaction | What it measures |
|---|---|
| `UI Startup` | Extension click → interactive UI. Service-worker boot is a separate trace, rooted under `/service-worker.js`, so background startup work is not in it |
| `/home.html` | Home page render |
| `Asset Details` | Token/NFT detail view render |
| `/notification.html` | dApp confirmation popup (approvals/signatures) — high-frequency for power users, compounds with usage |

## Query Template

```
is_transaction:true environment:production transaction:"UI Startup" (release:metamask-extension@13.11.2 OR release:metamask-extension@13.12.2 OR release:metamask-extension@13.13.1 OR release:metamask-extension@13.14.2 OR release:metamask-extension@13.15.0)
```

Swap the `transaction:"…"` value per metric; keep `statsPeriod=90d`.

## Version Selection — Highest-Sample Patch Per Minor

Anchor each minor line on its highest-sample patch, never the `.0`:

| Minor | Patch used | Rationale |
|---|---|---|
| 13.11 | 13.11.2 | Highest sample count |
| 13.12 | 13.12.2 | Highest sample count |
| 13.13 | 13.13.1 | Highest sample count |
| 13.14 | 13.14.2 | Highest sample count |
| 13.15 | 13.15.0 | Current release |

`.0` releases have **10–100× fewer samples** — never anchor a percentile on a `.0` when a higher patch exists in the same minor line.

## 90d vs 30d — Empirical

30d baselines ran **~2× higher** than 90d for the same metric (e.g. UI Startup p75 `9.39s → 3.47s` at 30d vs `4.40s → 3.34s` at 90d). Cause unconfirmed — residual-user population and/or sampling of residual traffic; **not** confirmed "power users" (no cohort segmentation). Report 90d; cite 30d only for context. Note: Sentry share links may render 30d in the UI even when the report figure is 90d — verify `statsPeriod=90d`.

## Hot-Path Files

| Path | Why it matters |
|---|---|
| `babel.config.js` | Build-time transforms (e.g. React Compiler) — broad scope |
| `ui/selectors/*.js` | Redux selectors — run on every state change |
| `ui/hooks/*.ts` | Hooks — component lifecycle |
| `ui/components/` | Virtualization / render patterns |
| `package.json` | Dependency runtime behavior + core-package bumps |

## Analysis Commands

```bash
git log v13.X.X..v13.Y.Y --oneline --no-merges | wc -l               # commit count between releases
git diff v13.X.X..v13.Y.Y --stat -- ui/selectors babel.config.js     # file-level change summary
git diff v13.X.X..v13.Y.Y -- <file>                                  # detailed diff for one file
git log v13.X.X..v13.Y.Y --oneline -- <paths>                        # commits touching specific paths
```

## Core Packages to Monitor

App-repo diffs miss work shipped as version bumps. Diff `package.json`, then read each package CHANGELOG:

| Package | Performance relevance |
|---|---|
| `@metamask/assets-controllers` | Token detection, balance fetching, NFT metadata |
| `@metamask/transaction-controller` | Transaction state size, history storage |
| `@metamask/network-controller` | RPC call handling, retry logic |

```bash
git diff v13.X.X..v13.Y.Y -- package.json | grep -E '^[-+] +"'   # every changed dependency, @metamask/* and others
```

Example findings:

- `@metamask/transaction-controller` v62.8.0 — deprecated `history` / `sendFlowHistory` from `TransactionMeta` → significant state-size reduction for power users (consumed in extension [#38665](https://github.com/MetaMask/metamask-extension/pull/38665)).
- `@metamask/assets-controllers` v94.0.0 ([core #7408](https://github.com/MetaMask/core/pull/7408)) — Account API v2 → v4 for token detection → fewer RPC calls, delegated detection.
- `@sentry/browser` 10.x: a CI benchmark ceiling breach was traced to this bump (benchmark harness, not production), so read bumps outside `@metamask/*` too.

## Worked Example: v13.11 → v13.15 (90d)

| Metric | p75 (typical) | p95 (tail) |
|---|---|---|
| UI Startup | 4.40s → 3.34s (-24%) | 15.65s → 9.11s (**-42%**, -6.5s) |
| /home.html | 1.69s → 1.19s (-30%) | 4.96s → 3.24s (-35%) |
| Asset Details | 100ms → 47ms (**-53%**) | 287ms → 94ms (**-67%**) |
| /notification.html | 1.36s → 1.05s (-23%) | 4.30s → 4.71s (+9%, **high variance — inconclusive**) |

Most UI Startup gains and the /home.html p95 gain landed in 13.12 (p95 UI Startup -40% in one release). /home.html p75 moved 1.69s → 1.56s in 13.12, 0.13s of its 0.50s drop, and its larger drops came in 13.14–13.15. Asset Details improved across 13.14 → 13.15. Treat the per-release header deltas as measured totals and attribute individual code changes as likely contributors only.
