---
name: gate-dex-cli
version: "2026.3.12-1"
updated: "2026-03-12"
description:
  "Gate Wallet CLI command-line tool. Dual-channel support: MCP (OAuth custodial signing) and OpenAPI (AK/SK
  self-custody signing). Use when users mention gate-wallet, CLI, command-line, openapi-swap, hybrid swap
  and other CLI-related operations. Covers authentication, asset queries, transfers, Swap, market data, and approvals."
---

# Gate DEX CLI

> CLI Command-Line Domain — gate-wallet dual-channel command-line tool, supporting MCP custodial signing and OpenAPI hybrid mode Swap. Covers authentication, assets, transfers, Swap, market data, and approval functions.

**Trigger Scenarios**: When user mentions "gate-wallet", "CLI", "command-line", "openapi-swap", "hybrid swap", "hybrid mode swap", "use CLI to operate", or when other Skills guide users to use CLI tools for operations.

## Installation

Install gate-wallet CLI before first use:

```bash
# Method 1: Use installation script (recommended, includes OpenAPI configuration guidance)
bash gate-dex-wallet/install_cli.sh

# Method 2: Direct npm install
npm install -g gate-wallet-cli
```

**Prerequisites**: Node.js >= 18

**Installation Contents**:
- `gate-wallet` CLI command (global)
- OpenAPI credential configuration (optional, for hybrid mode Swap)

## MCP Server Connection Detection

### First Session Detection

**Before the first MCP tool call in a session, perform a connection probe to confirm Gate Wallet MCP Server availability. Subsequent operations do not require repeated detection.**

```
CallMcpTool(server="gate-wallet", toolName="chain.config", arguments={chain: "eth"})
```

| Result | Handling |
| ------ | -------- |
| Success | MCP Server available, subsequent operations call business tools directly without re-probing |
| Failure | Display configuration guidance based on error type (see error handling below) |

### Runtime Error Fallback

If business tool calls fail during subsequent operations (connection errors, timeouts, etc.), handle according to these rules:

| Error Type | Keywords | Handling |
| ---------- | -------- | -------- |
| MCP Server not configured | `server not found`, `unknown server` | Display MCP Server configuration guidance |
| Remote service unreachable | `connection refused`, `timeout`, `DNS error` | Prompt to check server status and network connection |
| Authentication failed | `401`, `unauthorized`, `x-api-key` | Prompt to contact administrator for API Key |

## Authentication Notes

Most operations in this Skill **require `mcp_token`** (except `tools`/`chain-config`). Before calling any authenticated command, confirm the user is logged in.

- If not logged in → Execute `gate-wallet login` to complete login, then return.
- If command returns `Not logged in` or `token expired` → Execute `gate-wallet login` to re-login first.

## Dual-Channel Architecture

- **MCP Channel**: OAuth login → Server-side custodial signing → Full-featured wallet (balance / transfer / Swap / approval / market queries)
- **OpenAPI Channel** (login-free, self-custody): AK/SK authentication → Client-side signing → DEX Swap transactions. See [gate-dex-trade SKILL](../../gate-dex-trade/SKILL.md)

---

## Channel Routing (MUST evaluate first)

This project has two channels that **overlap on Swap functionality**. Agent MUST evaluate which channel to use **before** executing any swap-related operation.

### Routing Rules (in priority order)

**Rule 1 — Explicit user request (highest priority)**

| User says | Route to | Reason |
| --------- | -------- | ------ |
| "use openapi" / "openapi swap" / "AK/SK" / "direct API" / "DEX API" | **Hybrid or OpenAPI** — see Rule 1a below | User explicitly chose OpenAPI |
| "sign myself" / "use private key" | **OpenAPI channel** → read and follow [gate-dex-trade/SKILL.md](../../gate-dex-trade/SKILL.md) | User explicitly wants self-custody signing |
| "use MCP" / "use wallet" / "custodial signing" / "gate-wallet swap" | **MCP channel** → continue with this SKILL | User explicitly chose MCP |

**Rule 1a — OpenAPI request sub-routing (MUST check login status)**

When user requests OpenAPI, Agent MUST check whether the user is logged in (`~/.gate-wallet/auth.json` exists and valid):

