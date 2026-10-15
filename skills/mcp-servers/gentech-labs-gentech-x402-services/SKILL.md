---
name: gentech-x402-services
description: "GenTech Labs paid API gateway — 7 x402 pay-per-call services on Base USDC: token security, market data, agent discovery, DeFi LP analytics, wallet analysis, NFT search. Use when an agent needs token risk scoring, token prices, onchain agent discovery, LP/pool analytics, wallet portfolio data, or NFT collection search and is willing to pay USDC per request via x402 ($0.005–$0.02)."
version: 1.0.0
author: GenTech Labs
tags: [x402, payments, usdc, security, defi, nft, market-data, agents]
---

# GenTech x402 Services

Pay-per-call API gateway by GenTech Labs. No API key, no account, no signup — any x402-capable agent pays USDC on Base per request and gets data back.

## How to use (for Bankr agents)

1. Call the endpoint for your service. You'll get `HTTP 402 Payment Required` with an x402 v2 envelope.
2. The envelope tells you the price, USDC asset, payTo address, and EIP-712 domain (name "USD Coin", version "2").
3. Sign the payment via EIP-3009 (gasless `transferWithAuthorization`) and retry with `Authorization: x402 <proof>` or `X-Payment` header.
4. You get `HTTP 200` with real data. Payments settle on-chain on Base in USDC.

## Endpoints (all on https://api.gentechlabs.net)

| Endpoint | Service | Price | Example |
|---|---|---|---|
| `GET /v1/security/score/{address}` | Token security / rug risk | $0.01 | `/v1/security/score/So11111111111111111111111111111111111111112` |
| `GET /v1/market/price/{symbol}` | Market price | $0.005 | `/v1/market/price/ETH` |
| `GET /v1/agents/search?q={query}` | On-chain agent discovery (ERC-8004) | $0.01 | `/v1/agents/search?q=gentech` |
| `GET /v1/defi/lp/{address}` | LP pool analytics | $0.02 | `/v1/defi/lp/{tokenAddress}` |
| `GET /v1/wallet/portfolio/{address}` | Wallet analysis | $0.02 | `/v1/wallet/portfolio/{walletAddress}` |
| `GET /v1/nft/search?q={query}` | NFT collection search | $0.01 | `/v1/nft/search?q=mad%20lads` |
| `GET /v1/defender/classify/{chainId}/{token}` | Airdrop/dust-token defense — classifies tokens as KNOWN/SUSPICIOUS (homoglyph impersonation, no liquidity), quarantine + safe burn calldata | $0.01 | `/v1/defender/classify/43114/0x8e53ad52980478794bb5b459b7cbdd836975e4cb` |

## Discovery

- x402 manifest: `https://api.gentechlabs.net/.well-known/x402`
- Full bazaar manifest (all services + prices): `https://api.gentechlabs.net/.well-known/x402-bazaar`

## Example flow

```bash
# 1. Trigger the 402
curl -s https://api.gentechlabs.net/v1/market/price/ETH
# → 402 + accepts[{scheme: exact, network: eip155:8453, asset: 0x833589... (USDC Base), amount, payTo, extra: {name: "USD Coin", version: "2"}}]

# 2. Sign EIP-3009 transferWithAuthorization (gasless, USDC on Base), then retry:
curl -s -H "Authorization: x402 <proof>" https://api.gentechlabs.net/v1/market/price/ETH
# → 200 {"symbol":"ETH","priceUsd":...}
```

## Notes

- All payments in USDC on Base (eip155:8453), contract `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`.
- Prices are exact-scheme; underpayment is rejected with 402.
- EIP-712 domain: `{name: "USD Coin", version: "2"}` — required for signature.
- Supports both `Authorization: x402 <proof>` and `X-Payment: <proof>` headers.
