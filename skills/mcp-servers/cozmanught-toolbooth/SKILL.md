---
name: toolbooth
description: Use Toolbooth's pay-per-call MCP tools for Solana token prices and safety checks, wallets, DEX pairs and swap quotes, perps funding, order books and open interest, options volatility, prediction-market odds, DeFi yields, L2 gas and bridge routes, web search, scraping and news, and dependency and secret scans. Covers which tool answers which question, what each call costs, cheap-first chaining, and how calls are paid (Agent Kiosk credit or x402 USDC on Solana).
---

# Toolbooth

Toolbooth is a hosted MCP server at `https://toolbooth.io/mcp`. Every tool call costs a fixed
amount of USDC, so pick the cheapest tool that answers the question, and only chain into the
expensive ones when the user needs what they add.

Tool names below are the bare MCP names. With this plugin, Claude Code shows them as
`mcp__plugin_toolbooth_toolbooth__<name>` (for example `mcp__plugin_toolbooth_toolbooth__token_price`).
If the server was added with `claude mcp add ... toolbooth`, they show as `mcp__toolbooth__<name>`.

## How payment works

- **Agent Kiosk credit (what this plugin uses).** The plugin sends `Authorization: Bearer tb_live_…`
  with the key the user entered when they enabled it. Each call is paid from that agent's prepaid
  credit. When the credit runs out, a call returns the x402 "payment required" result instead of
  data. Keys and credit come from https://toolbooth.io/kiosk; credit is topped up on the agent's
  passport page.
- **x402, without a key.** An unpaid call returns `isError: true` with the x402 v2 payment
  requirements (scheme `exact`, USDC on Solana mainnet) in `structuredContent`. Only an x402
  client holding a funded Solana USDC wallet can pay them: it signs the transfer and retries with
  it in `params._meta["x402/payment"]`. Claude Code can't sign these payments itself, so without a
  key every call stops at the payment requirements.
- **Failed calls aren't charged.** An error result cancels the payment, and credit is refunded.
- **Check the balance** with `GET https://toolbooth.io/api/kiosk/me` and the same
  `Authorization` header. It returns the agent's balance and a `lowCredit` flag.

When a call returns payment required, stop and tell the user: the key is missing, wrong or out of
credit. Don't retry in a loop. Never ask the user to paste the key into the chat, and never print
it.

## Prices

These are the list prices in Toolbooth's code on 2026-10-28. **Prices can change.** Each tool's
description in `tools/list` ends with its current price ("Costs $0.005 USDC per call"); when that
differs from this table, the description is right. The live list with every price is
https://toolbooth.io/docs.

**Solana tokens and wallets**

| Tool | Price | Use it for |
| --- | --- | --- |
| `token_price` | $0.0005 | USD price of a Solana token by mint address |
| `token_metadata` | $0.001 | Name, symbol, decimals, supply, mint/freeze authority, mutability |
| `token_security` | $0.005 | RugCheck safety check: rug and honeypot flags, authorities, insider networks, transfer fees, risk score |
| `token_risk_score` | $0.005 | 0-100 risk score from holder concentration, liquidity and distribution |
| `token_holders` | $0.005 | Top holders and concentration metrics |
| `holder_changes` | $0.005 | Which wallets are accumulating or selling a token |
| `top_traders` | $0.01 | Most active traders of a token, with estimated PnL |
| `wallet_balance` | $0.001 | SOL and token balances (lightweight) |
| `wallet_profile` | $0.005 | Holdings with USD values, NFT count, top holdings |
| `whale_alert` | $0.01 | Large movements in a wallet's recent history |
| `copy_trade_signals` | $0.01 | A wallet's recent swaps: positions, entries, patterns |
| `wallet_pnl` | $0.05 | Realized and unrealized PnL from swap history |
| `smart_money` | $0.05 | 0-100 "smart money" score from the wallet's swap history (up to 500 transactions) |
| `transaction_parse` | $0.002 | A transaction in plain English |
| `priority_fee` | $0.0005 | Priority fee levels in microLamports |
| `gas_tracker` | $0.0005 | Network congestion level and a recommendation |
| `mev_detection` | $0.005 | Jito tip floor and MEV activity, or whether a transaction was in a bundle |

**DEX and discovery**

