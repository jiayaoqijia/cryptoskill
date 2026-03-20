# Liquidity Monitor — Tips & Tricks 💧

## Impermanent Loss Essentials

1. **IL is only "realized" when you withdraw** — If token prices return to entry ratio, IL disappears.
2. **High volatility pairs = high IL** — ETH/USDC has less IL than SHIB/ETH.
3. **Fee income offsets IL** — High-volume pools can more than compensate for IL through trading fees.
4. **Concentrated liquidity amplifies IL** — Uniswap V3 ranges increase both yield AND IL exposure.

## Pool Selection Strategy

- **TVL > $1M** for safety — Smaller pools are easier to manipulate
- **Volume/TVL ratio > 0.3** — This means fees are actively generated
- **Multiple LPs** — Pools dominated by 1-2 LPs are risky (they can pull liquidity)
- **Established pairs** — Major token pairs on audited DEXes are safest

## Monitoring Best Practices

- Check pool health score daily for active LP positions
- Set alerts for TVL drops >10% in 1 hour — could indicate a rug
- Monitor the pool ratio — extreme imbalance means one token is being dumped
- Track your accumulated fees separately from your LP position value

## Yield Calculation Gotchas

- ❌ Don't compare APY numbers across DEXes without normalizing — calculation methods differ
- ❌ Farm token rewards inflate APY — if the reward token drops 90%, so does your real yield
- ✅ Focus on fee APY (sustainable) vs reward APY (temporary)
- ✅ Always factor in gas costs for entering/exiting positions

## Red Flags

- 🚨 TVL dropping rapidly while price is stable = LPs are exiting (they know something)
- 🚨 Single LP controlling >50% of pool = withdrawal risk
- 🚨 Unaudited DEX protocol = smart contract risk
- 🚨 Brand new pool with very high APY = likely unsustainable, possible honeypot
