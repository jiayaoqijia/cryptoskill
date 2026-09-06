---
name: gate-dex-dapp
version: "2026.3.31-1"
updated: "2026-03-31"
description: "Gate Wallet DApp interaction module. Connect wallet, sign messages (EIP-712 / personal_sign), sign and send DApp-generated transactions, and manage ERC20 Approve authorizations. Includes mandatory confirmation gates, terminal tx-checkin before every signing MCP call, and contract security review."
---

# Gate DEX DApp

> DApp interaction module — connect wallet, sign messages, execute DApp transactions, and manage ERC20 Approve authorizations. Includes mandatory confirmation gates, **terminal tx-checkin before `dex_wallet_sign_message` and `dex_wallet_sign_transaction`**, and contract security review. 4 MCP tools + cross-skill calls.

## Applicable Scenarios

Use when the user wants to interact with external DApps:
- Connect wallet to a DApp: "connect to Uniswap", "link my wallet"
- Sign messages for DApp login: "sign this message", "verify my identity"
- Approve token spending: "approve USDC for Uniswap", "authorize contract"
- Revoke token approvals: "revoke approval", "remove authorization"
- Execute DeFi operations: "add liquidity", "stake ETH on Lido", "deposit to Aave", "borrow USDC"
- NFT operations: "mint NFT", "buy NFT on OpenSea"
- Arbitrary contract calls: "call this contract function", user provides ABI + params
- EIP-712 typed data signing: "sign this Permit", "sign typed data"

## Capability Boundaries

- Supports: Wallet connection, message signing (personal_sign + EIP-712), DApp transaction execution, ERC20 Approve/revoke, arbitrary contract calls
- Supported chains: eth, bsc, polygon, arbitrum, optimism, avax, base, sol
- Does **not** support: Token swap execution (-> `gate-dex-trade`), token transfers (-> [transfer.md](./transfer.md)), x402 payment / HTTP 402 (-> [x402.md](./x402.md)), market data queries (-> `gate-dex-market`)

**Prerequisites**: MCP Server available (see parent SKILL.md). All operations require `mcp_token`. If missing, route to [auth.md](./auth.md).

**Signing prerequisite**: After the user confirms the message or transaction, **always** run terminal [tx-checkin.md](./tx-checkin.md) **before** calling `dex_wallet_sign_message` or `dex_wallet_sign_transaction`. On check-in failure, abort. When an MCP preview returns **`txBundle`** (same shape as transfer preview), check-in **only** uses **`-tx-bundle-file`** with that string — do not build txbundle manually.

---

## MCP Tools

### 1. `dex_wallet_get_addresses` (Cross-Skill) — Get Wallet Addresses

Returns wallet addresses per chain. EVM chains share the same address.

| Field | Description |
|-------|-------------|
| **Parameters** | `{ account_id, mcp_token }` |
| **Returns** | `{ addresses: { [chain]: string } }` |

### 2. `dex_wallet_sign_message` — Sign Messages

Signs arbitrary messages using server-side custodial keys. Supports personal_sign and EIP-712. **Call only after** user confirmation **and** successful terminal [tx-checkin.md](./tx-checkin.md) (use `-message` / `-intent` per backend for the approved payload).

| Field | Description |
|-------|-------------|
| **Parameters** | `{ message, chain, account_id, mcp_token }` |
| **Returns** | `{ signature }` |

- `message`: Raw text for personal_sign, JSON string for EIP-712.
- Auto-detect signing type from message format.

### 3. `dex_wallet_sign_transaction` — Sign DApp Transactions

Signs unsigned transactions using server-side custodial keys. **Only call after explicit user confirmation and successful terminal** [tx-checkin.md](./tx-checkin.md).

| Field | Description |
|-------|-------------|
| **Parameters** | `{ raw_tx, chain, account_id, mcp_token }` |
| **Returns** | `{ signed_tx }` |

### 4. `dex_tx_send_raw_transaction` — Broadcast

Broadcasts signed transactions to the on-chain network.

| Field | Description |
|-------|-------------|
| **Parameters** | `{ signed_tx, chain, mcp_token }` |
| **Returns** | `{ hash_id }` |

