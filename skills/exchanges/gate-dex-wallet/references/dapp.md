---
name: gate-dex-dapp
description: "Gate Wallet interaction with external DApps. Connect wallet, sign messages (EIP-712/personal_sign),
  sign and send DApp-generated transactions, ERC20 Approve authorization. Use when users need to interact with DeFi protocols, NFT platforms,
  or any DApp. Includes transaction confirmation gating and security review."
---

# Gate DEX DApp

> DApp Interaction Domain — Connect wallet, sign messages, execute DApp transactions, ERC20 Approve authorization, with mandatory confirmation gating and contract security review. 4 MCP tools + cross-Skill calls.

**Trigger Scenarios**: When user mentions "connect DApp", "sign message", "authorization", "approve", "DApp interaction", "NFT mint", "DeFi operation", "add liquidity", "stake", "claim", "contract call", or when other Skills guide users to perform DApp-related operations.

## MCP Server Connection Detection

### First Session Detection

**Before the first MCP tool call in a session, perform a connection probe to confirm Gate Wallet MCP Server availability. Subsequent operations do not require repeated detection.**

```
CallMcpTool(server="gate-wallet", toolName="chain.config", arguments={chain: "eth"})
```

| Result | Handling |
|--------|----------|
| Success | MCP Server available, subsequent operations call business tools directly without re-probing |
| Failure | Display configuration guidance based on error type (see error handling below) |

### Runtime Error Fallback

If business tool calls fail during subsequent operations (connection errors, timeouts, etc.), handle according to these rules:

| Error Type | Keywords | Handling |
|------------|----------|----------|
| MCP Server not configured | `server not found`, `unknown server` | Display MCP Server configuration guidance |
| Remote service unreachable | `connection refused`, `timeout`, `DNS error` | Prompt to check server status and network connection |
| Authentication failed | `401`, `unauthorized`, `x-api-key` | Prompt to contact administrator for API Key |
## Authentication Notes

All operations in this Skill **require `mcp_token`**. Before calling any tool, confirm the user is logged in.

- If no `mcp_token` available → Guide to `gate-dex-auth` to complete login, then return.
- If `mcp_token` expired (MCP Server returns token expiration error) → First try `auth.refresh_token` for silent refresh, if failed then guide to re-login.

## DApp Interaction Scenarios Overview

| Scenario | Description | Core MCP Tool |
|----------|-------------|---------------|
| Wallet Connection | DApp requests wallet address | `wallet.get_addresses` |
| Message Signing | DApp login verification / EIP-712 typed data signing | `wallet.sign_message` |
| DApp Transaction Execution | Execute DApp-generated on-chain transactions (mint, stake, claim...) | `wallet.sign_transaction` → `tx.send_raw_transaction` |
| ERC20 Approve | Authorize DApp contract to use specified tokens | `wallet.sign_transaction` → `tx.send_raw_transaction` |

## MCP Tool Call Specifications

### 1. `wallet.get_addresses` (Cross-Skill Call) — Get Wallet Addresses

Get wallet addresses for the account on various chains, used for DApp connection. This tool belongs to the `gate-dex-wallet` domain, called cross-Skill here.

| Field | Description |
|-------|-------------|
| **Tool Name** | `wallet.get_addresses` |
| **Parameters** | `{ account_id: string, mcp_token: string }` |
| **Return Value** | `{ addresses: { [chain: string]: string } }` |

Call Example:

```
CallMcpTool(
  server="gate-wallet",
  toolName="wallet.get_addresses",
  arguments={ account_id: "acc_12345", mcp_token: "<mcp_token>" }
)
```

Return Example:

```json
{
  "addresses": {
    "eth": "0xABCdef1234567890ABCdef1234567890ABCdef12",
    "bsc": "0xABCdef1234567890ABCdef1234567890ABCdef12",
    "sol": "7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU"
  }
}
```

Agent Behavior: EVM chains share the same address. Provide the target chain address to DApp to complete wallet connection.

---

### 2. `wallet.sign_message` — Sign Message

Sign arbitrary messages using server-hosted private keys, supporting personal_sign and EIP-712 typed data signing.

| Field | Description |
|-------|-------------|
| **Tool Name** | `wallet.sign_message` |
| **Parameters** | `{ message: string, chain: string, account_id: string, mcp_token: string }` |
| **Return Value** | `{ signature: string }` |

