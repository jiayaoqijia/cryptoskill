# Execution And Guardrails

This file defines the execution-layer rules for the trading copilot.

---

## 1. Supported Execution Products

Only two execution products are supported:

1. **spot**
2. **USDT perpetual futures**

Not supported:

- options
- Alpha trading
- on-chain swap / bridge / DeFi execution
- TP/SL daemon-style auto-monitoring
- fully automated multi-product execution

---

## 2. Market Routing Rules

### 2.1 Route directly to spot

Route to spot when the request clearly implies:

- `buy BTC`
- `sell ETH`
- `spot`
- `buy with 1000U`
- `convert my holdings`

### 2.2 Route directly to futures

Route to USDT perpetual futures when the request clearly implies:

- `long / short`
- `perp / contract / perpetual`
- `leverage`
- `open / close / reverse`

### 2.3 Must clarify first

Ask for clarification if:

- the user only says `trade this move`
- the user only says `place an order for me`
- the request could reasonably mean either spot or futures

In that case ask:

- `Do you want spot or USDT perpetual futures?`

---

### 2.4 Runtime availability and authentication

Apply the shared runtime rules first via [`gate-runtime-rules.md`](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md).

At the execution layer, this skill assumes the runtime exposes the referenced `cex_spot_*` and `cex_fx_*` tools.

If the execution namespace is missing:

1. do not claim execution support
2. do not produce fake execution results
3. remain at analysis-only or draft-only level

If the shared runtime rules still leave the auth gate unresolved:

1. market-data reads may still run
2. draft generation may still run
3. real placement / amend / cancel / account verification must not be claimed as completed
4. follow the shared runtime handling before retrying execution

Never translate missing auth into a fake successful execution.

---

## 2.5 Execution-Layer MCP Mapping

### Spot

| Purpose | MCP Tools |
|---|---|
| account / balances | `cex_spot_get_spot_accounts`, `cex_spot_list_spot_account_book` |
| trading rules | `cex_spot_get_currency`, `cex_spot_get_currency_pair` |
| market data | `cex_spot_get_spot_tickers`, `cex_spot_get_spot_order_book`, `cex_spot_get_spot_candlesticks` |
| order placement | `cex_spot_create_spot_order`, `cex_spot_create_spot_batch_orders` |
| open orders | `cex_spot_list_all_open_orders`, `cex_spot_list_spot_orders` when the pair is already known |
| cancellation | `cex_spot_cancel_spot_order`, `cex_spot_cancel_all_spot_orders`, `cex_spot_cancel_spot_batch_orders` |
| amendment | `cex_spot_amend_spot_order`, `cex_spot_amend_spot_batch_orders` |
| fill verification | `cex_spot_list_spot_my_trades` |
| fee estimation | `cex_wallet_get_wallet_fee`, `cex_spot_get_spot_batch_fee` |

### Futures

| Purpose | MCP Tools |
|---|---|
| contract info | `cex_fx_get_fx_contract` |
| market data / order book | `cex_fx_get_fx_order_book`, `cex_fx_get_fx_tickers` |
| account / position mode | `cex_fx_get_fx_accounts` |
| position query | `cex_fx_list_fx_positions`, `cex_fx_get_fx_dual_position`, `cex_fx_get_fx_position` |
| margin-mode switching | `cex_fx_update_fx_dual_position_cross_mode`, `cex_fx_update_fx_position_cross_mode` |
| leverage update | `cex_fx_update_fx_dual_position_leverage`, `cex_fx_update_fx_position_leverage` |
| order placement | `cex_fx_create_fx_order` |
| order query | `cex_fx_list_fx_orders`, `cex_fx_get_fx_order` |
| cancellation | `cex_fx_cancel_fx_order`, `cex_fx_cancel_all_fx_orders` |
| amendment | `cex_fx_amend_fx_order` |

---

## 3. Order Draft Rules

### 3.1 When an order draft may be produced

All of the following must be true:

1. the target asset is clear
2. the market type is clear
3. the trade direction is clear
4. no hard block has been triggered

### 3.2 Draft must include

#### Spot

- trading pair
- buy / sell
- market / limit
- amount meaning
  - `market buy` = quote amount
  - `market sell` = base amount
- estimated pricing basis
- main risk note (slippage / min order / etc.)

#### Futures

- contract
- long / short
- market / limit
- contracts or converted contract size
- current/target margin mode
- current/target leverage
- core risk note (liquidation / crowding / price deviation)

### 3.3 Draft is not execution

If the user has not explicitly confirmed:

- do not place the real order
- remain at draft level

---

## 4. Strong Confirmation Rules

### 4.1 Actions that always require explicit confirmation

- spot order placement
- futures open
- futures close
- reverse
- batch placement
- batch amend
- batch cancel
- close all

### 4.2 Allowed confirmation phrases

- `confirm`
- `confirm order`
- `proceed`
- `execute`
- `yes, place it`

### 4.3 Confirmation must satisfy

1. it comes in the immediately previous user turn
2. it refers to the latest draft
3. parameters have not changed

If any of the following happens, old confirmation becomes invalid:

- the asset changes
- the direction changes
- the price/size changes
- the conversation shifts to another topic
- multiple candidate drafts were discussed

---

## 5. Spot Execution Rules

### 5.0 Common call order for spot

#### Market / limit buy or sell

