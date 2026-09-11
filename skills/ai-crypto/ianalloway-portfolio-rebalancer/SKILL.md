---
name: portfolio-rebalancer
description: "Calculate portfolio rebalancing trades to hit target allocations. Supports stocks, crypto, and mixed portfolios."
homepage: https://github.com/ianalloway/openclaw-skills
metadata:
  {
    "openclaw":
      {
        "emoji": "⚖️",
        "requires": { "bins": ["python3"] },
      },
  }
---

# Portfolio Rebalancer

Calculate the exact trades needed to rebalance any portfolio back to target allocations. Works with stocks, crypto, ETFs, or any mix of assets.

## Quick Rebalance

### Simple portfolio rebalance

```bash
python3 -c "
def rebalance(holdings, targets, prices=None):
    '''
    holdings: dict of {asset: quantity}
    targets: dict of {asset: target_pct} (must sum to 1.0)
    prices: dict of {asset: price_per_unit} (optional, defaults to 1.0)
    '''
    if prices is None:
        prices = {a: 1.0 for a in holdings}

    current_values = {a: holdings.get(a, 0) * prices.get(a, 1) for a in targets}
    total = sum(current_values.values())

    if total <= 0:
        print('Portfolio value is zero or negative.')
        return

    print(f'Total Portfolio Value: \${total:,.2f}')
    print(f'{\"\":-<60}')
    print(f'{\"Asset\":<12} {\"Current\":>10} {\"Target\":>10} {\"Diff\":>10} {\"Trade\":>14}')
    print(f'{\"\":-<60}')

    for asset in sorted(targets.keys()):
        current_pct = current_values[asset] / total
        target_pct = targets[asset]
        diff_pct = target_pct - current_pct
        trade_value = diff_pct * total
        trade_qty = trade_value / prices.get(asset, 1)
        action = 'BUY' if trade_value > 0 else 'SELL'

        if abs(trade_value) < 0.01:
            action = '  OK'
            print(f'{asset:<12} {current_pct:>9.1%} {target_pct:>9.1%} {diff_pct:>+9.1%} {\"balanced\":>14}')
        else:
            print(f'{asset:<12} {current_pct:>9.1%} {target_pct:>9.1%} {diff_pct:>+9.1%} {action} {abs(trade_qty):>7.4f}')

# Example: Crypto portfolio
holdings = {'BTC': 0.5, 'ETH': 4.0, 'SOL': 100}
targets = {'BTC': 0.50, 'ETH': 0.30, 'SOL': 0.20}
prices = {'BTC': 95000, 'ETH': 3200, 'SOL': 180}

rebalance(holdings, targets, prices)
"
```

### Rebalance with new deposit

```bash
python3 -c "
def rebalance_with_deposit(holdings, targets, prices, deposit=0):
    current_values = {a: holdings.get(a, 0) * prices.get(a, 1) for a in targets}
    total = sum(current_values.values()) + deposit

    print(f'Current Value: \${sum(current_values.values()):,.2f}')
    print(f'New Deposit:   \${deposit:,.2f}')
    print(f'New Total:     \${total:,.2f}')
    print(f'{\"\":-<65}')
    print(f'{\"Asset\":<10} {\"Now\":>10} {\"Target\":>10} {\"Action\":>8} {\"Qty\":>10} {\"Value\":>12}')
    print(f'{\"\":-<65}')

    for asset in sorted(targets.keys()):
        target_value = targets[asset] * total
        current_value = current_values.get(asset, 0)
        diff = target_value - current_value
        qty = diff / prices[asset]
        action = 'BUY' if diff > 0 else 'SELL' if diff < 0 else 'HOLD'
        pct_now = current_value / (total - deposit) * 100 if (total - deposit) > 0 else 0
        print(f'{asset:<10} {pct_now:>9.1f}% {targets[asset]*100:>9.1f}% {action:>8} {qty:>+10.4f} \${abs(diff):>10,.2f}')

# Example: Add \$5000 to a stock portfolio
holdings = {'VTI': 50, 'VXUS': 20, 'BND': 30, 'VTIP': 10}
targets = {'VTI': 0.50, 'VXUS': 0.20, 'BND': 0.20, 'VTIP': 0.10}
prices = {'VTI': 280, 'VXUS': 60, 'BND': 72, 'VTIP': 50}

rebalance_with_deposit(holdings, targets, prices, deposit=5000)
"
```

