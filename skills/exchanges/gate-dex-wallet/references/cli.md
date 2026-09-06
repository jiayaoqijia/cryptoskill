---
name: gate-dex-cli
version: "2026.4.3-1"
updated: "2026-04-03"
description: "Gate Wallet CLI command-line tool. Dual-channel support: MCP (OAuth custodial signing) and OpenAPI (AK/SK self-custodial signing). Signing commands (send, swap, openapi-swap) require mandatory terminal tx-checkin before execution per tx-checkin.md. Use when the user mentions gate-wallet, CLI, command line, openapi-swap, hybrid swap, or script automation. Covers authentication, asset queries, transfers, swap, market data, and approvals."
---

# Gate DEX CLI

> CLI module — gate-wallet dual-channel command-line tool. Supports MCP custodial signing and OpenAPI hybrid-mode swap. Covers authentication, assets, transfers, swap, market data, and approvals.

## Applicable Scenarios

Use when the user mentions `gate-wallet`, CLI, command line, `openapi-swap`, hybrid swap, script automation, or when another skill routes here for CLI operations:

- Direct CLI usage: "use CLI", "run gate-wallet", "command line", "terminal"
- Specific CLI commands: "gate-wallet balance", "gate-wallet send", "gate-wallet swap"
- Hybrid swap: "openapi-swap", "use openapi", "hybrid mode swap"
- Script/automation context: "automate transfers", "batch script", "cron job for balance check"
- Routed from other modules when CLI is the preferred execution method

## Capability Boundaries

- Supports: All wallet operations via command line (auth, balance, transfer, swap, approve, market data, chain/RPC)
- Dual channels: MCP (OAuth + custodial signing) and OpenAPI (AK/SK + self-custody signing)
- **Signing prerequisite**: All signing CLI commands (`send`, `swap`, `openapi-swap`) require terminal tx-checkin immediately before execution — see [tx-checkin.md](./tx-checkin.md). The CLI does NOT handle tx-checkin internally; the agent must run the prebuilt `tx-checkin` binary separately.
- Does **not** support: Direct DApp contract interactions (-> [dapp.md](./dapp.md)), x402 payment (-> [x402.md](./x402.md))

**Prerequisites**: Node.js >= 18. MCP Server available (see parent SKILL.md).

---

## Installation

### Cursor / VS Code

```bash
# Recommended: installation script (includes OpenAPI configuration guidance)
bash gate-dex-wallet/install_cli.sh

# Alternative: direct npm install
npm install -g gate-wallet-cli
```

### Codex CLI

```bash
# 1. Install the CLI tool globally
npm install -g gate-wallet-cli

# 2. Add OpenAPI credentials (required for hybrid swap)
mkdir -p ~/.gate-dex-openapi
cat > ~/.gate-dex-openapi/config.json << 'EOF'
{ "api_key": "<YOUR_AK>", "secret_key": "<YOUR_SK>" }
EOF

# 3. Login to MCP (required for most commands)
gate-wallet login
```

> Codex runs commands in a sandboxed environment. Ensure `gate-wallet` is on `$PATH` and `~/.gate-wallet/auth.json` is accessible to the sandbox.

**Storage**:
- OAuth token: `~/.gate-wallet/auth.json` (30-day TTL)
- OpenAPI credentials: `~/.gate-dex-openapi/config.json` (for hybrid swap)

---

## Dual-Channel Architecture

| Channel | Auth | Signing | Use Case |
|---------|------|---------|----------|
| **MCP** | OAuth login | Server-side custodial | Full wallet: balance, transfer, swap, approve, market data |
| **OpenAPI** | AK/SK (login-free) | Client-side self-custody | DEX swap trading (see `gate-dex-trade`) |

---

## Channel Routing (Evaluate First)

MCP and OpenAPI overlap on swap functionality. Evaluate which channel to use **before** executing.

### Priority Rules

**Rule 1 — Explicit user request (highest priority)**

| User says | Route to |
|-----------|----------|
| "use openapi" / "AK/SK" / "DEX API" | Hybrid or OpenAPI (check login status — see Rule 1a) |
| "self-signing" / "use private key" | OpenAPI -> `gate-dex-trade` |
| "use MCP" / "use wallet" / "gate-wallet swap" | MCP -> this module |

**Rule 1a — OpenAPI sub-routing**

| Condition | Route | Command |
|-----------|-------|---------|
| Logged in (has MCP token) | Hybrid mode | `gate-wallet openapi-swap ...` |
| Not logged in, has private key | OpenAPI channel | Follow `gate-dex-trade` |
| Not logged in, no private key | Hybrid (prompt login first) | `gate-wallet login` then `openapi-swap` |

