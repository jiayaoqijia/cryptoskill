# Gate Staking Assets — Query Positions & Balances

Query current staking positions, balances, and rewards on Gate.

## MCP tools and parameters

| Tool | Purpose | Required | Optional |
|------|---------|----------|----------|
| **cex_earn_asset_list** | Query staking positions | - | `coin`, `pid` |

- Returns an **array** of position records (one per product/pid)
- Optional `coin`: filter by mortgage coin; `pid`: filter by product ID
- Each record: `pid`, `mortgage_coin`, `mortgage_amount`, `freeze_amount`, `income_total`, `yesterday_income` / `yesterday_income_multi`, `reward_coins`, `defi_income`, `type`, `protocol_name`, `redeem_amount`, `createStamp`, `updateStamp`
- **type**: 0 = Certificate, 1 = Lock-up, 2 = Treasury (GUSD)
- **Redeemable amount**: **Not** `mortgage_amount` − `freeze_amount`. The actual redeemable = `mortgage_amount` × **exchange rate**. The exchange rate is obtained from **`cex_earn_find_coin`**: for the same coin (currency) and same **pid**, take the product item’s `exchangeRate` (or `exchangeRateReserve` as per API semantics). Use `redeem_amount` from the position response only when the API documents it as the final redeemable value.

**API response (array item fields):**

| Field | Type | Description |
|-------|------|-------------|
| pid | integer | Product ID |
| mortgage_coin | string | Staking coin(s), comma-separated (e.g. "USDT" or "USDT,USDC") |
| mortgage_amount | string | Position amount (staked) |
| freeze_amount | string | Locked/frozen amount |
| income_total | string | Total rewards for this position |
| yesterday_income | string | Yesterday's reward (single coin) |
| yesterday_income_multi | array | Yesterday's reward (multi-coin) |
| reward_coins | array | Reward config: reward_coin, interest_delay_days, reward_delay_days (-1 = on redeem) |
| defi_income | object | DeFi rewards: total = [{ coin, amount }] |
| type | integer | 0=Certificate, 1=Lock-up, 2=Treasury |
| protocol_name | string | e.g. "Gate USD", "Compound V3" |
| redeem_amount | string | Amount available/in redeem |
| createStamp, updateStamp | integer | Timestamps |
| extra_income, move_income | string | Extra / move income |
| status | integer | Status |

---

## Workflow

1. **Parse parameters**: Extract `coin` or `pid` from user query if present (e.g. "USDT position" → coin=USDT).
2. **Call positions**: Call `cex_earn_asset_list` with optional `coin` and/or `pid`. No parameters returns all positions.
3. **Redeemable amount**: For each position item, **do not** use `mortgage_amount` − `freeze_amount`. To get redeemable: call **`cex_earn_find_coin`** (optionally with `cointype` matching the position’s `mortgage_coin`), find the product entry with the same **pid** and matching **currency** (coin). Use that product’s **exchangeRate** (or **exchangeRateReserve** as per API). Then **redeemable** = `mortgage_amount` × that exchange rate. If the API provides `redeem_amount` and it is documented as the final redeemable value, prefer it when present.
4. **Key data to extract**: From each array item: `pid`, `mortgage_coin`, `mortgage_amount`, `freeze_amount`, `income_total`, `yesterday_income` or `yesterday_income_multi`, `protocol_name`, `type`, `reward_coins`, `defi_income`, `redeem_amount`. For redeemable, use the formula above with exchange rate from `cex_earn_find_coin` (same coin + pid).
5. **Format response**: Group by coin or show per-product; use the Response Template in the matching scenario below.

## Report Template

Use the **Response Template** block from the scenario that matches the user intent (all positions, specific coin, portfolio value). Show mortgage_coin, protocol_name, mortgage_amount, freeze_amount, **redeemable** (mortgage_amount × exchange rate from `cex_earn_find_coin` for same coin and pid), income_total, yesterday_income; for DeFi include defi_income and reward_coins.

**Number formatting**: Apply 8 decimal places precision with trailing zeros removed for amounts (mortgage_amount, freeze_amount, income_total, etc.). For exchange rates, use appropriate precision as returned by the API.

---

## Scenario 1: Query all staking positions

**Context**: User wants to see all their staking positions across different coins.

**Prompt Examples**:
- "Show my staking positions"
- "Check my staking assets"
- "What's my staked balance?"
- "Display all staking"

