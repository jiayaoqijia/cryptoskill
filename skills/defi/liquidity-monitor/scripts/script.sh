#!/usr/bin/env bash
# liquidity-monitor — DeFi Liquidity Analysis Reference
set -euo pipefail
VERSION="4.0.0"

cmd_intro() { cat << 'EOF'
# DeFi Liquidity — Overview

## Automated Market Maker (AMM) Mechanics
  Traditional order book: Buyers and sellers place limit orders
  AMM: Liquidity pools replace order books with mathematical formulas
  Core innovation: Anyone can be a market maker by depositing tokens

## Constant Product Formula (Uniswap V2)
  x × y = k  (where x and y are token reserves, k is constant)
  Price = y/x (token Y price in terms of token X)
  When you buy token X: x decreases, y increases, k stays same
  Larger pools = less slippage (price impact per trade is smaller)
  Example: Pool has 100 ETH × 200,000 USDC = k(20,000,000)
    Buy 1 ETH → new reserves: 99 ETH × 202,020 USDC → price ~$2,020

## Concentrated Liquidity (Uniswap V3)
  LPs specify price range for their liquidity (not full range)
  Capital efficiency: 4000x improvement possible vs V2
  Tick system: Price space divided into discrete ticks (1 bps each)
  Active liquidity: Only positions in current price range earn fees
  Risk: If price moves outside range, position becomes 100% one token

## Pool Types
  Uniswap V2/V3: General-purpose token pairs
  Curve StableSwap: Optimized for pegged assets (stablecoins, wETH/ETH)
    Uses StableSwap invariant: Amplification parameter (A) controls curve shape
  Balancer: Weighted pools (e.g., 80/20 ETH/USDC instead of 50/50)
  GMX/Synthetix: Liquidity pool as counterparty (LP vs traders)
  Concentrated ALMs: Arrakis, Gamma, Bunni (manage V3 positions automatically)
EOF
}

cmd_standards() { cat << 'EOF'
# AMM Mathematics & Standards

## Uniswap V2 Math
  Invariant: x × y = k
  Price: P = y / x
  Trade output: dy = y × dx / (x + dx) — minus 0.3% fee
  Price impact: 1 - (output / (input × spot_price))
  LP share: your_liquidity / total_liquidity × fees_earned

## Uniswap V3 Math
  Virtual reserves within price range [Pa, Pb]:
  L = sqrt(k) = sqrt(x × y)  (liquidity concentration)
  Real reserves: x_real = L × (1/sqrt(P) - 1/sqrt(Pb))
                 y_real = L × (sqrt(P) - sqrt(Pa))
  Fee tiers: 0.01% (stable), 0.05% (stable), 0.3% (standard), 1% (exotic)
  Tick spacing: 1 (0.01%), 10 (0.05%), 60 (0.3%), 200 (1%)

## Curve StableSwap Invariant
  Combines constant product (x×y=k) with constant sum (x+y=k):
  A × n^n × sum(xi) + D = A × D × n^n + D^(n+1) / (n^n × prod(xi))
  A = Amplification factor (typically 100-2000 for stablecoins)
  Higher A = flatter curve = less slippage for pegged assets
  A=0 → constant product, A=∞ → constant sum

## Balancer Weighted Pools
  Generalized invariant: prod(Bi^Wi) = k
  Bi = balance of token i, Wi = weight of token i
  Allows arbitrary weights (not just 50/50)
  80/20 pool: 80% exposure to token A, 20% to B
  Impermanent loss is lower with asymmetric weights

## Fee Distribution
  Uniswap V2: 0.3% fee, 100% to LPs
  Uniswap V3: Variable fee tier, 100% to active LPs
  Curve: 0.04% fee, 50% to LPs, 50% to veCRV holders
  Balancer: Configurable fee (0.01-10%), protocol revenue share
  Sushiswap: 0.3% (0.25% LPs, 0.05% xSUSHI stakers)
EOF
}

