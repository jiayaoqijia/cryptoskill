---
name: gate-dex-transfer
description: "Gate Wallet transfer execution. Build transaction, sign, and broadcast. Use when the user wants to
  'send ETH', 'transfer USDT', 'transfer', or 'send tokens'. Includes mandatory balance verification
  and user confirmation gating. Supports EVM multi-chain + Solana native/token transfers."
---

# Gate DEX Transfer

> Transfer domain — Gas estimation, transaction preview, balance verification, signing, broadcasting, with mandatory user confirmation gating. 4 MCP tools + 1 cross-Skill call.

**Trigger scenarios**: When the user mentions "transfer", "send", "send ETH", "send tokens", or when another Skill directs the user to execute an on-chain transfer.

## MCP Server Connection Detection

### Initial Session Detection

**Before calling any MCP tool for the first time in a session, perform a one-time connectivity probe to confirm the Gate Wallet MCP Server is available. Subsequent operations do not require repeated detection.**

```
CallMcpTool(server="gate-wallet", toolName="chain.config", arguments={chain: "eth"})
```

| Result | Action |
|--------|--------|
| Success | MCP Server is available; subsequent operations call business tools directly without re-probing |
| Failure | Display configuration guide based on error type (see error handling below) |

### Runtime Error Fallback

If a business tool call fails during subsequent operations (returning connection errors, timeouts, etc.), handle as follows:

| Error Type | Keywords | Action |
|------------|----------|--------|
| MCP Server not configured | `server not found`, `unknown server` | Display MCP Server configuration guide |
| Remote service unreachable | `connection refused`, `timeout`, `DNS error` | Prompt user to check server status and network connection |
| Authentication failed | `401`, `unauthorized`, `x-api-key` | Prompt user to contact admin for API Key |

## Authentication Notes

All operations in this Skill **require `mcp_token`**. You must confirm the user is logged in before calling any tool.

- If no `mcp_token` is available → Direct the user to `gate-dex-auth` to complete login, then return.
- If `mcp_token` has expired (MCP Server returns token expiry error) → First attempt silent refresh via `auth.refresh_token`; if that fails, direct the user to log in again.

## MCP Tool Call Specification

### 1. `wallet.get_token_list` (Cross-Skill Call) — Query Balance for Verification

Before transferring, you **must** call this tool to verify the sending token balance and Gas token balance. This tool belongs to the `gate-dex-wallet` domain and is invoked here as a cross-Skill call.

| Field | Description |
|-------|-------------|
| **Tool Name** | `wallet.get_token_list` |
| **Parameters** | `{ account_id: string, chain: string, mcp_token: string }` |
| **Return Value** | Token array, each item containing `symbol`, `balance`, `price`, `value`, `chain`, `contract_address`, etc. |

Call example:

```
CallMcpTool(
  server="gate-wallet",
  toolName="wallet.get_token_list",
  arguments={ account_id: "acc_12345", chain: "eth", mcp_token: "<mcp_token>" }
)
```

Agent behavior: Extract the transfer token balance and the chain's native token balance (for Gas) from the returned list, in preparation for subsequent balance verification.

---

### 2. `tx.gas` — Estimate Gas Fees

Estimate Gas fees for a transaction on a given chain, returning gas price and estimated consumption.

| Field | Description |
|-------|-------------|
| **Tool Name** | `tx.gas` |
| **Parameters** | `{ chain: string, from_address: string, to_address: string, value?: string, data?: string, mcp_token: string }` |
| **Return Value** | `{ gas_limit: string, gas_price: string, estimated_fee: string, fee_usd: number }` |

Parameter details:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `chain` | Yes | Chain identifier (e.g., `"eth"`, `"bsc"`, `"sol"`) |
| `from_address` | Yes | Sender address |
| `to_address` | Yes | Recipient address |
| `value` | No | Native token transfer amount (in wei / lamports format). Can be `"0"` for ERC20 transfers |
| `data` | No | Transaction data (transfer calldata for ERC20 transfers) |
| `mcp_token` | Yes | Authentication token |

Call example (native token transfer):

