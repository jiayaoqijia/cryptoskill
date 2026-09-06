// ============================================================
// Unit Test: Network Config
// ============================================================

import { describe, test, expect, beforeEach, afterEach } from 'bun:test';
import { getNetworkConfig, getRouterAddress, getDeadline, DEFAULT_SLIPPAGE } from '../../lib/config';

describe('getNetworkConfig', () => {
  const originalEnv = process.env.AWAKEN_NETWORK;

  afterEach(() => {
    if (originalEnv !== undefined) {
      process.env.AWAKEN_NETWORK = originalEnv;
    } else {
      delete process.env.AWAKEN_NETWORK;
    }
  });

  test('returns mainnet config by default', () => {
    delete process.env.AWAKEN_NETWORK;
    const config = getNetworkConfig();
    expect(config.chainId).toBe('tDVV');
    expect(config.rpcUrl).toBe('https://tdvv-public-node.aelf.io');
    expect(config.apiBaseUrl).toBe('https://app.awaken.finance');
  });

  test('returns testnet config when specified', () => {
    const config = getNetworkConfig('testnet');
    expect(config.chainId).toBe('tDVW');
    expect(config.rpcUrl).toBe('https://tdvw-test-node.aelf.io');
  });

  test('respects AWAKEN_NETWORK env var', () => {
    process.env.AWAKEN_NETWORK = 'testnet';
    const config = getNetworkConfig();
    expect(config.chainId).toBe('tDVW');
  });

  test('override param takes precedence over env', () => {
    process.env.AWAKEN_NETWORK = 'testnet';
    const config = getNetworkConfig('mainnet');
    expect(config.chainId).toBe('tDVV');
  });

  test('throws on invalid network', () => {
    expect(() => getNetworkConfig('invalid')).toThrow('Unknown network');
  });

  test('mainnet has all router addresses', () => {
    const config = getNetworkConfig('mainnet');
    const keys = Object.keys(config.router).sort();
    expect(keys).toEqual(['0.05', '0.1', '0.3', '3', '5']);
    for (const addr of Object.values(config.router)) {
      expect(addr.length).toBeGreaterThan(10);
    }
  });

  test('testnet has all router addresses', () => {
    const config = getNetworkConfig('testnet');
    const keys = Object.keys(config.router).sort();
    expect(keys).toEqual(['0.05', '0.1', '0.3', '3', '5']);
  });
});

describe('getRouterAddress', () => {
  test('returns correct router for fee rate 0.3', () => {
    const config = getNetworkConfig('mainnet');
    const addr = getRouterAddress(config, '0.3');
    expect(addr).toBe('JvDB3rguLJtpFsovre8udJeXJLhsV1EPScGz2u1FFneahjBQm');
  });

  test('throws on invalid fee rate', () => {
    const config = getNetworkConfig('mainnet');
    expect(() => getRouterAddress(config, '99')).toThrow('No router for feeRate=99');
  });
});

describe('getDeadline', () => {
  test('returns timestamp ~20 min in future by default', () => {
    const now = Math.floor(Date.now() / 1000);
    const deadline = getDeadline();
    expect(deadline).toBeGreaterThan(now + 19 * 60);
    expect(deadline).toBeLessThanOrEqual(now + 21 * 60);
  });

  test('respects custom minutes', () => {
    const now = Math.floor(Date.now() / 1000);
    const deadline = getDeadline(5);
    expect(deadline).toBeGreaterThan(now + 4 * 60);
    expect(deadline).toBeLessThanOrEqual(now + 6 * 60);
  });
});

describe('DEFAULT_SLIPPAGE', () => {
  test('is 0.005 (0.5%)', () => {
    expect(DEFAULT_SLIPPAGE).toBe('0.005');
  });
});
