---
name: gate-dex-withdraw
version: "2026.3.31-1"
updated: "2026-03-31"
description: "Gate Wallet withdraw: on-chain moves from the user wallet to Gate Exchange (deposit address resolved for their UID) or to a custom address, with Gate UID binding, min-deposit validation, mandatory confirmation, terminal tx-checkin before signing, and the shared transfer sign/broadcast pipeline. Use when the user wants to cash out to their exchange account, send funds to the exchange deposit address, rebind or verify exchange identity, or review withdrawal-related history for this flow."
---

# Gate DEX Withdraw

> Withdraw module — exchange binding, deposit-address resolution (with minimum-deposit checks), balance verification, transaction preview, mandatory user confirmation, **terminal tx-checkin before signing**, signing, and broadcasting. **6** withdraw/binding MCP tools + **Gate OAuth** tools + the transfer execution chain from [transfer.md](./transfer.md) (plus cross-skill balance).

## Product definition (Knowledge)

**What this is**: On-chain withdrawal from the user’s Gate DEX wallet — either to **their Gate Exchange account** (deposit address resolved for the bound UID) or to **any valid on-chain address** (same execution path as a standard transfer in [transfer.md](./transfer.md)).

**Common misconceptions**

- Withdraw-to-exchange is still an **on-chain transfer** to a deposit address; exchange crediting is downstream of broadcast — the agent does not move CEX balances directly.
- **Withdraw to a custom address** does not use `dex_withdraw_deposit_address`; collect `chain`, token, amount, and `to`, then follow **Flow B** and [transfer.md](./transfer.md).
- **Withdrawal / tx history** uses list/detail tools (e.g. `dex_tx_list`), not market or swap skills.

**Relationship to other modules**

- Parent router: [SKILL.md](../SKILL.md) (auth, MCP detection, and module index). If only generic “transfer” routing is present, still use **this** file whenever the user’s goal is **exchange deposit + UID**, not a simple peer send.
- Execution shared with [transfer.md](./transfer.md): gas, preview, confirm, [tx-checkin.md](./tx-checkin.md), sign, broadcast — this reference adds **binding, deposit resolution, and min-deposit** for the exchange leg.

---

## Scenarios and boundaries (Decision)

### Applicable scenarios

Use when the user wants to:

- Withdraw or send funds **to their Gate Exchange account** (wallet → exchange deposit address on-chain)
- **Bind or verify** Gate Exchange UID for withdraw-to-exchange (`gate_mcp` / `gate_quick` vs other wallets)
- **Query or replace** the current wallet ↔ Gate UID binding (per product and server rules)
- Withdraw **to a custom on-chain address** they specify (same execution path as a standard transfer)
- Another skill routes the user here for withdraw-to-exchange or “cash out to Gate” flows

### Capability boundaries

- **Supports**: Withdraw to Gate Exchange (deposit address from BW + min-deposit via Wallet-Core), binding/query/rebind flows, masked identity hints from binding API, then on-chain transfer using the shared preview/sign/broadcast pipeline
- **Supported chains**: Same as [transfer.md](./transfer.md) for the **on-chain** leg (e.g. `eth`, `bsc`, `polygon`, `arbitrum`, `optimism`, `avax`, `base`, `sol`) — subject to what the exchange lists for `chain_name` / `coin_symbol` in `dex_withdraw_deposit_address`
- **Does not support**: Exchange-initiated “push” from Gate balance to wallet (that is **deposit** / another product path), swap/exchange (→ `gate-dex-trade`), DApp calls (→ [dapp.md](./dapp.md)), x402 (→ [x402.md](./x402.md))
- **Custom address withdraw**: After parameters are known, follow **Flow B** below and the full tool chain in [transfer.md](./transfer.md) (address validation, gas, preview, confirm, sign, send)

**Prerequisites**: MCP Server available (see parent SKILL.md). All operations require a valid `mcp_token`. If missing or expired, route to [auth.md](./auth.md).

---

## MCP tools (execution)

