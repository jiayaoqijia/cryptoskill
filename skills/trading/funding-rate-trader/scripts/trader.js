#!/usr/bin/env node
const fs = require('fs');
const ccxt = require('ccxt');

const config = {
  leverage: 5,
  positionSize: 6,
  stopLoss: 0.15,
  takeProfit: 0.20,
  minRate: -0.001
};

async function main() {
  const keys = JSON.parse(fs.readFileSync(process.env.HOME + '/.openclaw/secrets/binance.json'));
  const exchange = new ccxt.binance({ apiKey: keys.apiKey, secret: keys.secret, options: { defaultType: 'future' } });
  
  console.log('Funding Rate Trader Started');
  console.log('Config:', JSON.stringify(config));
  console.log('Scanning for opportunities...');
  
  // Fetch funding rates
  const funding = await exchange.fetchFundingRates();
  const opps = Object.entries(funding)
    .filter(([sym, fr]) => sym.endsWith('/USDT:USDT') && fr.fundingRate < config.minRate)
    .sort((a,b) => a[1].fundingRate - b[1].fundingRate)
    .slice(0, 5);
  
  console.log('Top opportunities:', opps.map(([s,f]) => s.split('/')[0] + ' ' + (f.fundingRate*100).toFixed(3) + '%').join(', '));
}

main().catch(console.error);