| Condition | Route to | Command | Reason |
| --------- | -------- | ------- | ------ |
| User is logged in (has MCP token) | **Hybrid mode** → `openapi-swap` CLI command | `gate-wallet openapi-swap --chain ... --from ... --to ... --amount ...` | Uses OpenAPI for quote/build/submit + MCP for custodial signing. One CLI command handles everything. |
| User is NOT logged in but has private key | **OpenAPI channel** → [gate-dex-trade/SKILL.md](../../gate-dex-trade/SKILL.md) | Agent follows gate-dex-trade Skill | Self-custody signing with user's private key |
| User is NOT logged in and no private key | **Hybrid mode** (prompt login first) | `gate-wallet login` then `gate-wallet openapi-swap ...` | Login to enable MCP signing, then use hybrid flow |

> **Key insight**: "use openapi" does NOT mean "sign with private key myself". Most custodial wallet users want OpenAPI's quote/build advantages (custom fee_recipient, gas price queries, etc.) while still using MCP's convenient custodial signing. The `openapi-swap` hybrid command is designed exactly for this.

**Rule 2 — MCP-only operations (no overlap, always MCP)**

These features exist ONLY in MCP. No routing decision needed:

`balance` · `address` · `tokens` · `send` / `transfer` · `approve` / `revoke` · `gas` · `token-info` · `token-risk` · `token-rank` · `kline` · `liquidity` · `tx-stats` · `swap-tokens` · `bridge-tokens` · `new-tokens` · `rpc` · `chain-config` · `tx-detail` · `tx-history`

**Rule 3 — Overlapping Swap operations (agent decides)**

When user requests swap/quote/swap-detail/swap-history WITHOUT specifying a channel:

| Condition | Preferred channel | Reason |
| --------- | ----------------- | ------ |
| User is logged in (`~/.gate-wallet/auth.json` exists and valid) | **MCP** (`gate-wallet swap`) | Simpler flow, no private key needed, one-shot swap |
| User is NOT logged in but `~/.gate-dex-openapi/config.json` exists | **OpenAPI** | Already has AK/SK configured, can proceed without login |
| User is NOT logged in and no OpenAPI config exists | **MCP** (prompt login first) | MCP is the default path, guide user to login |
| User mentions private key / self-custody / fine-grained control | **OpenAPI** | OpenAPI allows step-by-step control and self-signing |
| User needs features only in OpenAPI (custom fee_recipient, MEV protection, gas price query, chain list query) | **Hybrid** (`gate-wallet openapi-swap`) | OpenAPI features + MCP custodial signing |

> **Hybrid mode priority**: When the user needs OpenAPI features but is logged in (has MCP token), **always use `gate-wallet openapi-swap`** — never construct inline Python/Node scripts to manually call OpenAPI quote → build → sign. The CLI command handles RLP encoding, gas buffer, signing format, and timeout internally.

### Overlap Reference

| Function | MCP Tool | OpenAPI Actions |
| -------- | -------- | --------------- |
| Swap quote | `tx.quote` | `trade.swap.quote` |
| Execute swap | `tx.swap` (one-shot) | `quote` → `approve` → `build` → `submit` |
| Swap order detail | `tx.swap_detail` | `trade.swap.status` |
| Swap history | `tx.history_list` | `trade.swap.history` |

## Quick Start

```bash
gate-wallet login
gate-wallet balance
gate-wallet send --chain ETH --to 0x... --amount 0.01

# Interactive REPL mode
gate-wallet
```

---

## Credential Storage

All credentials are stored in `~/.gate-wallet/` (user home directory):

| File | Content | Created by |
| ---- | ------- | ---------- |
| `~/.gate-wallet/auth.json` | OAuth `mcp_token` (30-day TTL) | `login` command (auto) |

---

## Agent Usage

Agent should use **single-command mode** — each command runs independently and exits.

> **IMPORTANT**: Agent runs in a non-interactive shell (no stdin). Any command that prompts for confirmation (`y/N`) will hang. **Always pass `-y` / `--yes`** for commands that support it (e.g. `openapi-swap -y`). For commands without a `-y` flag, use the quote/preview step to show details to the user, get explicit confirmation in chat, then execute.

```bash
gate-wallet balance
gate-wallet gas ETH
gate-wallet token-rank --chain eth
gate-wallet call wallet.get_addresses
gate-wallet openapi-swap --chain ETH --from - --to 0x... --amount 0.01 -y
```

