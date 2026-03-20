# Trend Following Strategy

## Core Principles

1. **Trade with the trend** - The trend is your friend
2. **Wait for confirmation** - Don't guess, wait for signals
3. **Cut losses quickly** - Let winners run
4. **Manage risk** - Never risk more than 2% per trade

## Entry Signals

### Bullish Entry (Buy YES)
- Price crosses above 20-day MA
- Volume confirmation (>1.5x average)
- RSI < 70 (not overbought)
- Price action: Higher highs, higher lows

### Bearish Entry (Buy NO)
- Price crosses below 20-day MA
- Volume confirmation (>1.5x average)
- RSI > 30 (not oversold)
- Price action: Lower highs, lower lows

## Position Sizing

### Kelly Criterion Formula
```
f* = (bp - q) / b

Where:
- f* = fraction of bankroll to risk
- b = odds received (decimal - 1)
- p = probability of winning
- q = probability of losing (1 - p)
```

### Simplified Sizing
| Confidence | Kelly % | R Multiple |
|------------|---------|-----------|
| High | 20-25% | 1R |
| Medium | 10-15% | 1.5R |
| Low | 5% | 2R |

## Exit Rules

### Take Profit
- 2R (twice risk amount) - first target
- 3R - second target
- Trail stop at 1.5R for remainder

### Stop Loss
- Maximum 20% of entry price
- Never exceed 2% of portfolio

## Time Frames

| Time Frame | Signals | Best For |
|------------|---------|----------|
| 5-15 min | Quick scalps | Day trading |
| 1-4 hour | Swings | Position trading |
| Daily | Trend | Investing |

## Trend Strength Indicators

### ADX (Average Directional Index)
- ADX > 25: Strong trend
- ADX < 20: No trend (avoid)

### Moving Average Alignment
- All MAs stacked: Strong trend
- MAs crossing: Trend change

## Example Trade Setup

```
Market: Will BTC hit $100K by Dec 2024?
Entry: $0.35 (YES)
Risk: $0.07 (20%)
Position: $100

Stop: $0.28
Target 1: $0.49 (1R = +$14)
Target 2: $0.56 (2R = +$21)
Target 3: $0.70 (3R = +$35)
```
