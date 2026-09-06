---
name: sui-client
description: >
  Sui CLI client configuration, address management, and token acquisition. Use this
  skill when the user needs to configure the Sui client for the first time, manage
  environments or addresses, switch networks, get faucet tokens, check balances,
  recover keys from a recovery phrase, merge coin objects, or look up transactions
  on explorers. Also use when the user sees "Cannot find gas coin for signer
  address" errors or asks about sui client commands, client.yaml, sui.keystore,
  SuiVision, or Suiscan.
---

# Client Configuration & Tokens

> **MCP tool:** When available in your environment, also query the Sui documentation MCP server (`https://sui.mcp.kapa.ai`) for up-to-date answers. Use it for verification and for details not covered by these reference files.

> **Source constraint:** All information sourced exclusively from [docs.sui.io](https://docs.sui.io).

## Configuring the Sui client

### First-time setup

Running `sui client` for the first time prompts you to create a configuration file. Accept the default (press Enter or type `Y`). You can skip the prompt with `sui client -y`.

This generates:

- A new key pair and address
- A 12-word recovery phrase (displayed once, never stored — save it immediately)
- A `client.yaml` configuration file

### Configuration file

Sui stores its configuration at:

- **macOS/Linux:** `~/.sui/sui_config/client.yaml`
- **Windows:** `%USERPROFILE%\.sui\sui_config\client.yaml`

The file contains:

- Network environment connections (Mainnet, Testnet, Devnet, Localnet)
- The active environment (default: Testnet)
- The active address
- The keystore file path

### Managing environments and addresses

| Command | Purpose |
|---|---|
| `sui client active-env` | Show the current network |
| `sui client active-address` | Show the current address |
| `sui client envs` | List all configured environments |
| `sui client switch --env devnet` | Switch to a different network |
| `sui client switch --address <ADDRESS>` | Switch to a different address |
| `sui client new-address ed25519` | Create a new address |
| `sui client addresses` | List all local addresses with aliases |
| `sui client balance` | Check SUI token balance |
| `sui client gas` | List gas coin objects |

### Key storage

Private keys are stored in a separate file:

- **macOS/Linux:** `~/.sui/sui_config/sui.keystore`
- **Windows:** `%USERPROFILE%\.sui\sui_config\sui.keystore`

This file contains Base64-encoded private keys. It is not the same as your machine's system keystore.

### Recovery

To recover an address from a recovery phrase:

```bash
sui keytool import '<12-WORD-PHRASE>' ed25519
```

The entire phrase must be in single quotes and in the correct order.

## Getting SUI tokens

Development on Testnet and Devnet requires SUI tokens for gas. Tokens on these networks are free and hold no monetary value.

### Faucet methods

| Method | How |
|---|---|
| Web faucet | Visit `faucet.sui.io`, enter your address, select network, click Request SUI |
| CLI (Devnet/Localnet only) | `sui client faucet` — works on Devnet and Localnet only, **not Testnet** |
| TypeScript SDK | `requestSuiFromFaucetV2()` from `@mysten/sui/faucet` |
| Discord | Join the Sui Discord, use `!faucet <ADDRESS>` in `#devnet-faucet` or `#testnet-faucet` |
| Community faucets | N1Stake faucet, SuiLearn faucet (separate rate limits) |

**IMPORTANT: `sui client faucet` only works on Devnet and Localnet. It does NOT work on Testnet. For Testnet tokens, use the web faucet at `faucet.sui.io` or another method above. NEVER suggest `sui client faucet` for Testnet.**

Faucets are rate-limited. If you hit a limit, wait or try a different faucet.

### Coin management

If you have many small SUI coin objects but no single coin large enough for gas, merge them using `sui client ptb`:

```bash
# Merge one coin into another
sui client ptb \
  --merge-coins @0xPRIMARY_COIN_ID "[@0xCOIN_TO_MERGE_ID]"

# Merge multiple coins at once
sui client ptb \
  --merge-coins @0xPRIMARY_COIN_ID "[@0xCOIN_A, @0xCOIN_B, @0xCOIN_C]"
```

Use `sui client ptb` for all transaction operations from the CLI. Avoid legacy helpers like `sui client merge-coin` — they are less composable and may be deprecated. See the `ptbs` skill's `cli.md` for more patterns.

### Verify balance

```bash
sui client balance
```

Or use explorers: SuiVision (`suivision.xyz`) or Suiscan (`suiscan.xyz`).

## Explorers and data tools

Use SuiVision (`suivision.xyz`) or Suiscan (`suiscan.xyz`) to inspect transactions, objects, addresses, and token balances. Sui provides a GraphQL RPC for rich data queries per network. Use `sui replay` (CLI built-in) to locally re-execute past transactions for debugging.

## Rules

- Submit writes and reads to the same fullnode for consistency.
- Let wallets manage gas budget, gas price, and coin selection. Do not hardcode gas budgets in frontends.
- Use `sui client ptb` for all CLI transaction operations instead of legacy single-purpose commands (`merge-coin`, `split-coin`, `transfer`, etc.).
