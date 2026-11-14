---
name: trading-scanner
description: Screen any list of stocks, ETFs, crypto or FX pairs with plain-English ideas turned into precise rules (or 14 ready presets like trend-template, momentum-leaders, breakout-volume, oversold-in-uptrend, squeeze, golden-cross), then rank the matches with key columns. Use when the user asks to find, filter or scan for stocks, "which of these are near highs", "show oversold names in an uptrend", wants a watchlist built from criteria, or describes conditions to search for.
license: MIT
metadata:
  author: reddygopalkrishna
  version: "0.2.0"
  pack: trading-skills
---

# Stock Screener (`trading-scanner`)

Translate the user's idea into a rule, validate it, run it on a universe, rank results.

```bash
python3 scripts/screen.py --presets                       # list presets
python3 scripts/screen.py --functions                     # list rule functions
python3 scripts/screen.py --check "close > sma(200) and rsi(2) < 10"
python3 scripts/screen.py --universe assets/watchlists/us-mega-caps.txt --preset trend-template
python3 scripts/screen.py --universe AAPL,MSFT,NVDA,TSLA --rule "pct_from_high(252) >= -5" --rank "roc(63)"
python3 scripts/screen.py --universe my_list.txt --preset breakout-volume --min-dollar-volume 5e6 --save hits.txt
```

## Turning words into rules

1. Map the request to a preset if one fits; otherwise write a rule with the
   [rule language](references/rule-language.md).
2. Run `--check` first if you wrote a custom rule.
3. Always add a liquidity filter for real trading ideas (`--min-price`, `--min-dollar-volume`).
4. Show the exact rule you used so the user can adjust it.

| user says | rule |
|---|---|
| "in an uptrend" | `close > sma(200) and sma(50) > sma(200)` |
| "near 52-week highs" | `pct_from_high(252) >= -5` |
| "oversold" | `rsi(14) < 30` (short-term: `rsi(2) < 10`) |
| "breaking out" | `close > shift(highest(high, 20), 1)` |
| "on big volume" | `rel_volume(50) >= 2` |
| "volatility contracting" | `percentile(bb_width(20), 120) <= 10` |
| "strong trend" | `adx(14) > 25 and plus_di(14) > minus_di(14)` |

## Universe

The user supplies the universe: a text file (one symbol per line), a CSV with a `symbol` column,
or a comma list. Starter lists live in `assets/watchlists/`. The screener does not invent
index membership - if the user names an index, ask for (or help build) the constituent file.
For lists of 300+ symbols expect a few minutes on free data; results are cached for the next run.

## Output

Columns: rank value, close, 1-day change, RSI14, 3-month ROC, relative volume, % from 52w high, ATR%.
`--json` for machine use, `--save FILE` to pass matches to trading-patterns or trading-backtest.