### Login Flow (first time / token expired)

Triggered when any command returns `Not logged in. Run: login` or `~/.gate-wallet/auth.json` is missing:

1. **Start login in background** (non-blocking, let user complete browser auth):

```bash
gate-wallet login
# For Google: gate-wallet login --google
```

2. **Browser auto-opens** the authorization page
3. **Poll terminal output** — wait 10-15s, then read terminal file for keywords:
   - `login successful` → proceed with subsequent commands
   - `Waiting for authorization` → user hasn't authorized yet, keep polling (every 10s, max 120s)
   - `Login failed` / `Login timed out` → prompt user to retry
4. **On success**: token auto-saved to `~/.gate-wallet/auth.json`

> **Important**: Login is interactive (opens browser). Run it in background, then poll terminal output for completion.

### MCP Tool Call Fallback Strategy

**Level 1 — CLI shortcut commands** (preferred, auto-handles auth):

```bash
gate-wallet balance
gate-wallet send --chain ETH --to 0x... --amount 0.1
```

**Level 2 — CLI `call` generic invocation** (when no shortcut exists):

```bash
gate-wallet call wallet.get_addresses
gate-wallet call tx.gas '{"chain":"SOL","from":"BTYz..."}'
```

**Level 3 — MCP JSON-RPC** (when Level 2 returns 401):

> The CLI `call` subcommand does not guarantee auto-injection of `mcp_token` for all tools. On any 401, fall back to raw JSON-RPC, reading `mcp_token` from `~/.gate-wallet/auth.json`.

```bash
# 1. Initialize (get session-id, reusable until timeout)
curl -s -D- -X POST {MCP_URL} \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: mcp_ak_demo' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"gate-wallet-cli","version":"1.0.0"}}}'

# 2. Call tool (extract mcp-session-id from response headers)
curl -s -X POST {MCP_URL} \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: mcp_ak_demo' \
  -H 'mcp-session-id: {session_id}' \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"{tool_name}","arguments":{"mcp_token":"{mcp_token}", ...}}}'
```

- Same session can call multiple tools without re-initializing
- `result.content[0].text` is a JSON string — requires double `JSON.parse`
- Session timeout returns "Invalid session ID" — re-initialize

### Fallback: REST API Manual Login

Only when `gate-wallet login` is unavailable (e.g. deps broken):

1. Read `MCP_URL` from `~/.gate-wallet/.env`, strip `/mcp` to get `baseUrl`
2. `curl -s -X POST {baseUrl}/oauth/gate/device/start -H 'Content-Type: application/json' -d '{}'`
3. Open returned `verification_url` with `open` (macOS), prompt user to authorize in browser
4. Poll `{baseUrl}/oauth/gate/device/poll` every 5s until `status: "ok"`
5. Extract `mcp_token`, write to `~/.gate-wallet/auth.json`

---

## Commands

### Authentication

| Command | Description |
| ------- | ----------- |
| `login` | Gate OAuth login (default) |
| `login --google` | Google OAuth login |
| `status` | Check current auth status |
| `logout` | Logout and clear local token |

### Wallet Queries

| Command | Description |
| ------- | ----------- |
| `balance` | Total asset value (USD) |
| `address` | Wallet addresses per chain (EVM / SOL) |
| `tokens` | Token list with balances |

### Transfers

| Command | Description |
| ------- | ----------- |
| `send --chain <chain> --to <addr> --amount <n> [--token <contract>] [--token-decimals <d>] [--token-symbol <sym>]` | One-shot transfer (preview → sign → broadcast) |
| `transfer --chain <chain> --to <addr> --amount <n> [--token <contract>] [--token-decimals <d>] [--token-symbol <sym>]` | Preview only (no execution) |
| `gas [chain]` | Gas fee estimation |
| `sol-tx --to <addr> --amount <n> [--mint <token>]` | Build SOL unsigned tx (native SOL only) |
| `sign-tx <raw_tx>` | Sign raw transaction (server-side) |
| `send-tx --chain <chain> --hex <signed_tx> --to <addr>` | Broadcast signed tx |
| `tx-detail <tx_hash>` | Transaction details |
| `tx-history [--page <n>] [--limit <n>]` | Transaction history |

### Token Approval

Via MCP tool `tx.approve_preview`:

| Scenario | amount | action | Returns |
| -------- | ------ | ------ | ------- |
| Exact approve | `"100"` | omit | `approve` |
| Unlimited approve | `"unlimited"` | omit | `approve_unlimited` |
| Revoke (EVM) | `"0"` | omit | `revoke` |
| Revoke (Solana) | `"0"` | `"revoke"` | `revoke` |

EVM params: `owner`, `spender`, `amount`, `token_contract`, `token_decimals`, `chain`
Solana params: `owner`, `spender`(=delegate), `amount`, `token_mint`, `token_decimals`, `chain`="SOL"

### Swap

| Command | Description |
| ------- | ----------- |
| `quote --from-chain <id> --to-chain <id> --from <token> --to <token> --amount <n>` | Get swap quote (MCP) |
| `swap --from-chain <id> --to-chain <id> --from <token> --to <token> --amount <n>` | One-shot swap via MCP (Quote→Build→Sign→Submit) |
| `openapi-swap --chain <chain> --from <token> --to <token> --amount <n>` | **Hybrid swap: OpenAPI quote/build/submit + MCP sign** |
| `swap-detail <order_id>` | Swap order details |
| `swap-history [--page <n>] [--limit <n>]` | Swap/bridge history |

`swap` extra options: `--slippage <pct>` · `--native-in <0|1>` · `--native-out <0|1>` · `--wallet <addr>` · `--to-wallet <addr>`

`openapi-swap` extra options: `--slippage <pct>` (default 0.03) · `-y, --yes` (skip confirmation)

> **Agent MUST use `openapi-swap` for hybrid mode** — never manually call OpenAPI APIs + MCP signing via inline scripts. The CLI handles RLP encoding, EIP-1559 formatting, gas buffer (1.2x), nonce fetching, Solana base58 encoding, and `signed_tx_string` JSON array formatting internally. Supports both EVM chains and Solana.

### Market Data & Token Queries

| Command | Description |
| ------- | ----------- |
| `kline --chain <chain> --address <addr>` | K-line / candlestick data |
| `liquidity --chain <chain> --address <addr>` | Liquidity pool events |
| `tx-stats --chain <chain> --address <addr>` | Trading volume stats |
| `swap-tokens [--chain <chain>] [--search <keyword>]` | Swappable token list |
| `bridge-tokens [--src-chain <chain>] [--dest-chain <chain>]` | Cross-chain bridge tokens |
| `token-info --chain <chain> --address <addr>` | Token details (price / mcap) |
| `token-risk --chain <chain> --address <addr>` | Security audit |
| `token-rank [--chain <chain>] [--limit <n>]` | Price change rankings |
| `new-tokens [--chain <chain>] [--start <RFC3339>]` | Filter tokens by creation time |

### Chain / RPC / Debug

| Command | Description |
| ------- | ----------- |
| `chain-config [chain]` | Chain configuration |
| `rpc --chain <chain> --method <method> [--params '<json>']` | JSON-RPC call |
| `tools` | List all MCP tools |
| `call <tool> [json]` | Call any MCP tool directly |

---

## Domain Knowledge

### Authentication Model

- **MCP**: Gate/Google OAuth → `mcp_token` stored in `~/.gate-wallet/auth.json` (30-day TTL)

### Custodial Wallet Architecture

```
OAuth login → mcp_token saved locally → server-side signing → on-chain broadcast
```

Users never handle private keys or mnemonics. `sign-tx` is server-side signing.

### Amount Format

All amount parameters use **human-readable values**, NOT chain-native smallest units.

| Correct | Wrong |
| ------- | ----- |
| `--amount 0.1` (0.1 ETH) | `--amount 100000000000000000` (wei) |
| `--amount 1` (1 SOL) | `--amount 1000000000` (lamports) |

### Native Token Handling

In swap operations, native tokens (ETH/SOL/BNB) use `-` as address, and require `--native-in 1` or `--native-out 1`.

### Common Stablecoin Addresses

