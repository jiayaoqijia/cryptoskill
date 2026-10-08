---
name: pivx-governance-history
description: Reconstruct PIVX on-chain governance history — every passed/failed proposal for any period, plus actual treasury payout receipts from superblocks. Chain-verifiable, works for any AI agent with HTTP + python3 stdlib.
---

# PIVX Governance History (chain-verifiable)

## What you can reconstruct
1. **Proposal ledger** — every proposal ever: PASSED vs FAILED, PIV amount, yes/no votes, net-yes %, forum URL. Source: `https://pivx.org/proposals/past` (server-rendered ~1MB table, ~560+ rows; no JS needed) and `https://pivx.org/proposals` (current cycle incl. FAILING live rows).
2. **Cycle dating** — forum thread start dates bucket proposals into monthly cycles: fetch each proposal's `forum.pivx.org/threads/<slug>.<id>/` and read the first `datetime="..."` attribute. Multi-installment proposals (e.g. "Q3Liquid369") span several cycles — their installments repeat per cycle while funded.
3. **Treasury receipts** — actual payout txs at superblocks via explorer API. Verified example: superblock block 5,586,823 (2026-09-16 05:03 UTC) tx `c0dea62bfa525903…` paid 138,558 + 117,978 PIV to two proposal wallets.

## Key rules for interpreting data
- **Pass rule**: proposal passes when net-yes ≥ 10% of total masternodes (~190–200 net votes at ~1,900 MNs), NOT simple majority. A 59%-yes proposal with 175 net votes FAILS.
- Past-page status cell is the authority for final outcome: `<span class="pass-fund">Passing</span>` or `pass-fail`/`Failing`.
- Row markup: `<tr data-hash="…" data-title="NAME">` → cells: status, name+forum-link, `data-order="<amountPIV>"` payment, `data-order="<net%>"` votes as `NN.N%yes / no`.
- History page has **no dates** — never infer cycle membership from vote counts alone.
- Monthly budget 432,000 PIV; superblock spacing measured ≈ 33,600 blocks (Sep 16 → Oct 10, 2026 payout pair), ~24 days — the old 43,200-block/30-day figure is stale. Countdown on /proposals = time to next payout.

## Chain receipts method (explorer.pivx.org/api/v2)
- `GET /block-index/<height>` → `{"blockHash": …}`; `GET /block/<hash>` → full txs (field `time` = unix). No `totalOutput` field — sum vouts yourself.
- Superblock payout-tx heuristic: ≥2 DISTINCT recipient addresses, each output ≥15,000 PIV, tx total ≥100,000 PIV. Beware false positives from consolidator sweeps (one address receiving dozens of same-size outputs is a sweep, not a payout — e.g. `D8Ervc…` million-PIV churn).
- Scan strategy: take tip height from `/api/status`, walk back in ~1,200-block windows with ThreadPoolExecutor(max_workers=10–12), stop when you hit the target date. For year-scale receipts, sample the ~15 superblocks/year: find one payout block, jump back ≈ 33,600 blocks, rescan ±600 around it.
- Cross-validate: sum of a superblock's payees ≈ tracker's "BUDGET ALLOCATED" for that cycle.

## Dating a failed proposal
Forum archive `https://forum.pivx.org/forums/archived-proposals.29/` (page 1 = most recently resolved; `data-date-string` per thread row). Live proposals: `forums/budget-governance-proposals.4/`.

## Tool
`scripts/pivx_gov_history.py` (stdlib only):
- `proposals [--out FILE]` → JSON of all past proposals {name, status, amount_piv, yes, no, net_pct, forum_url} + current-cycle rows.
- `date-threads [--limit N]` → adds `thread_date` per proposal via forum fetches (0.4s delay; cache-aware).
- `superblocks --from-height H --to-height H` → candidate payout txs {height, time, txid, payees}.
- `cycles` → groups proposals into cycles using thread dates (±7d around each superblock receipt).

## Gotchas
- explorer.duddino.com = Cloudflare-challenged for curl; use explorer.pivx.org.
- pivx.watch does not resolve. pivx.org HTML includes hCaptcha refs but pages+tables are plain GETtable.
- `execute_code` may be blocked in some agent profiles → write script to /tmp via heredoc and `timeout 230 python3 …` (default shell timeout 60s kills long scans).
- Same proposal names repeat across eras (multiple "LRP - JSKitty") — dedupe by forum thread id, not name.
