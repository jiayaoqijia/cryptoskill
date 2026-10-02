# Install: TRDEFI Liquidity MCP server

A **remote, read-only** MCP server. Nothing to install, no build step, no API key. Connecting is one
JSON block.

- **Endpoint:** `https://yield.trdefi.com/mcp`
- **Transport:** Streamable HTTP (answers `application/json`)
- **Credential:** none
- **Tools:** six, all read-only (`trdefi_stats`, `trdefi_chains`, `trdefi_positions`,
  `trdefi_position_detail`, `trdefi_quote`, `trdefi_badge`)

## Add it to an MCP client

```json
{
  "mcpServers": {
    "trdefi": {
      "type": "streamable-http",
      "url": "https://yield.trdefi.com/mcp"
    }
  }
}
```

## Verify it is live

```bash
curl -s https://yield.trdefi.com/mcp \
  -H 'content-type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

A healthy response lists six tools. No key, no OAuth, no account.

## Notes for the installing agent

- Every tool is a **read**: the server never signs, never broadcasts and never holds a key.
- Start with `trdefi_stats` to confirm the venue is alive, then `trdefi_chains` for the live networks.
- `trdefi_quote` may answer with a reason instead of a price — a maker can gate a position on the
  caller holding an access licence token. That is the maker's strategy, not a failure; try another
  position.
- Two paid HTTPS prepare endpoints (`POST /v1/positions`, `POST /v1/swaps`) exist outside the MCP
  surface and answer HTTP 402 at $0.02 USDC on Base. They are not part of this MCP server.
