#!/usr/bin/env node
const https = require('https');

https.get('https://fapi.binance.com/fapi/v1/premiumIndex', res => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    const rates = JSON.parse(data);
    const opps = rates
      .filter(r => r.symbol.endsWith('USDT'))
      .map(r => ({
        coin: r.symbol.replace('USDT',''),
        rate: parseFloat(r.lastFundingRate) * 100,
      }))
      .filter(r => r.rate < -0.01)
      .sort((a,b) => a.rate - b.rate)
      .slice(0, 15);
    
    console.log('=== Negative Funding Opportunities ===');
    console.log('Coin'.padEnd(10), 'Rate'.padEnd(10), 'Annual(5x)');
    opps.forEach(o => {
      console.log(o.coin.padEnd(10), (o.rate.toFixed(3)+'%').padEnd(10), (o.rate*3*365*5).toFixed(0)+'%');
    });
  });
});
