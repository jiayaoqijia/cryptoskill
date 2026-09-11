---
name: kelly-criterion
description: "Calculate optimal bet sizes using the Kelly Criterion formula. Maximize long-term bankroll growth while managing risk."
homepage: https://github.com/ianalloway/openclaw-skills
metadata:
  {
    "openclaw":
      {
        "emoji": "📊",
        "requires": { "bins": ["python3"] },
      },
  }
---

# Kelly Criterion Calculator

Calculate mathematically optimal bet sizes to maximize long-term bankroll growth while managing risk. The Kelly Criterion is used by professional bettors and investors to determine position sizing.

## The Formula

**Kelly % = (bp - q) / b**

Where:
- `b` = decimal odds - 1 (net odds received on the bet)
- `p` = probability of winning
- `q` = probability of losing (1 - p)

## Quick Calculator

### Basic Kelly calculation (Python one-liner)

```bash
# Usage: kelly(win_probability, decimal_odds)
python3 -c "
def kelly(p, odds):
    b = odds - 1
    q = 1 - p
    k = (b * p - q) / b
    return max(0, k)

# Example: 55% win probability at 2.0 odds (even money)
prob, odds = 0.55, 2.0
print(f'Kelly: {kelly(prob, odds):.2%} of bankroll')
"
```

### Convert American odds to decimal

```bash
python3 -c "
def american_to_decimal(american):
    if american > 0:
        return (american / 100) + 1
    else:
        return (100 / abs(american)) + 1

# Example: -110 American odds
american = -110
decimal = american_to_decimal(american)
print(f'{american:+d} American = {decimal:.3f} decimal')
"
```

### Full Kelly Calculator with fractional Kelly

```bash
python3 -c "
def kelly_full(win_prob, decimal_odds, fraction=1.0, bankroll=1000):
    b = decimal_odds - 1
    q = 1 - win_prob
    kelly_pct = max(0, (b * win_prob - q) / b)
    fractional = kelly_pct * fraction
    bet_amount = bankroll * fractional
    
    print(f'Win Probability: {win_prob:.1%}')
    print(f'Decimal Odds: {decimal_odds:.2f}')
    print(f'Full Kelly: {kelly_pct:.2%}')
    print(f'{fraction:.0%} Kelly: {fractional:.2%}')
    print(f'Bet Amount: \${bet_amount:.2f} (on \${bankroll} bankroll)')
    
    # Expected value
    ev = (win_prob * (decimal_odds - 1)) - (1 - win_prob)
    print(f'Expected Value: {ev:.2%} per unit')

# Example: 60% edge at -150 odds, using half Kelly on $1000 bankroll
kelly_full(0.60, 1.667, fraction=0.5, bankroll=1000)
"
```

## Common Scenarios

### Sports Betting: Find edge and optimal bet

```bash
python3 -c "
def analyze_bet(your_prob, market_odds_american, bankroll=1000):
    # Convert American to decimal
    if market_odds_american > 0:
        decimal_odds = (market_odds_american / 100) + 1
    else:
        decimal_odds = (100 / abs(market_odds_american)) + 1
    
    # Implied probability from market
    implied_prob = 1 / decimal_odds
    
    # Your edge
    edge = your_prob - implied_prob
    
    # Kelly calculation
    b = decimal_odds - 1
    kelly_pct = max(0, (b * your_prob - (1 - your_prob)) / b)
    
    print(f'Your probability: {your_prob:.1%}')
    print(f'Market odds: {market_odds_american:+d} ({decimal_odds:.3f} decimal)')
    print(f'Implied probability: {implied_prob:.1%}')
    print(f'Your edge: {edge:+.1%}')
    print(f'Full Kelly: {kelly_pct:.2%}')
    print(f'Half Kelly bet: \${bankroll * kelly_pct * 0.5:.2f}')
    
    if edge <= 0:
        print('WARNING: No edge - do not bet!')

# Example: You think team has 58% chance, market has them at -130
analyze_bet(0.58, -130, bankroll=1000)
"
```

### Multi-bet Kelly (simultaneous independent bets)

```bash
python3 -c "
def multi_kelly(bets, bankroll=1000):
    '''
    bets: list of (name, win_prob, decimal_odds) tuples
    '''
    total_kelly = 0
    print(f'Bankroll: \${bankroll}')
    print('-' * 50)
    
    for name, prob, odds in bets:
        b = odds - 1
        kelly = max(0, (b * prob - (1 - prob)) / b)
        total_kelly += kelly
        bet_amt = bankroll * kelly * 0.5  # Half Kelly
        print(f'{name}: {kelly:.2%} Kelly -> \${bet_amt:.2f} (half)')
    
    print('-' * 50)
    print(f'Total exposure: {total_kelly:.2%} (full) / {total_kelly*0.5:.2%} (half)')
    
    if total_kelly > 1:
        print('WARNING: Over-leveraged! Reduce bet sizes.')

# Example: Three simultaneous bets
bets = [
    ('Lakers ML', 0.55, 2.10),
    ('Chiefs -3', 0.52, 1.91),
    ('Yankees ML', 0.48, 2.20),  # No edge - will show 0
]
multi_kelly(bets, bankroll=1000)
"
```

## Fractional Kelly Recommendations

| Risk Tolerance | Kelly Fraction | Use Case |
|---------------|----------------|----------|
| Aggressive | 100% (Full) | Maximum growth, high variance |
| Moderate | 50% (Half) | Good balance, recommended for most |
| Conservative | 25% (Quarter) | Lower variance, slower growth |
| Very Conservative | 10% | Minimal drawdowns |

## Tips

1. **Never bet more than Kelly suggests** - overbetting leads to ruin
2. **Use fractional Kelly (25-50%)** - reduces variance significantly
3. **Be honest about your edge** - overestimating probability is the #1 mistake
4. **Track your results** - adjust probabilities based on actual performance
5. **Account for correlation** - reduce sizes when bets are correlated

## Edge Cases

- If Kelly returns negative, you have no edge - don't bet
- If Kelly > 25%, double-check your probability estimate
- For parlays, calculate the combined probability and use parlay odds

## Author

Created by [Ian Alloway](https://github.com/ianalloway) - Data Scientist specializing in sports analytics and ML.

## License

MIT License
