# Recomputing option IV & Greeks (Black-76 on the forward)

`api.option_chains` already carries Deribit's own `mark_iv` and Greeks, but only
for a recent snapshot window. The **trade tape goes back to inception** (Deribit
options since 2016, futures since 2017), so you can recompute implied volatility
and the Greeks for any historical option. This page shows how, and how to verify
the result against the chain.

## The pricing underlying is the forward, not spot

Deribit options are European and priced under **Black-76** off the **per-expiry
forward** `F`, with `r ≈ 0` (the carry is in the forward). `api.option_chains`
exposes both prices, and they are different:

| Column | Meaning |
|---|---|
| `index_price` | spot index (USD reference, used to convert coin premiums to USD) |
| `underlying_price` | the **per-expiry forward** — this is the Black-76 input |
| `mark_price` | mark premium, quoted **in coin** (BTC/ETH) |
| `mark_iv`, `delta`, `gamma`, `vega`, `theta` | Deribit's own values for the same `(F, K, T)` |

Using `index_price` (spot) instead of `underlying_price` (forward) mis-prices by
the basis. Feeding `underlying_price` into Black-76 reproduces Deribit's
`mark_iv` and Greeks to the digit (verified below).

## Model

```
d1 = (ln(F/K) + ½ σ² T) / (σ √T),   d2 = d1 − σ √T
Call = F·N(d1) − K·N(d2),   Put = K·N(−d2) − F·N(−d1)
```

