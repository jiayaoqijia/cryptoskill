---
name: robinhood
description: Robinhood portfolio advisor — read-only access to positions, quotes, fundamentals, news, earnings, analyst ratings, dividends, and options via MCP. Includes cache-first strategy, entity page workflows, and optional Obsidian vault integration.
version: 1.0.0
author: Uzair Ansar
license: MIT
metadata:
  hermes:
    tags: [trading, portfolio, robinhood, options, investing, mcp, finance]
    related_skills: [portfolio-obsidian-bridge, llm-wiki, obsidian]
    requires_mcp: true
    mcp_servers:
      robinhood:
        command: uvx
        args:
          - robinhood-mcp
        env:
          ROBINHOOD_USERNAME: "${ROBINHOOD_USERNAME}"
          ROBINHOOD_PASSWORD: "${ROBINHOOD_PASSWORD}"
          ROBINHOOD_TOTP_SECRET: "${ROBINHOOD_TOTP_SECRET}"
        timeout: 60
        connect_timeout: 30
---

# Robinhood Portfolio Advisor

Read-only access to your Robinhood portfolio via the `robinhood-mcp` server. Provides live data for positions, quotes, fundamentals, news, earnings, analyst ratings, dividends, and options.

## Prerequisites

### 1. Robinhood Account