API mapping, parameters, and call order for withdraw-to-exchange and related binding flows. On-chain send, preview, confirm, sign, and broadcast follow the same rules as [transfer.md](./transfer.md) unless noted below.

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `dex_wallet_get_wallet_type` | Classify wallet (`gate_mcp` / `gate_quick` / `other`), read `gateUid`, optionally start Gate OAuth for withdraw/bind | `wallet_address?`, `account_id?`, `for_withdraw_to_exchange?`, `for_gate_oauth_bind?`, `mcp_token` |
| `dex_wallet_get_bindings` | Current Gate UID binding + masked `emailOrPhone` when upstream returns it | `mcp_token` |
| `dex_wallet_bind_exchange_uid` | Bind `gateUid` after OAuth (non-link flows) | `gateUid`, `mcp_token` |
| `dex_wallet_replace_binding` | Rebind to a new Gate exchange UID (follow tool description + product limits) | `newUid`, `mcp_token` |
| `dex_wallet_google_gate_bind_start` | **Google MCP sessions only**: start Gate device OAuth to bind/update `gate_uid` without replacing `mcp_token` | `mcp_token` |
| `dex_withdraw_deposit_address` | Resolve exchange deposit addresses; enforce **min deposit** and disabled flags | `uid`, `chain_name`, `coin_symbol`, **`amount`** (required), `token_address?`, `mcp_token` |
| `dex_auth_gate_login_start` / `dex_auth_gate_login_poll` | Gate OAuth lifecycle (`link_mcp_token`, `auto_replace_binding` per server docs) | See auth / gate tool schemas |
| `dex_wallet_get_token_list` | Balance verification (cross-skill) | `account_id`, `chain`, `mcp_token` |
| `dex_wallet_get_addresses` | Resolve `from_address` for the target chain | `account_id`, `mcp_token` |
| `dex_tx_gas` | Estimate gas for the on-chain leg | `chain`, `from_address`, `to_address`, `value?`, `data?`, `mcp_token` |
| `dex_tx_transfer_preview` | Build unsigned tx to deposit or custom `to` | `chain`, `from_address`, `to_address`, `token_address`, `amount`, `account_id`, `mcp_token` |
| `dex_wallet_sign_transaction` | Sign after user confirms **and** terminal [tx-checkin.md](./tx-checkin.md) | `raw_tx`, `chain`, `account_id`, `mcp_token` |
| `dex_tx_send_raw_transaction` | Broadcast | `signed_tx`, `chain`, `mcp_token` |
| `dex_tx_list` | Outgoing / history (scope per product) | Per server schema |

### Tool Details

#### `dex_wallet_get_wallet_type` — Wallet class + Gate UID + OAuth hints

| Field | Description |
|-------|-------------|
| **Parameters** | `{ wallet_address?, account_id?, for_withdraw_to_exchange?, for_gate_oauth_bind?, mcp_token }` |
| **Returns** | `walletAddress`, `walletType`, `gateUid`; when binding needed: `requiresGateOAuthBinding`, `nextSteps`, `gateOAuthUrl`, `gateOAuthFlowId` |

- Use **`for_withdraw_to_exchange=true`** when the user intends withdraw to exchange and `gateUid` may be missing (starts Gate OAuth where applicable).
- Use **`for_gate_oauth_bind=true`** for explicit bind/rebind on **non–Gate-native** wallets per tool description.
- **Always** present a Markdown table of key fields to the user (not raw JSON only).

#### `dex_wallet_get_bindings` — Show trust signals

| Field | Description |
|-------|-------------|
| **Parameters** | `{ mcp_token }` |
| **Returns** | `gateUid`, `emailOrPhone` (often masked), `boundAt` when present |

- Use **before** heavy steps and in confirmation copy: users should see **UID + masked email/phone + deposit address**, not UID/address alone.

#### `dex_withdraw_deposit_address` — Exchange deposit list + suggestion

