---
name: gate-dex-market-mcp
version: "2026.3.14-2"
updated: "2026-03-14"
description: "Gate DEX Market MCP mode detailed skill. Calls through gate-dex MCP server for market data queries. No authentication required for market data operations."
---

# Gate DEX Market - MCP Mode Detailed Skill

> **MCP Mode Exclusive Skill** — Calls market data interfaces through gate-dex MCP Server, **no authentication required**.

> See SKILL.md for MCP detection. This file assumes MCP Server is available. For MCP Server setup instructions, see `setup.md`.

---

## MCP Tool Call Specifications

> **Important**: All MCP tool calls below **do not require `mcp_token` parameter** and can be called directly. This differs from wallet operations that require authentication.

### 1. `dex_market_get_kline` — K-line Data Query

Get K-line chart data for specified tokens, used for technical analysis and price trend viewing.

**Tool Signature**:

```javascript
CallMcpTool(
  server="gate-dex",
  toolName="dex_market_get_kline",
  arguments={
    chain: string,           // Chain identifier
    token_address: string,   // Token contract address
    interval: string,        // K-line period
    limit?: number          // Number of records to return (optional, default 100)
  }
)
```

**Parameter Details**:


| Parameter       | Type   | Required | Description                          | Example Values                                          |
| --------------- | ------ | -------- | ------------------------------------ | ------------------------------------------------------- |
| `chain`         | string | ✓        | Chain identifier                     | `"eth"`, `"bsc"`, `"polygon"`                           |
| `token_address` | string | ✓        | Token contract address (hexadecimal) | `"0xdAC17F958D2ee523a2206206994597C13D831ec7"`          |
| `interval`      | string | ✓        | K-line time interval                 | `"1m"`, `"5m"`, `"15m"`, `"1h"`, `"4h"`, `"1d"`, `"1w"` |
| `limit`         | number | ✗        | Number of K-line records to return   | `50`, `100`, `200` (default 100)                        |


**Call Example**:

```javascript
// Query USDT 1-hour K-line, latest 100 records
CallMcpTool(
  server="gate-dex",
  toolName="dex_market_get_kline",
  arguments={
    chain: "eth",
    token_address: "0xdAC17F958D2ee523a2206206994597C13D831ec7", // USDT
    interval: "1h",
    limit: 100
  }
)
```

**Return Value Structure**:

```json
{
  "success": true,
  "data": [
    {
      "timestamp": 1710388800,      // Timestamp
      "open": "1.0001",            // Open price
      "high": "1.0005",            // High price
      "low": "0.9998",             // Low price
      "close": "1.0003",           // Close price
      "volume": "1234567.89"       // Trading volume
    }
  ]
}
```

### 2. `dex_token_get_coin_info` — Token Information Query

Query token basic information including name, symbol, precision, current price, market cap and other key data.

**Tool Signature**:

```javascript
CallMcpTool(
  server="gate-dex",
  toolName="dex_token_get_coin_info",
  arguments={
    chain: string,           // Chain identifier
    token_address: string    // Token contract address
  }
)
```

**Parameter Details**:


| Parameter       | Type   | Required | Description            | Example Values                                 |
| --------------- | ------ | -------- | ---------------------- | ---------------------------------------------- |
| `chain`         | string | ✓        | Chain identifier       | `"eth"`, `"bsc"`, `"sol"`                      |
| `token_address` | string | ✓        | Token contract address | `"0xA0b86a33E6740955fF2A3532C85c44524e5c9C2F"` |


**Call Example**:

```javascript
// Query token info on ETH chain
CallMcpTool(
  server="gate-dex",
  toolName="dex_token_get_coin_info",
  arguments={
    chain: "eth",
    token_address: "0xA0b86a33E6740955fF2A3532C85c44524e5c9C2F"
  }
)
```

**Return Value Structure**:

```json
{
  "success": true,
  "data": {
    "name": "Gate Token",           // Token full name
    "symbol": "GT",                // Token symbol
    "decimals": 18,                // Precision digits
    "total_supply": "1000000000",  // Total supply
    "circulating_supply": "300000000", // Circulating supply
    "price_usd": "1.25",          // Current USD price
    "market_cap": "375000000",     // Market cap
    "volume_24h": "5000000",       // 24-hour trading volume
    "price_change_24h": "2.5%",    // 24-hour price change
    "logo_url": "https://...",     // Token logo
    "description": "Gate platform token" // Project description
  }
}
```

### 3. `dex_token_ranking` — Token Rankings

