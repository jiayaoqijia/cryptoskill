# Gate Staking Swap — Stake and Redeem (On-Chain Earn)

Execute stake and redeem operations for on-chain earn products using `cex_earn_swap_staking_coin`. **pid is required** for every swap call.

**Mint** is supported as **immediate stake**: when the user asks to mint, follow the **Stake** workflow below and call the swap with **side=0**. Same product selection, amount, and GUSD coin rule (USDT/USDC) as stake.

API reference: [Gate API v4 — On-Chain Earn Swap](https://www.gate.io/docs/developers/apiv4/)

---

## MCP tools

| Tool | Purpose | Required params | Optional params |
|------|---------|------------------|-----------------|
| **cex_earn_swap_staking_coin** | Submit stake or redeem order | `pid` | `amount`, **`side`** (0=stake, 1=redeem), **`coin`** (required for GUSD — see below) |
| **cex_earn_find_coin** | List products (to resolve pid before stake) | - | `cointype` |
| **cex_earn_asset_list** | List positions (to resolve pid before redeem) | - | `coin`, `pid` |

- **pid**: Product ID. **Must be passed on every swap.** Resolve from product list (stake) or position list (redeem).
- **amount**: Stake or redeem amount (string or number as per API).
- **side** (integer): Operation direction. **0** = stake; **1** = redeem. Pass `side=0` for stake, `side=1` for redeem.
- **coin** (GUSD / multi-currency): When the product is GUSD or has `currency` / `mortgage_coin` = `"USDT,USDC"`, **require the user to choose a coin**. Only **USDT** and **USDC** are supported. Pass the user’s choice as the `coin` parameter. Do not call the swap tool until the user has selected one.

---

## Workflow: Stake

1. **Parse user intent**: Extract **coin** and **amount** from the query (e.g. "stake 100 USDT", "stake 0.01 BTC").
2. **Get product list**: Call `cex_earn_find_coin(cointype=<coin>)` to get all products that accept that coin. If the user did not specify a coin, ask for it before proceeding.
3. **Filter by currency**: From the response, keep only items where `currency` includes the user’s coin (e.g. "USDT" or "USDT,USDC").
4. **Zero products**: If no products match, reply: "No staking products found for {coin}. Try another coin or check available products."
5. **GUSD / multi-currency (currency is "USDT,USDC")**: If the chosen product’s `currency` is `"USDT,USDC"` (e.g. Gate USD / GUSD), **do not** assume a coin. Ask the user: "This product accepts USDT or USDC. Which do you want to use: USDT or USDC?" Only **USDT** and **USDC** are allowed. Pass the user’s choice as the **`coin`** parameter to `cex_earn_swap_staking_coin`. Do not call the swap until the user has selected one.
6. **Single protocol (one pid)**: If exactly one product matches, use its `pid`. If that product is GUSD / "USDT,USDC", apply step 5 first to get `coin`. Optionally confirm with the user: "Stake {amount} {coin} in {protocolName} (pid {pid})? APY {estimateApr}, redeem period {redeemPeriod} days." Then call `cex_earn_swap_staking_coin(pid=<pid>, amount=<amount>, side=0, coin=<coin>)` (side=0 for stake; pass `coin` when product is GUSD / USDT,USDC).
7. **Multiple protocols (multiple pids for same coin)**: List each product with `protocolName`, `pid`, `estimateApr`, `redeemPeriod`, `minStakeAmount`. Ask the user to confirm which one, e.g. "Multiple products accept {coin}. Which do you want to stake in? 1) {protocolName} (pid {pid}), APY {estimateApr}; 2) …". Do **not** call the swap tool until the user has chosen a **pid**. If the chosen product has currency "USDT,USDC", then ask for USDT vs USDC and pass `coin`. Then call `cex_earn_swap_staking_coin(pid=<chosen_pid>, amount=<amount>, side=0, coin=<coin> when applicable)` (side=0 for stake).
8. **Validate amount**: If the API or product has `minStakeAmount` / `maxStakeAmount`, validate the user’s amount and inform them if it is below min or above max before calling the swap.
9. **Response**: After a successful swap, confirm in English. **Dynamic-rate products** (exchangeRate ≠ 1 from product): show **exchangeAmount** (what the user receives). Otherwise show amount. Example: "Stake order submitted: you will receive {exchangeAmount} {quote_coin} (staked {amount} {coin}) → product {protocolName} (pid {pid})." or for fixed rate: "Stake order submitted: {amount} {coin} → product {protocolName} (pid {pid})." On API error, surface the error message in English and suggest checking balance or product status.

---

## Workflow: Redeem

1. **Parse user intent**: Extract **coin**, **amount**, and **pid** (if provided). Examples: "redeem 50 USDT", "redeem my ETH", "redeem from pid 64".
2. **pid is required**: The swap tool **must** be called with a **pid**. If the user did not give a pid, resolve it:
   - Call `cex_earn_asset_list(coin=<coin>)` (or no filter if coin unknown) to get positions.
   - If **one** position matches the coin (and amount if applicable), use that position’s `pid`.
   - If **multiple** positions match (same coin, different pids), list them: "You have {coin} in: 1) {protocol_name} (pid {pid}); 2) … Which product do you want to redeem from?" Do **not** call the swap tool until the user has chosen a **pid**.
   - If **no** positions for that coin, reply: "You don't have any staking position for {coin}. Check your positions first."
3. **GUSD / multi-currency (mortgage_coin is "USDT,USDC")**: If the position’s `mortgage_coin` is `"USDT,USDC"` (e.g. Gate USD / GUSD), **require the user to choose a coin**. Ask: "This product uses USDT or USDC. Which do you want to redeem as: USDT or USDC?" Only **USDT** and **USDC** are allowed. Pass the user’s choice as the **`coin`** parameter. Do not call the swap until the user has selected one.
4. **Amount**: If the user said "redeem all" or did not specify amount, use the redeemable amount for that pid (from position: mortgage_amount × exchange rate from `cex_earn_find_coin` for same pid and currency). If the user specified an amount, use it; ensure it does not exceed redeemable.
5. **Call swap**: Call `cex_earn_swap_staking_coin(pid=<pid>, amount=<amount>, side=1, coin=<coin>)` (side=1 for redeem). Pass `coin` when the product is GUSD / "USDT,USDC" (user’s choice).
6. **Response**: After success, confirm in English. For **redeem** always show **amount** (what the user receives). Example: "Redeem order submitted: {amount} {coin} from {protocol_name} (pid {pid})." On error, show the message in English and suggest checking redeemable amount or lock period.

---

## Dynamic-rate display (exchangeRate ≠ 1)

When the product has **exchangeRate ≠ 1** (from `cex_earn_find_coin` for the same pid): in **stake** response data, **amount** = staked base coin quantity, **exchangeAmount** / **exchange_amount** = received quote/reward coin quantity. **Stake confirmation**: show **exchangeAmount** (what the user receives). **Redeem confirmation**: show **amount** (what the user receives).

## Number formatting

- **Amounts**: 8 decimal places precision, trailing zeros removed (e.g. `100`, `0.5`, `1.23456789`).
- **Rates (APY, estimateApr)**: 2 decimal places, trailing zeros retained (e.g. `5.20%`, `12.35%`).

---

## Report template (confirmation before swap)

**Stake — GUSD / multi-currency (ask for USDT or USDC)**
```
This product accepts USDT or USDC. Which do you want to use: USDT or USDC?
(Only USDT and USDC are supported. Your choice will be sent as the coin parameter.)
```

**Stake — single product**
```
Stake: {amount} {coin} → {protocolName} (pid {pid})
APY: {estimateApr}, Redeem period: {redeemPeriod} days, Min: {minStakeAmount} {coin}
Confirm to submit.
```

**Stake — multiple products (ask user to choose)**
```
Multiple products accept {coin}. Please choose one:
1) {protocolName} (pid {pid}) — APY {estimateApr}, redeem period {redeemPeriod} days, min {minStakeAmount}
2) ...
Reply with the number or product name to proceed.
```

**Redeem — GUSD / multi-currency (ask for USDT or USDC)**
```
This product uses USDT or USDC. Which do you want to redeem as: USDT or USDC?
(Only USDT and USDC are supported. Your choice will be sent as the coin parameter.)
```

**Redeem — single position**
```
Redeem: {amount} {coin} from {protocol_name} (pid {pid})
Confirm to submit.
```

**Redeem — multiple positions (ask user to choose)**
```
You have {coin} in multiple products. Which do you want to redeem from?
1) {protocol_name} (pid {pid}) — mortgage_amount: {mortgage_amount}, redeemable: {redeemable}
2) ...
Reply with the number or pid to proceed.
```

---

## Error handling

| Condition | Response |
|-----------|----------|
| No products for coin | "No staking products found for {coin}. Try another coin or browse products." |
| User did not specify coin for stake | "Which coin do you want to stake? (e.g. USDT, BTC)" |
| GUSD / USDT,USDC product and user has not chosen coin | "This product accepts USDT or USDC. Which do you want to use: USDT or USDC?" Do not call swap until user selects one. Only USDT and USDC are supported; pass selection as `coin`. |
| User chose a coin other than USDT or USDC for GUSD | "Only USDT and USDC are supported for this product. Please choose USDT or USDC." |
| User wants to cancel or revoke a redeem | **Do not call any tool.** Reply in English: "Cancelling or revoking a redeem is not supported here; please use the Gate website or app if needed. I can help you query positions or order history." |
| User did not specify amount | "How much do you want to stake / redeem?" |
| Multiple pids for coin, user has not chosen | List options and ask user to confirm which product (stake) or which position (redeem). Do not call swap until pid is determined. |
| No position for coin on redeem | "You don't have any staking position for {coin}." |
| Amount below minStakeAmount | "Amount is below the minimum {minStakeAmount} {coin} for this product." |
| Amount above redeemable | "Redeem amount exceeds your redeemable balance for this product." |
| API error / 401 | "Unable to complete the request. Please check your balance and try again." / "Please log in to complete this action." |

---

## Scenarios

### Scenario 1: Stake (single product for coin)

**Context**: User wants to stake a given amount of a coin, and only one product accepts that coin.

**Prompt examples**
- "Stake 100 USDT"
- "I want to stake 0.01 BTC"
- "Stake 500 USDT in on-chain earn"

**Expected behavior**
1. Extract coin and amount; call `cex_earn_find_coin(cointype=<coin>)`.
2. Filter by currency matching the coin; if exactly one product, get its `pid`.
3. Optionally show a one-line confirmation (protocolName, pid, estimateApr, redeemPeriod).
4. Call `cex_earn_swap_staking_coin(pid, amount, side=0)` (side=0 for stake).
5. Reply with success or error in English.

---

### Scenario 2: Stake (multiple products for coin — user must confirm)

**Context**: User wants to stake a coin that has multiple on-chain earn products (multiple pids).

**Prompt examples**
- "Stake 1000 USDT" (when USDT has e.g. Gate USD and Compound V3)
- "Stake my USDT"

**Expected behavior**
1. Call `cex_earn_find_coin(cointype=USDT)`; filter by currency containing USDT.
2. If more than one product: list each with protocolName, pid, estimateApr, redeemPeriod, minStakeAmount. Ask: "Multiple products accept USDT. Which do you want to stake in? 1) Gate USD (pid 70) … 2) Compound V3 (pid 64) …"
3. Do **not** call `cex_earn_swap_staking_coin` until the user has chosen a pid (by number, name, or pid).
4. After confirmation, call `cex_earn_swap_staking_coin(pid=<chosen_pid>, amount=<amount>, side=0)` (side=0 for stake).
5. Reply with success or error in English.

---

### Scenario 3: Redeem (user specifies pid)

**Context**: User specifies which product (pid) to redeem from.

**Prompt examples**
- "Redeem 50 USDT from pid 70"
- "Redeem all from product 64"

**Expected behavior**
1. Extract pid, coin, and amount (or "all").
2. If amount is "all", get redeemable for that pid (e.g. from `cex_earn_asset_list(pid=70)` and exchange rate from `cex_earn_find_coin`).
3. Call `cex_earn_swap_staking_coin(pid, amount, side=1)` (side=1 for redeem).
4. Reply with success or error in English.

---

### Scenario 4: Redeem (user specifies only coin — resolve pid)

**Context**: User wants to redeem a coin but did not specify pid. Resolve pid from positions.

**Prompt examples**
- "Redeem 100 USDT"
- "Redeem my ETH"
- "Unstake my USDT"

**Expected behavior**
1. Extract coin and amount; call `cex_earn_asset_list(coin=<coin>)`.
2. If one position: use its pid, then call `cex_earn_swap_staking_coin(pid, amount, side=1)` (side=1 for redeem).
3. If multiple positions: list protocol_name and pid for each, ask user to choose, then call swap with chosen pid.
4. If no positions: "You don't have any staking position for {coin}."
5. Reply with success or error in English.

---

### Scenario 5: Redeem (user specifies only coin, multiple positions — must confirm)

**Context**: User has the same coin in more than one product; they must choose which pid to redeem from.

**Expected behavior**
1. Call `cex_earn_asset_list(coin=<coin>)`; get redeemable per position (mortgage_amount × exchange rate from `cex_earn_find_coin`).
2. List: "You have {coin} in: 1) Gate USD (pid 70), redeemable …; 2) Compound V3 (pid 64), redeemable … Which do you want to redeem from?"
3. Do **not** call swap until user selects a pid.
4. Call `cex_earn_swap_staking_coin(pid, amount, side=1)` (side=1 for redeem) and confirm in English.
