# Routing And Analysis

This file defines:

1. how user intents are routed
2. which analysis modules should be used for which trading scenario
3. when to output `GO / CAUTION / BLOCK`

---

## 1. Intent Routing

| User Type | Typical Request | Handling |
|---|---|---|
| Judge before trading | `Can I buy BTC now?` | Enter single-asset trade-decision flow |
| Direction already chosen, wants risk control | `I want to long ETH, but check liquidation and momentum first` | Enter futures-focused decision flow |
| Event-driven trade | `ETH suddenly dumped, can I buy the dip?` | Run event explanation first, then technical + microstructure checks |
| New coin / long-tail trade | `Can I trade this newly listed coin?` | Run listing/risk check first, then pre-trade decision flow |
| Opportunity discovery | `What is a good trade today?` | Run lightweight market scan, then narrow to one asset |
| Order / position management | `Amend that order`, `close half` | Enter execution-management flow directly without full research loop |

---

## 2. Narrowing Rules: Asset and Market

### 2.1 Must be clear before execution

- one asset
- one market (spot or USDT perpetual futures)
- one action direction

### 2.2 Scan first, narrow second

If the user has trading intent but no clear asset yet, for example:

- `What is a good trade today?`
- `Is there anything worth trading right now?`

then a lightweight scan is allowed:

- market state
- current dominant events/news

Recommended MCP tools:

- `news_feed_search_news`
- `news_feed_get_exchange_announcements` when exchange activity matters
- `info_marketsnapshot_get_market_snapshot`
- `info_markettrend_get_technical_analysis` after narrowing to 1-2 candidate majors

At this stage, give at most **1-2 candidate directions**, then ask the user to choose a target asset before entering the real trading loop.

Never produce an order draft before narrowing down to one asset and one market.

---

## 3. Analysis Module Selection

### 3.0 Baseline MCP surfaces

Use the documented Gate MCP surfaces as the portable baseline for this composite skill:

- `info_*` -> Gate Info MCP
- `news_feed_*` -> Gate News MCP
- read-only `cex_spot_*` / `cex_fx_*` market-data calls -> Gate public market MCP or a local combined Gate MCP runtime
- private `cex_*` trading and account calls -> authenticated Gate Exchange MCP or a local authenticated Gate MCP runtime

If the runtime exposes extra namespaces beyond this baseline, they may be treated as optional accelerators only. The baseline scenarios in this file must remain viable without them.

### 3.0 Module-to-MCP Mapping

To make this composite skill self-contained, the core analysis modules are mapped below.

| Analysis Module | Purpose | MCP Tools |
|---|---|---|
| Market overview | Understand the broad market before trading | `news_feed_search_news`, `news_feed_get_exchange_announcements` when exchange activity matters, `info_markettrend_get_technical_analysis` after narrowing to 1-2 candidate majors, optional `info_marketsnapshot_get_market_snapshot` when it returns populated fields |
| News briefing | Understand current headlines and sentiment context | `news_feed_search_news`, `news_feed_get_exchange_announcements` when exchange activity matters, `news_feed_search_news` with `platform_type=\"social_ugc\"` when social chatter matters |
| Listing / exchange announcement context | Understand whether the asset is newly listed, delisting-related, or driven by exchange activity | `news_feed_get_exchange_announcements`, `info_coin_get_coin_info`, optional `info_marketsnapshot_get_market_snapshot` when it returns populated fields |
| Single-coin analysis | Understand whether an asset is worth trading | `info_coin_get_coin_info` for identity/disambiguation, `info_markettrend_get_technical_analysis`, `info_markettrend_get_kline`, `news_feed_search_news`, optional `info_marketsnapshot_get_market_snapshot` when it returns populated fields |
| Technical analysis | Understand trend, indicators, support, resistance | `info_markettrend_get_kline`, optional `info_markettrend_get_indicator_history` with array-form `indicators`, `info_markettrend_get_technical_analysis`, optional `info_marketsnapshot_get_market_snapshot` when it returns populated fields |
| Event explanation | Understand why a move happened | `news_feed_search_news`, `news_feed_search_news` with `platform_type=\"social_ugc\"` when social chatter matters, `news_feed_get_exchange_announcements` when exchange activity is suspected, `info_markettrend_get_kline`, optional `info_marketsnapshot_get_market_snapshot` or `info_onchain_get_token_onchain` when they return populated fields |
| Risk check | Check token / contract security | `info_coin_get_coin_info`, then `info_compliance_check_token_security` only after chain/address resolution |
| Address tracing | Check address profile, transactions, and tx-level flow fragments | `info_onchain_get_address_info`, `info_onchain_get_address_transactions`, `info_onchain_get_transaction` |
| Exchange microstructure | Check liquidity, slippage, momentum, liquidation, basis, order-book quality | `cex_spot_*` or `cex_fx_*` market-data tools, based on spot/futures routing |

### 3.0A Analysis-side availability rule

Apply the shared runtime rules first via [`gate-runtime-rules.md`](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md).

