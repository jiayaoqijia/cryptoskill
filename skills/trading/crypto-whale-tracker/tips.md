# 🐋 Whale Tracker Tips

## Getting Better Results

1. **Use an API key** — The free Whale Alert tier is limited to 10 requests/hour. Get a free key at https://whale-alert.io for 100 req/hour.

2. **Combine with price data** — Whale movements mean more when correlated with price action. A large exchange inflow during a price pump is a strong sell signal.

3. **Focus on stablecoins** — USDT/USDC whale movements to exchanges often precede large buys. Track them separately.

4. **Set up alerts** — Use cron to run the script every 30 minutes and pipe output to a notification system.

5. **Filter noise** — Internal exchange transfers (hot wallet rebalancing) create false signals. Use `--label true` to identify these.

## Reading Whale Signals

| Movement | Meaning | Confidence |
|----------|---------|------------|
| Crypto → Exchange | Possible sell | Medium |
| Exchange → Cold Wallet | Accumulation | High |
| Stablecoin → Exchange | Buying preparation | High |
| Whale → Whale | OTC deal or rebalance | Low |

## Pro Patterns

- **Accumulation**: Multiple small outflows from exchanges over days
- **Distribution**: Sudden large inflow to exchange
- **Wash trading**: Same amount moving back and forth between two addresses
- **Smart money**: Follow wallets that historically bought before pumps

## Common Mistakes

- Don't panic on a single whale transfer — look for patterns
- Exchange cold wallet movements are NOT sell signals
- Stablecoin minting ≠ buying (it's just issuance)
- Always check if a "whale" address is actually a smart contract
