# Gate Staking Products — Discover Available Options

Find and compare available staking products on Gate.

## MCP tools and parameters

| Tool | Purpose | Required | Optional |
|------|---------|----------|----------|
| **cex_earn_find_coin** | Find staking products | - | `cointype` |

- Returns all available products if no parameters provided
- Filter by specific coin using the `cointype` parameter

**API response (per-item fields):**

| Field | Type | Description |
|-------|------|-------------|
| pid | integer | Product ID |
| productType | integer | Product type: 0=Certificate, 1=Lock-up, 2=Treasury |
| isDefi | integer | Is DeFi protocol: 0=No, 1=Yes |
| currency | string | Staking coin(s), comma-separated |
| estimateApr | string | Estimated APR |
| minStakeAmount | string | Minimum stake amount |
| maxStakeAmount | string | Maximum stake amount |
| protocolName | string | Protocol name |
| redeemPeriod | string | Redemption period in days |
| exchangeRate | string | Exchange rate — use for **redeemable** in positions: redeemable = mortgage_amount × exchangeRate (match by same pid and currency in cex_earn_asset_list) |
| exchangeRateReserve | string | Reverse exchange rate |
| extraInterest | array | Extra rewards: start_time, end_time, reward_coin, segment_interest (money_min, money_max, money_rate) |
| currencyRewards | array | Reward config per coin: apr, reward_coin, reward_delay_days (-1=pay on redeem), interest_delay_days |

---

## Workflow

1. **Parse parameters**: Extract `cointype` from user query if present (e.g. "BTC staking products" → cointype=BTC).
2. **Call tool**: Call `cex_earn_find_coin` with optional `cointype`. No parameters returns all products.
3. **Key data to extract**: From each item: `pid`, `currency`, `protocolName`, `estimateApr`, `productType`, `redeemPeriod`, `minStakeAmount`, `maxStakeAmount`, `isDefi`, `currencyRewards`. Map productType: 0=Certificate, 1=Lock-up, 2=Treasury.
4. **Format response**: Sort or group by estimateApr/productType; use the Response Template in the matching scenario below.

## Report Template

Use the **Response Template** block from the scenario that matches the user intent (browse all, specific coin, high APY, flexible only). Show protocolName, currency, estimateApr, minStakeAmount, redeemPeriod, productType; include currencyRewards when relevant.

**Number formatting**: 
- For amounts (minStakeAmount, maxStakeAmount): Use 8 decimal places precision with trailing zeros removed
- For rates (estimateApr, apr, exchangeRate): Use 2 decimal places precision with trailing zeros retained (e.g., 5.20%, 12.35%)

---

## Scenario 1: Browse all staking products

**Context**: User wants to explore all available staking options.

**Prompt Examples**:
- "Show staking products"
- "What can I stake?"
- "Stakeable coins"
- "Available staking options"

**Expected Behavior**:
1. Call `cex_earn_find_coin()` without parameters
2. For each item use: `currency`, `protocolName`, `estimateApr`, `productType`, `redeemPeriod`, `minStakeAmount`, `isDefi`
3. Group by productType or estimateApr range
4. Show variety of options

**Response Template**:
```
📈 Available Staking Products

[From API: each item has pid, currency, protocolName, estimateApr, productType, redeemPeriod, minStakeAmount, maxStakeAmount, isDefi, currencyRewards]

High Yield (estimateApr >10%):
- protocolName: ETH DeFi Staking, currency: ETH, estimateApr: 12.30%, productType: 1, redeemPeriod: 0, isDefi: 1
- protocolName: DOT Lock, currency: DOT, estimateApr: 15.00%, productType: 1, redeemPeriod: 30, isDefi: 0
- protocolName: MATIC DeFi, currency: MATIC, estimateApr: 11.50%, productType: 1, isDefi: 1

Stable Returns (estimateApr 5-10%):
- protocolName: BTC Flexible, currency: BTC, estimateApr: 5.20%, productType: 0
- protocolName: USDT DeFi, currency: USDT, estimateApr: 8.50%, isDefi: 1
- protocolName: ETH Staking, currency: ETH, estimateApr: 6.80%, productType: 1

Safe Haven (estimateApr 3-5%):
- protocolName: Gate USD, currency: USDT,USDC, estimateApr: 4.50%, productType: 2
- protocolName: USDC Flexible, currency: USDC, estimateApr: 3.80%, productType: 0

Total: 25 products (use array length)
```

---

## Scenario 2: Find products for specific coin

**Context**: User wants staking options for a particular cryptocurrency.

**Prompt Examples**:
- "Show BTC staking options"
- "ETH staking products"
- "USDT staking products"
- "What can I do with my DOT?"

**Expected Behavior**:
1. Parse coin from request (e.g., "BTC")
2. Call `cex_earn_find_coin(cointype="BTC")`
3. Filter/display items where `currency` contains the coin
4. For each item show: `protocolName`, `pid`, `estimateApr`, `minStakeAmount`, `maxStakeAmount`, `redeemPeriod`, `productType`, `currencyRewards`

