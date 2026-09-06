---
name: gate-dex-wallet
version: "2026.4.3-2"
updated: "2026-04-03"
description: "Gate DEX wallet account management. Handles authentication (Google OAuth and Gate OAuth), token balance queries, wallet address retrieval, transaction and swap history, token transfers, on-chain withdraw to Gate Exchange (deposit address, UID binding, min-deposit), x402 payment (HTTP 402 Payment Required with EVM exact/upto and Solana exact/upto schemes; terminal tx-checkin before dex_tx_x402_fetch per references/x402.md), DApp wallet-connect and contract interactions, and CLI tooling. Signing MCP calls require mandatory terminal tx-checkin (prebuilt **`tools/tx-checkin/bin/`** — users do not compile) per references/tx-checkin.md. Use when the user wants to manage their on-chain wallet identity or assets — not for market data lookups or token swap execution."
---

# Gate DEX Wallet

> **Pure Routing Layer** — This SKILL.md is a lightweight router. All sub-module details live in `references/`.

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)

## Signing gate — terminal tx-checkin (mandatory)

Before **any** MCP call to `dex_wallet_sign_transaction`, `dex_wallet_sign_message`, or **`dex_tx_x402_fetch`**:

1. User must pass the existing confirmation gates (preview / message text / payment intent) for that operation.
2. Agent **MUST** run the terminal **`tx-checkin`** flow in [references/tx-checkin.md](./references/tx-checkin.md) and treat success as a **hard prerequisite**. Do not skip because a prior operation did not require it or no error was returned. Use the **prebuilt** check-in binaries under **`tools/tx-checkin/bin/`** — **end users do not compile** (`go build` / `go run` not required). Resolve the CLI from this skill’s **`skill_root`**: **Linux → `tx-checkin-linux-amd64`**, **macOS → `tx-checkin-darwin-universal`**, **Windows → `tx-checkin-windows-amd64.exe`** — **users need not set `TX_CHECKIN`** (optional override only); see [references/tx-checkin.md](./references/tx-checkin.md).
3. After **`dex_tx_transfer_preview`**, check-in **must** use the preview field **`txBundle`** only: write that string to a file and run **`tx-checkin -tx-bundle-file`** — **do not** assemble txbundle JSON from `unsigned_tx_hex` or other fields (see [references/tx-checkin.md](./references/tx-checkin.md)).
4. **x402 (`dex_tx_x402_fetch`)**: **Always** complete terminal check-in **before** the first `dex_tx_x402_fetch` call in that payment flow. **Do not** call `dex_tx_x402_fetch` first to probe 402 or “see if GV needs check-in.” After successful check-in, pass **`checkin_token`** from stdout JSON into `dex_tx_x402_fetch` when the tool exposes that parameter; use **`-intent` / `-message`** (or documented body) for check-in per [references/x402.md](./references/x402.md) and [references/tx-checkin.md](./references/tx-checkin.md).
5. Other single-step MCP tools that sign internally: same terminal check-in **immediately before** the tool when the gateway requires it; follow backend docs for `checkin_token` / intent payload.

## Applicable Scenarios

Use this skill when the user wants to **manage their on-chain wallet account, identity, or assets**:

- Authenticate or manage sessions (login via Google or Gate OAuth, logout)
- Query token balances, total portfolio value, or wallet addresses
- View transaction history or past swap records
- Transfer or send tokens to an address (single or batch); **mandatory terminal tx-checkin** before any signing ([references/tx-checkin.md](./references/tx-checkin.md))
- Withdraw or cash out **on-chain** to their Gate Exchange account (deposit address resolved for their UID; not CEX-internal balance moves from this skill)
- Pay for HTTP 402 resources via x402 protocol (EVM exact/upto, Solana exact/upto); **terminal tx-checkin before** `dex_tx_x402_fetch` ([references/x402.md](./references/x402.md), [references/tx-checkin.md](./references/tx-checkin.md))
- Interact with DApps (connect wallet, sign messages, approve tokens, call contracts)
- Use the gate-wallet CLI tool for any of the above
- Detect or configure MCP Server connectivity

---

## Capability Boundaries

| Supported | Not Supported (route elsewhere) |
|-----------|---------------------------------|
| Authentication & session management | Token price / K-line queries -> `gate-dex-market` |
| Balance & address queries | Token swap execution -> `gate-dex-trade` |
| Transaction & swap history | Token security audits -> `gate-dex-market` |
| Token transfers (EVM + Solana); on-chain withdraw to Gate Exchange (deposit address flow) | |
| x402 payment (EVM exact/upto + Solana exact/upto) | |
| DApp interactions & approvals | |
| CLI dual-channel operations | |

---

## Module Routing

Route to the corresponding sub-module based on user intent:

