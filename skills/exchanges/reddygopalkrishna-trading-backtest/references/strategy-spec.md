# Strategy spec

A strategy is a JSON file. Only `entry` is required.

```json
{
  "name": "RSI-2 pullback",
  "universe": ["AAPL", "MSFT", "NVDA"],
  "side": "long",
  "entry": "close > sma(200) and rsi(2) < {oversold}",
  "exit": "close > sma(5)",
  "stop": {"type": "atr", "mult": 2.5, "n": 14},
  "target": null,
  "trail": null,
  "max_bars": 10,
  "sizing": {"type": "risk", "risk_pct": 1.0},
  "max_positions": 5,
  "max_position_pct": 25,
  "rank_by": "-rsi(2)",
  "initial_capital": 100000,
  "costs": {"commission_pct": 0.03, "commission_fixed": 0, "slippage_pct": 0.05},
  "lot_size": 1,
  "fractional": false,
  "oos_start": "2021-01-01",
  "params": {"oversold": 10}
}
```

| key | values | notes |
|---|---|---|
| `entry` | rule | evaluated at each close; fills next bar's open |
| `exit` | rule or null | exit at next open when true |
| `stop` | `{"type":"atr","mult":2,"n":14}` / `{"type":"pct","value":5}` / `{"type":"expr","value":"lowest(low,10)"}` / `{"type":"none"}` | fixed at entry (uses signal-bar values) |
| `target` | `{"type":"r","value":2}` / `{"type":"pct","value":10}` / `{"type":"expr",...}` / null | |
| `trail` | `{"type":"atr","mult":3,"n":14}` / `{"type":"pct","value":8}` / null | ratchets only in your favour, updated at each close |
| `max_bars` | int | time stop, exits at the close of the Nth bar |
| `sizing` | `{"type":"risk","risk_pct":1}` / `{"type":"percent","pct":10}` / `{"type":"fixed","amount":5000}` | risk sizing needs a stop |
| `max_positions` | int | concurrent positions; extra signals ranked by `rank_by` |
| `rank_by` | rule | higher is better; prefix `-` for lower-is-better |
| `oos_start` | date | report in-sample vs out-of-sample separately |
| `params` | object | `{name}` placeholders in any string; override with `--set name=value` |

CLI flags override the file: `--entry --exit --stop atr:2 --target r:2 --trail atr:3 --max-bars 10
--max-positions 5 --risk-pct 0.5 --rank-by "roc(63)" --oos-start 2021-01-01 --set oversold=5`.

## Execution assumptions

Signals at the close, fills at the next open (+slippage). Stops fill at the stop or at the open on
gaps (+slippage). Targets fill at the target. Same-bar stop and target -> stop first. The entry bar
can stop out. Open positions are closed at the last bar. Cash-only longs (no leverage); shorts are
simplified (no borrow fees). Daily bars from Yahoo are split/dividend adjusted.

## Reading results honestly

- < 30 trades: anecdote, not evidence. Aim for 100+ across different market regimes.
- Compare to the benchmark's return **and** drawdown, not return alone.
- Out-of-sample should be "similar", not "better". A big drop after `oos_start` means curve-fitting.
- Every parameter you tune is a degree of freedom you spend. Prefer simple rules that work
  across many symbols and parameter values over one perfect combination.
- Survivorship bias: a universe of today's winners flatters any long strategy.
