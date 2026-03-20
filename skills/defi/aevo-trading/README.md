# AEVO Trading Skill

AI trading assistant skill for [AEVO](https://app.aevo.xyz), a decentralized derivatives exchange. Connects any MCP-compatible client to AEVO's 45 tools for market data, portfolio management, order execution, risk analysis, and options strategies.

## Quick Start

### Option 1: Claude Desktop / Claude Code (Direct MCP)

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "aevo": {
      "command": "uvx",
      "args": ["mcp-aevo-server"],
      "env": {
        "AEVO_API_KEY": "your-api-key",
        "AEVO_API_SECRET": "your-api-secret",
        "AEVO_WALLET_ADDRESS": "0x...",
        "AEVO_SIGNING_KEY_PRIVATE_KEY": "0x..."
      }
    }
  }
}
```

Or connect to AEVO's hosted MCP endpoint (no local server needed):

```json
{
  "mcpServers": {
    "aevo": {
      "url": "https://mcp.aevo.xyz/mcp",
      "headers": {
        "AEVO-KEY": "your-api-key",
        "AEVO-SECRET": "your-api-secret"
      }
    }
  }
}
```

### Option 2: OpenClaw

```bash
clawhub install aevo
```

Then in your OpenClaw config, add your AEVO credentials as environment variables.

### Option 3: Any MCP Client (Cursor, Windsurf, etc.)

Point your MCP client to AEVO's hosted endpoint:

- **Mainnet**: `https://mcp.aevo.xyz/mcp`
- **Testnet**: `https://mcp-testnet.aevo.xyz/mcp`

Authenticate via `AEVO-KEY` and `AEVO-SECRET` headers, or call `aevo_authenticate` after connecting.

## Getting Your Credentials

1. Go to [app.aevo.xyz/settings](https://app.aevo.xyz/settings)
2. Create an API key (gives you `api_key` + `api_secret`)
3. For trading: you also need your `wallet_address` and `signing_key_private_key`

### Credential Tiers

| Tier | Credentials | Access |
|------|------------|--------|
| Read-only | `api_key` + `api_secret` | Account data, positions, history |
| Trading | + `wallet_address` + `signing_key_private_key` | Orders, cancellations, strategies |

## What You Can Do

- **Market Analysis**: Real-time prices, funding rates, volatility snapshots, market regime classification
- **Portfolio Management**: Positions, risk metrics, Greeks, margin monitoring
- **Order Execution**: Limit orders, bracket orders (entry + SL + TP), batch operations
- **Options Strategies**: Straddles, strangles, spreads, iron condors, butterflies with live pricing
- **Risk Management**: Pre-trade validation, portfolio risk scoring, liquidation distance monitoring

## File Structure

```
SKILL.md              # Core skill definition (what the LLM reads)
README.md             # This file
references/
  tools.md            # All 45 tools with parameters and examples
  instruments.md      # Instrument naming conventions
  risk-rules.md       # Risk guardrails and safety rules
  workflows.md        # Step-by-step workflow recipes
  options.md          # Options strategy reference
examples/
  analyze.md          # Market analysis conversation
  trade.md            # Bracket trade conversation
  hedge.md            # Portfolio hedge conversation
```

## Testnet

For testing without real funds, use AEVO testnet:

- App: [testnet.aevo.xyz](https://testnet.aevo.xyz)
- API: `https://api-testnet.aevo.xyz`
- MCP: `https://mcp-testnet.aevo.xyz/mcp`

## Links

- [AEVO Exchange](https://aevo.xyz)
- [AEVO API Docs](https://docs.aevo.xyz)
- [MCP Server Package](https://pypi.org/project/mcp-aevo-server/)