Parameter Description:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `message` | Yes | Message to sign. For personal_sign pass raw text, for EIP-712 pass JSON string |
| `chain` | Yes | Chain identifier (e.g., `"eth"`, `"bsc"`) |
| `account_id` | Yes | User account ID |
| `mcp_token` | Yes | Authentication token |

Call Example (personal_sign):

```
CallMcpTool(
  server="gate-wallet",
  toolName="wallet.sign_message",
  arguments={
    message: "Welcome to Uniswap! Sign this message to verify your wallet. Nonce: abc123",
    chain: "eth",
    account_id: "acc_12345",
    mcp_token: "<mcp_token>"
  }
)
```

Call Example (EIP-712):

```
CallMcpTool(
  server="gate-wallet",
  toolName="wallet.sign_message",
  arguments={
    message: "{\"types\":{\"EIP712Domain\":[{\"name\":\"name\",\"type\":\"string\"}],\"Permit\":[{\"name\":\"owner\",\"type\":\"address\"},{\"name\":\"spender\",\"type\":\"address\"},{\"name\":\"value\",\"type\":\"uint256\"}]},\"primaryType\":\"Permit\",\"domain\":{\"name\":\"USDC\"},\"message\":{\"owner\":\"0xABC...\",\"spender\":\"0xDEF...\",\"value\":\"1000000000\"}}",
    chain: "eth",
    account_id: "acc_12345",
    mcp_token: "<mcp_token>"
  }
)
```

Return Example:

```json
{
  "signature": "0x1234abcd...ef5678"
}
```

Agent Behavior: Display the message content to user before signing, explain the signing purpose. Return the signature to user after completion.

---

### 3. `wallet.sign_transaction` — Sign DApp Transaction

Sign unsigned transactions built by DApp using server-hosted private keys. **Only call after user explicitly confirms**.

| Field | Description |
|-------|-------------|
| **Tool Name** | `wallet.sign_transaction` |
| **Parameters** | `{ raw_tx: string, chain: string, account_id: string, mcp_token: string }` |
| **Return Value** | `{ signed_tx: string }` |

Parameter Description:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `raw_tx` | Yes | Serialized unsigned transaction data (hex format) |
| `chain` | Yes | Chain identifier |
| `account_id` | Yes | User account ID |
| `mcp_token` | Yes | Authentication token |

Call Example:

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

Return Example:

```json
{
  "signed_tx": "0x02f8b2...signed..."
}
```

---

### 4. `tx.send_raw_transaction` — Broadcast Signed Transaction

Broadcast signed DApp transaction to the blockchain network.

| Field | Description |
|-------|-------------|
| **Tool Name** | `tx.send_raw_transaction` |
| **Parameters** | `{ signed_tx: string, chain: string, mcp_token: string }` |
| **Return Value** | `{ hash_id: string }` |

Parameter Description:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `signed_tx` | Yes | Signed transaction returned by `wallet.sign_transaction` |
| `chain` | Yes | Chain identifier |
| `mcp_token` | Yes | Authentication token |

Call Example:

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

Return Example:

```json
{
  "hash_id": "0xa1b2c3d4e5f6...7890"
}
```

## Supported DApp Interaction Types

| Type | Example Scenarios | Description |
|------|-------------------|-------------|
| DeFi Liquidity | Uniswap add/remove liquidity | Build Router contract addLiquidity / removeLiquidity calls |
| DeFi Lending | Aave deposit/borrow/repay | Build Pool contract supply / borrow / repay calls |
| DeFi Staking | Lido stake ETH | Build stETH contract submit call |
| NFT Mint | Custom NFT minting | Build mint contract call |
| NFT Trading | Buy/sell NFT | Build Marketplace contract call |
| Token Approve | Authorize any contract to use tokens | Build ERC20 approve(spender, amount) calldata |
| Arbitrary Contract Call | User provides ABI + parameters | Agent encodes calldata and builds transaction |
| Message Signing | DApp login verification | `wallet.sign_message`, no on-chain transaction needed |

## Supported Chains

