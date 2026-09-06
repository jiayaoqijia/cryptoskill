---
name: gate-info-marketoverview
version: "2026.4.6-1"
updated: "2026-04-06"
description: "Market overview. Use this skill ONLY when the user's query is exclusively about overall market conditions with no specific coin analysis. Trigger phrases: how is the market, market overview, what is happening in crypto. If the query ALSO mentions a specific coin to analyze, risk to check, technicals to review, or any other analysis dimension, use gate-info-research instead — it handles multi-dimension queries in a single unified report."
required_credentials: []
required_env_vars: []
required_permissions: []
---

# gate-info-marketoverview

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read `./references/gate-runtime-rules.md`
→ Also read `./references/info-news-runtime-rules.md` for gate-info / gate-news shared rules (tool degradation, report standards, security, routing, and graceful fallback behavior).
- **Only call MCP tools explicitly listed in this skill.** Tools not documented here must NOT be called, even if they
  exist in the MCP server.

> The crypto market "dashboard" Skill. The user asks about overall market conditions in a single sentence; the system calls 5 MCP Tools in parallel to fetch market-wide data + sector leaderboards + DeFi overview + recent events + macro summary, then the LLM aggregates into a market-briefing-level structured report.

**Trigger Scenarios**: User asks about overall market conditions — not about a specific coin.

## MCP Dependencies

### Required MCP Servers
| MCP Server | Status |
|------------|--------|
| Gate-Info | ✅ Required |

### MCP Tools Used

**Query Operations (Read-only)**

- info_coin_get_coin_rankings
- info_macro_get_macro_summary
- info_marketsnapshot_get_market_overview
- info_marketsnapshot_get_market_snapshot
- info_platformmetrics_get_defi_overview
- news_events_get_latest_events

### Authentication
- API Key Required: No
- Credentials Source: None; this skill uses read-only Gate Info / Gate News MCP access only.

### Installation Check
- Required: Gate-Info
- Install: Use the local Gate MCP installation flow for the current host IDE before continuing.
- Continue only after the required Gate MCP server is available in the current environment.

## Routing Rules

| User Intent | Keywords | Action |
|-------------|----------|--------|
| Market overview | "how's the market" "market overview" "what's happening in crypto" "are we up or down today" | Execute this Skill's full workflow |
| Single coin analysis | "how is BTC" "analyze ETH" | Route to `gate-info-coinanalysis` |
| News only | "what's happening" | Route to `gate-news-briefing` |
| DeFi deep-dive | "which DeFi protocol is best" "TVL rankings" | Route to `gate-info-defianalysis` |
| Macro deep-dive | "how's the jobs report" "any economic data today" | Route to `gate-info-macroimpact` |

---

## Execution Workflow

### Step 0: Multi-Dimension Intent Check

Before executing this Skill, check if the user's query involves multiple analysis dimensions:

- If the query is exclusively about overall market conditions with no specific coin to deep-dive, proceed with this Skill.
- If the query **also** mentions a specific coin to analyze, risk to check, technicals to review, or any other analysis dimension beyond market overview, route to `gate-info-research` — it handles multi-dimension queries with unified tool deduplication and coherent report aggregation.

### Step 1: Intent Recognition

Confirm the user is asking about overall market conditions (not a single coin). Optionally extract:
- `time_context`: e.g., "today", "this week", "recently" (affects news/event time range)

### Step 2: Call 5 MCP Tools in Parallel

| Step | MCP Tool | Parameters | Retrieved Data | Parallel |
|------|----------|------------|----------------|----------|
| 1a | `info_marketsnapshot_get_market_overview` | (none) | Full market: total market cap, 24h volume, BTC dominance, Fear & Greed Index, gainer/loser ratio | Yes |
| 1b | `info_coin_get_coin_rankings` | `ranking_type="gainers", time_range="24h", limit=5` | Top 5 gainers | Yes |
| 1c | `info_platformmetrics_get_defi_overview` | `category="all"` | DeFi total TVL, DEX 24h volume, stablecoin total market cap | Yes |
| 1d | `news_events_get_latest_events` | `time_range="24h", limit=5` | Major events in the past 24h | Yes |
| 1e | `info_macro_get_macro_summary` | (none) | Macro snapshot (DXY, rates, CPI trend) | Yes |

> All 5 Tools are called in parallel with no dependencies. If a tool is not available, omit that call and mark the corresponding report section as "No data". If `info_marketsnapshot_get_market_overview` is not available, use `info_marketsnapshot_get_market_snapshot` for BTC/ETH as fallback.

### Step 2b: Optional Supplementary Calls

| Condition | Supplementary Tool | Parameters | Purpose |
|-----------|--------------------|------------|---------|
| User asks about "this week" or needs trend context | `info_coin_get_coin_rankings` | `ranking_type="losers", time_range="24h", limit=5` | Add top losers |
| User is interested in sector rotation | `info_coin_get_coin_rankings` | `ranking_type="hot", limit=10` | Trending coins |