```
CallMcpTool(
  server="gate-wallet",
  toolName="tx.gas",
  arguments={
    chain: "eth",
    from_address: "0xABCdef1234567890ABCdef1234567890ABCdef12",
    to_address: "0xDEF4567890ABCdef1234567890ABCdef12345678",
    value: "1000000000000000000",
    mcp_token: "<mcp_token>"
  }
)
```

Return example:

```json
{
  "gas_limit": "21000",
  "gas_price": "30000000000",
  "estimated_fee": "0.00063",
  "fee_usd": 1.21
}
```

Call example (ERC20 token transfer):

```
CallMcpTool(
  server="gate-wallet",
  toolName="tx.gas",
  arguments={
    chain: "eth",
    from_address: "0xABCdef1234567890ABCdef1234567890ABCdef12",
    to_address: "0xdAC17F958D2ee523a2206206994597C13D831ec7",
    value: "0",
    data: "0xa9059cbb000000000000000000000000DEF4567890ABCdef1234567890ABCdef123456780000000000000000000000000000000000000000000000000000000077359400",
    mcp_token: "<mcp_token>"
  }
)
```

Agent behavior: Solana has a different Gas structure (fees are denominated in lamports); parameters and return fields may differ — handle according to the actual response.

---

### 3. `tx.transfer_preview` — Build Transaction Preview

Build an unsigned transaction and return a confirmation summary, including the server-side `confirm_message`. This is the final preview step before signing.

| Field | Description |
|-------|-------------|
| **Tool Name** | `tx.transfer_preview` |
| **Parameters** | `{ chain: string, from_address: string, to_address: string, token_address: string, amount: string, account_id: string, mcp_token: string }` |
| **Return Value** | `{ raw_tx: string, confirm_message: string, estimated_gas: string, nonce: number }` |

Parameter details:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `chain` | Yes | Chain identifier |
| `from_address` | Yes | Sender address |
| `to_address` | Yes | Recipient address |
| `token_address` | Yes | Token contract address. Use `"native"` for native tokens |
| `amount` | Yes | Transfer amount (human-readable format, e.g., `"1.5"` instead of wei) |
| `account_id` | Yes | User account ID |
| `mcp_token` | Yes | Authentication token |

Call example:

```
CallMcpTool(
  server="gate-wallet",
  toolName="tx.transfer_preview",
  arguments={
    chain: "eth",
    from_address: "0xABCdef1234567890ABCdef1234567890ABCdef12",
    to_address: "0xDEF4567890ABCdef1234567890ABCdef12345678",
    token_address: "0xdAC17F958D2ee523a2206206994597C13D831ec7",
    amount: "1000",
    account_id: "acc_12345",
    mcp_token: "<mcp_token>"
  }
)
```

Return example:

```json
{
  "raw_tx": "0x02f8...",
  "confirm_message": "Transfer 1000 USDT to 0xDEF4...5678 on Ethereum",
  "estimated_gas": "0.003",
  "nonce": 42
}
```

Agent behavior: After receiving `raw_tx`, **do not sign directly** — you must first present the confirmation summary to the user and wait for explicit confirmation.

---

### 4. `wallet.sign_transaction` — Server-Side Signing

Sign an unsigned transaction using the server-hosted private key. **Only call this after the user has explicitly confirmed.**

| Field | Description |
|-------|-------------|
| **Tool Name** | `wallet.sign_transaction` |
| **Parameters** | `{ raw_tx: string, chain: string, account_id: string, mcp_token: string }` |
| **Return Value** | `{ signed_tx: string }` |

Parameter details:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `raw_tx` | Yes | Unsigned transaction returned by `tx.transfer_preview` |
| `chain` | Yes | Chain identifier |
| `account_id` | Yes | User account ID |
| `mcp_token` | Yes | Authentication token |

Call example:

```
CallMcpTool(
  server="gate-wallet",
  toolName="wallet.sign_transaction",
  arguments={
    raw_tx: "0x02f8...",
    chain: "eth",
    account_id: "acc_12345",
    mcp_token: "<mcp_token>"
  }
)
```

Return example:

