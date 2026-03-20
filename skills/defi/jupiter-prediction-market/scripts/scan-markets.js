#!/usr/bin/env node

const {
  JupiterPrediction,
  parseEventsResponse,
  calculateProbability,
  formatUsd
} = require('../src');

const DEFAULT_OPTIONS = {
  category: 'crypto',
  filter: 'trending',
  limit: 20,
  minVolume: 10000,
  status: 'open',
  sortBy: 'volume'
};

async function scanMarkets(options = {}) {
  const config = { ...DEFAULT_OPTIONS, ...options };
  const client = new JupiterPrediction();

  const events = await client.list({
    category: config.category,
    filter: config.filter,
    limit: 50
  });

  const parsed = parseEventsResponse(events);

  let markets = [];
  for (const event of parsed.data) {
    for (const market of event.markets) {
      markets.push({
        marketId: market.marketId,
        title: market.title,
        eventTitle: event.title,
        eventCategory: event.category,
        status: market.status,
        yesPrice: market.buyYesPriceUsd,
        noPrice: market.buyNoPriceUsd,
        volumeUsd: market.volumeUsd,
        liquidityUsd: market.liquidityUsd,
        probability: calculateProbability(market.buyYesPriceUsd)
      });
    }
  }

  markets = markets.filter(m =>
    m.status === config.status &&
    m.volumeUsd >= config.minVolume
  );

  if (config.sortBy === 'volume') {
    markets.sort((a, b) => b.volumeUsd - a.volumeUsd);
  } else if (config.sortBy === 'probability') {
    markets.sort((a, b) => {
      const devA = Math.abs(a.probability - 50);
      const devB = Math.abs(b.probability - 50);
      return devB - devA;
    });
  }

  return markets.slice(0, config.limit);
}

if (require.main === module) {
  const args = process.argv.slice(2);
  const options = {
    category: args.includes('--crypto') ? 'crypto' : args.includes('--sports') ? 'sports' : 'all',
    minVolume: parseInt(args.find(a => a.startsWith('--min-volume='))?.split('=')[1] || 10000),
    limit: parseInt(args.find(a => a.startsWith('--limit='))?.split('=')[1] || 10),
    sortBy: args.includes('--by-probability') ? 'probability' : 'volume'
  };

  scanMarkets(options).then(markets => {
    console.log(`\n📊 Found ${markets.length} markets:\n`);
    markets.forEach((m, i) => {
      console.log(`${i + 1}. ${m.eventTitle}`);
      console.log(`   Market: ${m.title}`);
      console.log(`   YES: ${m.probability?.toFixed(1)}% | Volume: ${formatUsd(m.volumeUsd * 1000000)}`);
      console.log(`   ID: ${m.marketId}\n`);
    });
  }).catch(console.error);
}

module.exports = { scanMarkets, DEFAULT_OPTIONS };
