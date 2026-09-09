---
name: drift
description: "Read live Drift Protocol mainnet data — Solana's largest non-custodial perps DEX. Use for market scanning, funding analysis, orderbook depth, and user position auditing. The Solana-native alternative to Hyperliquid: same custody-free model (on-chain collateral, user-held keys), different blockchain. Read-only in this release — trading on Drift requires Solana program instructions + Ed25519 signing, which is deferred. Triggers: drift, drift protocol, solana perps, SOL-PERP, BONK-PERP, WIF-PERP, drift funding, perps on solana, app.drift.trade."
---

# ChainGPT Drift Skill

You read live Drift Protocol data on behalf of the user. Drift is Solana's dominant perpetuals DEX — same non-custodial model as Hyperliquid (user keeps the keys, the on-chain program holds collateral), running on Solana mainnet instead of an app-chain.

**This release is read-only.** Trading on Drift requires constructing Solana program instructions (Anchor IDL) and signing with the user's Solana keypair (Ed25519) — a different signing flow than the EVM-only path the rest of this plugin uses. Deferred to a follow-up.

## Tools

| Tool | Purpose |
|---|---|
| `chaingpt_drift_markets` | Enumerate all perp markets sorted by volume / OI / funding |
| `chaingpt_drift_market` | One-market detail: mark, oracle, funding, max leverage |
| `chaingpt_drift_orderbook` | L2 orderbook depth for sizing trades |
| `chaingpt_drift_funding` | Historical funding rates (24h / 7d) with annualized avg |
| `chaingpt_drift_user` | Account state: collateral, positions, leverage, open orders |

## When to use Drift over Hyperliquid

- The user is already on Solana and doesn't want to bridge to Hyperliquid's L1.
- The user wants to trade Solana-native memecoin perps (BONK, WIF, POPCAT, etc.) which Drift lists earlier and more aggressively than Hyperliquid.
- The user is running a Solana-side funding-rate arb (long spot on Jupiter, short perp on Drift) where keeping everything on one chain saves rent + transfer time.
- Composition with other Solana protocols (Kamino, marginfi) for delta-neutral yield strategies.

## When Hyperliquid is the right call

- Higher liquidity / tighter spreads on majors (BTC, ETH, SOL).
- Deeper orderbooks for large size.
- The user already has USDC on Hyperliquid's L1 and doesn't want to bridge to Solana.

## Typical pipeline

```text
chaingpt_drift_markets sortBy=volume           # scan top markets
       │  (user picks a candidate)
       ▼
chaingpt_drift_market marketIndex=0            # confirm mark/oracle/funding
chaingpt_drift_funding marketIndex=0 window=24h  # check recent funding trend
chaingpt_drift_orderbook marketIndex=0 depth=10  # check size vs liquidity
       │
       ▼
[user trades via https://app.drift.trade]
       │
       ▼
chaingpt_drift_user authority=<solana-pubkey>  # confirm fill landed
```

## Funding-rate arb workflow

```text
chaingpt_drift_markets sortBy=funding         # surface markets with extreme funding
       │  (positive funding = longs pay shorts; short the perp, long the spot)
       ▼
chaingpt_drift_funding marketIndex=<idx>      # is the funding skew persistent or one-spike?
chaingpt_dex_jupiter_quote                    # cost to acquire the spot leg
       │
       ▼
[execute: long spot on Jupiter + short perp on Drift via app.drift.trade]
```

## What this skill does NOT do

- Execute trades. The Solana signing flow is intentionally not wired here.
- Calculate liquidation prices. Drift's cross-margin model with multiple collateral types makes this nontrivial — surface raw collateral + leverage and let the user inspect on the official UI for liquidation.
- Cross-chain bridging into Solana — use `chaingpt_bridge_quote` for EVM↔EVM only. For EVM→Solana, suggest Wormhole / deBridge separately.

## Credit accounting

All Drift tools cost **0 ChainGPT credits**. The credit funnel comes from upstream tools the user calls before deciding to trade (`chaingpt_research_token`, `chaingpt_news_fetch`, etc.).

## Reference

- Drift docs: https://docs.drift.trade
- Public DLOB API: https://dlob.drift.trade
- Data API: https://data.api.drift.trade
- Drift v2 program id: `dRiftyHA39MWEi3m9aunc5MzRF1JYuBsbn6VPcn33UH`
