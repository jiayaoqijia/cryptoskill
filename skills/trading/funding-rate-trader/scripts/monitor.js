#!/usr/bin/env node
const fs = require('fs');
const ccxt = require('ccxt');

async function main() {
  const keys = JSON.parse(fs.readFileSync(process.env.HOME + '/.openclaw/secrets/binance.json'));
  const exchange = new ccxt.binance({ apiKey: keys.apiKey, secret: keys.secret, options: { defaultType: 'future' } });
  
  const positions = await exchange.fetchPositions();
  const active = positions.filter(p => Math.abs(p.contracts) > 0);
  
  console.log('=== Active Positions ===');
  let total = 0;
  active.forEach(p => {
    const pnl = p.unrealizedPnl || 0;
    total += pnl;
    console.log(p.symbol.replace('/USDT:USDT','').padEnd(10), pnl >= 0 ? '+' : '', pnl.toFixed(3));
  });
  console.log('Total PnL:', total.toFixed(2));
}

main().catch(console.error);
