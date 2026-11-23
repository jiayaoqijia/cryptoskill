# Worked case: Metina (metina.id) vs Meteora — Sep 2026

User dropped `https://x.com/MetinaID` and asked *"platform LP-nya gimana kalau ini? dibanding
meteora"*. Answer that landed: **it is not a competing LP platform — it is a UI layer on top of
Meteora**, so "pindah ke Metina" does not exist. Rating 7/10 as a manual helper tool (Meteora
protocol stays 8,5/10).

## What it turned out to be

Community tools for the LP Army, Indonesia. Built by **Yanman (@0xyanman)** with @dojigato and
@lifeatfarrel. X account created **2025-09-25** (snowflake `id 1971033495960158211`), 852 followers,
368 tweets, following 6 → small, young, single-dev project. Self-described funding = the dev's own
trading/LP profit + donations (no VC, no token, no points).

## Numbers verified by audit (all keyless, read-only)

| Probe | Result | Reading |
|---|---|---|
| `api.fxtwitter.com/MetinaID` | 852 followers, 368 tweets, "Managed by @0xyanman…🇮🇩" | indie, ~1 year old |
| `metina.id/api/online-users` | **count 3** | real concurrent usage is tiny |
| `metina.id/api/donate`, `/api/donations` | free-text rows: `fake_signature_12345`, "Hacker Donator", `<script>alert(1)</script>`, `<img src=x onerror=alert(1)>`, wallets "aaaaa" / "Sir_...ell_" | **not** verified revenue + stored-XSS finding |
| `_buildManifest.js` routes | `/pool /token-safety /portfolio /pnl-card /wrapper /treasury /monitor /donate /admin/evm-calendar` | full feature map, incl. `/admin/*` shipped publicly |
| chunk host grep | `dlmm.datapi.meteora.ag`, `damm-v2.datapi.meteora.ag`, `rugcheck.xyz`, Binance/Coinbase/CoinGecko, deepnets.ai | **data provenance = Meteora's own public API**; no proprietary data |
| `dlmm.datapi.meteora.ag/portfolio/total?user=<our wallet>` | `totalPnlUsd 50.18`, `totalPnlSol 0.5216`, `totalClosedPositions 17` | third-party PnL check |
| `…/portfolio?user=<our wallet>&page=1` | deposit $1.724,06 · withdrawal $1.739,82 · fee $34,43 (12 pools incl. 4 ghost pools with $0 deposit) | failed opens leave zero-deposit position accounts |

Features worth stealing for our stack: portfolio/PnL tracker (address-paste, no wallet connect),
PnL card generator (shareable image/video = content proof), treasury outflow tracker (accounting),
pool scanner across DLMM + DAMM v2. Not usable: `/monitor` auto-opens 0.1 SOL from **their** wallet
via `POST /api/meteora/launch`; client chunk sends no credentials, so it looks unauthenticated — did
**not** test-fire it, it touches their funds.

## The finding that mattered most for us

Our engine DB held **7 live closed positions (+$43.12)**; the protocol's own API reported
**17 closed positions / +$50.18 / +0.5216 SOL**; the chain wallet was still **−0,2498 SOL below the
3,14485 SOL return-of-capital line**. Three sources, three numbers — report all of them, and use the
protocol API as the standing independent check (see `references/web-tool-audit-recipe.md` §5).

## Reusable pitfalls this case produced

- Tool vs protocol is a *layer* question, not an A-vs-B question: say which question each answers,
  then rate both. A front-end that only re-serves the incumbent's API adds zero liquidity and cannot
  replace it.
- A tool's own `POST`/action endpoint is off-limits during DD (spends their money) — read-only is the
  rule; "looks unauthenticated" is a written finding, not something to demonstrate.
- Unverified donation/leaderboard APIs are not traction. Check the *shape* of the payload (free-text
  amount + wallet + signature = no verification) before quoting any total.
- Audit the bundle before believing the marketing: route list + upstream host list is ~3 commands and
  answers "what is this really?" faster than any docs page.
- Report in the user's framing (Indonesian, casual, numbers first) and save the note to
  `~/obsidian-vault/Ide Project - Metina (Tool LP Solana) vs Meteora.md` — the note is part of the
  deliverable, don't ask whether to write it.
