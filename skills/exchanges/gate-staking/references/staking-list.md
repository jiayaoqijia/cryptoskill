# Gate Staking List — Order History & Reward Records

Query staking/redemption order history and reward distribution records.

## MCP tools and parameters

| Tool | Purpose | Required | Optional |
|------|---------|----------|----------|
| **cex_earn_order_list** | Query stake/redeem orders | `status` | `coin`, `pid`, `type`, `page`, `limit` |
| **cex_earn_award_list** | Query reward records | - | `coin`, `pid`, `page` |

- **Order list**: Response has `page`, `pageSize`, `pageCount`, `totalCount`, and `list` (array). Each item in `list`: `pid`, `coin`, `amount`, `type` (0=stake, 1=redeem), `status`, `redeem_stamp`, `createStamp`, `exchange_amount`, `fee`. Filter by `coin`, `pid`, or `type`; use `page` for pagination.
- **Reward list**: Response has `page`, `pageSize`, `pageCount`, `totalCount`, and `list` (array). Each item in `list`: `pid`, `mortgage_coin`, `amount`, `reward_coin`, `interest`, `fee`, `status`, `bonus_date`, `should_bonus_stamp`. Filter by coin or pid; use `page` for pagination.

**cex_earn_order_list response (object):**

| Field | Type | Description |
|-------|------|-------------|
| page | integer | Current page |
| pageSize | integer | Page size |
| pageCount | integer | Total pages |
| totalCount | integer | Total records |
| list | array | Order records |
| list[].pid | integer | Product ID |
| list[].coin | string | Coin |
| list[].amount | string | Amount |
| list[].type | integer | 0=Stake, 1=Redeem |
| list[].status | integer | Status |
| list[].redeem_stamp | integer | Redeem settlement time |
| list[].createStamp | integer | Order time |
| list[].exchange_amount | string | Exchange rate |
| list[].fee | string | Fee |

**cex_earn_award_list response (object):**

| Field | Type | Description |
|-------|------|-------------|
| page | integer | Current page |
| pageSize | integer | Page size |
| pageCount | integer | Total pages |
| totalCount | integer | Total records |
| list | array | Reward records |
| list[].pid | integer | Product ID |
| list[].mortgage_coin | string | Staking coin |
| list[].amount | string | Amount |
| list[].reward_coin | string | Reward coin |
| list[].interest | string | Interest amount |
| list[].fee | string | Fee |
| list[].status | integer | Status |
| list[].bonus_date | string | Date |
| list[].should_bonus_stamp | integer | Expected distribution timestamp |

---

# Part 1: Order List

## Workflow

1. **Parse parameters**: Extract `coin`, `pid`, `type` (0=stake, 1=redeem), `page` from user query.
2. **Call tool**: Call `cex_earn_order_list` with `status="finished"` (required) and optional filters.
3. **Key data to extract**: From response object: `page`, `pageSize`, `pageCount`, `totalCount`. From each `list` item: `pid`, `coin`, `amount`, `type`, `createStamp`, `redeem_stamp`, `status`, `fee`.
4. **Format response**: Show as table or list; convert timestamps to dates; map type 0=Stake, 1=Redeem.

## Report Template

Use the **Response Template** block from the scenario that matches the user intent (all orders, specific coin, stake only, redeem only). Show coin, amount, type (Stake/Redeem), createStamp as date, status; include pagination info.

**Number formatting**: 
- For amounts (amount, fee): Use 8 decimal places precision with trailing zeros removed
- For exchange rates (exchange_amount): Use appropriate precision as returned by the API

---

## Scenario 1: Query all order history

**Context**: User wants to see all staking and redemption history.

**Prompt Examples**:
- "Show staking history"
- "View staking records"
- "View order records"
- "Transaction history"

**Expected Behavior**:
1. Call `cex_earn_order_list(status="finished")`
2. Display recent orders first (already sorted by createStamp desc)
3. Show both stake and redeem orders
4. Include pagination info

