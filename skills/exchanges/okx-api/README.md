# openclaw-okx-api-skill

[中文](README.zh.md)

An [OpenClaw](https://openclaw.ai) agent skill that enables AI agents to interact with the [OKX](https://www.okx.com) cryptocurrency exchange via the official REST API v5 and WebSocket streams.

---

## What This Skill Does

This skill teaches OpenClaw agents how to:

- Query real-time market data (price, order book, candlesticks, funding rates)
- Manage accounts and positions
- Place, amend, and cancel orders
- Subscribe to live data via WebSocket

When a user asks something like "查一下我的 OKX 账户余额" or "在 OKX 下一个 BTC 限价买单", the agent automatically loads this skill's context and uses it to produce correct, authenticated API calls.

---

## Scope and Responsibilities

### In scope

| Category | Capabilities |
|----------|-------------|
| Market data | Ticker, order book, trades, candlesticks, funding rate, mark price, open interest |
| Account | Balance query, position query |
| Order management | Place / amend / cancel single or batch orders |
| Order history | Pending orders, 7-day history, 3-month archive |
| WebSocket | Public channels (tickers, candles, trades, books); Private channels (orders, positions, account) |
| Instrument types | SPOT, MARGIN, SWAP (perpetual), FUTURES (delivery), OPTION |

### Out of scope

This skill does **not** cover:

- Fund transfers between accounts
- Lending and borrowing (margin)
- Earn / staking products
- Sub-account management
- Options-specific APIs (Greeks, exercise)
- Tax reporting or PnL analytics
- Order strategy execution (grid, DCA, iceberg)

---

## Repository Structure

```
openclaw-okx-api-skill/
├── SKILL.md                          # OpenClaw skill definition (frontmatter + guidance)
├── scripts/
│   └── okx_auth.py                   # Reusable auth/request helper — import this in your scripts
├── examples/
│   ├── get-balance.py                # Print account balance
│   ├── get-market-data.py            # Ticker + candlestick data
│   ├── place-order.py                # Place a limit order (with demo guard)
│   └── websocket-ticker.py          # Real-time price feed via WebSocket
└── references/
    ├── authentication.md             # HMAC SHA256 signature algorithm, edge cases, error codes
    ├── market-data-endpoints.md      # All public REST endpoints
    ├── trading-endpoints.md          # All private REST endpoints
    └── websocket.md                  # WebSocket channels, subscription format, private auth
```

---

## Installation

### Option 1 — Copy to OpenClaw workspace skills directory

```bash
cp -r openclaw-okx-api-skill ~/.openclaw/workspace/skills/okx-api
```

### Option 2 — Copy to agent-skills plugin directory

```bash
cp -r openclaw-okx-api-skill ~/.openclaw/skills/agent-skills/skills/okx-api
```

OpenClaw auto-discovers skills in both locations. No registration step needed.

---

## Configuration

Add your OKX API credentials to `~/.openclaw/openclaw.json` under the top-level `env` field:

```json
{
  "env": {
    "OKX_API_KEY": "your-api-key",
    "OKX_SECRET_KEY": "your-secret-key",
    "OKX_PASSPHRASE": "your-passphrase",
    "OKX_DEMO": "1"
  }
}
```

OpenClaw automatically injects these into every agent session.

| Variable | Description |
|----------|-------------|
| `OKX_API_KEY` | API key from OKX account settings |
| `OKX_SECRET_KEY` | Secret key |
| `OKX_PASSPHRASE` | Passphrase set when creating the API key |
| `OKX_DEMO` | Set to `"1"` to use sandbox (simulated trading); omit or set `"0"` for live |

> **Create API keys at**: OKX → Account → API → Create API Key
>
> For sandbox keys: OKX Demo Trading → Account → API

---

## Standalone Usage

The `scripts/okx_auth.py` helper can be used independently in any Python project:

```python
import sys
sys.path.insert(0, "path/to/openclaw-okx-api-skill/scripts")
from okx_auth import make_request

# Public endpoint — no credentials needed
ticker = make_request("GET", "/api/v5/market/ticker", params={"instId": "BTC-USDT"})
print(ticker[0]["last"])

# Private endpoint — requires OKX_API_KEY, OKX_SECRET_KEY, OKX_PASSPHRASE in env
balance = make_request("GET", "/api/v5/account/balance")

# Place an order
result = make_request("POST", "/api/v5/trade/order", body={
    "instId": "BTC-USDT",
    "tdMode": "cash",
    "side": "buy",
    "ordType": "limit",
    "px": "40000",
    "sz": "0.001",
})
```

Run the examples directly:

```bash
# Market data (no credentials)
python examples/get-market-data.py BTC-USDT 1H

# Account balance (credentials required)
OKX_API_KEY=... OKX_SECRET_KEY=... OKX_PASSPHRASE=... python examples/get-balance.py

# Simulated trading
OKX_DEMO=1 python examples/place-order.py BTC-USDT buy limit 40000 0.001

# Real-time price stream
python examples/websocket-ticker.py BTC-USDT ETH-USDT
```

---

## Requirements

```
requests
websocket-client   # only for websocket-ticker.py
```

Install:

```bash
pip install requests websocket-client
```

Python 3.10+ required (uses `dict | None` type union syntax).

---

## Authentication Overview

OKX API v5 uses HMAC SHA256 signatures for private endpoints:

```
signature = base64(hmac_sha256(timestamp + METHOD + path_with_query + body, secret_key))
```

The `make_request()` function in `scripts/okx_auth.py` handles this automatically. See `references/authentication.md` for the full algorithm, edge cases, and error code reference.

---

## Rate Limits

| Endpoint category | Limit |
|-------------------|-------|
| Public market data | 20 req / 2s per IP |
| Account endpoints | 10 req / 2s per UID |
| Order placement | 60 req / 2s per UID |
| Order cancellation | 60 req / 2s per UID |

On error code `50011` (rate limit exceeded), wait 2 seconds and retry.

---

## License

MIT