## Drift Detection

### Check if portfolio needs rebalancing

```bash
python3 -c "
def check_drift(holdings, targets, prices, threshold=0.05):
    '''Check if any asset has drifted beyond threshold from target.'''
    values = {a: holdings.get(a, 0) * prices.get(a, 1) for a in targets}
    total = sum(values.values())
    needs_rebalance = False

    print(f'Portfolio: \${total:,.2f} | Drift Threshold: {threshold:.0%}')
    print(f'{\"\":-<50}')

    for asset in sorted(targets.keys()):
        pct = values[asset] / total if total > 0 else 0
        drift = abs(pct - targets[asset])
        flag = ' ** REBALANCE' if drift > threshold else ''
        if drift > threshold:
            needs_rebalance = True
        print(f'{asset:<10} {pct:>8.1%} vs {targets[asset]:>6.1%}  drift: {drift:>5.1%}{flag}')

    print(f'{\"\":-<50}')
    if needs_rebalance:
        print('ACTION NEEDED: Portfolio has drifted beyond threshold.')
    else:
        print('Portfolio is within tolerance. No action needed.')

# Example
holdings = {'BTC': 0.8, 'ETH': 5.0, 'SOL': 50}
targets = {'BTC': 0.50, 'ETH': 0.30, 'SOL': 0.20}
prices = {'BTC': 97000, 'ETH': 3100, 'SOL': 175}

check_drift(holdings, targets, prices, threshold=0.05)
"
```

## Tax-Aware Rebalancing

### Minimize sells (buy-only rebalance using new cash)

```bash
python3 -c "
def buy_only_rebalance(holdings, targets, prices, cash):
    '''Rebalance by only buying - never selling (tax-efficient).'''
    values = {a: holdings.get(a, 0) * prices.get(a, 1) for a in targets}
    total = sum(values.values()) + cash

    print(f'Available Cash: \${cash:,.2f}')
    print(f'Post-Rebalance Total: \${total:,.2f}')
    print(f'{\"\":-<50}')

    buys = {}
    for asset in targets:
        target_value = targets[asset] * total
        current_value = values.get(asset, 0)
        deficit = max(0, target_value - current_value)
        buys[asset] = deficit

    buy_total = sum(buys.values())

    if buy_total > cash:
        scale = cash / buy_total
        buys = {a: v * scale for a, v in buys.items()}

    remaining = cash
    for asset in sorted(buys.keys(), key=lambda a: buys[a], reverse=True):
        buy_val = min(buys[asset], remaining)
        qty = buy_val / prices[asset]
        if buy_val > 0.01:
            print(f'BUY {qty:.4f} {asset:<8} (\${buy_val:,.2f})')
            remaining -= buy_val

    if remaining > 0.01:
        print(f'Remaining cash: \${remaining:,.2f}')

holdings = {'VTI': 100, 'VXUS': 30, 'BND': 40}
targets = {'VTI': 0.60, 'VXUS': 0.25, 'BND': 0.15}
prices = {'VTI': 280, 'VXUS': 60, 'BND': 72}
buy_only_rebalance(holdings, targets, prices, cash=3000)
"
```

## Tips

1. **Rebalance on a schedule** (quarterly or when drift exceeds 5%)
2. **Use new deposits to rebalance** before selling (tax-efficient)
3. **Consider transaction costs** - skip tiny trades under $50
4. **Keep target allocations simple** - fewer assets = easier to maintain
5. **Document your target allocation** and the reasoning behind it

## Common Allocations

| Strategy | Stocks | Bonds | Crypto | Real Estate |
|----------|--------|-------|--------|-------------|
| Aggressive Growth | 80% | 5% | 10% | 5% |
| Balanced | 60% | 25% | 5% | 10% |
| Conservative | 40% | 45% | 0% | 15% |
| Crypto-Heavy | 30% | 10% | 50% | 10% |

## Author

Created by [Ian Alloway](https://github.com/ianalloway) - Data Scientist specializing in AI/ML and portfolio optimization.

## License

MIT License
