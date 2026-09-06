# DeFi Yield Scout

**Find, compare, and risk-score DeFi yield opportunities across 20+ protocols and 10+ chains — no API keys required.**

DeFi Yield Scout is a SpoonOS skill that helps DeFi users discover the best yield farming opportunities, assess their risks, calculate impermanent loss, and build personalized yield strategies. Powered entirely by DeFiLlama's free public API.

---

## Why DeFi Yield Scout?

| Capability | Manually Checking | DeFi Aggregators | DeFi Yield Scout |
|-----------|------------------|-------------------|-----------------|
| Cross-protocol comparison | Visit each protocol individually | Limited to listed protocols | 20+ protocols in one query |
| Cross-chain scanning | Check each chain separately | Usually single-chain | 10+ chains simultaneously |
| Risk scoring | Subjective gut feeling | Basic TVL display | Quantified 0-10 risk score |
| Impermanent loss calc | Manual spreadsheet math | Rarely included | Built-in multi-scenario calculator |
| Strategy recommendations | Research forums/Twitter | Generic suggestions | Personalized to your capital and risk |
| APY sustainability check | Track historical rates | Sometimes shown | Automated sustainability analysis |
| Audit verification | Search audit databases | Not included | Curated database of 20+ protocols |
| Cost | Free (your time) | Free (limited) | Free (comprehensive) |
| API keys required | N/A | Sometimes | **None** |

---

## Quick Start

### Find Top Yields

```bash
echo '{"chain": "ethereum", "min_tvl": 10000000, "limit": 10}' | python3 yield_finder.py
```

### Risk-Score a Pool

```bash
echo '{"protocol": "aave-v3", "chain": "ethereum", "symbol": "USDC"}' | python3 yield_risk_scorer.py
```

### Calculate Impermanent Loss

```bash
echo '{"token_a_symbol": "ETH", "token_b_symbol": "USDC", "initial_price_a": 3000, "current_price_a": 3500}' | python3 impermanent_loss_calc.py
```

### Get Strategy Recommendations

```bash
echo '{"capital_usd": 10000, "risk_tolerance": "medium"}' | python3 yield_strategy.py
```

---

## Scripts

### 1. yield_finder.py

Discover and rank yield opportunities across DeFi with powerful filtering. Queries DeFiLlama's pools endpoint for real-time APY and TVL data.

#### Input Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `chain` | string | No | `"all"` | Filter by blockchain |
| `protocol` | string | No | — | Filter by protocol name |
| `min_tvl` | number | No | `1000000` | Minimum TVL in USD |
| `stablecoin_only` | bool | No | `false` | Only show stablecoin pools |
| `sort_by` | string | No | `"apy"` | Sort by `"apy"` or `"tvl"` |
| `limit` | number | No | `20` | Max results to return |

#### Example Input

```json
{
  "chain": "ethereum",
  "protocol": "aave",
  "min_tvl": 5000000,
  "stablecoin_only": true,
  "sort_by": "apy",
  "limit": 10
}
```

#### Example Output

```json
{
  "success": true,
  "query": {
    "chain": "ethereum",
    "protocol": "aave",
    "min_tvl": 5000000,
    "stablecoin_only": true
  },
  "total_pools_scanned": 8542,
  "results_count": 5,
  "results": [
    {
      "rank": 1,
      "pool": "USDC",
      "chain": "Ethereum",
      "protocol": "aave-v3",
      "apy_total": 5.23,
      "apy_base": 3.10,
      "apy_reward": 2.13,
      "tvl_usd": 1234567890,
      "tvl_display": "$1.23B",
      "stablecoin": true,
      "il_risk": "none",
      "tvl_trend": "growing"
    }
  ],
  "metadata": {
    "data_source": "DeFiLlama",
    "timestamp": "2025-01-15T12:00:00Z"
  }
}
```

#### Features

