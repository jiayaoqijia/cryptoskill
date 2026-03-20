#!/usr/bin/env node

const {
  JupiterPrediction,
  parsePositionsResponse,
  filterOpen
} = require('../src');

const DEFAULT_LIMITS = {
  maxPositionSize: 1000,
  maxTotalExposure: 10000,
  maxPositions: 20,
  minDiversification: 5
};

async function portfolioHealth(walletAddress, limits = {}) {
  const config = { ...DEFAULT_LIMITS, ...limits };
  const client = new JupiterPrediction();

  const issues = [];
  const warnings = [];

  const positions = await client.listPositions({ ownerPubkey: walletAddress });
  const parsed = parsePositionsResponse(positions);
  const open = filterOpen(parsed);

  if (open.length > config.maxPositions) {
    issues.push(`Too many positions: ${open.length} > ${config.maxPositions}`);
  }

  const totalExposure = open.reduce((sum, p) => sum + (p.totalCostUsd || 0), 0);
  if (totalExposure > config.maxTotalExposure) {
    issues.push(`Total exposure too high: $${totalExposure.toFixed(2)} > $${config.maxTotalExposure}`);
  }

  for (const pos of open) {
    if ((pos.totalCostUsd || 0) > config.maxPositionSize) {
      issues.push(`Position ${pos.marketId} exceeds limit: $${pos.totalCostUsd?.toFixed(2)} > $${config.maxPositionSize}`);
    }
  }

  const uniqueMarkets = new Set(open.map(p => p.marketId)).size;
  if (uniqueMarkets < config.minDiversification && open.length > 0) {
    warnings.push(`Low diversification: ${uniqueMarkets} unique markets`);
  }

  const eventGroups = {};
  for (const pos of open) {
    const eventId = pos.marketId.split('-')[0];
    eventGroups[eventId] = (eventGroups[eventId] || 0) + 1;
  }
  for (const [eventId, count] of Object.entries(eventGroups)) {
    if (count > 3) {
      warnings.push(`High concentration in event ${eventId}: ${count} positions`);
    }
  }

  return {
    healthy: issues.length === 0,
    totalExposure,
    positionCount: open.length,
    uniqueMarkets,
    issues,
    warnings
  };
}

if (require.main === module) {
  const walletAddress = process.argv[2];
  if (!walletAddress) {
    console.error('Usage: node portfolio-health.js <wallet-address> [--max-position=<amount>] [--max-exposure=<amount>]');
    process.exit(1);
  }

  const limits = {
    maxPositionSize: parseInt(process.argv.find(a => a.startsWith('--max-position='))?.split('=')[1]) || 1000,
    maxTotalExposure: parseInt(process.argv.find(a => a.startsWith('--max-exposure='))?.split('=')[1]) || 10000,
    maxPositions: parseInt(process.argv.find(a => a.startsWith('--max-positions='))?.split('=')[1]) || 20
  };

  portfolioHealth(walletAddress, limits).then(health => {
    console.log(`\n🏥 Portfolio Health Check\n`);
    console.log(`   Status: ${health.healthy ? '✅ Healthy' : '❌ Issues found'}`);
    console.log(`   Total Exposure: $${health.totalExposure.toFixed(2)}`);
    console.log(`   Open Positions: ${health.positionCount}`);
    console.log(`   Unique Markets: ${health.uniqueMarkets}`);

    if (health.issues.length > 0) {
      console.log(`\n❌ Issues:`);
      health.issues.forEach(i => console.log(`   - ${i}`));
    }

    if (health.warnings.length > 0) {
      console.log(`\n⚠️  Warnings:`);
      health.warnings.forEach(w => console.log(`   - ${w}`));
    }
  }).catch(console.error);
}

module.exports = { portfolioHealth, DEFAULT_LIMITS };