| Chain ID | Network Name | Type | Native Gas Token | Block Explorer |
|----------|--------------|------|------------------|----------------|
| `eth` | Ethereum | EVM | ETH | etherscan.io |
| `bsc` | BNB Smart Chain | EVM | BNB | bscscan.com |
| `polygon` | Polygon | EVM | MATIC | polygonscan.com |
| `arbitrum` | Arbitrum One | EVM | ETH | arbiscan.io |
| `optimism` | Optimism | EVM | ETH | optimistic.etherscan.io |
| `avax` | Avalanche C-Chain | EVM | AVAX | snowtrace.io |
| `base` | Base | EVM | ETH | basescan.org |
| `sol` | Solana | Non-EVM | SOL | solscan.io |

## Skill Routing

Route to corresponding Skill based on user intent after DApp operation completion:

| User Intent | Route Target |
|-------------|--------------|
| View updated balance | `gate-dex-wallet` |
| View transaction details / history | `gate-dex-wallet` (`tx.detail`, `tx.list`) |
| View contract security info | `gate-dex-market` (`token_get_risk_info`) |
| Transfer tokens | `gate-dex-transfer` |
| Swap tokens | `gate-dex-trade` |
| Login / Authentication expired | `gate-dex-auth` |

## Operation Flows

### Flow A: DApp Wallet Connection

```
Step 0: MCP Server Connection Detection
  Call chain.config({chain: "eth"}) to probe availability
  ↓ Success

Step 1: Authentication Check
  Confirm valid mcp_token and account_id
  No token → Guide to gate-dex-auth for login
  ↓

Step 2: Get Wallet Address
  Call wallet.get_addresses({ account_id, mcp_token })
  Extract target chain address
  ↓

Step 3: Display Address

  ────────────────────────────
  🔗 Wallet Connection Info

  Chain: {chain_name}
  Address: {address}

  Please use this address for DApp connection.
  EVM chains (Ethereum/BSC/Polygon etc.) share the same address.
  ────────────────────────────
```

### Flow B: Message Signing

```
Step 0: MCP Server Connection Detection
  ↓ Success

Step 1: Authentication Check
  ↓

Step 2: Intent Recognition + Parameter Collection
  Extract signing request from user input:
  - message: Content to sign (required)
  - chain: Target chain (optional, default eth)
  - Signing type: personal_sign or EIP-712 (auto-detect from message format)
  ↓

Step 3: Display Signing Content Confirmation

  ────────────────────────────
  ✍️ Message Signing Request

  Chain: {chain_name}
  Signing Type: {personal_sign / EIP-712}
  Content to Sign:
  {message_content}

  This signature will not create an on-chain transaction, no Gas consumed.
  Reply "confirm" to sign, "cancel" to abort.
  ────────────────────────────

  ↓ User confirms

Step 4: Execute Signing
  Call wallet.sign_message({ message, chain, account_id, mcp_token })
  ↓

Step 5: Display Signing Result

  ────────────────────────────
  ✅ Signing Complete

  Signature: {signature}

  Please submit this signature to DApp to complete verification.
  ────────────────────────────
```

### Flow C: DApp Transaction Execution (Main Flow)

