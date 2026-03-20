# vibetrading API Details

## Table of Contents
- [Backtest Engine](#backtest-engine)
- [Metrics Reference](#metrics-reference)
- [Equity Curve](#equity-curve)
- [Strategy Validation](#strategy-validation)
- [Strategy Patterns](#strategy-patterns)
- [Live Trading Setup](#live-trading-setup)
- [CLI Commands](#cli-commands)
- [Intervals](#intervals)
- [Common Mistakes](#common-mistakes)

## Backtest Engine

### `vibetrading.backtest.run()` — Full Parameters

```python
results = vibetrading.backtest.run(
    strategy_code,              # str: Python code with @vibe function
    interval="1h",              # "5m", "15m", "1h", "4h", "1d"
    initial_balances={"USDC": 10000},
    start_time=datetime(2025, 1, 1, tzinfo=timezone.utc),
    end_time=datetime(2025, 6, 1, tzinfo=timezone.utc),
    exchange="binance",         # For auto-download
    data=None,                  # Pre-loaded data dict (skips download)
    mute_strategy_prints=False, # Suppress strategy stdout
    slippage_bps=5.0,           # Basis points slippage on market orders
)
```

### Result Structure

```python
results = {
    "trades": [...],            # List of executed trades
    "metrics": {...},           # Performance metrics dict
    "simulation_info": {
        "interval": "1h",
        "liquidated": False,
        "steps": 3600,
    },
    "final_balances": {"USDC": 10500.0},
    "equity_curve": pd.DataFrame,  # total_value, returns, cumulative_returns, drawdown, peak
}
```

### Pre-loading Data

Always pre-load for multiple backtests (avoids re-downloading):

```python
import vibetrading.tools
data = vibetrading.tools.download_data(
    ["BTC", "ETH", "SOL"],
    exchange="binance",
    interval="1h",
    start_time=datetime(2025, 1, 1, tzinfo=timezone.utc),
    end_time=datetime(2025, 6, 1, tzinfo=timezone.utc),
)
# data keys: ("BTC/USDT:USDT", "1h"), etc.
# Pass to multiple backtest.run() calls
```

## Metrics Reference

All returned by `results["metrics"]`:

| Key | Type | Description |
|---|---|---|
| `total_return` | float | Decimal (0.10 = 10%) |
| `cagr` | float | Compound Annual Growth Rate |
| `sharpe_ratio` | float | Annualized |
| `sortino_ratio` | float | Annualized (downside only) |
| `calmar_ratio` | float | CAGR / max drawdown |
| `max_drawdown` | float | Negative decimal (-0.10 = -10%) |
| `max_drawdown_duration_hours` | float | Longest drawdown |
| `win_rate` | float | 0-1 scale |
| `profit_factor` | float | Gross profit / gross loss |
| `expectancy` | float | Expected USD per trade |
| `number_of_trades` | int | Total trades |
| `winning_trades` | int | Count |
| `losing_trades` | int | Count |
| `avg_win` | float | USD |
| `avg_loss` | float | Negative USD |
| `largest_win` | float | USD |
| `largest_loss` | float | Negative USD |
| `max_consecutive_wins` | int | Streak |
| `max_consecutive_losses` | int | Streak |
| `total_tx_fees` | float | USD |
| `funding_revenue` | float | Net USD |
| `initial_balance` | float | Starting USD |
| `total_value` | float | Final USD |

### Interpreting Metrics

- **Sharpe > 1.0**: Good risk-adjusted returns
- **Sortino > 1.5**: Good downside-adjusted returns
- **Profit Factor > 1.5**: Strong edge
- **Win Rate alone is misleading** — always check with profit factor/expectancy
- **Max Drawdown > 20%**: High risk for leveraged strategies

## Equity Curve

```python
ec = results["equity_curve"]
# Columns: total_value, returns, cumulative_returns, drawdown, peak
# Index: DatetimeIndex (UTC)

# Plot with matplotlib
ec["total_value"].plot(title="Equity Curve")
ec["drawdown"].plot(title="Drawdown")
```

## Strategy Validation

```python
result = vibetrading.strategy.validate(code)
result.is_valid      # bool
result.errors        # list[str] — must fix
result.warnings      # list[str] — should fix
result.format_for_llm()  # str — formatted for LLM feedback
```

Validation checks:
- Syntax errors
- Missing `@vibe` decorator
- Missing imports
- No risk management (stop loss / take profit)
- Leverage not set before trading
- Position not checked before entry

## Strategy Patterns

### Perp Long/Short with ATR Stop

```python
from vibetrading import vibe, get_perp_price, get_perp_position, get_perp_summary
from vibetrading import set_leverage, long, short, reduce_position, get_futures_ohlcv
from vibetrading.indicators import rsi, atr, ema
import math

@vibe(interval="1h")
def strategy():
    price = get_perp_price("BTC")
    if math.isnan(price):
        return

    ohlcv = get_futures_ohlcv("BTC", "1h", 50)
    if ohlcv is None or len(ohlcv) < 30:
        return

    current_atr = atr(ohlcv["high"], ohlcv["low"], ohlcv["close"], 14).iloc[-1]
    current_rsi = rsi(ohlcv["close"]).iloc[-1]
    trend = ema(ohlcv["close"], 50).iloc[-1]

    # Manage position
    position = get_perp_position("BTC")
    if position and position.get("size", 0) != 0:
        entry = position["entry_price"]
        size = position["size"]
        is_long = size > 0
        pnl_dist = (price - entry) if is_long else (entry - price)

        if pnl_dist <= -current_atr * 2:  # ATR stop
            reduce_position("BTC", abs(size))
        elif pnl_dist >= current_atr * 4:  # ATR take profit
            reduce_position("BTC", abs(size))
        return

    # Entry
    summary = get_perp_summary()
    margin = summary.get("available_margin", 0)
    if margin < 100:
        return

    set_leverage("BTC", 3)
    qty = (margin * 0.1 * 3) / price
    if qty * price < 15:
        return

    if current_rsi < 30 and price > trend:
        long("BTC", qty, price, order_type="market")
    elif current_rsi > 70 and price < trend:
        short("BTC", qty, price, order_type="market")
```

### Spot DCA

```python
from vibetrading import vibe, get_spot_price, buy, my_spot_balance
import math

@vibe(interval="1d")
def dca():
    price = get_spot_price("BTC")
    if math.isnan(price):
        return

    usdc = my_spot_balance("USDC")
    buy_amount = 100  # $100 per day

    if usdc >= buy_amount:
        qty = buy_amount / price
        buy("BTC", qty, price, order_type="market")
```

### Multi-Asset with Position Sizing

```python
from vibetrading import vibe, get_perp_price, get_perp_position, get_perp_summary
from vibetrading import set_leverage, long, reduce_position, get_futures_ohlcv
from vibetrading.indicators import rsi, atr
from vibetrading.sizing import risk_per_trade_size
import math

ASSETS = ["BTC", "ETH", "SOL"]

@vibe(interval="1h")
def multi_asset():
    summary = get_perp_summary()
    margin = summary.get("available_margin", 0)

    for asset in ASSETS:
        price = get_perp_price(asset)
        if math.isnan(price):
            continue

        position = get_perp_position(asset)
        if position and position.get("size", 0) != 0:
            pnl = (price - position["entry_price"]) / position["entry_price"]
            if pnl >= 0.04 or pnl <= -0.02:
                reduce_position(asset, abs(position["size"]))
            continue

        ohlcv = get_futures_ohlcv(asset, "1h", 20)
        if ohlcv is None or len(ohlcv) < 15:
            continue

        current_rsi = rsi(ohlcv["close"]).iloc[-1]
        current_atr = atr(ohlcv["high"], ohlcv["low"], ohlcv["close"]).iloc[-1]

        if current_rsi < 30 and margin > 100:
            stop_distance = current_atr * 2
            qty = risk_per_trade_size(margin, 0.01, stop_distance, price)
            set_leverage(asset, 3)
            if qty * price >= 15:
                long(asset, qty, price, order_type="market")
```

## Live Trading Setup

### Hyperliquid (most common)

```bash
pip install "vibetrading[hyperliquid]"
```

```python
# .env.local
# HYPERLIQUID_WALLET=0xYourWalletAddress
# HYPERLIQUID_PRIVATE_KEY=0xYourPrivateKey

import os, asyncio
from dotenv import load_dotenv
import vibetrading.live

load_dotenv(".env.local")

asyncio.run(vibetrading.live.start(
    open("my_strategy.py").read(),
    exchange="hyperliquid",
    api_key=os.environ["HYPERLIQUID_WALLET"],
    api_secret=os.environ["HYPERLIQUID_PRIVATE_KEY"],
    interval="1m",
))
```

### Direct Sandbox Access

```python
import vibetrading.sandbox

sandbox = vibetrading.sandbox.create("hyperliquid", api_key=..., api_secret=...)
price = sandbox.get_perp_price("BTC")
summary = sandbox.get_perp_summary()
print(f"BTC: ${price:,.2f}, Margin: ${summary.available_margin:,.2f}")
```

## CLI Commands

```bash
vibetrading backtest strategy.py -i 1h          # Backtest
vibetrading validate strategy.py                 # Static validation
vibetrading download BTC ETH SOL -i 1h -o data/  # Download data
vibetrading template momentum -o strategy.py      # Generate from template
vibetrading template --list                       # List templates
vibetrading version                               # Show version
```

## Intervals

Supported: `"5m"`, `"15m"`, `"1h"`, `"4h"`, `"1d"`

The `@vibe(interval=...)` sets candle interval for data. The `LiveRunner` interval sets execution frequency. They can differ.

## Common Mistakes

1. **Not checking `math.isnan(price)`** — Prices are NaN before data loads
2. **Not checking position before entry** — Leads to position stacking
3. **No stop loss** — Strategy will hold losing positions forever
4. **`qty * price < 15`** — Minimum notional; orders below this are rejected
5. **Not setting leverage** — Defaults to 1x; call `set_leverage()` before trading
6. **Using `import ta`** — Use `vibetrading.indicators` instead (pure pandas, always available)
7. **Tight stops in volatile markets** — Use ATR-based stops, not fixed percentages
8. **Too many trades** — Transaction fees kill edge; add cooldown periods
9. **Not pre-loading data for comparisons** — Causes redundant downloads
10. **Hardcoding credentials** — Use `.env.local` and `os.environ`
