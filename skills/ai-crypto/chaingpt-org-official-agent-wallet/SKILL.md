---
name: agent-wallet
description: "Use the optional agent wallet: an ERC-4337 session key that acts through the user's smart account within caps the owner grants on-chain, plus local policy and human confirmation. Triggers: agent wallet, agent address, session key, smart account caps, policy gate, kill switch, bounded signing."
---

# Agent wallet

**Currently disabled.** The `chaingpt_agent_wallet_*` tools are not available unless the operator set `CHAINGPT_AGENT_WALLET_ENABLED=true` in the MCP server launch environment. If they are missing, tell the user the agent wallet is disabled and offer an unsigned transaction they sign in their own wallet instead. Never suggest enabling it through a `.env` file or shell edits made by the agent.

Read `docs/wallet-safety.md` before setup or migration. First-run signing is disabled.

## Model

The agent never holds the funds' key. Funds sit in the user's ERC-4337 smart account (Nexus 1.x). The agent wallet
key is only a **session key**: the account owner grants it caps on-chain (`chaingpt_aa_session_build_grant`, signed in
the owner's wallet), and the chain refuses anything above them. An agent that reads the session key, the policy file or
the dashboard token still cannot raise those caps. Keep no funds on the session-key address itself.

Direct EOA, Solana and Tron signing was removed. If the user has funds on an old agent address, tell them to run
`node scripts/export-agent-key.mjs` themselves in a terminal and import the key into their own wallet. Never run it
for them, read its output, or ask for the key.

## Tools and boundaries

- `chaingpt_agent_wallet_init`: creates the session key (encrypted keystore).
- Address, status, balance and policy tools are read-only views.
- `chaingpt_agent_wallet_4337_sign_and_send`: the only signer. Requires a stable `operationId`; reuse it unchanged on retries.
- `chaingpt_aa_session_build_grant` / `_build_revoke` / `_status`: owner-signed grant and revoke calldata; session status.
- `chaingpt_agent_wallet_serve_ui`: localhost **admin** UI for the local policy. Its token is written to a 0600 file for the human; never read that file or ask for the token.
- `chaingpt_dashboard_serve`: separate read-only overview UI.

Passphrase resolution is the launch-environment variable (never a `.env` file), then the OS keychain. Do not retrieve or
print passphrases.

## Before signing

1. Check status, the session's on-chain caps (`chaingpt_aa_session_status`), the local policy, target, amount and fees.
2. Obtain human confirmation for the specific action. Keep the mainnet hook enabled.
3. For scheduled work, claim the due step with `claim=true` and use its returned operationId.
4. Call the signer once. Pending/uncertain responses require receipt reconciliation using the same id.
5. Record the hash and report the observed outcome accurately; broadcast does not mean confirmed.

## Safety state

The signer runs under a cross-process lock and reserves budget durably before signing; uncertain operations keep their
reservation. Earlier sessions stay live until the owner revokes them, and each has its own caps.

ERC-4337 on-chain caps remain beta until the documented live grant/over-cap/expiry/revoke proof on Base Sepolia passes.
