#!/usr/bin/env node
/**
 * Aave V3 Liquidation Monitor
 * Fetches user position, calculates health factor, and alerts on risk thresholds
 * 
 * Usage:
 *   node monitor.js <wallet_address> [chain]
 *   node monitor.js 0x1234...5678 ethereum
 */

const AAVE_GRAPHQL_ENDPOINT = 'https://api.v3.aave.com/graphql';

const CHAIN_CONFIG = {
  ethereum: {
    name: 'Ethereum',
    chainId: 1,
    marketAddress: '0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2', // Aave V3 Lending Pool
  },
  polygon: {
    name: 'Polygon',
    chainId: 137,
    marketAddress: '0x794a61358D6845594F94dc1DB02A252b5b4814aD',
  },
  arbitrum: {
    name: 'Arbitrum',
    chainId: 42161,
    marketAddress: '0x794a61358D6845594F94dc1DB02A252b5b4814aD',
  },
};

async function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function fetchUserPosition(walletAddress, chain = 'ethereum', retries = 3) {
  const config = CHAIN_CONFIG[chain];
  if (!config) {
    throw new Error(`Unknown chain: ${chain}. Supported: ${Object.keys(CHAIN_CONFIG).join(', ')}`);
  }

  let lastError;
  for (let attempt = 0; attempt < retries; attempt++) {
    try {
      // Query user market state (health factor, collateral, debt)
      const stateResponse = await fetch(AAVE_GRAPHQL_ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: `query {
            userMarketState(request: {
              user: "${walletAddress.toLowerCase()}"
              market: "${config.marketAddress}"
              chainId: ${config.chainId}
            }) {
              totalDebtBase
              totalCollateralBase
              healthFactor
            }
          }`,
        }),
        timeout: 10000,
      });

      if (!stateResponse.ok) {
        throw new Error(`HTTP ${stateResponse.status}: ${stateResponse.statusText}`);
      }

      const stateData = await stateResponse.json();

      if (stateData.errors) {
        // Do NOT log full response - only error messages
        const errorMsg = stateData.errors.map(e => e.message).join('; ');
        throw new Error(`GraphQL error: ${errorMsg}`);
      }

      if (!stateData.data || !stateData.data.userMarketState) {
        throw new Error('No user market state found. Check wallet address and chain.');
      }

      const marketState = stateData.data.userMarketState;

      // Query user borrows
      const borrowsResponse = await fetch(AAVE_GRAPHQL_ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: `query {
            userBorrows(request: {
              user: "${walletAddress.toLowerCase()}"
              markets: [{chainId: ${config.chainId}, address: "${config.marketAddress}"}]
            }) {
              currency { symbol decimals }
              debt { amount { value } }
              apy { value }
            }
          }`,
        }),
        timeout: 10000,
      });

      const borrowsData = await borrowsResponse.json();
      const borrows = borrowsData.data?.userBorrows || [];

      // Query user supplies
      const suppliesResponse = await fetch(AAVE_GRAPHQL_ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: `query {
            userSupplies(request: {
              user: "${walletAddress.toLowerCase()}"
              markets: [{chainId: ${config.chainId}, address: "${config.marketAddress}"}]
            }) {
              currency { symbol decimals }
              balance { amount { value } }
              apy { value }
              isCollateral
            }
          }`,
        }),
        timeout: 10000,
      });

      const suppliesData = await suppliesResponse.json();
      const supplies = suppliesData.data?.userSupplies || [];

      return {
        healthFactor: marketState.healthFactor,
        totalCollateralBase: marketState.totalCollateralBase,
        totalDebtBase: marketState.totalDebtBase,
        borrows,
        supplies,
      };
    } catch (error) {
      lastError = error;
      const backoffMs = Math.pow(2, attempt + 1) * 1000; // 2s, 4s, 8s
      if (attempt < retries - 1) {
        console.error(`Attempt ${attempt + 1} failed: ${error.message}. Retrying in ${backoffMs}ms...`);
        await sleep(backoffMs);
      }
    }
  }

  throw new Error(`Failed after ${retries} attempts: ${lastError.message}`);
}