**Response Template**:
```
🪙 BTC Staking Options

[API returns array; filter by currency containing BTC]

1. pid: 101, protocolName: BTC Flexible Staking
   - currency: BTC
   - estimateApr: 5.20%
   - minStakeAmount: 0.001, maxStakeAmount: 100
   - redeemPeriod: 0 (instant)
   - productType: 0 (Certificate)

2. pid: 102, protocolName: BTC 30-Day Lock
   - currency: BTC
   - estimateApr: 8.00%
   - minStakeAmount: 0.01, maxStakeAmount: 1000
   - redeemPeriod: 30
   - productType: 1 (Lock-up)

3. pid: 103, protocolName: BTC 90-Day Lock
   - currency: BTC
   - estimateApr: 10.00%
   - minStakeAmount: 0.01, maxStakeAmount: 500
   - redeemPeriod: 90
   - productType: 1 (Lock-up)

currencyRewards (e.g. for pid 101): apr, reward_coin, reward_delay_days, interest_delay_days
Recommendation: productType 0 for liquidity, redeemPeriod 30 for balance
```

---

## Scenario 3: Search high APY products

**Context**: User wants highest yielding products.

**Prompt Examples**:
- "Best staking APY"
- "Highest returns"
- "High yield staking"
- "Top yield products"

**Expected Behavior**:
1. Call `cex_earn_find_coin()`
2. Sort by `estimateApr` descending (parse as number)
3. Show top 5-10 products with `protocolName`, `currency`, `estimateApr`, `redeemPeriod`, `minStakeAmount`, `isDefi`
4. Include risk note (isDefi=1 = medium risk)

**Response Template**:
```
🏆 Highest estimateApr Staking Products

[Sort API array by estimateApr desc]

1. pid: 201, protocolName: DOT 90-Day Lock, currency: DOT
   - estimateApr: 18%
   - redeemPeriod: 90, minStakeAmount: 10
   - productType: 1, isDefi: 0

2. pid: 202, protocolName: ATOM 60-Day Lock, currency: ATOM
   - estimateApr: 16.5%
   - redeemPeriod: 60, minStakeAmount: 5
   - productType: 1, isDefi: 0

3. pid: 203, protocolName: MATIC DeFi, currency: MATIC
   - estimateApr: 12.3%
   - redeemPeriod: 0, minStakeAmount: 100
   - isDefi: 1

4. pid: 204, protocolName: ETH 30-Day Lock, currency: ETH
   - estimateApr: 12%
   - redeemPeriod: 30, minStakeAmount: 0.1
   - productType: 1, isDefi: 0

5. pid: 205, protocolName: USDT DeFi Compound, currency: USDT
   - estimateApr: 8.5%
   - redeemPeriod: 0, minStakeAmount: 10
   - isDefi: 1

Note: Higher estimateApr may mean longer redeemPeriod or isDefi=1
```

---

## Scenario 4: Find flexible products only

**Context**: User needs liquidity and wants no lock period.

**Prompt Examples**:
- "Flexible staking only"
- "No lock staking"
- "Flexible staking"
- "Instant redemption products"

**Expected Behavior**:
1. Call `cex_earn_find_coin()`
2. Filter where `redeemPeriod` is 0 or "0" (no lock)
3. Sort by `estimateApr` desc
4. Display `protocolName`, `currency`, `estimateApr`, `minStakeAmount`

**Response Template**:
```
💧 Flexible Staking Products (redeemPeriod=0)

[Filter API array: redeemPeriod "0" or 0]

1. protocolName: USDT Flexible, currency: USDT
   - estimateApr: 8.5%, minStakeAmount: 1, maxStakeAmount: 1000000

2. protocolName: ETH Flexible, currency: ETH
   - estimateApr: 6.8%, minStakeAmount: 0.01

3. protocolName: BTC Flexible, currency: BTC
   - estimateApr: 5.2%, minStakeAmount: 0.001

4. protocolName: USDC Flexible, currency: USDC
   - estimateApr: 3.8%, minStakeAmount: 1

5. protocolName: DAI Flexible, currency: DAI
   - estimateApr: 3.5%, minStakeAmount: 1

Features: redeemPeriod 0 = instant redemption; currencyRewards for apr/reward_coin
Perfect for: Active traders, uncertain markets
```

---

## Scenario 5: Product sold out

**Context**: User asks about a product that's currently sold out.

**Prompt Examples**:
- "I want to stake in the 20% APY product"
- "High yield BTC staking"

**Expected Behavior**:
1. Call `cex_earn_find_coin()` (or with cointype)
2. If product not in list or no capacity, suggest alternatives from same response using `protocolName`, `currency`, `estimateApr`, `redeemPeriod`
3. Sort alternatives by `estimateApr` desc

