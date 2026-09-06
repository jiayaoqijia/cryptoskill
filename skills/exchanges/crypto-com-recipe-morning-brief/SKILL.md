---
name: recipe-morning-brief
description: Morning market + portfolio briefing — prices, positions, P&L, overnight orders — as a single structured report.
---

# Morning Brief

## When to Use

- Start-of-day status check
- Daily automated report (cron / scheduler)
- Pre-market dashboard before trading session begins

Requires authentication for the portfolio half. The market half is public.

## Workflow

```
# --- Market half (public) ---

# 1. Market-wide snapshot
cdcx market ticker -o json > /tmp/cdcx-tickers.json

# 2. Top movers: pick N largest |change_24h|
jq '.data[] | {i:.i, last:.a, chg:(.c|tonumber)}' /tmp/cdcx-tickers.json | \
    jq -s 'sort_by(-(.chg|fabs)) | .[0:10]'

# --- Portfolio half (auth) ---

# 3. Cash balances
cdcx account summary -o json

# 4. Open positions + unrealized P&L
cdcx account positions -o json

# 5. Open orders left from overnight
cdcx trade open-orders -o json
cdcx advanced open-orders -o json

# 6. Yesterday's realized activity
cdcx history trades --start-time $(date -v-1d +%s)000 -o json
cdcx history transactions --start-time $(date -v-1d +%s)000 -o json

# 7. Equity curve snapshot
cdcx account balance-history --timeframe D1 -o json
```

(Note: `date -v-1d` is BSD/macOS. On GNU coreutils use `date -d '1 day ago' +%s`.)

## Assembled Report

Combine the above into a text briefing:

```
=== CDCX Morning Brief — $(date +%Y-%m-%d) ===

TOP MOVERS
  BTC_USDT        +3.2%   @ 51,250
  ETH_USDT        +2.1%   @ 2,820
  SOL_USDT        -4.5%   @  141

PORTFOLIO
  Cash:           12,450 USDT
  Positions:      3 open (BTC_USDT long, ETH_USDT long, SOL_USDT short)
  Unrealized P&L: +245 USDT

OVERNIGHT ORDERS
  2 open limit orders on BTC_USDT
  1 OTOCO bracket on ETH_USDT

YESTERDAY
  4 fills, 850 USDT realized P&L
```

## Notes

- `cdcx account balance-history` is useful for charting equity curves over time
- `c` field in ticker is a 24h change ratio (multiply by 100 for percent)
- `history trades` and `history transactions` take `--start-time` / `--end-time` as milliseconds-since-epoch
- Advanced orders (OTO/OTOCO) live in a separate namespace — include `cdcx advanced open-orders` or they'll be missed
