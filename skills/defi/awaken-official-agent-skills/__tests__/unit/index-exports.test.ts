// ============================================================
// Unit Test: Package index exports
// ============================================================

import { describe, test, expect } from 'bun:test';
import * as kit from '../../index';

describe('awaken-agent-kit package exports', () => {
  // Query
  test('exports getQuote', () => expect(typeof kit.getQuote).toBe('function'));
  test('exports getPair', () => expect(typeof kit.getPair).toBe('function'));
  test('exports getTokenBalance', () => expect(typeof kit.getTokenBalance).toBe('function'));
  test('exports getTokenAllowance', () => expect(typeof kit.getTokenAllowance).toBe('function'));
  test('exports getLiquidityPositions', () => expect(typeof kit.getLiquidityPositions).toBe('function'));

  // Trade
  test('exports executeSwap', () => expect(typeof kit.executeSwap).toBe('function'));
  test('exports addLiquidity', () => expect(typeof kit.addLiquidity).toBe('function'));
  test('exports removeLiquidity', () => expect(typeof kit.removeLiquidity).toBe('function'));
  test('exports approveTokenSpending', () => expect(typeof kit.approveTokenSpending).toBe('function'));

  // Kline
  test('exports fetchKline', () => expect(typeof kit.fetchKline).toBe('function'));
  test('exports getKlineIntervals', () => expect(typeof kit.getKlineIntervals).toBe('function'));

  // Config
  test('exports getNetworkConfig', () => expect(typeof kit.getNetworkConfig).toBe('function'));
  test('exports getRouterAddress', () => expect(typeof kit.getRouterAddress).toBe('function'));
  test('exports DEFAULT_SLIPPAGE', () => expect(kit.DEFAULT_SLIPPAGE).toBe('0.005'));

  // Utils
  test('exports getWalletByPrivateKey', () => expect(typeof kit.getWalletByPrivateKey).toBe('function'));
  test('exports KLINE_INTERVALS', () => expect(kit.KLINE_INTERVALS['1D']).toBe(86400));
});
