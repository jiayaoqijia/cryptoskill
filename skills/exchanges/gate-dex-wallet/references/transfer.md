---
name: gate-dex-transfer
version: "2026.3.31-2"
updated: "2026-03-31"
description: "Gate Wallet transfer execution module. Builds transactions, signs, and broadcasts. Use when the user wants to send tokens to an address, including single and batch transfers. Includes mandatory balance verification, user confirmation gate, and terminal tx-checkin before signing. Supports EVM multi-chain and Solana native/token transfers."
---

# Gate DEX Transfer

> Transfer module — gas estimation, transaction preview, balance verification, **terminal tx-checkin before signing**, signing, and broadcasting. Includes mandatory user confirmation gates. 4 MCP tools + 1 cross-skill call.

## Applicable Scenarios

Use when the user wants to:
- Send or transfer tokens to an on-chain address: "send ETH to 0x...", "transfer USDT", "pay someone"
- Execute batch transfers to multiple recipients: "send to these 3 addresses"
- Transfer native tokens (ETH, BNB, SOL) or token standards (ERC20, SPL)
- Move assets between their own wallets: "move my USDT to my other address"
- Another skill routes the user here for transfer operations

## Capability Boundaries

- **Supports**: Native token transfers, ERC20 transfers, SPL token transfers, batch transfers
- **Supported chains**: eth, bsc, polygon, arbitrum, optimism, avax, base, sol
- **Does not support**: Swap/exchange (-> `gate-dex-trade`), DApp contract calls (-> [dapp.md](./dapp.md)), x402 payment (-> [x402.md](./x402.md)), market data (-> `gate-dex-market`)

**Prerequisites**: MCP Server available (see parent SKILL.md). All operations require a valid `mcp_token`. If missing or expired, route to [auth.md](./auth.md).

---

## MCP Tools

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `dex_wallet_get_token_list` | Balance verification (cross-skill) | `account_id`, `chain`, `mcp_token` |
| `dex_tx_gas` | Estimate gas fee | `chain`, `from_address`, `to_address`, `value?`, `data?`, `mcp_token` |
| `dex_tx_transfer_preview` | Build unsigned tx + confirmation message | `chain`, `from_address`, `to_address`, `token_address`, `amount`, `account_id`, `mcp_token` |
| `dex_wallet_sign_transaction` | Server-side signing (**after** user confirm **and** terminal [tx-checkin.md](./tx-checkin.md)) | `raw_tx`, `chain`, `account_id`, `mcp_token` |
| `dex_tx_send_raw_transaction` | Broadcast signed tx | `signed_tx`, `chain`, `mcp_token` |

### Tool Details

#### `dex_wallet_get_token_list` (Cross-Skill) — Query Balance

Called before every transfer to verify the sending token balance and gas token balance.

| Field | Description |
|-------|-------------|
| **Parameters** | `{ account_id: string, chain: string, mcp_token: string }` |
| **Returns** | Token array with `symbol`, `balance`, `price`, `value`, `chain`, `contract_address` |

#### `dex_tx_gas` — Estimate Gas Fees

Estimates gas for a transaction on the specified chain.

| Field | Description |
|-------|-------------|
| **Parameters** | `{ chain, from_address, to_address, value?, data?, mcp_token }` |
| **Returns** | `{ gas_limit, gas_price, estimated_fee, fee_usd }` |

- For native token transfers: pass the `value` in wei/lamports.
- For ERC20 transfers: set `value` to `"0"` and provide `data` (transfer calldata).
- Solana gas structure differs (fee in lamports); handle according to actual returns.

#### `dex_tx_transfer_preview` — Build Transaction Preview

Builds an unsigned transaction and returns a confirmation summary including server-side `confirm_message`.

| Field | Description |
|-------|-------------|
| **Parameters** | `{ chain, from_address, to_address, token_address, amount, account_id, mcp_token }` (see live MCP schema for exact names such as `from` / `to` / `token_contract` / `token_mint`) |
| **Returns** | `unsigned_tx_hex` (use as `raw_tx` for signing), **`txBundle`** (string: exact check-in `message` for terminal [tx-checkin.md](./tx-checkin.md)), `key_info`, `confirm_message`, etc. |