- Filter by chain, protocol, minimum TVL, stablecoin-only
- Sort results by APY or TVL
- Shows base APY vs reward APY breakdown
- Flags IL risk for non-stablecoin pairs
- Displays TVL trend (growing/shrinking/stable)
- Human-readable TVL formatting ($1.23B, $45.6M)

---

### 2. yield_risk_scorer.py

Quantitatively risk-score individual yield opportunities using multiple risk dimensions.

#### Input Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `pool_id` | string | No | DeFiLlama pool ID for direct lookup |
| `protocol` | string | No | Protocol name (e.g., `"aave-v3"`) |
| `chain` | string | No | Chain filter when searching by symbol |
| `symbol` | string | No | Token symbol when searching by attributes |

Provide either `pool_id` or a combination of `protocol`, `chain`, and `symbol`.

#### Example Input

```json
{
  "protocol": "aave-v3",
  "chain": "ethereum",
  "symbol": "USDC"
}
```

#### Example Output

```json
{
  "success": true,
  "pool": {
    "symbol": "USDC",
    "chain": "Ethereum",
    "protocol": "aave-v3",
    "apy": 5.23,
    "tvl_usd": 1234567890
  },
  "risk_score": 1.5,
  "risk_level": "SAFE",
  "risk_breakdown": {
    "protocol_risk": {
      "score": 1.0,
      "reason": "Blue-chip protocol with multiple audits (Trail of Bits, OpenZeppelin)"
    },
    "tvl_risk": {
      "score": 0.5,
      "reason": "Very high TVL ($1.23B) indicates strong market confidence"
    },
    "apy_sustainability": {
      "score": 1.5,
      "reason": "APY of 5.23% is within sustainable range for lending"
    },
    "il_risk": {
      "score": 0.0,
      "reason": "Single-asset lending pool, no impermanent loss"
    },
    "chain_risk": {
      "score": 1.0,
      "reason": "Ethereum mainnet, most battle-tested chain"
    }
  },
  "audit_info": {
    "audited": true,
    "auditors": ["Trail of Bits", "OpenZeppelin"],
    "audit_score": 9
  },
  "recommendation": "Excellent low-risk yield opportunity. Suitable for conservative allocations."
}
```

#### Risk Dimensions

| Dimension | Weight | What It Measures |
|-----------|--------|-----------------|
| Protocol Risk | 25% | Age, audit history, track record |
| TVL Risk | 20% | Pool size and liquidity depth |
| APY Sustainability | 25% | Whether APY is realistically maintainable |
| IL Risk | 15% | Impermanent loss exposure |
| Chain Risk | 15% | Network maturity and security |

#### Audited Protocols Database

The scorer includes a curated database of 20+ major protocols with their audit history:

| Protocol | Auditors | Audit Score |
|----------|----------|-------------|
| Aave v3 | Trail of Bits, OpenZeppelin | 9/10 |
| Compound v3 | OpenZeppelin, ChainSecurity | 9/10 |
| Lido | Sigma Prime, Quantstamp | 9/10 |
| Uniswap v3 | Trail of Bits | 9/10 |
| MakerDAO | Trail of Bits, Runtime Verification | 9/10 |
| Curve | Trail of Bits, Quantstamp | 8/10 |
| Yearn Finance | Trail of Bits, MixBytes | 8/10 |
| Morpho | Spearbit, Trail of Bits | 8/10 |
| Rocket Pool | Sigma Prime, Consensys | 8/10 |
| Balancer v2 | Trail of Bits, OpenZeppelin | 8/10 |
| Pendle | Ackee Blockchain | 7/10 |
| GMX | ABDK, Quantstamp | 7/10 |
| Convex | MixBytes | 7/10 |
| Frax | Trail of Bits, ABDK | 7/10 |
| EigenLayer | Sigma Prime | 7/10 |
| PancakeSwap | PeckShield, SlowMist | 7/10 |
| SushiSwap | PeckShield, Quantstamp | 7/10 |
| Spark | ChainSecurity | 8/10 |
| Stargate | Quantstamp, Zokyo | 7/10 |
| Instadapp | MixBytes, Dedaub | 7/10 |