**Expected Behavior**:
1. Call `cex_earn_asset_list()` without parameters
2. Optionally call `cex_earn_find_coin()` to get exchange rates per product (pid + currency)
3. For each position item use: `mortgage_coin`, `mortgage_amount`, `freeze_amount`, `income_total`, `yesterday_income` or `yesterday_income_multi`, `protocol_name`, `type`
4. **Redeemable** = mortgage_amount × exchange rate; exchange rate from `cex_earn_find_coin` entry with same **pid** and matching **currency** (coin). Do not use mortgage_amount − freeze_amount.
5. Display formatted position summary

**Response Template**:
```
📊 Staking Positions

[Per position from API array — mortgage_coin, protocol_name, mortgage_amount, freeze_amount, redeemable = mortgage_amount × exchange_rate (exchange_rate from cex_earn_find_coin same pid + currency), income_total, yesterday_income]

Example (2 positions):

Gate USD (pid 70) — mortgage_coin: USDT,USDC
- Staked (mortgage_amount): 990.8323288 USDT
- Locked (freeze_amount): 0
- Redeemable: mortgage_amount × exchange_rate (from cex_earn_find_coin, same pid + currency)
- Total Rewards (income_total): 0.4580822 GUSD
- Yesterday (yesterday_income): 0 GUSD
- Type: Treasury (2)

Compound V3 (pid 64) — mortgage_coin: USDT
- Staked (mortgage_amount): 1 USDT
- Locked (freeze_amount): 0
- Redeemable: mortgage_amount × exchange_rate (from cex_earn_find_coin, same pid + currency)
- Total Rewards (income_total): 0 (rewards in reward_coins)
- Defi Income (defi_income.total): COMP 0.00000762
- Yesterday (yesterday_income_multi): []
- Type: Lock-up (1)
- reward_coins: USDT (paid on redeem), COMP (paid every 15 days)

Total Positions: 2 products
```

---

## Scenario 2: Query specific coin position

**Context**: User wants to check staking position for a specific cryptocurrency.

**Prompt Examples**:
- "Check my BTC staking"
- "Show ETH staking position"
- "Check USDT staking"
- "What's my DOT balance?"

**Expected Behavior**:
1. Parse coin from request (e.g., "USDT")
2. Call `cex_earn_asset_list(coin="USDT")`
3. Response array may contain multiple items where `mortgage_coin` equals or contains the coin
4. For each item use: `pid`, `mortgage_coin`, `mortgage_amount`, `freeze_amount`, `income_total`, `yesterday_income` / `yesterday_income_multi`, `protocol_name`, `type`, `reward_coins`, `defi_income`
5. **Redeemable** = mortgage_amount × exchange rate; get exchange rate from `cex_earn_find_coin` (same pid and matching currency). Do not use mortgage_amount − freeze_amount.
6. Display per-product breakdown

**Response Template**:
```
📊 USDT Staking Position

[API returns array of positions with mortgage_coin containing USDT]

Product 1 — Gate USD (pid 70), mortgage_coin: USDT,USDC
- Staked (mortgage_amount): 990.83232880 USDT
- Locked (freeze_amount): 0
- Redeemable: mortgage_amount × exchange_rate (cex_earn_find_coin, pid 70 + currency)
- Total Rewards (income_total): 0.4580822000 GUSD
- Yesterday (yesterday_income): 0 GUSD
- Type: Treasury (2)

Product 2 — Compound V3 (pid 64), mortgage_coin: USDT
- Staked (mortgage_amount): 1.0000000000 USDT
- Locked (freeze_amount): 0
- Redeemable: mortgage_amount × exchange_rate (cex_earn_find_coin, pid 64 + currency)
- income_total: 0
- defi_income.total: COMP 0.0000076200
- reward_coins: USDT, COMP
- Type: Lock-up (1)

Total: 2 products for USDT
```

---

## Scenario 3: Check available for redemption

**Context**: User wants to know how much they can redeem immediately.

**Prompt Examples**:
- "How much can I unstake?"
- "Available balance check"
- "Redeemable amount"
- "What's unlocked?"

