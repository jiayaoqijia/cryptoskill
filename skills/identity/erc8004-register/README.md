# ERC-8004 Registration Tool

CLI tool for registering and managing agents on the ERC-8004 Identity Registry.

## Quick Start

```bash
# Install dependencies
pip install web3 eth-account

# Set wallet (pick one)
export ERC8004_MNEMONIC="your twelve word mnemonic phrase here"
# OR
export ERC8004_PRIVATE_KEY="0x..."

# Register an agent
python scripts/register.py register --name "MyAgent" --description "AI assistant"

# View agent info
python scripts/register.py info 123

# Update metadata
python scripts/register.py update 123 --name "NewName" --image "https://example.com/avatar.png"

# Validate registration
python scripts/register.py validate 123
```

## Commands

| Command | Description |
|---------|-------------|
| `register` | Register a new agent (mints NFT + sets URI) |
| `update` | Update existing agent metadata |
| `info` | Display agent information |
| `validate` | Check registration for common issues |

## Registration Process

The `register` command performs two transactions:

1. **register()** - Mints the agent NFT and returns the agentId
2. **setAgentURI()** - Sets the full metadata including the agentId in the registrations array

This ensures the on-chain metadata correctly references itself.

## Supported Chains

- **Base** (default) - Cheapest gas fees
- **Ethereum** - Mainnet
- **Polygon** - Low fees
- **Monad** - Fast finality
- **BNB** - BSC

Use `--chain` flag to select: `--chain ethereum`

## Contract

Identity Registry: `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432`

Same address on all supported chains.

## Metadata Schema

Follows ERC-8004 registration-v1 specification:

```json
{
  "type": "https://eips.ethereum.org/EIPS/eip-8004#registration-v1",
  "name": "AgentName",
  "description": "What the agent does",
  "image": "https://example.com/image.jpg",
  "services": [
    {"name": "api", "endpoint": "https://api.example.com"}
  ],
  "x402Support": false,
  "active": true,
  "registrations": [
    {"agentId": 123, "agentRegistry": "eip155:8453:0x8004A169FB4a3325136EB29fA0ceB6D2e539a432"}
  ],
  "supportedTrust": ["reputation"]
}
```

## Validation Checks

The `validate` command checks for:

- Missing `type` field
- Local file paths as images (not accessible on-chain)
- Empty name or description
- Missing registrations array
- Unreachable image URLs

## Related Skills

- **erc8004-reputation** - Rate agents and check trust scores on the Reputation Registry

## License

MIT