**Response Template**:
```
📋 Staking Order History

[From API: page, pageSize, pageCount, totalCount, list[]]

Recent Orders (Page 1 of {pageCount}):

1. {coin} - {type: 0=Stake, 1=Redeem}
   Amount: {amount}
   Date: {createStamp as YYYY-MM-DD HH:mm}
   Status: {status}
   Product: pid {pid}
   {if type=1: Settlement: {redeem_stamp as date}}

2. {coin} - {type}
   Amount: {amount}
   Date: {createStamp}
   ...

Total: {totalCount} orders
Showing: {current range} of {totalCount}
```

---

## Scenario 2: Query specific coin history

**Context**: User wants history for a specific cryptocurrency.

**Prompt Examples**:
- "BTC staking history"
- "Show USDT orders"
- "USDT staking records"
- "ETH transactions"

**Expected Behavior**:
1. Parse coin from request (e.g., "USDT")
2. Call `cex_earn_order_list(status="finished", coin="USDT")`
3. Display filtered results
4. Show stake vs redeem summary

**Response Template**:
```
📋 USDT Order History

[Filtered by coin="USDT"]

Orders (Page {page} of {pageCount}):

1. USDT - Stake
   Amount: {amount}
   Date: {createStamp}
   Product: pid {pid}
   Fee: {fee}

2. USDT - Redeem
   Amount: {amount}
   Date: {createStamp}
   Settlement: {redeem_stamp}

Summary:
- Total Orders: {totalCount}
- Stakes: {count where type=0}
- Redeems: {count where type=1}
```

---

## Scenario 3: Filter by order type

**Context**: User wants only stake or only redeem orders.

**Prompt Examples**:
- "Show only stake orders"
- "Redemption history"
- "Only stake orders"
- "Just redemptions"

**Expected Behavior**:
1. Parse type from request (stake=0, redeem=1)
2. Call `cex_earn_order_list(status="finished", type=0)` or `type=1`
3. Display filtered results
4. Calculate totals

**Response Template**:
```
📋 Stake Orders Only

[Filtered by type=0]

Stake Orders (Page {page} of {pageCount}):

1. {coin} - Stake
   Amount: {amount}
   Date: {createStamp}
   Product: pid {pid}
   Status: {status}

2. {coin} - Stake
   ...

Total Staked: {sum of amounts by coin}
Total Orders: {totalCount}
```

---

## Scenario 4: Recent activity

**Context**: User wants most recent transactions.

**Prompt Examples**:
- "Recent staking activity"
- "Latest orders"
- "Recent staking records"
- "Today's transactions"

**Expected Behavior**:
1. Call `cex_earn_order_list(status="finished", page=1, limit=10)`
2. Focus on first page results
3. Highlight today's orders if any
4. Show time relative to now

**Response Template**:
```
📋 Recent Staking Activity

Latest 10 Orders:

1. {coin} - {type} - {relative time, e.g., "2 hours ago"}
   Amount: {amount}
   Time: {createStamp as HH:mm}
   
2. {coin} - {type} - {relative time}
   Amount: {amount}
   ...

{If any today: "Today: {count} orders"}
{If none today: "No orders today"}
```

---

## Scenario 5: Failed or pending orders

**Context**: User checking order status.

**Prompt Examples**:
- "Pending orders"
- "Failed orders"
- "Order status check"
- "Unfinished orders"

**Expected Behavior**:
1. Note that API requires `status="finished"`
2. Explain only completed orders are shown
3. Suggest checking Gate interface for pending
4. Show recent completed orders

**Response Template**:
```
ℹ️ Order Status

This API only shows completed orders (status="finished").
For pending or failed orders, please check the Gate interface.

Recent Completed Orders:
[Show last 5 completed orders]

All orders shown have been successfully processed.
```

---

# Part 2: Reward List

## Workflow

