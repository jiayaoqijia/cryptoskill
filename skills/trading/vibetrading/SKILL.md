---
name: vibetrading
description: "Build, backtest, and deploy cryptocurrency trading strategies using the vibetrading Python framework. Use when: (1) generating trading strategies from natural language, (2) backtesting strategies on historical data, (3) deploying strategies to live exchanges (Hyperliquid, Paradex, Lighter, Aster), (4) comparing strategy performance, (5) working with crypto trading indicators, position sizing, or risk management. NOT for: general finance questions, non-crypto trading, or strategies outside the vibetrading framework."
---

# vibetrading

Agent-first crypto trading framework. Strategies are Python functions decorated with `@vibe` that call sandbox functions (`get_perp_price`, `long`, `short`, etc.). Same code runs in backtest and live.

## Install

```bash
pip install vibetrading                    # Core
pip install "vibetrading[hyperliquid]"     # + Hyperliquid live trading
pip install "vibetrading[dev]"             # + pytest, ruff
```

## Core Workflow

### 1. Write a Strategy

```python
import math
from vibetrading import vibe, get_perp_price, get_perp_position, get_perp_summary
from vibetrading import set_leverage, long, reduce_position, get_futures_ohlcv
from vibetrading.indicators import rsi

@vibe(interval="1h")
def my_strategy():
    price = get_perp_price("BTC")
    if math.isnan(price):
        return

    position = get_perp_position("BTC")
    if position and position.get("size", 0) != 0:
        pnl = (price - position["entry_price"]) / position["entry_price"]
        if pnl >= 0.03 or pnl <= -0.02:
            reduce_position("BTC", abs(position["size"]))
        return

    ohlcv = get_futures_ohlcv("BTC", "1h", 20)
    if ohlcv is None or len(ohlcv) < 15:
        return

    if rsi(ohlcv["close"]).iloc[-1] < 30:
        summary = get_perp_summary()
        margin = summary.get("available_margin", 0)
        if margin > 100:
            set_leverage("BTC", 3)
            qty = (margin * 0.1 * 3) / price
            if qty * price >= 15:
                long("BTC", qty, price, order_type="market")
```

### 2. Backtest

```python
import vibetrading.backtest

results = vibetrading.backtest.run(code, interval="1h", slippage_bps=5)
m = results["metrics"]
# Keys: total_return, sharpe_ratio, sortino_ratio, calmar_ratio, max_drawdown,
#        win_rate, profit_factor, expectancy, number_of_trades, cagr, etc.
```

### 3. Deploy Live

```python
import vibetrading.live

await vibetrading.live.start(
    code,
    exchange="hyperliquid",
    api_key="0xWalletAddress",
    api_secret="0xPrivateKey",
    interval="1m",
)
```

## Strategy Rules

Every strategy **must**:
- Import and use `@vibe` or `@vibe(interval="1h")` decorator
- Guard against `math.isnan(price)` — prices are NaN before data loads
- Check position before entering (avoid stacking)
- Have both take-profit and stop-loss exits
- Check `margin > 50` and `qty * price >= 15` before trading

Order types: `"market"` (fills immediately + slippage) or `"limit"` (fills at price).

## Sandbox Functions

**Data**: `get_perp_price(asset)`, `get_spot_price(asset)`, `get_futures_ohlcv(asset, interval, limit)`, `get_spot_ohlcv(asset, interval, limit)`, `get_funding_rate(asset)`, `get_open_interest(asset)`, `get_current_time()`, `get_supported_assets()`

**Account**: `get_perp_summary()` → `{available_margin, total_margin, ...}`, `get_perp_position(asset)` → `{size, entry_price, pnl, leverage}` or `None`, `my_spot_balance(asset?)`, `my_futures_balance()`

**Trading**: `long(asset, qty, price, order_type="market")`, `short(asset, qty, price, order_type="market")`, `buy(asset, qty, price)`, `sell(asset, qty, price)`, `reduce_position(asset, qty)`, `set_leverage(asset, leverage)`

## Indicators

`from vibetrading.indicators import sma, ema, rsi, bbands, atr, macd, stochastic, vwap`

All take pandas Series, return pandas Series. Pure pandas — no dependencies.

| Function | Signature | Returns |
|---|---|---|
| `rsi` | `rsi(close, period=14)` | Series (0-100) |
| `bbands` | `bbands(close, period=20, std=2.0)` | `(upper, middle, lower)` |
| `macd` | `macd(close, fast=12, slow=26, signal=9)` | `(macd_line, signal, histogram)` |
| `atr` | `atr(high, low, close, period=14)` | Series |
| `stochastic` | `stochastic(high, low, close, k=14, d=3)` | `(%K, %D)` |

## Position Sizing

`from vibetrading.sizing import kelly_size, fixed_fraction_size, volatility_adjusted_size, risk_per_trade_size`

- `kelly_size(win_rate, avg_win, avg_loss, balance, fraction=0.5)` — half-Kelly default
- `risk_per_trade_size(balance, risk_pct, stop_distance, price)` — risk-based

## Templates

```python
from vibetrading.templates import momentum, mean_reversion, grid, dca, multi_momentum
code = momentum()  # Returns valid strategy code string
```

## AI Generation

```python
import vibetrading.strategy

code = vibetrading.strategy.generate("BTC RSI oversold entry, 3x leverage", model="claude-sonnet-4-20250514")
result = vibetrading.strategy.validate(code)  # Static analysis
report = vibetrading.strategy.analyze(results, strategy_code=code)  # LLM analysis
```

Requires `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` in environment.

## Comparing Strategies

```python
import vibetrading.compare

results = vibetrading.compare.run({"RSI": code1, "MACD": code2}, slippage_bps=5)
vibetrading.compare.print_table(results)
df = vibetrading.compare.to_dataframe(results)
```

## Data Download

```python
import vibetrading.tools
from datetime import datetime, timezone

data = vibetrading.tools.download_data(
    ["BTC", "ETH", "SOL"], exchange="binance", interval="1h",
    start_time=datetime(2025, 1, 1, tzinfo=timezone.utc),
    end_time=datetime(2025, 6, 1, tzinfo=timezone.utc),
)
results = vibetrading.backtest.run(code, data=data, slippage_bps=5)
```

## Exchange Credentials

Store in `.env.local` (gitignored):

| Exchange | `api_key` | `api_secret` | Extra |
|---|---|---|---|
| Hyperliquid | Wallet address `0x...` | Private key `0x...` | — |
| Paradex | StarkNet public key | StarkNet private key | `account_address=` |
| Lighter | API key | API secret | — |
| Aster | API key | API secret | `user_address=` |

## Common Patterns

For detailed API docs, strategy patterns, and exchange-specific setup: see [references/api-details.md](references/api-details.md).
