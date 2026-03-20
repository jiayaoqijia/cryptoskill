#!/usr/bin/env node

/**
 * TRC-8004 Utility Functions
 * Common utilities for all scripts
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

/**
 * Load private key with priority:
 * 1. Environment variable TRON_PRIVATE_KEY
 * 2. Environment variable PRIVATE_KEY
 * 3. File ~/.clawdbot/wallets/.deployer_pk
 * 4. Return null if not found
 */
function loadPrivateKey() {
  // Priority 1: TRON_PRIVATE_KEY environment variable
  if (process.env.TRON_PRIVATE_KEY) {
    return process.env.TRON_PRIVATE_KEY;
  }

  // Priority 2: PRIVATE_KEY environment variable
  if (process.env.PRIVATE_KEY) {
    return process.env.PRIVATE_KEY;
  }

  // Priority 3: File ~/.clawdbot/wallets/.deployer_pk
  const pkFile = path.join(os.homedir(), '.clawdbot', 'wallets', '.deployer_pk');
  if (fs.existsSync(pkFile)) {
    try {
      const privateKey = fs.readFileSync(pkFile, 'utf8').trim();
      if (privateKey) {
        return privateKey;
      }
    } catch (error) {
      // File exists but can't read, continue to return null
    }
  }

  return null;
}

/**
 * Get private key or exit with error message
 */
function getPrivateKeyOrExit() {
  const privateKey = loadPrivateKey();
  
  if (!privateKey) {
    console.error('❌ Error: No private key found');
    console.error('');
    console.error('Set your private key using one of these methods:');
    console.error('');
    console.error('1. Environment variable (recommended):');
    console.error('   export TRON_PRIVATE_KEY="your_private_key_here"');
    console.error('   export PRIVATE_KEY="your_private_key_here"');
    console.error('');
    console.error('2. File storage:');
    console.error('   mkdir -p ~/.clawdbot/wallets');
    console.error('   echo "your_private_key_here" > ~/.clawdbot/wallets/.deployer_pk');
    console.error('   chmod 600 ~/.clawdbot/wallets/.deployer_pk');
    console.error('');
    process.exit(1);
  }

  return privateKey;
}

/**
 * Format address for display (shorten if needed)
 */
function formatAddress(address, short = false) {
  if (!address) return '(not set)';
  if (short && address.length > 10) {
    return `${address.slice(0, 6)}...${address.slice(-4)}`;
  }
  return address;
}

/**
 * Format TRX amount from Sun
 */
function formatTRX(sun) {
  return (parseInt(sun) / 1e6).toFixed(6);
}

/**
 * Sleep for specified milliseconds
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Validate network name
 */
function validateNetwork(network, availableNetworks) {
  if (!availableNetworks[network]) {
    console.error(`❌ Invalid network: ${network}`);
    console.error(`Available networks: ${Object.keys(availableNetworks).join(', ')}`);
    process.exit(1);
  }
}

/**
 * Display transaction result
 */
function displayTxResult(tx, networkConfig, action = 'Transaction') {
  console.log('');
  console.log(`✅ ${action} successful!`);
  console.log('');
  console.log(`📋 Transaction: ${tx}`);
  console.log(`🔍 View on explorer: ${networkConfig.explorer}/#/transaction/${tx}`);
  console.log('');
}

/**
 * Display error
 */
function displayError(error, context = 'Operation') {
  console.error('');
  console.error(`❌ ${context} failed:`, error.message);
  if (error.error) {
    console.error('   Details:', error.error);
  }
  console.error('');
}

module.exports = {
  loadPrivateKey,
  getPrivateKeyOrExit,
  formatAddress,
  formatTRX,
  sleep,
  validateNetwork,
  displayTxResult,
  displayError
};