cmd_troubleshooting() { cat << 'EOF'
# Liquidity Troubleshooting

## Impermanent Loss (IL)
  Definition: Difference in value between holding tokens vs providing LP
  Formula: IL = 2×sqrt(price_ratio) / (1 + price_ratio) - 1
  Examples:
    1.25x price change → 0.6% IL
    1.50x price change → 2.0% IL
    2x price change    → 5.7% IL
    3x price change    → 13.4% IL
    5x price change    → 25.5% IL
  Becomes permanent when you withdraw at different price
  Mitigation: LP in correlated pairs (ETH/stETH), earn enough fees to offset

## Failed Swap Routes
  "INSUFFICIENT_OUTPUT_AMOUNT": Slippage too low for current volatility
  Fix: Increase slippage tolerance (0.5% → 1-3%)
  "TRANSFER_FROM_FAILED": Token has transfer tax/fee (reflection tokens)
  Fix: Increase slippage to cover tax (often 5-12%)
  "EXPIRED": Transaction deadline passed (block confirmation too slow)
  Fix: Increase deadline from 20 to 30+ minutes

## MEV Sandwich Attacks
  Attacker sees your pending swap in mempool
  Front-run: Buy before you, raising price
  Your swap executes at worse price
  Back-run: Attacker sells immediately after, pocketing difference
  Protection:
    - Use private transaction pools (Flashbots Protect, MEV Blocker)
    - Set tight slippage (but may cause failures)
    - Use DEX aggregators with MEV protection (CowSwap, 1inch Fusion)
    - Submit via builder API (bypasses public mempool)

## Liquidity Position Issues
  V3 "Out of range": Price moved outside your position range
    Option 1: Wait for price to return
    Option 2: Remove + create new position at current price
    Option 3: Use ALM (Arrakis, Gamma) for auto-rebalancing
  "Insufficient liquidity": Pool too small for your trade size
    Fix: Split trade across multiple pools, use aggregator
    Fix: Use limit orders instead of market swaps
EOF
}

cmd_performance() { cat << 'EOF'
# Liquidity Optimization

## Optimal Pool Selection
  Factors to evaluate:
    1. TVL: Higher = less slippage, more stable
    2. Volume/TVL ratio: Higher = more fee revenue for LPs
    3. Fee tier: Match to pair volatility (stable=0.05%, volatile=0.3%+)
    4. Protocol: Established (Uniswap, Curve) vs new (higher risk, higher APR)
    5. Chain: Gas costs matter — L2s for smaller positions

  APR estimation:
    APR = (daily_fees × 365) / position_value × 100%
    Don't forget: Subtract IL, gas costs for deposits/withdrawals/claims
    Real yield = Fees - IL - Gas - Opportunity cost

## Multi-Hop Routing
  Direct swap: ETH → USDC (one pool)
  Multi-hop: ETH → WBTC → USDC (two pools, sometimes cheaper)
  Aggregators find optimal routes across:
    - Multiple DEXs (Uniswap, Sushiswap, Curve, Balancer)
    - Multiple pools per DEX (different fee tiers)
    - Split orders (30% through Pool A, 70% through Pool B)
  Gas cost: Each hop costs ~100K gas, weigh against price improvement

## Gas Optimization
  Uniswap V3 position creation: ~300K gas (~$5-15 on Ethereum)
  Claim fees: ~100K gas
  Remove liquidity: ~200K gas
  Strategy: Compound less frequently for smaller positions
  L2 deployment: Same operations on Arbitrum/Optimism cost ~$0.10-0.50
  Batch operations: Some protocols allow multi-position management

## Position Sizing
  Small position (<$1K): Use L2s (Arbitrum, Optimism, Base)
  Medium ($1K-50K): Mainnet viable, choose wide ranges for less maintenance
  Large (>$50K): Consider managed solutions (Arrakis, professional LPs)
  Rule: Gas costs to deposit + claim should be <10% of expected annual fees
EOF
}

