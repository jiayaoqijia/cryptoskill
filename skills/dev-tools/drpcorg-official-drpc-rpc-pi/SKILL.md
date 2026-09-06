---
name: drpc-rpc-pi
description: Pi Agent-specific DRPC setup flow. Use alongside drpc-rpc when the user asks for blockchain data, DRPC setup, x402 API-key acquisition, Coinbase Payments MCP, pi-mcp-adapter, or when DRPC MCP is not configured in Pi.
---

# DRPC RPC — Pi Agent Setup Overlay

This skill is Pi Agent-specific. Generic DRPC RPC behavior lives in `skills/drpc-rpc/`.

## Scope

Use this overlay only in Pi Agent, when this repository is installed as a Pi package with its extension loaded.

The Pi extension provides:

- `drpc_setup` — agent-callable tool:
  - without `apiKey`: installs/configures Coinbase Payments MCP for secure x402 bootstrap
  - with `apiKey`: configures DRPC MCP in `~/.pi/agent/mcp.json`
- `drpc_coinbase_wallet_setup` — agent-callable tool to install/configure Coinbase Payments MCP
- `/drpc-setup` — manual DRPC API-key setup command
- `/drpc-coinbase-wallet-setup` — manual Coinbase Payments MCP setup command

## Pi Flow When DRPC MCP Is Missing

1. Check the MCP server list.
2. If DRPC MCP is unavailable but `drpc_setup` exists, call `drpc_setup` with no `apiKey`.
   - The Pi extension installs the Coinbase Payments MCP bundle if missing.
   - It writes/updates `~/.pi/agent/mcp.json` for `payments-mcp`.
3. Re-check the MCP server list.
4. If `payments-mcp` is still not visible, tell the user that the Pi/MCP session must reload or restart to pick up the newly written MCP server.
5. Once `payments-mcp` is visible, use it to acquire a DRPC API key via x402.
6. Call `drpc_setup` again with the acquired DRPC API key.
7. Re-check DRPC MCP. If it is still unavailable in the current session, execute the current request using the generic direct HTTP fallback from `skills/drpc-rpc/direct-http.md`.

Do not ask the user for private keys in Pi. Prefer Coinbase Agentic Wallet / Payments MCP for x402 so wallet custody stays outside Pi.
