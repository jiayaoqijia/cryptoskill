#!/usr/bin/env node
/**
 * Binance Trading Assistant - Position Checker
 * Lists all open futures positions with P&L
 */

const ccxt = require('ccxt');
const fs = require('fs');
const path = require('path');

async function checkPositions() {
  try {
    // Load credentials
    const secretsPath = path.join(process.env.HOME, '.openclaw/secrets/binance.json');
    if (!fs.existsSync(secretsPath)) {
      console.error('Error: Binance credentials not found.');
      process.exit(1);
    }

    const credentials = JSON.parse(fs.readFileSync(secretsPath, 'utf8'));
    
    // Initialize futures exchange
    const exchange = new ccxt.binance({
      apiKey: credentials.apiKey,
      secret: credentials.secret,
      options: { defaultType: 'future' }
    });

    // Fetch positions
    const positions = await exchange.fetchPositions();
    const openPositions = positions.filter(p => parseFloat(p.contracts) !== 0);

    if (openPositions.length === 0) {
      console.log(JSON.stringify({ message: 'No open positions', positions: [] }));
      return;
    }

    // Format positions
    const formattedPositions = openPositions.map(p => ({
      symbol: p.symbol,
      side: p.side,
      size: parseFloat(p.contracts),
      entryPrice: parseFloat(p.entryPrice),
      markPrice: parseFloat(p.markPrice),
      unrealizedPnl: parseFloat((p.unrealizedPnl || 0).toFixed(2)),
      percentage: parseFloat((p.percentage || 0).toFixed(2)),
      leverage: p.leverage,
      notional: parseFloat((p.notional || 0).toFixed(2))
    }));

    const totalPnl = formattedPositions.reduce((sum, p) => sum + p.unrealizedPnl, 0);

    const result = {
      timestamp: new Date().toISOString(),
      totalPositions: openPositions.length,
      totalUnrealizedPnl: parseFloat(totalPnl.toFixed(2)),
      positions: formattedPositions
    };

    console.log(JSON.stringify(result, null, 2));
    
  } catch (error) {
    console.error('Error checking positions:', error.message);
    process.exit(1);
  }
}

checkPositions();