function calculateHealthFactorRisk(healthFactor) {
  const hf = parseFloat(healthFactor);
  if (hf <= 1.05) return { level: 'CRITICAL', emoji: '🚨', color: 'red' };
  if (hf <= 1.2) return { level: 'WARNING', emoji: '⚠️', color: 'yellow' };
  return { level: 'STABLE', emoji: '✅', color: 'green' };
}

function formatAlertMessage(userPosition, chain = 'ethereum', thresholds = { critical: 1.05, warning: 1.2 }) {
  const hf = parseFloat(userPosition.healthFactor);
  const risk = calculateHealthFactorRisk(hf);

  const totalCollateral = parseFloat(userPosition.totalCollateralBase);
  const totalDebt = parseFloat(userPosition.totalDebtBase);

  let message = `${risk.emoji} AAVE ${risk.level}\n`;
  message += `Chain: ${CHAIN_CONFIG[chain]?.name || chain}\n`;
  message += `Health Factor: ${hf.toFixed(4)}\n`;
  message += `\n📊 Position:\n`;
  message += `Total Collateral: $${totalCollateral.toFixed(2)}\n`;
  message += `Total Debt: $${totalDebt.toFixed(2)}\n`;

  if (totalCollateral > 0) {
    const debtRatio = (totalDebt / totalCollateral) * 100;
    message += `Debt Ratio: ${debtRatio.toFixed(1)}%\n`;
  }

  if (userPosition.borrows.length > 0) {
    message += `\n💳 Borrowed Assets:\n`;
    userPosition.borrows.forEach(b => {
      const amount = parseFloat(b.debt.amount.value);
      message += `  ${b.currency.symbol}: ${amount.toFixed(4)}\n`;
    });
  }

  if (userPosition.supplies.length > 0) {
    message += `\n🏦 Supplied (Collateral):\n`;
    userPosition.supplies.forEach(s => {
      const amount = parseFloat(s.balance.amount.value);
      const collateralBadge = s.isCollateral ? ' (collateral enabled)' : ' (supplied but not collateral)';
      message += `  ${s.currency.symbol}: ${amount.toFixed(4)}${collateralBadge}\n`;
    });
  }

  if (risk.level === 'CRITICAL') {
    message += `\n⚡ URGENT: Liquidation at HF ≤ 1.0!\n`;
    message += `Actions:\n`;
    message += `  1. Repay debt immediately\n`;
    message += `  2. Add more collateral\n`;
    message += `  3. Consider eMode for correlated assets\n`;
  } else if (risk.level === 'WARNING') {
    message += `\n⚠️ ACTION SOON: Health factor approaching danger zone\n`;
  }

  message += `\n⏰ Checked: ${new Date().toISOString()}\n`;

  return { risk: risk.level, hfValue: hf, message };
}

async function main() {
  const args = process.argv.slice(2);

  if (args.length < 1) {
    console.error('Usage: node monitor.js <wallet_address> [chain]');
    console.error('Example: node monitor.js 0x1234567890abcdef1234567890abcdef12345678 ethereum');
    process.exit(1);
  }

  const walletAddress = args[0];
  const chain = args[1] || 'ethereum';

  // Validate wallet address format
  if (!/^0x[a-fA-F0-9]{40}$/.test(walletAddress)) {
    console.error(`Invalid wallet address: ${walletAddress}`);
    console.error('Expected format: 0x' + 'a'.repeat(40));
    process.exit(1);
  }

  try {
    console.log(`Fetching Aave position for ${walletAddress} on ${chain}...`);
    const userPosition = await fetchUserPosition(walletAddress, chain);
    const alertData = formatAlertMessage(userPosition, chain);

    console.log(alertData.message);
    console.log(`\nRisk Level: ${alertData.risk}`);
    console.log(`Health Factor: ${alertData.hfValue.toFixed(4)}`);

    // Exit code indicates risk level for cron integration
    if (alertData.risk === 'CRITICAL') process.exit(1);
    if (alertData.risk === 'WARNING') process.exit(2);
    process.exit(0); // STABLE
  } catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(127); // Error code
  }
}

if (require.main === module) {
  main().catch(error => {
    console.error(error);
    process.exit(1);
  });
}

module.exports = {
  fetchUserPosition,
  calculateHealthFactorRisk,
  formatAlertMessage,
};