1. `cex_spot_get_spot_accounts`
2. `cex_spot_get_currency_pair`
3. when live pricing or book data is needed:
   - `cex_spot_get_spot_tickers`
   - add `cex_spot_get_spot_order_book` if book depth matters
4. produce `Order Draft`
5. wait for user confirmation
6. `cex_spot_create_spot_order`
7. when verification is needed:
   - `cex_spot_list_spot_my_trades`
   - or `cex_spot_get_spot_accounts`

#### Amend / cancel

1. `cex_spot_list_all_open_orders`
   - if the pair is already known, `cex_spot_list_spot_orders(currency_pair="...")` is also valid
2. identify the target order
3. produce amend/cancel draft
4. wait for confirmation
5. call the corresponding amend/cancel tool

#### Batch actions

1. list candidate orders
2. let the user confirm the scope
3. then run batch amend / batch cancel

### 5.1 Supported spot actions

- market buy/sell
- limit buy/sell
- limit logic calculated from conditions
- balance query
- fill query
- amend
- cancel
- batch placement / batch amend / batch cancel (only when explicitly requested)

### 5.2 Do not pretend to support

- TP/SL auto-trigger engines
- persistent background watchers
- hidden multi-step automatic execution in one sentence

### 5.3 Multi-leg spot actions

Examples:

- `buy first, then place a sell order`
- `sell BTC, then buy ETH`

Rules:

1. split into separate legs
2. each leg needs its own draft
3. each leg needs its own confirmation

---

## 6. Futures Execution Rules

### 6.0 Common call order for futures

#### Open position

1. `cex_fx_get_fx_contract`
2. `cex_fx_get_fx_accounts`
3. choose the correct position-query tool based on single vs dual mode
4. if the user explicitly requests leverage or margin-mode changes, apply the corresponding update tools first
5. when price/book data is needed:
   - `cex_fx_get_fx_order_book`
   - `cex_fx_get_fx_tickers`
6. produce `Order Draft`
7. wait for confirmation
8. `cex_fx_create_fx_order`
9. verify the position:
   - `cex_fx_list_fx_positions`
   - or `cex_fx_get_fx_dual_position` / `cex_fx_get_fx_position`

#### Close / reverse

1. query the current position first
2. produce the action draft
3. wait for confirmation
4. `cex_fx_create_fx_order`
5. query again to verify the remaining position

#### Amend / cancel

1. `cex_fx_list_fx_orders`
2. identify the target order
3. produce amend/cancel draft
4. wait for confirmation
5. call `cex_fx_amend_fx_order` or `cex_fx_cancel_fx_order`

### 6.1 Supported futures actions

- open long / open short
- full close / partial close
- reverse
- amend
- cancel

### 6.2 Rules inherited from the futures execution layer

- USDT perpetual only
- if leverage is not specified, keep the current effective leverage
- if margin mode is not specified, keep the current effective mode
- close all, reverse, and batch cancellation always require strong confirmation

### 6.3 Futures should usually add these risk checks

Before opening a futures position, prefer to add one or more of:

- momentum
- liquidation
- funding / basis
- support / resistance

Do not open futures directly after only a broad fundamentals read.

---

## 7. Management Flow Rules

### 7.1 Requests that can enter management flow directly

- `amend that order`
- `cancel that buy order`
- `close half`
- `did that fill?`

### 7.2 Management flow does not need the full research chain

But it still must:

- locate the correct order or position
- make the intended modification explicit
- keep strong confirmation for high-risk actions

---

## 8. Hard Blocks

Must stop execution if:

1. the user asks to skip confirmation
2. the user asks the AI to decide and trade directly
3. the user asks to bypass compliance / risk / safety controls
4. the product is unsupported
5. the trading target is not tradable
6. token risk check indicates critical malicious risk:
   - honeypot
   - extreme malicious tax
   - clearly unsellable / highly malicious contract

When blocked:

- explain the reason
- do not produce an order draft

---

## 9. Soft Blocks

Default to `CAUTION` instead of direct execution when:

- liquidity is poor
- slippage is high
- holdings are highly concentrated
- the contract is not open-source
- a major abnormal move just happened and the direction is unresolved
- funding is extreme
- the asset is newly listed and still in price discovery

In these cases:

1. surface the warning clearly
2. if the user still wants to continue, drafting may proceed
3. confirmation is still mandatory

---

## 10. Unified Output After Execution

### 10.1 Execution Result template

```markdown
## Execution Result

### 1. Action
- {what was executed}

### 2. Status
- {success / failed / not executed}

### 3. Core Numbers
- {price / size / cost / fill status / remaining position}

### 4. Next Actions
- {verify fill / amend / cancel / close / keep watching}
```

### 10.2 If execution did not happen

State clearly whether it was due to:

- missing confirmation
- condition not met
- risk block
- unsupported product
- insufficient balance or minimum-order rule

Do not use vague wording.

---

## 11. Recommended Closed Loops

### 11.1 Spot loop

`analysis -> risk check -> order draft -> confirmation -> spot order -> fill verification`

### 11.2 Futures loop

`analysis -> momentum/liquidation/funding check -> order draft -> confirmation -> futures order -> position verification`

### 11.3 New-coin starter loop

`listing/risk check -> technical/liquidity check -> order draft -> confirmation -> small spot execution`