---

## Supported DApp Interaction Types

| Type | Example Scenarios | Description |
|------|-------------------|-------------|
| DeFi Liquidity | Uniswap add/remove liquidity | Router contract addLiquidity / removeLiquidity |
| DeFi Lending | Aave deposit/borrow/repay | Pool contract supply / borrow / repay |
| DeFi Staking | Lido stake ETH | stETH contract submit |
| NFT Mint | Custom NFT minting | Mint contract calls |
| NFT Trading | Buy/sell NFTs | Marketplace contract calls |
| Token Approve | Authorize contracts to use tokens | ERC20 approve(spender, amount) |
| Arbitrary Contract Calls | User provides ABI + params | Agent encodes calldata |
| Message Signing | DApp login verification | `dex_wallet_sign_message` (no on-chain tx) |

---

## Operation Flows

### Flow A: Wallet Connection

```
Step 1: Auth check -> Step 2: dex_wallet_get_addresses -> Step 3: Display address
"Wallet Connection: Chain: {chain}, Address: {address}. EVM chains share the same address."
```

### Flow B: Message Signing

```
Step 1: Auth check
  |
Step 2: Collect parameters (message, chain, signing type auto-detected)
  |
Step 3: Display signing content confirmation (MANDATORY GATE)
  "Message Signing Request - Chain: {chain}, Type: {personal_sign / EIP-712}
   Content: {message}. This will not generate on-chain transactions or consume gas.
   Reply 'confirm' to sign, 'cancel' to abort."
  |
Step 4: Terminal tx-checkin (MANDATORY) — [tx-checkin.md](./tx-checkin.md); on failure abort
  |
Step 5: Call dex_wallet_sign_message -> get signature
  |
Step 6: Display signature result for user to submit to DApp
```

### Flow C: DApp Transaction Execution (Primary)

```
Step 1: Auth check
  |
Step 2: Collect parameters (operation type, protocol, amounts, chain)
  |
Step 3: Get wallet info (cross-skill)
  dex_wallet_get_addresses -> from_address
  dex_wallet_get_token_list -> balances
  |
Step 4: Security review (recommended)
  dex_token_get_risk_info({ chain, address: contract }) via gate-dex-market
  |
Step 5: Build transaction (Agent encodes calldata)
  a) Known protocols (Uniswap/Aave/Lido): encode by protocol ABI
  b) User provides ABI + params: parse and encode
  c) User provides complete calldata: use directly
  |
Step 6: Check if Approve needed
  If ERC20 token involved and allowance insufficient -> execute Flow D first
  |
Step 7: Balance validation (MANDATORY)
  a) Native tokens involved:  native_balance >= amount + gas
  b) ERC20 tokens involved:   token_balance >= amount AND native_balance >= gas
  c) Gas only:                native_balance >= gas
  Failed -> abort with shortfall details
  |
Step 8: Display confirmation (MANDATORY GATE)
  Show: chain, protocol, operation, contract, details, balance info, gas, security audit
  Wait for explicit "confirm".
  |
Step 9: Terminal tx-checkin (MANDATORY) — [tx-checkin.md](./tx-checkin.md); on failure abort
  |
Step 10: Sign -> Step 11: Broadcast -> Step 12: Display result
  "✅ DApp transaction broadcast successfully!
   Operation: {operation_description}
   Tx Hash: {hash_id}
   Explorer: https://{explorer}/tx/{hash_id}

   You can:
   - Check your updated balance
   - View transaction details
   - Continue with other DApp operations
   - View contract security info"
```

### Flow D: ERC20 Approve

```
Step 1: Determine approve params (token_address, spender, amount)
  |
Step 2: Recommend exact authorization over unlimited
  "Exact: {amount} (safer, sufficient for this operation)
   Unlimited: no re-authorization needed, but higher risk"
  |
Step 3: Build approve calldata
  Selector: 0x095ea7b3 + spender (32 bytes padded) + amount (uint256)
  |
Step 4: Display approve confirmation (MANDATORY GATE)
  Show: chain, token, spender, amount, gas estimate
  |
Step 5: Terminal tx-checkin (MANDATORY) — [tx-checkin.md](./tx-checkin.md); then sign + broadcast approve tx
  |
Step 6: Continue to main DApp operation (Flow C Step 9)
```