| Field | Description |
|-------|-------------|
| **Parameters** | `{ uid, chain_name, coin_symbol, amount, token_address?, mcp_token }` |
| **Returns** | `deposit_addresses`, `suggested_to_address`, `suggested_pick_error?`, `min_deposit_amount?`, `exchange_symbol?` |

- **`amount` is mandatory**: server validates **≥ min_deposit** via Wallet-Core before returning addresses.
- **`token_address`**: omit for native; USDT may be inferred from `chain_name`; other ERC20 usually needs explicit contract.
- If `suggested_pick_error` is set or `suggested_to_address` is empty, **do not** sign until resolved.

#### `dex_wallet_bind_exchange_uid` / `dex_wallet_replace_binding`

| Tool | Parameters | Notes |
|------|------------|--------|
| `dex_wallet_bind_exchange_uid` | `gateUid`, `mcp_token` | After OAuth when the flow returns `gate_uid` and link-based bind is not used |
| `dex_wallet_replace_binding` | `newUid`, `mcp_token` | Prefer Google bind flow (`dex_wallet_google_gate_bind_start` → poll) when switching Gate account from Google session; standalone Gate session may use `auto_replace_binding` on poll per docs |

#### `dex_wallet_google_gate_bind_start` — Google-only

| Field | Description |
|-------|-------------|
| **Parameters** | `{ mcp_token }` |
| **Returns** | `flow_id`, `verification_url`, `next_steps`, … |

- Poll with **`dex_auth_gate_login_poll(flow_id)`**. On success, **`mcp_token` unchanged** when `linked_to_google_session=true`.

#### Transfer pipeline tools

For **`dex_tx_gas`**, **`dex_tx_transfer_preview`**, **`dex_wallet_sign_transaction`**, **`dex_tx_send_raw_transaction`**, and balance via **`dex_wallet_get_token_list`**, use the same parameter and safety rules as [transfer.md](./transfer.md).

---

## Tool Call Chain

**Entry decision (mandatory before any withdraw execution):**

```
If user says only "withdraw/cash out" (destination not explicit):
  Ask first: "Withdraw to Gate Exchange deposit address or to a custom on-chain address?"
  - Exchange deposit address -> use "Withdraw to Gate Exchange" chain below
  - Custom on-chain address -> use Flow B / transfer.md chain
Do not call dex_withdraw_deposit_address before destination is confirmed.
```

**Withdraw to Gate Exchange** (strict order; OAuth sub-path when `gateUid` missing):

```
0. dex_chain_config                          <- Session / chain help (if needed)
1. dex_wallet_get_wallet_type                <- for_withdraw_to_exchange=true when appropriate
2. [Gate OAuth: gateOAuthUrl / google_gate_bind_start → dex_auth_gate_login_poll]  <- If required
3. dex_wallet_bind_exchange_uid              <- Only when OAuth flow requires explicit bind (see poll result / nextSteps)
4. dex_wallet_get_bindings                   <- Show gateUid + masked emailOrPhone + boundAt
5. dex_withdraw_deposit_address              <- uid, chain_name, coin_symbol, amount (+ token_address?)
6. dex_wallet_get_addresses                  <- from_address for chain
7. dex_wallet_get_token_list                 <- Token + gas balance
8. dex_tx_gas                                <- Fee estimate to suggested_to_address
9. [Agent balance validation]                <- MANDATORY, same rules as transfer.md
10. dex_tx_transfer_preview                  <- to = suggested_to_address (unless product allows explicit pick)
11. [Display confirmation, wait for user]    <- MANDATORY gate
12. [Terminal tx-checkin]                    <- MANDATORY: [tx-checkin.md](./tx-checkin.md)
13. dex_wallet_sign_transaction
14. dex_tx_send_raw_transaction
```

**Withdraw to custom address**: use steps **0 → 6–14** from [transfer.md](./transfer.md) (no `dex_withdraw_deposit_address`); user supplies `to_address`.

---

## Execution Flow

### Flow 0: Destination Disambiguation (MANDATORY)

