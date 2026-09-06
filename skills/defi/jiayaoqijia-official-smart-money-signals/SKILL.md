---
name: smart-money-signals
description: >
  Track smart money trading signals on-chain. Monitor professional investor buy/sell activity,
  whale movements, alpha scanning, and signal performance. Use when asked about smart money,
  whale tracking, alpha signals, trading signals, or professional investor activity.
---

# Smart Money Signals

Track on-chain smart money trading activity — buy/sell signals, whale movements, and performance metrics.

## Binance Web3 Smart Money API (Free, no auth)

**Get smart money signals on Solana**:
```
exec command="curl -s -X POST 'https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/web/signal/smart-money' -H 'Content-Type: application/json' -H 'Accept-Encoding: identity' -d '{\"smartSignalType\":\"\",\"page\":1,\"pageSize\":50,\"chainId\":\"CT_501\"}'"
```

**Get smart money signals on BSC**:
```
exec command="curl -s -X POST 'https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/web/signal/smart-money' -H 'Content-Type: application/json' -H 'Accept-Encoding: identity' -d '{\"smartSignalType\":\"\",\"page\":1,\"pageSize\":50,\"chainId\":\"56\"}'"
```

### Supported Chains

| Chain | chainId |
|-------|---------|
| BSC | `56` |
| Solana | `CT_501` |

### Response Fields

| Field | Description |
|-------|-------------|
| `ticker` | Token symbol |
| `direction` | `buy` or `sell` |
| `smartMoneyCount` | Number of smart money addresses involved |
| `alertPrice` | Price when signal triggered |
| `currentPrice` | Current token price |
| `maxGain` | Maximum gain since signal (%) |
| `exitRate` | % of smart money that has exited |
| `status` | `active` / `timeout` / `completed` |
| `totalTokenValue` | Total trade value (USD) |
| `signalTriggerTime` | When signal fired (ms timestamp) |
| `launchPlatform` | Token launch platform (e.g., Pumpfun) |

### Signal Tags

| Category | Tags |
|----------|------|
| Sensitive Events | Smart Money Add Holdings, Smart Money Reduce Holdings, Whale Buy, Whale Sell |
| Launch Platform | Pumpfun, Moonshot |
| Social Events | DEX Paid |

## DefiLlama Yields (Whale-Tracked Pools)

**High-TVL pools** (proxy for institutional interest):
```
web_fetch url="https://yields.llama.fi/pools"
```
> Sort by TVL descending — highest TVL pools attract smart money.

## Etherscan Token Holders

**Top holders of a token** (identify whale wallets):
```
web_fetch url="https://api.etherscan.io/api?module=token&action=tokenholderlist&contractaddress=TOKEN_ADDRESS&page=1&offset=10&apikey=YOUR_KEY"
```

## Use Cases

- **Alpha scanning**: identify tokens smart money is accumulating early
- **Risk alerts**: detect when smart money starts selling a position
- **Performance tracking**: analyze historical signal accuracy via maxGain and exitRate
- **Whale monitoring**: track large wallet movements across chains
- **Strategy validation**: evaluate signal quality before acting

## Tips

- Higher `smartMoneyCount` = more reliable signal
- Focus on `active` signals — `timeout` signals are stale
- High `exitRate` means most smart money already exited — late entry risk
- `maxGain` shows the best possible return if you followed the signal
- Cross-reference with DefiLlama TVL trends for broader context
- Always DYOR — smart money signals are informational, not financial advice