> "Use openapi" does NOT mean "use private key." Most users want OpenAPI routing advantages with MCP custodial signing. The `openapi-swap` command is designed for this.

**Rule 2 — MCP-only operations (no overlap, always MCP)**

`balance` / `address` / `tokens` / `send` / `transfer` / `approve` / `gas` / `token-info` / `token-risk` / `token-rank` / `kline` / `liquidity` / `tx-stats` / `swap-tokens` / `bridge-tokens` / `new-tokens` / `rpc` / `chain-config` / `tx-detail` / `tx-history`

**Rule 3 — Swap without channel specified (agent decides)**

| Condition | Preferred | Reason |
|-----------|-----------|--------|
| Logged in | MCP (`gate-wallet swap`) | Simpler one-shot flow |
| Not logged in, has OpenAPI config | OpenAPI | AK/SK already configured |
| Not logged in, no config | MCP (prompt login) | MCP is the default path |
| User mentions private key / self-custody | OpenAPI | Self-signing control |
| Needs OpenAPI features (custom fee_recipient, MEV protection) | Hybrid (`openapi-swap`) | OpenAPI features + MCP signing |

---

## Agent Usage Notes

Agent should use **single-command mode** — each command runs independently.

**CRITICAL**: Agent runs in a non-interactive shell (no stdin). Commands that prompt for confirmation will hang. **Always pass `-y` / `--yes`** for commands that support it (e.g., `openapi-swap -y`). For others, use the preview step, get confirmation in chat, then execute.

### Login Flow

Triggered when any command returns `Not logged in` or `~/.gate-wallet/auth.json` is missing:

1. Run `gate-wallet login` (or `gate-wallet login --google`) in background.
2. Browser auto-opens the authorization page.
3. Poll terminal output (every 10s, max 120s) for:
   - `login successful` -> proceed
   - `Waiting for authorization` -> keep polling
   - `Login failed` / `Login timed out` -> prompt retry
4. Token auto-saved to `~/.gate-wallet/auth.json`.

### MCP Tool Call Fallback Strategy

| Level | Method | When |
|-------|--------|------|
| 1 | CLI shortcut commands | Preferred; auto-handles auth |
| 2 | `gate-wallet call <tool> [json]` | When no shortcut exists |
| 3 | Raw JSON-RPC via curl | When Level 2 returns 401 |

Level 3 requires reading `mcp_token` from `~/.gate-wallet/auth.json` and manually constructing JSON-RPC calls.

---

## Command Reference

### Authentication

| Command | Description |
|---------|-------------|
| `login` | Gate OAuth login (default) |
| `login --google` | Google OAuth login |
| `status` | Check current auth status |
| `logout` | Logout and clear local token |

### Wallet Queries

| Command | Description |
|---------|-------------|
| `balance` | Total asset value (USD) |
| `address` | Wallet addresses per chain |
| `tokens` | Token list with balances |

### Transfers

| Command | Description |
|---------|-------------|
| `send --chain <c> --to <addr> --amount <n> [--token <contract>] [--token-decimals <d>] [--token-symbol <sym>]` | One-shot transfer (preview -> sign -> broadcast) |
| `transfer --chain <c> --to <addr> --amount <n> [--token <contract>]` | Preview only (no execution) |
| `gas [chain]` | Gas fee estimation |
| `tx-detail <hash>` | Transaction details |
| `tx-history [--page <n>] [--limit <n>]` | Transaction history |

> **tx-checkin required**: Before running `send`, the agent MUST complete terminal tx-checkin per [tx-checkin.md](./tx-checkin.md). Run `transfer` (preview-only) first to get the `txBundle` field, write it to a file, then run `tx-checkin -tx-bundle-file <path>`. Only after successful check-in proceed with `send`.

### Token Approval

Via MCP tool `dex_tx_approve_preview`:

| Scenario | amount | Returns |
|----------|--------|---------|
| Exact approve | `"100"` | `approve` |
| Unlimited | `"unlimited"` | `approve_unlimited` |
| Revoke (EVM) | `"0"` | `revoke` |
| Revoke (Solana) | `"0"` + `action: "revoke"` | `revoke` |

### Swap

| Command | Description |
|---------|-------------|
| `quote --from-chain <id> --to-chain <id> --from <token> --to <token> --amount <n>` | Get swap quote (MCP) |
| `swap --from-chain <id> --to-chain <id> --from <token> --to <token> --amount <n>` | One-shot MCP swap |
| `openapi-swap --chain <c> --from <token> --to <token> --amount <n> [-y]` | Hybrid swap (OpenAPI + MCP signing) |
| `swap-detail <order_id>` | Swap order details |
| `swap-history` | Swap/bridge history |