```
Step 1: Check whether destination type is explicit
  - If user explicitly mentions "to Gate / to exchange / deposit address / UID" -> go to Flow A
  - If user provides a concrete on-chain address -> go to Flow B
  - If user only says "withdraw/cash out" without destination -> ask:
    "Do you want to withdraw to your Gate Exchange deposit address or to a custom on-chain address?"
    Wait for answer before calling withdraw execution tools
```

### Flow A: Withdraw to Gate Exchange

```
Step 1: Authentication check
  No mcp_token -> route to auth.md
  |
Step 2: Wallet type + binding intent
  Call dex_wallet_get_wallet_type({ for_withdraw_to_exchange: true, ... })
  If requiresGateOAuthBinding: follow nextSteps / gateOAuthUrl / Google bind start + poll
  If bind_exchange_uid needed: dex_wallet_bind_exchange_uid
  |
Step 3: Identity confirmation (MANDATORY for trust)
  Call dex_wallet_get_bindings
  Show: gateUid, emailOrPhone (masked), boundAt; align with user expectation
  Legacy Gate-login quick wallet: add explicit UID confirmation step if product requires
  |
Step 4: Resolve deposit address + min deposit
  Call dex_withdraw_deposit_address({ uid, chain_name, coin_symbol, amount, token_address? })
  Abort if below min deposit, deposit disabled, or suggested_pick_error / empty suggested_to_address
  |
Step 5: Resolve sender + balances
  dex_wallet_get_addresses -> from_address
  dex_wallet_get_token_list -> token balance + gas token balance
  |
Step 6: Gas estimate
  dex_tx_gas({ chain, from_address, to_address: suggested_to_address, ... })
  |
Step 7: Balance validation (MANDATORY)
  Same rules as transfer.md (native vs ERC20 vs SPL)
  |
Step 8: Build preview
  dex_tx_transfer_preview({ to_address: suggested_to_address, amount, token_address, ... })
  |
Step 9: Display confirmation (MANDATORY GATE)
  Show: chain, from, to (deposit address), Gate UID, masked email/phone if available,
        amount, balances, gas, server confirm_message
  Wait for explicit "confirm" / "cancel" / parameter change
  |
Step 10: Terminal tx-checkin (MANDATORY) — [tx-checkin.md](./tx-checkin.md): use **`dex_tx_transfer_preview` → `txBundle`** with **`-tx-bundle-file`** (no hand-built txbundle); on failure abort
  |
Step 11: Sign + broadcast
  dex_wallet_sign_transaction -> dex_tx_send_raw_transaction
  |
Step 12: Display hash + explorer + suggestions (see Post-Withdraw)
```

### Flow B: Withdraw to Custom On-Chain Address

Treat as **standard transfer** end-to-end:

```
Step 1: Authentication -> auth.md if needed
Step 2: Collect chain, token, amount, destination address (validate format — see transfer.md)
Step 3-12: Follow transfer.md Flow A (balance, gas, preview, confirm, tx-checkin, sign, broadcast)
```

Do **not** call `dex_withdraw_deposit_address` unless the user has explicitly selected exchange withdraw (Flow A) for their UID.

---

## Transaction Confirmation Templates

**These confirmations are MANDATORY gates. Agent must NOT sign before explicit user confirmation.**

### Withdraw to Gate Exchange

```
========== Withdraw to Exchange — Confirmation ==========
Chain:              {chain_name}
From (your wallet): {from_address}
To (deposit addr):  {suggested_to_address}
Gate Exchange UID:  {gate_uid}
Verified identity:  {masked_email_or_phone}   (if available from dex_wallet_get_bindings)
---------- Transfer ----------
Amount:             {amount} {coin_symbol}
Token contract:     {token_address_or_native}
---------- Balance ----------
{token_symbol} Balance: {token_balance} (Sufficient ✅ / Insufficient ❌)
{gas_symbol} (Gas):     {gas_balance}
---------- Fees ----------
Estimated Gas:      {estimated_fee} {gas_symbol} (≈ ${fee_usd})
---------- Server ----------
{confirm_message}
===========================================================
Reply "confirm" to execute, "cancel" to abort, or describe changes.
```

