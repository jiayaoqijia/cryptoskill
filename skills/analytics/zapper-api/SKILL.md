---
name: zapper-api
description: Query DeFi portfolios, token holdings, NFTs, transactions, and prices via Zapper API. Supports 50+ chains. Use when user asks about wallet balances, DeFi positions, NFT collections, token prices, or transaction history.
homepage: https://zapper.xyz
metadata: {"openclaw":{"emoji":"🟪","requires":{"bins":["python3"]},"primaryEnv":"ZAPPER_API_KEY"}}
---

# Zapper API

Query DeFi portfolios, NFTs, and transactions across 50+ chains using Zapper's GraphQL API.

## Setup

1. Get API key from [Zapper Dashboard](https://zapper.xyz/developers) (free tier available)
2. Configure in `~/.config/zapper/addresses.json`:
   ```json
   {
     "apiKey": "your-api-key",
     "wallets": [
       {"label": "Main", "address": "0x..."},
       {"label": "DeFi", "address": "0x..."}
     ]
   }
   ```

Or set environment variable: `export ZAPPER_API_KEY="your-api-key"`

## Commands

| Command | Description | Example |
|---------|-------------|---------|
| `portfolio <address>` | Token + DeFi totals | `zapper.py portfolio 0x123...` |
| `tokens <address>` | Detailed token holdings | `zapper.py tokens 0x123...` |
| `apps <address>` | DeFi positions (LPs, lending, staking) | `zapper.py apps 0x123...` |
| `nfts <address>` | NFT holdings by value | `zapper.py nfts 0x123...` |
| `tx <address>` | Recent transactions (30 days) | `zapper.py tx 0x123...` |
| `price <symbol>` | Token price lookup | `zapper.py price ETH` |
| `claimables <address>` | Unclaimed rewards | `zapper.py claimables 0x123...` |
| `config` | Show configuration | `zapper.py config` |

## Options

| Flag | Commands | Description |
|------|----------|-------------|
| `--24h` | portfolio, tokens | Show 24h price changes |
| `--short` | portfolio | Output only total value |
| `--per-wallet` | portfolio | Show each configured wallet separately |
| `--json` | all | Output raw JSON |
| `--limit N` | most | Max items to display |

## Usage

```bash
# Portfolio summary
python3 scripts/zapper.py portfolio 0xADDRESS

# With 24h price changes
python3 scripts/zapper.py portfolio 0xADDRESS --24h

# Just total value
python3 scripts/zapper.py portfolio 0xADDRESS --short

# Per-wallet breakdown
python3 scripts/zapper.py portfolio --per-wallet

# Token holdings with prices
python3 scripts/zapper.py tokens 0xADDRESS --24h

# DeFi positions
python3 scripts/zapper.py apps 0xADDRESS

# NFT holdings
python3 scripts/zapper.py nfts 0xADDRESS

# Recent transactions
python3 scripts/zapper.py tx 0xADDRESS

# Token price
python3 scripts/zapper.py price ETH

# Unclaimed rewards
python3 scripts/zapper.py claimables 0xADDRESS

# JSON output
python3 scripts/zapper.py portfolio 0xADDRESS --json
```

## Wallet Labels

Use configured wallet labels instead of addresses:

```bash
python3 scripts/zapper.py portfolio "Main"
python3 scripts/zapper.py tokens "DeFi"
```

## Supported Tokens (price command)

ETH, WETH, USDC, USDT, DAI, WBTC, LINK, UNI, AAVE, MKR

## Supported Chains

Ethereum, Base, Arbitrum, Optimism, Polygon, Solana, BNB Chain, Avalanche, zkSync, Linea, Scroll, Blast, and 40+ more.

## Notes

- Free tier API key available at [zapper.xyz/developers](https://zapper.xyz/developers)
- Rate limits apply - avoid rapid repeated requests
- NFT valuations based on floor prices
- Transaction history limited to 30 days

## References

- [API.md](references/API.md) - GraphQL query examples
- [Zapper Docs](https://build.zapper.xyz/docs/api/) - Official API documentation