---

### 3. impermanent_loss_calc.py

Calculate impermanent loss for liquidity pool positions with multi-scenario analysis. This is a pure math calculator with no external API calls.

#### Input Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `token_a_symbol` | string | No | `"TOKEN_A"` | First token name |
| `token_b_symbol` | string | No | `"TOKEN_B"` | Second token name |
| `initial_price_a` | number | No | — | Initial price of token A |
| `initial_price_b` | number | No | `1.0` | Initial price of token B |
| `current_price_a` | number | No | — | Current price of token A |
| `current_price_b` | number | No | `1.0` | Current price of token B |
| `investment_usd` | number | No | `10000` | Total investment amount in USD |
| `pool_apy` | number | No | `0` | Pool APY for net P&L calculation |
| `price_change_pct` | number | No | — | Quick calc: price change percentage |
| `holding_days` | number | No | `365` | Days held for APY reward calculation |

#### Example: Full Calculation

```json
{
  "token_a_symbol": "ETH",
  "token_b_symbol": "USDC",
  "initial_price_a": 3000,
  "initial_price_b": 1,
  "current_price_a": 3500,
  "current_price_b": 1,
  "investment_usd": 10000,
  "pool_apy": 25.0,
  "holding_days": 180
}
```

#### Example: Quick Calculation

```json
{
  "price_change_pct": 50
}
```

#### Example Output

```json
{
  "success": true,
  "input": {
    "token_a": "ETH",
    "token_b": "USDC",
    "initial_price_a": 3000,
    "current_price_a": 3500,
    "price_change_pct": 16.67
  },
  "impermanent_loss": {
    "il_percentage": -0.64,
    "il_dollar_amount": -64.00,
    "hold_value": 10833.33,
    "lp_value": 10769.33,
    "breakeven_apy": 1.28
  },
  "scenarios": [
    {"price_change": "-50%", "il_pct": "-5.72%", "lp_vs_hold": "-$572"},
    {"price_change": "-30%", "il_pct": "-1.90%", "lp_vs_hold": "-$190"},
    {"price_change": "-10%", "il_pct": "-0.11%", "lp_vs_hold": "-$11"},
    {"price_change": "+10%", "il_pct": "-0.11%", "lp_vs_hold": "-$11"},
    {"price_change": "+30%", "il_pct": "-0.87%", "lp_vs_hold": "-$87"},
    {"price_change": "+50%", "il_pct": "-2.02%", "lp_vs_hold": "-$202"},
    {"price_change": "+100%", "il_pct": "-5.72%", "lp_vs_hold": "-$572"},
    {"price_change": "+200%", "il_pct": "-13.40%", "lp_vs_hold": "-$1340"}
  ],
  "with_apy": {
    "pool_apy": 25.0,
    "holding_days": 180,
    "apy_earnings": 1232.88,
    "net_pnl": 1168.88,
    "profitable": true
  }
}
```

#### IL Formula

```
IL = 2 * sqrt(price_ratio) / (1 + price_ratio) - 1
```

Where `price_ratio = new_price / old_price` for the volatile asset relative to the stable asset.

---

### 4. yield_strategy.py

Generate personalized yield strategy recommendations based on capital, risk tolerance, and preferences.

#### Input Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `capital_usd` | number | No | `10000` | Investment capital in USD |
| `risk_tolerance` | string | No | `"medium"` | `"low"`, `"medium"`, or `"high"` |
| `preferred_chains` | list | No | `["all"]` | Preferred blockchains |
| `stablecoin_preference` | bool | No | `false` | Prefer stablecoin pools |
| `timeframe` | string | No | `"6m"` | Investment horizon (`"1m"`, `"3m"`, `"6m"`, `"1y"`) |

#### Example Input

```json
{
  "capital_usd": 50000,
  "risk_tolerance": "medium",
  "preferred_chains": ["ethereum", "arbitrum"],
  "stablecoin_preference": false,
  "timeframe": "6m"
}
```

