---
name: alchemy
description: "Alchemy — blockchain data, NFTs, token balances, transactions, gas prices, and webhooks."
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "⛓️", "requires": {"env": ["ALCHEMY_API_KEY"]}, "primaryEnv": "ALCHEMY_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---

# ⛓️ Alchemy

Alchemy — blockchain data, NFTs, token balances, transactions, gas prices, and webhooks.

## Requirements

| Variable | Required | Description |
|----------|----------|-------------|
| `ALCHEMY_API_KEY` | ✅ | Alchemy API key |


## Quick Start

```bash
# Get ETH balance
python3 {{baseDir}}/scripts/alchemy.py get-balance --address <value>

# Get ERC-20 token balances
python3 {{baseDir}}/scripts/alchemy.py get-token-balances --address <value>

# Get transaction by hash
python3 {{baseDir}}/scripts/alchemy.py get-transaction --hash <value>

# Get block by number
python3 {{baseDir}}/scripts/alchemy.py get-block --block "latest"

# Get NFTs for address
python3 {{baseDir}}/scripts/alchemy.py get-nfts --address <value>

# Get NFT metadata
python3 {{baseDir}}/scripts/alchemy.py get-nft-metadata --contract <value> --token-id <value>

# Get token metadata
python3 {{baseDir}}/scripts/alchemy.py get-token-metadata --contract <value>

# Get current gas price
python3 {{baseDir}}/scripts/alchemy.py get-gas-price

# Get latest block number
python3 {{baseDir}}/scripts/alchemy.py get-block-number

# Get event logs
python3 {{baseDir}}/scripts/alchemy.py get-logs --address <value> --from-block "0x0" --to-block "latest" --topics <value>

# Get asset transfers for address
python3 {{baseDir}}/scripts/alchemy.py get-asset-transfers --address <value> --category "external,erc20"

# Get NFT floor price
python3 {{baseDir}}/scripts/alchemy.py get-floor-price --contract <value>
```

## Output Format

All commands output JSON by default.

## Script Reference

| Script | Description |
|--------|-------------|
| `{baseDir}/scripts/alchemy.py` | Main CLI — all commands in one tool |

## Credits
Built by [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) | [agxntsix.ai](https://www.agxntsix.ai)
[YouTube](https://youtube.com/@aiwithabidi) | [GitHub](https://github.com/aiwithabidi)
Part of the **AgxntSix Skill Suite** for OpenClaw agents.

📅 **Need help setting up OpenClaw for your business?** [Book a free consultation](https://cal.com/agxntsix/abidi-openclaw)
