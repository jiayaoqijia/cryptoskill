---
name: sentio-connect
description: Answer questions about tracked crypto wallets using the Sentio Connect MCP tools — USD-valued token balances, token spot prices, total portfolio value, DeFi positions, 24h/7d holding history, and adding or removing a wallet in the user's tracked list. Use whenever the user mentions a wallet address, an ENS name, a Sui address, a token price, "my wallets", or their portfolio.
---

# Sentio Connect

All data comes from the `sentio` MCP server (hosted at `https://connect.sentio.xyz/v1/mcp`).
The user signs in once via OAuth; if a tool returns an authorization error, tell the user to run
`codex mcp login sentio` (CLI) or re-authorize Sentio Connect in the app's MCP settings.

## Tools

| Tool | Use it when |
| --- | --- |
| `list_wallet_addresses` | The user says "my wallets" / "the addresses I track". Call this first to resolve which wallets exist. No arguments. |
| `get_wallet_balances` | Native + token holdings valued in USD. One wallet on one chain (`address` + `chain`), on several chains in one call (`address` + a list in `chain`; EVM chains together, or `sui_mainnet` alone), on every chain it is tracked on (`address` alone), or every tracked wallet (no arguments). Prefer one call with a chain list, or `address` alone, over one call per chain. |
| `get_token_price` | USD spot price by `symbol` (e.g. `ETH`, `SUI`), or by `address` + `chain` for a specific token: a contract address on EVM chains, a coin type such as `0x2::sui::SUI` on Sui. |
| `get_portfolio_value` | Total USD value across all tracked wallets, broken down per address and chain. No arguments. |
| `get_defi_positions` | Lending, staking, LP and reward positions across chains — one wallet (`address`) or every tracked wallet (no arguments). Prefer the no-argument form when the user has several wallets. Each position carries its `chain` id. |
| `get_token_balance_history` | The user asks how one token holding changed over the last day or week. Take `address`, `chain`, `symbol` and `token` (contract address, omitted for an EVM chain's native coin; on Sui the coin type, always required — SUI too) from a `get_wallet_balances` row; `range` is `24h` or `7d`. Points carry amount, USD price at that instant and USD value. Slow (tens of seconds) — one holding per call, never every token in a wallet. |
| `get_defi_position_history` | The user asks how one DeFi position changed over the last day or week. Take `address`, `chain`, `protocol` (its `protocolId`) and `label` from a `get_defi_positions` row; `range` is `24h` or `7d`. Values are position size at today's prices, so the curve shows deposits, withdrawals, accrued debt and rewards — not price moves. Slow — one position per call. |
| `add_wallet_address` | The user asks to track / watch / add a wallet. `address` is a `0x` EVM address or a `.eth` ENS name (resolved before saving) on EVM chains, or a 64-hex Sui address on `sui_mainnet`; `chain` defaults to `1` (Ethereum). Idempotent — re-adding a tracked address returns the existing entry. Only affects the user's own list. |
| `remove_wallet_address` | The user asks to stop tracking / untrack / remove / delete a wallet. `address` is a `0x` address, a `.eth` name or a Sui address; pass `chain` to untrack it on one chain only, omit it to untrack it everywhere. Fails with "not tracked" when nothing matched. Confirm with the user before calling — it only affects their own list, but it is not undoable. |

Supported `chain` ids: Ethereum `1`, BNB Chain `56`, Base `8453`, Arbitrum `42161`, Sui `sui_mainnet`. Default is `1`. One wallet is either EVM or Sui, never both. Sui wallet addresses are 64 hex chars (`0x…`); Sui tokens are identified by coin type (`0x2::sui::SUI`) wherever a tool takes a token `address` or `token`.

## Guidance

- Prefer one `get_portfolio_value` call over looping `get_wallet_balances` when the user asks for a total.
- `get_wallet_balances` and `get_defi_positions` never double count: wallet holdings and DeFi positions are disjoint.
- Pass ENS names straight through; the server resolves them.
- Some tools may be disabled by the user in their Sentio Connect settings ("capability disabled"). Report that plainly and point them to https://connect.sentio.xyz rather than retrying.
- Write tools require an `mcp:write` connection. If `add_wallet_address` / `remove_wallet_address` are missing from the tool list, the connection is read-only.