### Withdraw to Custom Address

Use the **Native** or **ERC20 / SPL** templates from [transfer.md](./transfer.md) unchanged.

---

## Deposit Address and UID Rules

| Rule | Action |
|------|--------|
| Recipient for exchange withdraw | Always use API output; prefer **`suggested_to_address`** from `dex_withdraw_deposit_address` |
| User trust | Show **UID + masked email/phone + deposit address** in confirmation when data exists |
| Min deposit | Enforced server-side with required **`amount`**; never sign if user intent is below minimum |
| Custom `to` | User-provided address must pass chain format checks — see Address Validation in [transfer.md](./transfer.md) |

---

## Supported Chains (on-chain leg)

The **transfer** step supports the networks listed in [transfer.md](./transfer.md). Whether a **coin/chain** pair is available for **exchange deposit** is determined by `dex_withdraw_deposit_address` / upstream — if the tool errors, surface the message and do not guess addresses.

---

## Conversation Examples

**Example 1 (Happy path): Gate quick wallet, USDT to exchange**

User: “Withdraw 100 USDT to my Gate account on BSC.”

Agent:

1. Verify auth; `dex_wallet_get_wallet_type({ for_withdraw_to_exchange: true })` → `gate_quick` + `gateUid`.
2. `dex_wallet_get_bindings` → show masked `emailOrPhone` if present.
3. `dex_withdraw_deposit_address({ uid, chain_name: "BSC", coin_symbol: "USDT", amount: "100" })` → `suggested_to_address`.
4. `dex_wallet_get_addresses` + `dex_wallet_get_token_list` → balance check; `dex_tx_gas` → `dex_tx_transfer_preview` with `to = suggested_to_address`.
5. Show exchange confirmation template; user replies `confirm`.
6. Sign → broadcast → hash + explorer + post-withdraw suggestions.

**Example 2 (Happy path): Other wallet — OAuth bind then withdraw**

User: “Send 50 USDT from my wallet to the exchange.”

Agent:

1. `dex_wallet_get_wallet_type({ for_withdraw_to_exchange: true })` → `other`, OAuth URL or bind steps.
2. User completes browser flow; `dex_auth_gate_login_poll` → bind completed or `dex_wallet_bind_exchange_uid`.
3. `dex_wallet_get_bindings` → display trust fields.
4. Continue from `dex_withdraw_deposit_address` through preview → confirm → sign → broadcast.

**Example 3 (Edge case): Below minimum deposit**

User: “Withdraw 1 USDT to exchange.”

Agent:

1. After binding OK, `dex_withdraw_deposit_address` returns error (amount below `min_deposit_amount`).
2. Show `min_deposit_amount` and message; **do not** build preview or sign.

**Example 4 (Edge case): suggested_pick_error**

Agent:

1. Deposit API returns list but `suggested_pick_error` is set.
2. Explain issue; fix `chain_name` / `coin_symbol` / `uid` or escalate; **no sign**.

**Example 5 (Happy path): Custom TRC20-style address (conceptual)**

User: “Withdraw 20 USDT to TN2…”

Agent: Route to **Flow B** / [transfer.md](./transfer.md) — validate address for the chain, then standard preview → confirm → sign → broadcast.

**Example 6 (Edge case): User cancels**

User: `cancel` at confirmation.

Agent: Abort; no sign/broadcast; offer to change amount or destination.

**Example 7 (Boundary): Swap request**

User: “Swap USDT for ETH on the exchange.”

Agent: Not withdraw execution — route to `gate-dex-trade` or product-specific swap.

**Example 8 (Boundary: history only)**

User: “Show my withdrawal history.”

Agent: Use `dex_tx_list` (and related detail tools per asset-query / server docs); clarify labels with product if needed.

---

## Post-Withdraw Suggestions

After a successful on-chain withdraw (exchange or custom address), **proactively display next actions**.

