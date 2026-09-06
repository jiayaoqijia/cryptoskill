---
name: gate-dex-asset-query
version: "2026.3.25-1"
updated: "2026-03-25"
description: "Gate Wallet asset query module. Query token balances, total portfolio value, wallet addresses, transaction history, and swap history. Use when the user wants to check their holdings, view past transactions, or retrieve wallet addresses."
---

# Gate DEX Asset Query

> Asset query module — token balances, total portfolio value, wallet addresses, transaction history, and swap history. 7 MCP tools.

## Applicable Scenarios

Use when the user wants to:

- View their wallet holdings or check balances on a specific chain
- See total portfolio value in USD
- Retrieve wallet addresses (EVM / Solana)
- Browse transaction history or swap history
- Look up details of a specific transaction by hash

## Capability Boundaries

- **Supports**: Token balance queries, total asset value (USD), wallet address retrieval, transaction history, swap history, single transaction details, chain configuration
- **Does not support**: Token transfers (-> [transfer.md](./transfer.md)), token swaps (-> `gate-dex-trade`), market data queries (-> `gate-dex-market`), x402 payment (-> [x402.md](./x402.md))

**Prerequisites**: MCP Server available (see parent SKILL.md). All operations require a valid `mcp_token`. If missing or expired, route to [auth.md](./auth.md).

---

## MCP Tools


| Tool                         | Purpose                    | Key Parameters                                                               |
| ---------------------------- | -------------------------- | ---------------------------------------------------------------------------- |
| `dex_wallet_get_token_list`  | Token balances per chain   | `chain?`, `network_keys?`, `account_id?`, `mcp_token`, `page?`, `page_size?` |
| `dex_wallet_get_total_asset` | Total asset value (USD)    | `account_id`, `mcp_token`                                                    |
| `dex_wallet_get_addresses`   | Wallet addresses per chain | `account_id`, `mcp_token`                                                    |
| `dex_chain_config`           | Chain configuration info   | `chain`, `mcp_token`                                                         |
| `dex_tx_list`                | Transaction history        | `account_id`, `chain?`, `page?`, `limit?`, `mcp_token`                       |
| `dex_tx_detail`              | Single transaction details | `hash_id`, `chain`, `mcp_token`                                              |
| `dex_tx_history_list`        | Swap history               | `account_id`, `chain?`, `page?`, `limit?`, `mcp_token`                       |


---

## Execution Flow

```
Step 0: MCP Server connection detection (once per session)
  |
Step 1: Authentication check
  |- No mcp_token -> Route to auth.md
  +- Valid token  -> Continue
  |
Step 2: Execute query based on user intent
  |- Token balances:   dex_wallet_get_token_list({ chain?, mcp_token })
  |- Total assets:     dex_wallet_get_total_asset({ account_id, mcp_token })
  |- Wallet addresses: dex_wallet_get_addresses({ account_id, mcp_token })
  |- Chain config:     dex_chain_config({ chain, mcp_token })
  |- Tx history:       dex_tx_list({ account_id, chain?, mcp_token })
  |- Tx details:       dex_tx_detail({ hash_id, chain, mcp_token })
  +- Swap history:     dex_tx_history_list({ account_id, chain?, mcp_token })
  |
Step 3: Format and display results
  |- Group by chain, sort by value, filter zero balances
  |
Step 4: Proactively display post-query suggestions (see Post-Query Suggestions)
```

---

## Intent-to-Tool Mapping


| User Intent                                                                                          | Tool                         | Notes                                      |
| ---------------------------------------------------------------------------------------------------- | ---------------------------- | ------------------------------------------ |
| "What tokens do I have?" / "check balance" / "show my holdings" / "list my coins"                    | `dex_wallet_get_token_list`  | Pass `chain` if user specifies a chain     |
| "How much is my portfolio worth?" / "total assets" / "net worth" / "how much do I have in USD"       | `dex_wallet_get_total_asset` | Returns USD value with per-chain breakdown |
| "What is my wallet address?" / "my address" / "show my ETH address" / "give me my receiving address" | `dex_wallet_get_addresses`   | EVM chains share the same address          |
| "Show my recent transactions" / "tx history" / "what transfers did I make" / "past activity"         | `dex_tx_list`                | Paginated; pass `chain` to filter          |
| "What happened with tx 0xabc...?" / "check this transaction" / "look up this hash"                   | `dex_tx_detail`              | Requires `hash_id` and `chain`             |
| "Show my swap history" / "past swaps" / "exchange history" / "what did I trade"                      | `dex_tx_history_list`        | Paginated; pass `chain` to filter          |
| "What chains are supported?" / "which networks" / "chain config"                                     | `dex_chain_config`           | Returns RPC, block explorer, etc.          |
| "Do I have any USDT?" / "how many ETH do I hold" / "check my SOL balance"                            | `dex_wallet_get_token_list`  | Filter results for the specific token      |
| "Show everything on BSC" / "Arbitrum tokens" / "my Solana portfolio"                                 | `dex_wallet_get_token_list`  | Pass specific `chain` parameter            |


