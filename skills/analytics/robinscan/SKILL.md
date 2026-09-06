---
name: robinscan
description: Query Robinhood Chain blockchain data — look up wallet addresses, transactions, token transfers, tokenized stock prices, and network stats. Use when the user mentions Robinhood Chain, ROH token, on-chain activity, wallet history, tokenized equities (AAPL, TSLA, etc. on-chain), or wants to inspect any blockchain data on chain ID 4663.
---

# Robinhood Chain Explorer

You have access to real-time blockchain data for Robinhood Chain (chain ID 4663) via robinscan.io. Use this to answer any question about on-chain activity, wallet history, token movements, network health, or tokenized stock prices.

## When to use this skill

Trigger this skill when the user:
- Asks about Robinhood Chain, ROH, or chain ID 4663
- Wants to look up a wallet address or its transaction history
- Asks about token transfers, ERC-20/721/1155 activity
- Mentions tokenized stocks (equities issued as on-chain tokens)
- Wants to know gas prices, network stats, or chain health
- Asks to decode transaction logs or event data
- Wants live block data or recent chain activity
- Mentions any address starting with `0x` in the context of Robinhood Chain

## Core knowledge

Robinhood Chain is an EVM-compatible L2 with native tokenized equities. Key facts:
- **Chain ID:** 4663
- **Native currency:** ETH (18 decimals)
- **RPC:** `https://rpc.mainnet.chain.robinhood.com`
- **Explorer:** `https://robinscan.io`
- **Unique feature:** Real-world equities (AAPL, TSLA, NVDA, etc.) are issued as ERC-20 tokens on-chain

All API calls go to `https://robinscan.io`. No authentication required. Responses are JSON.

## API reference

### Network overview

```
GET /api/stats
```

Returns chain-wide metrics. Use this to answer "how is the network doing" or "what's the gas price."

Response fields:
- `coin_price` — ROH price in USD (string)
- `coin_price_change_percentage` — 24h change (number)
- `market_cap` — total market cap (string)
- `gas_prices` — `{ slow, average, fast }` in Gwei (numbers)
- `average_block_time` — milliseconds (number)
- `total_blocks`, `total_addresses`, `total_transactions` — lifetime totals (strings)
- `transactions_today` — today's count (string)

### Activity trend

```
GET /api/stats/chart
```

Returns 14 days of daily transaction counts. Use this to show trends or answer "is the chain getting busier."

Response: array of `{ date: "YYYY-MM-DD", transactions_count: number }`

### Address lookup

```
GET /api/address/{address}/txs?cursor={cursor}
GET /api/address/{address}/counters
```

- `address`: `0x` + 40 hex characters (checksummed or not)
- `cursor`: pagination token from previous response (omit for first page)

The `/txs` endpoint returns top-level transactions (not internal calls). The `/counters` endpoint returns total transaction and token transfer counts — call both to give the user a complete picture.

Transaction fields: `hash`, `blockNumber`, `timestamp`, `from`, `to`, `value` (wei string), `fee` (wei string), `method`, `status` ("ok" | "error")

### Token transfers

```
GET /api/address/{address}/transfers?cursor={cursor}
```

Returns ERC-20/721/1155 transfers involving this address. Use this when the user asks about token movements, DeFi activity, or NFT transfers.

Transfer fields: `txHash`, `logIndex`, `timestamp`, `from`, `to`, `amount`, `decimals`, `token` (with `address_hash`, `symbol`, `name`)

To get transfers for a specific token contract, add `&scope=token`:
```
GET /api/address/{tokenAddress}/transfers?scope=token&cursor={cursor}
```

### Token info

```
GET /api/token/{address}/counters
```

Returns total transfer count for a token contract. Use this to assess token activity level.

### Transaction logs

```
GET /api/tx/{hash}/logs
```

- `hash`: `0x` + 64 hex characters

Returns decoded event logs. Use this to debug failed transactions, understand contract interactions, or trace token movements at the contract level.

Log fields: `block_number`, `data`, `index`, `topics`, `transaction_hash`, `decoded` (with `method_call`, `parameters`), `smart_contract`

### Tokenized stock prices