You need a Robinhood account (free at [robinhood.com](https://robinhood.com)).

### 2. MCP Server Installation

The `robinhood-mcp` package provides the MCP server. Install it with one of:

```bash
# Recommended — runs via uvx (no global install needed, auto-managed)
# Just add to your agent config and it works. uvx installs it on first run.

# Alternative — global pip install
pip install robinhood-mcp
```

> **Note:** `uvx` is provided by the [uv](https://docs.astral.sh/uv/) Python package manager. Install it first: `curl -LsSf https://astral.sh/uv/install.sh | sh`

### 3. Environment Variables

Set these in your agent's `.env` file or shell profile:

| Variable | Required | Description |
|----------|----------|-------------|
| `ROBINHOOD_USERNAME` | Yes | Your Robinhood email |
| `ROBINHOOD_PASSWORD` | Yes | Your Robinhood password |
| `ROBINHOOD_TOTP_SECRET` | Only if using authenticator app | The TOTP secret from your authenticator setup. **Not needed** if using SMS verification. |

### 4. Agent Configuration

See the `templates/` directory for copy-paste config snippets for your agent. Quick reference:

**Hermes Agent** (`~/.hermes/config.yaml`):
```yaml
mcp_servers:
  robinhood:
    command: uvx
    args:
      - robinhood-mcp
    env:
      ROBINHOOD_USERNAME: "${ROBINHOOD_USERNAME}"
      ROBINHOOD_PASSWORD: "${ROBINHOOD_PASSWORD}"
      # ROBINHOOD_TOTP_SECRET: "${ROBINHOOD_TOTP_SECRET}"  # Uncomment for authenticator app
    timeout: 60
    connect_timeout: 30
```

**Other agents** — see `templates/` directory for Claude Desktop, Claude Code, Codex, OpenCode, Cline, and Windsurf.

After adding config, restart your agent. Verify with: `hermes mcp test robinhood` (Hermes) or check your agent's MCP status.

## Available MCP Tools

These tools are registered as `mcp_robinhood_*` in Hermes Agent (prefix varies by agent):

| Tool | Description |
|------|-------------|
| `robinhood_get_portfolio` | Portfolio value, equity, buying power, day change |
| `robinhood_get_positions` | All holdings with cost basis, current value, P&L |
| `robinhood_get_position` | Single holding by ticker (faster for one symbol) |
| `robinhood_get_watchlist` | Stocks in your watchlists |
| `robinhood_get_quote` | Real-time price, bid/ask, volume |
| `robinhood_get_fundamentals` | P/E ratio, market cap, dividend yield, 52-week range |
| `robinhood_get_historicals` | OHLCV price history (5min, 10min, hour, day, week) |
| `robinhood_get_news` | Recent news articles for a symbol |
| `robinhood_get_earnings` | Earnings dates, EPS estimates, actuals |
| `robinhood_get_ratings` | Analyst buy/hold/sell ratings |
| `robinhood_get_dividends` | Dividend payment history |
| `robinhood_get_options_positions` | Current options positions |
| `robinhood_search_symbols` | Search stocks by name or ticker |

## Local Cache

Portfolio data is cached locally at `~/.hermes/data/robinhood/portfolio_cache.json` (Hermes) or `~/.robinhood-mcp/cache.json` (other agents).

### Cache-First Strategy

**Always check the cache first.** Only call MCP tools when:
1. Cache is older than 15 minutes AND the user needs live data
2. User explicitly asks for a refresh ("refresh my portfolio", "get latest prices")
3. User asks about a specific ticker not in cache
4. User asks for rapidly changing data (news, real-time quotes)

### Updating the Cache

```bash
# Hermes Agent users
python3 scripts/refresh_cache.py

# With custom paths
python3 scripts/refresh_cache.py --cache-dir ~/my-data --vault-path ~/my-vault

# JSON output only (no Obsidian)
python3 scripts/refresh_cache.py --json-only

# Force refresh even if cache is fresh
python3 scripts/refresh_cache.py --force
```

The agent can also update the cache inline during any portfolio query by calling MCP tools and writing results to the cache file.

## Portfolio Query Workflow

When the user asks about their portfolio:

1. **Read cache** for context (portfolio value, positions, allocations)
2. **If data is stale** (>15 min) or user wants live data, call MCP tools
3. **Update cache** after any MCP fetch
4. **Answer with context** of their actual holdings — not generic advice
5. Reference their **cost basis, unrealized P&L, and allocation** when relevant
6. For options questions, cross-reference with the user's strategy if known

When the user asks about a **specific ticker**:

1. Check if `wiki/entities/<ticker>.md` exists (if using Obsidian)
2. Read it for existing thesis and research history
3. Fetch live data (quote, fundamentals, news, ratings) via MCP
4. Respond with synthesis of wiki knowledge + live data
5. **Append a Research Notes entry** to the entity page (if using Obsidian)
6. If ticker not in portfolio, track it in a research queue

## When to Use MCP vs Cache

| Scenario | Use |
|----------|-----|
| "What's my portfolio worth?" | Cache (if fresh enough) |
| "How's my NVDA doing?" | Cache first, MCP if stale or ticker missing |
| "Give me a full portfolio update" | MCP (always get live data) |
| "Any news on TSLA?" | MCP (news changes constantly) |
| "What are analyst ratings for AAPL?" | MCP (research data is always live) |
| "Show me my options positions" | Cache first, MCP if stale |
| "What dividends have I received?" | Cache first |
| "Refresh my data" | MCP then update cache |

## Research-to-Entity Workflow (Optional — Requires Obsidian)

**Problem:** Research queries about stocks get lost in chat sessions.
**Solution:** Every holding or researched ticker gets a persistent entity page. Research is appended, not forgotten.

### Entity Page Structure

Each ticker gets a page at `wiki/entities/<ticker>.md`:

```markdown
---
title: Company Name
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity
tags: [ticker, sector, ...]
---

# Company Name (TICKER)

Brief overview...

## Key Facts
...

## Investment Thesis
...

## Position History
> Updated automatically. Do not edit manually.

### Current Position
| Metric | Value |
|--------|-------|
| Quantity | 50 |
| Avg Cost | $40.69 |
| Current Price | $45.20 |
| Total Return | +10.8% |

### Position Updates
- **[2026-04-24]** 50 shares @ $40.69 avg

## Research Notes
> Agent appends dated entries after each research query.

### [2026-04-24] Should I add to HIMS at $30?
Key points: [bullet summary]
Decision: [if user stated one]
```

### When to Update Entity Pages

1. **On every portfolio pull** — Update position data for each holding
2. **After every research query** — Append a dated Research Notes entry
3. **When creating a new entity** — Fetch fundamentals, create page, add to wiki index

### Research Queue

`wiki/concepts/research-queue.md` tracks tickers being evaluated but not yet purchased:

| Ticker | Source | Thesis (1-line) | Status | Added | Notes |
|--------|--------|-----------------|--------|-------|-------|
| ABC | YouTube video | EV battery play | researching | 2026-04-24 | Mentioned by MKBHD |

**Status values:** `researching` → `ready to buy` → _(removed when purchased)_ or `passed`

## Obsidian Vault Integration (Optional)

Every portfolio pull can write two files to your Obsidian vault:

| File | Behavior |
|------|----------|
| `_ephemeral/portfolio/snapshots/YYYY-MM-DD-HHMM.md` | **Immutable** — one per pull, full data |
| `_ephemeral/portfolio/latest.md` | **Overwritten** — current state + deltas vs previous |

### Frontmatter for Dataview

Both files include YAML frontmatter:

```yaml
---
snapshot_time: 2026-04-24T18:58:02Z
date: 2026-04-24
time: 14:58
total_equity: 42700.94
day_change: -834.73
day_change_pct: -1.92
positions_count: 16
options_count: 1
dividends_ytd: 1.68
type: portfolio-snapshot
---
```

This enables Dataview queries like:
```dataview
TABLE date, total_equity, day_change_pct
FROM "_ephemeral/portfolio/snapshots"
SORT snapshot_time DESC
```

### Delta Computation

The `latest.md` compares against the most recent snapshot and highlights:
- 🆕 **New positions** (bought since last pull)
- ❌ **Closed positions** (sold since last pull)
- 📊 **Significant moves** (>5% price change OR >1% allocation shift)
- **Equity change** since last snapshot

To enable Obsidian integration, set the `--vault-path` argument when running `refresh_cache.py`, or set the `ROBINHOOD_VAULT_PATH` environment variable.

## Advisory Guidelines

1. Always answer with context of the user's actual holdings — not generic advice
2. Reference cost basis, unrealized P&L, and allocation percentages when relevant
3. For options questions, understand the user's strategy (e.g., 0DTE breakout)
4. When recommending actions, show the math (current allocation, risk/reward)
5. Never suggest trades unless the user explicitly asks for recommendations
6. Flag concentration risk when a single position exceeds 20% of portfolio
7. Cross-reference news with fundamentals — don't react to headlines alone

## Security & Privacy

- **No credentials stored in the skill** — auth is via environment variables in MCP config
- **Read-only access** — the MCP server cannot execute trades or modify account settings
- **Local processing** — credentials are used locally to authenticate; session tokens cached in `~/.tokens/robinhood.pickle`
- **Cache is local only** — `~/.hermes/data/robinhood/` is never transmitted
- **Obsidian vault** — snapshots are written to the user's local vault only

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Not logged in" | Verify `ROBINHOOD_USERNAME` and `ROBINHOOD_PASSWORD` env vars are set correctly |
| "Non-base32 digit found" | `ROBINHOOD_TOTP_SECRET` contains invalid characters — only A-Z and digits 2-7. Remove this var if using SMS verification |
| Rate limiting (429 errors) | `robin_stocks` has no built-in rate limiting. Pause activity for several minutes and retry |
| MCP server won't start | Ensure `uvx` is installed (`pip install uv` or `curl -LsSf https://astral.sh/uv/install.sh \| sh`). Run `uvx robinhood-mcp` manually to test |
| Cache script fails | Ensure `robin_stocks` and `pyotp` are installed: `pip install robin_stocks pyotp` |
| Stale quotes | Robinhood quotes are point-in-time, not live streaming. Refresh via MCP for latest data |

## Related

- [robinhood-mcp](https://github.com/verygoodplugins/robinhood-mcp) — The underlying MCP server
- [robin_stocks](https://github.com/robinhood-unofficial/robin_stocks) — Unofficial Robinhood API wrapper
- `portfolio-obsidian-bridge` — Generic Obsidian sync for any brokerage
- `llm-wiki` — Wiki architecture for persistent research
- `obsidian` — Obsidian vault operations