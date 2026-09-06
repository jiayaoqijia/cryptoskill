---
name: gate-dex-wallet-mcp
version: "2026.3.30-1"
updated: "2026-03-30"
description: "MCP execution specification for gate-dex-wallet. Covers auth, balance/address/history, transfer, withdraw-to-exchange, x402 payments, DApp interactions, and CLI-oriented MCP calls."
---

# Gate DEX Wallet MCP Specification

> Authoritative MCP execution document for `gate-dex-wallet`. `SKILL.md` is routing-focused; this file defines tool-level execution.

## 1. Scope and Trigger Boundaries

Use this document when user intent is wallet/account operations in DEX context:
- Authentication/session management
- Address/balance/portfolio/history query
- On-chain transfer
- Withdraw to Gate Exchange (deposit flow)
- x402 payment flow
- DApp connect/sign/approve/call

Common misroutes:
- Price/K-line/rank/security lookup only -> `gate-dex-market`
- Swap execution intent -> `gate-dex-trade`

## 2. MCP Detection and Fallback

Detection sequence (once per session):
1. Find MCP server exposing `dex_wallet_get_token_list` and at least one tx tool (`dex_tx_transfer_preview` or `dex_tx_send_raw_transaction`).
2. Verify with `dex_chain_config` (`chain=eth`).
3. Cache server id for this conversation.

Failure fallback:
- Server not configured: show setup instructions from `SKILL.md` and stop execution.
- Network/service unavailable: return degraded guidance and keep user intent context.
- Tool unavailable: route to corresponding reference module (`auth.md`, `asset-query.md`, `transfer.md`, etc.) and provide non-execution answer.

## 3. Authentication

Wallet operations require `mcp_token`.

Rules:
1. If no token/session, start OAuth (Google or Gate) via auth tools.
2. If token expired, call `dex_auth_refresh_token`; on failure require re-login.
3. Never print raw token in user-facing output.

Auth tools:
- `dex_auth_google_login_start`
- `dex_auth_google_login_poll`
- `dex_auth_gate_login_start`
- `dex_auth_gate_login_poll`
- `dex_auth_login_google_wallet`
- `dex_auth_login_gate_wallet`
- `dex_auth_refresh_token`
- `dex_auth_logout`

## 4. MCP Resources

No mandatory MCP Resource is required in this skill (unlike `gate-dex-trade`).
Use tool probing (`dex_chain_config`) for chain capability checks.

## 5. Tool Calling Specification

### 5.1 Account and Identity

| Tool | Required inputs | Key return fields | Common errors |
|---|---|---|---|
| `dex_wallet_get_addresses` | `account_id`, `mcp_token` | `EVM`, `SOL` | account not found, auth expired |
| `dex_wallet_get_wallet_type` | `mcp_token` | wallet/account type | auth expired |
| `dex_wallet_get_bindings` | `mcp_token` | existing UID bindings | no binding record |
| `dex_wallet_bind_exchange_uid` | `uid`, `mcp_token` | binding status | invalid uid, already bound |
| `dex_wallet_replace_binding` | `uid`, `mcp_token` | replace status | binding lock |
| `dex_wallet_google_gate_bind_start` | `mcp_token` | bind authorization url/state | auth/session invalid |

### 5.2 Asset, Balance, History

| Tool | Required inputs | Key return fields | Common errors |
|---|---|---|---|
| `dex_wallet_get_token_list` | `mcp_token` (+ `chain`/`network_keys`) | token list, balances (`orignCoinNumber`), value | chain unsupported |
| `dex_wallet_get_total_asset` | `mcp_token` | total portfolio value | auth expired |
| `dex_tx_list` | `mcp_token`, filters | tx list, status, hash | pagination/filter mismatch |
| `dex_tx_history_list` | `mcp_token`, filters | swap/tx history entries | empty history |
| `dex_tx_detail` | `mcp_token`, `tx_hash`/id | tx detail, state, fee | tx not found |

### 5.3 Transfer and Withdraw