### Flow E: Arbitrary Contract Calls

```
Step 1: Collect contract info (address, function/ABI, params, value?, chain)
  |
Step 2: Encode calldata
  |
Step 3-5: Security review + balance validation + confirmation gate (same as Flow C Steps 4-8)
  |
Step 6: Terminal tx-checkin then sign + broadcast (same as Flow C Steps 9-12)
```

---

## DApp Transaction Confirmation Template

**MANDATORY gate — Agent must NOT sign before explicit user confirmation and successful terminal [tx-checkin.md](./tx-checkin.md).**

```
========== DApp Transaction Confirmation ==========
Chain:          {chain_name}
DApp/Protocol:  {protocol_name}
Operation:      {operation}
Contract:       {contract_address}
---------- Transaction Details ----------
{operation_specific_details}
---------- Approve Info ----------
{approve_info or "No additional approval needed"}
---------- Balance ----------
{token_symbol} Balance: {balance} (Sufficient ✅ / Insufficient ❌)
{gas_symbol} Balance (Gas): {gas_balance} (Sufficient ✅)
---------- Fees ----------
Estimated Gas (Approve): {approve_gas} (if needed)
Estimated Gas (Tx): {tx_gas} {gas_symbol}
---------- Security Check ----------
Contract Audit: {risk_level}
====================================================
Reply "confirm" to execute, "cancel" to abort, or describe changes.
```

### Unknown Contract Warning

When the contract is unaudited or flagged high-risk, prepend:

```
⚠️ SECURITY WARNING: This contract is unaudited or flagged as high-risk.
Interacting with unknown contracts may result in asset loss.
Confirm you trust this contract before proceeding.
```

---

## EIP-712 Signature Parsing

When displaying EIP-712 signatures, parse JSON into human-readable format:

1. **Domain**: Extract `name`, `version`, `chainId`, `verifyingContract`.
2. **Primary Type**: Display main type (e.g., `Permit`, `Order`, `Vote`).
3. **Message Fields**: Show field by field; truncate addresses; convert uint256 to readable numbers.

| primaryType | Source | Risk | Notes |
|-------------|--------|------|-------|
| `Permit` | ERC-2612 | Medium | Off-chain authorization — no gas but grants spending rights |
| `Order` | DEX (0x, Seaport) | Medium | Trading order executable on-chain after signing |
| `Vote` | Governance | Low | Governance voting |
| Unknown | Any DApp | High | Warn user to review carefully |

---

## ERC20 Approve Calldata Encoding

```
Function: approve(address spender, uint256 amount)
Selector: 0x095ea7b3
Calldata: 0x095ea7b3 + spender (32 bytes padded) + amount (32 bytes uint256)
```

| Mode | Amount Value | Security | Convenience |
|------|-------------|----------|-------------|
| Exact | Actual needed amount | High | Low (re-approve each time) |
| Unlimited | `2^256 - 1` | Low | High (one-time) |

**Default to exact approval** unless user explicitly requests unlimited.

---

## Conversation Examples

**Example 1 (Happy Path): Connect wallet**
User: "Connect my wallet to Uniswap on Ethereum"
Agent: Get address via `dex_wallet_get_addresses`. Display ETH address for the user to use in the DApp.

**Example 2 (Happy Path): Sign a login message**
User: "Sign this message for Uniswap login: Welcome to Uniswap! Nonce: abc123"
Agent: Display the message content, confirm with user (no gas cost). On confirm, call `dex_wallet_sign_message`. Return the signature.

**Example 3 (Happy Path): Approve USDC for Uniswap**
User: "Approve USDC for Uniswap Router"
Agent:
1. Ask user for desired amount or recommend exact amount for the pending operation.
2. Build approve calldata (selector `0x095ea7b3`).
3. Display confirmation gate with chain, token, spender, amount, gas.
4. On confirm -> sign + broadcast -> display tx hash.

