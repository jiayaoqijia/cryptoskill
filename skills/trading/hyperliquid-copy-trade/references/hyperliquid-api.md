## Hyperliquid info endpoints (perps)

Base URL (mainnet only):

- `https://api.hyperliquid.xyz`

All requests below are `POST /info` with JSON body.

### Clearinghouse state (positions + account summary)

```
{
  "type": "clearinghouseState",
  "user": "0x..."
}
```

Use this for positions and account summary.

### Portfolio (wallet performance)

```
{
  "type": "portfolio",
  "user": "0x..."
}
```

Use this for performance stats (pnl, volume, roi).