```json
{
  "signed_tx": "0x02f8b2...signed..."
}
```

---

### 5. `tx.send_raw_transaction` — Broadcast Signed Transaction

Broadcast the signed transaction to the on-chain network.

| Field | Description |
|-------|-------------|
| **Tool Name** | `tx.send_raw_transaction` |
| **Parameters** | `{ signed_tx: string, chain: string, mcp_token: string }` |
| **Return Value** | `{ hash_id: string }` |

Parameter details:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `signed_tx` | Yes | Signed transaction returned by `wallet.sign_transaction` |
| `chain` | Yes | Chain identifier |
| `mcp_token` | Yes | Authentication token |

Call example:

```
CallMcpTool(
  server="gate-wallet",
  toolName="tx.send_raw_transaction",
  arguments={
    signed_tx: "0x02f8b2...signed...",
    chain: "eth",
    mcp_token: "<mcp_token>"
  }
)
```

Return example:

```json
{
  "hash_id": "0xa1b2c3d4e5f6...7890"
}
```

Agent behavior: After a successful broadcast, display the transaction hash to the user and provide a block explorer link.

## Supported Chains

| Chain ID | Network Name | Type | Native Gas Token | Block Explorer |
|----------|-------------|------|-----------------|----------------|
| `eth` | Ethereum | EVM | ETH | etherscan.io |
| `bsc` | BNB Smart Chain | EVM | BNB | bscscan.com |
| `polygon` | Polygon | EVM | MATIC | polygonscan.com |
| `arbitrum` | Arbitrum One | EVM | ETH | arbiscan.io |
| `optimism` | Optimism | EVM | ETH | optimistic.etherscan.io |
| `avax` | Avalanche C-Chain | EVM | AVAX | snowtrace.io |
| `base` | Base | EVM | ETH | basescan.org |
| `sol` | Solana | Non-EVM | SOL | solscan.io |

## MCP Tool Call Chain Overview

The complete transfer flow calls the following tools in sequence, forming a strict linear pipeline:

```
0. chain.config                         ← Initial session detection (if needed)
1. wallet.get_token_list                ← Cross-Skill: query balance (token + Gas token)
2. tx.gas                               ← Estimate Gas fees
3. [Agent balance check: balance >= amount + Gas]  ← Agent internal logic, not an MCP call
4. tx.transfer_preview                  ← Build unsigned transaction + server confirmation info
5. [Agent displays confirmation summary, waits for user confirmation]  ← Mandatory gate, not an MCP call
6. wallet.sign_transaction              ← Sign after user confirmation
7. tx.send_raw_transaction              ← Broadcast to chain
```

## Skill Routing

Based on the user's intent after the transfer completes, route to the corresponding Skill:

| User Intent | Route Target |
|-------------|-------------|
| View updated balance | `gate-dex-wallet` |
| View transaction details / history | `gate-dex-wallet` (`tx.detail`, `tx.list`) |
| Continue transferring to another address | Stay in this Skill |
| Swap tokens | `gate-dex-trade` |
| Login / authentication expired | `gate-dex-auth` |

## Operation Flow

### Flow A: Standard Transfer (Main Flow)