```
Step 0: MCP Server Connection Detection
  Call chain.config({chain: "eth"}) to probe availability
  ↓ Success

Step 1: Authentication Check
  Confirm valid mcp_token and account_id
  No token → Guide to gate-dex-auth for login
  ↓

Step 2: Intent Recognition + Parameter Collection
  Extract DApp operation intent from user input:
  - Operation type (e.g., "add liquidity", "stake ETH", "mint NFT")
  - Target protocol/contract (e.g., Uniswap, Aave, Lido)
  - Amount and token
  - Chain (optional, can be inferred from context)

  When parameters are missing, ask user one by one:

  ────────────────────────────
  Please provide DApp interaction info:
  - Operation: (required, e.g., "add ETH-USDC liquidity on Uniswap")
  - Chain: (optional, default Ethereum)
  - Amount: (may need multiple amounts depending on operation type)
  ────────────────────────────

  ↓ Parameters complete

Step 3: Get Wallet Info (Cross-Skill: gate-dex-wallet)
  Call wallet.get_addresses({ account_id, mcp_token }) → Get from_address
  Call wallet.get_token_list({ account_id, chain, mcp_token }) → Get balance
  ↓

Step 4: Security Review (Recommended Step)
  Call token_get_risk_info({ chain, address: contract_address }) (Cross-Skill: gate-dex-market)
  Evaluate contract risk level
  ↓

Step 5: Agent Builds Transaction
  Based on DApp operation type, Agent encodes contract call calldata:
  a) Known protocols (Uniswap/Aave/Lido etc.): Encode according to protocol ABI
  b) User provides ABI + parameters: Agent parses and encodes
  c) User provides complete calldata: Use directly

  Build transaction parameters:
  - to: Contract address
  - data: calldata
  - value: Native token amount to send (if any)
  ↓

Step 6: Determine if Approve is Needed
  If operation involves ERC20 tokens (non-native tokens):
  - Check if current allowance is sufficient
  - Insufficient → Execute Approve transaction first (see Flow D)
  ↓

Step 7: Agent Balance Verification (Mandatory)
  Verification rules:
  a) Operation involves native token: native_balance >= amount + estimated_gas
  b) Operation involves ERC20 token: token_balance >= amount AND native_balance >= estimated_gas
  c) Gas only: native_balance >= estimated_gas

  Verification failed → Abort transaction:

  ────────────────────────────
  ❌ Insufficient Balance, Cannot Execute DApp Operation

  Required {symbol}: {required_amount}
  Current Balance: {current_balance}
  Shortfall: {shortfall}

  Suggestions:
  - Reduce operation amount
  - Deposit tokens to wallet first
  ────────────────────────────

  ↓ Verification passed

Step 8: Display DApp Transaction Confirmation Summary (Mandatory Gating)
  Display content see "DApp Transaction Confirmation Template" below.
  Must wait for user to explicitly reply "confirm" before continuing.
  ↓

  User replies "confirm" → Continue to Step 9
  User replies "cancel" → Abort transaction
  User requests modification → Return to Step 2

Step 9: Sign Transaction
  Call wallet.sign_transaction({ raw_tx, chain, account_id, mcp_token })
  Get signed_tx
  ↓

Step 10: Broadcast Transaction
  Call tx.send_raw_transaction({ signed_tx, chain, mcp_token })
  Get hash_id
  ↓

Step 11: Display Result + Follow-up Suggestions

  ────────────────────────────
  ✅ DApp Transaction Broadcast Successfully!

  Operation: {operation_description}
  Transaction Hash: {hash_id}
  Block Explorer: https://{explorer}/tx/{hash_id}

  Transaction submitted to network, confirmation time depends on network congestion.

  You can:
  - View updated balance
  - View transaction details
  - Continue other operations
  ────────────────────────────
```

### Flow D: ERC20 Approve Authorization

```
Step 0: MCP Server Connection Detection
  ↓ Success

Step 1: Authentication Check
  ↓

Step 2: Determine Approve Parameters
  - token_address: Token contract address to authorize
  - spender: Authorized contract address (e.g., Uniswap Router)
  - amount: Authorization amount

  Agent recommends using exact amount instead of unlimited:

  ────────────────────────────
  💡 Authorization Amount Recommendation

  This operation requires authorizing {spender_name} to use your {token_symbol}.

  Recommended options:
  1. Exact authorization: {exact_amount} {token_symbol} (only enough for this operation, more secure)
  2. Unlimited authorization: unlimited (no need to re-authorize for future operations, but higher risk)

  Please choose authorization method, or specify a custom amount.
  ────────────────────────────

  ↓

Step 3: Build Approve Calldata
  Encode ERC20 approve(spender, amount) function call:
  - function selector: 0x095ea7b3
  - spender: Contract address (32 bytes padded)
  - amount: Authorization amount (uint256)
  ↓

Step 4: Display Approve Confirmation

  ────────────────────────────
  ========== Token Authorization Confirmation ==========
  Chain: {chain_name}
  Token: {token_symbol} ({token_address})
  Authorize to: {spender_name} ({spender_address})
  Authorization Amount: {amount} {token_symbol}
  Estimated Gas: {estimated_gas} {gas_symbol}
  ===============================
  Reply "confirm" to execute authorization, "cancel" to abort.
  ────────────────────────────

  ↓ User confirms

Step 5: Sign + Broadcast Approve Transaction
  Call wallet.sign_transaction({ raw_tx: approve_tx, chain, account_id, mcp_token })
  Call tx.send_raw_transaction({ signed_tx, chain, mcp_token })
  ↓

Step 6: Approve Success
  Display Approve transaction hash, continue with subsequent DApp operation (Flow C Step 9)
```