| Chain | USDT | USDC |
| ----- | ---- | ---- |
| Ethereum | `0xdAC17F958D2ee523a2206206994597C13D831ec7` | `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48` |
| BSC | `0x55d398326f99059fF775485246999027B3197955` | `0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d` |
| Arbitrum | `0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9` | `0xaf88d065e77c8cC2239327C5EDb3A432268e5831` |
| Solana | `Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB` | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` |

Use `token-info` or `swap-tokens --search <symbol>` to look up other token addresses.

### Chain Identifiers

| Chain | Chain ID | CLI Param |
| ----- | -------- | --------- |
| Ethereum | 1 | ETH |
| BSC | 56 | BSC |
| Polygon | 137 | POLYGON |
| Arbitrum | 42161 | ARB |
| Base | 8453 | BASE |
| Optimism | 10 | OP |
| Avalanche | 43114 | AVAX |
| Solana | 501 | SOL |

Chain names are case-insensitive. Swap commands use Chain ID; other commands use CLI param name.

---

## On-Chain Operation Flow

All fund-moving operations follow a unified **preview → confirm → execute** pattern:

1. **Pre-check**: `address` to get correct chain address → `balance`/`tokens` to confirm sufficient funds (including gas)
2. **Preview**: `transfer` (transfer) / `tx.approve_preview` (approval) / `quote` (swap)
3. **User confirmation**: Display key details, wait for explicit user approval
4. **Sign + broadcast**: `sign-tx` → `send-tx` / or `send`/`swap` one-shot commands
5. **Verify**: `tx-detail <hash>` / `swap-detail <order_id>`

> **NEVER execute signing without user confirmation.**

### Address Format Validation

| Chain Type | Format | Example |
| ---------- | ------ | ------- |
| EVM (ETH/BSC/ARB/...) | `0x` + 40 hex chars | `0xdb918f36a1c282a042758b544c64ae5a1d5767a2` |
| Solana | Base58 (32-44 chars, no `0`/`O`/`I`/`l`) | `BTYzBJ5N7L9exV4UAvHnPhfmovz4tmbVvagar4U7bfxE` |

EVM and Solana addresses are NOT interchangeable. Always call `address` first to get the correct chain-specific address.

---

## Typical Workflows

### Token Research

```
token-rank --chain eth --limit 10             # Top gainers
token-risk --chain eth --address 0x...        # Security audit
tx-stats --chain eth --address 0x...          # Trading volume
liquidity --chain eth --address 0x...         # Liquidity events
token-info --chain eth --address 0x...        # Full details
kline --chain eth --address 0x... --period 1h # K-line chart
```

### Safe Transfer

```
balance                                    # Confirm sufficient funds
gas ETH                                    # Estimate gas
transfer --chain ETH --to 0x... --amount 0.1  # Preview (dry run)
send --chain ETH --to 0x... --amount 0.1      # Execute after confirmation
tx-detail <hash>                           # Verify on-chain
```

### Solana SPL Token Transfer

SPL token transfer differs from native SOL and EVM ERC20. Key differences:

1. **Requires `token_mint` + `token_decimals`**: The MCP `tx.transfer_preview` tool requires both fields for SPL transfers. The CLI `send` command auto-resolves `token_decimals` and `token` symbol via `token_list_swap_tokens`, or accepts `--token-decimals` / `--token-symbol` explicitly.
2. **`token` param for display**: `tx.transfer_preview` uses the `token` parameter for display labels (default "USDT"). The CLI now auto-resolves the token symbol from `token_list_swap_tokens` and passes it as `token`. You can also specify `--token-symbol <sym>` explicitly.
3. **`tx.get_sol_unsigned` is native-SOL-only**: This tool rebuilds the unsigned tx with a fresh blockhash, but only supports native SOL transfers. For SPL tokens, the CLI skips this step and uses the `unsigned_tx_hex` from `transfer_preview` directly (blockhash valid ~90s, sufficient for immediate signing).
4. **Recipient ATA (Associated Token Account)**: If the recipient has no ATA for the SPL token, the transaction includes ATA creation (~0.002 SOL rent). Ensure sufficient SOL balance for both gas + rent.

```
# CLI one-shot (recommended — handles decimals + symbol automatically)
send --chain SOL --to <sol_addr> --amount 0.001 --token <token_mint>

# With explicit decimals and symbol
send --chain SOL --to <sol_addr> --amount 0.001 --token <token_mint> --token-decimals 6 --token-symbol TRUMP

