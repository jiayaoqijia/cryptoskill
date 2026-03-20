# API Reference

Complete API endpoint documentation.

## Client Configuration

```javascript
const { JupiterPrediction } = require('./src');

const client = new JupiterPrediction({
  maxRetries: 3,
  baseDelay: 1000,
  minRequestInterval: 100
});
```

## Endpoints

### Events

| Method | Endpoint | Description |
|--------|----------|-------------|
| `list(params)` | `GET /events` | List events |
| `search(query, limit)` | `GET /events/search` | Search events |
| `getEvent(eventId)` | `GET /events/:eventId` | Get event |
| `suggested(pubkey)` | `GET /events/suggested/:pubkey` | Suggested events |

### Markets

| Method | Endpoint | Description |
|--------|----------|-------------|
| `getMarket(marketId)` | `GET /markets/:marketId` | Market details |
| `orderbook(marketId)` | `GET /orderbook/:marketId` | Orderbook |

### Orders

| Method | Endpoint | Description |
|--------|----------|-------------|
| `create(orderData)` | `POST /orders` | Create order |
| `listOrders(params)` | `GET /orders` | List orders |
| `status(orderPubkey)` | `GET /orders/status/:orderPubkey` | Order status |
| `cancelOrder(orderPubkey, ownerPubkey)` | `DELETE /orders/:orderPubkey` | Cancel |

### Positions

| Method | Endpoint | Description |
|--------|----------|-------------|
| `listPositions(params)` | `GET /positions` | List positions |
| `getPosition(positionPubkey)` | `GET /positions/:positionPubkey` | Get position |
| `closePosition(positionPubkey, ownerPubkey)` | `DELETE /positions/:positionPubkey` | Close |
| `claim(positionPubkey, ownerPubkey)` | `POST /positions/:positionPubkey/claim` | Claim |

### Social

| Method | Endpoint | Description |
|--------|----------|-------------|
| `profile(pubkey)` | `GET /profiles/:pubkey` | User profile |
| `pnlHistory(pubkey, interval, count)` | `GET /profiles/:pubkey/pnl-history` | P&L |
| `trades(params)` | `GET /trades` | Recent trades |
| `leaderboards(params)` | `GET /leaderboards` | Leaderboards |

## Utilities

| Function | Description |
|----------|-------------|
| `microUsdToUsd(microUsd)` | Convert micro USD to USD |
| `usdToMicroUsd(usd)` | Convert USD to micro USD |
| `formatUsd(microUsd, decimals)` | Format as currency |
| `calculateProbability(yesPrice)` | Implied probability % |
| `parseEventsResponse(response)` | Parse events |
| `parseMarketResponse(market)` | Parse market |
| `parsePositionsResponse(response)` | Parse positions |
| `filterClaimable(positions)` | Filter claimable |
| `filterOpen(positions)` | Filter open |
| `aggregatePnL(positions)` | Total P&L |

## Error Classes

| Class | Status |
|-------|--------|
| `JupiterPredictionError` | Base |
| `RateLimitError` | 429 |
| `ValidationError` | 400 |
| `AuthenticationError` | 401 |
| `NotFoundError` | 404 |