**Agent MUST always pass `-y` for `openapi-swap`** — without it the command hangs at the confirmation prompt.

> **tx-checkin required**: Before running `swap` or `openapi-swap`, the agent MUST complete terminal tx-checkin per [tx-checkin.md](./tx-checkin.md). Use `quote` first for user confirmation, then run `tx-checkin -message "<swap intent>" -wallet <addr> -chain <chain> -chain-category <cat>`. Only after successful check-in proceed with `swap` or `openapi-swap -y`.

### Market Data

| Command | Description |
|---------|-------------|
| `kline --chain <c> --address <addr>` | K-line / candlestick data |
| `liquidity --chain <c> --address <addr>` | Liquidity pool events |
| `tx-stats --chain <c> --address <addr>` | Trading volume stats |
| `swap-tokens [--chain <c>] [--search <kw>]` | Swappable token list |
| `bridge-tokens [--src-chain <c>] [--dest-chain <c>]` | Cross-chain bridge tokens |
| `token-info --chain <c> --address <addr>` | Token details (price/mcap) |
| `token-risk --chain <c> --address <addr>` | Security audit |
| `token-rank [--chain <c>] [--limit <n>]` | Price change rankings |
| `new-tokens [--chain <c>] [--start <RFC3339>]` | Filter by creation time |

### Chain / Debug

| Command | Description |
|---------|-------------|
| `chain-config [chain]` | Chain configuration |
| `rpc --chain <c> --method <m> [--params '<json>']` | JSON-RPC call |
| `tools` | List all MCP tools |
| `call <tool> [json]` | Call any MCP tool directly |

---

## Hybrid Swap (openapi-swap)

The `openapi-swap` command combines OpenAPI quote/build/submit with MCP custodial signing.

```bash
# EVM (Arbitrum)
gate-wallet openapi-swap --chain ARB --from - --to <token> --amount 0.01 --slippage 0.03 -y

# Solana
gate-wallet openapi-swap --chain SOL --from - --to <token> --amount 0.01 --slippage 0.05 -y
```

| Option | Required | Description |
|--------|----------|-------------|
| `--chain` | Yes | Chain name or ID |
| `--from` | Yes | Source token, native = `-` |
| `--to` | Yes | Target token address |
| `--amount` | Yes | Human-readable amount |
| `--slippage` | No | Default 0.03 (3%) |
| `-y, --yes` | No | Skip confirmation (**REQUIRED** for agent) |

The command handles the entire flow automatically:
1. Connect MCP, get wallet address
2. Call OpenAPI quote, display for user
3. Chain-specific execution:
   - **EVM**: Auto-approve if needed -> re-quote -> build -> RLP encode EIP-1559 -> MCP sign -> submit
   - **Solana**: Re-quote -> build -> base64->base58 conversion -> MCP sign -> submit
4. Poll order status

**Prerequisites**: `~/.gate-dex-openapi/config.json` with `api_key`/`secret_key` + logged in (`~/.gate-wallet/auth.json`).

**Key rules for Agent**:
1. Use the CLI command — never construct inline scripts for hybrid swap.
2. Always pass `-y` to avoid hanging.
3. ERC20 approve is handled automatically by the CLI.
4. Show quote to user in chat first, get confirmation, then run with `-y`.
5. **tx-checkin before execution**: Run terminal tx-checkin per [tx-checkin.md](./tx-checkin.md) immediately before running `openapi-swap`. The CLI does not handle check-in internally.

---

## On-Chain Operation Flow

All fund-moving operations follow: **preview -> confirm -> tx-checkin -> execute**.

1. **Pre-check**: `address` for correct chain address -> `balance`/`tokens` for sufficient funds
2. **Preview**: `transfer` (transfer) / `dex_tx_approve_preview` (approval) / `quote` (swap)
3. **User confirmation**: Display details, wait for explicit approval
4. **Terminal tx-checkin** (MANDATORY): Run the prebuilt `tx-checkin` binary per [tx-checkin.md](./tx-checkin.md) immediately before signing. CLI `send`/`swap`/`openapi-swap` do NOT handle tx-checkin internally — the agent must run it separately. For transfers: use preview `txBundle` -> `tx-checkin -tx-bundle-file`. For swaps: use `tx-checkin -message` with swap intent.
5. **Sign + broadcast**: `send`/`swap`/`openapi-swap` one-shot commands (only after successful check-in)
6. **Verify**: `tx-detail <hash>` / `swap-detail <order_id>`

