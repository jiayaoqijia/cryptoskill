#!/usr/bin/env node
/**
 * Funding Rate Trader - 自动交易脚本
 * 需要 Binance API Key
 */

const ccxt = require('ccxt');
const fs = require('fs');

// 配置
const CONFIG = {
  LEVERAGE: 20,
  STOP_LOSS: 0.10,
  TAKE_PROFIT: 0.20,
  MIN_RATE: -0.0003,
  MIN_SIZE: 5,
};

async function main() {
  // 读取 API Key
  const keyPath = process.env.HOME + '/.openclaw/secrets/binance.json';
  if (!fs.existsSync(keyPath)) {
    console.log('❌ 请先配置 Binance API Key');
    console.log('   创建文件:', keyPath);
    return;
  }
  
  const keys = JSON.parse(fs.readFileSync(keyPath));
  const exchange = new ccxt.binance({ 
    apiKey: keys.apiKey, 
    secret: keys.secret, 
    options: { defaultType: 'future' },
    enableRateLimit: true
  });
  
  console.log('═══════════════════════════════════════════════════════');
  console.log('     🤖 Funding Rate Trader v1.0');
  console.log('═══════════════════════════════════════════════════════');
  
  // 获取余额
  const balance = await exchange.fetchBalance();
  const available = balance.USDT.free;
  
  console.log('\n可用资金:', available.toFixed(2), 'USDT');
  
  if (available < CONFIG.MIN_SIZE) {
    console.log('❌ 资金不足，最少需要', CONFIG.MIN_SIZE, 'USDT');
    return;
  }
  
  // 扫描机会
  const targets = ['AXS','SAND','INJ','PENDLE','BLUR','APT','SUI','ICP'];
  let best = null;
  
  for (const t of targets) {
    try {
      const [f, tk] = await Promise.all([
        exchange.fetchFundingRate(t + '/USDT:USDT'),
        exchange.fetchTicker(t + '/USDT:USDT')
      ]);
      
      if (f.fundingRate < CONFIG.MIN_RATE && tk.percentage > -5) {
        const score = Math.abs(f.fundingRate) * (1 + tk.percentage / 20);
        if (!best || score > best.score) {
          best = { symbol: t, rate: f.fundingRate, change: tk.percentage, price: tk.last, score };
        }
      }
    } catch(e) {}
  }
  
  if (!best) {
    console.log('❌ 无合适机会');
    return;
  }
  
  console.log('\n🎯 目标:', best.symbol);
  console.log('   费率:', (best.rate * 100).toFixed(3) + '%');
  console.log('   24h:', best.change.toFixed(2) + '%');
  
  // 开仓
  const size = Math.min(available * 0.9, 100);
  await exchange.setLeverage(CONFIG.LEVERAGE, best.symbol + '/USDT:USDT');
  
  const qty = (size * CONFIG.LEVERAGE) / best.price;
  await exchange.createOrder(best.symbol + '/USDT:USDT', 'market', 'buy', qty, null, {
    positionSide: 'LONG'
  });
  console.log('\n✅ 开仓:', qty.toFixed(4), best.symbol, '@', best.price);
  
  // 等待
  await new Promise(r => setTimeout(r, 1500));
  
  // 设置止损止盈
  const positions = await exchange.fetchPositions([best.symbol + '/USDT:USDT']);
  const pos = positions.find(p => p.contracts > 0);
  
  if (pos) {
    const stopLoss = best.price * (1 - CONFIG.STOP_LOSS);
    const takeProfit = best.price * (1 + CONFIG.TAKE_PROFIT);
    
    await exchange.createOrder(best.symbol + '/USDT:USDT', 'STOP_MARKET', 'sell', pos.contracts, null, {
      positionSide: 'LONG',
      triggerPrice: stopLoss
    });
    
    await exchange.createOrder(best.symbol + '/USDT:USDT', 'TAKE_PROFIT_MARKET', 'sell', pos.contracts, null, {
      positionSide: 'LONG',
      triggerPrice: takeProfit
    });
    
    console.log('✅ 止损:', stopLoss.toFixed(4), '(-' + (CONFIG.STOP_LOSS * 100) + '%)');
    console.log('✅ 止盈:', takeProfit.toFixed(4), '(+' + (CONFIG.TAKE_PROFIT * 100) + '%)');
  }
  
  console.log('\n═══════════════════════════════════════════════════════');
}

main().catch(e => console.error('错误:', e.message));
