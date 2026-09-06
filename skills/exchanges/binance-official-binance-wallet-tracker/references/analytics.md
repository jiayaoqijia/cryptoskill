# Wallet Tracker — 9 Analysis Scenarios

Built-in analysis patterns for `tracker tx query` data. Each scenario defines detection rules, algorithm, and output format.

**Data source**: All scenarios operate on the trade records returned by `baw tracker tx query --json`. Fetch the full dataset first, then apply analysis client-side.

**⚠️ Critical**: `ts` field is in **seconds** (10-digit Unix timestamp), not milliseconds. All time-delta calculations (10min window, <1h round-trip, >72h wake-up) must use seconds. Multiply by 1000 only if converting to JS `Date` objects.

**Common prerequisite**: The A3 API does NOT accept `ca` or `address` as filter parameters. The Skill must fetch all records via `tx query`, then filter by matching `ca` (contract address) or `address` (wallet) to enable single-token or single-address focus scenarios.

---

## 1. Rhythm — per-address trading rhythm

**Purpose**: Profile each address's trading pattern — frequency, buy/sell ratio, average ticket, active hours.

**Algorithm**:
```
Group records by `address`:
  count = total records
  buys = records where tradeSideCategory ∈ {11, 19}
  sells = records where tradeSideCategory ∈ {21, 29}
  mean_usd = mean(txUsdValue)
  active_hours = histogram of ts by hour-of-day
  intervals = sorted diffs between consecutive ts
  median_interval = median(intervals)
```

**Output**:
```
📊 Group Trading Rhythm

Address: {address} ({label})
  Total Trades: {count} | Buy: {buys} | Sell: {sells}
  Mean Amount: ${mean_usd} | Median Interval: {median_interval}min
  Active Hours: {top3_active_hours}
```

---

## 2. Anomaly — Large Order Detection

**Purpose**: Detect abnormally large transactions.

**Detection rule**: `txUsdValue > 3 × mean(txUsdValue for same address) AND txUsdValue > 500`

**Algorithm**:
```
1. Group records by `address`
2. Compute mean(txUsdValue) per address
3. Flag records where txUsdValue > 3 × mean AND txUsdValue > 500
```

**Output**:
```
⚠️ Anomaly Large Order

{ts} | {address} ({label}) | {tradeSide} {tokenName} | ${txUsdValue}
  (Mean ${mean_usd}, {multiplier}×Mean)
```

---

## 3. Co-buy — Consensus Buying

**Purpose**: Detect coordinated buying of the same token within a short window.

**Detection rule**: Same `ca`, ≥3 distinct addresses buying within 10-minute window.

**Algorithm**:
```
1. Filter records: tradeSideCategory ∈ {11, 19} (buys)
2. Group by `ca`
3. For each token, sort buy records by `ts`
4. Sliding window: find any 10-min window (600s) with ≥3 distinct addresses
```

**Output**:
```
🔥 Consensus Buy

{tokenName} ({ca}) | {n}consensus | Window: {window_start} - {window_end}
  Buyers: {addr1} ${v1}, {addr2} ${v2}, {addr3} ${v3}
```

---

## 4. Round-trip — Quick In-and-Out

**Purpose**: Detect addresses that buy and sell the same token within 1 hour.

**Detection rule**: Same `address`, same `ca`, buy followed by sell, time gap < 1h.

**Algorithm**:
```
1. Group records by (address, ca)
2. Sort by `ts`
3. Find pairs where: first is buy (11/19), second is sell (21/29), gap < 3600s (1h)
4. Compute profit = (sellPrice - buyPrice) / buyPrice
```

**Output**:
```
⚡ Round-Trip

{address} ({label}) | {tokenName} ({ca})
  Buy: {buy_ts} @ ${buy_price}
  Sell: {sell_ts} @ ${sell_price}
  Holding: {holding_minutes}min | Profit: {profit_pct}%
```

---

## 5. Rotation — Sector Rotation

**Purpose**: Detect capital flowing from one set of tokens to another across time windows.

**Detection rule**: Compare token top-N by volume between two consecutive time windows.

