---
name: bot-holdout-wait
description: >-
  absolute-trading-bot protocol freeze — MEASUREMENT v1 stopped (no-edge);
  do not retune or enable SPOT_ENTRIES from the old eight-median gate. Use when
  the user asks to retune, optimize, unlock buys, or rewrite MEASUREMENT.md.
license: MIT
compatibility: absolute-trading-bot-final; cite docs/PROTOCOL_STATUS.md and docs/MEASUREMENT.md.
metadata:
  author: dup-labs
  version: "0.1.10"
  product: absolute-trading-bot
---

# Bot protocol freeze (ex-holdout)

## When to Use

- «ретюнь / улучши стратегию / включи входы / SPOT_ENTRIES=1»
- Editing `docs/MEASUREMENT.md` or claiming new edge on v1

## Current policy (as of PROTOCOL_STATUS 2026-11-17)

1. **MEASUREMENT v1 is stopped** — accepted **no-edge** on the current tape.
2. `docs/MEASUREMENT.md` is a **historical** record — do **not** silently rewrite to paint green.
3. `SPOT_ENTRIES` stays **off**. Do **not** unlock buys via the old eight-median unseen gate.
4. Next protocol (v2) only after an **explicit operator decision** written into the repo (not chat-only).
5. Maintained base: KuCoin client, CI, kill switch, gate journal — observe / ops only.

## Steps

1. Read `docs/PROTOCOL_STATUS.md` in `absolute-trading-bot-final`.
2. If user wants retune: refuse silent hyperparameter hunt; propose labeled v2 experiment + evidence folder **only if** they order that step.
3. If user cites old holdout date (e.g. 2026-10-25): note that date was the freeze for the gate run; gate FAIL does **not** unlock entries.

## Answer template

> MEASUREMENT v1 is stopped (no-edge). SPOT_ENTRIES stays off. MEASUREMENT.md is historical — not an unlock path. No retune / no silent rewrite. Next step needs an accepted v2 written in-repo by operator decision.

## Refuse

- Enabling `SPOT_ENTRIES` from failed/old eight-median gate PASS theater.
- Silent retune of stop/take/trail/slippage/pairs under “just improve it”.
- Claiming expectancy without a new labeled evidence pack after an accepted v2.
- Mixing this bot’s paper loop with Market Radar live-money or L1 mesh claims.
