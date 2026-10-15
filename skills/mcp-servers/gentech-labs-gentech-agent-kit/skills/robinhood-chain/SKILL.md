---
name: robinhood-chain
description: "Build AI agents that trade tokenized stocks and use x402 payments on Robinhood Chain. Covers USDG settlement, stock price APIs, and Naven Network facilitator integration."
---

# Robinhood Chain for AI Agents

Robinhood Chain (chain ID 4663) is an EVM-compatible OP Stack chain with native tokenized stocks (AAPL, NVDA, TSLA) and USDG settlement via x402.

## Network Details

| Property | Value |
|----------|-------|
| Chain ID | 4663 |
| RPC | `https://rpc.mainnet.chain.robinhood.com` |
| Explorer | `https://robinhoodchain.blockscout.com` |
| Native Token | ETH |
| Settlement Token | USDG (`0x5fc5360D0400a0Fd4f2af552ADD042D716F1d168`) |
| x402 Facilitator | `https://facilitator.naven.network` |

## Tokenized Stocks (16)

| Symbol | Name | Category |
|--------|------|----------|
| AAPL | Apple Inc. | Stock |
| NVDA | NVIDIA Corporation | Stock |
| TSLA | Tesla Inc. | Stock |
| MSFT | Microsoft Corporation | Stock |
| META | Meta Platforms Inc. | Stock |
| AMZN | Amazon.com Inc. | Stock |
| GOOGL | Alphabet Inc. | Stock |
| COIN | Coinbase Global Inc. | Stock |
| QQQ | Invesco QQQ Trust | ETF |
| SPY | SPDR S&P 500 ETF Trust | ETF |
| SGOV | iShares 0-3 Month Treasury Bond ETF | ETF |

Full list: `rh_list_stocks()` tool.

## Agent Kit Tools

| Tool | Description | Price |
|------|-------------|-------|
| `rh_info()` | Chain status, block number, facilitator health | Free |
| `rh_list_stocks()` | All available tokenized stocks | Free |
| `rh_get_stock(symbol)` | Stock price (AAPL, NVDA, etc.) | $0.005 USDG |
| `rh_crypto_quote(symbol)` | Crypto price via CMC | $0.001 USDG |
| `rh_verify_payment(proof)` | Verify x402 payment via Naven | x402 fee |

## Integration with Atelier

GenTech agents are listed on Atelier marketplace and now hireable from Robinhood Chain. Payment flow:

1. Agent selects a service on Atelier
2. Signs x402 payment (USDG on Robinhood Chain)
3. Naven Network facilitates settlement
4. Order created, seller paid within seconds

## RWA Strategy

Robinhood Chain makes tokenized stocks accessible to AI agents. Use cases:
- **Portfolio rebalancing agents** — check stock prices, trigger trades
- **Yield comparison agents** — compare stock returns vs DeFi yields
- **Research agents** — pull real-time market data across asset classes

Combine with the Output Enforcer to validate all financial data responses.
