# Agent Workflows

Pre-built workflows for autonomous AI agents.

## Workflow 1: Market Scanner

Scan and filter markets by criteria.

```javascript
async function scanMarkets(options = {}) {
  const {
    category = 'crypto',
    filter = 'trending',
    limit = 20,
    minVolume = 10000,
    status = 'open'
  } = options;

  const events = await client.list({ category, filter, limit: 50 });
  const parsed = parseEventsResponse(events);

  let markets = [];
  for (const event of parsed.data) {
    for (const market of event.markets) {
      markets.push({
        marketId: market.marketId,
        title: market.title,
        eventTitle: event.title,
        status: market.status,
        volumeUsd: market.volumeUsd,
        probability: calculateProbability(market.buyYesPriceUsd)
      });
    }
  }

  return markets
    .filter(m => m.status === status && m.volumeUsd >= minVolume)
    .sort((a, b) => b.volumeUsd - a.volumeUsd)
    .slice(0, limit);
}
```

## Workflow 2: Opportunity Finder

Find potentially mispriced markets.

```javascript
async function findOpportunities(options = {}) {
  const { minVolume = 50000, deviationThreshold = 20 } = options;

  const events = await client.list({ category: 'crypto', filter: 'trending', limit: 30 });
  const parsed = parseEventsResponse(events);

  const opportunities = [];
  
  for (const event of parsed.data) {
    for (const market of event.markets) {
      if (market.status !== 'open' || market.volumeUsd < minVolume) continue;
      
      const probYes = calculateProbability(market.buyYesPriceUsd);
      const deviation = Math.abs(probYes - 50);
      
      if (deviation >= deviationThreshold) {
        opportunities.push({
          marketId: market.marketId,
          eventTitle: event.title,
          yesProbability: probYes,
          recommendation: probYes > 50 ? 'NO' : 'YES',
          edge: deviation
        });
      }
    }
  }

  return opportunities.sort((a, b) => b.edge - a.edge);
}
```

## Workflow 3: Portfolio Monitor

Monitor positions and P&L.

```javascript
async function monitorPortfolio(walletAddress) {
  const positions = await client.listPositions({ ownerPubkey: walletAddress });
  const parsed = parsePositionsResponse(positions);
  const pnl = aggregatePnL(parsed);

  return {
    totalValue: pnl.totalValue,
    unrealizedPnL: pnl.totalPnL,
    realizedPnL: pnl.totalRealizedPnL,
    openCount: filterOpen(parsed).length,
    claimableCount: filterClaimable(parsed).length
  };
}
```

## Workflow 4: Auto-Claim

Batch claim all claimable positions.

```javascript
async function autoClaim(walletAddress, options = {}) {
  const { dryRun = false } = options;

  const positions = await client.listPositions({ ownerPubkey: walletAddress });
  const claimable = filterClaimable(positions.data);

  if (dryRun) {
    console.log('Would claim:', claimable.map(p => p.marketId));
    return;
  }

  for (const pos of claimable) {
    await client.claim(pos.pubkey, walletAddress);
  }
}
```

## Workflow 5: Portfolio Health Check

Risk management checks.

```javascript
async function portfolioHealth(walletAddress, limits = {}) {
  const { maxPositionSize = 1000, maxTotalExposure = 10000 } = limits;

  const positions = await client.listPositions({ ownerPubkey: walletAddress });
  const open = filterOpen(parsePositionsResponse(positions));

  const issues = [];
  const totalExposure = open.reduce((sum, p) => sum + (p.totalCostUsd || 0), 0);

  if (totalExposure > maxTotalExposure) {
    issues.push(`Exposure too high: $${totalExposure.toFixed(2)}`);
  }

  for (const pos of open) {
    if ((pos.totalCostUsd || 0) > maxPositionSize) {
      issues.push(`Position ${pos.marketId} exceeds limit`);
    }
  }

  return { healthy: issues.length === 0, issues, totalExposure };
}
```

## Scheduling

| Workflow | Frequency |
|----------|-----------|
| Market Scanner | Every 1-2 hours |
| Portfolio Monitor | Every 30 min |
| Auto-Claim | Every 1 hour |
| Portfolio Health | Before new trades |