### Flow E: Arbitrary Contract Call (User Provides ABI)

```
Step 0: MCP Server Connection Detection
  ↓ Success

Step 1: Authentication Check
  ↓

Step 2: Collect Contract Call Information
  User provides:
  - Contract address
  - Function name or ABI
  - Function parameters
  - value (optional, required when sending native tokens)
  - Chain
  ↓

Step 3: Agent Encodes Calldata
  Encode function call data based on ABI and parameters
  ↓

Step 4: Security Review + Balance Verification + Confirmation Gating
  Same as Flow C Step 4 ~ Step 8
  ↓

Step 5: Sign + Broadcast
  Same as Flow C Step 9 ~ Step 11
```

## DApp Transaction Confirmation Template

**Before user explicitly replies "confirm", Agent must not execute signing operation. This is a mandatory gating that cannot be skipped.**

### Standard DApp Transaction Confirmation

```
========== DApp Transaction Confirmation ==========
Chain: {chain_name}
DApp/Protocol: {protocol_name} (e.g., Uniswap V3)
Operation: {operation} (e.g., Add Liquidity)
Contract Address: {contract_address}
---------- Transaction Details ----------
{operation_specific_details}
(e.g., Token A: 0.5 ETH, Token B: 1000 USDC)
---------- Authorization Info ----------
{approve_info_if_needed}
(e.g., Approve Required: USDC → Uniswap Router, Amount: 1000 USDC)
(When no authorization needed: No additional authorization required)
---------- Balance Info ----------
{token_symbol} Balance: {balance} (Sufficient ✅ / Insufficient ❌)
{gas_symbol} Balance (Gas): {gas_balance} (Sufficient ✅)
---------- Fee Info ----------
Estimated Gas (Approve): {approve_gas} (if needed)
Estimated Gas (Transaction): {tx_gas} {gas_symbol}
---------- Security Check ----------
Contract Security Audit: {risk_level} (e.g., Audited/Low Risk/High Risk/Unknown)
===============================
Reply "confirm" to execute, "cancel" to abort, or specify modifications.

Note: DApp interaction involves smart contract calls, please confirm contract address and operation are correct.
```

### Unknown Contract Warning Confirmation

When target contract is not security audited or audit result is high risk:

```
========== ⚠️ DApp Transaction Confirmation (Security Warning) ==========
Chain: {chain_name}
Contract Address: {contract_address}

⚠️ Security Warning: This contract is not security audited or marked as high risk.
Interacting with unknown contracts may result in asset loss. Please confirm you trust this contract.

---------- Transaction Details ----------
{operation_details}
---------- Balance Info ----------
{balance_info}
---------- Fee Info ----------
{gas_info}
---------- Security Check ----------
Contract Audit Status: {risk_detail}
=================================================
Reply "confirm" to proceed anyway (at your own risk), "cancel" to abort.
```

## Cross-Skill Workflows

### Complete DApp Interaction Flow (From Login to Completion)

```
gate-dex-auth (Login, get mcp_token + account_id)
  → gate-dex-wallet (wallet.get_addresses → Get address)
    → gate-dex-wallet (wallet.get_token_list → Verify balance)
      → gate-dex-market (token_get_risk_info → Contract security review)
        → gate-dex-dapp (Approve? → Confirm → Sign → Broadcast)
          → gate-dex-wallet (View updated balance)
```

### DApp Message Signing (No Transaction Needed)

```
gate-dex-auth (Login)
  → gate-dex-dapp (wallet.sign_message → Return signature result)
```

### Guided by Other Skills

| Source Skill | Scenario | Description |
|--------------|----------|-------------|
| `gate-dex-wallet` | User wants to connect DApp after viewing address | Carries account_id and address info |
| `gate-dex-market` | User wants to participate in DeFi after viewing token | Carries token and chain context |
| `gate-dex-trade` | User wants to further participate in DeFi after Swap | Carries chain and token context |

### Calling Other Skills