**Response Template**:
```
⚠️ Product Status

The product you're interested in is not available or has no capacity.

Alternatives from cex_earn_find_coin (high estimateApr):

1. pid: 201, protocolName: DOT 90-Day Lock
   - currency: DOT, estimateApr: 18%, redeemPeriod: 90, minStakeAmount: 10

2. pid: 202, protocolName: ATOM 60-Day Lock
   - currency: ATOM, estimateApr: 16.5%, redeemPeriod: 60, minStakeAmount: 5

3. pid: 204, protocolName: ETH 30-Day Lock
   - currency: ETH, estimateApr: 12%, redeemPeriod: 30, minStakeAmount: 0.1

Tip: Check back later or try another protocolName/currency from the list.
```

---

## Scenario 6: Compare products by lock period

**Context**: User wants to compare different lock periods for same coin.

**Prompt Examples**:
- "Compare ETH staking periods"
- "BTC lock options"
- "Different lock period comparison"

**Expected Behavior**:
1. Call `cex_earn_find_coin(cointype="ETH")`
2. Group results by `redeemPeriod` (0, 30, 60, 90, etc.)
3. For each group show `protocolName`, `estimateApr`, `currency`, `currencyRewards` (apr)
4. Show redeemPeriod and estimateApr progression

**Response Template**:
```
📊 ETH Staking - redeemPeriod Comparison

[Group API items by redeemPeriod for currency containing ETH]

redeemPeriod 0 (Flexible):
- protocolName: ETH Flexible, currency: ETH
  estimateApr: 6.8%, minStakeAmount: 0.01
  currencyRewards: apr, reward_coin, reward_delay_days, interest_delay_days
  Best for: Liquidity

redeemPeriod 30:
- protocolName: ETH 30-Day Lock, currency: ETH
  estimateApr: 9.5%, minStakeAmount: 0.1
  productType: 1 (Lock-up)

redeemPeriod 60:
- protocolName: ETH 60-Day Lock, currency: ETH
  estimateApr: 11%, minStakeAmount: 0.1

redeemPeriod 90:
- protocolName: ETH 90-Day Lock, currency: ETH
  estimateApr: 12.5%, minStakeAmount: 0.1

Longer redeemPeriod generally higher estimateApr (productType 1).
```

---

## Scenario 7: Check minimum requirements

**Context**: User wants to know minimum amounts needed.

**Prompt Examples**:
- "Minimum staking amounts"
- "How much do I need to stake?"
- "Minimum staking requirements"

**Expected Behavior**:
1. Call `cex_earn_find_coin()`
2. Extract `minStakeAmount`, `currency`, `protocolName` from each item
3. Sort by minStakeAmount (numeric) or group by approximate USD tier
4. Show in user-friendly format

**Response Template**:
```
💰 Minimum Staking Requirements (minStakeAmount)

[From API: minStakeAmount, currency, protocolName per item]

Low minStakeAmount:
- currency: USDT, protocolName: USDT Flexible, minStakeAmount: 1
- currency: MATIC, protocolName: MATIC DeFi, minStakeAmount: 10
- currency: DOT, protocolName: DOT Flexible, minStakeAmount: 0.1

Medium:
- currency: ETH, protocolName: ETH Flexible, minStakeAmount: 0.01
- currency: BTC, protocolName: BTC Flexible, minStakeAmount: 0.001
- currency: SOL, protocolName: SOL Staking, minStakeAmount: 1

Higher:
- currency: BTC, protocolName: BTC 30-Day Lock, minStakeAmount: 0.01, redeemPeriod: 30
- currency: ETH, protocolName: ETH 90-Day Lock, minStakeAmount: 0.1, redeemPeriod: 90

Tip: Filter by currency and compare minStakeAmount / maxStakeAmount.
```

---

## Scenario 8: DeFi vs Traditional comparison

**Context**: User wants to understand DeFi staking options.

**Prompt Examples**:
- "What's DeFi staking?"
- "DeFi vs regular staking"
- "DeFi staking explanation"

**Expected Behavior**:
1. Call `cex_earn_find_coin()`
2. Split by `isDefi`: isDefi=1 (DeFi) vs isDefi=0 (traditional)
3. For each show `protocolName`, `currency`, `estimateApr`, `redeemPeriod`, `currencyRewards`
4. Explain productType (0/1/2) and isDefi

**Response Template**:
```
🔄 DeFi vs Traditional Staking

[Partition API array by isDefi]

DeFi (isDefi: 1):
- protocolName: USDT Compound, currency: USDT
  estimateApr: 8.5%, redeemPeriod: 0
  currencyRewards: apr, reward_coin, reward_delay_days (-1 = on redeem), interest_delay_days
- protocolName: ETH Lido, currency: ETH
  estimateApr: 5.2%, isDefi: 1
  Features: Variable estimateApr, protocol rewards

Traditional (isDefi: 0):
- protocolName: USDT Flexible, currency: USDT
  estimateApr: 8.5%, productType: 0, redeemPeriod: 0
- protocolName: ETH Staking, currency: ETH
  estimateApr: 6.8%, productType: 1
  Features: Gate managed, productType 0=Certificate 1=Lock-up 2=Treasury

Key: productType 0/1/2; isDefi 0=No 1=Yes; currencyRewards for reward details; extraInterest for bonus segments
Recommendation: Mix isDefi 0 and 1 for diversification
```