| User Intent | Target |
|-------------|--------|
| Login, logout, sign in, sign out, token expired, session expired, OAuth, Google login, Gate login, authenticate, re-login, switch account, "I can't access my wallet", "not logged in" | [references/auth.md](./references/auth.md) |
| Check balance, total assets, portfolio value, wallet address, my address, how much do I have, show my tokens, tx history, transaction history, swap history, past transactions, "what do I own", "how many ETH", "list my coins", "show holdings" | [references/asset-query.md](./references/asset-query.md) |
| Withdraw to Gate Exchange, cash out to my Gate account, send funds to the exchange deposit address, move coins from wallet to Gate (on-chain deposit), bind or rebind Gate UID for withdraw | [references/withdraw.md](./references/withdraw.md) |
| Transfer, send tokens, send to address, batch transfer, "send 1 ETH to 0x...", "transfer USDT", "move tokens", "pay someone", "send crypto to a friend" (arbitrary or known on-chain address — not exchange deposit resolution) | [references/transfer.md](./references/transfer.md) + [references/tx-checkin.md](./references/tx-checkin.md) before sign |
| Any signing: before `dex_wallet_sign_transaction` / `dex_wallet_sign_message`; checkin_token; "run check-in"; terminal tx-checkin | [references/tx-checkin.md](./references/tx-checkin.md) (read **before** signing) |
| 402 payment, x402 pay, payment required, pay for API, pay for URL, "fetch and pay", "call this URL and pay", "paid endpoint", "pay for access", "HTTP 402", Permit2 payment, upto payment | [references/tx-checkin.md](./references/tx-checkin.md) **then** [references/x402.md](./references/x402.md) (check-in before `dex_tx_x402_fetch`) |
| DApp connect, connect wallet, sign message, approve, revoke approval, contract call, EIP-712, Permit, personal_sign, "interact with Uniswap", "add liquidity", "stake on Lido", "mint NFT", "sign for DApp login", authorize contract | [references/dapp.md](./references/dapp.md) + [references/tx-checkin.md](./references/tx-checkin.md) before every sign |
| gate-wallet CLI, command line, terminal, openapi-swap, hybrid swap, "use CLI", "run command", "gate-wallet balance", script automation, npm gate-wallet | [references/cli.md](./references/cli.md) |

---

## MCP Server Connection Detection

Before the first MCP tool call in a session, perform one connection probe:

1. **Discover**: Scan configured MCP servers for tools `dex_wallet_get_token_list`, `dex_tx_quote`, and `dex_tx_swap`.
2. **Identify**: Accept flexible server names (gate-wallet, gate-dex, dex, wallet, user-gate-wallet, or any custom name).
3. **Verify**: `CallMcpTool(server="<id>", toolName="dex_chain_config", arguments={chain: "eth"})`.

| Result | Action |
|--------|--------|
| Success | Record server identifier; use for all subsequent calls this session |
| Failure | Display setup guide below (at most once per session); re-detect next session |

### OpenClaw Platform Detection

When the OpenClaw/mcporter platform is detected, route MCP calls through `mcporter`:

```text
CallMcpTool(server="mcporter", toolName="call_tool", arguments={
  server: "<gate-dex-server>",
  tool: "<tool_name>",
  arguments: { ...params }
})
```

### Setup Guide (shown once on detection failure)

```
Gate DEX MCP Server:
  URL:  https://api.gatemcp.ai/mcp/dex
  Type: HTTP

  Cursor:      Settings -> MCP -> Add server, or edit ~/.cursor/mcp.json
  Claude Code:  claude mcp add --transport http gate-dex --scope project https://api.gatemcp.ai/mcp/dex
  Codex CLI:    codex mcp add gate-dex --transport http --url https://api.gatemcp.ai/mcp/dex
```

### Runtime Error Handling

| Error Type | Keywords | Action |
|------------|----------|--------|
| MCP Server not configured | `server not found`, `unknown server` | Show setup guide |
| Remote service unreachable | `connection refused`, `timeout`, `DNS error` | Prompt to check server status and network |
| Authentication failure | `400`, `401`, `unauthorized` | Follow §3 of [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md) |

---

## Follow-up Routing

After completing an operation, **proactively suggest 2-4 relevant next actions** to the user (see each module's "Post-XXX Suggestions" section for templates). Then route based on the user's response:

| User Intent After Operation | Target |
|-----------------------------|--------|
| View token prices, K-line charts, market cap, trading volume | `gate-dex-market` |
| Run a token security audit, check if token is safe | `gate-dex-market` |
| Transfer or send tokens to an arbitrary on-chain address | [references/transfer.md](./references/transfer.md) |
| Withdraw or cash out on-chain to Gate Exchange | [references/withdraw.md](./references/withdraw.md) |
| Swap, exchange, buy, sell, convert tokens on DEX | `gate-dex-trade` |
| Pay for a 402 resource, x402 payment | [references/tx-checkin.md](./references/tx-checkin.md) then [references/x402.md](./references/x402.md) |
| Interact with a DApp, connect wallet, sign, approve | [references/dapp.md](./references/dapp.md) |
| Mandatory tx-checkin in terminal before any signing, checkin_token | [references/tx-checkin.md](./references/tx-checkin.md) |
| Login, re-login, fix expired auth, switch account | [references/auth.md](./references/auth.md) |
| Use CLI commands, gate-wallet terminal operations | [references/cli.md](./references/cli.md) |
| Check balance, view assets, transaction history | [references/asset-query.md](./references/asset-query.md) |

---

## NOT This Skill (Common Misroutes)

These intents should NOT trigger this skill:

| User Intent | Correct Skill |
|-------------|---------------|
| "What is the price of ETH?" / "Show BTC chart" / "Token rankings" | `gate-dex-market` |
| "Swap ETH for USDT" / "Buy SOL" / "Exchange tokens" / "DEX trade" | `gate-dex-trade` |
| "Is this token safe?" / "Audit contract 0x..." / "Honeypot check" | `gate-dex-market` |
| "Show top gainers" / "New token listings" / "Market overview" | `gate-dex-market` |

---

## Supported Chains

EVM: `eth`, `bsc`, `polygon`, `arbitrum`, `optimism`, `avax`, `base` | Non-EVM: `sol`

---

## Security Rules

1. **Authentication first**: Verify `mcp_token` validity before all operations; on failure follow §3 of [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md).
2. **Token confidentiality**: Never display `mcp_token` in plaintext; use placeholders like `<mcp_token>`.
3. **MCP Server errors**: Display all MCP Server error messages to users transparently — never hide or modify them.
