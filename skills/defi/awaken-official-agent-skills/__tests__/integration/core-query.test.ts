// ============================================================
// Integration Test: Core query functions (mainnet, read-only)
// ============================================================

import { describe, test, expect } from 'bun:test';
import { getNetworkConfig } from '../../lib/config';
import { getQuote, getPair, getTokenBalance, getTokenAllowance, getLiquidityPositions } from '../../src/core/query';
import BigNumber from 'bignumber.js';

const config = getNetworkConfig('mainnet');
const testAddress = 'vc6sUvrJUutTLR6JsW7Am3wDpSnWyg5UtbuVsStKRVTeLmS9b';

describe('core getQuote (mainnet)', () => {
  test('quotes 1 ELF -> USDT', async () => {
    const result = await getQuote(config, {
      symbolIn: 'ELF',
      symbolOut: 'USDT',
      amountIn: '1',
    });
    expect(result.amountIn).toBe('1');
    expect(new BigNumber(result.amountOut).gt(0)).toBe(true);
    expect(result.distributions.length).toBeGreaterThanOrEqual(1);
  }, 15000);
});

describe('core getPair (mainnet)', () => {
  test('gets ELF/USDT pair', async () => {
    const pair = await getPair(config, { token0: 'ELF', token1: 'USDT', feeRate: '0.3' });
    expect(pair.id).toBeDefined();
    expect(pair.token0.symbol).toBe('ELF');
    expect(pair.token1.symbol).toBe('USDT');
    expect(pair.price).toBeGreaterThan(0);
  }, 15000);
});

describe('core getTokenBalance (mainnet)', () => {
  test('queries ELF balance', async () => {
    const result = await getTokenBalance(config, { address: testAddress, symbol: 'ELF' });
    expect(result.symbol).toBe('ELF');
    expect(result.owner).toBe(testAddress);
    expect(new BigNumber(result.balance).gte(0)).toBe(true);
  }, 15000);
});

describe('core getTokenAllowance (mainnet)', () => {
  test('queries allowance', async () => {
    const result = await getTokenAllowance(config, {
      owner: testAddress,
      spender: config.router['0.3'],
      symbol: 'ELF',
    });
    expect(result.symbol).toBe('ELF');
    expect(new BigNumber(result.allowance).gte(0)).toBe(true);
  }, 15000);
});

describe('core getLiquidityPositions (mainnet)', () => {
  test('queries user liquidity', async () => {
    const result = await getLiquidityPositions(config, { address: testAddress });
    expect(result.address).toBe(testAddress);
    expect(result.totalPositions).toBeGreaterThanOrEqual(0);
    expect(Array.isArray(result.positions)).toBe(true);
  }, 30000);
});