- **IV**: solve `Black(σ) = premium_usd`, where `premium_usd = mark_price × index_price`.
- **Greeks** (closed form; units match Deribit's chain):

```
delta = N(d1)   [call],   N(d1) − 1   [put]
gamma = n(d1) / (F σ √T)
vega  = F·n(d1)·√T / 100             # USD per vol-point
theta = −F·n(d1)·σ / (2 √T) / 365    # USD per day
```

`T = act/365`, `N` = normal CDF, `n` = normal PDF. `mark_iv` is in **percent**
(see data-tables.md), so divide by 100 before use and multiply the result back.

## Recompute + verify in one SQL query

ClickHouse has `erf()` (so `N`/`n` are expressible) and `arrayFold` (to unroll
Newton-Raphson), so IV **and all Greeks** compute server-side. The query returns
each value next to Deribit's own. Newton from an ATM seed is robust near the
money; for deep ITM/OTM (vega → 0, IV not identifiable from price) restrict to
`abs(delta) BETWEEN 0.10 AND 0.90` or use a Python solver (`py_vollib`).

```sql
WITH base AS (
  SELECT instrument_name, option_type AS cp,
         toFloat64(strike) AS K, toFloat64(underlying_price) AS F, toFloat64(index_price) AS S,
         toFloat64(mark_price) AS mark_btc,
         toFloat64(mark_iv) AS d_iv, toFloat64(delta) AS d_delta, toFloat64(gamma) AS d_gamma,
         toFloat64(vega) AS d_vega, toFloat64(theta) AS d_theta,
         (toFloat64(toUnixTimestamp64Nano(expiration)) - toFloat64(toUnixTimestamp64Nano(timestamp)))
           / 1e9 / (365*86400) AS T
  FROM api.option_chains
  WHERE exchange = 'deribit' AND underlying_asset = 'BTC' AND mark_iv > 0 AND mark_price > 0
    AND abs(toFloat64(delta)) BETWEEN 0.10 AND 0.90
    AND dateDiff('day', timestamp, expiration) BETWEEN 5 AND 60
  ORDER BY timestamp DESC LIMIT 300
),
prep AS (
  SELECT *,
    if(cp = 'C', mark_btc*S, mark_btc*S + (F-K)) AS prem_call_usd,   -- put -> call premium (parity, r=0)
    log(F/K) AS lnFK, sqrt(T) AS sqrtT,
    greatest(0.05, sqrt(2*pi()/T)*(mark_btc*S)/F) AS seed            -- Brenner-Subrahmanyam seed
  FROM base
),
solved AS (                                                          -- Newton-Raphson, 40 unrolled steps
  SELECT *,
    arrayFold((acc, i) -> greatest(0.0001,
      acc - ( ( F*0.5*(1+erf(((lnFK+0.5*acc*acc*T)/(acc*sqrtT))/sqrt(2)))
              - K*0.5*(1+erf(((lnFK+0.5*acc*acc*T)/(acc*sqrtT)-acc*sqrtT)/sqrt(2))) ) - prem_call_usd )
            / ( F*exp(-0.5*pow((lnFK+0.5*acc*acc*T)/(acc*sqrtT),2))/sqrt(2*pi())*sqrtT ) ),
      range(60), seed) AS iv
  FROM prep
),
g AS (
  SELECT *, (lnFK+0.5*iv*iv*T)/(iv*sqrtT) AS d1,
            exp(-0.5*pow((lnFK+0.5*iv*iv*T)/(iv*sqrtT),2))/sqrt(2*pi()) AS pdf
  FROM solved
)
SELECT instrument_name, cp,
       round(100*iv,2) AS iv_calc,   round(d_iv,2) AS iv_deribit,
       round(if(cp='C', 0.5*(1+erf(d1/sqrt(2))), 0.5*(1+erf(d1/sqrt(2)))-1), 4) AS delta_calc,
       round(d_delta,4) AS delta_deribit,
       round(pdf/(F*iv*sqrtT), 8) AS gamma_calc,          round(d_gamma,8) AS gamma_deribit,
       round(F*pdf*sqrtT/100, 2) AS vega_calc,            round(d_vega,2)  AS vega_deribit,
       round(-(F*pdf*iv)/(2*sqrtT)/365, 2) AS theta_calc, round(d_theta,2) AS theta_deribit
FROM g ORDER BY iv_calc
```

Near the money (`abs(delta)` ≈ 0.3–0.7) the recomputed IV matches `mark_iv` to a
few hundredths of a vol-point and the Greeks to ~0.1%. Across the `[0.10, 0.90]`
delta band the median IV deviation is ~0.15 vol-point, rising toward the band
edges; `gamma` matches modulo Deribit reporting it to ~1 significant figure. The
in-SQL Newton solver is meant for liquid, near-the-money strikes — in the wings
(`abs(delta)` < ~0.1 or > ~0.9) the option is almost all intrinsic value, vega → 0,
and IV is poorly identifiable from price, so use `py_vollib` (Jäckel's "Let's Be
Rational") for the full surface and sub-day tenors.

## Going beyond the chain window: forward from the futures tape

Deribit **derivatives use suffixed exchange ids** in the trade tape (spot stays
clean), so the deep history lives there:

| Input | Source |
|---|---|
| Option premium | `api.trade` where `exchange = 'deribit-option'` (since 2016; `market` is the instrument, `price` is the premium in coin) |
| Forward `F` | `api.trade` where `exchange = 'deribit-future'` — the matching-expiry dated future is the forward; use the perpetual for very short tenors |
| Index (coin → USD) | the Deribit perpetual, or `deribit` spot |

`ASOF JOIN` the option trade to the nearest dated-future trade at or before it to
recover the forward (it matches the chain's `underlying_price` to ~0.003%), then
run the same Black-76 inversion. **API-id quirk**: the `option_chains` and
`volatility-index` endpoints take plain `deribit`; the trade and OHLCV tapes use
the suffixed `deribit-option` / `deribit-future`.

## Notes

- **DVOL is not a per-option IV.** It is a single 30-day, ATM index value
  (`api.volatility_index` / `/volatility-index`); it is a seed or cross-check,
  never the σ for a specific strike/expiry.
- **Traded vs mark IV.** Inverting a *trade* gives the IV that print executed at;
  `mark_iv` is Deribit's fitted mark. They agree closely but are not identical.
- The in-SQL Newton solver is for near-the-money strikes; for the full surface
  (deep wings, sub-day tenors) use `py_vollib` / `py_vollib_vectorized` (Jäckel's
  "Let's Be Rational"), which is exact across all moneyness.
