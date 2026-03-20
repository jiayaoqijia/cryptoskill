# Gate Exchange Trading Copilot — Scenarios & Prompt Examples

## Scenario 1: Spot Buy Decision And Draft
**Context**: The user wants a single cryptocurrency trading skill on Gate Exchange to judge whether BTC is worth buying now and then prepare a spot draft.
**Prompt Examples**:
- "Check whether BTC is worth buying now, and if the setup looks good, give me a spot buy draft."
- "Analyze BTC first, and if the setup is acceptable, give me a spot buy draft."
**Expected Behavior**:
1. Fetch coin identity and headline context via `info_coin_get_coin_info(query="BTC", query_type="symbol", scope="detailed")` and `news_feed_search_news(query="BTC", coin="BTC", sort_by="importance", limit=5)`
2. Fetch trend confirmation via `info_markettrend_get_technical_analysis(symbol="BTC")` and `info_markettrend_get_kline(symbol="BTC", timeframe="1h", period="24h", with_indicators=true)`
3. Add `info_marketsnapshot_get_market_snapshot(symbol="BTC", timeframe="1h", source="spot")` only as supplementary context when it returns populated fields
4. Fetch executable spot context via `cex_spot_get_currency_pair(currency_pair="BTC_USDT")` and `cex_spot_get_spot_tickers(currency_pair="BTC_USDT")`
5. Calculate a pre-trade judgment and risk conclusion
6. Output a `Trading Brief`, then a spot `Order Draft` if not blocked

## Scenario 2: Futures Long With Microstructure Check
**Context**: The user wants to long ETH perpetual, but only after checking momentum, liquidation pressure, and funding conditions.
**Prompt Examples**:
- "I want to long ETH perpetual, but check momentum, liquidation, and funding first before deciding whether to place the order."
- "I want to long ETH perpetual. Check momentum, liquidation, and funding before drafting the trade."
**Expected Behavior**:
1. Fetch data via `cex_fx_get_fx_contract(settle="usdt", contract="ETH_USDT")` and `cex_fx_get_fx_tickers(settle="usdt", contract="ETH_USDT")`
2. Fetch microstructure via `cex_fx_get_fx_order_book(settle="usdt", contract="ETH_USDT")`, `cex_fx_list_fx_liq_orders(settle="usdt", contract="ETH_USDT")`, and `cex_fx_get_fx_funding_rate(settle="usdt", contract="ETH_USDT")`
3. Calculate the futures-side trade setup and liquidation or funding risk
4. Output a futures-oriented `Trading Brief`
5. Output a futures `Order Draft` with leverage visibility, then wait for explicit confirmation

## Scenario 3: News-Driven Dip Buy
**Context**: The user notices a sharp ETH move and wants explanation plus a small follow-up spot trade plan on Gate Exchange.
**Prompt Examples**:
- "ETH just dumped hard. Explain what happened, then tell me whether a small dip-buy makes sense."
- "ETH just dumped. Explain why, then tell me whether a small spot dip-buy makes sense."
**Expected Behavior**:
1. Fetch recent headlines via `news_feed_search_news(query="ETH", coin="ETH", sort_by="importance", limit=10)`
2. Fetch social context via `news_feed_search_news(query="ETH", coin="ETH", platform_type="social_ugc", sort_by="sentiment", limit=5)` when a sentiment read is needed
3. Fetch market confirmation via `info_markettrend_get_kline(symbol="ETH", timeframe="15m", period="24h", with_indicators=true)` and `cex_spot_get_spot_tickers(currency_pair="ETH_USDT")`
4. Add `info_marketsnapshot_get_market_snapshot(symbol="ETH", timeframe="1h", source="spot")` or `info_onchain_get_token_onchain(token="ETH", chain="ethereum", scope="activity")` only as supplementary context when they return populated fields
5. Calculate whether the move is news-driven, sentiment-driven, liquidation-driven, or momentum continuation
6. Output a `Trading Brief` that separates catalyst risk from entry timing, then a conservative spot `Order Draft` only if the risk gate is not blocked

## Scenario 4: New Listing Risk Gate
**Context**: The user wants to trade a newly listed token. The skill should not jump directly into execution without listing context and token security checks.
**Prompt Examples**:
- "This newly listed token looks risky. Check it before telling me whether I can buy it."
- "This newly listed token looks interesting. Check the risk before giving me any trade plan."
**Expected Behavior**:
1. Fetch data via `news_feed_get_exchange_announcements(coin="TOKEN", announcement_type="listing")` and `info_coin_get_coin_info(query="TOKEN", query_type="symbol", scope="detailed")`
2. Resolve the chain or contract address from coin info or user input before security analysis
3. Fetch security context via `info_compliance_check_token_security(token="TOKEN", chain="RESOLVED_CHAIN")` only after chain resolution
4. If chain or address cannot be resolved confidently, stop at `CAUTION` or ask for the contract address instead of pretending the security check completed
5. Calculate whether liquidity, security, or manipulation concerns require a hard block
6. Output a `Trading Brief` with `GO / CAUTION / BLOCK`
7. Output a refusal or warning instead of an executable draft when the risk gate remains blocked

## Scenario 5: Amend An Existing Spot Order
**Context**: The user already has an unfilled spot order and wants to raise the bid slightly without rerunning the full research workflow.
**Prompt Examples**:
- "Raise the unfilled BTC buy order I just placed by 1%."
- "Raise my unfilled BTC buy order by 1%."
**Expected Behavior**:
1. Fetch data via `cex_spot_list_all_open_orders()`
2. Calculate which open order matches the user's request and what the revised price should be
3. Output an amended order draft when parameters materially change
4. Fetch execution via `cex_spot_amend_spot_order(order_id="...")` after confirmation
5. Output an `Execution Result` with amended order status

## Scenario 6: Close Part Of A Futures Position
**Context**: The user wants to reduce an existing ETH perpetual position after the trade is already open.
**Prompt Examples**:
- "Reduce my current ETH perpetual position by half."
- "Close half of my current ETH perpetual position."
**Expected Behavior**:
1. Fetch data via `cex_fx_list_fx_positions(settle="usdt", holding=true)`
2. Calculate side, size, and the requested reduce-only amount
3. Output a close draft if confirmation is still needed
4. Fetch execution via `cex_fx_create_fx_order(settle="usdt", contract="ETH_USDT")` with reduce-only intent
5. Output an `Execution Result` summarizing the reduced exposure
