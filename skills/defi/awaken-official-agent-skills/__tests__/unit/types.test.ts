// ============================================================
// Unit Test: Types & Constants
// ============================================================

import { describe, test, expect } from 'bun:test';
import { KLINE_INTERVALS } from '../../lib/types';

describe('KLINE_INTERVALS', () => {
  test('has all expected intervals', () => {
    expect(Object.keys(KLINE_INTERVALS)).toEqual(['1m', '15m', '30m', '1h', '4h', '1D', '1W']);
  });

  test('1m = 60 seconds', () => {
    expect(KLINE_INTERVALS['1m']).toBe(60);
  });

  test('15m = 900 seconds', () => {
    expect(KLINE_INTERVALS['15m']).toBe(900);
  });

  test('1h = 3600 seconds', () => {
    expect(KLINE_INTERVALS['1h']).toBe(3600);
  });

  test('4h = 14400 seconds', () => {
    expect(KLINE_INTERVALS['4h']).toBe(14400);
  });

  test('1D = 86400 seconds', () => {
    expect(KLINE_INTERVALS['1D']).toBe(86400);
  });

  test('1W = 604800 seconds', () => {
    expect(KLINE_INTERVALS['1W']).toBe(604800);
  });
});
