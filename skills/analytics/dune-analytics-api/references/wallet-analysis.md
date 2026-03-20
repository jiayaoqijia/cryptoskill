# Wallet Analysis Patterns

## Table of Contents
1. [Wallet Identification](#wallet-identification)
2. [Solana Wallet Queries](#solana-wallet-queries)
3. [EVM Wallet Queries](#evm-wallet-queries)
4. [Multi-chain Aggregation](#multi-chain-aggregation)
5. [Fee Analysis](#fee-analysis)

---

## Wallet Identification

### Common Wallet Router Addresses

Check `dune.lz_web3.dataset_crypto_wallet_router` for known wallet addresses:
```sql
SELECT DISTINCT address, name
FROM dune.lz_web3.dataset_crypto_wallet_router
WHERE name IN ('OKX', 'BinanceWallet', 'Rabby', 'Phantom')
```

### ⚠️ JOIN Type Casting Rule

When joining `dune.lz_web3.dataset_crypto_wallet_router` with other Dune tables (e.g., `dex_aggregator.trades`, `dex.trades`), the `address` column in the router table is `varchar`. **Always cast the address column from the other Dune table to `varchar`**, not the other way around.

```sql
-- ✅ Correct: cast Dune table's address to varchar
WHERE CAST(tx_to AS VARCHAR) IN (
  SELECT address FROM dune.lz_web3.dataset_crypto_wallet_router
)

-- ❌ Wrong: do NOT cast router table's address to varbinary
WHERE tx_to IN (
  SELECT CAST(address AS VARBINARY) FROM dune.lz_web3.dataset_crypto_wallet_router
)
```

**Reason:** The router table stores addresses as `varchar`. Converting `varchar` → `varbinary` can cause silent mismatches due to encoding/checksum differences. Always convert the Dune native table's `varbinary` address → `varchar` instead.

### Identifying by Program/Contract

**Solana:** Check account_keys for known program addresses
```sql
WHERE CONTAINS(account_keys, 'known_program_address')
```

**EVM:** Check tx_to for router contracts
```sql
WHERE tx_to IN (SELECT address FROM wallet_routers)
```

---

## Solana Wallet Queries

### Basic DEX Volume by Wallet
```sql
SELECT
  DATE(block_time) as dt,
  COUNT(DISTINCT tx_id) as tx_count,
  COUNT(DISTINCT trader_id) as active_traders,
  SUM(amount_usd) as volume_usd
FROM dex_solana.trades
WHERE block_date = DATE('{{dt}}')
  AND tx_id IN (
    SELECT id FROM solana.transactions
    WHERE block_date = DATE('{{dt}}')
      AND CONTAINS(account_keys, 'wallet_program_address')
  )
GROUP BY 1
```

### With Token Breakdown
```sql
SELECT
  token_sold_symbol,
  token_bought_symbol,
  CAST(token_sold_mint_address AS VARCHAR) as from_contract,
  CAST(token_bought_mint_address AS VARCHAR) as to_contract,
  COUNT(DISTINCT tx_id) as tx_count,
  SUM(amount_usd) as volume_usd
FROM dex_solana.trades
WHERE block_date = DATE('{{dt}}')
  AND tx_id IN (SELECT tx_id FROM wallet_filtered_txs)
GROUP BY 1, 2, 3, 4
ORDER BY volume_usd DESC
LIMIT 1000
```

### Parsing Order ID from Logs
```sql
WITH wallet_txs AS (
  SELECT
    id as tx_id,
    account_keys[4] as user_address,  -- typical user position
    FILTER(log_messages, x -> x LIKE '%order_id:%') as order_logs
  FROM solana.transactions
  WHERE block_date = DATE('{{dt}}')
    AND CONTAINS(account_keys, 'wallet_program')
)
SELECT
  tx_id,
  user_address,
  REGEXP_EXTRACT(ARRAY_MIN(order_logs), 'order_id: ([0-9]+)', 1) as order_id
FROM wallet_txs
```

---

## EVM Wallet Queries

### Using dex_aggregator.trades (Recommended)
```sql
SELECT
  blockchain,
  COUNT(DISTINCT tx_hash) as tx_count,
  COUNT(DISTINCT tx_from) as active_traders,
  SUM(amount_usd) as volume_usd
FROM dex_aggregator.trades
WHERE block_date = DATE('{{dt}}')
  AND tx_to IN (SELECT address FROM wallet_routers WHERE name = 'WalletName')
GROUP BY 1
```

### Cross-chain Token Breakdown
```sql
SELECT
  blockchain,
  token_sold_symbol,
  token_bought_symbol,
  CAST(token_sold_address AS VARCHAR) as from_contract,
  CAST(token_bought_address AS VARCHAR) as to_contract,
  COUNT(DISTINCT tx_hash) as tx_count,
  SUM(amount_usd) as volume_usd
FROM dex_aggregator.trades
WHERE block_date = DATE('{{dt}}')
  AND tx_to IN (SELECT address FROM wallet_routers)
GROUP BY 1, 2, 3, 4, 5
```

---

## Multi-chain Aggregation

### Union EVM + Solana
```sql
WITH evm_data AS (
  SELECT
    blockchain,
    token_bought_symbol,
    token_sold_symbol,
    CAST(token_bought_address AS VARCHAR) as token_bought_address,
    CAST(token_sold_address AS VARCHAR) as token_sold_address,
    amount_usd,
    CAST(tx_from AS VARCHAR) as user
  FROM dex_aggregator.trades  -- or dex.trades
  WHERE block_date = DATE('{{dt}}')
    AND tx_to IN (SELECT address FROM evm_routers)
),

solana_data AS (
  SELECT
    'solana' AS blockchain,
    token_bought_symbol,
    token_sold_symbol,
    CAST(token_bought_mint_address AS VARCHAR) as token_bought_address,
    CAST(token_sold_mint_address AS VARCHAR) as token_sold_address,
    amount_usd,
    CAST(trader_id AS VARCHAR) as user
  FROM dex_solana.trades
  WHERE block_date = DATE('{{dt}}')
    AND tx_id IN (SELECT tx_id FROM solana_wallet_txs)
),

combined AS (
  SELECT * FROM evm_data
  UNION ALL
  SELECT * FROM solana_data
)

SELECT
  blockchain,
  SUM(amount_usd) as volume_usd,
  COUNT(DISTINCT user) as active_traders
FROM combined
GROUP BY 1
```

---

## Fee Analysis

### Finding Fee Receiver Address
1. Get sample swap transactions from the wallet
2. Look for small percentage transfers (~0.25-0.5%) going to consistent address
3. Verify across multiple chains

### Fee Volume Query
```sql
-- Once fee address is identified
SELECT
  DATE(block_time) as dt,
  blockchain,
  SUM(amount_usd) as fee_volume_usd
FROM dex.trades
WHERE block_date >= DATE('{{start_dt}}')
  AND tx_to = 'fee_receiver_address'
GROUP BY 1, 2
```

### Calculating Fee Rate
```sql
WITH swap_with_fee AS (
  SELECT
    tx_hash,
    SUM(CASE WHEN tx_to = 'router' THEN amount_usd END) as swap_volume,
    SUM(CASE WHEN tx_to = 'fee_address' THEN amount_usd END) as fee_amount
  FROM dex.trades
  WHERE block_date = DATE('{{dt}}')
  GROUP BY 1
)
SELECT
  AVG(fee_amount / NULLIF(swap_volume, 0)) as avg_fee_rate
FROM swap_with_fee
WHERE fee_amount > 0
```

---

## Exclusions & Filters

### Exclude Wash Trading / Bots
```sql
-- Exclude known bot/internal addresses
WHERE trader_id NOT IN (
  'internal_address_1',
  'internal_address_2'
)

-- Exclude unrealistic volumes
AND amount_usd < 10000000  -- 10M cap

-- Exclude specific tokens (wrapped native, etc.)
AND token_bought_mint_address NOT IN (
  'So11111111111111111111111111111111111111112',  -- WSOL
  '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'   -- WETH
)
```
