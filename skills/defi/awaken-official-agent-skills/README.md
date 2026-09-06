# Awaken Agent Kit

[![中文文档](https://img.shields.io/badge/docs-%E4%B8%AD%E6%96%87%E6%96%87%E6%A1%A3-blue)](./README.zh-CN.md)
[![Unit Tests](https://github.com/Awaken-Finance/awaken-agent-skills/actions/workflows/test.yml/badge.svg)](https://github.com/Awaken-Finance/awaken-agent-skills/actions/workflows/test.yml)
[![Coverage](https://img.shields.io/endpoint?url=https://Awaken-Finance.github.io/awaken-agent-skills/coverage.json)](https://Awaken-Finance.github.io/awaken-agent-skills/coverage.json)

> AI Agent toolkit for [Awaken DEX](https://awaken.finance) on the [aelf](https://aelf.com) blockchain — swap tokens, manage liquidity, and fetch K-line data.

---

## Architecture

```
awaken-agent-kit/
├── index.ts                  # SDK entry — direct import for LangChain / LlamaIndex
├── src/
│   ├── core/                 # Pure business logic (no I/O side effects)
│   │   ├── query.ts          # getQuote, getPair, getTokenBalance, getTokenAllowance, getLiquidityPositions
│   │   ├── trade.ts          # executeSwap, addLiquidity, removeLiquidity, approveTokenSpending
│   │   └── kline.ts          # fetchKline, getKlineIntervals
│   └── mcp/
│       └── server.ts         # MCP adapter — for Claude Desktop, Cursor, GPT, etc.
├── awaken_query_skill.ts     # CLI adapter — OpenClaw / terminal query commands
├── awaken_trade_skill.ts     # CLI adapter — OpenClaw / terminal trade commands
├── awaken_kline_skill.ts     # CLI adapter — OpenClaw / terminal K-line commands
├── cli-helpers.ts            # CLI output helpers (outputSuccess / outputError)
├── lib/
│   ├── config.ts             # Network config, env overrides, defaults
│   ├── aelf-client.ts        # aelf-sdk wrapper (wallet, contract calls, decimals)
│   └── types.ts              # TypeScript interfaces & constants
├── openclaw.json             # OpenClaw tool definitions
├── mcp-config.example.json   # MCP client config example
├── .env.example              # Environment variable template
└── __tests__/                # Unit / Integration / E2E tests
```

**Core + Adapters pattern:**

| Layer | Location | Role |
|-------|----------|------|
| **Core** | `src/core/` | Pure functions. No `process.exit`, no `console.log`. Throw on error. |
| **CLI Adapter** | `awaken_*_skill.ts` | Thin wrappers using `commander`. Parses args → calls core → outputs JSON. |
| **MCP Adapter** | `src/mcp/server.ts` | Registers core functions as MCP tools for Claude Desktop, Cursor, GPT, etc. |
| **SDK** | `index.ts` | Re-exports core functions + types. `import { executeSwap } from '@awaken-finance/agent-kit'`. |

---

## Features

| # | Category | Capability | CLI Tool | MCP Tool | SDK Function |
|---|----------|-----------|----------|----------|-------------|
| 1 | Query | Swap quote & route | `awaken-query-quote` | `awaken_quote` | `getQuote` |
| 2 | Query | Trade pair info | `awaken-query-pair` | `awaken_pair` | `getPair` |
| 3 | Query | Token balance | `awaken-query-balance` | `awaken_balance` | `getTokenBalance` |
| 4 | Query | Token allowance | `awaken-query-allowance` | `awaken_allowance` | `getTokenAllowance` |
| 5 | Query | Liquidity positions (+ USD) | `awaken-query-liquidity` | `awaken_liquidity` | `getLiquidityPositions` |
| 6 | Trade | Swap tokens | `awaken-trade-swap` | `awaken_swap` | `executeSwap` |
| 7 | Trade | Add liquidity | `awaken-trade-add-liquidity` | `awaken_add_liquidity` | `addLiquidity` |
| 8 | Trade | Remove liquidity | `awaken-trade-remove-liquidity` | `awaken_remove_liquidity` | `removeLiquidity` |
| 9 | Trade | Approve token spending | `awaken-trade-approve` | `awaken_approve` | `approveTokenSpending` |
| 10 | K-Line | Fetch candlestick data | `awaken-kline-fetch` | `awaken_kline_fetch` | `fetchKline` |
| 11 | K-Line | List intervals | `awaken-kline-intervals` | `awaken_kline_intervals` | `getKlineIntervals` |

---

## Prerequisites

- [Bun](https://bun.sh) ≥ 1.0
- An aelf wallet private key (for trade operations only)

---

## Quick Start

### 1. Install

```bash
# As a dependency
bun add @awaken-finance/agent-kit

# Or clone and install locally
git clone https://github.com/AwakenFinance/awaken-agent-skills.git
cd awaken-agent-skills
bun install
```

### 2. Configure

```bash
cp .env.example .env
# Edit .env — add your AELF_PRIVATE_KEY
```

### 3. One-Command Setup (Recommended)

```bash
# Setup for Claude Desktop
bun run bin/setup.ts claude

# Setup for Cursor (project-level)
bun run bin/setup.ts cursor

# Setup for Cursor (global)
bun run bin/setup.ts cursor --global

# Setup for IronClaw
bun run bin/setup.ts ironclaw

# Generate OpenClaw config
bun run bin/setup.ts openclaw

# Check configuration status
bun run bin/setup.ts list

# Remove config from a platform
bun run bin/setup.ts uninstall claude
bun run bin/setup.ts uninstall ironclaw
```

The setup tool auto-detects your OS, resolves paths, and merges config safely (won't overwrite other MCP servers). After setup, edit the generated config to replace `<YOUR_PRIVATE_KEY>` with your actual key.

### IronClaw

```bash
bun run bin/setup.ts ironclaw
bun run bin/setup.ts uninstall ironclaw
```

The IronClaw setup writes a stdio MCP entry to `~/.ironclaw/mcp-servers.json` and installs this repo's `SKILL.md` to `~/.ironclaw/skills/awaken-agent-skills/SKILL.md`.

Important trust model note:

- Use the trusted skill path above for write-capable flows such as swap, liquidity, and approve.
- Do not rely on `~/.ironclaw/installed_skills/` for the primary install path when you need write approval behavior.
- This MCP server emits both standard MCP camelCase annotations and IronClaw-compatible snake_case annotations so the current IronClaw source can honor read/write hints.

Remote activation contract:

- GitHub repo/tree URLs are discovery sources only, not the final IronClaw install payload.
- Preferred IronClaw activation from npm: `bunx -p @awaken-finance/agent-kit awaken-setup ironclaw`
- Prefer ClawHub / managed install for OpenClaw when available; otherwise use `bunx -p @awaken-finance/agent-kit awaken-setup openclaw`
- Local repo checkout remains a development smoke-test path only.

Minimal smoke test:

1. `bun run bin/setup.ts ironclaw`
2. Ask IronClaw for a read prompt like `quote ELF to USDT on Awaken`
3. Ask it to `approve ELF for Awaken` and confirm approval appears before execution

**Advanced options:**

```bash
# Custom config file path
bun run bin/setup.ts claude --config-path /custom/path/config.json

# Custom MCP server path
bun run bin/setup.ts cursor --server-path /my/custom/server.ts

# Force overwrite existing entry
bun run bin/setup.ts claude --force
```

**Config priority (high → low):**

1. Function params (SDK callers)
2. CLI args (`--network`, `--slippage`)
3. MCP env block (`mcp.json` → `env: {}`)
4. Environment variables (`AWAKEN_*`)
5. `.env` file
6. Code defaults

See [`.env.example`](./.env.example) for all available overrides (RPC URL, API URL, contract addresses, slippage, etc.).

---

## Usage

### CLI (OpenClaw / Terminal)

```bash
# Query swap quote
bun run awaken_query_skill.ts quote --symbol-in ELF --symbol-out USDT --amount-in 10

# Query trade pair
bun run awaken_query_skill.ts pair --token0 ELF --token1 USDT --fee-rate 0.3

# Query balance
bun run awaken_query_skill.ts balance --address YOUR_ADDRESS --symbol ELF

# Query liquidity positions
bun run awaken_query_skill.ts liquidity --address YOUR_ADDRESS

# Swap tokens (requires signer via input/context/env)
bun run awaken_trade_skill.ts swap --symbol-in ELF --symbol-out USDT --amount-in 1

# Add liquidity (requires signer via input/context/env)
bun run awaken_trade_skill.ts add-liquidity --token-a ELF --token-b USDT --amount-a 10 --amount-b 5

# Remove liquidity (requires signer via input/context/env)
bun run awaken_trade_skill.ts remove-liquidity --token-a ELF --token-b USDT --lp-amount 0.5

# Fetch K-line data
bun run awaken_kline_skill.ts fetch --pair-id PAIR_UUID --interval 1D

# List K-line intervals
bun run awaken_kline_skill.ts intervals
```

All commands output standardized JSON on success. Errors go to stderr with `[ERROR]` prefix.

### MCP (Claude Desktop / Cursor / GPT)

1. Copy the config from [`mcp-config.example.json`](./mcp-config.example.json) into your AI tool's MCP settings:

   - **Claude Desktop**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Cursor (project)**: `.cursor/mcp.json`
   - **Cursor (global)**: `~/.cursor/mcp.json`

2. Update the path and environment variables:

**EOA mode** (direct private key signing):

```json
{
  "mcpServers": {
    "awaken-agent-kit": {
      "command": "bun",
      "args": ["run", "/ABSOLUTE/PATH/TO/src/mcp/server.ts"],
      "env": {
        "AELF_PRIVATE_KEY": "your_private_key_here",
        "AWAKEN_NETWORK": "mainnet"
      }
    }
  }
}
```

**CA mode** (Portkey Contract Account):

```json
{
  "mcpServers": {
    "awaken-agent-kit": {
      "command": "bun",
      "args": ["run", "/ABSOLUTE/PATH/TO/src/mcp/server.ts"],
      "env": {
        "PORTKEY_PRIVATE_KEY": "your_manager_private_key",
        "PORTKEY_CA_HASH": "your_ca_hash",
        "PORTKEY_CA_ADDRESS": "your_ca_address",
        "AWAKEN_NETWORK": "mainnet"
      }
    }
  }
}
```

3. Start the MCP server manually (for debugging):

```bash
bun run mcp
```

### Cross-Skill signer context (recommended)

Write tools (`swap`, `addLiquidity`, `removeLiquidity`, `approve`) now resolve signer in this order:

1. explicit signer input (`signer.privateKey` or CA tuple)
2. active wallet context from `~/.portkey/skill-wallet/context.v1.json`
3. env fallback (`AELF_PRIVATE_KEY` or `PORTKEY_*`)

`signer` input (optional) supports:

```json
{
  "signerMode": "auto",
  "walletType": "EOA",
  "address": "ELF_...",
  "password": "optional-password",
  "privateKey": "optional-explicit-private-key"
}
```

`signerMode=daemon` is reserved and currently returns `SIGNER_DAEMON_NOT_IMPLEMENTED`.

### SDK (TypeScript / JavaScript)

```typescript
import {
  getQuote,
  executeSwap,
  getNetworkConfig,
  getLiquidityPositions,
} from '@awaken-finance/agent-kit';

// Query a swap quote
const config = getNetworkConfig('mainnet');
const quote = await getQuote(config, {
  symbolIn: 'ELF',
  symbolOut: 'USDT',
  amountIn: '10',
});
console.log(quote);

// Execute a swap (requires privateKey)
const result = await executeSwap(config, wallet, {
  symbolIn: 'ELF',
  symbolOut: 'USDT',
  amountIn: '10',
  slippage: '0.005',
});
console.log(result.transactionId);
```

### OpenClaw

Import the [`openclaw.json`](./openclaw.json) file into your OpenClaw configuration. All 11 tools are pre-configured with descriptions optimized for AI comprehension.

---

## Network

| Network | Chain ID | RPC | Explorer |
|---------|----------|-----|----------|
| **mainnet** (default) | tDVV | `https://tdvv-public-node.aelf.io` | `https://aelfscan.io/tDVV` |
| testnet | tDVW | `https://tdvw-test-node.aelf.io` | `https://testnet.aelfscan.io/tDVW` |

Switch via `--network testnet` (CLI), `AWAKEN_NETWORK=testnet` (env), or pass config directly (SDK).

---

## Testing

```bash
# All tests
bun test

# Unit tests only
bun run test:unit

# Integration tests (requires network access)
bun run test:integration

# E2E tests (requires AELF_PRIVATE_KEY, sends real txns on mainnet)
bun run test:e2e
```

| Test Level | Scope |
|------------|-------|
| **Unit** | Config, types, decimal math, core exports, error paths, MCP server, CLI helpers |
| **Integration** | Awaken API, on-chain view calls, SignalR K-line, core query functions |
| **E2E** | Real swap & liquidity add/remove on mainnet |

---

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `AELF_PRIVATE_KEY` | For trades (EOA) | — | aelf wallet private key |
| `PORTKEY_PRIVATE_KEY` | For trades (CA) | — | Portkey Manager private key |
| `PORTKEY_CA_HASH` | For trades (CA) | — | Portkey CA hash |
| `PORTKEY_CA_ADDRESS` | For trades (CA) | — | Portkey CA address |
| `PORTKEY_WALLET_PASSWORD` | No | — | Optional password cache for EOA wallet context decryption |
| `PORTKEY_CA_KEYSTORE_PASSWORD` | No | — | Optional password cache for CA keystore context decryption |
| `PORTKEY_SKILL_WALLET_CONTEXT_PATH` | No | `~/.portkey/skill-wallet/context.v1.json` | Override active wallet context path |
| `AWAKEN_NETWORK` | No | `mainnet` | `mainnet` or `testnet` |
| `AWAKEN_RPC_URL` | No | Per network | Override RPC endpoint |
| `AWAKEN_API_BASE_URL` | No | Per network | Override API endpoint |
| `AWAKEN_SOCKET_URL` | No | Per network | Override SignalR endpoint |
| `AWAKEN_EXPLORER_URL` | No | Per network | Override explorer URL |
| `AWAKEN_TOKEN_CONTRACT` | No | Per network | Override token contract address |
| `AWAKEN_SWAP_HOOK_CONTRACT` | No | Per network | Override swap hook contract |
| `AWAKEN_DEFAULT_SLIPPAGE` | No | `0.005` | Default slippage tolerance |

---

## Security

- **Never commit your `.env` file.** It is git-ignored by default.
- Private keys are only needed for trade operations (swap, add/remove liquidity, approve). Query and K-line operations are read-only.
- When using MCP, pass the private key via the `env` block in your MCP config — it is not transmitted over the network.

---

## License

MIT
