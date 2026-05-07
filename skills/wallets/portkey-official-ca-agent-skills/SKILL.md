---
name: "portkey-ca-agent-skills"
version: "2.3.0"
description: "Portkey CA wallet registration/auth/guardian/transfer operations for agents."
activation:
  keywords:
    - ca
    - guardian
    - recovery
    - register
    - auth
    - ca hash
    - portkey
  exclude_keywords:
    - mnemonic
    - import private key
    - eoa
    - wallet create
    - dex
  tags:
    - wallet
    - ca
    - guardian
    - aelf
  max_context_tokens: 1800
---

# Portkey CA Agent Skill

## When to use
- Use this skill when you need CA wallet auth, guardian flow, and transaction operations on aelf.
- Default to this skill for CA identity, guardian, recovery, register, and CA transfer workflows.

## Capabilities
- Auth operations: verifier, email code, register, recover, status
- Query operations: account, guardian, assets, chain config, transfer preflight
- Tx operations: transfer, contract call, approvals, keystore workflows
- Shared wallet context: auto-set active CA profile for cross-skill signer resolution
- Supports SDK, CLI, MCP, OpenClaw, and IronClaw integration from one codebase.

## Safe usage rules
- Never print private keys, mnemonics, or tokens in channel outputs.
- For write operations, require explicit user confirmation and validate parameters before sending transactions.
- Prefer read-only preflight checks first when available.
- Route `Get*` and other read-only contract methods through `view-call` / `callContractViewMethod`, not `forward-call`.
- Route `forward-call` / `managerForwardCall` only to state-changing methods.
- For `Empty`-input view methods such as `GetConfig`, omit params entirely so the runtime performs `.call()` with no arguments.
- Treat backend `3002 / Guardian not exist.` as an unregistered account and route to `register`.
- Before `transfer` / `cross-chain-transfer`, run `transfer-preflight` to decide whether the path is:
  - direct transfer
  - one-time guardian approval
  - transfer-limit modification
  - wallet security upgrade / guardian sync
- Recommended stable write path is:
  - `recover-and-save`
  - poll `manager-sync-status` on the target chain
  - collect fresh `transferApprove` proofs
  - submit `transfer` / `cross-chain-transfer` with `loginEmail + password`
- Older AA/CA accounts recovered on `AELF` and then written on `tDVV` are a high-risk sync scenario; always check `manager-sync-status` before the first `forward-call` / claim / transfer on `tDVV`.
- `transfer-preflight` reports both the transferred asset balance and the chain default fee-token balance (`feeSymbol` / `feeBalance` / `feeDecimals`) when deciding one-time approval eligibility.
- `send-code` / `verify-code` support `transferApprove` for one-time transfer approval proof collection.
- `transfer`, `cross-chain-transfer`, and transfer-related `forward-call` accept optional `guardiansApproved`.
- `transfer`, `cross-chain-transfer`, and generic `forward-call` now block early when the current manager has not yet synced to the target chain.
- CLI write commands can resolve signer directly from CA keystore options (`loginEmail` / `password` / `keystoreFile`) instead of relying on a previous in-memory `unlock`.
- `wallet-status` returns `recommendedAction` / `userHint` when a local keystore exists but is still locked. `recommendedAction=unlock` is the next machine step; `userHint` explains how to verify the selected `loginEmail` / `keystoreFile` first and then route to `recover-and-save` only if the password was truly forgotten.
- `VirtualTransactionCreated` is forwarded-write evidence only; it is not a decoded view payload and not a standalone proof that a read-only contract query succeeded.

## Command recipes
- Start MCP server: `bun run mcp`
- Run CLI entry: `bun run portkey_query_skill.ts chain-info`
- Run transfer preflight: `bun run portkey_query_skill.ts transfer-preflight --ca-hash <hash> --ca-address <addr> --chain-id tDVV --symbol ELF --amount 100000000`
- Run manager sync status: `bun run portkey_query_skill.ts manager-sync-status --ca-hash <hash> --chain-id tDVV --manager-address <addr-from-recover-and-save-or-selected-signer>`
- Read active wallet context: `portkey_get_active_wallet`
- Set active wallet context: `portkey_set_active_wallet`
- Install into IronClaw: `bun run setup ironclaw`
- Generate OpenClaw config: `bun run build:openclaw`
- Verify OpenClaw config: `bun run build:openclaw:check`
- Run CI coverage gate: `bun run test:coverage:ci`

## Distribution / Activation
- GitHub repo/tree URLs are discovery-only for hosts and agents.
- Preferred IronClaw activation from npm: `bunx -p @portkey/ca-agent-skills portkey-ca-setup ironclaw`
- Preferred OpenClaw activation from npm when managed install is unavailable: `bunx -p @portkey/ca-agent-skills portkey-ca-setup openclaw`
- Local repo checkout is for development and smoke tests only.
- Migration note: `portkey-setup` was removed in `2.0.0`; use `portkey-ca-setup` for npm-based activation.

## Limits / Non-goals
- This skill focuses on domain operations and adapters; it is not a full wallet custody system.
- Do not hardcode environment secrets in source code or docs.
- Avoid bypassing validation for external service calls.
- Do not use this skill for EOA mnemonic/private-key wallet lifecycle flows.