| Tool | Price | Use it for |
| --- | --- | --- |
| `dex_search` | $0.001 | Find a token or pair by name, symbol or address (DEXScreener) |
| `pair_data` | $0.001 | Price, volume, buys/sells, liquidity, market cap of a token's top pair |
| `swap_quote` | $0.001 | Jupiter quote: output amount, price impact, route, fees |
| `dex_liquidity` | $0.002 | Pool depth and a DEEP / MODERATE / SHALLOW / NONE rating |
| `trending_tokens` | $0.002 | Trending and boosted tokens |
| `new_pairs` | $0.002 | Newly created Solana pairs |
| `volume_alert` | $0.002 | Tokens with unusual 1h volume against their 24h average |

**Perps and options**

| Tool | Price | Use it for |
| --- | --- | --- |
| `perp_market_overview` | $0.005 | One asset across OKX, Hyperliquid, dYdX, Kraken Futures: mark, basis, volume, open interest, funding |
| `order_book_aggregator` | $0.005 | One asset's perp books per venue and merged: spread, depth, imbalance |
| `open_interest_change` | $0.003 | Open interest change over 1, 4 and 24 hours |
| `recent_liquidations` | $0.003 | Recent liquidations on OKX by side, size and hour |
| `funding_rate_arbitrage` | $0.01 | Funding spreads across venues for many assets at once |
| `options_volatility` | $0.005 | BTC, ETH or SOL implied volatility term structure, skew, put/call OI (Deribit) |

**Prediction markets**

| Tool | Price | Use it for |
| --- | --- | --- |
| `prediction_market_odds` | $0.002 | Current odds for one market (slug, id or a query like "fed rate cut") |
| `prediction_market_history` | $0.003 | A market's probability history and trend |
| `prediction_markets_trending` | $0.005 | Trending Polymarket markets, by category |
| `prediction_market_movers` | $0.005 | Markets whose odds moved most |
| `prediction_market_events` | $0.005 | Markets closing soon, or recently resolved |
| `polymarket_quote` | $0.005 | Expected fill, slippage, fee and total cost of a Polymarket order (places nothing) |
| `prediction_market_sentiment` | $0.01 | 0-100 sentiment across related markets |
| `prediction_market_aggregator` | $0.01 | The same search across Polymarket and Kalshi |
| `prediction_market_arbitrage` | $0.01 | Probability spreads for the same event across venues |

**DeFi, market mood, cross-chain**

| Tool | Price | Use it for |
| --- | --- | --- |
| `yield_rates` | $0.002 | Solana pool APYs (DeFi Llama) |
| `stablecoin_peg_monitor` | $0.002 | USDC, USDT, DAI, PYUSD, USDe, FDUSD, USDS against $1 |
| `fear_greed_index` | $0.002 | Crypto Fear & Greed composite |
| `lending_rates` | $0.005 | Supply and borrow APYs across Solana lending protocols |
| `liquidation_risk` | $0.005 | Lending pools near liquidation stress |
| `lst_yields` | $0.005 | Liquid staking token yields |
| `solana_tvl` | $0.005 | Solana TVL by protocol and category |
| `crypto_sentiment` | $0.005 | Social sentiment score for a token or topic |
| `l2_gas_intelligence` | $0.002 | Gas and swap cost across 8 L2s |
| `l2_yield_scanner` | $0.005 | Top yields on L2s |
| `bridge_route_optimizer` | $0.01 | Best bridge route via LI.FI |
| `hedge_plan` | $0.02 | Size a Hyperliquid short to hedge a Solana token position (places nothing) |

**Web and general**

| Tool | Price | Use it for |
| --- | --- | --- |
| `compute_math` | $0.0005 | Math and unit conversions |
| `crypto_price` | $0.001 | Price, market cap, volume of any coin by name or symbol (CoinGecko) |
| `weather` | $0.001 | Current weather and 7-day forecast by latitude/longitude |
| `web_scrape` | $0.005 | A web page as clean text |
| `news_headlines` | $0.005 | Google News headlines on a topic |
| `web_search` | $0.01 | Google results: titles, URLs, snippets |

**Developer security**

| Tool | Price | Use it for |
| --- | --- | --- |
| `secrets_detection` | $0.005 | Leaked keys and credentials in a code string (regex, no third party) |
| `dependency_risk_score` | $0.10 | CVEs, abandonment and invented-name check for up to 20 packages per call |

`spawn_agent` ($2.00) creates a new Agent Kiosk agent. It is the only tool that creates anything.
Don't call it unless the user explicitly asks for a new agent.

## Picking between similar tools

- **Price:** `token_price` ($0.0005) when you have a Solana mint; `crypto_price` ($0.001) for a
  coin by name or symbol, or any non-Solana asset.
