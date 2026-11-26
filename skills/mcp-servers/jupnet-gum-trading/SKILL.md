---
name: gum-trading
description: Trade spot tokens, tokenized stocks, and up to 50x perpetual futures (GUM Perps), inspect orderbooks and funding rates, and manage omnichain deposits and withdrawals on GUM (gum.ag by Jupiter) using the @gumag/cli (`gumag`) CLI or MCP server. Use when the user asks to quote, buy, sell, long, short, close positions, check balances, or bridge/withdraw on GUM.
license: MIT
metadata:
  author: GUM by Jupiter
  homepage: https://docs.gum.ag/trading-api/cli
---

# GUM Trading (`@gumag/cli`)

Use `gumag` (or `npx -y @gumag/cli@latest`) — or the connected `gum` MCP server — to query markets and execute spot, tokenized stock, perpetual futures, and omnichain transfer workflows on GUM (`https://gum.ag`).

Docs: `https://docs.gum.ag/trading-api/cli` · OpenAPI: `https://api.gum.ag/app/v1/openapi.json`

## Discovery first (do not guess flags)

- Check wallet and spend limits first: `gumag auth status` (or MCP tool `whoami`).
- Find the exact command for any task instead of paging through `--help`:
  `gumag cli search "<task>"` (or MCP `search_api`).
- Inspect exact typed inputs before running an unfamiliar command:
  `gumag schema <command>` (for example `gumag schema perps orders create`).
- Every CLI command outputs JSON on stdout. Failures emit `{"error":{"code","message","details"}}` on stderr with exit code `1`: branch on `error.code`, not the message text.

## Core workflows

### Spot tokens & tokenized stocks
- Search tokens or chains: `gumag tokens search SOL`, `gumag chains list`.
- Quote without signing: `gumag swaps quote ...`.
- Buy / sell (USD notional for `buy`, token units for `sell`):
  `gumag buy SOL 5 --dry-run`
  `gumag sell SOL 0.05 --dry-run`
- Wait for settlement: `gumag swaps watch <id>` or `gumag swaps get <id> --wait` (`final: true` means settled).

### Perpetual futures (GUM Perps)
- Inspect live markets, funding rates, and orderbook:
  - `gumag perps markets list`
  - `gumag perps orderbook get BTC --depth 5`
  - `gumag perps funding history BTC`
- Inspect account, positions, and resting orders:
  - `gumag perps account get`
  - `gumag perps positions`
  - `gumag perps orders list`
- Manage collateral and leverage:
  - `gumag perps deposit 50 --dry-run`
  - `gumag perps withdraw 25 --dry-run`
  - `gumag perps leverage set BTC 5 --dry-run`
- Open or close positions:
  - USD-sized shortcuts (market by default): `gumag long BTC 25 --dry-run`, `gumag short ETH 25 --dry-run`
  - Base-unit or limit/post-only orders: `gumag perps orders create ...`
  - Close a position (reduce-only): `gumag perps close BTC --dry-run`
  - Cancel resting orders: `gumag perps orders cancel ...`

### Omnichain deposits & withdrawals
- Deposit addresses: `gumag deposit`
- Quote a withdrawal without signing: `gumag withdrawals quote ...`
- Withdraw: `gumag withdraw ... --dry-run`

## Safety rules (always follow)

1. **Never print, log, or commit private keys.** Keys live locally in `~/.config/gum` (`gumag auth login`) or env vars (`GUM_SOLANA_SECRET_KEY`, `GUM_EVM_PRIVATE_KEY`).
2. **Always enforce a spend cap** via `GUM_MAX_TRADE_USD` or `gumag auth login --max-usd <usd>`.
3. **Preview before moving funds:**
   - Use read-only quote commands (`swaps quote`, `withdrawals quote`, `perps orders quote`) when only checking prices.
   - Use `--dry-run` (MCP `dryRun: true`) to test a signed flow end-to-end without executing.
4. **Respect `confirmation_required`:** Non-interactive signing commands stop with `confirmation_required` and return the quote in `error.details` unless `--yes` is passed. Show the quote to the user and get explicit approval before re-running with `--yes`.
5. **Never blindly retry ambiguous submissions:**
   - On `status_unavailable`, run the read-only command in `error.details.recovery.command` — do **not** repeat the signed command.
   - When `error.details.retrySubmission` is `false`, check `gumag history list` or `gumag perps orders list` before submitting again.
6. **Only point `GUM_API_URL` at a trusted API** (default: `https://api.gum.ag/app/v1`), because `gumag` signs transactions built by that API.

## MCP server setup

```bash
claude mcp add gum -- npx -y @gumag/cli@latest mcp
```

Use `GUM_MAX_TRADE_USD` on the MCP server environment before calling signed write tools (`trade`, `withdraw`, `perps_place_order`, `perps_close_position`, `perps_cancel_order`, `perps_deposit`, `perps_withdraw`, `perps_set_leverage`), including `dryRun: true` (which still signs locally). Use `quote`, `quote_withdrawal`, and `quote_perps_order` for unsigned quotes.