```
Initial session detection (if needed)
  Call chain.config({chain: "eth"}) to probe availability
  ↓ Success

Step 1: Authentication Check
  Confirm possession of a valid mcp_token and account_id
  No token → Direct to gate-dex-auth for login
  ↓

Step 2: Intent Recognition + Parameter Collection
  Extract transfer intent from user input, collect the following required parameters:
  - to_address: Recipient address (required)
  - amount: Transfer amount (required)
  - token: Transfer token (required, e.g., ETH, USDT)
  - chain: Target chain (optional, can be inferred from token or context)

  When parameters are missing, ask the user for each one:

  ────────────────────────────
  Please provide the transfer details:
  - Recipient address: (required, please provide the full address)
  - Transfer amount: (required, e.g., 1.5)
  - Token: (required, e.g., ETH, USDT)
  - Chain: (optional, defaults to Ethereum. Supported: eth/bsc/polygon/arbitrum/optimism/avax/base/sol)
  ────────────────────────────

  ↓ All parameters collected

Step 3: Get Wallet Address
  Call wallet.get_addresses({ account_id, mcp_token })
  Extract from_address for the target chain
  ↓

Step 4: Query Balance (Cross-Skill: gate-dex-wallet)
  Call wallet.get_token_list({ account_id, chain, mcp_token })
  Extract:
  - Transfer token balance (e.g., USDT balance)
  - Chain native Gas token balance (e.g., ETH balance)
  ↓

Step 5: Estimate Gas Fees
  Call tx.gas({ chain, from_address, to_address, value?, data?, mcp_token })
  Obtain estimated_fee (denominated in native token) and fee_usd
  ↓

Step 6: Agent Balance Verification (Mandatory)
  Verification rules:
  a) Native token transfer: balance >= amount + estimated_fee
  b) ERC20 token transfer: token_balance >= amount AND native_balance >= estimated_fee
  c) Solana SPL token transfer: token_balance >= amount AND sol_balance >= estimated_fee

  Verification failed → Abort transaction, display insufficient balance details:

  ────────────────────────────
  ❌ Insufficient balance, unable to execute transfer

  Transfer amount: 1000 USDT
  Current USDT balance: 800 USDT (insufficient, short by 200 USDT)

  Or:

  Transfer amount: 1.0 ETH
  Estimated Gas: 0.003 ETH
  Total required: 1.003 ETH
  Current ETH balance: 0.9 ETH (insufficient, short by 0.103 ETH)

  Suggestions:
  - Reduce the transfer amount
  - Top up your wallet first
  ────────────────────────────

  ↓ Verification passed

Step 7: Build Transaction Preview
  Call tx.transfer_preview({ chain, from_address, to_address, token_address, amount, account_id, mcp_token })
  Obtain raw_tx and confirm_message
  ↓

Step 8: Display Confirmation Summary (Mandatory Gate)
  You must present the full confirmation details to the user and wait for an explicit "confirm" reply before proceeding.
  See the "Transaction Confirmation Template" below for display content.
  ↓

  User replies "confirm" → Proceed to Step 9
  User replies "cancel" → Abort transaction, display cancellation notice
  User requests changes → Return to Step 2 to re-collect modified parameters

Step 9: Sign Transaction
  Call wallet.sign_transaction({ raw_tx, chain, account_id, mcp_token })
  Obtain signed_tx
  ↓

Step 10: Broadcast Transaction
  Call tx.send_raw_transaction({ signed_tx, chain, mcp_token })
  Obtain hash_id
  ↓

Step 11: Display Result + Follow-up Suggestions

  ────────────────────────────
  ✅ Transfer broadcast successful!

  Transaction Hash: {hash_id}
  Block Explorer: https://{explorer}/tx/{hash_id}

  The transaction has been submitted to the network. Confirmation time depends on network congestion.

  You can:
  - View your updated balance
  - View transaction details
  - Continue with other operations
  ────────────────────────────
```

### Flow B: Batch Transfer

```
Initial session detection (if needed)
  ↓ Success

Step 1-2: Authentication + Parameter Collection
  Identify multiple transfer intents, collect to_address, amount, token, chain for each transfer
  ↓

Step 3-8: Execute each transfer individually
  Each transfer independently goes through Steps 3–8 (query balance → Gas → verification → preview → confirmation)
  Each transfer displays a separate confirmation summary for individual approval:

  ────────────────────────────
  📦 Batch Transfer (Transaction 1/3)

  [Display confirmation summary for this transaction]

  Reply "confirm" to execute this transaction, "skip" to skip it, or "cancel all" to abort all remaining.
  ────────────────────────────

  ↓ User confirms each transaction individually

Step 9-10: Sign + broadcast each confirmed transaction
  ↓

Step 11: Summary of Results

  ────────────────────────────
  📦 Batch Transfer Results

  | # | Recipient Address | Amount | Status | Hash |
  |---|-------------------|--------|--------|------|
  | 1 | 0xDEF...5678 | 100 USDT | ✅ Success | 0xa1b2... |
  | 2 | 0x123...ABCD | 200 USDT | ✅ Success | 0xc3d4... |
  | 3 | 0x456...EF01 | 50 USDT  | ⏭ Skipped | — |

  Successful: 2/3 transactions
  ────────────────────────────
```