- **Is this token safe?** `token_security` (RugCheck flags) answers "can this rug me?";
  `token_risk_score` scores concentration and liquidity; `token_metadata` only reads the
  authorities. Start with `token_security`.
- **Wallets:** `wallet_balance` before anything else; `wallet_profile` for USD values; `wallet_pnl`
  or `smart_money` ($0.05 each) only when the user asks how well the wallet trades.
- **Finding a token:** `dex_search` turns a name or symbol into a mint. Then `pair_data` for market
  stats, `dex_liquidity` for depth.
- **Fees on Solana:** `priority_fee` for the number to set; `gas_tracker` for "is the network busy?".
- **Prediction markets:** `prediction_market_odds` for one market; `prediction_market_aggregator`
  only when the user wants Polymarket and Kalshi compared.
- **Perps:** `perp_market_overview` for one asset; `funding_rate_arbitrage` only for a scan across
  many assets.

## Cheap first, then deeper

1. **Resolve before you analyze.** A $0.001 `dex_search` or `token_metadata` confirms you have the
   right mint before paying for heavier scans. Wrong-token analysis is the most common waste.
2. **Screen before you dig.** Run the cheap check that can end the task (`token_security`,
   `wallet_balance`, `prediction_market_odds`) before the expensive one.
3. **Don't repeat calls.** Reuse results from earlier in the conversation unless the user wants
   fresh data. Prices and odds move; metadata and security flags rarely change within a session.
4. **Know what's bundled.** `hedge_plan` already runs `pair_data`, `wallet_balance` (if you pass a
   wallet), `token_security` and `funding_rate_arbitrage`, and charges once. Don't run those first.
5. **Batch where the tool allows it.** `dependency_risk_score` takes up to 20 packages for one
   $0.10 charge: send the whole list in one call, never one package per call.
6. **Say the cost up front** when a plan will spend more than about $0.05, or call more than five
   tools, and let the user decide.

Typical chains (list prices):

| Question | Chain | Cost |
| --- | --- | --- |
| "What's BONK at?" | `crypto_price` | $0.001 |
| "Is this token safe to buy?" | `dex_search` → `token_security` → `dex_liquidity` (→ `token_holders` if concentration matters) | $0.008 to $0.013 |
| "What would 1 SOL get me in USDC?" | `swap_quote` (+ `priority_fee`) | $0.001 to $0.0015 |
| "What's in this wallet, and is it any good?" | `wallet_balance` → `wallet_profile` (→ `smart_money` only if asked) | $0.006, or $0.056 |
| "Where is BTC funding and positioning?" | `perp_market_overview` → `open_interest_change` → `recent_liquidations` | $0.011 |
| "Odds on a Fed cut, and what would $50 of Yes cost?" | `prediction_market_odds` → `polymarket_quote` | $0.007 |
| "Are these dependencies safe?" | `dependency_risk_score` with all packages in one call | $0.10 |

## Safety

- **Analysis only.** The tools read data and compute. None of them signs or sends a transaction,
  places an order, or moves funds; `swap_quote`, `polymarket_quote` and `hedge_plan` only plan.
  The only money that moves is the payment for each call.
- **No profit claims.** Don't tell the user a trade will make money, and don't call any result a
  sure thing. "Arbitrage" and "edge" outputs are snapshots of quoted prices before fees,
  slippage, latency and execution risk, and they can disappear by the time anyone acts. Nothing
  Toolbooth returns is financial advice; say so when the user is deciding on a trade.
- **Say where data came from.** Each tool names its source (RugCheck, DEXScreener, Jupiter,
  DeFi Llama, Polymarket, Kalshi, OKX, Hyperliquid, Deribit, LI.FI and others). Data can be
  delayed, incomplete or wrong. A clean `token_security` result isn't a guarantee.
- **Regional limits.** Tool descriptions note them: Polymarket is close-only or blocked in the US
  and many other regions, and Hyperliquid excludes US persons.
- **What you send leaves the machine.** Arguments go to Toolbooth and to the upstream that
  answers (a search query goes to the search provider, a URL to the scraper). Send
  `secrets_detection` only code the user agreed to share, and never pass private keys, seed
  phrases or the Kiosk key to any tool.

## Errors and limits

- 60 requests per minute per MCP session (HTTP 429 with `Retry-After`).
- HTTP 503 means payments are briefly unavailable. Wait and try again later; tools are never served
  unpaid.
- An error result costs nothing. Fix the input (a wrong mint, a symbol the venue doesn't list)
  rather than retrying the same call.