---

## Conversation Examples

**Example 1 (Happy Path): Check balance on a specific chain**
User: "What tokens do I have on Ethereum?"
Agent:

1. Verify `mcp_token` is valid.
2. Call `dex_wallet_get_token_list({ chain: "eth", mcp_token })`.
3. Format and display token list with symbols, balances, and USD values.
4. Display post-query suggestions (balance template).

**Example 2 (Happy Path): Total portfolio value**
User: "How much are my assets worth in total?"
Agent:

1. Verify `mcp_token` is valid.
2. Call `dex_wallet_get_total_asset({ account_id, mcp_token })`.
3. Display total value in USD with per-chain breakdown.
4. Display post-query suggestions (total asset template).

**Example 3 (Happy Path): View transaction history**
User: "Show my recent transactions"
Agent:

1. Verify `mcp_token` is valid.
2. Call `dex_tx_list({ account_id, mcp_token })`.
3. Display transactions with hash, amount, timestamp, and status.
4. Display post-query suggestions (transaction history template).

**Example 4 (Happy Path): Check specific token balance**
User: "How many ETH do I have?"
Agent:

1. Verify `mcp_token` is valid.
2. Call `dex_wallet_get_token_list({ mcp_token })`.
3. Filter results for ETH, display balance and USD value.
4. If ETH not found, reply: "No ETH found in your wallet. You may not hold any ETH at this time."

**Example 5 (Happy Path): Multi-chain balance overview**
User: "Show all my tokens across all chains"
Agent:

1. Verify `mcp_token` is valid.
2. Call `dex_wallet_get_token_list({ mcp_token })` without chain filter.
3. Group results by chain, sort by USD value.
4. Display summary table with chain, token, balance, USD value.

**Example 6 (Edge Case): Get wallet address for a specific chain**
User: "What is my Solana address?"
Agent:

1. Verify `mcp_token` is valid.
2. Call `dex_wallet_get_addresses({ account_id, mcp_token })`.
3. Display the Solana address. Note that EVM chains share one address.
4. Display post-query suggestions (address template).

**Example 7 (Edge Case): Empty results**
User: "Show my tokens on Avalanche"
Agent:

1. Verify `mcp_token` is valid.
2. Call `dex_wallet_get_token_list({ chain: "avax", mcp_token })`.
3. Result is empty. Reply: "No tokens found on Avalanche. You may not hold any assets on this chain yet."
4. Suggest: "You can check balances on other chains or view your wallet addresses."

**Example 8 (Edge Case): Transaction lookup by hash**
User: "What happened with this tx: 0xa1b2c3..."
Agent:

1. Verify `mcp_token` is valid.
2. Ask which chain if not specified: "Which chain was this transaction on? (e.g., Ethereum, BSC, Solana)"
3. Call `dex_tx_detail({ hash_id: "0xa1b2c3...", chain: "eth", mcp_token })`.
4. Display transaction details: status, from, to, amount, gas used, timestamp.

**Example 9 (Edge Case): Swap history filtered by chain**
User: "Show my swaps on Arbitrum"
Agent:

1. Call `dex_tx_history_list({ account_id, chain: "arbitrum", mcp_token })`.
2. Display swap history with token pairs, amounts, timestamps.

**Example 10 (Edge Case): Vague balance request**
User: "How much do I have?"
Agent:

1. Interpret as total portfolio value.
2. Call `dex_wallet_get_total_asset({ account_id, mcp_token })`.
3. Display total USD value. Suggest viewing per-chain breakdown if needed.

**Example 11 (Boundary Case): Not this module — market data**
User: "What is ETH price right now?"
Agent: This is a market data query. Route to `gate-dex-market`.

**Example 12 (Boundary Case): Not this module — transfer**
User: "Send 1 ETH to 0xABC..."
Agent: This is a transfer operation. Route to [transfer.md](./transfer.md).

