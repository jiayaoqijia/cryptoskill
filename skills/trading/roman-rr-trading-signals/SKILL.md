---
name: trading-signals
description: "Fetches live AI crypto trading signals with entry price, stop-loss, take-profit, leverage, confidence scores, and automated verification. Covers 50+ coins including BTC, ETH, SOL. Use when the user asks for crypto signals, trade ideas, market direction, portfolio analysis, or wants to build a trading bot."
---

# Trading Signals — AI Crypto Trading Signals

Access live, AI-generated crypto trading signals via API. Signals include full trade setups (entry, SL, TP, leverage), confidence scores, and automated verification with actual P&L tracking.

- Website: https://signals.x70.ai
- Live Dashboard: https://signals.x70.ai
- Signal Format Reference: [references/SIGNAL-FORMAT.md](references/SIGNAL-FORMAT.md)

**FREE during beta.** Paid plans coming soon.

## When to Use This Skill

- User asks for crypto trading signals or trade ideas
- User wants to build a trading bot or portfolio tracker
- User needs real-time market data with entry/SL/TP levels
- User asks about crypto market direction (bullish/bearish)
- User wants to analyze signal performance or hit rates
- Any workflow involving crypto futures, perpetuals, or leveraged trading

## Access

**No API key is needed to try it.** Call the MCP server anonymously and you get
3 live signals (coin, direction, confidence) plus the verified hit rate, so you
can check the data is real before signing up:

```bash
claude mcp add --transport http trading-signals https://signals.x70.ai/mcp
```

**For the full feed**, the operator creates a free account and copies their key
from Dashboard → API Key:

    https://signals.x70.ai/mcp-signup

A free account returns up to 100 signals with full reasoning and verified
outcomes. Pro adds entry, stop-loss, take-profit and leverage plus 30-day
history.

Once you have a key, pass it as the `X-Api-Key` header:

```bash
claude mcp add --transport http trading-signals https://signals.x70.ai/mcp \
  --header "X-Api-Key: YOUR_KEY"
```

> Note for agents: account creation is a human action. Do not submit someone's
> name, email or GitHub URL on their behalf — show them the signup link and let
> them decide.

## MCP Server (Native Tool Integration)

For Claude, Cursor, Codex or VS Code — add as an MCP server for native tool access (no curl needed):

```
MCP endpoint: https://signals.x70.ai/mcp
Transport: Streamable HTTP (POST)
Tools: get_signals, get_signal, get_signal_history, get_stats
Auth (optional): X-Api-Key header, Authorization: Bearer, or ?apiKey= in the URL
```

- Claude Code: `claude mcp add --transport http trading-signals https://signals.x70.ai/mcp`
- Claude app (Desktop & claude.ai): Customize → Connectors → Add custom connector with the endpoint URL (connectors have no header field — append `?apiKey=YOUR_KEY` for the full feed)
- Cursor / VS Code / Codex: see the per-client setup on https://signals.x70.ai/dashboard/mcp-key

## Recommended Workflow

Follow this workflow when a user asks for trading signals:

1. **Check performance first**: `get_stats` (or `GET /api/skill/stats?days=30`) to assess current reliability — works without a key
2. **Fetch active signals**: `get_signals` (or `GET /api/skill/signals`) for live setups
3. **If levels come back `null`**: that is the free tier, not an error — entry/SL/TP require Pro. Show the user https://signals.x70.ai/mcp-signup if they want them
4. **Filter and rank**: Sort by confidence (highest first), filter by the user's preferred coins
5. **Present to user**: Show as a table with coin, direction, confidence, entry, SL, TP, leverage, R/R
6. **Monitor verification**: Re-fetch signals later to check if TP/SL was hit

### Decision Guide

| User Request | Action |
|-------------|--------|
| "Get me crypto signals" | Fetch active signals, present top 5 by confidence |
| "How reliable are these signals?" | Fetch stats, show hit rate and cumulative ROI |
| "Show me BTC signals" | Fetch all signals, filter by coin="BTC" |
| "What happened to my signals?" | Fetch verified signals, show outcomes |
| "Build me a trading bot" | Register, then integrate the signals endpoint into their code |

