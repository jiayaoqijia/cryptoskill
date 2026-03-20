#!/usr/bin/env node
/**
 * Cron Runner for Aave Liquidation Monitor
 * Integrates with OpenClaw's cron scheduler
 * 
 * This script is invoked by OpenClaw's cron system based on the configured interval
 * It does NOT store credentials - it uses OpenClaw's message routing system
 */

const monitor = require('./monitor.js');

async function runMonitor(walletAddress, chain = 'ethereum', config = {}) {
  const {
    thresholds = { critical: 1.05, warning: 1.2 },
  } = config;

  try {
    const userPosition = await monitor.fetchUserPosition(walletAddress, chain);
    const alertData = monitor.formatAlertMessage(userPosition, chain, thresholds);

    // Only log risk level and HF, NOT full API response
    console.log(`Health Factor: ${alertData.hfValue.toFixed(4)} | Risk: ${alertData.risk}`);

    // Return structured data for OpenClaw to route to messaging
    return {
      success: true,
      riskLevel: alertData.risk,
      healthFactor: alertData.hfValue,
      message: alertData.message,
      timestamp: new Date().toISOString(),
    };
  } catch (error) {
    console.error(`Monitor error: ${error.message}`);
    return {
      success: false,
      error: error.message,
      timestamp: new Date().toISOString(),
    };
  }
}

// Export for OpenClaw cron integration
module.exports = { runMonitor };

// CLI fallback if run directly
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length < 1) {
    console.error('Usage: node cron-runner.js <wallet> [chain]');
    process.exit(1);
  }
  
  runMonitor(args[0], args[1] || 'ethereum').then(result => {
    if (!result.success) process.exit(1);
  });
}