**Example 13 (Boundary Case): Not this module — swap**
User: "Swap my ETH for USDT"
Agent: This is a swap operation. Route to `gate-dex-trade`.

**Example 14 (Boundary Case): Not this module — security audit**
User: "Is this token safe? Contract: 0xDEF..."
Agent: This is a security audit. Route to `gate-dex-market`.

---

## Post-Query Suggestions

After displaying query results, **proactively display relevant next actions** based on what the user just viewed. Every suggestion template is paired with the Follow-up Routing Table below.

**After balance / token list query:**

```
Your token balances are shown above.

You can:
- Transfer tokens to another address
- Swap tokens on DEX
- View token price charts or run a security audit
- Check your transaction history
```

**After total asset value query:**

```
Your total portfolio value is shown above.

You can:
- View balances broken down by chain
- Transfer tokens to another address
- Swap tokens on DEX
- View token price charts
```

**After transaction history query:**

```
Your recent transactions are shown above.

You can:
- View details of a specific transaction (provide the tx hash)
- Check your current balances
- Make a new transfer
```

**After swap history query:**

```
Your swap history is shown above.

You can:
- View details of a specific swap transaction
- Check your current token balances
- Execute a new swap on DEX
```

**After wallet address query:**

```
Your wallet addresses are shown above.

You can:
- Share this address to receive tokens
- Connect this address to a DApp
- Check your token balances
- View transaction history
```

### Follow-up Routing Table


| User Follow-up Intent                  | Target                                    |
| -------------------------------------- | ----------------------------------------- |
| View token prices or K-line charts     | `gate-dex-market`                         |
| Run a token security audit             | `gate-dex-market`                         |
| Transfer or send tokens                | [transfer.md](./transfer.md)              |
| Swap or exchange tokens                | `gate-dex-trade`                          |
| Pay for a 402 resource                 | [x402.md](./x402.md)                      |
| Interact with a DApp                   | [dapp.md](./dapp.md)                      |
| Login or fix expired auth              | [auth.md](./auth.md)                      |
| Use CLI commands                       | [cli.md](./cli.md)                        |
| View details of a specific transaction | `dex_tx_detail` (this module)             |
| Check balances on another chain        | `dex_wallet_get_token_list` (this module) |


---

## Cross-Skill Collaboration

This module provides the **wallet data center** — other skills call its tools:


| Caller                       | Scenario                                                | Tools Used                  |
| ---------------------------- | ------------------------------------------------------- | --------------------------- |
| `gate-dex-trade`             | Pre-swap balance verification, token address resolution | `dex_wallet_get_token_list` |
| `gate-dex-trade`             | Retrieve chain-specific wallet address                  | `dex_wallet_get_addresses`  |
| `gate-dex-market`            | Guide user to view holdings after a market query        | `dex_wallet_get_token_list` |
| [transfer.md](./transfer.md) | Pre-transfer balance check (token + gas)                | `dex_wallet_get_token_list` |


---

## Error Handling


| Scenario                              | Handling                                                                                        |
| ------------------------------------- | ----------------------------------------------------------------------------------------------- |
| `mcp_token` missing or expired        | Attempt silent refresh via `dex_auth_refresh_token`; on failure route to [auth.md](./auth.md)   |
| Chain not supported                   | Inform user; list supported chains from parent SKILL.md                                         |
| `dex_tx_detail` with invalid hash     | Display error; prompt user to verify the transaction hash and chain                             |
| Empty result (no tokens / no history) | Inform user the result is empty (e.g., "No tokens found on this chain") — do not fabricate data |
| Pagination out of range               | Inform user no more results; offer to return to the first page                                  |
| MCP Server connection failure         | Display error message transparently; suggest retry                                              |
| Network timeout                       | Inform user of timeout; suggest retrying in a moment                                            |


---

## Security Rules

1. **Authentication first**: Verify `mcp_token` validity before all queries.
2. **Token confidentiality**: Never display `mcp_token` in plaintext.
3. **Account ID masking**: Show only partial `account_id` characters in any user-facing output.
4. **Silent refresh**: Prioritize `dex_auth_refresh_token` on token expiration before routing to re-login.
5. **No data fabrication**: If a query returns empty or errors, report truthfully. Never invent balances or transaction data.
6. **Transparent errors**: Display all MCP Server error messages to users without modification.
7. **MCP Server required**: Abort all operations if connection detection fails.

