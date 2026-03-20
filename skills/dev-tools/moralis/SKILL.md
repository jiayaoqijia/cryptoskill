---
name: moralis
description: "Moralis — Web3 data, token prices, wallet history, NFTs, DeFi positions, and blockchain events."
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "🌐", "requires": {"env": ["MORALIS_API_KEY"]}, "primaryEnv": "MORALIS_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---

# 🌐 Moralis

Moralis — Web3 data, token prices, wallet history, NFTs, DeFi positions, and blockchain events.

## Requirements

| Variable | Required | Description |
|----------|----------|-------------|
| `MORALIS_API_KEY` | ✅ | Moralis API key |


## Quick Start

```bash
# Get native balance
python3 {{baseDir}}/scripts/moralis.py get-native-balance --address <value> --chain "eth"

# Get ERC-20 token balances
python3 {{baseDir}}/scripts/moralis.py get-token-balances --address <value> --chain "eth"

# Get wallet transactions
python3 {{baseDir}}/scripts/moralis.py get-transactions --address <value> --chain "eth"

# Get token price
python3 {{baseDir}}/scripts/moralis.py get-token-price --address <value> --chain "eth"

# Get NFTs for wallet
python3 {{baseDir}}/scripts/moralis.py get-nfts --address <value> --chain "eth"

# Get NFT metadata
python3 {{baseDir}}/scripts/moralis.py get-nft-metadata --address <value> --token-id <value> --chain "eth"

# Get NFT transfers
python3 {{baseDir}}/scripts/moralis.py get-nft-transfers --address <value> --chain "eth"

# Get token transfers
python3 {{baseDir}}/scripts/moralis.py get-token-transfers --address <value> --chain "eth"

# Get DeFi positions
python3 {{baseDir}}/scripts/moralis.py get-defi-positions --address <value> --chain "eth"

# Resolve ENS/Unstoppable domain
python3 {{baseDir}}/scripts/moralis.py resolve-domain --domain <value>

# Search token by symbol
python3 {{baseDir}}/scripts/moralis.py search-token --symbol <value>

# Get block details
python3 {{baseDir}}/scripts/moralis.py get-block --block <value> --chain "eth"
```

## Output Format

All commands output JSON by default.

## Script Reference

| Script | Description |
|--------|-------------|
| `{baseDir}/scripts/moralis.py` | Main CLI — all commands in one tool |

## Credits
Built by [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) | [agxntsix.ai](https://www.agxntsix.ai)
[YouTube](https://youtube.com/@aiwithabidi) | [GitHub](https://github.com/aiwithabidi)
Part of the **AgxntSix Skill Suite** for OpenClaw agents.

📅 **Need help setting up OpenClaw for your business?** [Book a free consultation](https://cal.com/agxntsix/abidi-openclaw)