- `token_address`: Use `"native"` for native tokens.
- `amount`: Human-readable format (e.g., `"1.5"`, not wei).

**CRITICAL**: After preview, do **not** sign until the user explicitly confirms. For terminal check-in, **only** use the preview field **`txBundle`** with `tx-checkin -tx-bundle-file` (see [tx-checkin.md](./tx-checkin.md)). **Do not** build txbundle JSON from `unsigned_tx_hex` or other fields. Call `dex_wallet_sign_transaction` with **`raw_tx` = `unsigned_tx_hex`** after successful check-in.

#### `dex_wallet_sign_transaction` — Server-side Signing

Signs an unsigned transaction using server-side custodial keys. **Only call after explicit user confirmation and after successful terminal tx-checkin** ([tx-checkin.md](./tx-checkin.md)).

| Field | Description |
|-------|-------------|
| **Parameters** | `{ raw_tx, chain, account_id, mcp_token }` |
| **Returns** | `{ signed_tx }` |

#### `dex_tx_send_raw_transaction` — Broadcast

Broadcasts a signed transaction to the on-chain network.

| Field | Description |
|-------|-------------|
| **Parameters** | `{ signed_tx, chain, mcp_token }` |
| **Returns** | `{ hash_id }` |

---

## Tool Call Chain

Complete transfer flow in strict linear sequence:

```
0. dex_chain_config                          <- Session detection (if needed)
1. dex_wallet_get_token_list                 <- Cross-skill: query balance (token + gas)
2. dex_tx_gas                                <- Estimate gas fees
3. [Agent balance validation]                <- Internal logic, not an MCP call
4. dex_tx_transfer_preview                   <- Build unsigned tx + confirmation info
5. [Display confirmation, wait for user]     <- MANDATORY gate, not an MCP call
6. [Terminal tx-checkin]                     <- MANDATORY: preview **txBundle** -> `-tx-bundle-file` per [tx-checkin.md](./tx-checkin.md), not an MCP call
7. dex_wallet_sign_transaction               <- Sign only after steps 5–6 succeed
8. dex_tx_send_raw_transaction               <- Broadcast on-chain
```

---

## Execution Flow

### Flow A: Standard Transfer

```
Step 1: Authentication check
  No mcp_token -> route to auth.md
  |
Step 2: Intent recognition + parameter collection
  Extract: to_address (required), amount (required), token (required), chain (optional)
  If parameters missing, ask the user for each:
  "Please provide: recipient address, transfer amount, token (e.g., ETH, USDT), and chain (optional, default Ethereum)."
  |
Step 3: Get wallet address
  Call dex_wallet_get_addresses({ account_id, mcp_token }) -> extract from_address for target chain
  |
Step 4: Query balance (cross-skill)
  Call dex_wallet_get_token_list({ account_id, chain, mcp_token })
  Extract transfer token balance and native gas token balance
  |
Step 5: Estimate gas
  Call dex_tx_gas({ chain, from_address, to_address, value?, data?, mcp_token })
  |
Step 6: Balance validation (MANDATORY)
  Rules:
  a) Native transfer:  balance >= amount + estimated_fee
  b) ERC20 transfer:   token_balance >= amount AND native_balance >= estimated_fee
  c) SPL transfer:     token_balance >= amount AND sol_balance >= estimated_fee
  Validation failed -> abort and display shortfall details with suggestions
  |
Step 7: Build transaction preview
  Call dex_tx_transfer_preview({ chain, from_address, to_address, token_address, amount, account_id, mcp_token })
  |
Step 8: Display confirmation (MANDATORY GATE)
  Show: chain, type, sender, recipient, amount, balances, gas estimate, server confirm_message
  Wait for explicit "confirm" reply.
  - "confirm" -> proceed to Step 9
  - "cancel"  -> abort, display cancellation notice
  - modification request -> return to Step 2
  |
Step 9: Terminal tx-checkin (MANDATORY)
  Run [tx-checkin.md](./tx-checkin.md): persist preview **`txBundle`** to a file (e.g. `jq -r '.txBundle' preview.json > bundle.txt` if the preview JSON is saved), then **`tx-checkin -tx-bundle-file bundle.txt`** with `-wallet`, `-chain`, `-chain-category` from the same preview / `key_info`. **Do not** hand-assemble txbundle.
  On failure -> abort; do not sign.
  |
Step 10: Sign transaction
  Call dex_wallet_sign_transaction({ raw_tx: **unsigned_tx_hex** from the same preview, chain, account_id, mcp_token })
  |
Step 11: Broadcast
  Call dex_tx_send_raw_transaction({ signed_tx, chain, mcp_token }) -> get hash_id
  |
Step 12: Display result + proactive suggestions
  Show tx hash, block explorer link, and post-transfer suggestions (see Post-Transfer Suggestions)
```

