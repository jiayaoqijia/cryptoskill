# Kraken

Applies to Kraken's agent tooling (the Kraken CLI with its built-in MCP server; see [Kraken's MCP docs](https://docs.kraken.com/home/mcp)). Follow Kraken's own documentation for setup, API key permissions and approvals.

- **Read balances:** use the read-only balance tool or command the Kraken connection exposes. A query-only API key is enough.
- **Symbols:** Kraken uses some legacy asset codes (for example `XBT` for bitcoin, and `X`/`Z` prefixes on older codes). Convert to common tickers (`BTC`, `ETH`) before sending them to CRYPTYX. If unsure, call `check_coverage`.
- **Orders:** place, change or cancel only through Kraken's own tools and approval flow.

Use the tool names the Kraken connection actually exposes. Do not guess them.
