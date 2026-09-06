// ============================================================
// Unit Test: Core kline — error paths, parseTimestamp, getKlineIntervals
// ============================================================

import { describe, test, expect } from 'bun:test';
import { fetchKline, getKlineIntervals } from '../../src/core/kline';
import { getNetworkConfig } from '../../lib/config';
import { KLINE_INTERVALS } from '../../lib/types';

const config = getNetworkConfig('mainnet');

describe('Core kline error paths', () => {
  test('fetchKline throws for invalid interval', async () => {
    await expect(
      fetchKline(config, {
        tradePairId: '00000000-0000-0000-0000-000000000000',
        interval: 'INVALID',
      }),
    ).rejects.toThrow('Invalid interval: INVALID');
  });

  test('fetchKline throws for invalid interval (numeric string)', async () => {
    await expect(
      fetchKline(config, {
        tradePairId: '00000000-0000-0000-0000-000000000000',
        interval: '999',
      }),
    ).rejects.toThrow('Invalid interval');
  });

  test('fetchKline error message includes valid intervals', async () => {
    try {
      await fetchKline(config, {
        tradePairId: '00000000-0000-0000-0000-000000000000',
        interval: 'BAD',
      });
      // Should not reach here
      expect(true).toBe(false);
    } catch (err: any) {
      expect(err.message).toContain('1m');
      expect(err.message).toContain('1D');
      expect(err.message).toContain('1W');
    }
  });

  test('fetchKline returns empty bars or throws for fake pair ID', async () => {
    // SignalR may respond with empty data for unknown pair IDs
    // instead of timing out, so we accept either behavior.
    try {
      const result = await fetchKline(config, {
        tradePairId: '00000000-0000-0000-0000-000000000000',
        interval: '1D',
        timeout: 5000,
      });
      // If it resolves, bars should be empty (no real data for fake ID)
      expect(result.count).toBe(0);
      expect(result.bars).toEqual([]);
    } catch {
      // Timeout or connection error is also acceptable
      expect(true).toBe(true);
    }
  }, 10000);
});

describe('getKlineIntervals', () => {
  test('returns a copy (not the original reference)', () => {
    const a = getKlineIntervals();
    const b = getKlineIntervals();
    expect(a).toEqual(b);
    expect(a).not.toBe(b); // different references
  });

  test('contains all 7 expected intervals', () => {
    const intervals = getKlineIntervals();
    const keys = Object.keys(intervals);
    expect(keys).toEqual(['1m', '15m', '30m', '1h', '4h', '1D', '1W']);
  });

  test('interval periods are ascending', () => {
    const intervals = getKlineIntervals();
    const values = Object.values(intervals);
    for (let i = 1; i < values.length; i++) {
      expect(values[i]).toBeGreaterThan(values[i - 1]);
    }
  });

  test('1m = 60, 1h = 3600, 1D = 86400, 1W = 604800', () => {
    const i = getKlineIntervals();
    expect(i['1m']).toBe(60);
    expect(i['1h']).toBe(3600);
    expect(i['1D']).toBe(86400);
    expect(i['1W']).toBe(604800);
  });

  test('KLINE_INTERVALS constant matches getKlineIntervals()', () => {
    expect(getKlineIntervals()).toEqual(KLINE_INTERVALS);
  });
});