#### Example Output

```json
{
  "success": true,
  "profile": {
    "capital_usd": 50000,
    "risk_tolerance": "medium",
    "timeframe": "6 months"
  },
  "strategies": [
    {
      "name": "Conservative Foundation",
      "allocation_pct": 50,
      "allocation_usd": 25000,
      "expected_apy_range": "3-6%",
      "risk_score": 1.5,
      "risk_level": "SAFE",
      "il_exposure": "none",
      "positions": [
        {"protocol": "aave-v3", "chain": "Ethereum", "pool": "USDC Lending", "apy": 5.2, "amount": 15000},
        {"protocol": "lido", "chain": "Ethereum", "pool": "stETH", "apy": 3.8, "amount": 10000}
      ]
    },
    {
      "name": "Balanced Growth",
      "allocation_pct": 35,
      "allocation_usd": 17500,
      "expected_apy_range": "8-15%",
      "risk_score": 4.0,
      "risk_level": "MEDIUM",
      "il_exposure": "moderate",
      "positions": [
        {"protocol": "curve-dex", "chain": "Ethereum", "pool": "3pool", "apy": 8.5, "amount": 10000},
        {"protocol": "uniswap-v3", "chain": "Arbitrum", "pool": "ETH-USDC", "apy": 15.2, "amount": 7500}
      ]
    },
    {
      "name": "Aggressive Alpha",
      "allocation_pct": 15,
      "allocation_usd": 7500,
      "expected_apy_range": "20-40%",
      "risk_score": 6.5,
      "risk_level": "HIGH",
      "il_exposure": "high",
      "positions": [
        {"protocol": "pendle", "chain": "Arbitrum", "pool": "PT-stETH", "apy": 28.0, "amount": 5000},
        {"protocol": "gmx", "chain": "Arbitrum", "pool": "GLP", "apy": 22.0, "amount": 2500}
      ]
    }
  ],
  "portfolio_summary": {
    "weighted_apy": 9.8,
    "weighted_risk": 3.1,
    "total_allocation": 50000,
    "expected_annual_yield": 4900
  }
}
```

#### Strategy Categories

| Category | Risk Level | Typical APY | Characteristics |
|----------|-----------|-------------|-----------------|
| Conservative | SAFE-LOW | 3-6% | Blue-chip lending, liquid staking |
| Balanced | LOW-MEDIUM | 8-15% | Major LP positions, L2 opportunities |
| Aggressive | MEDIUM-HIGH | 20-40% | Yield farming, smaller protocols |

---

## Risk Classification

| Level | Score Range | Description | Recommended Action |
|-------|-----------|-------------|--------------------|
| SAFE | 0-1 | Blue-chip protocols, battle-tested, high TVL | Suitable for large allocations |
| LOW | 2-3 | Established protocols, minor concerns | Good for core portfolio positions |
| MEDIUM | 4-5 | Moderate risk, monitor regularly | Limit to 20-30% of portfolio |
| HIGH | 6-7 | Significant risks present | Small allocation only (5-10%) |
| CRITICAL | 8-10 | Unsustainable APY or dangerous | Avoid entirely |

### Risk Factors Explained

- **Protocol Risk**: Based on audit history, team reputation, age, and track record of security incidents
- **TVL Risk**: Larger TVL indicates more market confidence and liquidity for exits
- **APY Sustainability**: Very high APYs (>50%) often rely on token emissions that dilute value
- **IL Risk**: Volatile asset pairs can suffer significant impermanent loss
- **Chain Risk**: Established mainnets (Ethereum) are safer than newer L2s or sidechains

---

## Composability

DeFi Yield Scout is designed to work with other SpoonOS skills:

### With Smart Contract Auditor
```
1. Find high-yield pool with yield_finder
2. Audit the pool's contract with smart-contract-auditor
3. Risk-score the opportunity with yield_risk_scorer
4. Calculate IL exposure with impermanent_loss_calc
```

