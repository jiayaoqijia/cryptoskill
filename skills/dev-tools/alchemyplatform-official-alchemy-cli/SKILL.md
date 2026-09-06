---
name: alchemy-cli
description: Use the Alchemy CLI (`@alchemy/cli`) for live blockchain data, transaction lookups, NFT/token/portfolio queries, simulation, tracing/debugging, contract reads/writes, wallet-signed sends, swaps and cross-chain bridges, Solana RPC/DAS plus wallet sends, webhook management, and Alchemy app administration. Preferred runtime path for live agent work (querying, admin, local automation) when the CLI is installed locally — or when both CLI and MCP are available. If neither is installed, install the CLI with `npm i -g @alchemy/cli`. Use for live agent work in this session, not for building application code that ships to production. For application code, use the `alchemy-api` skill (with API key) or `agentic-gateway` skill (without).
license: MIT
compatibility: Requires `@alchemy/cli` (`npm i -g @alchemy/cli`) and shell access. Works across Claude Code, Cursor, Codex, and any agent with shell access.
metadata:
  author: alchemyplatform
  version: "2.1"
---
# Alchemy CLI

Use the [Alchemy CLI](https://www.npmjs.com/package/@alchemy/cli) (`@alchemy/cli`) for live blockchain queries, admin work, transaction signing, and local automation from the terminal. The CLI groups commands by chain (`evm`, `solana`, `xchain`) and by product area (`wallet`, `app`, `webhook`, `auth`, `config`), each with structured JSON output.

## When to use this skill

Use `alchemy-cli` when **all** of the following are true:

- The user wants **live agent work** — live querying, analysis, admin work, or local automation that the agent runs now in this session
- `@alchemy/cli` is installed locally, **or** both the CLI and an MCP server are available, **or** neither is available (in which case install the CLI — see [Install](#install))

The CLI is the **preferred local fallback runtime path** for live agent work. When in doubt about CLI vs MCP, prefer the CLI.

## When to use a different skill

| Situation | Use this skill instead |
| --- | --- |
| MCP is already wired into your client and the CLI is **not** installed locally | `alchemy-mcp` |
| Building application code that runs outside this agent session, with an Alchemy API key | `alchemy-api` |
| Building application code without an API key, or as an autonomous agent that needs to pay for itself, or you explicitly want x402/MPP | `agentic-gateway` |

Do **not** use this skill to write production application code — CLI commands are for live agent work, not for embedding into shipped software.

## Install

```bash
npm i -g @alchemy/cli
```

If the CLI is not installed and the user wants live agent work, install it. Do not fall back to raw curl/HTTP calls — those are the API-key path covered by `alchemy-api`.

## Bootstrap

Run this at the start of any session to get the full command contract (every command, flag, auth method, error code, and example):

```bash
alchemy --json --no-interactive agent-prompt
```

For wallet-scoped agent work, use the narrower contract that lists only wallet, EVM, Solana, and cross-chain commands plus the session-signer capability set:

```bash
alchemy --json --no-interactive agent-prompt --scope wallet
```

When the CLI is not installed yet but the agent needs the same contract, the unauthenticated `npx` variant works:

```bash
npx -y @alchemy/cli@latest --json --no-interactive agent-prompt --scope wallet
```

## Execution rules

- ALWAYS pass `--json --no-interactive` on every command
- Parse stdout as JSON on exit code 0
- Parse stderr as JSON on nonzero exit code
- NEVER run bare `alchemy` without `--json --no-interactive`
- NEVER use curl or raw HTTP when an `alchemy` CLI command exists for the task — that's the `alchemy-api` (API-key) path, not this skill
- NEVER use the CLI to generate production application code; hand off to `alchemy-api` or `agentic-gateway` for shipped code
- For onchain actions (`evm send`, `evm contract call`, `evm approve`, `evm swap`, `xchain bridge`, `solana send`), run `alchemy --json --no-interactive wallet status --verify` first to confirm the session is still valid, then prefer `--dry-run` before broadcast. Treat sponsorship policies (`--gas-policy-id`, `--fee-policy-id`) as fee controls, not wallet spend limits.

## Preflight

Before the first command, run **both** of these checks:

```bash
alchemy --json --no-interactive doctor
alchemy --json --no-interactive evm gas
```

`doctor` (alias: `alchemy config status`) reports what's configured plus a `nextCommands` list of remediation steps. **Do not rely on its top-level OK alone** — there is a known false positive where it reports the session is set up but RPC commands still fail with `AUTH_REQUIRED` because no API key has been derived from the auth token.

`evm gas` is a lightweight RPC smoke test that catches this. If it returns `{"gasPrice": "0x...", ...}`, RPC is wired up correctly. If it returns `{"error": {"code": "AUTH_REQUIRED", ...}}`, run `alchemy auth login` (which fetches and saves the API key) or `alchemy config set api-key <key>`, then re-run `evm gas` to confirm.

If `doctor` reports missing config, follow its `nextCommands` first, then run `evm gas` to verify.

## Auth setup

The fastest way to authenticate is via browser login:

```bash
alchemy auth login
```

For headless environments (SSH, GitHub Codespaces, CI, sandboxes) where the browser can't reach the CLI's localhost callback, force the OAuth 2.0 Device Authorization Grant flow:

```bash
alchemy auth login --device-code
```

Plain `alchemy auth` auto-detects non-interactive sessions and switches to device-code mode automatically. Requires `@alchemy/cli` 0.18.0 or later.

This opens a browser, completes the OAuth flow, and configures both the API key (for RPC/Data) and the Admin API access internally. There is no separate access key step anymore — admin commands (`alchemy app ...`) work straight after `alchemy auth login`.

To check auth status: `alchemy auth status`
To log out: `alchemy auth logout`

### Alternative auth methods

| Method | Config command | Env var | Used by |
|--------|---------------|---------|---------|
| Browser login | `alchemy auth login` (add `--device-code` for headless) | -- | All commands (covers both RPC/Data and Admin) |
| API key | `alchemy config set api-key <key>` | `ALCHEMY_API_KEY` | RPC/Data commands (`evm rpc`, `evm data`, `evm tx`, `solana rpc`, etc.) |
| Webhook key | `alchemy config set webhook-api-key <key>` | `ALCHEMY_WEBHOOK_API_KEY` | `webhook` |
| Agent wallet session | `alchemy wallet connect --mode session --instance-name <label>` (approve in dashboard) | -- | `evm send`, `evm contract call`, `evm approve`, `evm swap`, `xchain bridge`, `evm status`, `solana send`, `solana status`, `solana delegate` |
| Local wallet | `alchemy wallet connect --mode local` (`--import <path>` for EVM key) | -- | Same wallet-signed commands as session, with `--signer local` override |
| x402 gateway auth (Alchemy API path) | `alchemy wallet connect --mode local --chain evm` then `alchemy config set x402 true` | `ALCHEMY_WALLET_KEY` | RPC and Data commands when `--x402` is active. This is Alchemy API auth via wallet, distinct from `alchemy x402 request` (see below). |
| x402 payments (third-party APIs) | `alchemy wallet connect --mode local` — a signer configured for x402 payments | -- | `alchemy x402 request <url>`, `alchemy x402 balance` (pays third-party APIs in USDC per RFC 402) |

`alchemy evm network list` / `alchemy solana network list` and `alchemy version` / `update-check` need no auth.

### Selecting a default app

Many `app` subcommands operate on a "default app." If you see `APP_REQUIRED` in an error response, select one:

```bash
alchemy --json --no-interactive app select <id>
# or equivalently
alchemy --json --no-interactive config set app <id>
```

Get an Alchemy account at [dashboard.alchemy.com](https://dashboard.alchemy.com/).

## Task-to-command map

### EVM — onchain reads

| Task | Command |
|------|---------|
| Native balance (ETH, MATIC, ...) | `alchemy evm data balance <address>` |
| Transaction details | `alchemy evm tx <hash>` |
| Transaction receipt | `alchemy evm receipt <hash>` |
| Block details | `alchemy evm block <number\|latest>` |
| Gas prices | `alchemy evm gas` |
| Event logs | `alchemy evm logs --address <addr> --from-block <n> --to-block <n>` |
| Raw JSON-RPC | `alchemy evm rpc <method> [params...]` |
| Trace methods | `alchemy evm trace <method> [params...]` |
| Debug methods | `alchemy evm debug <method> [params...]` |
| Contract view/pure call | `alchemy evm contract read <address> <function> [--args ...] [--abi-file <path>]` |

### EVM — Data API

| Task | Command |
|------|---------|
| ERC-20 balances | `alchemy evm data tokens balances <address>` |
| ERC-20 balances (formatted) | `alchemy evm data tokens balances <address> --metadata` |
| Token metadata | `alchemy evm data tokens metadata <contract>` |
| Token allowance | `alchemy evm data tokens allowance --owner <addr> --spender <addr> --contract <addr>` |
| List owned NFTs | `alchemy evm data nfts <address> [--limit <n>] [--page-key <key>]` |
| NFT metadata | `alchemy evm data nfts metadata --contract <addr> --token-id <id>` |
| NFT contract metadata | `alchemy evm data nfts contract <address>` |
| Asset transfer history | `alchemy evm data history <address> [--from-block <n>] [--to-block <n>] [--max-count <n>] [--page-key <key>]` |
| Spot prices by symbol | `alchemy evm data price symbol ETH,USDC` |
| Spot prices by address | `alchemy evm data price address --addresses '<json>'` |
| Historical prices | `alchemy evm data price historical --body '<json>'` |
| Cross-network token portfolio | `alchemy evm data portfolio tokens --body '<json>'` |
| Token balances by address/network pairs | `alchemy evm data portfolio token-balances --body '<json>'` |
| Cross-network NFT portfolio | `alchemy evm data portfolio nfts --body '<json>'` |
| NFT contracts by address/network pairs | `alchemy evm data portfolio nft-contracts --body '<json>'` |

### EVM — Simulation

| Task | Command |
|------|---------|
| Simulate single tx (asset deltas) | `alchemy evm simulate asset-changes --tx '<json>' [--block-tag <tag>]` |
| Simulate single tx (execution trace) | `alchemy evm simulate execution --tx '<json>' [--block-tag <tag>]` |
| Simulate bundle (asset deltas) | `alchemy evm simulate asset-changes-bundle --txs '<json-array>' [--block-tag <tag>]` |
| Simulate bundle (execution trace) | `alchemy evm simulate execution-bundle --txs '<json-array>' [--block-tag <tag>]` |

### EVM — wallet-signed transactions

Wallet-signed EVM actions return a smart wallet **call ID**. Use `alchemy evm status <call-id-or-tx-hash>` to check either value. Use `--gas-sponsored` and `--gas-policy-id <id>` on supported actions to request gas sponsorship; set defaults with `alchemy config set evm-gas-sponsored true` and `alchemy config set evm-gas-policy-id <id>`.

| Task | Command |
|------|---------|
| Send native token | `alchemy evm send <to> <amount> [-n <network>]` |
| Send ERC-20 | `alchemy evm send <to> <amount> --token <token-address>` |
| Execute a contract function | `alchemy evm contract call <address> <function> [--args ...] [--abi-file <path>\|--abi '<json>'] [--value <wei>]` |
| Approve / revoke / reset ERC-20 allowance | `alchemy evm approve <spender-address> --token-address <addr> [--amount <n>\|--unlimited\|--revoke]` |
| Quote same-chain swap | `alchemy evm swap quote --from <token> --to <token> --amount <n>` |
| Execute same-chain swap | `alchemy evm swap execute --from <token> --to <token> --amount <n>` |
| Check call / tx status | `alchemy evm status <call-id-or-tx-hash>` |

Native token address for swaps: `0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE`.

Most wallet-signed EVM commands accept `--signer session|local` to override the active signer for that invocation. When both signers are configured and no active one is chosen, the CLI defaults to `session` and prints a warning.

### Solana

Solana transaction commands use a local Solana wallet (`alchemy wallet connect --mode local --chain solana`). Use `--fee-sponsored` and `--fee-policy-id <id>` on supported actions to request fee sponsorship; persist defaults with `alchemy config set solana-fee-sponsored true` / `alchemy config set solana-fee-policy-id <id>`.

| Task | Command |
|------|---------|
| Solana JSON-RPC | `alchemy solana rpc <method> [params...]` |
| Solana DAS (NFTs/assets) | `alchemy solana das <method> '<json>'` |
| Send native SOL | `alchemy solana send <to> <amount> [-n solana-mainnet]` |
| Approve SPL token delegate | `alchemy solana delegate approve --token-account <addr> --mint <addr> --delegate <addr> --amount <n> --decimals <n>` |
| Revoke SPL token delegate | `alchemy solana delegate revoke --token-account <addr>` |
| Check Solana tx status | `alchemy solana status <signature>` |
| List program accounts | `alchemy solana program accounts <program-id> [--filters '<json>'] [--encoding <enc>] [--limit <n>]` |
| Show Solana account | `alchemy solana program account <address>` |
| Show Solana program metadata | `alchemy solana program show <program-id>` |
| List Solana network IDs | `alchemy solana network list` |

`alchemy solana swap` is reserved for future support and is not implemented.

### Cross-chain

Bridge supports EVM mainnets. For same-chain token exchanges, use `alchemy evm swap`.

| Task | Command |
|------|---------|
| Quote a bridge | `alchemy xchain bridge quote --from <token> --to <token> --amount <n> --to-network <network>` |
| Execute a bridge | `alchemy xchain bridge execute --from <token> --to <token> --amount <n> --to-network <network>` |

Source network comes from `-n, --network`.

### Wallets and signing

A wallet **session** is a CLI-bound signer that the user approves in the [Agent Wallets dashboard](https://dashboard.alchemy.com/products/agent-wallet/evm-wallet). The agent never sees the private key. Sessions expire automatically and can be revoked from the CLI or the dashboard. Session signing capabilities the server may grant: `evm.signMessage`, `evm.signTypedData`, `evm.signAuthorization`, `evm.prepareCalls`, `evm.sendCalls`, `solana.signTransaction`. The session signer does **not** support raw EVM transaction signing — use the action commands (`evm send`, `evm contract call`, `evm approve`, `evm swap`, `xchain bridge`, `solana send`), which execute through Alchemy smart-wallet calls.

Run `alchemy --json --no-interactive wallet status --verify` before any state-changing wallet action — it returns the active signer, expiry, chain-specific session metadata, backend status, and enabled signer capabilities.

| Task | Command |
|------|---------|
| Connect a wallet (session) | `alchemy wallet connect --mode session --instance-name <label>` |
| Connect local EVM wallet (import private key file) | `alchemy wallet connect --mode local --chain evm --import <path>` |
| Connect local Solana wallet | `alchemy wallet connect --mode local --chain solana` |
| Show wallet status | `alchemy wallet status [--verify]` |
| Show configured wallet addresses | `alchemy wallet address` |
| Render an address as a QR code | `alchemy wallet qr` |
| Pick active signer for EVM txns | `alchemy wallet use <session\|local>` |
| Disconnect / revoke wallet | `alchemy wallet disconnect` |
| Per-command signer override | append `--signer session\|local` |

### Webhook (Notify)

| Task | Command |
|------|---------|
| List webhooks | `alchemy webhook list` |
| Create webhook | `alchemy webhook create --body '<json>' [--dry-run]` |
| Update webhook | `alchemy webhook update --body '<json>' [--dry-run]` |
| Delete webhook | `alchemy webhook delete <id> [--yes] [--dry-run]` |
| Get address-activity webhook addresses | `alchemy webhook addresses <id>` |
| Get NFT-activity webhook filters | `alchemy webhook nft-filters <id>` |

### App management (Admin API)

| Task | Command |
|------|---------|
| List apps | `alchemy app list [--cursor <c>] [--limit <n>] [--all] [--search <q>] [--id <appId>]` |
| Get app details | `alchemy app get <id>` |
| Create app | `alchemy app create --name "My App" --networks eth-mainnet [--description <desc>] [--products <ids>] [--dry-run]` |
| Update app metadata | `alchemy app update <id> --name "New Name" [--description <desc>] [--dry-run]` |
| Update app network allowlist | `alchemy app networks <id> --networks eth-mainnet,base-mainnet [--dry-run]` |
| Update app address allowlist | `alchemy app address-allowlist <id> --addresses 0xAA,0xBB [--dry-run]` |
| Update app origin allowlist | `alchemy app origin-allowlist <id> --origins https://a.com,https://b.com [--dry-run]` |
| Update app IP allowlist | `alchemy app ip-allowlist <id> --ips 1.2.3.4,5.6.7.8 [--dry-run]` |
| Delete app | `alchemy app delete <id> [--yes] [--dry-run]` |
| Select default app | `alchemy app select <id>` (equivalent to `alchemy config set app <id>`) |
| List networks configured for an app | `alchemy app configured-networks [--app-id <id>]` |
| List Admin API chain identifiers (for `app create`/`update`) | `alchemy app chains` |
| List EVM RPC network slugs (for `--network`) | `alchemy evm network list [--mainnet-only] [--testnet-only] [--search <term>]` |

The CLI's `app` and `usage` commands are thin wrappers over Alchemy's public **Admin API** (`api.g.alchemy.com/admin-api/v1/...`). Apps and Chains endpoints are public and self-serve; Usage endpoints are also self-serve for app-scoped queries. See `references/operational-admin-api.md` for the REST surface, auth model (`x-alchemy-token` bearer or the CLI's browser session), and endpoint enumeration.

### Usage and metering

| Task | Command |
|------|---------|
| Summary of usage over a range | `alchemy usage summary --start-date <YYYY-MM-DD> --end-date <YYYY-MM-DD> [--app-ids <ids>] [--networks <slugs>] [--metrics amount,usd]` |
| Timeseries of usage over a range | `alchemy usage timeseries --start-date <YYYY-MM-DD> --end-date <YYYY-MM-DD> [--granularity minute\|hour\|day\|month] [--products <ids>] [--metrics amount] [--app-ids <ids>] [--networks <slugs>] [--methods <names>] [--request-types <types>] [--group-by <field>]` |
| Timeseries (alias) | `alchemy usage time-series ...` |

**Range limits** on timeseries queries (as of 2026-07-02):

- Free plan: **7 days** maximum lookback.
- Pay-as-you-go: **30 days** maximum lookback.
- Longer ranges: contact sales.

If the requested range exceeds the plan limit, the CLI does NOT error — it returns the allowed range and surfaces both the requested and returned range in the response so you can detect the truncation.

**`--metrics` semantics** differ by endpoint:

- `alchemy usage timeseries` accepts only `amount`. The `usd` metric is **not** valid on time-series responses (removed 2026-08-13 per API-side change); pass `--metrics amount` or omit the flag.
- `alchemy usage summary` accepts both `amount` and `usd` (comma-separated) on summary responses.

Auth: same browser session as `alchemy app` (Admin API access).

### x402 payments (third-party APIs)

`alchemy x402 request` and `alchemy x402 balance` pay **third-party** APIs in USDC per RFC 402. This is a separate axis from `--x402` / `alchemy config set x402 true` (which handles Alchemy-API auth for Alchemy's own gateway). Requires `@alchemy/cli` 0.22.0 or later.

| Task | Command |
|------|---------|
| Make an x402-paid request | `alchemy x402 request <url> [--dry-run] [--estimate] [--max-payment <usdc>] [--yes]` |
| Show current x402 wallet balance | `alchemy x402 balance` |

- Pass `--max-payment <usdc>` in non-interactive mode; without it the CLI exits `9` (non-interactive without cap).
- Combining `--yes` with no `--max-payment` exits `2` (yes without cap).
- Uses Circle Gateway batched nanopayments or direct EIP-3009 settlement depending on the third-party server.
- Live example endpoint: `https://nano.blockrun.ai` (returns HTTP 402 on the first hit, then completes after the client-signed payment).

### CLI admin and utilities

| Task | Command |
|------|---------|
| Check for CLI updates | `alchemy update-check` |
| View config | `alchemy config list` |
| Reset config | `alchemy config reset --yes` |
| CLI version | `alchemy version` |
| Install MCP / Skills for a client | `alchemy install mcp` / `alchemy install skills` |
| Shell completions | `alchemy completions <bash\|zsh\|fish>` |

## Global flags

| Flag | Description |
|------|-------------|
| `--json` | Force JSON output (auto-enabled when piped) |
| `--no-interactive` | Disable prompts and REPL |
| `-n, --network <network>` | Target network (default: `eth-mainnet`, env: `ALCHEMY_NETWORK`) |
| `--api-key <key>` | Override API key per command (env: `ALCHEMY_API_KEY`) |
| `--x402` | Use x402 wallet-based gateway auth for this command |
| `--wallet-key-file <path>` | Path to an EVM wallet private key file (for x402) |
| `--solana-wallet-key-file <path>` | Path to a Solana wallet key file |
| `--timeout <ms>` | Request timeout in milliseconds |
| `-q, --quiet` | Suppress non-essential output |
| `--verbose` | Log request/response details to stderr |
| `--debug` | Enable debug diagnostics |
| `--no-color` | Disable color output |
| `--reveal` | Show secrets in plain text (use with care; intended for explicit reveal flows) |

## Error handling

Errors return structured JSON on stderr. Each error has a `code`, an `exitCode` (1–9), a `retryable` boolean, and a `recovery` hint. Key codes (from `agent-prompt`):

| Code | Exit | Retryable | Recovery |
|------|------|-----------|----------|
| `AUTH_REQUIRED` | 3 | No | Run `alchemy auth login`, or set `ALCHEMY_API_KEY` / `alchemy config set api-key <key>` |
| `INVALID_API_KEY` | 3 | No | Check the API key; set a valid one with `alchemy config set api-key <key>` |
| `APP_REQUIRED` | 3 | No | Select a default app: `alchemy app select <id>` (or `alchemy config set app <id>`) |
| `NETWORK_NOT_ENABLED` | 3 | No | Enable the target network for your app at dashboard.alchemy.com |
| `SETUP_REQUIRED` | 3 | No | Run `alchemy --json doctor` and follow `nextCommands` |
| `PAYMENT_REQUIRED` | 9 | No | Fund x402 wallet or switch to API key auth |
| `RATE_LIMITED` | 5 | Yes | Wait and retry with backoff; consider upgrading your plan |
| `NETWORK_ERROR` | 6 | Yes | Check connection and retry |
| `RPC_ERROR` | 7 | No | Check method, params, and network; verify API key has access |
| `ADMIN_API_ERROR` | 8 | No | Check the error message; admin commands require an authenticated browser session |
| `NOT_FOUND` | 4 | No | Verify the resource identifier (address, hash, id) is correct |
| `INVALID_ARGS` | 2 | No | Check command usage via `alchemy --json help <command>` |
| `INTERNAL_ERROR` | 1 | No | Unexpected error; retry or report a bug |

Get the full canonical list any time with `alchemy --json --no-interactive agent-prompt`.

## Handing off to other skills

| The user wants to... | Hand off to |
| --- | --- |
| Wire Alchemy into application code that ships to production, with an API key | `alchemy-api` |
| Wire Alchemy into application code without an API key, or pay-per-request as an autonomous agent | `agentic-gateway` |
| Run live work but the CLI isn't installed and they prefer not to install it (MCP is wired in) | `alchemy-mcp` |

### Bridging into the `alchemy-api` flow (extract an API key)

If the user is starting an app-code project and `$ALCHEMY_API_KEY` isn't set in their shell, use the CLI to fetch a key from their Alchemy account, **persist it to the project's `.env`** so it survives across terminal sessions, and export it for the current shell so the agent can use it immediately.

> **Security:** NEVER echo, print, or otherwise surface the extracted API key value in conversation output. Refer to it only as `$ALCHEMY_API_KEY` after exporting. Treat it the same as a password.

```bash
# 1. Try to read a cached key from CLI config (read-only, safe non-interactive).
KEY="$(alchemy --no-interactive --json --reveal config get api-key 2>/dev/null | jq -r .value)"

# 2. If empty/null, run the interactive flow.
#    Note: auth login opens a browser and app select shows a picker, so do NOT
#    pass --no-interactive here. If you already know the app id, pass it
#    explicitly to skip the picker: `alchemy --no-interactive --json app select <id>`.
if [ -z "$KEY" ] || [ "$KEY" = "null" ]; then
  alchemy auth login              # opens browser; sets up account credentials
  alchemy --json app select       # interactive picker (omit --no-interactive so it can render)
  KEY="$(alchemy --no-interactive --json --reveal config get api-key | jq -r .value)"
fi

# 3. Persist to the project's .env (standard practice — survives terminal restarts
#    and gets loaded by dotenv / framework env loaders at runtime).
#    Use .env.local if the project's framework expects that (e.g. Next.js).
ENV_FILE=".env"
touch "$ENV_FILE"
if grep -q '^ALCHEMY_API_KEY=' "$ENV_FILE"; then
  sed -i.bak "s|^ALCHEMY_API_KEY=.*|ALCHEMY_API_KEY=$KEY|" "$ENV_FILE" && rm "$ENV_FILE.bak"
else
  echo "ALCHEMY_API_KEY=$KEY" >> "$ENV_FILE"
fi
grep -qxF "$ENV_FILE" .gitignore 2>/dev/null || echo "$ENV_FILE" >> .gitignore

# 4. Export to the current shell so the agent can call the API immediately.
export ALCHEMY_API_KEY="$KEY"
```

Hand off to the `alchemy-api` skill once `.env` has the key and `ALCHEMY_API_KEY` is exported.

## Official links

- [CLI on npm](https://www.npmjs.com/package/@alchemy/cli)
- [Alchemy docs](https://www.alchemy.com/docs)
- [Get API key](https://dashboard.alchemy.com/)