```
GET /api/stocks/{symbol}/bars?range={range}
```

- `symbol`: uppercase ticker (e.g. `AAPL`, `TSLA`, `NVDA`) — 1-10 characters
- `range`: `1D` | `5D` | `1M` | `6M` | `1Y` (default: `1D`)

Returns historical price bars and current quote. Use this when the user asks about tokenized equity prices or wants a chart.

Response:
- `bars`: array of `{ t: epoch_ms, c: close_price }`
- `quote`: `{ symbol, price, previousClose, changePct }`

Note: Market data requires Alpaca API keys configured on the server. If unavailable, the endpoint returns 503.

### Live blocks

```
GET /api/home/blocks
```

Returns the 12 most recent blocks with their transactions. Use this to show live chain activity or answer "what's happening right now."

Block fields: `number`, `hash`, `timestamp`, `miner`, `gasUsed`, `gasLimit`, `baseFeePerGas`, `transactions` (array with `hash`, `from`, `to`, `value`)

## Pagination

Paginated endpoints return:
```json
{
  "items": [...],
  "next": "base64url-cursor-or-null"
}
```

Pass the `next` value as the `cursor` query parameter to get the next page. When `next` is `null`, you've reached the end.

## Error handling

| Status | Meaning | What to do |
|--------|---------|------------|
| 200 | Success | Process the response |
| 400 | Invalid input | Check address/hash format (must be `0x` + correct hex length) |
| 502 | Backend unavailable | Robinscan.io could not reach its upstream — retry once, then tell the user |

Error responses look like: `{ "error": "error message" }`

## Workflows

### "What's the gas price on Robinhood Chain?"

1. Call `GET /api/stats`
2. Extract `gas_prices.average` (or `.slow` / `.fast` based on user preference)
3. Present as: "Gas is currently X Gwei (slow: Y, fast: Z)"

### "Show me recent activity for this wallet: 0xabc...def"

1. Call `GET /api/address/0xabc...def/counters` for totals
2. Call `GET /api/address/0xabc...def/txs` for recent transactions
3. Summarize: "This wallet has X transactions and Y token transfers. Here are the most recent ones..."

### "How many transfers does USDC have on Robinhood Chain?"

1. Call `GET /api/token/{USDC_ADDRESS}/counters`
2. Present the transfer count
3. If user wants details, call `GET /api/address/{USDC_ADDRESS}/transfers?scope=token`

### "What's the price of tokenized AAPL?"

1. Call `GET /api/stocks/AAPL/bars?range=1D`
2. Extract `quote.price` and `quote.changePct`
3. Present: "AAPL is trading at $X.XX (up/down Y% today)"
4. If user wants history, describe the `bars` array trend

### "Decode the logs on this transaction"

1. Validate hash is `0x` + 64 hex chars
2. Call `GET /api/tx/{hash}/logs`
3. Present each log: emitting contract, event name, decoded parameters
4. Highlight any failed or reverted events

### "What's happening on Robinhood Chain right now?"

1. Call `GET /api/home/blocks`
2. Show the latest blocks with transaction counts
3. Highlight any unusually large transactions or high gas usage

### "Is Robinhood Chain usage growing?"

1. Call `GET /api/stats/chart`
2. Compare recent days to earlier days
3. Present trend: "Transaction volume has increased/decreased over the last 14 days..."

### Investigating a suspicious address

1. Call `/api/address/{addr}/counters` to see activity level
2. Call `/api/address/{addr}/txs` to see transaction patterns
3. Call `/api/address/{addr}/transfers` to see token movements
4. Look for patterns: rapid token movements, interactions with known contracts, unusual gas usage

## Response formatting guidelines

- **Addresses:** Show first 6 + last 4 chars: `0x1234...5678`
- **Transaction hashes:** Show first 8 + last 4: `0x12345678...5678`
- **Values:** Convert wei to ETH (divide by 10^18) for readability
- **Timestamps:** Convert to human-readable dates
- **Token amounts:** Apply decimals (e.g., 1000000 with 6 decimals = 1.0 USDC)
- **Gas:** Always in Gwei (the API returns Gwei directly)
- **Tables:** Use markdown tables for comparing multiple items
