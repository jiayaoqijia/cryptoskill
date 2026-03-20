#!/usr/bin/env node

const {
  JupiterPrediction,
  parseEventsResponse,
  calculateProbability
} = require('../src');

const DEFAULT_OPTIONS = {
  minVolume: 50000,
  deviationThreshold: 20,
  limit: 10
};

async function findOpportunities(options = {}) {
  const config = { ...DEFAULT_OPTIONS, ...options };
  const client = new JupiterPrediction();

  const events = await client.list({ category: 'crypto', filter: 'trending', limit: 30 });
  const parsed = parseEventsResponse(events);

  const opportunities = [];

  for (const event of parsed.data) {
    for (const market of event.markets) {
      if (market.status !== 'open' || market.volumeUsd < config.minVolume) continue;

      const probYes = calculateProbability(market.buyYesPriceUsd);
      const deviation = Math.abs(probYes - 50);

      if (deviation >= config.deviationThreshold) {
        opportunities.push({
          marketId: market.marketId,
          eventTitle: event.title,
          marketTitle: market.title,
          yesProbability: probYes,
          noProbability: 100 - probYes,
          volumeUsd: market.volumeUsd,
          deviation,
          recommendation: probYes > 50 ? 'NO' : 'YES',
          edge: deviation
        });
      }
    }
  }

  opportunities.sort((a, b) => b.edge - a.edge);
  return opportunities.slice(0, config.limit);
}

if (require.main === module) {
  const args = process.argv.slice(2);
  const options = {
    minVolume: parseInt(args.find(a => a.startsWith('--min-volume='))?.split('=')[1] || 50000),
    deviationThreshold: parseInt(args.find(a => a.startsWith('--threshold='))?.split('=')[1] || 20),
    limit: parseInt(args.find(a => a.startsWith('--limit='))?.split('=')[1] || 10)
  };

  findOpportunities(options).then(opps => {
    console.log(`\n🎯 Found ${opps.length} opportunities:\n`);
    opps.forEach((opp, i) => {
      console.log(`${i + 1}. ${opp.eventTitle}`);
      console.log(`   Market: ${opp.marketTitle}`);
      console.log(`   YES: ${opp.yesProbability.toFixed(1)}% | NO: ${opp.noProbability.toFixed(1)}%`);
      console.log(`   Volume: $${(opp.volumeUsd / 1e6).toFixed(2)}`);
      console.log(`   Edge: ${opp.deviation.toFixed(1)}% → Bet: ${opp.recommendation}`);
      console.log(`   ID: ${opp.marketId}\n`);
    });
  }).catch(console.error);
}

module.exports = { findOpportunities, DEFAULT_OPTIONS };
