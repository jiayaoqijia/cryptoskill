# Technical Indicators Skill

Agents need more than just current price; they need trends. The **Technical Indicators** skill provides the mathematical backbone for algorithmic trading agents within SpoonOS.

## Features

- **RSI (Relative Strength Index)**: Detects overbought/oversold conditions.
- **SMA (Simple Moving Average)**: Smoothes out price noise.
- **Signal Generation**: Simple "Buy/Sell/Hold" suggestion based on basic strategies.

## Usage

### Parameters

- `prices` (list of float, required): Ordered list of prices (oldest to newest).
- `period` (int, optional): Lookback period for calculations (default: 14).

### Example Agent Prompts

> "Analyze this list of ETH prices and tell me if it's overbought."
> "Calculate the 14-day RSI."

### Output

```json
{
  "last_price": 150.0,
  "rsi_14": 72.5,
  "sma_14": 142.0,
  "signal": "SELL (Overbought)"
}
```
