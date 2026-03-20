#!/usr/bin/env node
/**
 * Funding Rate Scanner - 扫描负费率机会
 * 无需 API Key，任何人都可以使用
 */

const https = require('https');

const COINS = ['BTC','ETH','SOL','DOGE','XRP','ADA','AVAX','LINK','DOT','ATOM','UNI','LTC','INJ','PENDLE','AXS','MANA','SAND','SNX','AAVE','CRV','GMX','DYDX','ARB','OP','SUI','SEI','TIA','BLUR','WLD','PEPE','SHIB','NEAR','APT','FTM','MATIC','FIL','ICP','RUNE','ENS','LDO','MKR','COMP','YFI','SUSHI','1INCH'];

async function fetchFundingRate(symbol) {
  return new Promise((resolve) => {
    const url = `https://fapi.binance.com/fapi/v1/premiumIndex?symbol=${symbol}USDT`;
    https.get(url, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          resolve({ symbol, rate: parseFloat(json.lastFundingRate) });
        } catch(e) {
          resolve(null);
        }
      });
    }).on('error', () => resolve(null));
  });
}

async function fetch24hChange(symbol) {
  return new Promise((resolve) => {
    const url = `https://fapi.binance.com/fapi/v1/ticker/24hr?symbol=${symbol}USDT`;
    https.get(url, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          resolve(parseFloat(json.priceChangePercent));
        } catch(e) {
          resolve(0);
        }
      });
    }).on('error', () => resolve(0));
  });
}

async function main() {
  console.log('═══════════════════════════════════════════════════════');
  console.log('     📊 Funding Rate Scanner v1.0');
  console.log('═══════════════════════════════════════════════════════');
  console.log('');
  
  const results = [];
  
  for (const coin of COINS) {
    const funding = await fetchFundingRate(coin);
    if (funding && funding.rate < -0.0001) {
      const change = await fetch24hChange(coin);
      results.push({ ...funding, change });
    }
  }
  
  results.sort((a, b) => a.rate - b.rate);
  
  console.log('Coin\t\tRate\t\t24h\t\tAnnual(20x)');
  console.log('─'.repeat(55));
  
  for (const r of results.slice(0, 15)) {
    const annual = (Math.abs(r.rate) * 3 * 365 * 20 * 100).toFixed(0);
    const signal = r.change > 0 ? '🟢' : (r.change > -5 ? '⚪' : '🔴');
    console.log(`${signal} ${r.symbol.padEnd(8)}\t${(r.rate * 100).toFixed(3)}%\t\t${r.change.toFixed(1)}%\t\t${annual}%`);
  }
  
  const best = results.find(r => r.change > -3);
  if (best) {
    console.log('');
    console.log('🏆 Best opportunity:', best.symbol);
    console.log('   Rate:', (best.rate * 100).toFixed(3) + '%');
    console.log('   24h:', best.change.toFixed(1) + '%');
    console.log('   Annual (20x):', (Math.abs(best.rate) * 3 * 365 * 20 * 100).toFixed(0) + '%');
  }
  
  console.log('');
  console.log('═══════════════════════════════════════════════════════');
}

main();
