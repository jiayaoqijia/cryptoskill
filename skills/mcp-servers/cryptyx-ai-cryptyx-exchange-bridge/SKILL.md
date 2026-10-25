---
name: cryptyx-exchange-bridge
description: Use an exchange connection (Coinbase, Kraken, Binance, Hyperliquid) together with CRYPTYX - read which coins the user holds with the exchange's own tools, send only the symbols to CRYPTYX, and hand any order back to the exchange's approval flow. Use when the user asks CRYPTYX questions about "my holdings" or "my portfolio".
---

# Exchange bridge

Follow the [CRYPTYX router](../cryptyx/SKILL.md). This skill connects two tools the user has already approved: their exchange and CRYPTYX.

## Steps

1. **Read holdings on the exchange.** Use the exchange's read-only balance or portfolio tool. See the reference for the exchange below. Follow that exchange's own skill and approval rules. Reading balances does not authorise any trade.
2. **Extract symbols.** Keep the coin symbols with a non-zero balance. Drop stablecoins and fiat (USD, USDC, USDT, EUR and so on). Do not pass amounts.
3. **Ask CRYPTYX.** Scan the symbols with `get_heat_check`, then run THE STUDY (`get_coin_study`) on the coins that stand out. Follow [cryptyx-holdings](../cryptyx-holdings/SKILL.md) for the answer.
4. **Orders stay with the exchange.** If the user decides to place, change or cancel an order, use the exchange's own trading skill and approval flow. CRYPTYX evidence is not an approval.

## Privacy

Only coin symbols go to CRYPTYX: no balances, position sizes, portfolio IDs or account details. Tell the user this if they ask what is shared.

## Exchange references

Load only the one that matches the user's connected exchange.

- [Coinbase](references/coinbase.md)
- [Kraken](references/kraken.md)
- [Binance](references/binance.md)
- [Hyperliquid](references/hyperliquid.md)

Tool names change. Use the names and schemas the connected exchange actually exposes, and never guess a tool name.
