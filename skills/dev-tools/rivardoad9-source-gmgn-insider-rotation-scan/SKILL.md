---
name: gmgn-insider-rotation-scan
description: Detect insider wallets & whale rotation in low caps.
version: 1.0.0
author: Hermes
license: MIT
metadata:
  tool: ~/.hermes/scripts/insider_scan.py
  db: ~/.hermes/data/lowcap_alert.db
  platforms: [linux]
  hermes:
    tags: [crypto, gmgn, onchain, lowcap, insider, wallet-rotation]
    related_skills: [gmgn-holder-analysis, gmgn-wallet-analysis, lowcap-priority-alerts]
---

# Insider & wallet-rotation scan (GMGN meme / low cap)

## When to use

- "Ada wallet insider yang masuk nggak di token X?"
- "Wallet yang beli itu track record-nya bagus nggak?"
- "Bisa track whale yang pindah-pindah / cuci wallet?"
- As the enrichment step of the low-cap alert card (P2/P3 lanes).

Chains: `sol`, `bsc`, `base`, `eth`, `arbitrum`, `hyperevm`, `robinhood`, `arc`, `stable`.
**GMGN does NOT support Plasma** — for XPL/Plasma use the Routescan API instead.

## Steps

```bash
export PATH="$HOME/.local/bin:$PATH"
gmgn-cli config --check                                        # must exit 0

python3 ~/.hermes/scripts/insider_scan.py --chain <c> --address <a>   # human card
python3 ~/.hermes/scripts/insider_scan.py --chain <c> --address <a> --json
python3 ~/.hermes/scripts/insider_scan.py --selftest           # offline, no network
```

Then, only for wallets that carry a real track record, pull the record:

```bash
gmgn-cli portfolio profits --chain <c> --wallet <A> --wallet <B> --period all --raw
gmgn-cli portfolio stats   --chain <c> --wallet <A> --period 7d --raw
```

`--wallet` is repeatable, but **`portfolio stats` only returns the FIRST wallet** when passed
several — call it once per wallet, or rely on `profits` for the multi-wallet view.

## The metrics that matter, in order

1. **Free-token ratio** — `buy_volume_cur == 0` while `balance > 0`. Verified near-identical to the
   `transfer_in` tag (boar: 60 of 64 overlap; every wallet with `buy_volume_cur > 0` had
   `transfer_in_count == 0`). Report the **ratio**: 3% is unremarkable, **45–66% means the holder
   base was allocated, not bought**.
2. **Smart money = 0 is a real answer.** Across 189 top-trader wallets in 5 tokens, `smart_degen`,
   `pump_smart`, and `renowned` scored **zero**. Only 2 wallets carried `kol`. Do not manufacture a
   smart-money finding out of `transfer_in` or `whale`.
3. **Insider tags** — `bundler`, `sniper`, `sandwich_bot`, `rat_trader`, `creator`, `wash_trader`,
   `fresh_wallet`. A tall bundler count (23, 32, 51) is a distribution signal, not adoption.
   Sandwich bots among top traders are value *extractors*, not participants.
4. **Funder clusters** — group holders by `native_transfer.from_address`. A group funded **within
   60s** is a scripted batch (strong). A span of months is weak — a long-running funder is not a
   fresh sybil cluster. Always print the span.
5. **Leaderboards lie.** A "top profit" wallet can be realized-negative: KITTY's #2 profit wallet
   was **−$7,877 realized (−5.8%)**, propped up only by unrealized gains. Always separate realised
   from unrealized.

## Verdict ladder

`INSIDER_DUMP` 🔴 → `SMART_IN` 🟢 → `INSIDER_WARN` 🟡 → `CLEAN` 🟢; `NO_DATA` ⚪ under 10 holders.

Order matters: **strong insider signals outrank smart money.** 4 KOLs plus 23 bundlers is a
sponsored distribution, not a smart-money entry — that exact case is pinned in `--selftest`.

## Track-record expectations (real samples, 27 Sep 2026)

| Wallet | Claim | Reality |
|---|---|---|
| KOL 29K followers (`@NeoCallss`) | "top KOL" | lifetime ROI 18.4%, **7d win-rate 28.6%**, tagged `arbitrager` |
| SEND creator | #1 profit $168K | lifetime $416K realised on $2.38M = 17.5%; 200 of 211 weekly tokens in the 0–2x band |
| NOCK top | +335% | **6 trades total** (2 buys, 4 sells), zero activity for 7 days |
| KITTY top | healthy | ROI ~20%, 7d win-rate 44.4%, 0 losses >50%, funded from Binance |

An `arbitrager` tag means the profit came from spread, not from picking winners. Say so.

## Pitfalls

- **GMGN is a leaky bucket per IP.** `HTTP 429 ... Rate limit resets at <ts> (~Ns remaining)`, and
  **each retry extends the ban by 5s up to 5 minutes**. Never loop-retry. `insider_scan.py` writes
  the reset to `~/.hermes/data/gmgn_cooldown.txt` and refuses further calls until it passes; a file
  lock at `~/.hermes/data/gmgn_gate.txt` enforces a minimum gap across processes.
- `token_transfer_in` / `token_transfer_out` return **empty** on the holders endpoint — do not use
  them for counterparties. Only `native_transfer.from_address` is populated (~35% coverage).
- `holders` needs `--order-by amount_percentage` to be meaningful; filter `addr_type == 0`
  (1 = burn/dead, 2 = DEX/pool) or the percentages skew.
- Don't hand-roll the block format — `fmt_block()` is the single source. Cache (360 min TTL) lives
  in the `insider_scan` table of `lowcap_alert.db`; recompute ratios when reading an old cached row.
- The upstream `gmgn-*` skills are **symlinks to `~/.agents/skills/`** (externally managed) — patch
  them and the change is lost on update. Put local knowledge here instead.

## Verification

- `python3 ~/.hermes/scripts/insider_scan.py --selftest` → must print `LULUS (0 gagal)`.
- Spot-check the free-token count against tags on one token before trusting an unfamiliar field.