## Transaction Confirmation Template

**The Agent must not execute the signing operation until the user explicitly replies "confirm" to this confirmation summary. This is a mandatory, non-skippable gate.**

### Native Token Transfer Confirmation

```
========== Transaction Confirmation ==========
Chain: {chain_name} (e.g., Ethereum)
Type: Native Token Transfer
Sender Address: {from_address}
Recipient Address: {to_address}
Transfer Amount: {amount} {symbol} (e.g., 1.5 ETH)
---------- Balance Info ----------
{symbol} Balance: {balance} {symbol} (Sufficient ✅)
---------- Fee Info ----------
Estimated Gas: {estimated_fee} {gas_symbol} (≈ ${fee_usd})
Remaining After Transfer: {remaining_balance} {symbol}
---------- Server Confirmation ----------
{confirm_message from tx.transfer_preview}
===============================================
Reply "confirm" to execute, "cancel" to abort, or specify what to change.
```

### ERC20 / SPL Token Transfer Confirmation

```
========== Transaction Confirmation ==========
Chain: {chain_name} (e.g., Ethereum)
Type: ERC20 Token Transfer
Sender Address: {from_address}
Recipient Address: {to_address}
Transfer Amount: {amount} {token_symbol} (e.g., 1000 USDT)
Token Contract: {token_address}
---------- Balance Info ----------
{token_symbol} Balance: {token_balance} {token_symbol} (Sufficient ✅)
{gas_symbol} Balance (Gas): {gas_balance} {gas_symbol} (Sufficient ✅)
---------- Fee Info ----------
Estimated Gas: {estimated_fee} {gas_symbol} (≈ ${fee_usd})
Remaining After Transfer: {remaining_token} {token_symbol} / {remaining_gas} {gas_symbol}
---------- Server Confirmation ----------
{confirm_message from tx.transfer_preview}
===============================================
Reply "confirm" to execute, "cancel" to abort, or specify what to change.
```

## Cross-Skill Workflows

### Complete Transfer Flow (From Login to Completion)

```
gate-dex-auth (login, obtain mcp_token + account_id)
  → gate-dex-wallet (wallet.get_token_list → verify balance)
    → gate-dex-wallet (wallet.get_addresses → get sender address)
      → gate-dex-transfer (tx.gas → tx.transfer_preview → confirm → sign → broadcast)
        → gate-dex-wallet (view updated balance)
```

### Directed From Other Skills

| Source Skill | Scenario | Notes |
|-------------|----------|-------|
| `gate-dex-wallet` | User wants to transfer after viewing balance | Carries account_id, chain, from_address info |
| `gate-dex-trade` | User wants to send out resulting tokens after a swap | Chain and token context already available |
| `gate-dex-dapp` | Tokens from DApp operations need to be sent out | Chain and address context already available |

### Calling Other Skills

| Target Skill | Call Scenario | Tool Used |
|-------------|--------------|-----------|
| `gate-dex-wallet` | Query balance before transfer | `wallet.get_token_list` |
| `gate-dex-wallet` | Get sender address before transfer | `wallet.get_addresses` |
| `gate-dex-wallet` | View updated balance after transfer | `wallet.get_token_list` |
| `gate-dex-auth` | Not logged in or token expired | `auth.refresh_token` or full login flow |
| `gate-dex-wallet` | View transaction details after transfer | `tx.detail`, `tx.list` |

## Address Validation Rules

Before initiating a transfer, the Agent must validate the recipient address format:

| Chain Type | Format Requirement | Validation Rule |
|-----------|-------------------|-----------------|
| EVM (eth/bsc/polygon/...) | Starts with `0x`, 40 hex characters (42 total) | Regex `^0x[0-9a-fA-F]{40}$`, EIP-55 checksum validation recommended |
| Solana | Base58 encoded, 32–44 characters | Regex `^[1-9A-HJ-NP-Za-km-z]{32,44}$` |

