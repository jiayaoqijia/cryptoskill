# Adding Custom Strategies

## Overview

The trading system is designed to be strategy-agnostic. Add new strategies by:
1. Implementing a signal check method in `PaperTrader`
2. Registering it in `update_kline()` dispatch

## Template

```python
def check_my_strategy(self, strategy: str, symbol: str):
    """Your strategy description."""
    if symbol not in self.klines or len(self.klines[symbol]) < MINIMUM_CANDLES:
        return

    closes = [k["c"] for k in self.klines[symbol]]
    price = closes[-1]

    # Real-time SL/TP
    if symbol in self.prices:
        self.check_sl_tp(strategy, self.prices[symbol])

    # === YOUR SIGNAL LOGIC ===
    buy_signal = False   # Replace with your condition
    sell_signal = False   # Replace with your condition

    # Position management
    if strategy in self.positions:
        pos = self.positions[strategy]
        if pos["side"] == "long" and sell_signal:
            self.close_position(strategy, price, "Your exit reason")
        elif pos["side"] == "short" and buy_signal:
            self.close_position(strategy, price, "Your exit reason")
    else:
        if buy_signal:
            self.open_position(strategy, symbol, "long", price)
        elif sell_signal:
            self.open_position(strategy, symbol, "short", price)
```

## Register in Dispatch

In `update_kline()`, add your strategy to the candle close handler:

```python
if kline_data.get("confirm", False):
    if symbol == "BTCUSDT":
        self.check_my_strategy("BTC_MYSTRAT", symbol)
```

## Strategy Ideas

- **Bollinger Bands**: Mean reversion when price touches upper/lower band
- **MACD**: Signal line crossover with histogram confirmation
- **Volume Profile**: Breakout on high volume above resistance
- **Funding Rate**: Short when funding > 0.1%, long when < -0.1%
- **Multi-timeframe**: Confirm 1h signal with 4h trend direction

## Adding to Backtest

Copy the pattern from `backtest_ema()` or `backtest_rsi()` in `backtest.py`. 
The structure is identical — loop candles, check SL/TP, check signals, track trades.
