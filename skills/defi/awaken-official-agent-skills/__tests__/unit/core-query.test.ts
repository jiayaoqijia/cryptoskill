// ============================================================
// Unit Test: Core query functions (import validation)
// ============================================================

import { describe, test, expect } from 'bun:test';
import { getQuote, getPair, getTokenBalance, getTokenAllowance, getLiquidityPositions } from '../../src/core/query';

describe('Core query exports', () => {
  test('getQuote is a function', () => {
    expect(typeof getQuote).toBe('function');
  });

  test('getPair is a function', () => {
    expect(typeof getPair).toBe('function');
  });

  test('getTokenBalance is a function', () => {
    expect(typeof getTokenBalance).toBe('function');
  });

  test('getTokenAllowance is a function', () => {
    expect(typeof getTokenAllowance).toBe('function');
  });

  test('getLiquidityPositions is a function', () => {
    expect(typeof getLiquidityPositions).toBe('function');
  });

  test('getQuote throws when no amount provided', async () => {
    const { getNetworkConfig } = await import('../../lib/config');
    const config = getNetworkConfig('mainnet');
    await expect(getQuote(config, { symbolIn: 'ELF', symbolOut: 'USDT' })).rejects.toThrow(
      'Either amountIn or amountOut is required',
    );
  });
});
