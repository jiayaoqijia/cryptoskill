---
name: polymarket
description: >
  Query Polymarket prediction markets — top markets, search, event details, and odds.
  Use when asked about prediction markets, event odds, Polymarket data, election markets,
  crypto predictions, or betting odds on real-world events.
---

# Polymarket

Query prediction market data from Polymarket. Free, no authentication required for read operations.

## API

Base: `https://gamma-api.polymarket.com`

**Top markets by volume**:
```
web_fetch url="https://gamma-api.polymarket.com/markets?limit=20&order=volume24hr&ascending=false&active=true"
```

**Search markets**:
```
web_fetch url="https://gamma-api.polymarket.com/markets?limit=10&active=true&tag=crypto"
```

**Market by slug**:
```
web_fetch url="https://gamma-api.polymarket.com/markets?slug=will-bitcoin-reach-100k-in-2026"
```

**Events list**:
```
web_fetch url="https://gamma-api.polymarket.com/events?limit=20&active=true&order=volume24hr&ascending=false"
```

**Event by slug**:
```
web_fetch url="https://gamma-api.polymarket.com/events?slug=2026-us-midterms"
```

## CLOB API (Order Book)

Base: `https://clob.polymarket.com`

**Market order book**:
```
web_fetch url="https://clob.polymarket.com/book?token_id=TOKEN_ID"
```

**Market price history**:
```
web_fetch url="https://clob.polymarket.com/prices-history?market=CONDITION_ID&interval=1d&fidelity=60"
```

## Response Fields

| Field | Description |
|-------|-------------|
| `question` | The market question |
| `outcomePrices` | Current prices (probabilities) for each outcome |
| `volume` | Total volume traded (USD) |
| `volume24hr` | 24-hour volume |
| `liquidity` | Current liquidity in the market |
| `endDate` | Market resolution date |
| `active` | Whether market is still trading |
| `outcomes` | Array of outcome names |

## Use Cases

- **Event forecasting**: check odds on elections, crypto milestones, geopolitical events
- **Sentiment gauge**: market-implied probabilities as a signal for other strategies
- **Arbitrage detection**: compare Polymarket odds with other prediction platforms
- **Portfolio hedging**: identify hedge opportunities for crypto positions

## Usage Tips

- Prices represent probabilities (0.65 = 65% chance)
- Volume and liquidity indicate market confidence
- Active markets only — check `active=true` filter
- Markets resolve based on verifiable real-world outcomes
- Polymarket operates on Polygon for settlement