### With DeFi Safety Shield
```
1. Get strategy from yield_strategy
2. Verify each protocol's safety with defi-safety-shield
3. Monitor positions for risk changes
```

### With Crypto Market Intelligence
```
1. Check market conditions with crypto-market-intel
2. Adjust strategy based on market sentiment
3. Find yields that align with market outlook
```

---

## Use Cases

### 1. Stablecoin Yield Optimization
Find the best risk-adjusted stablecoin yields for capital preservation:
```bash
echo '{"stablecoin_only": true, "min_tvl": 50000000, "sort_by": "apy", "limit": 15}' | python3 yield_finder.py
```

### 2. Cross-Chain Yield Comparison
Compare the same protocol across multiple chains:
```bash
echo '{"protocol": "aave", "sort_by": "apy"}' | python3 yield_finder.py
```

### 3. Due Diligence on High-APY Pools
Investigate suspiciously high yields before investing:
```bash
echo '{"protocol": "some-new-protocol", "chain": "arbitrum", "symbol": "USDC"}' | python3 yield_risk_scorer.py
```

### 4. LP Position Planning
Calculate expected IL before entering a volatile pair LP:
```bash
echo '{"token_a_symbol": "ETH", "token_b_symbol": "USDC", "initial_price_a": 3000, "current_price_a": 3000, "investment_usd": 50000, "pool_apy": 25}' | python3 impermanent_loss_calc.py
```

### 5. Portfolio Strategy Building
Build a diversified yield portfolio matching your risk profile:
```bash
echo '{"capital_usd": 100000, "risk_tolerance": "low", "preferred_chains": ["ethereum"], "stablecoin_preference": true}' | python3 yield_strategy.py
```

### 6. Protocol Safety Comparison
Compare risk scores across lending protocols:
```bash
echo '{"protocol": "aave-v3", "chain": "ethereum", "symbol": "USDC"}' | python3 yield_risk_scorer.py
echo '{"protocol": "compound-v3", "chain": "ethereum", "symbol": "USDC"}' | python3 yield_risk_scorer.py
echo '{"protocol": "morpho", "chain": "ethereum", "symbol": "USDC"}' | python3 yield_risk_scorer.py
```

### 7. Market Downturn Preparation
Assess how price drops affect your LP positions:
```bash
echo '{"token_a_symbol": "ETH", "token_b_symbol": "USDC", "initial_price_a": 3000, "current_price_a": 2000, "investment_usd": 25000, "pool_apy": 30}' | python3 impermanent_loss_calc.py
```

---

## Supported Chains

| Chain | DeFiLlama Key | Yield Finder | Risk Scorer | IL Calc | Strategy |
|-------|---------------|-------------|-------------|---------|----------|
| Ethereum | `Ethereum` | Yes | Yes | Yes | Yes |
| BSC | `BSC` | Yes | Yes | Yes | Yes |
| Polygon | `Polygon` | Yes | Yes | Yes | Yes |
| Arbitrum | `Arbitrum` | Yes | Yes | Yes | Yes |
| Base | `Base` | Yes | Yes | Yes | Yes |
| Optimism | `Optimism` | Yes | Yes | Yes | Yes |
| Avalanche | `Avalanche` | Yes | Yes | Yes | Yes |
| Solana | `Solana` | Yes | Yes | Yes | Yes |
| Fantom | `Fantom` | Yes | Yes | Yes | Yes |
| Gnosis | `Gnosis` | Yes | Yes | Yes | Yes |

---

## API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `https://yields.llama.fi/pools` | GET | All DeFi pools with APY/TVL data |
| `https://api.llama.fi/protocols` | GET | Protocol metadata (TVL, chains, etc.) |

Both endpoints are free, require no API keys, and have no strict rate limits (be respectful with retry logic for 429 responses).

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| *(none)* | — | **No environment variables or API keys needed** |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-01-15 | Initial release with all four scripts |

---

## License

Open source. Free to use, modify, and distribute.
