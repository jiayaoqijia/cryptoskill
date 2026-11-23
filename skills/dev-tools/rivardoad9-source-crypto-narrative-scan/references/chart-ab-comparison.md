# Chart A/B — picking between two hits in the same narrative (worked 2 Oct 2026)

Trigger: a narrative scan returns a *set* (e.g. gaming meta → IMX / ILV / ALICE). The user's next message
is usually a choice between two of them, often carrying their own read ("ILV kali ya, jujur chartnya lebih
menarik dibanding IMX"). Test that read with numbers. It is often right — the job is to **confirm it with
data and still name the flaw**, not to agree reflexively or to defend the previous ranking.

> SKILL.md could not be patched on this date (curator read-before-write guard vs. skill_view dedup), so
> this file carries the method — treat it as part of the procedure, not an appendix. See also
> `sector-heat-and-trap-checks.md` (same guard, same workaround).

## Data pulls (keyless)

```python
# 365 daily closes. NOTE: the volume series is `total_volumes` — `volume` raises KeyError.
cg(f"coins/{cid}/market_chart?vs_currency=usd&days=365&interval=daily")   # {'prices': [[ms,px]], 'total_volumes': [[ms,v]], 'market_caps': [...]}
cg(f"coins/{cid}?localization=false&market_data=true")                    # supply, MC, FDV, ATH/ATL + %, vol24
# live price + 24h range from the venue the user trades on:
# https://api.binance.com/api/v3/ticker/24hr?symbols=["ILVUSDT","IMXUSDT"]  -> lastPrice, priceChangePercent, highPrice, lowPrice
```

Identify the CoinGecko id explicitly — a plausible-looking ticker string is often a dead token
(`immutable` = $0.0019 dara coin, MC 0; the real one is `immutable-x`). Verify by checking MC/holders.

## Metrics, in the order that decides the pick

| # | Metric | How | What it means |
|---|---|---|---|
| 1 | **Position in 30d/90d range** | `(px - low)/(high - low)` on last 30/90 closes | 100% = breaking to new local highs; 40–60% = mid-range chop (beta without breakout) |
| 2 | **MA stack** | px vs MA7/30/60/90/200 | above all = trend intact; the *distance* also shows how extended the move is |
| 3 | **Higher-lows per month** | bucket daily closes by month, read lows | rising low sequence (Jul 2.74 → Agu 2.85 → Sep 3.01 → Okt 3.90) = structure that survives a pullback |
| 4 | **Legroom to next resistance** | last significant monthly high above spot | the real payoff metric: ILV $5.00–5.21 (+21–26%) vs IMX $0.1906 (+6%) — same narrative, very different upside |
| 5 | **Volume confirmation** | `avg(vol[-7:]) / avg(vol[-30:])` | >1 = volume expanding into the move (confirmed); <1 = price up on *shrinking* volume = unconfirmed breakout (ILV 0.59×) |
| 6 | **MC vs FDV + distance from ATL** | CoinGecko market_data | float/overhang: ILV $34.5M/$40.0M (1.16×) vs IMX $163.1M/$360.6M (2.2×); +54% vs +90% off ATL |

Turnover / liquidity (vol24 vs market cap, and single-venue volume) decides **how to enter**, not whether:
thin book → limit orders, split tranches, never a market buy in size. Quote 24h high/low too, so an
intraday rejection wick (ILV printed $4.29 then fell back to $4.14) can be named instead of hidden.

## Worked example — ILV vs IMX (gaming / GTA6 narrative, 2 Okt 2026)

| | ILV | IMX |
|---|---|---|
| Live | $4.14 (+8.9% 24h) | $0.1787 (+7.3% 24h) |
| 30d/90d range position | **100% / 100%** (new highs) | 85% / 88% (retest of $0.1906) |
| Next resistance | **$5.00–5.21 (+21–26%)** | $0.1906 / $0.2023 (+6% / +12%) |
| Volume avg7/avg30 | **0.59× — shrinking** ⚠ | **1.28× — expanding** ✓ |
| MC / FDV | $34.5M / $40.0M (1.16×) | $163.1M / $360.6M (2.2×) |
| From ATL | +54% (ATL $2.69, 29 Jul) | +90% (ATL $0.0948, 19 Agu) |

Verdict given: **user's instinct valid** — ILV is the higher-torque chart (cleaner structure, far more
legroom, smaller float) → became the pick; IMX kept as the conservative alternative (infra, deeper book).
Counter-evidence stated in the same breath: unconfirmed volume, thin liquidity, intraday rejection.
Closing line that matters: *the two are one bet, don't size both.*

## Report discipline for an A/B

1. Open with "insting lu valid / gak valid" + the two or three numbers that decide it.
2. Then the counter-evidence, unprompted. An honest flaw is what makes the confirmation trustworthy.
3. Concrete plan for the winner only: retest entry zone, tranche 2, invalidation on a **daily close**,
   trim level, 2×/3× levels, and the dated catalyst window.
4. Two names, one narrative = one bet. Say it.
5. Save the comparison table into the dated vault note (new "Revisi <date>" section) and name the file.
6. Hand off to a level-crossing alert rather than promising to "watch" it —
   `hermes-cron-automation` → `references/level-crossing-entry-zone-alerts.md`.
