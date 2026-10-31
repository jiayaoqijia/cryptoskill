---
name: trading-signals
description: "Fetches live AI crypto trading signals with entry price, stop-loss, take-profit, leverage, confidence scores, and automated verification. Covers 50+ coins including BTC, ETH, SOL. Use when the user asks for crypto signals, trade ideas, market direction, portfolio analysis, or wants to build a trading bot."
---

# Trading Signals — AI Crypto Trading Signals

Access live, AI-generated crypto trading signals via API. Signals include full trade setups (entry, SL, TP, leverage), confidence scores, and automated verification with actual P&L tracking.

- Website: https://signals.x70.ai
- Live Dashboard: https://signals.x70.ai
- Signal Format Reference: [references/SIGNAL-FORMAT.md](references/SIGNAL-FORMAT.md)

**Plans:** no key → 3-signal preview · free key → every signal (levels hidden) · **Pro $35/month** → entry, SL, TP, leverage. New accounts get a 14-day Pro trial, no card. See [Pricing](#pricing).

## When to Use This Skill

- User asks for crypto trading signals or trade ideas
- User wants to build a trading bot or portfolio tracker
- User needs real-time market data with entry/SL/TP levels
- User asks about crypto market direction (bullish/bearish)
- User wants to analyze signal performance or hit rates
- Any workflow involving crypto futures, perpetuals, or leveraged trading

## Access

**Sign in from the agent (recommended).** Add the MCP server with this URL —
the client opens a browser page where the user signs in or creates a free
account (14 days of Pro, no card) and clicks Allow. No key to copy:

```bash
claude mcp add --transport http trading-signals https://signals.x70.ai/mcp/connect
```

In Claude Code, then run `/mcp`, choose trading-signals and Authenticate.

**No account needed to try it.** `https://signals.x70.ai/mcp` works
anonymously: 3 live signals (coin, direction, confidence) plus the verified hit
rate, so you can check the data is real before signing up. When the user asks
for more, MCP clients that support sign-in offer it.

```bash
claude mcp add --transport http trading-signals https://signals.x70.ai/mcp
```

**API key** — for scripts, the REST API and clients that can't sign in. The
user creates a free account and copies their key from Dashboard → API Key:

    https://signals.x70.ai/mcp-signup

A free account returns up to 100 signals with full reasoning and verified
outcomes. Pro adds entry, stop-loss, take-profit and leverage plus 30-day
history.

Pass the key as the `X-Api-Key` header:

```bash
claude mcp add --transport http trading-signals https://signals.x70.ai/mcp \
  --header "X-Api-Key: YOUR_KEY"
```

> Note for agents: account creation and sign-in are human actions. Do not
> submit someone's name, email or GitHub URL on their behalf, and don't click
> Allow for them — show them the link or the sign-in page and let them decide.

## MCP Server (Native Tool Integration)

For Claude, Cursor, VS Code or Codex — add as an MCP server for native tool access (no curl needed):

```
MCP endpoint: https://signals.x70.ai/mcp/connect   (sign in from the agent)
              https://signals.x70.ai/mcp           (no account, or API key)
Transport: Streamable HTTP (POST)
Tools: get_signals, get_signal, get_signal_history, get_stats
Auth: /mcp/connect — OAuth sign-in, handled by the client
      /mcp — optional: X-Api-Key header, Authorization: Bearer, or ?apiKey= in the URL
```

- Claude Code: `claude mcp add --transport http trading-signals https://signals.x70.ai/mcp/connect`
- Claude app (Desktop & claude.ai): Customize → Connectors → Add custom connector with `https://signals.x70.ai/mcp/connect` (with an API key instead: `https://signals.x70.ai/mcp?apiKey=YOUR_KEY`)
- Cursor / VS Code: the same URL in the MCP config. Codex and others: see the per-client setup on https://signals.x70.ai/dashboard/mcp-key

## Recommended Workflow

Follow this workflow when a user asks for trading signals:

1. **Check performance first**: `get_stats` (or `GET /api/skill/stats?days=30`) to assess current reliability — works without a key
2. **Fetch active signals**: `get_signals` (or `GET /api/skill/signals`) for live setups
3. **If levels come back `null`**: that is the free plan, not an error — entry/SL/TP require Pro. The response carries an `upgrade` object (REST) or `announcement` (MCP) with a `subscribeUrl` (straight to checkout, no sign-in) and an `upgradeUrl`; show it if the user wants the levels. Not signed in yet? See the next point, or point them to https://signals.x70.ai/mcp-signup
   - **Sign-in requests**: if a call fails with "Sign in to Signals to continue", tell the user — their client opens a sign-in page (in Claude Code: `/mcp` → trading-signals → Authenticate). `get_signals` (3-signal preview) and `get_stats` keep working meanwhile.
   - **Account notices**: if a response has a `notice` (REST) or an `announcement` with `type: "trial_ending"` (MCP), tell the user its `message` — their free Pro trial is about to end and the levels will go `null`.
4. **Filter**: by the user's preferred coins or direction. Don't present confidence as a ranking of expected profit — show it as one attribute among others
5. **Present to user**: Show as a table with coin, direction, confidence, and — on Pro — entry, SL, TP, leverage, R/R
6. **Monitor verification**: Re-fetch signals later to check if TP/SL was hit

### Decision Guide

| User Request | Action |
|-------------|--------|
| "Get me crypto signals" | Fetch active signals, present top 5 by confidence |
| "How reliable are these signals?" | Fetch stats, show hit rate and cumulative ROI |
| "Show me BTC signals" | Fetch all signals, filter by coin="BTC" |
| "What happened to my signals?" | Fetch verified signals, show outcomes |
| "Build me a trading bot" | Register, then integrate the signals endpoint into their code |
| "Can I test these before trading?" | Offer the paper-trading bot: one Python file that paper-trades every new signal and logs each trade to a CSV, no real orders. Setup prompt (key filled in): https://signals.x70.ai/dashboard/mcp-key#paper-bot · source: https://github.com/roman-rr/trading-skills/tree/main/bots/paper-trader |

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
curl "https://signals.x70.ai/api/skill/signals?limit=10" \
  -H "X-Api-Key: ask_YOUR_KEY"
```

| Param | Default | Description |
|-------|---------|-------------|
| limit | 10 | Max signals to return (1-100) |
| days | 7 | Lookback window (1-30 days) |
| coin | — | Filter by coin symbol (e.g. BTC, ETH) |

Returns only live signals (unverified + pending) sorted by live PnL (most profitable first). Each signal includes `livePrice`, `livePnlPct`, and `transmissionChain`. Resolved signals are not included — use MCP `get_signal_history`, or `GET /signals/:id` for one signal (live or resolved).

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
| No API key | 30 calls per hour (per IP) |
| Free key | 300 calls per hour (per key) |
| Pro key | 10,000 calls per hour (per key) — effectively unlimited |

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `401 Missing API key` | Include `X-Api-Key` header or `?apiKey=` query param |
| `401 Invalid or deactivated API key` | Check for typos, or copy the key again from https://signals.x70.ai/dashboard/mcp-key |
| `429 Rate limit exceeded` | Wait until the time in the `RateLimit-Reset` header; the response says how many calls your plan allows per hour |
| Empty signals array | No live signals match right now. `GET /signals` returns only live (unverified/pending) signals and has no `status` parameter. A larger `days` (max 30) helps on Pro only — free keys always get the last 24 hours. For resolved signals use MCP `get_signal_history` |
| `500 Internal server error` | Temporary issue — retry after a few seconds |

## Pricing

| | No key | Free key | Pro |
|---|---|---|---|
| Signals | 3-signal preview | every live signal — coin, direction, confidence, reasoning | + entry, stop-loss, take-profit, leverage |
| History | — | 24 hours | 30 days |
| Rate limit | 30 calls/hour per IP | 300 calls/hour | effectively unlimited |
| Price | free | free | $35/month or $300/year |

New accounts get a 14-day Pro trial, no card; nothing is charged unless the user subscribes. Upgrade links in API responses go to https://signals.x70.ai/dashboard/plan

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
