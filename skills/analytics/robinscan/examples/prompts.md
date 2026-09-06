# Example Prompts

Here are example user prompts and how the skill would handle them:

## 1. Chain Overview
**User:** "What's the current state of Robinhood Chain?"

**Action:** Call `GET /api/stats`
- Extract price, gas, total txs, total addresses
- Format as a summary

## 2. Address Lookup
**User:** "Show me what 0x1234...5678 has been doing on Robinhood Chain"

**Action:** 
1. Call `GET /api/address/0x1234...5678/counters` for totals
2. Call `GET /api/address/0x1234...5678/txs` for recent transactions
3. Summarize activity

## 3. Token Investigation
**User:** "How popular is this token: 0xabcd...ef01?"

**Action:**
1. Call `GET /api/token/0xabcd...ef01/counters` for transfer count
2. Call `GET /api/address/0xabcd...ef01/transfers?scope=token` for recent transfers
3. Summarize usage

## 4. Stock Price Check
**User:** "What's the price of tokenized AAPL?"

**Action:** Call `GET /api/stocks/AAPL/bars?range=1D`
- Return current price and daily change
- Optionally show price trend

## 5. Transaction Debugging
**User:** "Decode the logs on transaction 0x9876...4321"

**Action:** Call `GET /api/tx/0x9876...4321/logs`
- Return decoded event logs with method signatures and parameters

## 6. Network Monitoring
**User:** "What's happening on Robinhood Chain right now?"

**Action:** Call `GET /api/home/blocks`
- Return latest 12 blocks with transactions
- Highlight any interesting activity

## 7. Activity Trend
**User:** "Is Robinhood Chain usage going up?"

**Action:** Call `GET /api/stats/chart`
- Return 14-day transaction count trend
- Note any patterns

## 8. Transfer History
**User:** "Show me all USDC transfers for this address"

**Action:** Call `GET /api/address/0x.../transfers`
- Filter results to show only USDC transfers
- Paginate if needed