### Flow B: Batch Transfer

Each transfer independently goes through Steps 3-8, confirmed one by one:

```
Step 1-2: Auth + collect all transfer intents

Step 3-8: Per transfer (sequential)
  Each transfer gets its own confirmation:
  "confirm" -> Execute this transfer
  "skip"    -> Skip this transfer, continue to next
  "cancel all" -> Abort remaining transfers

Step 9: Terminal tx-checkin (MANDATORY) per transfer: each transfer’s preview **txBundle** -> `-tx-bundle-file`, then sign (`unsigned_tx_hex`) + broadcast confirmed transfers only

Step 10: Summary table + proactive suggestions
  | # | To | Amount | Status | Hash |
  |---|-----|--------|--------|------|
  | 1 | 0xDEF...5678 | 100 USDT | ✅ Success | 0xa1b2... |
  | 2 | 0x123...ABCD | 200 USDT | ⏭ Skipped | — |
```

---

## Transaction Confirmation Templates

**These confirmations are MANDATORY gates. Agent must NOT sign before receiving explicit user confirmation.**

### Native Token Transfer

```
========== Transaction Confirmation ==========
Chain:          {chain_name}
Type:           Native token transfer
From:           {from_address}
To:             {to_address}
Amount:         {amount} {symbol}
---------- Balance ----------
{symbol} Balance: {balance} (Sufficient ✅)
---------- Fees ----------
Estimated Gas:  {estimated_fee} {gas_symbol} (≈ ${fee_usd})
Remaining:      {remaining_balance} {symbol}
---------- Server Confirmation ----------
{confirm_message}
===============================================
Reply "confirm" to execute, "cancel" to abort, or describe changes.
```

### ERC20 / SPL Token Transfer

```
========== Transaction Confirmation ==========
Chain:          {chain_name}
Type:           ERC20 token transfer
From:           {from_address}
To:             {to_address}
Amount:         {amount} {token_symbol}
Contract:       {token_address}
---------- Balance ----------
{token_symbol} Balance: {token_balance} (Sufficient ✅)
{gas_symbol} Balance (Gas): {gas_balance} (Sufficient ✅)
---------- Fees ----------
Estimated Gas:  {estimated_fee} {gas_symbol} (≈ ${fee_usd})
Remaining:      {remaining_token} {token_symbol} / {remaining_gas} {gas_symbol}
---------- Server Confirmation ----------
{confirm_message}
===============================================
Reply "confirm" to execute, "cancel" to abort, or describe changes.
```

---

## Address Validation

| Chain Type | Format | Regex |
|------------|--------|-------|
| EVM (eth/bsc/polygon/...) | `0x` + 40 hex chars (42 total) | `^0x[0-9a-fA-F]{40}$` |
| Solana | Base58, 32-44 chars | `^[1-9A-HJ-NP-Za-km-z]{32,44}$` |

Validation failure -> Reject transfer with format guidance. Same-address warning -> Confirm intentional operation.

---

## Supported Chains

| Chain ID | Network | Gas Token | Block Explorer |
|----------|---------|-----------|----------------|
| `eth` | Ethereum | ETH | etherscan.io |
| `bsc` | BNB Smart Chain | BNB | bscscan.com |
| `polygon` | Polygon | MATIC | polygonscan.com |
| `arbitrum` | Arbitrum One | ETH | arbiscan.io |
| `optimism` | Optimism | ETH | optimistic.etherscan.io |
| `avax` | Avalanche C-Chain | AVAX | snowtrace.io |
| `base` | Base | ETH | basescan.org |
| `sol` | Solana | SOL | solscan.io |