Get token ranking data, supports sorting by different dimensions (market cap, trading volume, price change, etc.).

**Tool Signature**:

```javascript
CallMcpTool(
  server="gate-dex",
  toolName="dex_token_ranking",
  arguments={
    chain?: string,      // Chain identifier (optional)
    sort_by?: string,    // Sort method (optional)
    limit?: number       // Return count (optional)
  }
)
```

**Parameter Details**:


| Parameter | Type   | Required | Description                                  | Optional Values/Examples                                                  |
| --------- | ------ | -------- | -------------------------------------------- | ------------------------------------------------------------------------- |
| `chain`   | string | ✗        | Chain identifier, all chains if not provided | `"eth"`, `"bsc"`, `"polygon"`, `"sol"`                                    |
| `sort_by` | string | ✗        | Sort dimension, default by market cap        | `"market_cap"`, `"volume_24h"`, `"price_change_24h"`, `"price_change_7d"` |
| `limit`   | number | ✗        | Return count, default 50                     | `10`, `20`, `50`, `100`                                                   |


**Call Example**:

```javascript
// Get top 20 tokens by market cap on Ethereum
CallMcpTool(
  server="gate-dex",
  toolName="dex_token_ranking",
  arguments={
    chain: "eth",
    sort_by: "market_cap",
    limit: 20
  }
)

// Get top 10 tokens by 24h price change across all chains
CallMcpTool(
  server="gate-dex",
  toolName="dex_token_ranking",
  arguments={
    sort_by: "price_change_24h",
    limit: 10
  }
)
```

**Return Value Structure**:

```json
{
  "success": true,
  "data": [
    {
      "rank": 1,
      "chain": "eth",
      "token_address": "0x...",
      "name": "Ethereum",
      "symbol": "ETH",
      "price_usd": "2000.00",
      "market_cap": "240000000000",
      "volume_24h": "12000000000",
      "price_change_24h": "3.2%",
      "price_change_7d": "-1.5%"
    }
  ]
}
```

### 4. `dex_token_get_risk_info` — Security Risk Audit

Perform security audit on specified tokens, detecting honeypot risks, buy/sell taxes, holder concentration and other risk factors.

**Tool Signature**:

```javascript
CallMcpTool(
  server="gate-dex",
  toolName="dex_token_get_risk_info",
  arguments={
    chain: string,           // Chain identifier
    token_address: string    // Token contract address
  }
)
```

**Parameter Details**:


| Parameter       | Type   | Required | Description            | Example Values                |
| --------------- | ------ | -------- | ---------------------- | ----------------------------- |
| `chain`         | string | ✓        | Chain identifier       | `"eth"`, `"bsc"`, `"polygon"` |
| `token_address` | string | ✓        | Token contract address | `"0x1234..."`                 |


**Call Example**:

```javascript
// Check security risks of a token
CallMcpTool(
  server="gate-dex",
  toolName="dex_token_get_risk_info",
  arguments={
    chain: "bsc",
    token_address: "0x1234567890abcdef1234567890abcdef12345678"
  }
)
```

**Return Value Structure**:

```json
{
  "success": true,
  "data": {
    "risk_level": "LOW",              // Risk level: LOW/MEDIUM/HIGH
    "risk_score": 25,                 // Risk score 0-100
    "checks": {
      "honeypot": {
        "is_honeypot": false,         // Is honeypot
        "buy_tax": "0%",             // Buy tax
        "sell_tax": "5%",            // Sell tax
        "max_sell_amount": "1000000" // Max sell amount
      },
      "ownership": {
        "is_renounced": true,         // Is ownership renounced
        "owner_address": null,        // Owner address
        "can_mint": false            // Can mint new tokens
      },
      "liquidity": {
        "locked_percent": "95%",      // Liquidity lock percentage
        "lock_until": 1735689600,     // Lock expiration timestamp
        "can_remove": false          // Can remove liquidity
      },
      "holder_concentration": {
        "top_10_percent": "15%",      // Top 10 holders percentage
        "holder_count": 5420         // Total holder count
      }
    },
    "warnings": [                     // Risk warnings
      "Sell tax is 5%, higher than average",
      "Low holder count may indicate limited adoption"
    ]
  }
}
```

### 5. `dex_token_list_swap_tokens` — Tradeable Token List

Get list of tradeable tokens supported by the platform, used for swap operations or token selection.

**Tool Signature**:

