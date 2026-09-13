---
name: app
description: >-
  Use when the user asks about interacting with the app's API — querying data,
  creating resources, checking status. This skill covers all MCP tools and
  REST endpoints exposed by the server.
version: 0.1.0
---

# App Plugin

This is the consolidated skill for interacting with your app's API. It covers all MCP tools and REST endpoints.

## Available Tools

<!-- Generated during implementation. Replace this section with your actual tools. -->

| Tool | Access | Description |
|------|--------|-------------|
| echo | free | Echo a message back (connectivity test) |

## Usage Pattern

1. Check if the MCP server is connected (`.mcp.json` config)
2. If connected, use MCP tools directly
3. If not connected, fall back to REST API calls
4. For auth-gated endpoints, include the API key
5. For x402-gated endpoints, follow the payment flow

## Payment Flow (x402)

For paid tools:
1. Call the tool WITHOUT a `payment` parameter
2. Server returns payment requirements (price, network, pay-to address)
3. Present the price to the user and ask for confirmation
4. If confirmed and agent has wallet: sign and submit payment
5. If no wallet: suggest using an API key or the REST endpoint directly

## Error Handling

If a tool call fails:
- Check the error code and message
- Present the `suggestion` field to the user
- If MCP is unavailable, fall back to REST
