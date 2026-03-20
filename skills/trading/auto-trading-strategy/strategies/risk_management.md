# Risk Management Framework

## Core Rules

### Rule 1: Never Risk More Than 2%
**Maximum loss per trade = 2% of total capital**

```
Example:
- Capital: $1000
- Max Risk: $20 per trade
- If stop loss is 10%, max position = $200
```

### Rule 2: R-Multiple System
**Measure everything in terms of risk (R)**

| Outcome | R Multiple | Meaning |
|---------|-----------|---------|
| Full loss | -1R | Hit stop loss |
| Break even | 0R | Exit at entry |
| Small win | +1R | Risk = Reward |
| Good win | +2R | Target 1 |
| Great win | +3R | Target 2 |
| Home run | +5R+ | Let it run |

### Rule 3: Win Rate vs R-Multiple
**You need either high win rate OR high R-multiple**

| Win Rate | Required R-Multiple |
|----------|---------------------|
| 50% | 1.1R+ |
| 40% | 1.5R+ |
| 30% | 2.3R+ |
| 25% | 3R+ |

## Position Sizing Calculator

### Step-by-Step

1. **Determine account size**: $1000
2. **Set risk per trade**: 2% = $20
3. **Find stop loss distance**: 10% from entry
4. **Calculate position size**:
   ```
   Position = Risk / Stop Loss %
   Position = $20 / 0.10 = $200
   ```

### Kelly Criterion (Advanced)

```python
def kelly_fraction(win_rate, avg_win, avg_loss):
    """
    Calculate optimal position size using Kelly Criterion
    """
    b = avg_win / avg_loss  # Odds ratio
    p = win_rate
    q = 1 - win_rate
    
    kelly = (b * p - q) / b
    
    # Use half-Kelly for safety
    return kelly * 0.5
```

## Portfolio Management

### Diversification Rules
- Max 20% in single market
- Max 50% in single category
- Keep 20% cash for opportunities

### Correlation Awareness
Avoid over-exposure to correlated markets:
- BTC + ETH = correlated
- Trump + Republican = correlated
- Multiple crypto markets = correlated

## Drawdown Management

### Drawdown Levels

| Level | Drawdown | Action |
|-------|----------|--------|
| Green | <5% | Normal trading |
| Yellow | 5-10% | Reduce size 50% |
| Orange | 10-15% | Stop new trades |
| Red | >15% | Review all positions |

### Recovery Formula

```
To recover X% loss, you need Y% gain:

X = 10% → Y = 11.1%
X = 20% → Y = 25%
X = 30% → Y = 43%
X = 50% → Y = 100%

Lesson: Don't let losses compound!
```

## Stop Loss Strategies

### Fixed Percentage
- Simple: Set at -20% from entry
- Pros: Easy to execute
- Cons: May get stopped on noise

### Volatility-Based
- Set at 2x ATR (Average True Range)
- Pros: Adapts to market conditions
- Cons: More complex

### Time-Based
- Exit if no movement in X hours
- Pros: Frees up capital
- Cons: May miss late moves

## Daily Limits

| Limit | Value | Purpose |
|-------|-------|---------|
| Max trades/day | 20 | Avoid overtrading |
| Max loss/day | 6% | Prevent tilt |
| Max drawdown/week | 15% | Protect capital |

## Psychology Rules

1. **No revenge trading** - After a loss, take a break
2. **No FOMO** - Missed move = missed move
3. **No averaging down** - If wrong, cut it
4. **No overleveraging** - Stick to position sizing

## Checklist Before Every Trade

- [ ] Position size correct (≤2% risk)?
- [ ] Stop loss set?
- [ ] Target defined (≥1.5R)?
- [ ] Trend confirmed?
- [ ] Not overtrading today?
- [ ] Head clear (no tilt)?
