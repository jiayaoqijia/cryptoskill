---
name: hyperliquid
version: 1.1.0
description: Query Hyperliquid DEX for account balances, positions, PnL, and margin data via ClawdBot API
author: ClawdBot
category: finance
tags:
  - defi
  - trading
  - perpetuals
  - hyperliquid
  - crypto
  - portfolio
  - positions
  - margin-trading
  - dex
  - derivatives
env:
  - name: TRADING_WALLET_ADDRESS
    description: Default wallet address to query (0x format)
    required: false
keywords:
  - hyperliquid account
  - perp positions
  - unrealized pnl
  - margin usage
  - liquidation price
  - cross margin
  - leverage trading
triggers:
  - hyperliquid
  - my perp positions
  - hyperliquid balance
  - check my HL account
  - show positions on hyperliquid
---

# Hyperliquid DEX Integration

Query your Hyperliquid perpetuals account for real-time balances, open positions, unrealized PnL, and margin data.

## ClawdBot Integration

This skill is designed for **ClawdBot** - it calls ClawdBot's internal API server which proxies requests to the official Hyperliquid API at `https://api.hyperliquid.xyz`.

**Architecture:**
```
User → ClawdBot Gateway → ClawdBot API Server → Hyperliquid Public API
                         (Railway)              (api.hyperliquid.xyz)
```

The ClawdBot API server handles:
- Timeout protection (15s)
- Response parsing and formatting
- Default wallet address from env vars

## Capabilities

- **Account Overview**: Get total account value, free collateral, and margin usage
- **Position Tracking**: View all open perpetual positions with size, direction, entry price
- **PnL Monitoring**: Real-time unrealized PnL and return on equity per position
- **Risk Management**: Liquidation prices and leverage info for each position
- **Multi-Wallet**: Query any wallet address or use configured trading wallet

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `TRADING_WALLET_ADDRESS` | No | Default wallet address (0x format) to query when none provided |

## API Endpoint

**ClawdBot Internal API:**
```
POST {CLAWDBOT_API_URL}/api/hyperliquid/account
```

**Upstream API (called by ClawdBot):**
```
POST https://api.hyperliquid.xyz/info
```

### Request (Optional Body)

```json
{
  "walletAddress": "0x..."
}
```

If no wallet address provided, uses `TRADING_WALLET_ADDRESS` env var.

### Response

```json
{
  "timestamp": "2026-02-10T03:30:00.000Z",
  "walletAddress": "0x...",
  "account": {
    "accountValue": 10523.45,
    "totalPositionNotional": 25000.00,
    "freeCollateral": 5200.00,
    "totalMarginUsed": 5323.45
  },
  "positions": [
    {
      "coin": "ETH",
      "direction": "long",
      "size": 2.5,
      "entryPrice": 2450.00,
      "positionValue": 6250.00,
      "unrealizedPnl": 125.50,
      "returnOnEquity": 0.024,
      "leverage": { "type": "cross", "value": 5 },
      "liquidationPrice": 1850.00,
      "marginUsed": 1250.00
    }
  ],
  "positionCount": 1
}
```

## Security Notes

- **Read-only**: This skill only reads account data, no trading/signing capabilities
- **Public API**: Uses Hyperliquid's public info API (no authentication required)
- **No private keys**: Only wallet addresses (public) are used
- **Timeout protected**: 15-second timeout prevents hanging requests

## Example Usage

### Check Account Balance
```
"What's my Hyperliquid balance?"
"Show my HL account value"
```

### View Positions
```
"What positions do I have open on Hyperliquid?"
"Am I in profit on my perps?"
"What's my unrealized PnL?"
```

### Risk Check
```
"What are my liquidation prices on Hyperliquid?"
"How much margin am I using?"
"What leverage am I running?"
```

## Related

- [Hyperliquid Docs](https://hyperliquid.gitbook.io/hyperliquid-docs)
- `ichimoku` - Ichimoku Cloud trading signals
- `wallet-tracker` - Monitor wallet balances across chains
- `crypto-tracker` - Track crypto prices and portfolios
