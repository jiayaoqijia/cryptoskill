// ============================================================
// Awaken Agent Kit - Network Configuration
// ============================================================
// Config priority (high → low):
//   1. Function params (SDK callers pass config directly)
//   2. CLI args (--network, --slippage)
//   3. MCP env block (mcp.json env: {})
//   4. Environment variables (AWAKEN_*)
//   5. .env file (Bun auto-loads)
//   6. Code defaults (below)

import type { NetworkConfig } from './types';

// ---- Built-in defaults per network ----

const MAINNET_DEFAULTS: NetworkConfig = {
  chainId: 'tDVV',
  rpcUrl: 'https://tdvv-public-node.aelf.io',
  apiBaseUrl: 'https://app.awaken.finance',
  socketUrl: 'https://app.awaken.finance/signalr-hubs/trade',
  explorerUrl: 'https://aelfscan.io/tDVV',
  tokenContract: '7RzVGiuVWkvL4VfVHdZfQF2Tri3sgLe9U991bohHFfSRZXuGX',
  swapHookContract: 'T3mdFC35CQSatUXQ5bQ886pULo2TnzS9rfXxmsoZSGnTq2a2S',
  router: {
    '0.05': '83ju3fGGnvQzCmtjApUTwvBpuLQLQvt5biNMv4FXCvWKdZgJf',
    '0.3': 'JvDB3rguLJtpFsovre8udJeXJLhsV1EPScGz2u1FFneahjBQm',
    '0.1': 'hyiwdsbDnyoG1uZiw2JabQ4tLiWT6yAuDfNBFbHhCZwAqU1os',
    '3': '2q7NLAr6eqF4CTsnNeXnBZ9k4XcmiUeM61CLWYaym6WsUmbg1k',
    '5': 'UYdd84gLMsVdHrgkr3ogqe1ukhKwen8oj32Ks4J1dg6KH9PYC',
  },
  factory: {
    '0.05': '2b7Gf7YqVmjhZXir7uehmZoRwsYo1KNFTo9JDZiiByxPBQS1d8',
    '0.3': '2AJXAXSwyHbKTHQhKFiaYozakUUQDeh3xrHW9FGi3vYDMBjtiS',
    '0.1': '25CkLPA8qwDRGQci2kFg77i6pZXVivvX4DHW78i1B7rPHdBkoK',
    '3': '2PwfVguYDmYcpJVPmoH9doEpBgd8L28NCcUDiuq77CzvEWzuKZ',
    '5': '2eJ4MnRWFo7YJXB92qj2AF3NWoB3umBggzNLhbGeahkwDYYLAD',
  },
};

const TESTNET_DEFAULTS: NetworkConfig = {
  chainId: 'tDVW',
  rpcUrl: 'https://tdvw-test-node.aelf.io',
  apiBaseUrl: 'https://test-app.awaken.finance',
  socketUrl: 'https://test-app.awaken.finance/signalr-hubs/trade',
  explorerUrl: 'https://testnet.aelfscan.io/tDVW',
  tokenContract: 'ASh2Wt7nSEmYqnGxPPzp4pnVDU4uhj1XW9Se5VeZcX2UDdyjx',
  swapHookContract: '2vahJs5WeWVJruzd1DuTAu3TwK8jktpJ2NNeALJJWEbPQCUW4Y',
  router: {
    '0.05': 'fGa81UPViGsVvTM13zuAAwk1QHovL3oSqTrCznitS4hAawPpk',
    '0.3': '2YnkipJ9mty5r6tpTWQAwnomeeKUT7qCWLHKaSeV1fejYEyCdX',
    '0.1': 'LzkrbEK2zweeuE4P8Y23BMiFY2oiKMWyHuy5hBBbF1pAPD2hh',
    '3': 'EG73zzQqC8JencoFEgCtrEUvMBS2zT22xoRse72XkyhuuhyTC',
    '5': '23dh2s1mXnswi4yNW7eWNKWy7iac8KrXJYitECgUctgfwjeZwP',
  },
  factory: {
    '0.05': 'pVHzzPLV8U3XEAb3utFPnuFL7p6AZtxemgX1yX4tCvKQDQNud',
    '0.3': '2L8uLZRJDUNdmeoA7RT6QbB7TZvu2xHra2gTz2bGrv9Wxs7KPS',
    '0.1': '5KN5uqSC1vz521Lpfh9H1ZLWpU96x6ypEdHrTZF8WdjMmQFQ5',
    '3': '2iFrdeaSKHwpNGWviSMVacjHjdgtZbfrkNeoV1opRzsfBrPVsm',
    '5': 'T25QvHLdWsyHaAeLKu9hvk33MTZrkWD1M7D4cZyU58JfPwhTh',
  },
};

const NETWORK_DEFAULTS: Record<string, NetworkConfig> = {
  mainnet: MAINNET_DEFAULTS,
  testnet: TESTNET_DEFAULTS,
};

// ---- Env override layer ----
// Any AWAKEN_* env var overrides the corresponding field in the selected network config.

function applyEnvOverrides(config: NetworkConfig): NetworkConfig {
  return {
    ...config,
    rpcUrl: process.env.AWAKEN_RPC_URL || config.rpcUrl,
    apiBaseUrl: process.env.AWAKEN_API_BASE_URL || config.apiBaseUrl,
    socketUrl: process.env.AWAKEN_SOCKET_URL || config.socketUrl,
    explorerUrl: process.env.AWAKEN_EXPLORER_URL || config.explorerUrl,
    tokenContract: process.env.AWAKEN_TOKEN_CONTRACT || config.tokenContract,
    swapHookContract: process.env.AWAKEN_SWAP_HOOK_CONTRACT || config.swapHookContract,
  };
}

// ---- Public API ----

export function getNetworkConfig(override?: string): NetworkConfig {
  const network = override || process.env.AWAKEN_NETWORK || 'mainnet';
  const defaults = NETWORK_DEFAULTS[network];
  if (!defaults) {
    throw new Error(`[ERROR] Unknown network: ${network}. Use "mainnet" or "testnet".`);
  }
  return applyEnvOverrides(defaults);
}

export function getRouterAddress(config: NetworkConfig, feeRate: string): string {
  const addr = config.router[feeRate];
  if (!addr) {
    throw new Error(`[ERROR] No router for feeRate=${feeRate}. Available: ${Object.keys(config.router).join(', ')}`);
  }
  return addr;
}

/** Default slippage tolerance (env: AWAKEN_DEFAULT_SLIPPAGE) */
export const DEFAULT_SLIPPAGE = process.env.AWAKEN_DEFAULT_SLIPPAGE || '0.005';

/** Default deadline: 20 minutes from now */
export function getDeadline(minutes = 20): number {
  return Math.floor(Date.now() / 1000) + minutes * 60;
}

/** Channel ID */
export const CHANNEL_ID = '';

/** Labs fee rate for swap (basis points) */
export const SWAP_LABS_FEE_RATE = 15;

/** Safety cap for E2E tests: max amount in base units */
export const E2E_MAX_AMOUNT = '1000000'; // 0.01 ELF (8 decimals)
