# SnapTrade — Getting Started (docs.snaptrade.com/docs/getting-started)

Source: https://docs.snaptrade.com/docs/getting-started

> Imported for reference. Keep this file as a lightweight summary of the official guide.

## Topics covered
- API keys (clientId / consumerKey)
- Registering SnapTrade users (userId / userSecret)
- Creating connections via Connection Portal
- Accounts & positions
- Placing trades (checked trade flow)
- Links to webhooks + connection portal integration

## Key takeaways (summary)
- Use **clientId + consumerKey** to sign API requests.
- A **SnapTrade user** is identified by userId + userSecret.
- Generate a **Connection Portal** link via `Authentication_loginSnapTradeUser`.
- To get positions, use `AccountInformation_getUserAccountPositions`.
- Trades can be placed via checked flow (`getOrderImpact` → `placeOrder`) or direct force order.

Refer to the official doc for full details.
