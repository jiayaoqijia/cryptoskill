// ============================================================
// Unit Test: Core kline functions (import validation)
// ============================================================

import { describe, test, expect } from 'bun:test';
import { fetchKline, getKlineIntervals } from '../../src/core/kline';

describe('Core kline exports', () => {
  test('fetchKline is a function', () => {
    expect(typeof fetchKline).toBe('function');
  });

  test('getKlineIntervals is a function', () => {
    expect(typeof getKlineIntervals).toBe('function');
  });

  test('getKlineIntervals returns all intervals', () => {
    const intervals = getKlineIntervals();
    expect(Object.keys(intervals)).toEqual(['1m', '15m', '30m', '1h', '4h', '1D', '1W']);
    expect(intervals['1D']).toBe(86400);
  });
});
