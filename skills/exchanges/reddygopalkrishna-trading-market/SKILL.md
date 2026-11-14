---
name: trading-market
description: Classify the current market regime for any index, ETF or crypto benchmark - risk-on uptrend, selective uptrend, choppy, correction or risk-off - from trend (50/200-SMA), momentum, volatility percentile, drawdown and optional breadth across a watchlist, with a suggested exposure level. Use when the user asks "how is the market", "should I be buying now", "is it risk-on", wants market context before trading, or needs to scale position sizes to conditions.
license: MIT
metadata:
  author: reddygopalkrishna
  version: "0.2.0"
  pack: trading-skills
---

# Market Regime (`trading-market`)

Most individual setups fail when the overall market is falling. Check the tide before the waves.

```bash
python3 scripts/regime.py                                   # config benchmark
python3 scripts/regime.py --index ^GSPC
python3 scripts/regime.py --index ^GSPC --universe assets/watchlists/us-mega-caps.txt
python3 scripts/regime.py --index ^GSPC ^FTSE ^N225 ^NSEI BTC-USD   # cross-market dashboard
```

If no benchmark is configured, ask the user which market they trade and suggest the obvious index
(`^GSPC`/`SPY`, `^NDX`, `^FTSE`, `^GDAXI`, `^N225`, `^NSEI`, `^HSI`, `^AXJO`, `BTC-USD`), then offer to
save it with `trading-setup`: `setup.py set account.benchmark ^GSPC`.

## Model

Points from: price vs 200-SMA (+-2), 200-SMA slope, price vs 50-SMA, 50 vs 200, price vs 21-EMA,
3-month momentum, and (with `--universe`) % of stocks above 50/200-SMA. High volatility
(top 20% of the year) cuts exposure one notch.

| score | regime | exposure |
|---|---|---|
| >= 6 (normal vol) | risk-on uptrend | 100% |
| 4-5 | uptrend, selective / volatile | 75% |
| 0-3 | pullback / choppy | 50% |
| -1..-4 | correction | 25% |
| <= -5 | downtrend / risk-off | 0% |

## Using the result

- Multiply the user's normal risk per trade by exposure% when sizing (trading-plan `--risk-pct`).
- In choppy/correction regimes favour fewer trades, quicker profits, tighter stops.
- It is a rules-based description of current conditions, not a forecast of where the market goes next.