1. **Parse parameters**: Extract `coin`, `pid`, `page` from user query.
2. **Call tool**: Call `cex_earn_award_list` with optional filters.
3. **Key data to extract**: From response: `page`, `pageSize`, `pageCount`, `totalCount`. From each `list` item: `pid`, `mortgage_coin`, `amount`, `reward_coin`, `interest`, `bonus_date`, `should_bonus_stamp`, `status`.
4. **Format response**: Group by reward_coin; sum interest; show daily/monthly views.

## Report Template

Use the **Response Template** block from the scenario that matches the user intent (all rewards, specific coin, time period, reward summary). Show mortgage_coin, reward_coin, interest, bonus_date; calculate totals.

**Number formatting**: 
- For amounts (amount, interest, fee): Use 8 decimal places precision with trailing zeros removed
- For calculated totals and sums: Use 8 decimal places precision with trailing zeros removed

---

## Scenario 6: Query all rewards

**Context**: User wants to see all staking rewards.

**Prompt Examples**:
- "Show staking rewards"
- "My earnings history"
- "Reward calculation"
- "All rewards"

**Expected Behavior**:
1. Call `cex_earn_award_list()`
2. Group by reward_coin
3. Calculate total earnings
4. Show recent distributions

**Response Template**:
```
💰 Staking Rewards

[From API: page, pageSize, pageCount, totalCount, list[]]

Recent Rewards (Page {page} of {pageCount}):

1. {bonus_date} - {reward_coin}
   Amount: {interest}
   From: {mortgage_coin} (pid {pid})
   Status: {status}

2. {bonus_date} - {reward_coin}
   ...

Summary by Reward Coin:
- {reward_coin}: {sum of interest} total
- {reward_coin}: {sum of interest} total

Total Records: {totalCount}
```

---

## Scenario 7: Specific coin rewards

**Context**: User wants rewards for a specific coin.

**Prompt Examples**:
- "USDT rewards"
- "Show BTC earnings"
- "ETH reward history"
- "USDT earnings"

**Expected Behavior**:
1. Parse coin from request
2. Call `cex_earn_award_list(coin="USDT")`
3. Note this filters by mortgage_coin
4. Calculate totals and averages

**Response Template**:
```
💰 USDT Staking Rewards

[Filtered by mortgage_coin="USDT"]

USDT Rewards (Page {page} of {pageCount}):

1. {bonus_date}
   Reward: {interest} {reward_coin}
   Product: pid {pid}
   
2. {bonus_date}
   Reward: {interest} {reward_coin}
   ...

Summary:
- Total Rewards: {totalCount} distributions
- Reward Coins: {unique reward_coins}
- Total Earned: {sum by each reward_coin}
```

---

## Scenario 8: Yesterday's rewards

**Context**: User checking recent earnings.

**Prompt Examples**:
- "Yesterday's rewards"
- "What did I earn yesterday?"
- "Yesterday's earnings"
- "Recent earnings"

**Expected Behavior**:
1. Call `cex_earn_award_list()`
2. Filter results where bonus_date = yesterday
3. If none, show most recent
4. Calculate daily average

**Response Template**:
```
💰 Yesterday's Rewards

[Filter list where bonus_date = yesterday's date]

{If found:}
Yesterday ({date}):
- {reward_coin}: {sum of interest}
- {reward_coin}: {sum of interest}
Total: {count} distributions

{If none:}
No rewards distributed yesterday.

Recent Rewards:
[Show last 3 days with rewards]

Daily Average: {calculate from recent data}
```

---

## Scenario 9: Reward sources

**Context**: User wants to understand reward origins.

**Prompt Examples**:
- "Where are rewards from?"
- "Reward sources"
- "Which products pay rewards?"
- "Reward breakdown by product"

**Expected Behavior**:
1. Call `cex_earn_award_list()`
2. Group by pid and mortgage_coin
3. Show which products generate which rewards
4. Include reward frequency

**Response Template**:
```
💰 Reward Sources

By Product:

Product {pid} - {mortgage_coin}:
- Pays: {reward_coin}
- Total: {sum of interest}
- Distributions: {count}
- Latest: {most recent bonus_date}

Product {pid} - {mortgage_coin}:
...

Active Products: {unique pid count}
Reward Coins: {unique reward_coins}
```