---

## Conversation Examples

**Example 1 (Happy Path): Successful ETH transfer**
User: "Send 0.5 ETH to 0xDEF...5678"
Agent:
1. Verify auth -> call `dex_wallet_get_addresses` -> get `from_address`.
2. Call `dex_wallet_get_token_list` -> check ETH balance.
3. Call `dex_tx_gas` -> estimate gas fee.
4. Validate: 0.5 + gas <= ETH balance.
5. Call `dex_tx_transfer_preview` -> display confirmation template.
6. User replies "confirm".
7. Run terminal [tx-checkin.md](./tx-checkin.md) with preview **`txBundle`** -> `-tx-bundle-file` -> success required.
8. Call `dex_wallet_sign_transaction` with **`unsigned_tx_hex`** -> call `dex_tx_send_raw_transaction`.
9. Display tx hash + etherscan link + post-transfer suggestions.

**Example 2 (Happy Path): ERC20 transfer with full details**
User: "Send 100 USDT to 0xABC...1234 on Ethereum"
Agent:
1. Verify auth -> get wallet address for ETH chain.
2. Call `dex_wallet_get_token_list({ chain: "eth" })` -> verify USDT balance >= 100 AND ETH balance >= gas fee.
3. Call `dex_tx_gas` -> estimate gas.
4. Call `dex_tx_transfer_preview` -> display ERC20 confirmation template.
5. User replies "confirm".
6. Run terminal [tx-checkin.md](./tx-checkin.md) with preview **`txBundle`** -> `-tx-bundle-file` -> success required.
7. Call `dex_wallet_sign_transaction` with **`unsigned_tx_hex`** -> call `dex_tx_send_raw_transaction`.
8. Display tx hash + explorer link + post-transfer suggestions.

**Example 3 (Happy Path): Solana native transfer**
User: "Send 2 SOL to BTYz...bfxE"
Agent:
1. Verify auth -> get Solana wallet address.
2. Call `dex_wallet_get_token_list({ chain: "sol" })` -> verify SOL balance >= 2 + gas.
3. Call `dex_tx_transfer_preview({ chain: "sol", token_address: "native", amount: "2", ... })`.
4. Display confirmation. On confirm -> terminal [tx-checkin.md](./tx-checkin.md) with **`txBundle`** (`-tx-bundle-file`) -> sign (`unsigned_tx_hex`) -> broadcast -> display tx hash + solscan link.

**Example 4 (Happy Path): SPL token transfer (e.g., USDC on Solana)**
User: "Transfer 50 USDC to my friend's Solana address BTYz..."
Agent:
1. Verify auth -> get Solana address.
2. Call `dex_wallet_get_token_list({ chain: "sol" })` -> verify USDC balance >= 50 AND SOL >= gas + ATA rent.
3. Call `dex_tx_transfer_preview` with token mint address.
4. Display confirmation including note about possible ATA creation fee.
5. On confirm -> terminal [tx-checkin.md](./tx-checkin.md) with **`txBundle`** -> sign (`unsigned_tx_hex`) -> broadcast.

**Example 5 (Happy Path): Transfer on L2 (Arbitrum)**
User: "Send 200 USDT to 0xDEF... on Arbitrum"
Agent:
1. Get wallet address (same as ETH — EVM chains share address).
2. Check USDT balance on Arbitrum and ETH balance for gas.
3. Build preview, display confirmation with Arbitrum-specific gas estimate.
4. On confirm -> terminal [tx-checkin.md](./tx-checkin.md) with **`txBundle`** -> sign (`unsigned_tx_hex`) -> broadcast -> display arbiscan link.

**Example 6 (Edge Case): Insufficient token balance**
User: "Transfer 1000 USDT on Ethereum"
Agent:
1. Call `dex_wallet_get_token_list` -> USDT balance is 800.
2. Abort: "Insufficient balance. You have 800 USDT but need 1000 USDT. Please reduce the amount or top up first."
3. Suggest: "You can check your balances on other chains or swap tokens to get more USDT."

