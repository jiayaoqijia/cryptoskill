# Rule language

Shared by trading-scanner, trading-backtest and trading-chart `--eval`. A rule is one expression
evaluated on every bar. Comparisons give true/false; arithmetic gives numbers.

## Fields

`open high low close volume hl2 hlc3 ohlc4 bar_index`

## Operators

`+ - * / % **`  `> >= < <= == !=`  `and or not` (also `&&`, `||`, `AND`, `OR`)

## Functions

Arguments are positional. `[src,]` means the source series is optional (defaults to `close`).

| function | meaning |
|---|---|
| `sma([src,] n)` `ema` `wma` `rma` | moving averages (rma = Wilder) |
| `stdev([src,] n)` `zscore([src,] n)` | dispersion |
| `rsi([src,] n=14)` | Wilder RSI |
| `roc([src,] n)` `pct_change([src,] n=1)` `change([src,] n=1)` | momentum (% / % / absolute) |
| `slope([src,] n)` | regression slope, % per bar |
| `atr(n=14)` `atr_pct(n=14)` | average true range (absolute / % of close) |
| `bb_upper([src,] n=20, k=2)` `bb_lower` `bb_mid` `bb_width` | Bollinger Bands (`bb_width` in % of mid) |
| `kc_upper(n=20, mult=1.5)` `kc_lower` `kc_mid` | Keltner channel |
| `macd(fast, slow, signal)` `macd_signal(...)` `macd_hist(...)` | MACD (defaults 12, 26, 9) |
| `adx(n=14)` `plus_di(n)` `minus_di(n)` | trend strength / direction |
| `stoch_k(n=14, k=3, d=3)` `stoch_d(...)` | stochastic |
| `cci(n=20)` `mfi(n=14)` | CCI, money flow index |
| `supertrend(n=10, mult=3)` `supertrend_dir(n, mult)` | Supertrend line / direction (+1/-1) |
| `vwap()` `obv()` | session VWAP (intraday) / on-balance volume |
| `highest([src,] n)` `lowest([src,] n)` | rolling max (default `high`) / min (default `low`) |
| `shift(src, n=1)` `ref(src, n)` | value n bars ago |
| `cross_above(a, b)` `cross_below(a, b)` | crossed this bar |
| `rising([src,] n=3)` `falling([src,] n=3)` | strictly rising/falling for n bars |
| `rel_volume(n=50)` | volume / average of the prior n bars |
| `pct_from_high(n=252)` `pct_from_low(n=252)` | % from n-bar high (<= 0) / low (>= 0) |
| `realized_vol(n=20)` | annualized volatility % |
| `percentile(src, n)` | rank of the current value within the last n (0-100) |
| `abs(x)` `sqrt(x)` `log(x)` `max(a, b, ...)` `min(a, b, ...)` | math |

## Examples

```text
close > sma(200) and rsi(2) < 10                         # pullback in uptrend
cross_above(ema(20), ema(50))                            # EMA crossover today
close > shift(highest(high, 20), 1) and rel_volume(50) > 1.5   # 20-day breakout on volume
percentile(bb_width(20), 120) <= 10                      # volatility squeeze
pct_from_high(252) >= -5 and adx(14) > 25                # strong trend near highs
close < bb_lower(20, 2) and rsi(14) < 30                 # stretched below the band
sma(close * volume, 50) > 10000000                       # liquidity filter
```

Notes:
- `highest(high, 20)` includes the current bar; use `shift(highest(high, 20), 1)` for "prior 20-bar high".
- During indicator warm-up values are empty and comparisons are false.
- Validate a rule without data: `python3 scripts/screen.py --check "RULE"`.