# Preview only
transfer --chain SOL --to <sol_addr> --amount 0.001 --token <token_mint> --token-symbol TRUMP
```

**Fallback (Level 3 JSON-RPC)** — when CLI `call` returns 401 for `tx.transfer_preview`:

```
# 1. Initialize MCP session
curl -s -D- -X POST {MCP_URL} -H 'Content-Type: application/json' -H 'x-api-key: mcp_ak_demo' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{...}}'

# 2. Call tx.transfer_preview with token_mint + token_decimals
curl -s -X POST {MCP_URL} -H 'mcp-session-id: {session_id}' \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"tx.transfer_preview","arguments":{"mcp_token":"{token}","chain":"SOL","from":"{sol_addr}","to":"{recipient}","amount":"0.001","token_mint":"{mint}","token_decimals":6}}}'

# 3. Sign: wallet.sign_transaction(raw_tx=unsigned_tx_hex, chain=SOL)
# 4. Broadcast: tx.send_raw_transaction
```

### Swap (MCP one-shot)

```
quote --from-chain 1 --to-chain 1 --from - --to 0xA0b8... --amount 0.01 --native-in 1 --native-out 0
swap --from-chain 1 --to-chain 1 --from - --to 0xA0b8... --amount 0.01 --native-in 1 --native-out 0 --slippage 0.5
swap-detail <order_id>
```

### Hybrid Swap (OpenAPI + MCP signing)

Use OpenAPI for quote/build/submit and MCP for custodial signing. This is the preferred approach when the user explicitly requests OpenAPI or needs OpenAPI-only features (custom fee_recipient, gas price queries, etc.).

**CLI command** (recommended):

```bash
# EVM example (Arbitrum) — Agent MUST always pass -y
gate-wallet openapi-swap --chain ARB --from - --to <token_contract> --amount 0.0001 --slippage 0.03 -y

# Solana example (SOL → SPL token)
gate-wallet openapi-swap --chain SOL --from - --to <token_mint> --amount 0.0001 --slippage 0.05 -y