**Example 4 (Happy Path): Add liquidity to Uniswap**
User: "Add liquidity for ETH/USDC on Uniswap (Ethereum)"
Agent:
1. Get wallet address, check ETH and USDC balances.
2. If USDC allowance insufficient for Uniswap Router, execute Flow D (approve) first.
3. Run security review on Uniswap Router contract.
4. Build addLiquidity calldata using Uniswap V3 ABI.
5. Display confirmation with pool details, amounts, gas.
6. On confirm -> sign -> broadcast -> display tx hash.

**Example 5 (Happy Path): Stake ETH on Lido**
User: "Stake 1 ETH on Lido"
Agent:
1. Get wallet address, verify ETH balance >= 1 + gas.
2. Run security review on Lido stETH contract.
3. Build submit() calldata with value = 1 ETH.
4. Display confirmation: "Stake 1 ETH via Lido, receive stETH."
5. On confirm -> sign -> broadcast.

**Example 6 (Edge Case): EIP-712 Permit signing**
User: "Sign this Permit message: {types: {...}, domain: {...}, message: {owner, spender, value, ...}}"
Agent:
1. Parse EIP-712 JSON: display domain (name, chainId, verifyingContract), primary type `Permit`, message fields.
2. Warn: "This Permit signature grants off-chain spending rights (no gas), but is equivalent to an on-chain approval."
3. On confirm -> call `dex_wallet_sign_message` with the JSON string -> return signature.

**Example 7 (Edge Case): Revoke approval**
User: "Revoke USDC approval for contract 0xDEF..."
Agent:
1. Build approve calldata with amount = 0 (revoke).
2. Display confirmation: "Revoke USDC spending authorization for 0xDEF..."
3. On confirm -> sign -> broadcast.

**Example 8 (Edge Case): Unknown contract — security warning**
User: "Call function mint() on contract 0xUNKNOWN..."
Agent:
1. Run `dex_token_get_risk_info` on the contract.
2. If unaudited/high-risk: display warning: "This contract is unaudited. Interacting may result in asset loss."
3. Require re-confirmation before proceeding.

**Example 9 (Edge Case): Unlimited approval request**
User: "Approve unlimited USDT for this contract"
Agent:
1. Display high-risk warning: "Unlimited approval grants permanent spending rights. Exact-amount approval is safer."
2. Require secondary confirmation: "Are you sure you want to approve unlimited USDT?"
3. On confirm -> build approve with max uint256 -> sign -> broadcast.

**Example 10 (Edge Case): Arbitrary contract call with ABI**
User: "Call function claimReward(uint256 poolId) with poolId=5 on contract 0xABC... on Ethereum"
Agent:
1. Parse ABI: encode calldata for `claimReward(5)`.
2. Run security review on contract.
3. Display confirmation with function, params, contract, gas.
4. On confirm -> sign -> broadcast.

**Example 11 (Edge Case): Message signing for NFT marketplace**
User: "Sign this order for OpenSea: {EIP-712 typed data for Seaport Order}"
Agent:
1. Parse EIP-712: identify primaryType = `Order`, source = Seaport.
2. Display: domain, order details, risk level (Medium — trading order).
3. On confirm -> call `dex_wallet_sign_message` -> return signature.

**Example 12 (Boundary Case): Not this module — transfer**
User: "Send 1 ETH to 0xABC..."
Agent: Route to [transfer.md](./transfer.md) — this is a direct transfer, not a DApp interaction.

**Example 13 (Boundary Case): Not this module — x402 payment**
User: "Pay for this API with 402 payment"
Agent: Route to [x402.md](./x402.md) — this is an x402 HTTP payment, not a DApp contract interaction.

**Example 14 (Boundary Case): Not this module — swap**
User: "Swap ETH for USDT on Uniswap"
Agent: Route to `gate-dex-trade` — this is a token swap execution. (DApp module handles contract interactions like approvals and liquidity, but direct swap execution is handled by the trade skill.)

**Example 15 (Boundary Case): Not this module — market data**
User: "Is this token contract safe?"
Agent: Route to `gate-dex-market` — for security audits without executing any transaction.