cmd_security() { cat << 'EOF'
# DeFi Liquidity Security

## Rug Pull Detection
  Check before providing liquidity:
    1. Locked liquidity: Is LP locked in a time-lock contract?
       Tools: Team.finance, Unicrypt, DXSale lock checker
    2. Contract verified on Etherscan: Unverified = red flag
    3. Renounced ownership: Owner can't mint/pause/blacklist
    4. Audit reports: CertiK, Trail of Bits, OpenZeppelin
    5. Token distribution: >50% held by one wallet = centralized risk

  Red flags:
    - Anonymous team with no history
    - Forked contract with hidden modifications
    - Unrealistic APY (>1000% sustained = unsustainable)
    - No time-lock on admin functions
    - Transfer fees >5% or modifiable transfer tax

## Honeypot Token Detection
  Honeypot: Can buy but cannot sell
  How: Token contract restricts transfers for non-whitelisted addresses
  Check tools:
    - honeypot.is (EVM chains)
    - tokensniffer.com (scam score)
    - gopluslabs.io (security API)
    - dexscreener.com (check sell transactions exist)
  Test: Try selling small amount before large position

## Flash Loan Attack Vectors
  Price oracle manipulation:
    1. Borrow large amount via flash loan
    2. Manipulate pool price (large swap)
    3. Exploit protocol using manipulated price
    4. Repay flash loan with profit
  Prevention for protocols:
    - Use TWAP oracles (not spot price)
    - Chainlink price feeds (off-chain, manipulation-resistant)
    - Multi-block TWAP (harder to manipulate across blocks)

## Smart Contract Risks
  Always check: Is the pool contract the official deployment?
  Verify: Factory contract address matches official docs
  Risk: Interacting with fake pool drains your tokens
  Approval: Don't approve unlimited tokens to unknown contracts
  Revoke: Use revoke.cash to remove old approvals
EOF
}

cmd_migration() { cat << 'EOF'
# Liquidity Migration Guide

## Uniswap V2 → V3 Migration
  Why migrate:
    - V3 concentrated liquidity = higher capital efficiency
    - V3 multiple fee tiers = better fee optimization
    - V2 liquidity gradually declining
  Steps:
    1. Remove V2 LP position (receive token A + token B)
    2. Choose V3 fee tier (0.05% stable, 0.3% standard, 1% exotic)
    3. Set price range (wider = less maintenance, narrower = higher fees)
    4. Deposit tokens into V3 position
    5. Monitor: Rebalance if price moves outside range
  Warning: V3 requires active management vs V2 set-and-forget
  ALM option: Deposit into Arrakis/Gamma vault for auto-rebalancing

## Cross-Chain Liquidity Bridging
  Canonical bridges (safest, slowest):
    Arbitrum bridge: 7-day withdrawal wait
    Optimism bridge: 7-day withdrawal wait
    zkSync bridge: Minutes for deposits, hours for withdrawals
  Third-party bridges (faster, more risk):
    Across Protocol: Minutes, competitive fees
    Stargate (LayerZero): Fast, multiple chains
    Wormhole: Many chains, $320M hack history (2022)
    Hop Protocol: L2-to-L2 fast transfers
  Best practice:
    - Large amounts: Use canonical bridges (worth the wait)
    - Small amounts: Third-party bridges acceptable
    - Never bridge >10% of portfolio through one bridge

## Single-Chain → Multi-Chain LP
  Strategy: Spread liquidity across chains for diversification
  Popular chains for LPing:
    Ethereum: Highest TVL, highest fees, highest gas
    Arbitrum: ~80% of Ethereum liquidity, much lower gas
    Base: Growing fast, Coinbase-backed
    Polygon: Low gas, ample liquidity
    BSC: High volume, different user base
  Tools: DefiLlama for TVL comparison across chains
EOF
}

cmd_cheatsheet() { cat << 'EOF'
# DeFi Liquidity Quick Reference

## DEX Aggregator APIs
  1inch:     api.1inch.dev/swap/v5.2/{chainId}/swap
  0x:        api.0x.org/swap/v1/quote
  Paraswap:  apiv5.paraswap.io/prices
  CowSwap:   api.cow.fi/mainnet/api/v1/quote
  Jupiter:   quote-api.jup.ag/v6/quote (Solana)

## Pool Analytics Dashboards
  DefiLlama:    defillama.com/yields (APY across all protocols)
  Revert:       revert.finance (Uniswap V3 position analytics)
  Dune:         dune.com (custom queries for any on-chain data)
  DexScreener:  dexscreener.com (real-time pair charts and TVL)
  GeckoTerminal: geckoterminal.com (multi-chain DEX data)
  APY.vision:   apy.vision (LP position tracking and P&L)

## Impermanent Loss Calculator
  IL% = 2×sqrt(r) / (1+r) - 1    where r = new_price / old_price
    r=1.1  → IL=0.11%    r=1.5  → IL=2.02%
    r=2.0  → IL=5.72%    r=3.0  → IL=13.4%
    r=5.0  → IL=25.5%    r=0.5  → IL=5.72% (same as 2x)
  Breakeven: Fees earned must exceed IL for profit

## TVL Tracking
  DefiLlama total DeFi TVL: ~$90B (as of late 2024)
  Top protocols by TVL:
    Lido:     ~$15B (liquid staking)
    AAVE:     ~$10B (lending)
    Uniswap:  ~$5B  (DEX)
    Curve:    ~$2B  (stablecoin DEX)
    MakerDAO: ~$8B  (CDP/stablecoin)

## Key Contract Addresses (Ethereum)
  Uniswap V3 Router:  0xE592427A0AEce92De3Edee1F18E0157C05861564
  Uniswap V3 Factory: 0x1F98431c8aD98523631AE4a59f267346ea31F984
  Curve 3pool:        0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7
  Balancer Vault:     0xBA12222222228d8Ba445958a75a0704d566BF2C8
  WETH:               0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2
EOF
}