**Example 7 (Edge Case): Insufficient gas token**
User: "Send 100 USDT to 0xDEF... on Ethereum"
Agent:
1. Call `dex_wallet_get_token_list` -> USDT balance is 200 (sufficient), ETH balance is 0.0001 (insufficient for gas).
2. Abort: "Insufficient gas. You need approximately 0.003 ETH for gas but only have 0.0001 ETH. Please acquire more ETH for gas fees."

**Example 8 (Edge Case): Missing parameters — vague request**
User: "I want to send some tokens"
Agent:
1. Identify intent: transfer, but missing recipient, amount, and token.
2. Reply: "Please provide: recipient address, transfer amount, and token (e.g., ETH, USDT). Optionally specify the chain (default Ethereum)."

**Example 9 (Edge Case): Missing only the chain**
User: "Send 50 USDT to 0xABC..."
Agent:
1. Chain not specified. Default to Ethereum.
2. Optionally ask: "I'll default to Ethereum. Would you like to send on a different chain (e.g., Arbitrum, BSC)?"

**Example 10 (Edge Case): Invalid address format**
User: "Send 1 ETH to abc123"
Agent:
1. Validate address: "abc123" does not match EVM (`0x` + 40 hex) or Solana (Base58) format.
2. Reject: "Invalid address format. EVM addresses start with 0x and are 42 characters. Solana addresses are 32-44 Base58 characters. Please check and retry."

**Example 11 (Edge Case): Sender == recipient**
User: "Send 1 ETH to 0x... (same as own address)"
Agent:
1. Detect sender and recipient are identical.
2. Warn: "The recipient address is the same as your wallet address. Are you sure you want to proceed? This will only consume gas without moving tokens."

**Example 12 (Edge Case): User cancels confirmation**
User: (After seeing confirmation) "cancel"
Agent:
1. Immediately abort. No signing or broadcasting occurs.
2. Reply: "Transfer cancelled. No transaction was signed or broadcast."

**Example 13 (Edge Case): User modifies parameters after preview**
User: (After seeing confirmation) "Change the amount to 0.3 ETH"
Agent:
1. Return to parameter collection with updated amount.
2. Re-run balance check, gas estimation, and preview with new amount.

**Example 14 (Edge Case): Batch transfer**
User: "Send 100 USDT to 0xAAA..., 200 USDT to 0xBBB..., and 50 USDT to 0xCCC..."
Agent:
1. Parse 3 transfer intents.
2. Process each sequentially with individual confirmations.
3. Display summary table at end.

**Example 15 (Boundary Case): Not this module — swap request**
User: "Swap ETH for USDT"
Agent: This is a swap operation. Route to `gate-dex-trade`.

**Example 16 (Boundary Case): Not this module — DApp interaction**
User: "Connect my wallet to Uniswap"
Agent: This is a DApp interaction. Route to [dapp.md](./dapp.md).

**Example 17 (Boundary Case): Not this module — x402 payment**
User: "Pay for this API endpoint"
Agent: This is an x402 payment. Route to [x402.md](./x402.md).

**Example 18 (Boundary Case): Not this module — balance check only**
User: "How much ETH do I have?"
Agent: This is a balance query, not a transfer. Route to [asset-query.md](./asset-query.md).

---

## Post-Transfer Suggestions

After a successful transfer, **proactively display next actions**. This template is paired with the Follow-up Routing Table below.

**After successful single transfer:**
```
✅ Transfer broadcast successfully!
Tx Hash: {hash_id}
Explorer: https://{explorer}/tx/{hash_id}
Transaction submitted. Confirmation time depends on network congestion.

You can:
- Check your updated balance
- View transaction details on block explorer
- Make another transfer
- Swap tokens on DEX
```

**After successful batch transfer:**
```
✅ Batch transfer complete! {success_count}/{total_count} transfers succeeded.
See the summary table above for individual tx hashes.

You can:
- Check your updated balances
- View details of any specific transaction
- Make additional transfers
- Swap tokens on DEX
```