| Tool | Required inputs | Key return fields | Common errors |
|---|---|---|---|
| `dex_tx_transfer_preview` | chain, token, amount, destination, `mcp_token` | preview amount, fee, unsigned payload/meta | insufficient balance/gas |
| `dex_tx_get_sol_unsigned` | sol transfer payload params | unsigned Sol tx payload | invalid sol params |
| `dex_wallet_sign_transaction` | unsigned tx + `mcp_token` | signed raw tx | sign rejected |
| `dex_tx_send_raw_transaction` | signed raw tx + chain | `tx_hash`, submit status | nonce/fee/route failure |
| `dex_withdraw_deposit_address` | uid/account + chain/token + `mcp_token` | Gate deposit address + network info | no deposit route |
| `dex_tx_gas` | chain + tx context | estimated gas native/usd | chain RPC unavailable |

### 5.4 x402 and DApp

| Tool | Required inputs | Key return fields | Common errors |
|---|---|---|---|
| `dex_tx_x402_fetch` | payment target + scheme + `mcp_token` | payment requirement, quote, execution result | unsupported scheme |
| `dex_wallet_sign_message` | message typed/plain + `mcp_token` | signature | user rejected |
| `dex_tx_approve_preview` | token, spender, amount, chain | approval preview + tx meta | token unsupported |
| `dex_token_list_swap_tokens` | chain/filter | token metadata | empty list |
| `dex_token_get_risk_info` | token/contract + chain | token risk labels | service degraded |

## 6. Execution SOP (Non-Skippable)

### 6.1 Query SOP (balance/address/history)
1. Validate auth (`mcp_token`).
2. Confirm scope (chain/account/time range).
3. Call minimal read tools.
4. Return structured summary + source fields.

### 6.2 Transfer SOP
1. Resolve source/target chain and address type (EVM/SOL).
2. Pre-check token balance and native gas sufficiency (`dex_wallet_get_token_list` + `dex_tx_gas`).
3. Preview transfer (`dex_tx_transfer_preview`).
4. **Mandatory confirmation gate** (single-use confirmation): show destination, chain, token, amount, fee, irreversible warning.
5. Build/sign/send (`dex_wallet_sign_transaction` + `dex_tx_send_raw_transaction`).
6. Return `tx_hash` and verification advice.

### 6.3 Withdraw-to-Exchange SOP
1. Ensure Gate UID binding status.
2. Fetch deposit address/network (`dex_withdraw_deposit_address`).
3. Transfer preview + fee estimation.
4. **Mandatory confirmation gate** with exchange destination details.
5. Sign/send and return tx hash.

### 6.4 x402 SOP
1. Fetch payment requirement (`dex_tx_x402_fetch`).
2. Explain payment amount/network/expiry.
3. Confirm payment intent.
4. Execute and return access result plus transaction trace.

## 7. Output Templates

### 7.1 Query Output

```markdown
## Wallet Summary
- Account: {account_id}
- Chains: {chains}
- Total Asset: {total_asset}
- Key Holdings: {top_tokens}
- Recent Activity: {recent_tx_count} tx
```

### 7.2 Transfer / Withdraw Draft

```markdown
## Transfer Draft
- From: {source_address} ({chain})
- To: {destination}
- Token/Amount: {token} {amount}
- Est. Fee: {fee_native} ({fee_usd})
- Warning: On-chain transfer is irreversible.
Reply "Confirm" to execute.
```

### 7.3 Execution Result

```markdown
## Execution Result
- Status: {success_or_failed}
- Tx Hash: {tx_hash}
- Network: {chain}
- Submitted At: {timestamp}
- Notes: {error_or_followup}
```

## 8. Safety and Degradation Rules

1. Any state-changing wallet action requires explicit confirmation immediately before execution.
2. Never infer destination chain from address shape alone when context is ambiguous.
3. Always show irreversible warning for transfer/withdraw/payment.
4. If auth refresh fails, stop writes and route user to re-login flow.
5. If key tools are degraded, provide read-only fallback guidance and do not fabricate execution status.