cmd_faq() { cat << 'EOF'
# DeFi Liquidity — FAQ

Q: Is providing liquidity profitable?
A: Depends on pair, pool, and market conditions.
   Profitable when: High volume/TVL ratio, fees > impermanent loss.
   Unprofitable when: Large price divergence, low trading volume.
   Stablecoin pairs (USDC/USDT): Low IL, steady fees (~5-15% APR).
   Volatile pairs (ETH/SHIB): High fees but high IL risk.
   Track with revert.finance or APY.vision to know your actual P&L.

Q: V2 or V3 — which should I use?
A: V3 for active LPs: Higher capital efficiency, more fees per dollar.
   V2 for passive LPs: Set and forget, no range management.
   Compromise: Use V3 with wide ranges (mimics V2 behavior).
   Or use ALM vaults (Arrakis, Gamma) for automated V3 management.
   V2 still has liquidity for some pairs; check both before choosing.

Q: How do I avoid MEV/sandwich attacks?
A: Use private transaction submission:
   - Flashbots Protect RPC: Add to MetaMask as custom network
   - MEV Blocker: rpc.mevblocker.io
   - CowSwap: Batch auctions inherently MEV-resistant
   Set reasonable slippage (0.5-1%) — too high invites sandwiching.
   Large trades: Use TWAP (split over time) or limit orders.

Q: What's the minimum amount to LP profitably?
A: On Ethereum mainnet: $5K+ (gas costs eat into smaller positions).
   On L2s (Arbitrum/Base): $100+ is viable.
   Rule: Annual fees should be >10x your gas costs for deposits+claims.
   Example: $500 position earning 10% = $50/year.
   If gas for setup+3 claims = $15, that's 30% of earnings (too high).

Q: How do I track my LP position performance?
A: Tools: revert.finance (V3), APY.vision, DeBank.
   Key metrics: Fees earned, IL incurred, net P&L vs holding.
   Tax: Each deposit/withdrawal may be a taxable event.
   Record: Save transaction hashes for tax reporting.
EOF
}

cmd_help() {
    echo "liquidity-monitor v$VERSION — DeFi Liquidity Analysis Reference"
    echo ""
    echo "Usage: liquidity-monitor <command>"
    echo ""
    echo "Commands:"
    echo "  intro           AMM mechanics, pool types, concentrated liquidity"
    echo "  standards       Uniswap V2/V3 math, Curve, Balancer formulas"
    echo "  troubleshooting IL calculation, failed swaps, MEV protection"
    echo "  performance     Pool selection, routing, gas optimization"
    echo "  security        Rug pull detection, honeypots, flash loans"
    echo "  migration       V2→V3, cross-chain bridging, multi-chain LP"
    echo "  cheatsheet      DEX APIs, analytics tools, IL calculator, TVL"
    echo "  faq             Profitability, V2 vs V3, MEV, minimum amounts"
    echo "  help            Show this help"
}

case "${1:-help}" in
    intro) cmd_intro ;; standards) cmd_standards ;;
    troubleshooting) cmd_troubleshooting ;; performance) cmd_performance ;;
    security) cmd_security ;; migration) cmd_migration ;;
    cheatsheet) cmd_cheatsheet ;; faq) cmd_faq ;;
    help|--help|-h) cmd_help ;;
    *) echo "Unknown: $1"; echo "Run: liquidity-monitor help" ;;
esac
