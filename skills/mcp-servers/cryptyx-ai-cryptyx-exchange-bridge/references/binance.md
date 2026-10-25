# Binance

Applies to Binance's agent skills and API connections. Follow Binance's own documentation for setup, API key permissions and approvals.

- **Read balances:** use the read-only account or balance tool the Binance connection exposes. A read-only API key is enough.
- **Symbols:** Binance balances list assets such as `BTC` and `ETH`. Trading pairs like `ETHUSDT` are not assets, so send only the base asset to CRYPTYX. Drop `LD`-prefixed savings assets, or map them to the underlying coin.
- **Orders:** place, change or cancel only through Binance's own tools and approval flow.

Use the tool names the Binance connection actually exposes. Do not guess them.