---

## Scenario 10: Monthly rewards

**Context**: User wants monthly earnings summary.

**Prompt Examples**:
- "Monthly rewards"
- "This month's earnings"
- "Monthly earnings"
- "Month to date rewards"

**Expected Behavior**:
1. Call `cex_earn_award_list()`
2. Filter by current month's bonus_date
3. Group by reward_coin
4. Compare to previous month

**Response Template**:
```
💰 Monthly Rewards - {Month Year}

This Month:
- {reward_coin}: {sum of interest}
- {reward_coin}: {sum of interest}
Total Distributions: {count}

By Week:
- Week 1: {sum}
- Week 2: {sum}
- Week 3: {sum}
- Week 4: {sum}

{If have previous month data:}
vs Last Month: {percentage change}
```

---

## Scenario 11: Verify APY

**Context**: User comparing actual vs advertised returns.

**Prompt Examples**:
- "Verify my APY"
- "Actual vs promised returns"
- "Verify yield rate"
- "Check real APY"

**Expected Behavior**:
1. Call `cex_earn_award_list()` for rewards
2. Call `cex_earn_asset_list()` for positions
3. Calculate actual APY from interest/principal/time
4. Note this requires position data too

**Response Template**:
```
📊 APY Verification

Reward History:
[From award_list]

To calculate actual APY:
1. Total Rewards: {sum of interest by coin}
2. Period: {date range from bonus_dates}
3. Need position amounts from asset_list

Actual APY = (Total Rewards / Principal / Days × 365) × 100%

Note: Complete calculation requires position data.
Would you like to see your current positions?
```

---

## Scenario 12: Empty rewards

**Context**: User has no rewards yet.

**Prompt Examples**:
- "Show my rewards" (when none exist)

**Expected Behavior**:
1. Call `cex_earn_award_list()`
2. Receive empty list or totalCount=0
3. Explain reward timing
4. Suggest checking positions

**Response Template**:
```
No rewards found yet.

Possible reasons:
1. New staking positions - rewards typically start after 24 hours
2. No active staking positions
3. Products may pay on specific schedules

To check your positions: "show staking positions"
To see available products: "show staking products"
```

---

## Scenario 13: Reward types

**Context**: User wants to understand different reward types.

**Prompt Examples**:
- "Explain reward types"
- "Different reward coins"
- "Why different rewards?"
- "Reward type explanation"

**Expected Behavior**:
1. Call `cex_earn_award_list()`
2. Identify unique mortgage_coin → reward_coin pairs
3. Explain common patterns
4. Show examples from user's data

**Response Template**:
```
💡 Reward Types in Your Portfolio

Your Reward Patterns:
[Group by mortgage_coin → reward_coin]

1. {mortgage_coin} → {reward_coin}
   Example: Stake USDT, earn USDT (same coin)
   Total earned: {sum}

2. {mortgage_coin} → {reward_coin}
   Example: Stake USDT, earn GUSD (different coin)
   Total earned: {sum}

Common Types:
- Same coin rewards (BTC → BTC)
- Stable rewards (any → USDT/USDC)
- Platform tokens (any → GT)
- DeFi rewards (any → protocol token)
```

---

## Scenario 14: Pagination handling

**Context**: User has many records and needs to navigate.

**Prompt Examples**:
- "Next page"
- "Show more rewards"
- "Page 2 of orders"
- "All rewards" (when many exist)

**Expected Behavior**:
1. Initial call with page=1
2. Show pagination info clearly
3. Offer to fetch next page
4. Summarize if too many

**Response Template**:
```
📋 Order History - Page {page} of {pageCount}

Showing {start}-{end} of {totalCount} total orders

[List current page items]

Navigation:
- Next page: "show page 2"
- Previous: "show page 1"
- Jump to: "show page 5"

Or view summary: "summarize all orders"
```