**Algorithm**:
```
1. Split records into two windows: first half and second half (by ts median)
2. For each window, compute token volume ranking (sum txUsdValue by ca)
3. exiting = top tokens in window1 not in window2 top
4. entering = top tokens in window2 not in window1 top
5. intersection = tokens in both windows' top
```

**Output**:
```
🔄 Sector Rotation

Exiting Tokens: {exiting_tokens} (window1 top but not in window2)
Entering Tokens: {entering_tokens} (window2 top but not in window1)
Persistent Hot: {intersection} (in both windows)
```

---

## 6. First-mover — Pioneer Buying

**Purpose**: Identify the earliest buyer of each token.

**Detection rule**: For each `ca`, find the address with the earliest buy `ts`.

**Algorithm**:
```
1. Filter records: tradeSideCategory ∈ {11, 19} (buys)
2. Group by `ca`
3. For each token, find record with minimum `ts`
4. That address is the first-mover for that token
```

**Output**:
```
🎯 First BuyAddress

{tokenName} ({ca}) | First Buy: {address} ({label}) @ {first_buy_ts}
  Buy Price: ${price} | Current Price: ${current_price}
```

---

## 7. Leader-follower — Follower Delay

**Purpose**: Measure how quickly followers copy the first-mover.

**Detection rule**: After first-mover buys, compute median delay for subsequent buyers.

**Algorithm**:
```
1. For each ca, identify first-mover (scenario 6)
2. Find all subsequent buys for same ca (sorted by ts)
3. Delays = [follower_ts - first_mover_ts for each follower]
4. Median delay = median(delays)
```

**Output**:
```
👥 Leader + Followers

{tokenName} ({ca})
  Leader: {first_mover_address} @ {leader_ts}
  Follower Count: {n_followers}
  Median Follower Delay: {median_delay}min
  Delay Distribution: <5min: {n1} | 5-30min: {n2} | >30min: {n3}
```

---

## 8. Wake-up — Dormant Wallet Activation

**Purpose**: Detect addresses that were inactive for >72h then suddenly trade again.

**Detection rule**: Gap between consecutive transactions for same address > 72h.

**Algorithm**:
```
1. Group records by `address`
2. Sort by `ts`
3. Compute intervals between consecutive records
4. Flag addresses where any interval > 259200s (72h)
5. The record after the gap is the "wake-up" trade
```

**Output**:
```
😴➡️⚡ Wake-Up

{address} ({label})
  Last Trade: {last_ts} ({days_ago}days ago)
  Current Trade: {wake_ts} | {tradeSide} {tokenName} | ${txUsdValue}
  Sleep Days: {sleep_days}
```

---

## 9. Bot-like — Bot Activity Detection

**Purpose**: Detect addresses exhibiting automated trading patterns.

**Detection rule**: Three evidence pieces — low interval variance + high night ratio + low amount dispersion.

**Algorithm**:
```
1. Group records by `address`
2. Compute:
   a. Interval variance: std(intervals) / mean(intervals) — low = bot-like
   b. Night ratio: fraction of trades between 00:00-06:00 UTC — high = bot-like
   c. Amount dispersion: std(txUsdValue) / mean(txUsdValue) — low = bot-like
3. Bot score = (1 if interval_cv < 0.3 else 0) +
              (1 if night_ratio > 0.4 else 0) +
              (1 if amount_cv < 0.5 else 0)
4. If bot_score ≥ 2, flag as bot-like
```

**Output**:
```
🤖 Bot-Like

{address} ({label}) | Bot score: {score}/3
  IntervalCV: {interval_cv} (Low if < 0.3, else Normal)
  Night Ratio: {night_ratio} (High if > 0.4, else Normal)
  AmountCV: {amount_cv} (Low if < 0.5, else Normal)
  Evidence: {evidence_list}
```

---

## Scenario Composition

Multiple scenarios can be combined for comprehensive analysis:

- **4h Comprehensive Summary**: Run rhythm + anomaly + co-buy + rotation on 4h data window
- **Group Profile**: Run rhythm for all addresses → summarize group behavior
- **Token Heat**: Run co-buy + first-mover + leader-follower for a specific token (filter by ca client-side)

### Data Fetching Strategy

Since `tx query` returns all records without pagination, fetch once and apply all scenarios in memory. For large groups, consider filtering by `--trade-side` to reduce dataset size before analysis.
