// ============================================================
// Unit Test: Core query — error paths and edge cases
// ============================================================

import { describe, test, expect } from 'bun:test';
import { getQuote, getPair, getTokenBalance, getTokenAllowance, getLiquidityPositions } from '../../src/core/query';
import { getNetworkConfig } from '../../lib/config';

const config = getNetworkConfig('mainnet');

describe('Core query error paths', () => {
  // ---- getQuote ----
  test('getQuote throws when neither amountIn nor amountOut provided', async () => {
    await expect(
      getQuote(config, { symbolIn: 'ELF', symbolOut: 'USDT' }),
    ).rejects.toThrow('Either amountIn or amountOut is required');
  });

  test('getQuote throws when both amounts are empty strings', async () => {
    await expect(
      getQuote(config, { symbolIn: 'ELF', symbolOut: 'USDT', amountIn: '', amountOut: '' }),
    ).rejects.toThrow();
  });

  test('getQuote throws for invalid token symbol', async () => {
    await expect(
      getQuote(config, { symbolIn: 'NONEXISTENT_TOKEN_XYZ', symbolOut: 'USDT', amountIn: '1' }),
    ).rejects.toThrow();
  });

  // ---- getPair ----
  test('getPair throws for non-existent pair', async () => {
    await expect(
      getPair(config, { token0: 'NONEXISTENT_TOKEN_XYZ', token1: 'USDT', feeRate: '0.3' }),
    ).rejects.toThrow();
  });

  test('getPair throws for invalid fee rate', async () => {
    await expect(
      getPair(config, { token0: 'ELF', token1: 'USDT', feeRate: '99.9' }),
    ).rejects.toThrow();
  });

  // ---- getTokenBalance ----
  test('getTokenBalance throws for invalid token symbol', async () => {
    await expect(
      getTokenBalance(config, { address: 'someAddress', symbol: 'NONEXISTENT_TOKEN_XYZ' }),
    ).rejects.toThrow();
  });

  // ---- getTokenAllowance ----
  test('getTokenAllowance throws for invalid token symbol', async () => {
    await expect(
      getTokenAllowance(config, {
        owner: 'someAddress',
        spender: 'someContract',
        symbol: 'NONEXISTENT_TOKEN_XYZ',
      }),
    ).rejects.toThrow();
  });

  // ---- getLiquidityPositions ----
  test('getLiquidityPositions returns empty for address with no positions', async () => {
    // A valid-looking but unused address should return empty results, not crash
    const result = await getLiquidityPositions(config, {
      address: 'JKjoabe2wyrdD1HYMjVFcKJkGpDZkCPtF3CcsnDmrFWJD3HKm',
    });
    expect(result.totalPositions).toBe(0);
    expect(result.positions).toEqual([]);
  });

  test('getLiquidityPositions respects token0 filter', async () => {
    const result = await getLiquidityPositions(config, {
      address: 'JKjoabe2wyrdD1HYMjVFcKJkGpDZkCPtF3CcsnDmrFWJD3HKm',
      token0: 'NONEXISTENT',
    });
    expect(result.totalPositions).toBe(0);
  });
});
