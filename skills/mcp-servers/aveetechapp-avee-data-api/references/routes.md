# Every /api/v1 route

Base: `https://api.preview.avee.tech/api/v1`. **CU** is the route's `x-avee-cost-cu`; a keyless call spends
CU ÷ 10 units (at least 1) of a 5-per-second budget, so **calls/min** is the keyless pace when you use
only that route. † marks a recently added route that may answer `404 not_found` ("no operation is
served at this path") on a host not yet upgraded.

Path placeholders: `{chain}` is a slug or numeric id, `{address}` a chain-native address.

## Discovery and meta

| Route | CU | Calls/min | Answers |
|---|---|---|---|
| `GET /status` | 0 | 300 | liveness and upstream health |
| `GET /key` | 0 | 300 | plan and limits of the key you send |
| `GET /config` | 10 | 300 | enumerations and defaults |
| `GET /chains` | 10 | 300 | chains served now, head block, lag, DEX names |
| `GET /search` | 30 | 100 | `q` = symbol, ticker or address → `tokens[]` and `pairs[]` |
| `GET /.well-known/x402` | 0 | 300 | payable operations and prices, when x402 is enabled |

## Pairs, trades, candles

| Route | CU | Calls/min | Answers |
|---|---|---|---|
| `GET /pairs` | 30 | 100 | the screener: `chains, q, protocols, dex_names, min/max_liquidity_usd, min/max_apr, min/max_score, min/max_age_seconds, market_type, only_trustable, sort, order, timeframe` |
| `GET /chains/{chain}/pairs/{address}` | 20 | 150 | one pair: tokens, liquidity, fee, APR, score, verdict, windows |
| `GET /chains/{chain}/pairs/{address}/trades` | 40 | 75 | trade tape: `tx_type, maker, from, to, order` |
| `GET /chains/{chain}/pairs/{address}/candles` | 60 | 50 | OHLCV, TradingView arrays: `res`, `from`, `to` (required), `currency=usd|native`; `s: no_data` is a success |
| `POST /pairs/batch` † | 40 | 75 | up to 50 pairs: body `{"items":[{"chain":"robinhood","address":"0x…"}]}` |
| `GET /trending` † | 20 | 150 | trending pairs now |
| `GET /pairs/new` † | 20 | 150 | newest pairs of one `chain`, `min_liquidity_usd`, `max_age_seconds` |
| `GET /launchpads/tokens` † | 20 | 150 | launches of one `chain` by `launch_status=new|bonding|graduated` |

## Tokens and trust

| Route | CU | Calls/min | Answers |
|---|---|---|---|
| `GET /tokens` | 30 | 100 | token market list, by market cap unless `sort` = `volume, liquidity, price_change, created_at, holders, rating, fdv, txns`; `q`, `categories`, ranges |
| `GET /chains/{chain}/tokens/{address}` | 20 | 150 | one token: identity, market roll-up, supply, rating, categories, launch record |
| `GET /tokens/{id}` | 20 | 150 | a registry token by id |
| `GET /tokens/by-slug/{slug}` | 20 | 150 | a registry token by slug |
| `POST /tokens/batch` | 100 | 30 | up to 200 tokens: body `{"items":[{"chain":"…","address":"…"}]}` |
| `GET /chains/{chain}/tokens/{address}/pairs` | 30 | 100 | a token's top pairs by 24h volume |
| `GET /chains/{chain}/tokens/{address}/brief` | 20 | 150 | the safety decision in one call: verdict, score and signals, liquidity with lock and burn, market, holders, deployer, flags |
| `GET /chains/{chain}/tokens/{address}/verdict` | 40 | 75 | the EIP-712 signed verdict alone; never priced under x402 |
| `GET /chains/{chain}/tokens/{address}/proof` | 20 | 150 | Merkle proof of the verdict at the last published epoch; never priced |
| `GET /chains/{chain}/tokens/{address}/holders` † | 40 | 75 | top holders with labels |
| `GET /chains/{chain}/tokens/{address}/traders` † | 40 | 75 | wallets that traded the token, with their PnL on it |
| `GET /deployers/{address}/tokens` † | 40 | 75 | every launch of one deployer, with its reputation card |

## Wallets and boards

| Route | CU | Calls/min | Answers |
|---|---|---|---|
| `GET /wallets` | 50 | 60 | traders ranked on one `chain`: `window, sort, min_win_rate, min_trades, min_human_score, exclude_bots, only_copy_eligible, tiers`; `sort=human_score` ranks long-term people |
| `GET /wallets/stats` | 20 | 150 | trader population per chain |
| `POST /wallets/labels/batch` | 60 | 50 | bot, sniper and scammer labels: body `{"chain":"…","addresses":["…"]}`, up to 200 |
| `GET /wallets/{address}/overview` | 60 | 50 | one wallet across every chain it traded |
| `GET /chains/{chain}/wallets/{address}` | 30 | 100 | trader profile, metrics for every window |
| `GET /chains/{chain}/wallets/{address}/positions` | 40 | 75 | open and closed positions: `state`, `sort` |
| `GET /chains/{chain}/wallets/{address}/trades` | 40 | 75 | raw trade history |
| `GET /chains/{chain}/wallets/{address}/chart` | 30 | 100 | PnL and ROI series over `window` |
| `GET /chains/{chain}/wallets/{address}/best-trades` | 30 | 100 | best and worst closed trades |
| `GET /chains/{chain}/wallets/{address}/rounds` | 40 | 75 | entry and exit cycles, optionally for one `token` |
| `GET /chains/{chain}/wallets/{address}/funding` † | 20 | 150 | who funded the wallet first |
| `GET /leaderboard` | 20 | 150 | `scope=chains`, or `scope=protocols&chain=…` for DEXes and launchpads; `seasonal`, `season` |

Win rate: sorting by `win_rate` ranks only wallets with enough rated positions. A wallet with
`win_rate` 0 but clear winners has too small a sample; read `trade_win_rate` and `rated_positions`.

## Farms, perps, oracle

| Route | CU | Calls/min | Answers |
|---|---|---|---|
| `GET /farms` | 30 | 100 | yield farm screener; `chains` is required |
| `GET /chains/{chain}/farms/{address}` | 20 | 150 | one farm |
| `GET /perps` † | 20 | 150 | perpetual markets with mark, funding and open interest |
| `GET /perps/{market}/history` † | 30 | 100 | OI, funding and mark history; `market` as `pair_address` spells it (`BTC`), `interval=5m|1h` |
| `GET /perps/{market}/stats` † | 10 | 300 | position flow by side over 5m/1h/6h/24h, liquidations, OI a day ago |
| `GET /perps/liquidations` † | 30 | 100 | daily liquidations of one market or a whole venue |
| `GET /prices` † | 10 | 300 | latest avee oracle prices, `ids` = comma-separated feed ids |
| `GET /prices/at` † | 20 | 150 | oracle prices at `ts` (unix seconds) |

For oracle prices at volume, streaming, or a Pyth-compatible shape, use the Astra oracle instead
(the `astra-oracle` skill).