**NEVER execute signing without user confirmation and successful tx-checkin.**

---

## tx-checkin Binary for CLI Operations

When using CLI commands that involve signing (`send`, `swap`, `openapi-swap`), the agent must run the prebuilt `tx-checkin` binary before executing the command. The binary is located at `{skill_root}/tools/tx-checkin/bin/` — see [tx-checkin.md](./tx-checkin.md) for OS-specific paths and usage.

**CLI flow for `send` (transfer)**:
1. `gate-wallet transfer --chain <c> --to <addr> --amount <n>` (preview only, returns `txBundle`)
2. Write `txBundle` string to a temp file
3. `tx-checkin -tx-bundle-file <path> -wallet <addr> -chain <chain> -chain-category <cat>`
4. On success -> `gate-wallet send --chain <c> --to <addr> --amount <n>`

**CLI flow for `swap` / `openapi-swap`**:
1. `gate-wallet quote --from-chain <id> --to-chain <id> --from <token> --to <token> --amount <n>` (get quote)
2. Display quote to user, wait for confirmation
3. `tx-checkin -message "<swap intent description>" -wallet <addr> -chain <chain> -chain-category <cat>`
4. On success -> `gate-wallet swap ...` or `gate-wallet openapi-swap ... -y`

> Resolve the binary from `skill_root`: Linux → `tx-checkin-linux-amd64`, macOS → `tx-checkin-darwin-universal`, Windows → `tx-checkin-windows-amd64.exe`. Users need not set `TX_CHECKIN` (optional override only).

---

## Domain Knowledge

### Amount Format

All amounts use **human-readable values**, not chain-native smallest units.

| Correct | Wrong |
|---------|-------|
| `--amount 0.1` (0.1 ETH) | `--amount 100000000000000000` (wei) |

### Native Token Handling

In swap operations, native tokens (ETH/SOL/BNB) use `-` as address and require `--native-in 1` or `--native-out 1`.

### Chain Identifiers

| Chain | Chain ID | CLI Param |
|-------|----------|-----------|
| Ethereum | 1 | ETH |
| BSC | 56 | BSC |
| Polygon | 137 | POLYGON |
| Arbitrum | 42161 | ARB |
| Base | 8453 | BASE |
| Optimism | 10 | OP |
| Avalanche | 43114 | AVAX |
| Solana | 501 | SOL |

Chain names are case-insensitive.

### Common Stablecoin Addresses