### Step 3: LLM Aggregation

---

## Report Template

```markdown
## Crypto Market Overview

> Data as of: {timestamp}

### 1. Market Summary

| Metric | Current Value | 24h Change |
|--------|--------------|------------|
| Total Market Cap | ${total_market_cap} | {change}% |
| 24h Volume | ${total_volume_24h} | {change}% |
| BTC Dominance | {btc_dominance}% | {change}pp |
| Fear & Greed Index | {fear_greed_index} | {Extreme Fear/Fear/Neutral/Greed/Extreme Greed} |
| Gainer/Loser Ratio | {gainers}/{losers} | {Bulls/Bears/Balanced} |

**Market Status**: {One-sentence description of the current market state based on the above metrics}

### 2. Sectors & Leaderboard

**24h Top Gainers**

| Rank | Coin | Price | 24h Change |
|------|------|-------|------------|
| 1 | {symbol} | ${price} | +{change}% |
| 2 | ... | ... | ... |

**24h Top Losers** (if data available)

| Rank | Coin | Price | 24h Change |
|------|------|-------|------------|
| 1 | {symbol} | ${price} | {change}% |
| 2 | ... | ... | ... |

{If the leaderboards show sector patterns (e.g., L2s rallying, Memes dumping), flag sector rotation}

### 3. DeFi Overview

| Metric | Value | Change |
|--------|-------|--------|
| DeFi Total TVL | ${defi_tvl} | {change}% |
| DEX 24h Volume | ${dex_volume} | {change}% |
| Stablecoin Total Market Cap | ${stablecoin_cap} | {change}% |

### 4. Recent Major Events

1. 🔴/🟡/🟢 [{event_title}] — {event_summary} ({time})
2. ...

> 🔴 = High impact, 🟡 = Medium impact, 🟢 = Low impact

### 5. Macro Environment

| Metric | Value | Trend |
|--------|-------|-------|
| US Dollar Index (DXY) | {dxy} | {Rising/Falling/Sideways} |
| 10Y Treasury Yield | {yield_10y}% | {Rising/Falling} |
| Fed Funds Rate | {fed_rate}% | {Hiking/Cutting/Paused} |

{If there are upcoming macro events (NFP, CPI, FOMC), briefly mention potential market impact}

### 6. Overall Assessment

{LLM generates a 3-5 sentence assessment:}
- Current market phase (bull / bear / sideways / recovery)
- Primary drivers
- Key risks or opportunities to watch

> The above analysis is data-driven and does not constitute investment advice.
```

---

## Decision Logic

| Condition | Label/Assessment |
|-----------|-----------------|
| fear_greed > 75 | "Extreme Greed — exercise caution at highs" |
| fear_greed < 25 | "Extreme Fear — potential opportunity amid panic" |
| BTC dominance > 55% and most altcoins declining | "Capital rotating back to BTC — altcoins under pressure" |
| BTC dominance declining + most altcoins rising | "Potential altcoin season" |
| Gainer/Loser ratio > 3:1 | "Broad-based rally — bulls in control" |
| Gainer/Loser ratio < 1:3 | "Broad-based decline — bears in control" |
| DeFi TVL 7d change > +10% | "Significant capital inflow into DeFi" |
| Stablecoin market cap rising | "Off-exchange capital flowing in — bullish signal" |
| Any Tool returns empty/error | Skip that section; note "Data unavailable" |

---

## Error Handling

| Error Type | Handling |
|------------|----------|
| get_market_overview or core snapshot fails | Return degraded version showing only available sections; or use get_market_snapshot for BTC/ETH as fallback |
| Macro data unavailable | Skip "Macro Environment" section; note "Macro data temporarily unavailable" |
| Event data unavailable | Skip "Recent Major Events" section |
| All Tools fail | Return error message; suggest the user try again later |

---

## Cross-Skill Routing

| User Follow-up Intent | Route To |
|-----------------------|----------|
| "How is BTC?" / clicks on a specific coin | `gate-info-coinanalysis` |
| "Why did XX pump?" | `gate-news-eventexplain` |
| "Any recent news?" | `gate-news-briefing` |
| "DeFi details" | `gate-info-defianalysis` |
| "Macro data impact" | `gate-info-macroimpact` |
| "Give me a BTC technical analysis" | `gate-info-trendanalysis` |

---

## Safety Rules

1. **No investment advice**: Market assessments are data-driven; must include a "not investment advice" disclaimer
2. **No trend predictions**: Do not output "tomorrow will go up/down" style predictions
3. **Data transparency**: Label data source and update time
4. **Flag missing data**: When any section has no data, explicitly state it — never fabricate data
5. **Avoid emotional language**: Use objective, neutral language to describe market conditions
