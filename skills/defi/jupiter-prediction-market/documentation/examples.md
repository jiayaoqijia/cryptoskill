# Code Examples

Quick reference for common operations.

## Setup

```javascript
const { 
  JupiterPrediction, 
  parseEventsResponse,
  parseMarketResponse,
  formatUsd, 
  filterClaimable, 
  aggregatePnL,
  microUsdToUsd,
  calculateProbability
} = require('./src');

const client = new JupiterPrediction();
```

## Discover Trending Markets

```javascript
async function discoverMarkets() {
  const events = await client.list({ 
    category: 'crypto', 
    filter: 'trending', 
    limit: 10 
  });
  
  const parsed = parseEventsResponse(events);
  
  for (const event of parsed.data) {
    console.log(`\n${event.title}`);
    console.log(`   Category: ${event.category}`);
    
    const markets = event.markets
      .filter(m => m.status === 'open' && m.volumeUsd > 0)
      .sort((a, b) => b.volumeUsd - a.volumeUsd)
      .slice(0, 3);
    
    for (const m of markets) {
      const probYes = calculateProbability(m.buyYesPriceUsd);
      console.log(`   ${m.title}: YES ${probYes?.toFixed(1)}% | Vol: $${m.volumeUsd?.toFixed(2)}`);
    }
  }
}
```

## Check Orderbook

```javascript
async function checkOrderbook(marketId) {
  const orderbook = await client.orderbook(marketId);
  
  console.log('YES Orders (top 5):');
  orderbook.yes.slice(0, 5).forEach(([price, size]) => {
    console.log(`  $${(price * 1000000).toFixed(2)}: ${size} contracts`);
  });
  
  console.log('\nNO Orders (top 5):');
  orderbook.no.slice(0, 5).forEach(([price, size]) => {
    console.log(`  $${(price * 1000000).toFixed(2)}: ${size} contracts`);
  });
}
```

## Check P&L

```javascript
async function checkPnL(walletAddress) {
  const positions = await client.listPositions({ ownerPubkey: walletAddress });
  const pnl = aggregatePnL(positions.data);
  
  console.log('Total Value:', formatUsd(pnl.totalValue * 1000000));
  console.log('Total P&L:', formatUsd(pnl.totalPnL * 1000000));
  console.log('Realized P&L:', formatUsd(pnl.totalRealizedPnL * 1000000));
}
```

## Claim Payouts

```javascript
async function claimAll(walletAddress) {
  const positions = await client.listPositions({ ownerPubkey: walletAddress });
  const claimable = filterClaimable(positions.data);
  
  console.log(`Found ${claimable.length} claimable positions`);
  
  for (const pos of claimable) {
    const claim = await client.claim(pos.pubkey, walletAddress);
    console.log(`Claimed: ${claim.transaction ? 'Success' : 'Failed'}`);
  }
}
```

## Portfolio Summary

```javascript
async function checkPortfolio(walletAddress) {
  const positions = await client.listPositions({ ownerPubkey: walletAddress });
  const { parsePositionsResponse, filterOpen, filterClaimable } = require('./src');
  const parsed = parsePositionsResponse(positions);
  
  const pnl = aggregatePnL(parsed);
  console.log('\nPortfolio Summary:');
  console.log(`   Total Value:    $${pnl.totalValue?.toFixed(2) || 0}`);
  console.log(`   Unrealized P&L: $${pnl.totalPnL?.toFixed(2) || 0}`);
  console.log(`   Open Positions: ${filterOpen(parsed).length}`);
  console.log(`   Claimable:      ${filterClaimable(parsed).length}`);
}
```

## Error Handling

```javascript
const { JupiterPredictionError, RateLimitError } = require('./src');

try {
  const result = await client.getMarket('market-id');
} catch (error) {
  if (error.status === 429) {
    console.log('Rate limited, retry after:', error.retryAfter);
  } else if (error.status === 401) {
    console.log('Invalid API key');
  }
  console.error(error.message);
}
```
