# Binance Trading Assistant Skill

Monitor Binance account balances, positions, and get price alerts through your AI assistant.

## Capabilities

This skill enables your AI assistant to:
- Query Binance spot and futures balances
- Monitor open positions with real-time P&L
- Track portfolio performance
- Set price alerts for cryptocurrencies

## Commands

The assistant can handle requests like:
- "Check my Binance balance"
- "Show my open positions"
- "What's my total P&L today?"
- "How much BTC do I have?"

## Setup

1. Create Binance API keys (read-only recommended)
2. Store credentials in `~/.openclaw/secrets/binance.json`:
```json
{
  "apiKey": "your_api_key",
  "secret": "your_api_secret"
}
```

## Tools

### check_binance_balance
Query account balances across spot and futures.

**Usage**: "Check my Binance balance"

### check_positions
List all open futures positions with P&L.

**Usage**: "Show my open positions"

### get_portfolio_summary
Get a complete portfolio overview.

**Usage**: "What's my portfolio worth?"

## Safety

- Use read-only API keys
- Keys stored locally, never transmitted
- No trading permissions required

## Pricing

$5/month subscription via ClawHub

## Author

AI Trading Tools
