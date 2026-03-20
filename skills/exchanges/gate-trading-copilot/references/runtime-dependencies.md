# Runtime Dependencies

This file defines the minimum runtime dependencies for `gate-exchange-trading-copilot`.

## 1. Required MCP Surfaces

The skill is portable only when the runtime exposes these baseline surfaces:

- `info_*` from Gate Info MCP
- `news_feed_*` from Gate News MCP
- read-only `cex_spot_*` / `cex_fx_*` market-data tools from Gate public market MCP or a local combined Gate MCP runtime
- private `cex_*` trading and account tools from authenticated Gate Exchange MCP or a local authenticated Gate MCP runtime

Optional runtime extras may exist, but the skill must not depend on them for baseline scenarios.

## 2. Baseline Tool Families

### 2.1 Analysis Side

- `info_coin_get_coin_info`
- `info_marketsnapshot_get_market_snapshot`
- `info_markettrend_get_kline`
- `info_markettrend_get_indicator_history`
- `info_markettrend_get_technical_analysis`
- `info_compliance_check_token_security`
- `info_onchain_get_address_info`
- `info_onchain_get_address_transactions`
- `info_onchain_get_transaction`
- `info_onchain_get_token_onchain`
- `news_feed_search_news`
- `news_feed_get_exchange_announcements`
- `news_feed_get_social_sentiment` only when a specific `post_id` is available

Notes:

- `info_marketsnapshot_get_market_snapshot` may return sparse payloads in some runtimes; use it as supplementary context rather than primary evidence unless populated.
- `info_markettrend_get_indicator_history` may require array-form `indicators` in the current runtime.
- `info_compliance_check_token_security` requires resolved `chain` plus token/address context.
- generic social context should prefer `news_feed_search_news` with `platform_type=\"social_ugc\"`; reserve `news_feed_get_social_sentiment` for post-specific follow-up.

### 2.2 Execution Side

- spot read/write: `cex_spot_*`
- futures read/write: `cex_fx_*`
- wallet fee and balance helpers when needed: selected `cex_wallet_*`

## 3. Authentication Rules

- `info_*` and `news_feed_*` are expected to work without authentication in the normal Gate hosted MCP deployment.
- read-only public market data may work without authentication, depending on the runtime surface.
- private order placement, order management, position queries, balances, and account verification require authenticated Gate execution tools.

## 4. Runtime Gate Expectations

Before analysis or execution, the runtime should prove:

1. Gate MCP is installed and reachable.
2. The required baseline tool families are exposed.
3. Authenticated execution tools are available before private trading/account actions.

If a required tool family is missing:

- do not overclaim full skill coverage
- do not synthesize fake execution or fake analysis depth
- narrow to the supported subset or block the workflow

## 5. Tool Drift Guidance

If the runtime exposes newer or extra tools:

- prefer the current runtime tool list over stale examples
- keep baseline scenarios compatible with the documented tool surface
- treat non-baseline extras, such as undocumented helper namespaces, as optional accelerators only