```javascript
CallMcpTool(
  server="gate-dex",
  toolName="dex_token_list_swap_tokens",
  arguments={
    chain?: string,      // Chain identifier (optional)
    search?: string      // Search keyword (optional)
  }
)
```

**Parameter Details**:


| Parameter | Type   | Required | Description                                                | Example Values                 |
| --------- | ------ | -------- | ---------------------------------------------------------- | ------------------------------ |
| `chain`   | string | ✗        | Chain identifier, returns all chain tokens if not provided | `"eth"`, `"bsc"`, `"polygon"`  |
| `search`  | string | ✗        | Search keyword (name or symbol)                            | `"USDT"`, `"Uniswap"`, `"UNI"` |


**Call Example**:

```javascript
// Get all tradeable tokens on Ethereum
CallMcpTool(
  server="gate-dex",
  toolName="dex_token_list_swap_tokens",
  arguments={
    chain: "eth"
  }
)

// Search for tokens containing "BTC"
CallMcpTool(
  server="gate-dex",
  toolName="dex_token_list_swap_tokens",
  arguments={
    search: "BTC"
  }
)
```

**Return Value Structure**:

```json
{
  "success": true,
  "data": [
    {
      "chain": "eth",
      "token_address": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
      "name": "Tether USD",
      "symbol": "USDT",
      "decimals": 6,
      "logo_url": "https://...",
      "is_verified": true,          // Is verified
      "price_usd": "1.000",
      "volume_24h": "50000000000",
      "liquidity_usd": "800000000" // Liquidity (USD)
    }
  ],
  "total_count": 1250              // Total count
}
```

### 6. `dex_token_list_cross_chain_bridge_tokens` — Cross-chain Bridge Token List

Get list of tokens supported by cross-chain bridges, used for cross-chain transfer operations.

**Tool Signature**:

```javascript
CallMcpTool(
  server="gate-dex",
  toolName="dex_token_list_cross_chain_bridge_tokens",
  arguments={
    src_chain?: string,     // Source chain (optional)
    dest_chain?: string     // Destination chain (optional)
  }
)
```

**Parameter Details**:


| Parameter    | Type   | Required | Description                  | Example Values                |
| ------------ | ------ | -------- | ---------------------------- | ----------------------------- |
| `src_chain`  | string | ✗        | Source chain identifier      | `"eth"`, `"bsc"`, `"polygon"` |
| `dest_chain` | string | ✗        | Destination chain identifier | `"eth"`, `"bsc"`, `"polygon"` |


**Call Example**:

```javascript
// Get cross-chain tokens from Ethereum to BSC
CallMcpTool(
  server="gate-dex",
  toolName="dex_token_list_cross_chain_bridge_tokens",
  arguments={
    src_chain: "eth",
    dest_chain: "bsc"
  }
)

// Get all cross-chain bridge supported tokens
CallMcpTool(
  server="gate-dex",
  toolName="dex_token_list_cross_chain_bridge_tokens",
  arguments={}
)
```

**Return Value Structure**:

```json
{
  "success": true,
  "data": [
    {
      "src_chain": "eth",
      "src_token_address": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
      "dest_chain": "bsc",
      "dest_token_address": "0x55d398326f99059fF775485246999027B3197955",
      "token_name": "Tether USD",
      "token_symbol": "USDT",
      "min_amount": "10",           // Minimum cross-chain amount
      "max_amount": "1000000",     // Maximum cross-chain amount
      "fee_percent": "0.1%",       // Fee percentage
      "estimated_time": "10-30min" // Estimated arrival time
    }
  ]
}
```

---

## Supported Chains


| Chain ID   | Network Name      | Type    | Primary Use                  |
| ---------- | ----------------- | ------- | ---------------------------- |
| `eth`      | Ethereum          | EVM     | DeFi, NFT, Stablecoins       |
| `bsc`      | BNB Smart Chain   | EVM     | Low-fee DeFi, Gaming tokens  |
| `polygon`  | Polygon           | EVM     | Scalability apps, Layer2     |
| `arbitrum` | Arbitrum One      | EVM     | Ethereum Layer2 scaling      |
| `optimism` | Optimism          | EVM     | Ethereum Layer2 scaling      |
| `avax`     | Avalanche C-Chain | EVM     | High-performance DeFi        |
| `base`     | Base              | EVM     | Coinbase Layer2              |
| `sol`      | Solana            | Non-EVM | High-throughput applications |


---

## Common Use Cases

### Scenario 1: Technical Analysis

