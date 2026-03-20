#!/usr/bin/env node

const {
  JupiterPrediction,
  parsePositionsResponse,
  filterOpen,
  filterClaimable,
  aggregatePnL,
  formatUsd
} = require('../src');

async function monitorPortfolio(walletAddress) {
  const client = new JupiterPrediction();

  const report = {
    timestamp: new Date().toISOString(),
    wallet: walletAddress,
    summary: {},
    openPositions: [],
    claimable: [],
    warnings: []
  };

  const positions = await client.listPositions({ ownerPubkey: walletAddress });
  const parsed = parsePositionsResponse(positions);

  const pnl = aggregatePnL(parsed);
  report.summary = {
    totalValue: pnl.totalValue,
    totalCost: pnl.totalCost,
    unrealizedPnL: pnl.totalPnL,
    realizedPnL: pnl.totalRealizedPnL,
    feesPaid: pnl.totalFees,
    openCount: filterOpen(parsed).length,
    claimableCount: filterClaimable(parsed).length
  };

  const open = filterOpen(parsed);
  report.openPositions = open.map(p => ({
    marketId: p.marketId,
    side: p.side,
    contracts: p.contracts,
    avgPriceUsd: p.avgPriceUsd,
    currentValue: p.valueUsd,
    unrealizedPnL: p.pnlUsd
  }));

  const claimable = filterClaimable(parsed);
  report.claimable = claimable.map(p => ({
    marketId: p.marketId,
    payoutUsd: p.payoutUsd,
    won: p.contracts > 0
  }));

  if (report.summary.unrealizedPnL < -100) {
    report.warnings.push('Large unrealized loss detected');
  }
  if (report.claimable.length > 0) {
    report.warnings.push(`${report.claimable.length} positions ready to claim`);
  }

  return report;
}

if (require.main === module) {
  const walletAddress = process.argv[2];
  if (!walletAddress) {
    console.error('Usage: node monitor-portfolio.js <wallet-address>');
    process.exit(1);
  }

  monitorPortfolio(walletAddress).then(report => {
    console.log(`\n📊 Portfolio Report - ${report.timestamp}\n`);
    console.log(`💰 Summary:`);
    console.log(`   Total Value:    $${report.summary.totalValue?.toFixed(2) || 0}`);
    console.log(`   Total Cost:     $${report.summary.totalCost?.toFixed(2) || 0}`);
    console.log(`   Unrealized P&L: $${report.summary.unrealizedPnL?.toFixed(2) || 0}`);
    console.log(`   Realized P&L:   $${report.summary.realizedPnL?.toFixed(2) || 0}`);
    console.log(`   Fees Paid:      $${report.summary.feesPaid?.toFixed(2) || 0}`);

    console.log(`\n📌 Open Positions: ${report.openPositions.length}`);
    report.openPositions.slice(0, 5).forEach(p => {
      console.log(`   ${p.marketId}: ${p.contracts} ${p.side} @ $${p.avgPriceUsd?.toFixed(4)} ($${p.unrealizedPnL?.toFixed(2)})`);
    });

    console.log(`\n🎁 Claimable: ${report.claimable.length}`);
    report.claimable.forEach(p => {
      console.log(`   ${p.marketId}: $${p.payoutUsd?.toFixed(2)}`);
    });

    if (report.warnings.length > 0) {
      console.log(`\n⚠️  Warnings:`);
      report.warnings.forEach(w => console.log(`   - ${w}`));
    }
  }).catch(console.error);
}

module.exports = { monitorPortfolio };