---

## Post-Operation Suggestions

After a successful DApp operation, **proactively display next actions**:

**After transaction execution:**
```
✅ DApp transaction completed!
Tx Hash: {hash_id}
Explorer: https://{explorer}/tx/{hash_id}

You can:
- Check your updated balance
- View transaction details on block explorer
- Perform another DApp operation
- Check contract security info
```

**After message signing (no on-chain tx):**
```
✅ Signature complete. Please submit this signature to the DApp to finish verification.

You can also:
- Connect to another DApp
- Check your token balances
- Sign another message
```

### Follow-up Routing Table

| User Follow-up Intent | Route Target |
|------------------------|--------------|
| View updated balance | [asset-query.md](./asset-query.md) |
| View transaction details | [asset-query.md](./asset-query.md) (`dex_tx_detail`) |
| Check contract security | `gate-dex-market` |
| Transfer tokens | [transfer.md](./transfer.md) |
| Swap tokens | `gate-dex-trade` |
| Pay for a 402 resource (x402) | [x402.md](./x402.md) |
| Login / auth expired | [auth.md](./auth.md) |
| Use CLI commands | [cli.md](./cli.md) |

---

## Error Handling

| Scenario | Handling |
|----------|----------|
| Not logged in / no `mcp_token` | Route to [auth.md](./auth.md) |
| Token expired | Silent refresh; on failure re-login via [auth.md](./auth.md) |
| Gas token insufficient | Abort tx/approve; display shortfall; suggest top-up |
| Approve token not in holdings | Warn user (approve possible but meaningless); confirm intent |
| Spender contract is high risk | Strongly warn; recommend cancellation; allow only with re-confirmation |
| Spender contract is unknown | Display "unknown contract" warning; prompt user to verify source |
| Contract address format invalid | Refuse; show expected format |
| `dex_wallet_sign_message` fails | Display error; do not auto-retry |
| EIP-712 JSON parsing fails | Display raw JSON; prompt user to verify format |
| `dex_wallet_sign_transaction` fails | Display error; do not auto-retry |
| `dex_tx_send_raw_transaction` fails | Display broadcast error with suggested action |
| User cancels any confirmation | Immediately abort; never sign or broadcast |
| Approve amount = 0 | Treat as "revoke authorization"; confirm with user |
| User requests unlimited approval | Display high-risk warning; require secondary confirmation |
| Duplicate approve for same spender | Inform new approve overrides old; confirm intent |
| Solana message signing | Inform user that Solana message signing is not yet supported (EVM only) |

---

## Security Rules

1. **Token confidentiality**: Never display `mcp_token` in plaintext. Use placeholders like `<mcp_token>`.
2. **Account masking**: Show only partial `account_id`.
3. **Silent refresh**: Prioritize silent token refresh on expiration.
4. **Confirmation + tx-checkin before all signing**: All signing operations (messages, transactions, approves) require explicit user confirmation **and** terminal [tx-checkin.md](./tx-checkin.md). Never skip or auto-confirm.
5. **Contract security review**: For unknown contracts, call `dex_token_get_risk_info` and display results. High-risk contracts get additional prominent warnings.
6. **Default exact authorization**: ERC20 Approve defaults to exact amount. Unlimited authorization requires explicit user request plus risk warning.
7. **EIP-712 transparency**: Parse and display all key fields in human-readable format. Never omit `verifyingContract`, `spender`, or amount fields.
8. **Mandatory gas validation**: Always validate gas token balance before transactions and approves.
9. **No auto-retry**: Display errors clearly on failure; never retry in the background.
10. **Broadcast promptly**: Sign and broadcast immediately; do not hold signed transactions.
11. **Permit risk notification**: EIP-2612 Permit signatures consume no gas but are equivalent to authorization — remind users about spender and amount.
12. **Phishing prevention**: Never proactively construct transactions targeting unknown contracts. All DApp interaction data must come from the user or trusted sources.
13. **raw_tx confidentiality**: Keep unsigned transaction data between agent and MCP Server only.
