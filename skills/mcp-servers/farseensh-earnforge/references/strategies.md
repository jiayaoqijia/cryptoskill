# Yield Strategy Presets

4 built-in strategy presets for portfolio allocation and vault filtering.

## 1. Conservative

**Description:** Stablecoin-tagged, TVL > $50M, APY 3-7%, blue-chip protocols only.

| Filter | Value |
|--------|-------|
| Tags | `stablecoin` |
| Min TVL | $50,000,000 |
| Protocols | aave, morpho, euler, pendle, yearn |
| Sort | APY descending |

**Best for:** Capital preservation. Large allocations where safety is the priority. Institutional deposits.

**Expected APY range:** 3-7%

## 2. Max APY

**Description:** Sort by APY descending, no TVL floor.

| Filter | Value |
|--------|-------|
| Tags | (none) |
| Min TVL | (none) |
| Protocols | (all) |
| Sort | APY descending |

**Best for:** Yield maximizers willing to accept higher risk. Smaller allocations where loss is tolerable.

**Expected APY range:** 5-50%+ (higher APY often correlates with higher risk)

## 3. Diversified

**Description:** Spread across 3+ chains, 3+ protocols, mix of stablecoin and LST.

| Filter | Value |
|--------|-------|
| Tags | (none) |
| Min TVL | $1,000,000 |
| Protocols | (all) |
| Sort | APY descending |

**Best for:** Balanced risk through diversification. Medium-sized portfolios. Reducing single-chain or single-protocol exposure.

**Expected APY range:** 4-15%

## 4. Risk-Adjusted

**Description:** Filter by risk score >= 7, then sort by APY.

| Filter | Value |
|--------|-------|
| Tags | (none) |
| Min TVL | (none) |
| Min Risk Score | 7 (low risk only) |
| Protocols | (all) |
| Sort | APY descending |

**Best for:** Optimizing the risk/return ratio. Getting the highest yield among safe vaults. Data-driven allocation.

**Expected APY range:** 3-10%

## Combining Strategies with Suggestions

Pass `--strategy` to `earnforge suggest` to apply a preset:

```bash
# Conservative allocation for $100K USDC
earnforge suggest --amount 100000 --asset USDC --strategy conservative

# Max yield for $1K ETH
earnforge suggest --amount 1000 --asset ETH --strategy max-apy

# Diversified across chains
earnforge suggest --amount 50000 --asset USDC --strategy diversified --max-chains 5

# Only low-risk vaults
earnforge suggest --amount 25000 --asset USDC --strategy risk-adjusted
```

Strategies can be combined with `--max-vaults` and `--max-chains` to further constrain the allocation.
