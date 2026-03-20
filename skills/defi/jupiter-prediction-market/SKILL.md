---
name: jupiter-prediction-market
description: >
  Complete Node.js client for Jupiter Prediction Market API. Use when building AI agents for prediction market trading, portfolio management, or automated trading bots on Solana. Covers: (1) Querying events, markets, orders, positions, payouts, history, and social features, (2) Creating/managing trading positions, (3) Claiming payouts after market settlement, (4) Building autonomous agent workflows for market scanning, opportunity finding, portfolio monitoring, and risk management.
---

# Jupiter Prediction Skill v1.0

## Purpose
Enable AI agents to interact with Jupiter Prediction Market API for autonomous trading and portfolio management.

## When to Use
- Build autonomous trading bots or agents
- Query market data, events, and user positions
- Create automated market scanning and opportunity detection
- Monitor portfolio health and risk
- Claim payouts after market settlement

## Scope
- Read/write access to Jupiter Prediction API
- Requires API key from [Jupiter Portal](https://portal.jup.ag)
- All transactions require user signature via Solana wallet
- Beta API - subject to breaking changes

## Quick Start

```javascript
const { JupiterPrediction, parseEventsResponse, formatUsd } = require('./src');

const client = new JupiterPrediction();

const events = await client.list({ category: 'crypto', filter: 'trending', limit: 5 });
const parsed = parseEventsResponse(events);
console.log('Events:', parsed.data.map(e => e.title));
```

## Configuration

```bash
export JUPITER_API_KEY=your-api-key
```

Or use config file `config/api-key.json`.

## Supported Capabilities

### Client Endpoints

| Category | Methods |
|----------|---------|
| Events | `list`, `search`, `getEvent`, `suggested` |
| Markets | `getMarket`, `orderbook` |
| Orders | `create`, `listOrders`, `status`, `cancelOrder` |
| Positions | `listPositions`, `getPosition`, `closePosition`, `closeAllPositions`, `claim` |
| History | `listHistory`, `getHistoryByPosition` |
| Social | `profile`, `pnlHistory`, `trades`, `leaderboards`, `follow/unfollow` |

### Utility Functions

| Function | Description |
|----------|-------------|
| `microUsdToUsd(microUsd)` | Convert micro USD to USD |
| `formatUsd(microUsd, decimals)` | Format as currency string |
| `calculateProbability(yesPrice)` | Implied probability (%) |
| `parseEventsResponse(response)` | Parse event data |
| `parseMarketResponse(market)` | Parse market data |
| `parsePositionsResponse(response)` | Parse position data |
| `filterClaimable(positions)` | Filter claimable positions |
| `filterOpen(positions)` | Filter open positions |
| `aggregatePnL(positions)` | Calculate total P&L |

## Bundled Scripts

Run from project root:

```bash
# Scan markets by criteria
node scripts/scan-markets.js --crypto --limit=10 --min-volume=10000

# Find mispriced opportunities
node scripts/find-opportunities.js --threshold=20 --min-volume=50000

# Monitor portfolio
node scripts/monitor-portfolio.js <wallet-address>

# Auto-claim winnings
node scripts/auto-claim.js <wallet-address> [--dry-run] [--min=1]

# Portfolio health check
node scripts/portfolio-health.js <wallet-address>
```

## Bundled Workflows

The bundled scripts provide complete autonomous agent workflows:

1. **Market Scanner** - Find markets by volume, probability, category
2. **Opportunity Finder** - Detect mispriced markets
3. **Portfolio Monitor** - Track positions, P&L, claimable
4. **Auto-Claim** - Batch claim winnings
5. **Portfolio Health** - Risk checks (position limits, diversification)
6. **Trading Cycle** - Complete discovery → evaluation → execution

## Code Examples

See `src/` for available endpoints and utilities:
- `src/client.js` - Main API client class
- `src/index.js` - Exports and utility functions
- `src/endpoints/` - Individual endpoint modules
- `src/utils/` - Helper functions (parser, prices, errors)

## API Reference

Client methods are documented in code comments. Main classes:
- `JupiterPrediction` - Main client (src/client.js)
- Utility functions in src/index.js

## Verification

Verify syntax:
```bash
node --check src/index.js
node --check src/client.js
```

Run a script (requires JUPITER_API_KEY):
```bash
export JUPITER_API_KEY=your-key
node scripts/scan-markets.js --crypto --limit=5
```

## Version
- v1.0.0

## License
MIT
