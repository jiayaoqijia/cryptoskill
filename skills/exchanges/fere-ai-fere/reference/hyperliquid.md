# Hyperliquid — perps and spot

Fere fronts Hyperliquid for both perpetuals (`/v1/perp/*`, 9 ops, MCP `fere_perp_*`)
and USDC-quoted spot (`/v1/spot_hl/*`, 6 ops, MCP `fere_spot_hl_*`). This is the one
venue where the fee model has been measured cell by cell with real fills.

**The HL account is per agent.** `GET /v1/perp/setup` on a wallet registered five
minutes ago returns *its own* `eoa_address`, so a product can give every end user their
own perp and spot account — same as Polymarket, and something no wallet vendor we
compared provisions for you. Verified on fresh agents (2026-09-11/12): the status read,
and that **`POST /v1/perp/setup` on an empty account fails** — the task ends
`FAILURE {"error": "Hyperliquid account requires a Bridge2 deposit before
approveAgent.", "error_code": "HYPERLIQUID_NOT_FUNDED"}`, and it takes **longer than
90 s** to say so (a 90 s poll saw only `TIMEOUT`; 240 s caught it). `GET /v1/perp/setup`
still shows `last_error: null` afterwards, so the status read will not tell you setup
failed — only the task does. We have **not** funded a fresh agent to the $50 floor and
watched it activate, and every HL fill we have was on our own account through MCP.
Status shape (verified 2026-09-09):

```jsonc
{ "setup_complete": false, "account_activated": false, "last_error": null,
  "eoa_address": "0x…",            // this agent's EVM address
  "api_wallet_address": null,      // the HL API signing wallet, once provisioned
  "current_env_agent_name": "FereAI_Prod", "updated_at": null,
  "min_fund_usd": 50.0 }           // ← perps need ~$50 to activate, not $5
```

