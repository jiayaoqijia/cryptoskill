---
name: robinhood-trading-mcp
description: "Connect to Robinhood's official Trading MCP for portfolio research and order placement in a dedicated Agentic account. Supports eligible equities, options and crypto access through Robinhood authentication."
version: 1.0.0
author: Robinhood
tags: [robinhood, mcp, portfolio, stocks, options, crypto, official]
user-invocable: true
can-move-funds: true
---

# Robinhood Trading MCP

CryptoSkill maintains this connection guide for Robinhood's official hosted service.
The service and account permissions are controlled by Robinhood.

## Connect

Use Streamable HTTP at `https://agent.robinhood.com/mcp/trading`.

For Claude Code:

```sh
claude mcp add robinhood-trading-mcp --transport http https://agent.robinhood.com/mcp/trading
```

Open the client's MCP authentication flow on desktop and finish Robinhood's
onboarding. Authenticate through Robinhood; do not put account credentials in
this skill or share access tokens in chat.

## Scope

The connection can read account, portfolio and transaction information.
Order placement is limited to the dedicated Agentic account. Crypto access
requires the corresponding Crypto account, accepted agreements and eligibility.
The trading connection does not support crypto transfers, staking or lending.

## Workflow

Start with a read-only account or portfolio request. Before any request to place
an order, obtain the user's authorization for the asset, side, size, order type
and account. Check the returned order status before claiming execution.
Never interpret a connection, preview or pending order as a completed trade.

## Troubleshooting

For authentication failures, reconnect through the client's MCP settings. Check
account eligibility and permissions for rejected operations. Use the current
[Robinhood support guide](https://robinhood.com/us/en/support/articles/agentic-trading-overview/)
for onboarding and supported features.