This composite skill assumes the runtime exposes the referenced `info_*` and `news_*` tools.

If the current runtime does **not** expose the required analysis namespace:

1. do not pretend that full pre-trade judgment was completed
2. do not synthesize a fake `GO` decision from missing data
3. do not continue into a new-trade `Order Draft`
4. report that the analysis-side environment remains unavailable after applying the shared runtime rules

Allowed exception:

- if the user request is pure order/position management, the skill may still continue with the execution-management flow, because that path can be valid without re-running the full research chain

For new-trade requests, missing core analysis modules should be treated as a runtime block rather than silently degraded into execution.

### 3.0B Tool-name drift and fallback rules

This skill must validate concrete tool names against the current runtime tool list before calling them. Prefer the current runtime surface over older examples, screenshots, or stale repo docs.

Known fallback rules:

1. If `info_marketsnapshot_get_market_overview` is unavailable, do not try to recreate full market breadth from a sparse `info_marketsnapshot_get_market_snapshot` payload. Use `news_feed_search_news`, `info_markettrend_get_technical_analysis`, and exchange market-data reads for the narrowed asset instead.
2. If `info_coin_get_coin_rankings` or `info_macro_get_macro_summary` is unavailable, do not claim ranking coverage or macro-summary coverage. Narrow to 1-2 candidate majors first, then use `info_coin_get_coin_info`, trend tools, and relevant news tools.
3. If `info_onchain_trace_fund_flow` is unavailable, use `info_onchain_get_address_transactions` and `info_onchain_get_transaction` for manual trace fragments, plus `info_onchain_get_token_onchain` only as supporting context when it returns populated fields. Do not present this as a full automated fund-flow trace.
4. Prefer the documented `news_feed_*` tools as the default news path. Do not make undocumented `news_events_*` tools a prerequisite for any baseline scenario in this file.
5. Do not use `news_feed_get_social_sentiment` as a default coin-level sentiment tool. In the current runtime it requires `post_id`, so use `news_feed_search_news(platform_type=\"social_ugc\")` for generic social context and reserve `news_feed_get_social_sentiment` for post-specific follow-up only.
6. Do not call `info_compliance_check_token_security` until the chain or contract address is resolved with confidence.

### 3.0.1 Spot microstructure tools

- `cex_spot_get_spot_order_book`
- `cex_spot_get_spot_candlesticks`
- `cex_spot_get_spot_tickers`
- `cex_spot_get_spot_trades`

### 3.0.2 Futures microstructure tools

- `cex_fx_get_fx_contract`
- `cex_fx_get_fx_order_book`
- `cex_fx_get_fx_candlesticks`
- `cex_fx_get_fx_tickers`
- `cex_fx_get_fx_trades`
- `cex_fx_get_fx_funding_rate`
- `cex_fx_list_fx_liq_orders`
- `cex_fx_get_fx_premium_index`

### 3.1 Base mode (default)

Use when:

- the user already gave one asset
- the user simply wants to know whether buying/selling/longing/shorting makes sense now

Call:

1. `single-coin analysis`
   - `info_coin_get_coin_info`
   - `info_markettrend_get_technical_analysis`
   - `info_markettrend_get_kline`
   - add `news_feed_search_news` only when headline context matters
   - add `info_marketsnapshot_get_market_snapshot` only when it returns populated fields
2. `technical analysis`
   - `info_markettrend_get_kline`
   - `info_markettrend_get_indicator_history` with array-form `indicators` only when the extra detail is needed
   - `info_markettrend_get_technical_analysis`
   - `info_marketsnapshot_get_market_snapshot` only when it returns populated fields

Expected output:

- directional read
- key price levels
- current uncertainty

### 3.2 Execution-sensitive mode

Use when:

- the user cares about execution quality
- the size is large
- the user explicitly asks about slippage, liquidity, support/resistance, order book, or liquidation
- the user wants futures

Add:

3. `exchange microstructure analysis`

Recommended patterns:

- spot liquidity / slippage
  - `cex_spot_get_spot_order_book` -> `cex_spot_get_spot_tickers`
- spot momentum
  - `cex_spot_get_spot_trades` -> `cex_spot_get_spot_tickers` -> `cex_spot_get_spot_candlesticks`
- futures momentum
  - `cex_fx_get_fx_trades` -> `cex_fx_get_fx_tickers` -> `cex_fx_get_fx_candlesticks` -> `cex_fx_get_fx_funding_rate`
- futures liquidation
  - `cex_fx_list_fx_liq_orders` -> `cex_fx_get_fx_candlesticks` -> `cex_fx_get_fx_tickers`
- futures basis / funding
  - `cex_fx_get_fx_tickers` -> `cex_fx_get_fx_funding_rate` -> `cex_fx_get_fx_premium_index`

Preferred sub-scenarios:

| Scenario | When to use |
|---|---|
| Liquidity / Slippage | Large spot or futures trade; user asks whether the market can absorb the size |
| Momentum | User wants futures direction judgment |
| Liquidation | User asks about squeeze / wipeout / forced-move conditions |
| Basis / Funding | User wants perpetual futures, especially short-term trading |
| Support / Resistance | User asks for entry level, breakout level, or resistance level |

