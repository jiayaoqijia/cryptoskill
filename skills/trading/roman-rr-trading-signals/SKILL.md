---
name: trading-signals
description: "Fetches live AI crypto trading signals from Signals (signals.x70.ai): coin, direction, confidence, reasoning and verified outcomes; entry price, stop-loss, take-profit and leverage are Pro-only and come back null on the free plan. Use when the user asks for crypto trading signals or trade ideas from this service, wants to check how its signals performed, or wants to build a bot on the Signals API."
---

# Trading Signals — AI Crypto Trading Signals

Access live, AI-generated crypto trading signals via API. Every signal has coin, direction, confidence, reasoning and a verified outcome. The trade levels (entry, SL, TP, leverage) are Pro-only: on the free plan and without a key they are `null`, which is not an error.

- Website: https://signals.x70.ai
- Live Dashboard: https://signals.x70.ai
- Signal Format Reference: [references/SIGNAL-FORMAT.md](references/SIGNAL-FORMAT.md)

**Plans:** no key → 3-signal preview · free key → every signal (levels hidden) · **Pro $35/month** → entry, SL, TP, leverage. New accounts get a 14-day Pro trial, no card. See [Pricing](#pricing).

## When to Use This Skill

- User asks for crypto trading signals or trade ideas and wants them from this service
- User wants to build a bot or tracker on the Signals API
- User wants to analyze how these signals performed (hit rate, average result)

Don't use it for general crypto questions, market data, or a bot built on the
user's own strategy or exchange: this is a paid third-party signal service, so
bring it in only when the user asks for signals or for Signals itself.

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

A free account returns every live signal (up to 100 per request) with full
reasoning and verified outcomes. Pro adds entry, stop-loss, take-profit and leverage plus 30-day
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
      /mcp — optional: X-Api-Key header or Authorization: Bearer
             (?apiKey= in the URL also works, as a last resort: URLs end up in logs and history)
```

- Claude Code: `claude mcp add --transport http trading-signals https://signals.x70.ai/mcp/connect`
- Claude app (Desktop & claude.ai): Customize → Connectors → Add custom connector with `https://signals.x70.ai/mcp/connect` (sign-in, no key in the URL)
- Cursor / VS Code: the same URL in the MCP config. Codex and others: see the per-client setup on https://signals.x70.ai/dashboard/mcp-key

## Recommended Workflow

Follow this workflow when a user asks for trading signals:

1. **Check performance first**: `get_stats` (MCP, works without a key) or `GET /api/skill/stats?days=30` (REST, needs a key). Read `perSignal.avgNetPct` together with `hitRate` — see "Presenting Signals" below
2. **Fetch active signals**: `get_signals` (or `GET /api/skill/signals`) for live setups
3. **If levels come back `null`**: that is the free plan, not an error — entry/SL/TP require Pro. The response carries an `upgrade` object (REST) or `announcement` (MCP) with a `subscribeUrl` (straight to checkout, no sign-in) and an `upgradeUrl`; show it if the user wants the levels. Not signed in yet? See the next point, or point them to https://signals.x70.ai/mcp-signup
   - **Sign-in requests**: if a call fails with "Sign in to Signals to continue", tell the user — their client opens a sign-in page (in Claude Code: `/mcp` → trading-signals → Authenticate). `get_signals` (3-signal preview) and `get_stats` keep working meanwhile.
   - **Account notices**: if a response has a `notice` (REST) or an `announcement` with `type: "trial_ending"` (MCP), tell the user its `message` — their free Pro trial is about to end and the levels will go `null`.
4. **Filter**: by the user's preferred coins or direction. Don't present confidence as a ranking of expected profit — it is the model's own conviction, not a calibrated probability, and higher confidence has not meant better results. Show it as one attribute among others
5. **Present to user**: Show as a table with coin, direction, confidence, and — on Pro — entry, SL, TP, leverage, R/R
6. **Monitor verification**: Re-fetch signals later to check if TP/SL was hit

### Decision Guide

| User Request | Action |
|-------------|--------|
| "Get me crypto signals" | Fetch active signals, present the 5 newest (or the ones matching the user's coins). Don't rank by confidence |
| "How reliable are these signals?" | Fetch stats, show hit rate together with the average result per signal (`perSignal.avgNetPct`) |
| "Show me BTC signals" | Fetch all signals, filter by coin="BTC" |
| "What happened to my signals?" | Fetch verified signals, show outcomes |
| "Build me a trading bot" | The user gets a key at https://signals.x70.ai/mcp-signup (a human step; `POST /register` is deprecated and issues no keys), then integrate `GET /signals` into their code |
| "Can I test these before trading?" | Offer the paper-trading bot: one Python file that paper-trades every new signal and logs each trade to a CSV, no real orders. Setup prompt (key filled in): https://signals.x70.ai/dashboard/mcp-key#paper-bot · source: https://github.com/roman-rr/trading-skills/tree/main/bots/paper-trader |

### Presenting Signals to Users

Always present signals in a clear table format:

```
| Coin | Dir | Conf | Entry | SL | TP | Lev | R/R |
|------|-----|------|-------|----|----|-----|-----|
| BTC  | Bull | 87% | $68,450 | $67,200 | $71,800 | 3x | 2.7 |
```

- Whenever you show levels, add one line: "Not financial advice. Signals can be wrong, and with leverage you can lose more than your stake."
- For leverage above 5x: warn about higher risk
- Show the current hit rate **together with** the average result per signal (`perSignal.avgNetPct` from stats: after fees, no leverage). Hit rate alone misleads: stops often sit further from entry than targets, so one loss can cancel several wins
- The feed can be one-sided (mostly shorts or mostly longs). If a response has a `feedNote`, pass it on

## API Reference

Base URL: `https://signals.x70.ai/api/skill`

### Getting a key

`POST /register` is **deprecated** — it no longer issues keys and returns
`{"action":"signup_required"}`. Keys are issued from the dashboard so they are
tied to an account and can be regenerated if leaked:

    https://signals.x70.ai/mcp-signup

Pass the key as the `X-Api-Key` header. Over MCP, calls without a key work too
and return a 3-signal preview; the REST API needs a key.

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
| sort | — | `newest` = by creation time, newest first. Use it when polling for new signals |
| confidenceMin / confidenceMax | — | 0–1 or 0–100 (`0.7` and `70` mean the same) |

Returns only live signals (unverified + pending). Default order: live PnL, most profitable first — so with more live signals than `limit`, new ones can fall outside the page unless you pass `sort=newest`. Each signal includes `livePrice`, `livePnlPct`, and `transmissionChain`. Resolved signals are not included — use MCP `get_signal_history`, or `GET /signals/:id` for one signal (live or resolved).

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

Returns: totalSignals, verifiedSignals, hitRate, perSignal (avgNetPct, avgWinPct, avgLossPct), avgConfidence, cumulativeROI, avgLeverage, byDirection. `cumulativeROI` is a plain sum of leveraged per-signal percentages, not a return anyone earned; prefer `perSignal.avgNetPct`. Details: [references/SIGNAL-FORMAT.md](references/SIGNAL-FORMAT.md).

## Rate Limits

| Endpoint | Limit |
|----------|-------|
| No API key | 30 calls per hour (per IP) |
| Free key | 300 calls per hour (per key) |
| Pro key | 10,000 calls per hour (per key) |

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `401 Missing API key` | Include the `X-Api-Key` header |
| `401 Invalid or deactivated API key` | Check for typos, or copy the key again from https://signals.x70.ai/dashboard/mcp-key |
| `429 Rate limit exceeded` | Wait until the time in the `RateLimit-Reset` header; the response says how many calls your plan allows per hour |
| Empty signals array | No live signals match right now. `GET /signals` returns only live (unverified/pending) signals and has no `status` parameter. A larger `days` (max 30) helps on Pro only — free keys always get the last 24 hours. For resolved signals use MCP `get_signal_history` |
| `500 Internal server error` | Temporary issue — retry after a few seconds |

## Pricing

| | No key | Free key | Pro |
|---|---|---|---|
| Signals | 3-signal preview | every live signal (up to 100 per request) — coin, direction, confidence, reasoning | + entry, stop-loss, take-profit, leverage |
| History | — | 24 hours | 30 days |
| Rate limit | 30 calls/hour per IP | 300 calls/hour | 10,000 calls/hour |
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