When validation fails:

```
❌ Invalid recipient address format

Provided address: {user_input}
Expected format: {expected_format}

Please verify the address is correct, complete, and matches the target chain.
```

## Edge Cases and Error Handling

| Scenario | Handling |
|----------|---------|
| MCP Server not configured | Abort all operations, display Cursor configuration guide |
| MCP Server unreachable | Abort all operations, display network check prompt |
| Not logged in (no `mcp_token`) | Direct to `gate-dex-auth` to complete login, then automatically return to continue the transfer |
| `mcp_token` expired | First attempt silent refresh via `auth.refresh_token`; if that fails, direct to re-login |
| Insufficient transfer token balance | Abort transaction, display current balance vs. required amount difference, suggest reducing amount or topping up first |
| Insufficient Gas token balance | Abort transaction, display Gas token shortage info, suggest obtaining Gas tokens first |
| Invalid recipient address format | Refuse to initiate the transaction, prompt with the correct address format |
| Recipient address same as sender address | Warn the user and confirm whether this is intentional, to prevent accidental transfers |
| `tx.gas` estimation failed | Display error info; possible causes: network congestion, contract call exception. Suggest retrying later |
| `tx.transfer_preview` failed | Display server-returned error message, do not silently retry |
| `wallet.sign_transaction` failed | Display signing error; possible causes: account permissions, server exception. Do not auto-retry |
| `tx.send_raw_transaction` failed | Display broadcast error (e.g., nonce conflict, insufficient gas, network congestion), suggest appropriate action based on error type |
| User cancels confirmation | Immediately abort, do not execute signing or broadcasting. Display cancellation notice in a friendly manner |
| Amount exceeds token precision | Prompt about token precision limits, auto-truncate or ask user to correct |
| Transfer amount is 0 or negative | Refuse to execute, prompt user to enter a valid positive amount |
| Unsupported chain identifier | Display the list of supported chains, ask user to select again |
| Target chain does not match token | Inform user the token does not exist on the target chain, suggest the correct chain |
| Broadcast succeeded but transaction unconfirmed for a long time | Inform user the transaction has been submitted, confirmation time depends on network conditions, track via block explorer |
| Network interruption | Display network error, suggest checking network and retrying. If network drops after signing but before broadcasting, inform user the signed transaction can still be broadcast later |
| A transaction fails during batch transfer | Mark that transaction as failed, continue processing subsequent transactions, display a summary of all results at the end |

## Security Rules

1. **`mcp_token` confidentiality**: Never display `mcp_token` in plaintext to the user; use the placeholder `<mcp_token>` in call examples only.
2. **`account_id` redaction**: When displaying to the user, show only partial characters (e.g., `acc_12...89`).
3. **Automatic token refresh**: When `mcp_token` expires, attempt silent refresh first; only require re-login if refresh fails.
4. **Mandatory balance verification**: Before every transfer, you **must** verify balance (token + Gas); **do not** initiate signing or broadcasting if balance is insufficient.
5. **Mandatory user confirmation**: Before signing, you **must** present the full confirmation summary and receive an explicit "confirm" reply. Do not skip, simplify, or auto-confirm.
6. **Individual confirmation for batch transfers**: For batch transfers, display a separate confirmation summary for each transaction and wait for user confirmation individually.
7. **No automatic retry of failed transactions**: After a signing or broadcast failure, clearly display the error to the user; do not auto-retry in the background.
8. **Address validation**: Validate recipient address format before sending to prevent asset loss due to incorrect addresses.
9. **No operations when MCP Server is unconfigured or unreachable**: If the Step 0 connection check fails, abort all subsequent steps.
10. **MCP Server error transparency**: Display all MCP Server error messages to the user as-is; do not hide or alter them.
11. **`raw_tx` must not be leaked**: Unsigned raw transaction data flows only between the Agent and MCP Server; do not display the raw hex to the user.
12. **Broadcast promptly after signing**: After a successful signing, broadcast immediately; do not hold signed transactions for an extended period.
