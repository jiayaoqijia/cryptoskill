# TRDEFI Liquidity — MCP server

[![Listed on mcpservers.org](https://mcpservers.org/badge.svg)](https://mcpservers.org/servers/trdefi/mcp-server)
[![M8ven Score](https://m8ven.ai/badge/mcp/trdefi-mcp-server-wq7ly5?v=ae8d4ca3fb29c4fa076ae4d31b3bd3ee)](https://m8ven.ai/mcp/trdefi-mcp-server-wq7ly5)
[![Glama score](https://glama.ai/mcp/connectors/io.github.TRDEFI/liquidity/badges/score.svg)](https://glama.ai/mcp/connectors/io.github.TRDEFI/liquidity)
[![Smithery](https://img.shields.io/badge/Smithery-listed-blue)](https://smithery.ai/server/@trdefi/liquidity)

A **remote, read-only** [Model Context Protocol](https://modelcontextprotocol.io) server for the live
TRDEFI non-custodial stablecoin liquidity catalogue.

**Endpoint:** `https://yield.trdefi.com/mcp` · **Transport:** Streamable HTTP · **Credential:** none

Add it to any MCP-capable client and the six tools below appear. There is nothing to install, no key
to request, and nothing it can do that moves a single token — every tool is a read.

This repository holds only the registry manifest (`server.json`). The server itself runs on the same
host as the public API it reads.

## Tools

| Tool | Answers |
|---|---|
| `trdefi_stats` | How much liquidity is open, across how many networks, and how much has settled over 1, 7 and 30 days |
| `trdefi_chains` | Which networks are live, their engine addresses, and the tokens a position can be built from |
| `trdefi_positions` | The open positions — filter by network and by pair |
| `trdefi_position_detail` | One position, by its strategy hash |
| `trdefi_quote` | A swap simulated on-chain against one position, at the current block |
| `trdefi_badge` | A shields.io payload, so a README can show live figures |

## What an agent can do with it

* Understand the liquidity landscape before proposing anything: which networks, which pairs, how deep
* Find a specific position and inspect it
* Price a swap, or learn why one cannot be priced — a maker may gate a position on the caller holding
  an access licence token, and those answer with that reason rather than a number

## What it deliberately does not do

**Creating a position and swapping are absent.** Both return *unsigned* transactions and need a
signing flow that has not been designed. Shipping a tool an agent cannot finish would only teach it
that we are broken.

The underlying API is **prepare-only** in any case: it never signs, never broadcasts and never holds a
key. Funds stay in the owner's wallet behind a bounded, revocable allowance.

## Connecting

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

## Links

* API reference — https://yield.trdefi.com/docs/api
* OpenAPI 3.1 — https://yield.trdefi.com/openapi.json
* Agent index — https://yield.trdefi.com/llms.txt
* Live statistics — https://yield.trdefi.com/stats.html

## Listings

* Official MCP Registry — `io.github.TRDEFI/liquidity`
* Glama — https://glama.ai/mcp/connectors/io.github.TRDEFI/liquidity
* Smithery — https://smithery.ai/server/@trdefi/liquidity
* mcpservers.org — https://mcpservers.org/servers/trdefi/mcp-server
* M8ven — https://m8ven.ai/mcp/trdefi-mcp-server-wq7ly5
* Coinbase x402 Bazaar — discoverable as a paid x402 service (the two prepare endpoints answer `402`)

## Registry

Published to the official MCP Registry as `io.github.TRDEFI/liquidity`.

## License

All rights reserved.