### Presenting Signals to Users

Always present signals in a clear table format:

```
| Coin | Dir | Conf | Entry | SL | TP | Lev | R/R |
|------|-----|------|-------|----|----|-----|-----|
| BTC  | Bull | 87% | $68,450 | $67,200 | $71,800 | 3x | 2.7 |
```

- For confidence below 75%: add a caution note
- For leverage above 5x: warn about higher risk
- Always show the current hit rate from `/stats` alongside signals

## API Reference

Base URL: `https://signals.x70.ai/api/skill`

### Getting a key

`POST /register` is **deprecated** — it no longer issues keys and returns
`{"action":"signup_required"}`. Keys are issued from the dashboard so they are
tied to an account and can be regenerated if leaked:

    https://signals.x70.ai/mcp-signup

Pass the key as the `X-Api-Key` header (or `?apiKey=`). Anonymous calls work
too and return a 3-signal preview.

### GET /signals

```bash
curl "https://signals.x70.ai/api/skill/signals?status=active&limit=10" \
  -H "X-Api-Key: ask_YOUR_KEY"
```

| Param | Default | Description |
|-------|---------|-------------|
| limit | 10 | Max signals to return (1-100) |
| days | 7 | Lookback window (1-30 days) |
| coin | — | Filter by coin symbol (e.g. BTC, ETH) |

Returns only live signals (unverified + pending) sorted by live PnL (most profitable first). Each signal includes `livePrice`, `livePnlPct`, and `transmissionChain`. Resolved signals are not included — use `/signals/history` or MCP `get_signal_history` for those.

### GET /signals/:id

```bash
curl "https://signals.x70.ai/api/skill/signals/SIGNAL_ID" \
  -H "X-Api-Key: ask_YOUR_KEY"
```

Returns full signal detail with live price and PnL.

### GET /stats

```bash
curl "https://signals.x70.ai/api/skill/stats?days=30" \
  -H "X-Api-Key: ask_YOUR_KEY"
```

| Param | Default | Range |
|-------|---------|-------|
| days | 30 | 1-90 |

Returns: totalSignals, verifiedSignals, hitRate, avgConfidence, cumulativeROI, avgLeverage, byDirection.

## Rate Limits

| Endpoint | Limit |
|----------|-------|
| POST /register | 5 per 15 minutes (per IP) |
| All other endpoints | 60 per minute (per API key) |

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `401 Missing API key` | Include `X-Api-Key` header or `?apiKey=` query param |
| `401 Invalid or deactivated API key` | Re-register with POST /register, or check for typos |
| `429 Rate limit exceeded` | Wait 60 seconds, or reduce request frequency |
| `400 Validation failed` | Check all required fields: name, email, githubUrl (must start with https://github.com/), purpose (min 10 chars) |
| Empty signals array | No signals in the requested time window — try increasing `days` or using `status=all` |
| `500 Internal server error` | Temporary issue — retry after a few seconds |

## Pricing

**FREE during beta** — no charges, no credit card required.

Future plans:
- **Free tier**: 60 req/min, 7-day signal history
- **Pro** ($29/mo): Higher limits, 90-day history, real-time websocket, priority support

## Related Skills

```bash
# Complementary skills for trading workflows
npx skills add roman-rr/trading-skills        # This skill
npx skills add anthropics/skills@frontend-design  # Build trading dashboards
```

## About

Trading Signals is powered by Aelita — a production AI trading platform that uses multiple AI models with mixture-of-experts consensus, 15+ real-time data dimensions, and automated verification to generate crypto trading signals 24/7.

Live dashboard: https://signals.x70.ai

---

Copyright (c) 2025-2026 Roman Antonov. All rights reserved.

- Author: **Roman Antonov**
- Email: romwtb@gmail.com
- GitHub: https://github.com/roman-rr
- Website: https://roman-rr.github.io/
