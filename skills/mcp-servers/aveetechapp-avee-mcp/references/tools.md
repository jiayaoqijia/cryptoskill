# avee MCP tools

Every tool is read-only. The server's `tools/list` is authoritative: a deployment advertises only the
tools whose data source it runs. ◦ marks a tool that is not on every deployment (wallet analytics,
farms, the oracle, and recently added market tools). If it is missing from `tools/list`, use the
fallback given, or the REST API (the `avee-data-api` skill).

Most tools that take one pair, token or wallet need `address` plus `chain` (a name from the enum) or
`chain_id` (a number, which wins when both are given).

## Resolve and discover

| Tool | Use it for |
|---|---|
| `find_asset` | **First call** whenever the user gives a name, symbol or ticker, or an address without a chain. Returns matching tokens and pairs with chain, address and liquidity. |
| `get_chains` | Which chains this server serves, with TVL, volume, scam counts and the DEX names valid for `dex_names`. |
| `get_latest_blocks` | How fresh the data is: the last block indexed per chain. |
| `get_dex_list` | Every indexed DEX deployment with volume, liquidity and pair count. |

## Tokens and safety

| Tool | Use it for |
|---|---|
| `get_token_brief` | **"Is this token safe, and what is it?"** in one call: verdict, score and signals, both liquidity figures with lock and burn, market, holders, deployer history, flags. Prefer it over combining the three below. |
| `get_token_verdict` | Only the signed verdict (`blocked`, `watch`, `ok`, `unknown`), when a signature for on-chain use is needed. |
| `get_token` | Everything held on one token: supply, market roll-up, rating, categories, launch record. |
| `get_token_list` | Token market list: sort by market cap, volume, liquidity, price change, launch time, holders, rating; filter by chain, category, ranges. |
| `get_token_holders` ◦ | Top holders with labels (`token`, `chain`). |
| `get_token_traders` ◦ | Wallets that traded one token, with their PnL on it. |

## Pairs, trades and charts

| Tool | Use it for |
|---|---|
| `get_pair` | One pair in full; `agg_statistics: true` adds the 5m/1h/6h/24h windows. |
| `get_pair_list` | Screener: sort by liquidity, volume, transactions, price change, score, or `popular`/`hottest`/`trending`; filter by chain, DEX, liquidity range, `only_trustable`. |
| `get_trending` ◦ | Trending pairs now. Fallback: `get_pair_list` with `sort_by: trending`. |
| `get_movers` ◦ | Biggest gainers or losers over a window. Fallback: `get_pair_list` with `sort_by: price_change`. |
| `get_new_pairs` ◦ | Newest pairs of one chain. Fallback: `get_pair_list` with `sort_by: created_at`. |
| `get_launchpad_tokens` ◦ | Launchpad pools by stage: `new`, `bonding`, `graduated`. |
| `get_order_book` | A pair's trades and liquidity events, with maker and both legs priced. |
| `get_candles` | OHLCV at 1 minute to 1 month, in the quote token or USD (`price_in_usd`). |

## Deployers and boards

| Tool | Use it for |
|---|---|
| `get_deployer_launches` | One deployer's launches and reputation: how many went bad. |
| `get_deployer_list` | Deployers ranked by reputation, launches or spoiled launches. |
| `get_leaderboard` | `scope: chains` ranks chains; `scope: protocols` with a chain ranks its DEXes and launchpads; `seasonal` for the season board. |

## Wallets ◦

| Tool | Use it for |
|---|---|
| `get_top_wallets` ◦ | Rank traders by PnL, volume, win rate, trades or score; exclude bots and scammers. |
| `get_wallet_overview` ◦ | One wallet across chains over a trailing window. |
| `get_wallet_positions` ◦ | Open or closed positions with cost basis and PnL. |
| `get_wallet_trades` ◦ | Trade history, newest first. |
| `get_wallet_best_trades` ◦ | How a trader made their money: best trades by realized PnL. |
| `get_wallet_pnl_series` ◦ | Daily realized PnL: the equity curve. |
| `get_wallet_position_rounds` ◦ | Entry, exit, hold time and PnL per round trip. |
| `get_wallet_labels` ◦ | Bot, sniper, wash-trader, scammer and copy-eligibility labels for many wallets. |
| `get_wallet_funding` ◦ | Who sent a wallet its first native funds (`address`, `chain`). |
| `get_wallet_stats` ◦ | Trader population per chain: humans versus bots, scammers, daily PnL. |

## Farms, perps, oracle

| Tool | Use it for |
|---|---|
| `get_farm_list` ◦ | Yield farms with TVL, every reward stream with its APR share, the APR (a base–max range when boosted), and whether the contract is verified. |
| `get_perp_markets` ◦ | Perp markets with mark, funding and open interest. Fallback: `get_pair_list` on `hyperliquid`. |
| `get_oracle_prices` ◦ | avee oracle prices by feed id, latest or at `publish_time`. For streaming, use Astra (the `astra-oracle` skill). |

## Resources

`avee://chains` (the chains served) and `avee://reasons` (the verdict reason bits and their labels).
A resource read costs the same as a tool call.
