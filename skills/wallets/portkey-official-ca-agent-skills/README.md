# Portkey CA Agent Skills

> AI Agent toolkit for [Portkey Wallet](https://portkey.finance) on the [aelf](https://aelf.com) blockchain — Email registration, login, transfers, guardian management, and generic contract calls.

[中文文档](./README.zh-CN.md)
[![Unit Tests](https://github.com/Portkey-Wallet/ca-agent-skills/actions/workflows/test.yml/badge.svg)](https://github.com/Portkey-Wallet/ca-agent-skills/actions/workflows/test.yml)
[![Coverage](https://img.shields.io/endpoint?url=https://Portkey-Wallet.github.io/ca-agent-skills/coverage.json)](https://Portkey-Wallet.github.io/ca-agent-skills/coverage.json)

## Architecture

```
ca-agent-skills/
├── index.ts                    # SDK entry — direct import for LangChain / LlamaIndex
├── src/
│   ├── core/                   # Pure business logic (no I/O side effects)
│   │   ├── account.ts          # checkAccount, getGuardianList, getHolderInfo, getChainInfo
│   │   ├── auth.ts             # sendVerificationCode, verifyCode, registerWallet, recoverWallet
│   │   ├── assets.ts           # getTokenBalance, getTokenList, getNftCollections, getNftItems, getTokenPrice
│   │   ├── transfer.ts         # sameChainTransfer, crossChainTransfer, recoverStuckTransfer
│   │   ├── guardian.ts         # addGuardian, removeGuardian
│   │   ├── contract.ts         # managerForwardCall, callContractViewMethod
│   │   └── keystore.ts         # Encrypted wallet persistence (save, unlock, lock)
│   └── mcp/
│       └── server.ts           # MCP adapter — for Claude Desktop, Cursor, GPT, etc.
├── portkey_query_skill.ts      # CLI adapter — query commands
├── portkey_auth_skill.ts       # CLI adapter — registration & login commands
├── portkey_tx_skill.ts         # CLI adapter — transfer & guardian commands
├── cli-helpers.ts              # CLI output helpers
├── bin/
│   └── setup.ts                # One-command setup for AI platforms
├── lib/
│   ├── config.ts               # Network config, env overrides
│   ├── types.ts                # TypeScript interfaces & enums
│   ├── aelf-client.ts          # aelf-sdk wrapper (wallet, contract, signing)
│   └── http.ts                 # HTTP client for Portkey backend API
└── __tests__/                  # Unit / Integration / E2E tests
```

**Core + Adapters pattern:** Three adapters (MCP, CLI, SDK) call the same Core functions — zero duplicated logic.

## Features

| # | Category | Capability | MCP Tool | CLI Command | SDK Function |
|---|----------|-----------|----------|-------------|--------------|
| 1 | Account | Check email registration | `portkey_check_account` | `check-account` | `checkAccount` |
| 2 | Account | Get guardian list | `portkey_get_guardian_list` | `guardian-list` | `getGuardianList` |
| 3 | Account | Get CA holder info | `portkey_get_holder_info` | `holder-info` | `getHolderInfo` |
| 4 | Account | Get chain info | `portkey_get_chain_info` | `chain-info` | `getChainInfo` |
| 5 | Auth | Get verifier server | `portkey_get_verifier` | `get-verifier` | `getVerifierServer` |
| 6 | Auth | Send verification code | `portkey_send_code` | `send-code` | `sendVerificationCode` |
| 7 | Auth | Verify code | `portkey_verify_code` | `verify-code` | `verifyCode` |
| 8 | Auth | Register wallet | `portkey_register` | `register` | `registerWallet` |
| 9 | Auth | Recover wallet (login) | `portkey_recover` | `recover` | `recoverWallet` |
| 10 | Auth | Check status | `portkey_check_status` | `check-status` | `checkRegisterOrRecoveryStatus` |
| 11 | Assets | Token balance | `portkey_balance` | `balance` | `getTokenBalance` |
| 12 | Assets | Token list | `portkey_token_list` | `token-list` | `getTokenList` |
| 13 | Assets | NFT collections | `portkey_nft_collections` | `nft-collections` | `getNftCollections` |
| 14 | Assets | NFT items | `portkey_nft_items` | `nft-items` | `getNftItems` |
| 15 | Assets | Token price | `portkey_token_price` | `token-price` | `getTokenPrice` |
| 16 | Transfer | Same-chain transfer | `portkey_transfer` | `transfer` | `sameChainTransfer` |
| 17 | Transfer | Cross-chain transfer | `portkey_cross_chain_transfer` | `cross-chain-transfer` | `crossChainTransfer` |
| 18 | Transfer | Transaction result | `portkey_tx_result` | `tx-result` | `getTransactionResult` |
| 19 | Transfer | Recover stuck transfer | `portkey_recover_stuck_transfer` | `recover-stuck-transfer` | `recoverStuckTransfer` |
| 20 | Guardian | Add guardian | `portkey_add_guardian` | `add-guardian` | `addGuardian` |
| 21 | Guardian | Remove guardian | `portkey_remove_guardian` | `remove-guardian` | `removeGuardian` |
| 22 | Contract | ManagerForwardCall | `portkey_forward_call` | `forward-call` | `managerForwardCall` |
| 23 | Contract | View method call | `portkey_view_call` | `view-call` | `callContractViewMethod` |
| 24 | Wallet | Create wallet | `portkey_create_wallet` | `create-wallet` | `createWallet` |
| 25 | Wallet | Save keystore | `portkey_save_keystore` | `save-keystore` | `saveKeystore` |
| 26 | Wallet | Unlock wallet | `portkey_unlock` | `unlock` | `unlockWallet` |
| 27 | Wallet | Lock wallet | `portkey_lock` | `lock` | `lockWallet` |
| 28 | Wallet | Wallet status | `portkey_wallet_status` | `wallet-status` | `getWalletStatus` |
| 29 | Wallet | Get active wallet context | `portkey_get_active_wallet` | — | `getActiveWallet` |
| 30 | Wallet | Set active wallet context | `portkey_set_active_wallet` | — | `setActiveWallet` |
| 31 | Wallet | Manager sync status | `portkey_manager_sync_status` | `manager-sync-status` | `checkManagerSyncState` |

## Contract Call Routing

Choose the contract tool by method type, not just by wallet type.

- `forward-call` / `managerForwardCall` are for state-changing methods only.
- `view-call` / `callContractViewMethod` are for `Get*` and other read-only methods.
- For `Empty`-input view methods such as `GetConfig`, omit `--params` entirely so the tool performs `.call()` with no arguments.
- If a read-only method is routed through `forward-call`, the result is a `CA.ManagerForwardCall` receipt, not the inner method's decoded view return payload.
- `VirtualTransactionCreated` is expected on successful forwarded writes. It proves that the CA contract created the inner call, but it is not the decoded return value and not a standalone proof of final business success.

Resonance examples:

```bash
# Read-only queue status lookup
bun run portkey_query_skill.ts view-call \
  --rpc-url https://tdvv-public-node.aelf.io \
  --contract-address 28Lot71VrWm1WxrEjuDqaepywi7gYyZwHysUcztjkHGFsPPrZy \
  --method-name GetPairQueueStatus \
  --params '"<address>"'

# State-changing queue join
bun run portkey_tx_skill.ts forward-call \
  --login-email "user@example.com" \
  --password "your-password" \
  --ca-hash "<caHash>" \
  --contract-address 28Lot71VrWm1WxrEjuDqaepywi7gYyZwHysUcztjkHGFsPPrZy \
  --method-name JoinPairQueue \
  --args '{}' \
  --chain-id tDVV
```

## Wallet Persistence (Keystore)

Manager private keys are encrypted and stored locally using aelf-sdk's keystore scheme (scrypt + AES-128-CTR).

**Storage location:** `~/.portkey/ca/{network}.keystore.json`

### First-time setup (after registration/recovery)

```bash
# AI flow: create_wallet → register → check_status → save_keystore(password)
# The wallet is auto-unlocked after saving.
```

### New conversation

```bash
# AI calls portkey_wallet_status to check the active or targeted keystore
# For profile keystores, pass --login-email (or use the active CA profile from a prior save/recover)
# If locked, ask for password → portkey_unlock(password)
# If the password was forgotten, switch to recover-and-save with fresh guardian verification codes
# Write operations in the same process now work automatically
```

### Manual CLI usage

```bash
# Save keystore
bun run portkey_auth_skill.ts save-keystore \
  --password "your-password" \
  --private-key "hex-key" \
  --mnemonic "word1 word2 ..." \
  --ca-hash "xxx" --ca-address "ELF_xxx_tDVV" \
  --origin-chain-id "tDVV"

# Unlock
bun run portkey_auth_skill.ts unlock --password "your-password"

# Or target a specific profile/keystore file
bun run portkey_auth_skill.ts unlock --password "your-password" --login-email "user@example.com"

# If the password was forgotten, re-login / recover and save a new reusable keystore
bun run portkey_auth_skill.ts recover-and-save \
  --email "user@example.com" \
  --guardians-approved '[...]' \
  --chain-id AELF \
  --password "new-password"

# Check status
bun run portkey_auth_skill.ts wallet-status

# Lock
bun run portkey_auth_skill.ts lock
```

### How it works

1. **Save** — encrypts the Manager private key + mnemonic with a user-provided password, writes to `~/.portkey/ca/`
2. **Unlock** — decrypts the keystore, loads the wallet into memory for the current process
3. **Lock** — clears the private key from memory
4. **Write operations** — automatically use the unlocked wallet for the current process; falls back to `PORTKEY_PRIVATE_KEY` env var if no keystore is unlocked

### Recommended CA transfer path

```bash
# 1. recover -> save reusable keystore
bun run portkey_auth_skill.ts recover-and-save \
  --email "user@example.com" \
  --guardians-approved '[...]' \
  --chain-id AELF \
  --password "your-password"

# 2. poll manager sync on the target chain
bun run portkey_query_skill.ts manager-sync-status \
  --ca-hash "<caHash>" \
  --chain-id tDVV \
  --manager-address "<managerAddress from recover-and-save or the selected signer>"

# 3. collect fresh transferApprove proofs
# 4. transfer using the saved keystore directly in the tx command
bun run portkey_tx_skill.ts transfer \
  --login-email "user@example.com" \
  --password "your-password" \
  --ca-hash "<caHash>" \
  --token-contract "<tokenContract>" \
  --symbol ELF \
  --to "<receiver>" \
  --amount 101000000 \
  --chain-id tDVV \
  --guardians-approved '[...]'
```

Notes:

- CA write commands can now resolve signer directly from `--login-email` + `--password`, so they no longer depend on a previous `unlock` from another CLI process.
- Same-chain and cross-chain transfers now check whether the current manager is already synced to the target chain before sending any transaction.
- Generic `forward-call` now performs the same manager sync precheck before fee preview or transaction send.
- `wallet-status` returns `recommendedAction` and `userHint` when a local keystore exists but is still locked. `recommendedAction` is the machine-routable next step (`unlock`), while `userHint` carries the fallback guidance for wrong profile selection or forgotten passwords.
- Transfer results include a fee preview when the chain can calculate it, including `chargingAddress` and whether the CA appears to be paying the fee.

## Cross-skill signing

- `portkey_save_keystore` and `portkey_unlock` automatically update shared active wallet context.
- Other write-capable skills can resolve signer by `explicit -> active context -> env` (auto mode).
- Shared context stores pointers only (no plaintext private key).

## Prerequisites

- [Bun](https://bun.sh) >= 1.0
- An aelf wallet private key or an unlocked keystore (for write operations only)

## Quick Start

### 1. Install

```bash
bun add @portkey/ca-agent-skills

# Or clone locally
git clone https://github.com/AwakenFinance/ca-agent-skills.git
cd ca-agent-skills
bun install
```

### 2. Configure

```bash
cp .env.example .env
# Edit .env — add your PORTKEY_PRIVATE_KEY (only for write operations)
```

### 3. One-Command Setup

```bash
# Claude Desktop
bun run bin/setup.ts claude

# Cursor (project-level)
bun run bin/setup.ts cursor

# Cursor (global)
bun run bin/setup.ts cursor --global

# OpenClaw — output config to stdout
bun run bin/setup.ts openclaw

# OpenClaw — merge into existing config
bun run bin/setup.ts openclaw --config-path ./my-openclaw.json

# IronClaw — install trusted skill + stdio MCP server
bun run bin/setup.ts ironclaw

# Check status (Claude, Cursor, OpenClaw, IronClaw)
bun run bin/setup.ts list

# Remove
bun run bin/setup.ts uninstall claude
bun run bin/setup.ts uninstall cursor
bun run bin/setup.ts uninstall openclaw --config-path ./my-openclaw.json
bun run bin/setup.ts uninstall ironclaw
```

### IronClaw

```bash
# Install trusted skill + stdio MCP server
bun run bin/setup.ts ironclaw

# Remove IronClaw integration
bun run bin/setup.ts uninstall ironclaw
```

The IronClaw setup does two things by default:

- Writes a stdio MCP server entry to `~/.ironclaw/mcp-servers.json`
- Copies this repo's `SKILL.md` to `~/.ironclaw/skills/portkey-ca-agent-skills/SKILL.md`

Important trust model note:

- Use the trusted skill path above for write-capable CA wallet operations.
- Do **not** rely on `~/.ironclaw/installed_skills/` for this package if you need registration, recovery, transfer, guardian management, or other write actions.
- IronClaw attenuates installed skills to read-only tools, which can make the agent appear to "query only" even though the MCP server is available.

The MCP server exposes destructive annotations for CA write operations so IronClaw can request approval before registration, recovery, transfer, guardian, and contract calls.
For compatibility, the MCP server currently emits both standard MCP camelCase annotations and IronClaw-compatible snake_case annotations because the current IronClaw source parses snake_case fields for MCP approval hints.

Remote activation contract:

- GitHub repo/tree URLs are discovery sources only, not the final IronClaw install payload.
- Preferred IronClaw activation from npm: `bunx -p @portkey/ca-agent-skills portkey-ca-setup ironclaw`
- Prefer ClawHub / managed install for OpenClaw when available; otherwise use `bunx -p @portkey/ca-agent-skills portkey-ca-setup openclaw`
- Local repo checkout remains a development smoke-test path only.
- Migration note: `portkey-setup` was removed in `2.0.0`; switch npm-based activation to `portkey-ca-setup`.

## Usage

### MCP (Claude Desktop / Cursor)

Add to your MCP config (`mcp-config.example.json`):

```json
{
  "mcpServers": {
    "ca-agent-skills": {
      "command": "bun",
      "args": ["run", "/path/to/ca-agent-skills/src/mcp/server.ts"],
      "env": {
        "PORTKEY_PRIVATE_KEY": "your_private_key_here",
        "PORTKEY_NETWORK": "mainnet"
      }
    }
  }
}
```

### OpenClaw

The `openclaw.json` in the project root defines 13 CLI-based tools for OpenClaw. Use `bun run bin/setup.ts openclaw` to generate or merge the config.

### CLI

```bash
# Check if email is registered
bun run portkey_query_skill.ts check-account --email user@example.com

# Get chain info
bun run portkey_query_skill.ts chain-info

# Create wallet
bun run portkey_auth_skill.ts create-wallet

# Resolve the correct flow + chain first
bun run portkey_query_skill.ts prepare-auth-flow --email user@example.com

# Low-level auth tools require explicit chainId from prepare-auth-flow.resolvedChainId
bun run portkey_auth_skill.ts get-verifier --chain-id <resolvedChainId>
bun run portkey_auth_skill.ts send-code --email user@example.com --verifier-id <id> --operation recovery --chain-id <resolvedChainId>
bun run portkey_auth_skill.ts verify-code --email user@example.com --code 123456 --verifier-id <id> --session-id <sid> --operation recovery --chain-id <resolvedChainId>

# Token list strategy: aa | auto | eoa (default: auto)
bun run portkey_query_skill.ts token-list --ca-address-infos '[{"chainId":"tDVV","caAddress":"xxx"}]' --strategy auto

# Transfer tokens (requires PORTKEY_PRIVATE_KEY env)
bun run portkey_tx_skill.ts transfer --ca-hash xxx --token-contract xxx --symbol ELF --to xxx --amount 100000000 --chain-id tDVV
```

Recovery proof validation:
- `recover` now validates each guardian proof locally before submitting.
- Guardian `verificationDoc` must come from `verify-code` with `--operation recovery`; register proofs are rejected.

### SDK

```typescript
import { getConfig, checkAccount, createWallet, getTokenBalance } from '@portkey/ca-agent-skills';

const config = getConfig({ network: 'mainnet' });

// Check account
const account = await checkAccount(config, { email: 'user@example.com' });

// Create wallet
const wallet = createWallet();

// Get balance
const balance = await getTokenBalance(config, {
  caAddress: 'xxx',
  chainId: 'tDVV',
  symbol: 'ELF',
});
```

## Network

| Network | Chain IDs | AA API URL | EOA API URL |
|---------|-----------|------------|-------------|
| mainnet (default) | AELF, tDVV | `https://aa-portkey.portkey.finance` | `https://eoa-portkey.portkey.finance` |

`testnet` has been decommissioned and is no longer supported at runtime.

Asset query strategy (`token-list`):
- `aa`: query AA endpoint only (`/api/app/user/assets/token`).
- `auto` (default): AA first; if `401 Unauthorized`, auto-fallback to EOA endpoint.
- `eoa`: query EOA endpoint only.
- Fallback can be disabled with `PORTKEY_EOA_FALLBACK_ENABLED=false`.
- Fallback retry behavior is configurable via `PORTKEY_EOA_FALLBACK_RETRY_COUNT` and `PORTKEY_EOA_FALLBACK_RETRY_DELAY_MS`.
- In fallback mode, chain scope is loaded from EOA `chainsinfoindex` dynamically (currently mainnet returns `AELF`, `tDVV`).

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `PORTKEY_PRIVATE_KEY` | Fallback | — | Manager wallet private key (fallback if keystore not unlocked) |
| `PORTKEY_CA_KEYSTORE_PASSWORD` | No | — | Optional password cache for active CA keystore in cross-skill signer resolution |
| `PORTKEY_SKILL_WALLET_CONTEXT_PATH` | No | `~/.portkey/skill-wallet/context.v1.json` | Override shared wallet context path |
| `PORTKEY_NETWORK` | No | `mainnet` | Mainnet only. `testnet` is decommissioned and rejected. |
| `PORTKEY_API_URL` | No | Per network | Override API endpoint |
| `PORTKEY_EOA_API_URL` | No | Per network | Override EOA API endpoint used by token-list fallback |
| `PORTKEY_GRAPHQL_URL` | No | Per network | Override GraphQL endpoint |
| `PORTKEY_EOA_FALLBACK_ENABLED` | No | `true` | Enable/disable AA -> EOA fallback in token-list auto mode |
| `PORTKEY_EOA_FALLBACK_RETRY_COUNT` | No | `2` | Fallback retry attempts (including first attempt) |
| `PORTKEY_EOA_FALLBACK_RETRY_DELAY_MS` | No | `200` | Delay between fallback retries in milliseconds |

## Testing

```bash
bun test                    # All tests
bun run test:unit           # Unit tests only
bun run test:integration    # Integration (requires network)
bun run test:e2e            # E2E (requires private key)
```

### IronClaw Smoke Test

1. Run `bun run bin/setup.ts ironclaw`
2. Ask a read prompt like `show my guardian list for this Portkey CA wallet`
3. Ask a local write prompt like `create a new Portkey CA wallet`
4. Ask a network write prompt like `transfer 1 ELF from my CA wallet`
5. Confirm CA prompts stay on this skill and EOA wallet-lifecycle prompts do not

## Security

- Never commit your `.env` file (git-ignored by default)
- Private keys are only needed for write operations (transfer, guardian management, contract calls)
- **Keystore encryption**: Manager private keys are encrypted with scrypt (N=8192) + AES-128-CTR via aelf-sdk's keystore module. Files are stored with `0600` permissions.
- **In-memory lifecycle**: private keys exist in memory only while unlocked; `portkey_lock` clears them immediately
- When using MCP, the keystore password only exists in the AI conversation context — it is never written to disk
- `PORTKEY_PRIVATE_KEY` env var is supported as a fallback but keystore is the recommended approach

## License

MIT