**Budget $50 per user for perps** (Polymarket's Safe asks $5, spot swaps $5). That floor
is the practical blocker on "give all 500 users a perp account", not the API.

## The flow — fund, and setup happens for you

**One call, not two.** `POST /v1/perp/fund` (≥$50) runs setup itself: its task result
carries a `setup_task_id`, and `account_activated` flipped true 9 s after the deposit
landed. Calling `POST /v1/perp/setup` afterwards is a 3 s idempotent no-op. On an
*unfunded* agent setup still fails with `HYPERLIQUID_NOT_FUNDED`, which is why the
order matters. Timings measured 2026-09-12: fund 19 s, setup 3 s, **withdraw ~5.5 min**
— longer than any sane poll window, so a withdraw `TIMEOUT` is expected; keep the task
id and re-poll it.

### (as originally written)

```
fere_perp_fund   {amount, source_chain_id, source_token?}   # smallest units, from your wallet;
                                      # ≥ $50 (min_fund_usd) — this is a bridge into HL's Bridge2
                                      # and needs no setup (on an empty wallet it fails with the
                                      # swap's "Balance validation failed", not a setup error)
fere_perp_setup                       # signing-wallet provisioning, AFTER the deposit lands
                                      # (HYPERLIQUID_NOT_FUNDED otherwise); {force_rerun:true}
                                      # re-runs it. REST: GET /v1/perp/setup = status, POST = provision
fere_perp_open   {asset:"HYPE", is_buy:false, size:0.17, leverage:3, is_cross:true,
                  order_type:"market"|"limit", limit_price?, tp_price?, sl_price?,
                  reduce_only?, slippage_pct:0.5, idempotency_key?}
fere_perp_orders                      # open orders + TP/SL triggers + mark prices
fere_perp_close  {asset, size?}       # omit size = full close; taker only
fere_perp_orders_cancel {asset, order_id}         # order_id is the venue oid (int)
fere_perp_withdraw {amount_usd, destination_chain_id, destination_token?}
```

Spot is the same shape: `fere_spot_hl_buy {asset, size, tp_price?, sl_price?}`,
`fere_spot_hl_sell {asset, size?}` (omit size = sell all), `fere_spot_hl_tpsl
{asset, tp_price?, sl_price?, size?}`, `fere_spot_hl_orders`. `size` is the **base
token amount**, not USD.

`perp_withdraw` and `spot` sells land back in your Fere wallet — they are not a path
to an external address. There is still no way out to an arbitrary wallet. **Withdraw
minimum is $6** (`"Minimum Hyperliquid withdraw is $6.00 USDC ($1 HL fee + $5 net)"`),
so anything under $6 left on HL is stranded there.

**Every perp and spot write returns HTTP 200 with a `task_id`, then fails in the task**
when it cannot run — no collateral, no position, no setup. Poll the task; the status
code means "queued". Before setup, every one of them (open, close, cancel, spot buy,
sell, tp-sl, spot cancel) fails with the same string: `"Hyperliquid setup not complete
for this agent. Call POST /hyperliquid/setup before placing perp trades."` — **that path
does not exist**; the real one is `POST /v1/perp/setup`. Spot shares the perp setup
and the perp-worded error; there is no separate spot setup.

## Fees — measured live, every cell

| Leg | Taker | Maker |
|---|---|---|
| Perp | **5.50 bps** | 2.50 bps |
| Spot | **7.0 bps buy / 8.0 bps sell** | 4.00 bps |

≈ HL base + ~1 bps Fere builder fee. **Spot is the more expensive taker leg**, so a
maker strategy has to make *both* legs. Round-trip both legs: 26 bps all-taker,
13 bps all-maker.

> **`fee` is denominated in the token you RECEIVED.** A spot buy's fee comes back in
> the base token, so a raw `0.00011899` on HYPE is not 0.11 bps, it is `× $62 = 7.0
> bps`. Convert by `feeToken` or you will misread the cost by 70×. We did.

## Rules learned by losing money

1. **Min order $10.** 0.16 HYPE ($9.99) is rejected; 0.17 fills. The floor also blocks
   fine delta-tuning — you cannot clear a sub-$10 dust residual, so a small net-delta
   remainder is unavoidable at small size.
2. **Perp size decimals vary per asset** (`decimals` in the markets list = szDecimals;
   BTC 5, HYPE 2, AERO **0** — integer contracts only). Size the *other* leg to the
   perp's rounding, not the reverse.
3. **Don't chase maker on entry.** Posting a perp sell ~0.8¢ *above* the ask still
   crossed to taker — the market moved 12¢ during Fere→HL routing latency. Guaranteed
   rest needs a ~0.3–0.5 % buffer, which means sitting one-legged with directional risk
   that dwarfs the maker saving. **Neutralize fast (taker is fine) and take the maker
   win on the exit**, which is fully time-controlled: reduce-only limit (perp), limit
   sell (spot). `fere_perp_close` and a market spot sell are taker-only.
4. **Leg risk is real.** Posting both legs at the touch, the perp crossed to taker while
   the spot rested and filled maker. A production router posts 1+ tick off the touch and
   falls back to taker on the laggard after a timeout.
5. **HL has two sub-balances, and `perp fund` picks the wrong one.** Perp (margin) and
   spot are separate; HL moves between them with a class transfer that Fere does not
   expose. `perp fund` deposits into **perp**, so `spot_hl/*` fails
   `"Insufficient spot balance asset=10107"` — while a *web-app*-funded account holds
   USDC in **spot**, which both buys spot and margins perps (our June carry ran on an
   account with perp balance 0.00). Net: **HL spot is unusable on a key-registered
   agent today**, and the old "perp and spot share one balance" note was describing the
   spot→perp direction only. `perp fund` deposits into
   the *perp* clearinghouse; spot `balances` stays `[]` and `spot_hl/buy` fails with
   `"Insufficient spot balance asset=10107"`. Fere exposes no perp→spot transfer, so the
   spot fee table below applies only to an account that already holds spot USDC (ours did,
   via the web app). Verified 2026-09-12.
   The older note — that spot USDC margins
   perp positions directly, no transfer needed. HL's *public* `clearinghouseState`
   reports them as separate clearinghouses and can show perp `withdrawable: 0` while a
   position uses its isolated view of margin — that is a public-endpoint artifact, not
   your constraint.
6. **Leverage on a hedged position adds no price risk**, only capital efficiency:
   notional (= funding income) is identical at any leverage. 3× *cross* put liquidation
   +438 % away — safer than 1× *isolated*, because cross backs the short with the whole
   balance.
7. **An on-chain spot hedge against an HL perp does not pay.** ~80 bps per side on the
   swap vs ~5 bps on HL; fat alt funding has a ~90-minute half-life (AERO went 79 % →
   11 % in 90 minutes), so the math never closes. If you want carry, do it inside HL or
   across two perp venues.

## Reading markets — the MCP `search` is ignored, the REST `search_text` is not

`fere_perp_markets` and `fere_spot_hl_markets` accept a `search` parameter and **return
the entire universe anyway**: 178 perp tokens (~127 KB) and 309 spot markets (~204 KB),
enough to blow an MCP output cap. Expect the full list and filter it yourself.

**REST is different, and the earlier "search is ignored" note did not hold there:**
`GET /v1/perp/markets?search_text=BTC` returns exactly one row (verified 2026-09-15), so
an empty answer is a real "not indexed", not a dropped filter — which is how P1-18 was
proved. There is no market-detail route: `GET /v1/perp/markets/{asset}` is a 404.

Rows are Codex-shaped `TokenSearchResult`, not an exchange schema:

```jsonc
{ "symbol":"HYPE", "address":"hl:perp:HYPE",   // "hl:spot:HYPE" for spot
  "chainId":999, "decimals":2,                  // decimals = szDecimals
  "priceUSD":84.96, "liquidity":364480221.7,    // liquidity = 24h volume, not book depth
  "name":"Hyperliquid · 10x max",               // max leverage lives in the NAME
  "description":"10x max · Vol $364.48M · 8h fund -0.0011% · OI $23.33M · 24h +1.25%" }
```

**The 178 tokens are the MAIN dex only, and that is also what `perp/open` will
route.** Hyperliquid has 519 markets across 11 dexes; every HIP-3 builder-dex perp
(`xyz:NVDA`, `xyz:GOLD` — i.e. all the tokenised equities and metals) is rejected by
`perp/open` under **five** different spellings with `"Unknown Hyperliquid perp asset:
<name>"`, and each builder dex has **its own perp clearinghouse** (same wallet, same
second: main `accountValue` 96.77, `{"dex":"xyz"}` 0.0) that Fere exposes no
`perpDexClassTransfer` route into. Tested live, funded: `API_FEEDBACK.md` P1-18.
Mark them unroutable in your UI *before* the tap — `reference/consumer-app.md` §6.

**Max leverage and funding are only in those two prose strings** — parse them or read
funding from HL's public API (`metaAndAssetCtxs`, `userFunding` for realized funding,
`clearinghouseState` for positions). HL's public endpoints need no auth and are the
ground truth for anything you plan to trade on; Fere is execution, not a price feed.

## Tolls, fees and dust — measured 2026-09-12

| Step | Cost |
|---|---|
| `perp fund` (Base USDC → HL) | **53–56 bps** bridge — 55.4 on $55 (2026-09-12), 53.4 on $97.35 (2026-09-15). Not a flat rate and not quotable in advance: there is no pre-trade cost endpoint, so show a range |
| `perp withdraw` | **$1 flat, taken out of `amount_usd`**, then **55 bps** on the return bridge — about 97.6 % of what you ask for lands |
| Perp taker | **5.50 bps**, and `builderFee` (1.00 bps) is *inside* that, not on top; `feeToken` is USDC |

A $55 round trip into HL and back costs **~$1.60 before you trade**. Fere's perp task
results carry no fee field at all — pull `userFills` from Hyperliquid's public API.

- **`tp_oids` / `sl_oids` in the open result come back empty even when both brackets are
  resting.** Confirm with `perp orders`. Brackets auto-cancel when you `perp close`.
- **Dust strands.** Withdraw rounds to 2 dp, so $0.004615 stayed on HL — and `/v1/holdings`
  drops the HL row once it falls below display, so Fere's own balance under-reports it.