**After successful withdraw to exchange:**

```
✅ Transaction broadcast successfully!
Tx Hash: {hash_id}
Explorer: https://{explorer}/tx/{hash_id}
Funds are sent on-chain to your Gate deposit address; crediting time depends on the exchange and network.

You can:
- Check transaction status on the explorer
- View updated wallet balance
- See activity in dex_tx_list
- Make another transfer or withdraw
```

**After cancel:**

```
Withdraw cancelled. No transaction was signed or broadcast.

You can:
- Adjust amount or chain
- Re-verify binding with dex_wallet_get_bindings
- Try a transfer to a custom address (transfer.md)
```

### Follow-up Routing Table

| User Follow-up Intent | Target |
|------------------------|--------|
| View balance | [transfer.md](./transfer.md) / `dex_wallet_get_token_list` |
| Tx detail / history | `dex_tx_list`, `dex_tx_detail` (per server / asset-query docs) |
| Another withdraw to exchange | Stay in this module |
| Send to arbitrary address | [transfer.md](./transfer.md) |
| Deposit from exchange to wallet | Product deposit flow / future deposit reference |
| Swap | `gate-dex-trade` |
| Auth expired | [auth.md](./auth.md) |

---

## Error Handling

| Scenario | Handling |
|----------|----------|
| Not logged in / `mcp_token` missing | Same as transfer.md: refresh then [auth.md](./auth.md) |
| `gateUid` missing for exchange withdraw | Run wallet type + OAuth / bind per `nextSteps`; never invent UID |
| `dex_withdraw_deposit_address` rejects amount | Show min deposit / disabled message; do not sign |
| `suggested_pick_error` or empty `suggested_to_address` | Stop; resolve inputs with user or support |
| Binding API error | Surface server message; may need rebind or different session |
| Insufficient token or gas | Abort with shortfall details (same as transfer.md) |
| User cancels confirmation | Abort; no sign/broadcast |
| Preview / sign / broadcast failure | Display error; no silent auto-retry |
| `dex_wallet_google_gate_bind_start` on non-Google session | Refuse; use correct Gate login path without link token |

---

## Security Rules

1. **Token confidentiality**: Never display `mcp_token` in plaintext.
2. **Account ID masking**: Show only partial `account_id` in user-facing output.
3. **Mandatory user confirmation**: Full summary including **deposit address, Gate UID, and masked identity fields** when available — then explicit **confirm** before sign.
4. **Never skip min-deposit check**: Always pass real **`amount`** into `dex_withdraw_deposit_address`.
5. **Recipient integrity**: For exchange withdraw, **`to`** must come from API (`suggested_to_address`); do not substitute user-typed deposit addresses unless product explicitly allows.
6. **Raw tx confidentiality**: `raw_tx` only between Agent and MCP Server — never show to users.
7. **OAuth session rules**: After Google-linked poll, **do not** replace `mcp_token` when `linked_to_google_session=true`; follow tool descriptions for `auto_replace_binding`.
8. **Transparent errors**: Show MCP errors faithfully; do not paraphrase into misleading success.
9. **No sign on ambiguity**: If binding, deposit address, or balance is unclear, resolve before `dex_wallet_sign_transaction`.

---

## Quick validation (before sign)

Use this as a final pass after preview and before `dex_wallet_sign_transaction`:

- [ ] Valid `mcp_token`; user authenticated ([auth.md](./auth.md) if not)
- [ ] Destination type confirmed first: exchange deposit (Flow A) or custom address (Flow B)
- [ ] For exchange withdraw: `gateUid` resolved or OAuth/bind completed; `dex_wallet_get_bindings` shown for trust copy
- [ ] `dex_withdraw_deposit_address` succeeded with real **`amount`**; `suggested_to_address` present; no `suggested_pick_error`
- [ ] Token and gas balances meet or exceed send + fee (same checks as [transfer.md](./transfer.md))
- [ ] User gave explicit **confirm** after the full summary (deposit address, UID, masked identity when available)