### 3.3 Event-driven mode

Use when:

- the user is triggered by a sudden move
- the user asks `why did this happen, and is it tradable now?`

Call:

1. `event explanation`
   - `news_feed_search_news`
   - `news_feed_search_news` with `platform_type="social_ugc"` when social chatter matters
   - `news_feed_get_exchange_announcements` when exchange activity is suspected
   - `info_markettrend_get_kline`
   - `info_marketsnapshot_get_market_snapshot` only when it returns populated fields
   - `info_onchain_get_token_onchain` only when on-chain confirmation is needed and the payload is non-sparse
2. `technical analysis`
3. `exchange microstructure analysis`
4. add `single-coin analysis` when broader context is still needed

Goal:

- decide whether the move is driven by news, on-chain flow, liquidation, or sentiment
- then decide whether it is tradable

### 3.4 New coin / long-tail mode

Use when:

- the user mentions a newly listed coin
- the user mentions exchange listing / new listing / recently listed
- the user mentions meme / contract address / honeypot / rug / safety
- the user wants to trade an unfamiliar small-cap asset

Call:

1. `listing / exchange announcement context` when the request is explicitly listing-driven
   - `news_feed_get_exchange_announcements`
   - `info_coin_get_coin_info`
   - `info_marketsnapshot_get_market_snapshot` only when it returns populated fields
2. `risk check`
   - `info_coin_get_coin_info`
   - `info_compliance_check_token_security` only after chain/address resolution
3. `address tracing` only when the user provides an address and wants fund-source tracing
   - `info_onchain_get_address_info`
   - `info_onchain_get_address_transactions`
   - `info_onchain_get_transaction`
4. `single-coin analysis`
5. `technical analysis`
6. `exchange microstructure analysis`

Important:

- risk check is not optional in this mode; it is the trade gate

---

## 4. Risk Gate Rules

### 4.1 Mandatory risk-check triggers

Run token/contract risk check before drafting if any of these apply:

- the user explicitly asks about safety / honeypot / rug / scam / risk
- the user provides a contract address
- the user says `new coin`, `new listing`, `meme`, `small cap`, `long-tail`
- the trading target is not a common major asset and identity confidence is low

### 4.2 Address tracing should only be used when

- the user provides an address directly
- the user asks where funds came from / who is selling / who is buying
- the user suspects a project or whale address is driving price action

Do not use address tracing as a default step before every trade.

### 4.3 Risk result translation

| Result | Meaning | Next Action |
|---|---|---|
| `GO` | No trade-breaking risk was identified | Order draft may be produced |
| `CAUTION` | Trading is possible, but meaningful risk exists | Warn clearly, then drafting may continue |
| `BLOCK` | The workflow should not continue to execution | Stop at analysis level; do not draft |

### 4.4 Default `BLOCK` cases

- honeypot / likely unsellable token
- invalid or non-tradable pair / contract
- exchange currently does not allow trading on that asset
- the user asks to bypass security or compliance
- the requested execution ability is outside supported scope

### 4.5 Default `CAUTION` cases

- high token tax
- concentrated holdings
- poor liquidity
- notable slippage
- extreme funding
- elevated liquidation / crowding risk
- a major event just happened and direction is unresolved
- newly listed asset still in price discovery

---

## 5. Trading Brief Template

Before any execution, produce a `Trading Brief` with at least five parts:

```markdown
## Trading Brief

### 1. User Intent
- {what the user wants to do}

### 2. Market Read
- {bullish / bearish / sideways / event-driven / elevated risk}

### 3. Key Evidence
- {technical evidence}
- {event/news evidence}
- {liquidity / order book / liquidation evidence}
- {risk-check evidence, if any}

### 4. Risk Level
- {GO / CAUTION / BLOCK}

### 5. Next Step
- {continue to order draft / suggest waiting / ask for missing inputs}
```

Constraints:

- never say `guaranteed`
- never turn analysis into certainty
- if the result is `BLOCK`, stop there

---

## 6. Typical Composite Paths

### 6.1 Spot trade after judgment

`single-coin analysis` -> `technical analysis` -> optional `liquidity/slippage` -> `Trading Brief` -> `spot order draft`

### 6.2 Futures trade after judgment

`technical analysis` -> `momentum/liquidation/funding` -> optional `event explanation` -> `Trading Brief` -> `futures order draft`

### 6.3 New-coin starter trade

`listing info` -> `risk check` -> `technical analysis` -> `liquidity/slippage` -> `Trading Brief` -> `spot order draft`

### 6.4 Buy-the-dip after a dump

`event explanation` -> `technical analysis` -> `liquidity/liquidation` -> `Trading Brief` -> `spot or futures order draft`

### 6.5 Market scan to opportunity

`market overview` -> `news briefing` -> pick 1-2 candidates -> user chooses one asset -> normal pre-trade workflow -> order draft

Important: scanning is not execution. Execution must still return to one-asset closure.