**After user cancels transfer:**
```
Transfer cancelled. No transaction was signed or broadcast.

You can:
- Start a new transfer with different parameters
- Check your current balances
- Swap tokens instead
```

**After transfer fails (balance insufficient):**
```
Transfer could not proceed due to insufficient balance.

You can:
- Check your balances across all chains
- Swap tokens to acquire the needed asset
- Try a smaller transfer amount
```

### Follow-up Routing Table

| User Follow-up Intent | Target |
|------------------------|--------|
| View updated balance | [asset-query.md](./asset-query.md) (`dex_wallet_get_token_list`) |
| View transaction details / history | [asset-query.md](./asset-query.md) (`dex_tx_detail`, `dex_tx_list`) |
| Continue transferring to other addresses | Stay in this module |
| Swap tokens | `gate-dex-trade` |
| Pay for a 402 resource | [x402.md](./x402.md) |
| Interact with a DApp | [dapp.md](./dapp.md) |
| Login / auth expired | [auth.md](./auth.md) |
| Check token prices | `gate-dex-market` |
| Use CLI commands | [cli.md](./cli.md) |

---

## Error Handling

| Scenario | Handling |
|----------|----------|
| Not logged in / `mcp_token` missing | Attempt silent refresh via `dex_auth_refresh_token`; on failure route to [auth.md](./auth.md) |
| Token expired mid-transfer | Attempt silent refresh; on failure route to re-login, preserve transfer intent for retry |
| Transfer token balance insufficient | Abort; show current balance vs. required amount; suggest reducing amount or topping up |
| Gas token balance insufficient | Abort; display gas token shortfall; suggest acquiring gas tokens |
| Invalid recipient address format | Refuse to initiate; show correct format for the target chain |
| Recipient == sender | Warn user; confirm if intentional |
| `dex_tx_gas` estimation failed | Display error; suggest retry later (possible network congestion or contract issue) |
| `dex_tx_transfer_preview` failed | Display server error; do not silently retry |
| `dex_wallet_sign_transaction` failed | Display signing error; do not auto-retry |
| `dex_tx_send_raw_transaction` failed | Display broadcast error (nonce conflict, gas too low, network congestion); suggest action based on error type |
| User cancels confirmation | Immediately abort; do not sign or broadcast |
| Amount is 0 or negative | Refuse to execute; prompt for a valid positive amount |
| Amount exceeds token precision | Prompt precision limit; auto-truncate or ask user to correct |
| Token not available on target chain | Prompt that the token doesn't exist on the target chain; suggest the correct chain |
| Unsupported chain | Show supported chain list from Supported Chains table |
| Broadcast succeeds but tx unconfirmed | Inform user tx submitted; confirmation depends on network |
| Network interruption after signing | Inform signed tx can be broadcast later; do not discard |
| Batch transfer partial failure | Mark failed transfers, continue remaining; show summary at end |

---

## Security Rules

1. **Token confidentiality**: Never display `mcp_token` in plaintext.
2. **Account ID masking**: Show only partial `account_id` characters in user-facing output.
3. **Silent refresh**: Attempt `dex_auth_refresh_token` before routing to re-login.
4. **Mandatory balance validation**: Always validate balance (token + gas) before transfer. Never initiate signing when balance is insufficient.
5. **Mandatory user confirmation**: Before signing, display a complete confirmation summary and get an explicit "confirm" reply. Never skip, simplify, or auto-confirm.
6. **Individual confirmation for batches**: Each transaction in a batch must be confirmed individually.
7. **No auto-retry on failure**: After signing or broadcast failure, display the error clearly. Never auto-retry in the background.
8. **Address validation**: Validate recipient address format before sending to prevent asset loss.
9. **MCP Server required**: Abort all operations if connection detection fails.
10. **Transparent errors**: Display all MCP Server errors truthfully without modification.
11. **Raw tx confidentiality**: `raw_tx` hex data flows only between Agent and MCP Server — never display to users.
12. **Broadcast immediately after signing**: Do not hold signed transactions for extended periods.