| Chain | USDT | USDC |
|-------|------|------|
| Ethereum | `0xdAC17F958D2ee523a2206206994597C13D831ec7` | `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48` |
| BSC | `0x55d398326f99059fF775485246999027B3197955` | `0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d` |
| Arbitrum | `0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9` | `0xaf88d065e77c8cC2239327C5EDb3A432268e5831` |
| Solana | `Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB` | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` |

Use `token-info` or `swap-tokens --search <symbol>` to look up other token addresses.

---

## Common Pitfalls

1. **Not logged in**: All commands except `tools`/`chain-config` require `login` first.
2. **CLI `call` returns 401**: Fall back to JSON-RPC (Level 3) with manual `mcp_token`.
3. **Address format mismatch**: EVM uses `0x` hex, Solana uses Base58 — never mix them.
4. **Always fetch addresses first**: Call `address`; never guess.
5. **Native token in swap**: Use `-` as address AND set `--native-in 1` / `--native-out 1`.
6. **Always preview before execute**: All fund operations must be previewed and confirmed.
7. **Insufficient balance**: Check balance (including gas) before transfer/swap.
8. **Quote / blockhash expiry**: Quote ~30s, Solana blockhash ~90s — re-fetch if stale.
9. **Slippage**: Stablecoins 0.5-1%, volatile 1-3%, meme 3-5%+. Both `--slippage 3` and `--slippage 0.03` are accepted (auto-converted to decimal 0.03).
10. **SOL SPL transfer**: Requires `token_mint` and `token_decimals`. CLI `send` auto-resolves; for manual `call`, look up via `dex_token_list_swap_tokens`.
11. **`dex_tx_get_sol_unsigned` is native-SOL-only**: Do NOT use for SPL tokens.
12. **SOL ATA rent**: If recipient has no Associated Token Account, ~0.002 SOL rent is required.
13. **EVM native transfer**: Must set `token = "ETH"` (or `"NATIVE"`) in `dex_tx_transfer_preview`; otherwise defaults to USDT.
14. **L2 balance indexing**: `tokens` / `dex_wallet_get_token_list` may not show L2 balances. Use `rpc` with `eth_getBalance` or `eth_call` (ERC20 `balanceOf`) to verify.
15. **Hybrid swap: use CLI only**: Always use `openapi-swap` CLI command. Never write inline scripts.
16. **Gas buffer for L2**: Multiply `eth_gasPrice` by 1.2x. L2 baseFee fluctuates.
17. **OpenAPI `signed_tx_string`**: Must be JSON array format: `json.dumps(["0x02f8..."])`.
18. **OpenAPI numeric params**: `chain_id`, `slippage`, `slippage_type` must be numeric, not strings.
19. **Solana MCP signing**: Expects base58-encoded `raw_tx`, returns base58 `signedTransaction`. CLI handles base64->base58 conversion.
20. **EIP-1559 on Ethereum mainnet**: `maxPriorityFeePerGas` must be >= 1 wei.
21. **Agent must always pass `-y`**: Non-interactive shell; without `-y`, `openapi-swap` hangs forever.
22. **Ethereum mainnet swap minimum**: Very small amounts may cause `execution reverted`. Recommend >= 0.001 ETH.
23. **`token` param required for display**: In `dex_tx_transfer_preview`, pass `token` to get the correct display label; omitting it defaults to USDT.
24. **tx-checkin before CLI signing**: `send`, `swap`, and `openapi-swap` do NOT run tx-checkin internally. The agent must run the `tx-checkin` binary from `tools/tx-checkin/bin/` before these commands, per [tx-checkin.md](./tx-checkin.md).

---

## Post-Operation Suggestions

After a successful CLI operation, **proactively suggest relevant next actions** based on what was just performed:

**After balance / token query:**
```
You can also:
- Transfer tokens: gate-wallet send --chain ETH --to 0x... --amount 0.1
- Swap tokens: gate-wallet swap ...
- View token security: gate-wallet token-risk --chain eth --address 0x...
```

**After transfer / swap:**
```
You can:
- Check updated balance: gate-wallet balance
- View transaction details: gate-wallet tx-detail <hash>
- Make another transfer or swap
```

**After market data query:**
```
You can also:
- Check your holdings of this token: gate-wallet tokens
- Swap this token: gate-wallet swap ...
- View security audit: gate-wallet token-risk ...
```

### Follow-up Routing Table

| User Intent | Route Target | Display Template |
|-------------|--------------|------------------|
| View balance / assets | [asset-query.md](./asset-query.md) | `gate-wallet balance` or `gate-wallet tokens` |
| View transaction details | [asset-query.md](./asset-query.md) (`dex_tx_detail`, `dex_tx_list`) | `gate-wallet tx-detail <hash>` |
| View token prices, K-line | `gate-dex-market` | `gate-wallet kline --chain <c> --address <addr>` |
| Token security audit | `gate-dex-market` | `gate-wallet token-risk --chain <c> --address <addr>` |
| Transfer tokens (MCP flow) | [transfer.md](./transfer.md) | `gate-wallet send --chain <c> --to <addr> --amount <n>` |
| Swap tokens (MCP flow) | `gate-dex-trade` | `gate-wallet swap --from-chain <id> --from <token> --to <token> --amount <n>` |
| Pay for a 402 resource | [x402.md](./x402.md) | Route to x402 module; CLI does not support x402 directly |
| DApp interaction | [dapp.md](./dapp.md) | Route to DApp module; CLI does not support DApp directly |
| Login / auth expired | [auth.md](./auth.md) or `gate-wallet login` | `gate-wallet login` or `gate-wallet login --google` |

---

## Security Rules

1. **Confirm before fund operations**: `send`/`swap`/`approve` involve real funds. Always confirm target, amount, token, and chain with user.
2. **Preview before execute**: Transfer -> `transfer` preview, Swap -> `quote`, Approval -> `dex_tx_approve_preview`.
3. **Terminal tx-checkin before signing**: All signing operations (`send`, `swap`, `openapi-swap`) require successful terminal tx-checkin immediately before execution per [tx-checkin.md](./tx-checkin.md). Do not skip because a previous operation succeeded without it.
4. **Approval safety**: Prefer exact-amount over unlimited; only approve trusted contracts.
5. **Risk audit**: Run `token-risk` before trading unfamiliar tokens.
6. **Credential safety**: `~/.gate-wallet/` stores credentials in user home. Never commit to Git.
7. **Server-side signing**: Users never expose private keys, but must trust Gate custodial service.
