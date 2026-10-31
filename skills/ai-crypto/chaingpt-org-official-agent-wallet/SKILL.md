---
name: agent-wallet
description: "Use the optional encrypted EVM, Solana and Tron agent wallet with strict admin policy, durable signing reservations, explicit asset/recipient budgets and human confirmation. Triggers: agent wallet, agent address, fund the agent, policy gate, kill switch, bounded signing, session key."
---

# Agent wallet

**Currently disabled.** The `chaingpt_agent_wallet_*` tools are not available unless the operator set `CHAINGPT_AGENT_WALLET_ENABLED=true` in the MCP server launch environment. If they are missing, tell the user the agent wallet is disabled and offer an unsigned transaction they sign in their own wallet instead. Never suggest enabling it through a `.env` file or shell edits made by the agent.

Read `docs/wallet-safety.md` before setup or migration. First-run signing is disabled.
The administrator explicitly enables the intended chains and configures native and token limits.
Keep only the working capital intended for this separate hot wallet.

## Tools and boundaries

- `chaingpt_agent_wallet_init`: encrypted EVM keystore; also controls the Tron address.
- `chaingpt_agent_wallet_solana_init`: independent Ed25519 key, shared admin passphrase source.
- Address, status, balance and policy tools are read-only views.
- Every `*_sign_and_send` requires a stable `operationId`. Reuse it unchanged on retries.
- `chaingpt_agent_wallet_serve_ui`: localhost **admin** UI; can edit policy. Its token is privileged.
- `chaingpt_dashboard_serve`: separate read-only overview UI.

Passphrase resolution is explicit environment variable, then the OS keychain. Do not retrieve or
print passphrases. Backups and recovery belong in an administrator-controlled context.

## Before signing

1. Check status, policy, chain, recipient, asset, amount, fees and remaining allowance.
2. Obtain human confirmation for the specific action. Keep the mainnet hook enabled.
3. Build and inspect the intent. Restricted mode supports canonical transfers and bounded ERC-20
   approvals. Opaque swaps/lending/compositions use unsigned builders and external signing.
4. For tokens, require an exact `assetLimits` rule, recipient and base-unit amount budget.
5. For scheduled work, claim the due step with `claim=true` and use its returned operationId.
6. Call the signer once. Pending/uncertain responses require receipt reconciliation using the same id.
7. Record the hash and report the observed outcome accurately; broadcast does not mean confirmed.

## Safety state

All signers share a cross-process filesystem lock. Budget is reserved durably before signing,
then signed bytes/hash are persisted before broadcast. A timeout, corrupt ledger or disk error
never restores allowance. Uncertain operations do not age out automatically. Confirmed operations
consume a rolling 24h budget. Follow the administrative recovery procedure in the linked guide;
never delete a journal or bypass a stale lock to recover spending capacity.

Native caps include fee reserves. Token budgets and recipients are separate. SPL recipients are
token account addresses; SOL recipients are wallet addresses. See the guide for policy examples.
Existing unrestricted mode is an explicit administrative opt-out from per-operation caps and
must never be described as bounded autonomy.

## Trust assumptions

The MCP surface has no policy-editing tool. This does not isolate files or keychain access from
an agent with host shell, file or browser tools. Keep the signer and dashboard administration
outside that agent's OS authority. The localhost UI intentionally can edit policy.

ERC-4337 session signing supports Nexus 1.x after explicit policy opt-in. Its on-chain-cap
layer remains beta pending the documented live grant/over-cap/expiry/revoke proof.
