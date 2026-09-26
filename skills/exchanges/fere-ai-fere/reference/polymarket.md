# Polymarket

Each key-registered agent gets its own Safe. Setup:

```bash
python3 scripts/fere.py poly setup alice    # POST /polymarket/setup
python3 scripts/fere.py poly status alice
```

Setup returns `safe_address`, `deposit_address_evm`, `deposit_address_svm`, and `min_fund_usd` (5). An unfunded order reaches the CLOB and fails `Insufficient Polymarket cash balance`.

The `/polymarket/*` routes accept an `agt_*` bearer and scope the response to that agent. Unauthenticated calls are `401`.

## MCP versus REST

| | MCP (`fere_polymarket_*`) | REST (`/polymarket/*`) |
|---|---|---|
| Who | The signed-in account | One Safe per agent |
| Discovery and live prices | `markets`, `markets_for_event`, `prices`, `whale_data` | None. Use `gamma-api.polymarket.com` and `clob.polymarket.com`. |
| Setup, fund, order, cancel, redeem, withdraw | Yes | Yes |
| Request bodies | Tool schema | No OpenAPI body. The fields below come from 422s. |

| MCP tool | REST |
|---|---|
| `fere_polymarket_setup` | `POST /polymarket/setup`. The MCP tool posts `/setup/v2`, which fails on a fresh agent with `v1 setup not complete`. On a fresh agent use the REST route, or let `fere_polymarket_account` run setup. |
| `fere_polymarket_account` | `GET /polymarket/setup/status`, `/orders/open`, `/activity`, and `GET /v1/holdings`. The MCP tool aggregates these and runs setup when `v2_complete` is false. |
| `fere_polymarket_fund` | `POST /polymarket/fund-safe`. REST `amount` is smallest units (`"10000000"` = $10). The MCP tool takes a decimal string. |
| `fere_polymarket_order` / `_order_cancel` | `POST /polymarket/order` with `{side, price, amount, order_type, token_id}`. Cancel needs one of `order_id`, `market_id`, or `cancel_all: true`. The MCP `mode` field is not the REST body. |
| `fere_polymarket_redeem` | `POST /polymarket/redeem`. Requires `condition_id`. Pass `negative_risk` too. REST does not resolve `event_slug`. |
| `fere_polymarket_withdraw` | `POST /polymarket/withdraw` with `{"amount_usdc":"<decimal>","destination_chain_id":<int>}`. `amount_usdc` is a decimal, not smallest units. `destination_chain_id` is required. MCP names `chain` and `token` are ignored and 422. Lands in the Fere wallet on that chain. |
| `markets`, `markets_for_event`, `prices`, `whale_data` | No REST equivalent. |
| — | `GET /polymarket/meta`, `POST /polymarket/disclaimer/acknowledge`. No MCP tool. |

`fere.py poly` sends the write body as JSON (`--body '…'`). Every write returns HTTP 200 and a `task_id`, then fails in the task. A bad `token_id` is a task error, not an HTTP error. A 502 (`All connection attempts failed`) means retry shortly. It does not mean setup is missing.

Prefer a direct deposit to the setup `deposit_addresses` over `fere_polymarket_fund`.

## Prices

Discovery feeds and the account snapshot are cached and can be an hour stale. Use them to find a market. Call `fere_polymarket_prices` (at most 20 token ids) before deciding or ordering. It is live and uncached.

## Ordering

```jsonc
fere_polymarket_order {
  side: "BUY"|"SELL",
  outcome_token: "YES"|"NO",
  token_id: "…",                  // or event_slug + outcome for multi-outcome events
  price: "0.42",
  order_type: "GTC"|"GTD"|"FOK"|"FAK",
  size: "25",
  amount: "10",
  expiration_seconds: 3600,       // GTD only
  take_profit_price: "0.80"
}
```

- `price` is the worst price you accept, not the fill. Read the fill from `activity`.
- There is no market order. Price inside the book. Do not use 0.01 or 0.99 as a fake market.
- Minimum notional is $5 on BUY. SELL is not pre-checked by Fere. The CLOB still rejects a tiny `shares × price`. Price a few cents inside the bid to exit.
- `size` is shares for GTC/GTD. `amount` on FOK/FAK is USD for BUY and shares for SELL.
- `take_profit_price` is BUY only. It places a GTC SELL after the fill.
- A GTC that crosses the spread fills immediately and does not rest.

## Redeeming

`fere_polymarket_redeem {event_slug, outcome?}` lets the gateway resolve `condition_id` and the neg-risk flag. A raw `condition_id` also needs `negative_risk`. The wrong flag hits the wrong adapter. If redeem times out, check resolution on Gamma or the CLOB (`outcomePrices` is `[1,0]` or `[0,1]`), not a Fere flag, and retry once that is final.

## Holdings

Safe cash is a `pUSD` row on Polygon (`chain_id` 137, `protocol:"Polymarket"`, token `0xC011a7E12a19f7B1f670d46F03B03f3342E82DFB`). Outcome rows carry `condition_id`, `negative_risk`, and `redeemable`. Drop `avgPrice == 0` rows from any leaderboard. They are not real positions.

## Fees

Read `taker_base_fee` on `clob.polymarket.com/markets/{conditionId}` before sizing. `1000` means `0.05 × p × (1−p)` per share. On a sports market that is several percent per leg. `value_usd` in `activity` includes the fee.