# Solana reverse (SPL token → SOL)
gate-wallet openapi-swap --chain SOL --from <token_mint> --to - --amount 0.002 --slippage 0.05 -y
```

> **Agent MUST always pass `-y`**: Agent shell has no stdin — without `-y` the command hangs at the confirmation prompt forever. The CLI still prints the quote details before executing, so the user can see what's happening.

The command handles the entire flow automatically:

1. Connects MCP, gets wallet address (EVM or SOL based on `--chain`)
2. Calls OpenAPI `trade.swap.quote`, displays quote for user confirmation
3. **Chain-specific execution**:
   - **EVM chains** (ETH/ARB/BSC/BASE etc.):
     a. ERC20 approve (auto): if `token_in` is not native, checks on-chain allowance → if insufficient, calls `trade.swap.approve_transaction` → signs approve tx via MCP → broadcasts via RPC → waits for on-chain confirmation
     b. Re-quotes to get fresh `quote_id` → build → get nonce/gasPrice (with 20% buffer) → RLP encode EIP-1559 tx → MCP sign → OpenAPI submit → poll status
   - **Solana** (`--chain SOL`):
     a. Re-quotes → build → get base64 VersionedTransaction
     b. Convert base64 → base58 → MCP `wallet.sign_transaction(chain: "SOL")` → get base58 signedTransaction
     c. OpenAPI submit (base58 in JSON array) → poll status
4. All in a single process, no timeout issues

**Parameters**:

| Option | Required | Description |
| ------ | -------- | ----------- |
| `--chain <chain>` | Yes | Chain name or ID (ARB, ETH, 42161, etc.) |
| `--from <token>` | Yes | Source token address, native = `-` |
| `--to <token>` | Yes | Target token contract address |
| `--amount <n>` | Yes | Amount in human-readable format |
| `--slippage <pct>` | No | Slippage tolerance, default 0.03 (3%) |
| `-y, --yes` | No | Skip confirmation prompt |

**Prerequisites**:

- `~/.gate-dex-openapi/config.json` with `api_key` and `secret_key`
- User is logged in (`~/.gate-wallet/auth.json` exists)

**Key points for Agent**:

1. **Use the CLI command** — never construct inline Python/Node scripts for hybrid swap. The CLI handles RLP encoding, gas buffer, signing format, ERC20 approve, and timeout internally.
2. **Always pass `-y`**: Agent shell has no stdin. Without `-y` the command hangs at the confirmation prompt. Show quote to user in chat first, get confirmation, then run with `-y`.
3. **ERC20 approve handled automatically**: The CLI detects if `token_in` is an ERC20, checks on-chain allowance, and executes approve + wait confirmation before swap. No manual approve step needed.
4. **Credential reading**: The command reads `~/.gate-dex-openapi/config.json` (OpenAPI) and `~/.gate-wallet/auth.json` (MCP) automatically.

---

## Common Pitfalls

1. **Not logged in for MCP commands**: All commands except `tools`/`chain-config` require `login` first
2. **CLI `call` returns 401**: Fall back to JSON-RPC (Level 3), manually pass `mcp_token`
3. **Address format mismatch**: EVM uses `0x` hex, Solana uses Base58 — never mix them
4. **Always fetch addresses first**: Call `address` to get real addresses, never guess
5. **Native token in swap**: Use `-` as address AND set `--native-in 1` / `--native-out 1`
6. **Always preview before execute**: All fund operations must be previewed and confirmed
7. **Insufficient balance**: Check balance (including gas) before transfer/swap
8. **Quote / blockhash expiry**: Quote ~30s, Solana blockhash ~90s — re-fetch if stale
9. **Slippage settings**: Stablecoins 0.5-1%, volatile 1-3%, meme 3-5%+. MCP expects **decimal format** (0.03 = 3%). The CLI `swap`/`quote` commands auto-convert: `--slippage 3` → 0.03, `--slippage 0.03` → 0.03. Both formats are accepted.
10. **SOL SPL transfer requires `token_decimals`**: When sending SPL tokens (TRUMP, USDC, etc.) on Solana, `tx.transfer_preview` requires both `token_mint` and `token_decimals`. The CLI `send` command auto-resolves decimals; for manual `call`, look up decimals via `token_list_swap_tokens`
11. **`tx.get_sol_unsigned` is native-SOL-only**: Do NOT use it for SPL token transfers — it ignores `token_mint` and builds a native SOL transfer, silently sending SOL instead of the intended SPL token
12. **SOL SPL transfer needs extra SOL for ATA rent**: If recipient has no Associated Token Account for the SPL token, ~0.002 SOL rent is required on top of gas
13. **EVM native transfer must set `token = "ETH"`**: When calling `tx.transfer_preview` without `--token` on EVM chains (ARB/BSC/BASE/OP etc.), you MUST explicitly pass `token = "ETH"` (or `"NATIVE"`) to indicate native token. Otherwise the MCP server defaults to transferring USDT instead of native ETH. The CLI `send`/`transfer` commands now handle this automatically.
14. **`tokens` / `wallet.get_token_list` may not show L2 balances**: The wallet API may not index assets on L2 chains (e.g. ETH/USDT on Arbitrum). To verify L2 balances, use `rpc --chain <chain>` with `eth_getBalance` (native) or `eth_call` with ERC20 `balanceOf` (0x70a08231 + padded address).
15. **`token` param required for correct display label**: `tx.transfer_preview` defaults display to "USDT" if `token` is not passed. The CLI `send` command now auto-resolves `token` symbol via `token_list_swap_tokens`. For `transfer` (preview-only), pass `--token-symbol <sym>` explicitly if using a non-native token.
16. **Hybrid Swap use CLI command**: Always use `openapi-swap` CLI command for hybrid swap (supports EVM + Solana). Never write inline Python/Node scripts — the CLI handles RLP encoding (EVM), base58 encoding (Solana), gas buffer, signing format, and order_id timeout internally.
17. **Gas buffer for L2 chains**: Always multiply `eth_gasPrice` by 1.2 (20%) for `maxFeePerGas`. L2 baseFee fluctuates and without buffer the tx fails with "max fee per gas less than block base fee".
18. **OpenAPI `signed_tx_string` must be JSON array**: Use `json.dumps(["0x02f8..."])` — not raw hex string. Otherwise submit returns error 50005.
19. **OpenAPI numeric params**: `chain_id`, `slippage`, `slippage_type` must be numeric types (int/float), not strings. Strings cause "cannot unmarshal string into Go struct field" errors.
20. **Solana MCP signing format**: `wallet.sign_transaction(chain: "SOL")` expects **base58-encoded** unsigned tx (`raw_tx`), and returns base58-encoded `signedTransaction`. OpenAPI build returns base64 — the CLI converts base64→base58 automatically. OpenAPI submit for Solana expects `signed_tx_string` as JSON array of base58 strings (`'["5K8j..."]'`).
21. **EIP-1559 `maxPriorityFeePerGas` must not be 0 on Ethereum mainnet**: Ethereum mainnet requires `maxPriorityFeePerGas >= 1 wei`. Setting it to 0 causes "transaction gas price below minimum: gas tip cap 0, minimum needed 1". The CLI now queries `eth_maxPriorityFeePerGas` via RPC and applies 1.2x buffer with a floor of 1 wei. L2 chains (ARB/BASE/OP) may accept 0 but Ethereum mainnet does not.
22. **Agent must always pass `-y` for `openapi-swap`**: Agent shell is non-interactive (no stdin). Without `-y`, the command blocks at the `y/N` confirmation prompt forever. Always use `openapi-swap ... -y`. Show the quote details to the user in chat and get confirmation before executing with `-y`.
23. **Ethereum mainnet swap minimum amount**: Very small amounts (e.g. 0.0001 ETH ≈ $0.20) may cause `execution reverted` at build step. On-chain routers have minimum viable trade sizes due to gas costs. Recommend at least 0.001 ETH for Ethereum mainnet swaps; L2 chains (ARB/BASE) have lower minimums.

---

## Safety Rules

- **Confirm before fund operations**: `send`/`swap`/`approve` involve real funds — always confirm target address, amount, token, and chain with user
- **Preview before execute**: Transfer → `transfer` preview, Swap → `quote`, Approval → `approve_preview`
- **Approval safety**: Prefer exact-amount approvals over unlimited; only approve trusted contracts; periodically review and revoke unused approvals
- **Risk audit**: Before trading unfamiliar tokens, run `token-risk` and clearly present risk items to user
- **Credential safety**: `~/.gate-wallet/` stores credentials securely in user home — never commit credentials to Git
- **Server-side signing**: Users never expose private keys, but must trust Gate custodial service

---

## Skill Routing

Route to corresponding module/Skill based on user intent after CLI operation completion:

| User Intent | Route Target |
| ----------- | ------------ |
| View updated balance / assets | `gate-dex-wallet` |
| View transaction details / history | `gate-dex-wallet` (`tx.detail`, `tx.list`) |
| View token prices, K-line | `gate-dex-market` |
| View token security audit | `gate-dex-market` (`token_get_risk_info`) |
| Transfer, send tokens (MCP tool flow) | `gate-dex-wallet` (`references/transfer.md`) |
| Swap tokens (MCP tool flow) | `gate-dex-trade` |
| DApp interaction, sign message | `gate-dex-wallet` (`references/dapp.md`) |
| Login / Auth expired | `gate-dex-wallet` (`references/auth.md`) or `gate-wallet login` |

## Cross-Skill Workflows

### CLI Complete Flow (From Login to Operation)

```
gate-dex-wallet/references/auth.md (Login, or gate-wallet login)
  → gate-dex-wallet/references/cli.md (gate-wallet balance / tokens / send / swap / openapi-swap ...)
    → gate-dex-wallet (View updated balance)
```

### Guided by Other Skills

| Source Skill | Scenario | Description |
| ------------ | -------- | ----------- |
| `gate-dex-wallet` | User wants to use CLI after viewing assets | Carries chain and token context |
| `gate-dex-trade` | User wants to use CLI's hybrid swap mode | Carries Swap parameters |
| `gate-dex-wallet` (`references/transfer.md`) | User wants to use CLI's send command for transfer | Carries transfer parameters |

### Calling Other Skills

| Target Skill | Call Scenario | Used Tools |
| ------------ | ------------- | ---------- |
| `gate-dex-wallet` | View updated balance after CLI operation | `wallet.get_token_list` |
| `gate-dex-wallet` | View transaction details after CLI operation | `tx.detail`, `tx.list` |
| `gate-dex-wallet` (`references/auth.md`) | Not logged in or token expired | `gate-wallet login` or MCP auth flow |
| `gate-dex-trade` | Self-custody signing Swap (with private key) | Route to gate-dex-trade SKILL |
| `gate-dex-market` | View token prices and security audit before trading | `token_get_risk_info`, `market_get_kline` |