| Target Skill | Call Scenario | Tool Used |
|--------------|---------------|-----------|
| `gate-dex-wallet` | Get wallet address for DApp connection | `wallet.get_addresses` |
| `gate-dex-wallet` | Verify balance before DApp transaction | `wallet.get_token_list` |
| `gate-dex-wallet` | View updated balance after DApp transaction | `wallet.get_token_list` |
| `gate-dex-auth` | Not logged in or token expired | `auth.refresh_token` or complete login flow |
| `gate-dex-market` | Contract security review | `token_get_risk_info` |
| `gate-dex-wallet` | View transaction details after DApp transaction | `tx.detail`, `tx.list` |

## Contract Address Validation Rules

Contract address validation for DApp transactions and Approve:

| Chain Type | Format Requirements | Validation Rules |
|------------|---------------------|------------------|
| EVM (eth/bsc/polygon/...) | Starts with `0x`, 40 hex characters (42 total) | Regex `^0x[0-9a-fA-F]{40}$`, recommend EIP-55 checksum validation |
| Solana | Base58 encoded, 32-44 characters | Regex `^[1-9A-HJ-NP-Za-km-z]{32,44}$` |

When validation fails:

```
❌ Invalid Contract Address Format

Provided address: {user_input}
Expected format: {expected_format}

Please check if the address is correct, complete, and matches the target chain.
```

## ERC20 Approve Calldata Encoding Specification

When Agent builds Approve transaction, encode calldata according to these rules:

```
Function signature: approve(address spender, uint256 amount)
Selector: 0x095ea7b3

Calldata structure:
0x095ea7b3
+ spender address (32 bytes, left-padded with zeros)
+ amount (32 bytes, uint256)

Example (approve Uniswap Router to use 1000 USDT, 6 decimals):
0x095ea7b3
000000000000000000000000 68b3465833fb72A70ecDF485E0e4C7bD8665Fc45  ← spender
00000000000000000000000000000000000000000000000000000000 3B9ACA00  ← 1000 * 10^6
```

Exact authorization vs Unlimited authorization:

| Method | amount Value | Security | Convenience |
|--------|--------------|----------|-------------|
| Exact authorization | Actual required amount | High (expires when used) | Low (need to re-authorize each time) |
| Unlimited authorization | `2^256 - 1` (`0xfff...fff`) | Low (contract can transfer tokens anytime) | High (one-time authorization, permanently valid) |

**Recommend exact authorization**, unless user explicitly requests unlimited authorization.

## EIP-712 Signature Data Parsing Specification

When Agent displays EIP-712 signing requests, parse JSON structured data into human-readable format:

### Parsing Key Points

1. **Domain Info**: Extract `name`, `version`, `chainId`, `verifyingContract`, display in table format
2. **Primary Type**: Clearly indicate the main type of signing data (e.g., `Order`, `Permit`, `Vote`)
3. **Message Fields**: Display field by field, truncate `address` types, convert `uint256` types to human-readable values
4. **Known Type Recognition**:
   - `Permit` (EIP-2612) → Label as "Token Authorization Permit", highlight spender and value
   - `Order` (DEX Order) → Label as "Trade Order", highlight trading pair and amount
   - `Vote` (Governance Vote) → Label as "Governance Vote", highlight voting content

### Known EIP-712 Signature Types

| primaryType | Common Source | Risk Level | Description |
|-------------|---------------|------------|-------------|
| `Permit` | ERC-2612 tokens | Medium | Off-chain signature authorization, no Gas but grants spender permission to use tokens |
| `Order` | DEX (e.g., 0x, Seaport) | Medium | Represents trade order, can be executed on-chain after signing |
| `Vote` | Governance protocols (e.g., Compound) | Low | Governance voting |
| `Delegation` | Governance protocols | Low | Voting power delegation |
| Unknown type | Any DApp | High | Need extra warning for user to carefully review content |

## Edge Cases and Error Handling

