# Venus Protocol Overview (BNB Chain)

Venus is a money market protocol on BNB Chain. Users supply assets to earn yield and borrow against posted collateral.

## Concepts
- **vToken**: interest-bearing market token representing supplied assets.
- **Collateral factor / liquidation threshold**: determines borrowable value from collateral.
- **Health**: collateral safety against liquidation.
- **Utilization**: borrowed / supplied in a market; strongly affects rates.
- **Isolated pools**: pool-specific risk params and asset sets.

## Practical analysis checklist
1. Confirm pool/market parameters (CF/LT, caps, liquidity).
2. Compute current health and liquidation buffer.
3. Stress test proposed borrow.
4. Recommend conservative limit and fallback action (repay/add collateral).
