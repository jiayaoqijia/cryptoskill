#!/usr/bin/env node
/**
 * Binance Trading Assistant - Balance Checker
 * Queries Binance spot and futures balances
 */

const ccxt = require('ccxt');
const fs = require('fs');
const path = require('path');

async function checkBalance() {
  try {
    // Load credentials
    const secretsPath = path.join(process.env.HOME, '.openclaw/secrets/binance.json');
    if (!fs.existsSync(secretsPath)) {
      console.error('Error: Binance credentials not found. Please create ~/.openclaw/secrets/binance.json');
      process.exit(1);
    }

    const credentials = JSON.parse(fs.readFileSync(secretsPath, 'utf8'));
    
    // Initialize exchange
    const exchange = new ccxt.binance({
      apiKey: credentials.apiKey,
      secret: credentials.secret,
      options: { defaultType: 'spot' }
    });

    // Fetch spot balance
    const spotBalance = await exchange.fetchBalance();
    const spotTotal = Object.entries(spotBalance.total)
      .filter(([_, amount]) => amount > 0)
      .map(([currency, amount]) => ({ currency, amount: parseFloat(amount.toFixed(8)) }));

    // Fetch futures balance
    const futuresExchange = new ccxt.binance({
      apiKey: credentials.apiKey,
      secret: credentials.secret,
      options: { defaultType: 'future' }
    });
    
    const futuresBalance = await futuresExchange.fetchBalance();
    const futuresUSDT = futuresBalance.USDT ? futuresBalance.USDT.total : 0;

    // Fetch positions
    const positions = await futuresExchange.fetchPositions();
    const openPositions = positions.filter(p => parseFloat(p.contracts) !== 0);
    
    let totalUnrealizedPnl = 0;
    openPositions.forEach(p => {
      totalUnrealizedPnl += p.unrealizedPnl || 0;
    });

    // Output results
    const result = {
      timestamp: new Date().toISOString(),
      spot: spotTotal,
      futures: {
        balance: parseFloat(futuresUSDT.toFixed(2)),
        unrealizedPnl: parseFloat(totalUnrealizedPnl.toFixed(2)),
        openPositions: openPositions.length
      },
      totalValue: parseFloat((spotTotal.reduce((sum, item) => {
        // Simplified: only count USDT for now
        return item.currency === 'USDT' ? sum + item.amount : sum;
      }, 0) + futuresUSDT + totalUnrealizedPnl).toFixed(2))
    };

    console.log(JSON.stringify(result, null, 2));
    
  } catch (error) {
    console.error('Error checking balance:', error.message);
    process.exit(1);
  }
}

checkBalance();