**Expected Behavior**:
1. Call `cex_earn_asset_list()`
2. Call `cex_earn_find_coin()` (or with cointype) to get exchange rate per product (pid + currency)
3. For each array item: **redeemable** = `mortgage_amount` × exchange rate (from find_coin entry with same pid and matching currency). Do not use mortgage_amount − freeze_amount. Use `redeem_amount` only if API documents it as final redeemable.
4. Show `mortgage_coin`, `protocol_name`, redeemable vs locked (`freeze_amount`)
5. If `freeze_amount` > 0, show locked; optionally use `updateStamp` / product rules for unlock time

**Response Template**:
```
💰 Available for Redemption

[Per position: redeemable = mortgage_amount × exchange_rate; exchange_rate from cex_earn_find_coin for same pid + currency]

Gate USD (pid 70) — mortgage_coin: USDT,USDC
- mortgage_amount: 990.83232880 USDT
- freeze_amount: 0
- Redeemable: mortgage_amount × exchange_rate (from find_coin pid 70)
- (show percentage if applicable)

Compound V3 (pid 64) — mortgage_coin: USDT
- mortgage_amount: 1.0000000000 USDT
- freeze_amount: 0
- Redeemable: mortgage_amount × exchange_rate (from find_coin pid 64)

Total Redeemable: (sum of redeemable across positions, in each coin)
```

---

## Scenario 4: Empty positions

**Context**: User queries but has no staking positions.

**Prompt Examples**:
- "Show my staking" (when user has none)

**Expected Behavior**:
1. Call `cex_earn_asset_list()`
2. Receive **empty array** `[]`
3. Suggest available products
4. Guide user to start staking

**Response Template**:
```
No staking positions found.

To start earning:
1. Check available products with "show staking products"
2. Choose a coin and APY that suits you
3. Stake through the Gate interface

Popular options:
- BTC Flexible: 5.2% APY
- ETH Staking: 6.8% APY
- USDT DeFi: 8.5% APY
```

---

## Scenario 5: Position with multiple products

**Context**: User has same coin staked in multiple products.

**Prompt Examples**:
- "Show my USDT staking details"
- "Break down my ETH positions"

**Expected Behavior**:
1. Call `cex_earn_asset_list(coin="USDT")`
2. Response array may have multiple items with `mortgage_coin` containing USDT
3. For each item show: `protocol_name`, `pid`, `mortgage_amount`, `freeze_amount`, `income_total`, `yesterday_income` / `yesterday_income_multi`, `type`, `defi_income` if present
4. **Redeemable** per item = mortgage_amount × exchange rate (from `cex_earn_find_coin` same pid + currency). Do not use mortgage_amount − freeze_amount.
5. Sum mortgage_amount by coin for total

**Response Template**:
```
📊 USDT Staking Breakdown

[API returns array; each element = one product position]

1. Gate USD (pid 70) — type Treasury (2)
   - mortgage_amount: 990.83232880 USDT
   - freeze_amount: 0
   - income_total: 0.4580822000 GUSD
   - yesterday_income: 0

2. Compound V3 (pid 64) — type Lock-up (1)
   - mortgage_amount: 1.0000000000 USDT
   - freeze_amount: 0
   - income_total: 0
   - defi_income.total: COMP 0.0000076200
   - reward_coins: USDT, COMP

Total mortgage_amount (USDT): 991.83232880 USDT
Total income_total / defi_income by product as above
```

---

## Scenario 6: Calculate total portfolio value

**Context**: User wants to know total staking portfolio value.

**Prompt Examples**:
- "Total staking value"
- "Portfolio worth"
- "Total staking value"

**Expected Behavior**:
1. Call `cex_earn_asset_list()`
2. Aggregate by `mortgage_coin`: sum `mortgage_amount` per coin (split by comma if mortgage_coin is "USDT,USDC")
3. Get current prices for each coin (external or from context)
4. Total value = sum(mortgage_amount × price); show income_total / defi_income where relevant

**Response Template**:
```
💼 Staking Portfolio Value

[From API array: group by mortgage_coin, sum mortgage_amount; then convert to USD]

By mortgage_coin (sum of mortgage_amount per coin):
- USDT: 991.83232880 USDT × $1 = $991.83
- USDC: (if in mortgage_coin) …

By product:
- Gate USD (pid 70): 990.83232880 USDT
- Compound V3 (pid 64): 1.0000000000 USDT

Total Portfolio (example): $991.83
Total Rewards (income_total / defi_income): GUSD 0.4580822000, COMP 0.0000076200
```