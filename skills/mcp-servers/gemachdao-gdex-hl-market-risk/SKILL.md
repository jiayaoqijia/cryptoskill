---
name: gdex-hl-market-risk
description: HyperLiquid core-perp risk via GDEX: funding, open interest, oracle premium, leverage caps, delisting for ~234 markets, as NDJSON from a deterministic script.
---

# GDEX: HyperLiquid Market Risk

A read-only risk snapshot of every market on HyperLiquid's **core** perpetual DEX, as served
through GDEX. One JSON object per market.

## Run it

```bash
python3 scripts/hl_market_risk.py                  # all core markets (NDJSON on stdout)
python3 scripts/hl_market_risk.py --symbol BTC ETH
python3 scripts/hl_market_risk.py --active-only
```

Standard library only — no install, no API key. A non-zero exit means the read failed; never
treat it as "no markets".

## Rule for agents

**Report numbers exactly as the script prints them.** Do not estimate, interpolate, round
away precision, or compute new figures in prose. If a figure is needed that the script does
not print, say so.

## Fields

| Field | Meaning |
|---|---|
| `mark_px_usd`, `oracle_px_usd`, `mid_px_usd` | prices, USD |
| `premium_pct` | `(mark − oracle) / oracle`, percent — oracle deviation versus market |
| `funding_hourly_pct` | hourly funding rate, percent (HL's decimal fraction × 100) |
| `open_interest_base` / `open_interest_usd` | OI in coin units / × mark |
| `volume_24h_usd` | 24h notional volume |
| `max_leverage` | protocol cap; **core HL tops out at 40x** |
| `is_delisted` / `is_active` | always present (upstream omits `isDelisted` when false) |

**Delisted markets** (about a quarter of the universe) are kept with `is_active: false` so you
filter deliberately. They have no order book, so `mid_px_usd` and `premium_pct` are absent on
exactly those rows. An *active* market without them makes the script fail loudly.

## Scope

Core DEX only. GDEX also lists ~140 builder-deployed perpetuals (equities, FX, commodities,
indices); they are excluded here on purpose.
