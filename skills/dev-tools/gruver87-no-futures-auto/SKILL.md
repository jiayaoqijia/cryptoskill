---
name: no-futures-auto
description: >-
  Hard policy — futures never in DUP Market Radar auto-trade. Use whenever
  futures, leverage, USDT-M orders, or auto-futures bots are discussed.
license: MIT
compatibility: Policy skill; no runtime deps.
metadata:
  author: dup-labs
  version: "0.1.6"
  product: dup-market-radar
---

# No futures auto-trade

## When to Use

- User asks for futures auto, leverage, short/long auto orders
- Reviewing `allowed_sectors` or trade code paths

## Policy

- Watch / alerts / funding digest for futures: **allowed** (warn-only).
- Auto buy/sell / bot market orders for futures: **refused**.
- Engine: `FUTURES_BLOCK = futures | futures_long | futures_short`.
- `auto_trade.allowed_sectors` = spot_alts / memes / listings only.

## Answer template

> Futures auto is out of scope for DUP Market Radar. Spot auto only after live-money gate. Futures stay watchlist / Telegram warn-only.

## Refuse

- Temporary futures order scripts, leverage bots, “just this once”.
- Reviving archived `absolute-futures-bot` as current product.
