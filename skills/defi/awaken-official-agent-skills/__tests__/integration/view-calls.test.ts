// ============================================================
// Integration Test: On-chain view calls (mainnet, read-only)
// ============================================================

import { describe, test, expect } from 'bun:test';
import { getNetworkConfig } from '../../lib/config';
import { getBalance, getAllowance, getTokenInfo, callViewMethod } from '../../lib/aelf-client';
import BigNumber from 'bignumber.js';

const config = getNetworkConfig('mainnet');

// A known address with ELF balance (Awaken router 0.3% contract - always has token approvals)
const KNOWN_CONTRACT = config.router['0.3'];

describe('getTokenInfo (mainnet)', () => {
  test('gets ELF token info', async () => {
    const info = await getTokenInfo(config.rpcUrl, config.tokenContract, 'ELF');
    expect(info.symbol).toBe('ELF');
    expect(info.decimals).toBe(8);
  }, 15000);

  test('gets USDT token info', async () => {
    const info = await getTokenInfo(config.rpcUrl, config.tokenContract, 'USDT');
    expect(info.symbol).toBe('USDT');
    expect(info.decimals).toBe(6);
  }, 15000);
});

describe('getBalance (mainnet)', () => {
  test('queries ELF balance for a known contract', async () => {
    const balance = await getBalance(config.rpcUrl, config.tokenContract, 'ELF', KNOWN_CONTRACT);
    // Balance should be a numeric string (possibly "0")
    expect(new BigNumber(balance).isNaN()).toBe(false);
    expect(new BigNumber(balance).gte(0)).toBe(true);
  }, 15000);
});

describe('getAllowance (mainnet)', () => {
  test('queries allowance (may be 0)', async () => {
    const allowance = await getAllowance(
      config.rpcUrl,
      config.tokenContract,
      'ELF',
      KNOWN_CONTRACT,
      config.router['0.05'],
    );
    expect(new BigNumber(allowance).isNaN()).toBe(false);
    expect(new BigNumber(allowance).gte(0)).toBe(true);
  }, 15000);
});
