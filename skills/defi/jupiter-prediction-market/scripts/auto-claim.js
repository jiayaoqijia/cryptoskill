#!/usr/bin/env node

const {
  JupiterPrediction,
  filterClaimable,
  formatUsd
} = require('../src');

const DEFAULT_OPTIONS = {
  dryRun: false,
  minPayout: 1
};

async function autoClaim(walletAddress, options = {}) {
  const config = { ...DEFAULT_OPTIONS, ...options };
  const client = new JupiterPrediction();

  const positions = await client.listPositions({ ownerPubkey: walletAddress });
  const claimable = filterClaimable(positions.data);

  const eligible = claimable.filter(p => p.payoutUsd >= config.minPayout);

  console.log(`Found ${eligible.length} claimable positions (min $${config.minPayout})`);

  if (config.dryRun) {
    console.log('Dry run - would claim:');
    eligible.forEach(p => console.log(`  ${p.marketId}: $${p.payoutUsd.toFixed(2)}`));
    return { dryRun: true, count: eligible.length };
  }

  const results = [];
  for (const pos of eligible) {
    try {
      const result = await client.claim(pos.pubkey, walletAddress);
      results.push({
        marketId: pos.marketId,
        success: !!result.transaction,
        tx: result.transaction
      });
      console.log(`✓ Claimed ${pos.marketId}: ${result.transaction ? 'Success' : 'No TX'}`);
    } catch (error) {
      results.push({
        marketId: pos.marketId,
        success: false,
        error: error.message
      });
      console.log(`✗ Failed ${pos.marketId}: ${error.message}`);
    }
  }

  const successCount = results.filter(r => r.success).length;
  console.log(`\nClaimed ${successCount}/${eligible.length} positions`);

  return { successCount, failedCount: eligible.length - successCount, results };
}

if (require.main === module) {
  const walletAddress = process.argv[2];
  const options = {
    dryRun: process.argv.includes('--dry-run'),
    minPayout: parseInt(process.argv.find(a => a.startsWith('--min='))?.split('=')[1]) || 1
  };

  if (!walletAddress) {
    console.error('Usage: node auto-claim.js <wallet-address> [--dry-run] [--min=<amount>]');
    process.exit(1);
  }

  autoClaim(walletAddress, options).catch(console.error);
}

module.exports = { autoClaim, DEFAULT_OPTIONS };
