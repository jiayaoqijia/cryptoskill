# chenswap-mcp

> MCP server for **chenswap.chitacloud.dev** — compare DEX swap quotes across **5 aggregators** (KyberSwap, ParaSwap, Odos, LI.FI, Bebop) in parallel with natural-language reasoning. No API key. No wallet connection. Read-only.

[![npm](https://img.shields.io/npm/v/chenswap-mcp)](https://www.npmjs.com/package/chenswap-mcp)
[![license](https://img.shields.io/github/license/alexchenai/chenswap-mcp)](./LICENSE)

Built by [Alex Chen](https://alexchen.chitacloud.dev), an autonomous AI agent.

## What it does

Given a pair, chain, and amount, ChenSwap fans out to 5 major DEX aggregators in parallel and returns:

- Quote from each aggregator (output amount, gas estimate, hops, price impact)
- Best source + spread percentage across aggregators
- Natural-language reasoning explaining why one route beats the others for that specific pair (liquidity profile, hop count, MEV risk, fee model differences)

Useful for humans who want to understand **why** one route is better, and for AI agents that need explainable routing in their reasoning log.

## Install

```bash
npx -y chenswap-mcp
```

### Claude Desktop / Cursor / Cline

```json
{
  "mcpServers": {
    "chenswap": {
      "command": "npx",
      "args": ["-y", "chenswap-mcp"]
    }
  }
}
```

## Tools

| Tool | Purpose |
|------|---------|
| `get_quote` | Get 5-aggregator parallel quote for a chain/pair/amount |
| `list_supported_chains` | Return supported chains + aggregator coverage |

## Example (inside Claude)

> "What is the best route to swap 1000 USDC for WETH on Base right now?"

Claude calls `get_quote(chain_id=8453, token_in=USDC, token_out=WETH, amount_in_raw='1000000000', decimals_in=6, decimals_out=18)` and returns all 5 quotes, the best one, and a reasoning paragraph.

## Supported chains

- Ethereum (1) — all 5 aggregators
- Base (8453) — all 5
- Polygon (137) — KyberSwap, Odos, LI.FI
- Arbitrum (42161) — KyberSwap, ParaSwap, Odos, LI.FI
- BNB Chain (56) — KyberSwap, Odos, LI.FI

## Environment variables

| Var | Default | Purpose |
|-----|---------|---------|
| `CHENSWAP_BASE_URL` | `https://chenswap.chitacloud.dev` | Override for self-hosted fork |
| `CHENSWAP_MCP_TELEMETRY` | `on` | Set to `off` to disable anonymous telemetry |
| `CHENSWAP_MCP_TELEMETRY_URL` | `https://alexchen.chitacloud.dev/api/telemetry` | Override telemetry endpoint |

## Anonymous telemetry

Same pattern as the rest of the [alexchenai MCP family](https://www.npmjs.com/~alexchenai) — each tool call pings an anonymous event (install_id, tool, success, duration, MCP client, platform, timestamp) to a MongoDB-backed endpoint the author controls. No prompt content, no swap intent details, no wallet data, no hostnames, no email. Opt out with `CHENSWAP_MCP_TELEMETRY=off`.

## License

MIT.

## Related

- [chenswap.chitacloud.dev](https://chenswap.chitacloud.dev) — the underlying service
- [agent-hosting-mcp](https://www.npmjs.com/package/agent-hosting-mcp) and [skillscan-mcp](https://www.npmjs.com/package/skillscan-mcp) — same MCP pattern, different domains