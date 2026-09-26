# Hyperliquid

Perps are `/v1/perp/*` (MCP `fere_perp_*`). USDC-quoted spot is `/v1/spot_hl/*` (MCP `fere_spot_hl_*`). The Hyperliquid account is per agent: `GET /v1/perp/setup` returns that agent's `eoa_address`.

```jsonc
{ "setup_complete": false, "account_activated": false, "last_error": null,
  "eoa_address": "0x…",
  "api_wallet_address": null,
  "min_fund_usd": 50.0 }
```

`last_error` stays null after a failed setup. The task is the verdict, not this read. Budget $50 before the account can trade. For comparison, an on-chain swap needs $5 and Polymarket's Safe needs $5.

## Calls

Fund first. `POST /v1/perp/fund` with at least $50 runs setup itself and returns `setup_task_id`. A later `POST /v1/perp/setup` is a no-op. Setup on an empty account fails `HYPERLIQUID_NOT_FUNDED` and can take longer than 90 seconds to say so. Poll past 90 seconds. A withdraw can take several minutes. Keep the task id and re-poll. A timeout is unknown.

```
fere_perp_fund            {amount, source_chain_id, source_token?}   # smallest units, ≥ $50
fere_perp_setup           # only if fund did not already activate the account
fere_perp_open            {asset, is_buy, size, leverage, is_cross, order_type:"market"|"limit", limit_price?, tp_price?, sl_price?, reduce_only?, slippage_pct:0.5}
fere_perp_orders                      # open orders + TP/SL triggers + mark prices
fere_perp_close           {asset, size?}          # omit size = full close, taker only
fere_perp_orders_cancel   {asset, order_id}       # order_id is the venue oid
fere_perp_withdraw        {amount_usd, destination_chain_id, destination_token?}
```

Spot: `fere_spot_hl_buy {asset, size, tp_price?, sl_price?}`, `fere_spot_hl_sell {asset, size?}` (omit size = sell all), `fere_spot_hl_tpsl`, `fere_spot_hl_orders`. `size` is base-token amount, not USD.

Withdrawals and spot sells land in the Fere wallet, not an outside address. Withdraw minimum is $6 (`"Minimum Hyperliquid withdraw is $6.00 USDC ($1 HL fee + $5 net)"`). Less than $6 left on HL is stranded. Withdraw rounds to 2 decimals, so dust below that stays on HL and can disappear from `/v1/holdings`.

Every perp and spot write returns HTTP 200 and a `task_id`, then fails in the task when it cannot run. Before setup, the task error says `Call POST /hyperliquid/setup`. That path does not exist. The real one is `POST /v1/perp/setup`. Spot uses the same setup and the same error string.

`tp_oids` and `sl_oids` on the open result can be empty while both brackets are resting. Confirm with `fere_perp_orders`. `perp close` cancels the brackets.

## Fees

| Leg | Taker | Maker |
|---|---|---|
| Perp | 5.50 bps | 2.50 bps |
| Spot | 7.0 bps buy / 8.0 bps sell | 4.00 bps |

`fee` is denominated in the token received. A spot buy's fee is in the base token. Convert with `feeToken` before you quote bps. Perp task results have no fee field. Read `userFills` from Hyperliquid's public API. Builder fee is inside the perp taker fee, not on top.

`perp fund` from Base USDC costs about 53–56 bps. There is no pre-trade quote. `perp withdraw` takes $1 out of `amount_usd`, then about 55 bps on the return bridge. A $50 deposit can land under $50, so fund at least $60 if the user needs a $10 order afterwards.

## Orders

- Minimum order is $10. Size below that is rejected, and a sub-$10 residual cannot be closed.
- `decimals` on a market row is `szDecimals` (BTC 5, HYPE 2, AERO 0). Round size down to that. Integer markets reject fractional size.
- `fere_perp_close` and a market spot sell are taker-only. A resting order can still cross during routing. Use a taker entry when the position has to exist now.
- Perp margin and spot USDC are separate balances. `perp fund` credits perp. `spot_hl/buy` then fails `Insufficient spot balance`. There is no perp-to-spot transfer. HL spot on a key-registered agent stays empty unless that account already holds spot USDC.
- Hyperliquid's public `clearinghouseState` can show perp `withdrawable: 0` while an isolated position is using margin. That is the public endpoint, not a Fere constraint.

## Markets

MCP `fere_perp_markets` and `fere_spot_hl_markets` accept `search` and still return the full list (about 178 perp tokens, about 309 spot markets). Filter it yourself.

REST honors the filter: `GET /v1/perp/markets?search_text=BTC` returns one row. An empty answer means the asset is not indexed. `GET /v1/perp/markets/{asset}` is 404.

```jsonc
{ "symbol":"HYPE", "address":"hl:perp:HYPE",
  "chainId":999, "decimals":2,
  "priceUSD":84.96, "liquidity":364480221.7,
  "name":"Hyperliquid · 10x max" }
```

`liquidity` is 24h volume, not book depth. Max leverage and funding are only in `name` and `description`. Parse them, or read Hyperliquid's public `metaAndAssetCtxs`. Fere is execution, not a price feed.

The catalogue and `perp/open` are the main dex only. HIP-3 names (`xyz:NVDA`, `xyz:GOLD`, and the other prefixed spellings) fail with `Unknown Hyperliquid perp asset`. Each builder dex has its own clearinghouse, and Fere has no transfer into it. Mark those markets unroutable before the user can tap them. See `reference/consumer-app.md`.
