# Coinbase

Applies to the Coinbase remote MCP (`https://agents.coinbase.com/mcp`, Coinbase for Agents) and the plugins from [coinbase/agents](https://github.com/coinbase/agents). Follow Coinbase's own `coinbase` and `coinbase-portfolios` skills for setup and approvals.

| Step | Coinbase tool (core name; hosts may add a prefix) |
| --- | --- |
| Find the portfolio | `coinbase_portfolios_list` with `{}` |
| Read balances | `coinbase_balance` with the chosen `portfolio_id` |
| Place or change an order | Coinbase's `coinbase-trading` skill and its approval flow |

Notes:

- Omitting `portfolio_id` in `coinbase_balance` reads the default portfolio only. If the user has several portfolios, ask which one, or read each one they approve.
- Follow `cursor` pagination until the balance list is complete.
- Equity listings (e.g. `AAPL-USD`) are not crypto. Leave them out of the CRYPTYX request.
- Coinbase's own x402 research tool pays only for resources in its curated catalog. CRYPTYX is reached through its own connection, not through that tool.
