---
name: agentic-opportunity-hunter
description: Screen and claim free agentic-BSC mints and airdrops.
---

# Agentic opportunity hunter

Pipeline for the BSC "free stuff" lane: watchlist + X discovery -> on-chain verification -> preview-gated execution -> ledger -> daily digest. For the Agentic Wallet (keyless, `baw`).

## Files

All under `~/.hermes/scripts/hunter/`:

- `hunter_lib.py` — RPC rotation, selector table, Sourcify ABI, risk scan, ledger I/O.
- `hunter_scan.py` — poll watchlist + X feed, verify each contract, print ONLY new eligible items.
- `hunter_intake.py 0xADDR "name"` — verify one address (from a tweet/chat) and add to watchlist.
- `hunter_act.py` — execute eligible rows through `baw contract-call` with the safety gate.
- `hunter_digest.py` — daily 24h summary (found / executed / gas / holdings / balance).
- `selectors.json` — precomputed function selectors. Keep this: `/usr/bin/python3` has no pycryptodome, so scripts must work without importing Crypto.

Data: `~/.hermes/data/hunter_watchlist.json`, `hunter_ledger.jsonl` (append-only), `hunter_state.json`, `hunter_auto` (arming flag).

## Verdicts

`eligible` = free + open + verified + no owner levers + not held/claimed. `held` = already in wallet. `watch` = paid, paused, unverified, risky ABI, already claimed, or the free call reverts. `reject` = no bytecode.

Risk levers that force `watch`: blacklist/setTax/setFee/setTrading/upgrade/withdraw in the ABI (view functions ignored).

## Safety gate (do not weaken)

1. Free only: `--value 0`, never a paid mint and never an approval.
2. `baw contract-call preview` must show an incoming asset, zero allowance/authority changes and zero risks. Otherwise nothing is sent.
3. Execution only when `~/.hermes/data/hunter_auto` exists. Without it the job only proposes.
4. Never auto-execute a candidate from a tweet unless `hunter_intake` returned `eligible`.

Arm: `touch ~/.hermes/data/hunter_auto`. Disarm: `rm ~/.hermes/data/hunter_auto`.

**After arming, prove it with one run and keep the dead-session path silent.** Run `hunter_act.py`
once: armed with nothing claimable it must exit 0 with empty stdout. If the wallet session has expired
every preview answers `SESSION_EXPIRED`, so treat auth errors (`SESSION_EXPIRED`, `NOT_LOGGED_IN`,
`UNAUTHORIZED`) as a non-event — no ledger row, no message — or the 30-minute job rewrites the ledger
and reports the same failure forever. Re-login is the user's QR/link step: see `agentic-wallet-ops` →
"Re-auth from a headless box is a link, not a QR".

## Cron (installed)

- `hunter scan 30m` — `*/30 * * * *`, silent unless something new is eligible.
- `hunter act 30m` — `5,35 * * * *`, proposes (or executes when armed).
- `hunter digest harian` — `0 20 * * *`.
- `hunter discovery X 2x` — `0 9,21 * * *`, agent job with web tools, `deliver: local`, feeds the watchlist.

## Pitfalls

- **A proposal is not a mint.** The cron message only names a candidate; `hunter_act` proposes and
  stops unless armed. Before answering "udah di mint?", read the latest ledger row (`executed` flag)
  and `balanceOf(wallet)` on the contract, then name which blocker applies — not armed, or the wallet
  session is dead. Both leave the wallet untouched and saying "should be minted" is wrong.
- X search cannot be scraped from the VPS: nitter mirrors are dead (451/403) and Google News RSS ignores `site:`. Per-tweet text is reachable via `https://api.fxtwitter.com/status/<id>`. Discovery therefore runs as an agent job using `web_search`.
- `publicnode` rate-limits (`limit exceeded`) after heavy `eth_getLogs` scanning; rotate to `bsc-dataseed.binance.org`.
- Free phases reverting with `phase pause` are normal: the scanner reports "belum buka".
- Exit liquidity is the bottleneck: the Element API key is still pending, so acquired NFTs cannot be listed and "sell at 5x" cannot be automated. Never claim otherwise in reports.
- Ledger is append-only; `hunter_act` only considers the latest row per contract.