```javascript
// 1. Get token basic information
CallMcpTool(server="gate-dex", toolName="dex_token_get_coin_info", arguments={
  chain: "eth", token_address: "0x..."
})

// 2. Get K-line data for technical analysis
CallMcpTool(server="gate-dex", toolName="dex_market_get_kline", arguments={
  chain: "eth", token_address: "0x...", interval: "4h", limit: 100
})
```

### Scenario 2: Investment Research

```javascript
// 1. View market rankings
CallMcpTool(server="gate-dex", toolName="dex_token_ranking", arguments={
  chain: "eth", sort_by: "market_cap", limit: 50
})

// 2. Security risk assessment
CallMcpTool(server="gate-dex", toolName="dex_token_get_risk_info", arguments={
  chain: "eth", token_address: "0x..."
})
```

### Scenario 3: Trading Preparation

```javascript
// 1. Search tradeable tokens
CallMcpTool(server="gate-dex", toolName="dex_token_list_swap_tokens", arguments={
  chain: "eth", search: "UNI"
})

// 2. Security check
CallMcpTool(server="gate-dex", toolName="dex_token_get_risk_info", arguments={
  chain: "eth", token_address: "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984"
})
```

---

## Error Handling

### Common Error Types


| Error Code           | Error Message          | Cause                      | Solution                                             |
| -------------------- | ---------------------- | -------------------------- | ---------------------------------------------------- |
| `invalid_chain`      | Unsupported chain: xyz | Invalid chain identifier   | Use supported chain identifiers                      |
| `invalid_address`    | Invalid token address  | Token address format error | Check address format (starts with 0x, 42 characters) |
| `token_not_found`    | Token not found        | Token does not exist       | Confirm correct token address or token is listed     |
| `rate_limited`       | Too many requests      | Request rate too high      | Wait and retry                                       |
| `connection_refused` | Connection refused     | Network connection failed  | Check network connection and server status           |


---

## Data Processing and Display Specifications

### K-line Data Display

```markdown
**ETH/USDT 1-hour K-line** (Latest 24 hours)

Time Range: 2026-03-12 00:00 - 2026-03-12 23:59
Current Price: $2,045.67 (+2.3%)

| Time | Open | High | Low | Close | Volume |
|------|------|------|-----|-------|---------|
| 23:00 | 2040.12 | 2048.90 | 2038.50 | 2045.67 | 1.2M |
| 22:00 | 2035.80 | 2042.15 | 2033.40 | 2040.12 | 0.9M |
...

**Technical Observations**:
- 24h Change: +2.3%
- 24h Volume: 28.5M USDT
- Trend: In upward channel, support at $2,030
```

### Token Information Display

```markdown
**Uniswap (UNI)** - 0x1f9840a85d5af5bf1d1762f925bdaddc4201f984

**Basic Information**:
- Network: Ethereum (ETH)
- Current Price: $6.25 (+3.2% 24h)
- Market Cap: $4.68B (Rank #17)
- Circulating Supply: 749.5M UNI
- Total Supply: 1,000M UNI

**Market Data**:
- 24h Volume: $89.2M
- 24h High: $6.45
- 24h Low: $5.98
- 52w High: $12.88
- 52w Low: $3.12
```

### Security Risk Display

```markdown
**Security Audit Results** - RiskToken (RISK)

**Risk Level: HIGH** (Score: 78/100)

**Key Risks**:
- **Honeypot Risk**: Sell restrictions detected
- **High Buy/Sell Tax**: Buy tax 2%, Sell tax 15%
- **Holder Concentration**: Top 10 addresses hold 65% of tokens
- **Liquidity Risk**: Only 35% liquidity locked

**Detailed Checks**:
- Contract Ownership: Not renounced (possible backdoors)
- Minting Function: Disabled
- Liquidity Lock: 35% locked until 2026-12-31
- Holder Count: 1,247 (relatively low)

**Investment Warning**: This token has multiple high-risk factors. Recommend careful investment and thorough research.
```

---

## Security Rules

1. **Read-only Operations**: All MCP tool calls are query operations, no on-chain writes involved
2. **Objective Data**: Present price, ranking and other data objectively, no investment advice
3. **Risk Warnings**: When displaying security audit results, clearly remind users to judge risks themselves
4. **Privacy Protection**: Do not record or cache users' query history
5. **Minimum Permissions**: Market query tools in MCP mode require no user authentication
6. **Data Accuracy**: Indicate data source and update time when displaying data
7. **Investment Warnings**: Provide clear risk warnings for high-risk tokens