| Scenario | Handling |
|----------|----------|
| MCP Server not configured | Abort all operations, display Cursor configuration guidance |
| MCP Server unreachable | Abort all operations, display network check prompt |
| Not logged in (no `mcp_token`) | Guide to `gate-dex-auth` to complete login, then auto-return to continue DApp operation |
| `mcp_token` expired | First try `auth.refresh_token` for silent refresh, if failed then guide to re-login |
| Gas token balance insufficient | Abort transaction/Approve, display Gas insufficient info, suggest deposit |
| Token to Approve not in holdings | Prompt user doesn't hold this token, Approve can execute but has no practical meaning. Confirm whether to continue |
| Spender contract is high risk | Strongly warn user, suggest cancel. If user insists, can still continue (requires re-confirmation) |
| Spender contract is unknown (not indexed) | Display "unknown contract" warning, prompt user to verify contract source |
| Contract address format invalid | Refuse to initiate transaction, prompt correct address format |
| `wallet.sign_message` failed | Display signing error info, possible causes: incorrect message format, account anomaly. Do not auto-retry |
| EIP-712 JSON parsing failed | Display raw JSON content, prompt format may be incorrect, ask user to confirm or re-obtain from DApp |
| `wallet.sign_transaction` failed | Display signing error, possible causes: invalid transaction data, account permission issues. Do not auto-retry |
| `tx.send_raw_transaction` failed | Display broadcast error (nonce conflict, insufficient gas, network congestion, etc.), suggest corresponding measures based on error type |
| User cancels confirmation (signing/transaction/Approve) | Abort immediately, do not execute any signing or broadcast. Display cancellation prompt, remain friendly |
| `tx.gas` estimation failed | Display error info, possible causes: contract call will revert, incorrect parameters. Suggest checking transaction data |
| Approve amount is 0 | Treat as "revoke authorization" operation, confirm with user whether to revoke authorization for this spender |
| User requests unlimited authorization | Display high risk warning template, require user second confirmation |
| Duplicate Approve for same spender | Prompt existing authorization, new Approve will override old authorization. Confirm whether to continue |
| Network disconnected after signing but before broadcast | Prompt signed transaction can still be broadcast later, suggest retry after network recovery |
| DApp provided raw_tx format abnormal | Refuse to sign, prompt transaction data format incorrect, suggest regenerating from DApp |
| Chain identifier not supported | Display supported chains list, ask user to re-select |
| Message signing request chain is Solana | Prompt Solana message signing not supported yet, only EVM chains supported |
| Network interruption | Display network error, suggest checking network and retry |

## Security Rules

1. **`mcp_token` Confidentiality**: Never display `mcp_token` in plaintext to user, use placeholder `<mcp_token>` in call examples only.
2. **`account_id` Masking**: When displaying to user, show only partial characters (e.g., `acc_12...89`).
3. **Token Auto-refresh**: When `mcp_token` expires, prioritize silent refresh, only require re-login if failed.
4. **Confirmation Required Before Signing**: All signing operations (message signing, transaction signing, Approve) **must** display complete content to user and receive explicit "confirm" reply before execution. Cannot skip, simplify, or auto-confirm.
5. **Contract Security Review**: When DApp interaction involves unknown contracts, **must** call `token_get_risk_info` for security review and display results to user. High-risk contracts require additional prominent warning.
6. **Default Exact Authorization**: ERC20 Approve defaults to exact authorization amount. Only use unlimited authorization when user explicitly requests, and **must** display unlimited authorization risk warning.
7. **EIP-712 Content Transparency**: EIP-712 signing requests must be fully parsed and displayed in human-readable format to user, cannot omit any key fields (especially `verifyingContract`, `spender`, amount-related fields).
8. **Mandatory Gas Balance Verification**: **Must** verify Gas token balance before DApp transaction and Approve, **prohibit** initiating signing and broadcast when balance insufficient.
9. **No Auto-retry for Failed Operations**: After signing or broadcast failure, clearly display error info to user, do not auto-retry in background.
10. **Prohibit Operations When MCP Server Not Configured or Unreachable**: If Step 0 connection detection fails, abort all subsequent steps.
11. **MCP Server Error Transparency**: Display all error messages returned by MCP Server to user truthfully, do not hide or alter.
12. **`raw_tx` Non-disclosure**: Unsigned transaction raw data only flows between Agent and MCP Server, do not display hex raw content to user.
13. **Broadcast Promptly After Signing**: Should broadcast immediately after successful signing, should not hold signed transaction for extended period.
14. **Permit Signature Risk Warning**: EIP-2612 Permit signature has no Gas consumption but is equivalent to authorization operation, must remind user to pay attention to spender and authorization amount.
15. **Phishing Prevention**: Agent does not proactively construct transactions or signing requests pointing to unknown contracts. All DApp interaction data should be provided by user or obtained from trusted sources.
