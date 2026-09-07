---
name: dydx-gateway
description: "Use when the user asks about anything dYdX — markets, prices, funding, OI, volumes, perps — or mentions a perp trader address to vet (equity, PnL curve, day-winrate, maxDD, farmer flag), funding/OI anomalies, liquidation cascades, leaderboards, or wants TA and ATR-based stop plans. Provides dYdX v4 perps analytics via a local read-only MCP gateway: market data, funding heatmap, verified trader PnL, leaderboards, OI and liquidation-cascade anomaly detection."
when_to_use: "Use for any dYdX questions — markets, prices, funding, OI, volumes; anomalies (OI spikes without price movement, liquidation cascades, extreme funding, trader equity jumps); trader analysis by address (equity, PnL curve, day-winrate, maxDD, farmer flag) before copy-trading; leaderboard and onchain trader screening; TA and ATR-based stop plans. Trigger words: dYdX, perps, funding, OI anomaly, trader PnL, vet this trader, liquidation cascade."
metadata:
  version: "0.3.0"
  agent:
    requires:
      bins: ["python3"]
---

# dYdX Agent Gateway (local MCP server)

The gateway is deployed on this host, endpoint **http://127.0.0.1:8901/mcp**
(streamable HTTP, systemd unit `dydx-mcp.service`; check with
`systemctl is-active dydx-mcp`). The code lives at the repository root
of https://github.com/alekskram/dydx-agent-gateway
(the skill's source is `.agents/skills/dydx-gateway/`; after edits,
copy it to `~/.zcode/skills/dydx-gateway/`). If the gateway is not
running, start it per the repo README Install section
(`uvx --from git+https://github.com/alekskram/dydx-agent-gateway
dydx-agent-gateway --http --port 8901`).

Background data: the block scanner (`dydx-scanner`, the address registry
keeps growing), detectors every 5 min (`dydx-detectors.timer`),
leaderboard every 6 h (`dydx-leaderboard.timer`), watchdog report on the
1st of each month.

## MCP tools (22)

Data: `list_markets`, `market_detail`, `candles`, `recent_trades`, `height`
· Analytics: `funding_heatmap(min_oi_usd)`, `historical_funding(limit≤500)`,
`market_ta`, `suggest_stops`, `trader_profile`,
`trader_pnl_stats(limit≤5000)`, `fills_review`, `raw_fills(limit≤200)`,
`cvd(trades_limit)`, `correlation(ticker_a, ticker_b)`
· Discovery: `market_digest` (one-call briefing — start here),
`leaderboard`, `discover_traders`, `list_traders`, `registry_stats`,
`latest_events`, `usage_stats`

## Quick path without an MCP client

```bash
cd <repo root> && python -c "
import sys; sys.path.insert(0,'.')
from dydx_mcp import server as s
import json; print(json.dumps(s.market_digest(), indent=1, default=str)[:800])"
```

Full-blown connections (stdio / Claude Desktop, Codex, Cursor configs):
`examples/` in the repo.

## Important data caveats

Read `references/data-gotchas.md` (5 documented indexer-API gotchas:
candle ordering, netTransfers, priceChange24H, subticksPerTick, no
liquidation feed). Rule of thumb: funding without an OI ≥ $100k filter
is noise.

## Where to look next

- Reports: `reports/` (monthly data-quality watchdog, digests)
