# Crypto.com Exchange Skill

AI agent skill for trading on Crypto.com Exchange via the [`cdcx` CLI](https://github.com/crypto-com/cdcx-cli).

## What This Skill Does

Gives your AI agent the ability to:
- Fetch market data (prices, orderbook, candles, instruments) — no auth needed
- Place, amend, and cancel spot and derivatives orders (LIMIT, MARKET)
- Create advanced orders (STOP_LOSS, STOP_LIMIT, TAKE_PROFIT, TAKE_PROFIT_LIMIT)
- Manage OCO, OTO, and OTOCO bracket order groups
- Query balances, positions, order history, and trade history
- Withdraw funds and check deposit/withdrawal status
- Paper trade with live market prices (no auth, no risk)
- Stream real-time market data via WebSocket

## How It Works

This skill delegates all API interaction to the `cdcx` CLI binary, which handles:
- Authentication and HMAC-SHA256 request signing
- Safety tier enforcement (read / sensitive_read / mutate / dangerous)
- Dry-run previews before live execution
- Output formatting (JSON, table, NDJSON)
- Rate limit awareness

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Main skill definition — capabilities, commands, workflows, agent behavior |
| `references/install.md` | Installation methods (npm, curl, cargo, plugin) |
| `references/authentication.md` | Credential setup, profiles, environments, error codes |

## Quick Start

```bash
# 1. Install
npx @cryptocom/cdcx-cli@latest --version

# 2. Authenticate
cdcx auth login --oauth

# 3. Verify
cdcx account summary -o json

# 4. Trade
cdcx trade order BUY BTC_USDT 0.01 --type LIMIT --price 50000 --dry-run -o json
```

## Environments

| Environment | Base URL |
|-------------|----------|
| Production | `https://api.crypto.com/exchange/v1/` |
| UAT Sandbox | `https://uat-api.3ona.co/exchange/v1/` |

## Coverage

- **86+ endpoints** via OpenAPI-driven CLI (auto-discovered, always current)
- **Safety tiers** — read-only by default, opt-in for mutations
- **Paper trading** — test strategies without real funds
- **Streaming** — real-time WebSocket data

## License

MIT
