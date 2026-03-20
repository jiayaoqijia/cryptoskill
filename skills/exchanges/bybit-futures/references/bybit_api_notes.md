# Bybit API Notes & Gotchas

## Account Setup

- Use **Unified Trading Account (UTA)** — supports spot + derivatives in one account
- API permissions: **Read-Write** for Contract. Never enable Assets/Withdrawal for trading bots
- Testnet available at `https://api-testnet.bybit.com` (set `sandbox: true` in ccxt)

## ccxt Configuration

```python
exchange = ccxt.bybit({
    "apiKey": "YOUR_KEY",
    "secret": "YOUR_SECRET",
    "enableRateLimit": True,
    "options": {"defaultType": "swap"},  # USDT perpetuals
})
```

## Common Pitfalls

1. **Leverage must be set before opening position** — `exchange.set_leverage(5, symbol)`
2. **Symbol format**: ccxt uses `ETH/USDT:USDT` for USDT perpetuals, Bybit WS uses `ETHUSDT`
3. **Rate limits**: 120 requests/min for order endpoints, 600/min for market data
4. **Minimum order size**: varies by symbol (ETH: 0.01, SOL: 0.1, BTC: 0.001)
5. **Funding every 8h**: 00:00, 08:00, 16:00 UTC — check before opening positions

## WebSocket

- Public endpoint: `wss://stream.bybit.com/v5/public/linear`
- Private endpoint: `wss://stream.bybit.com/v5/private` (requires auth)
- Ping interval: 20s recommended
- Topics: `tickers.<symbol>`, `kline.<interval>.<symbol>`, `orderbook.<depth>.<symbol>`
- Kline `confirm: true` = candle closed (use this for signal calculation)

## Fee Structure

- Maker: 0.02% | Taker: 0.06%
- Funding rate: variable, check every 8h
- Use limit orders when possible to save on fees

## Position Modes

- **One-way mode** (default): single position per symbol
- **Hedge mode**: separate long/short positions per symbol
- Set via API: `exchange.set_position_mode(hedged=False, symbol=symbol)`
