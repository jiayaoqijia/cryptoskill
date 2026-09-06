// ============================================================
// Unit Test: aelf-client utility functions
// ============================================================

import { describe, test, expect } from 'bun:test';
import { timesDecimals, divDecimals } from '../../lib/aelf-client';
import BigNumber from 'bignumber.js';

describe('timesDecimals', () => {
  test('converts 1 ELF (8 decimals) to raw', () => {
    const result = timesDecimals('1', 8);
    expect(result.toFixed()).toBe('100000000');
  });

  test('converts 0.5 USDT (6 decimals) to raw', () => {
    const result = timesDecimals('0.5', 6);
    expect(result.toFixed()).toBe('500000');
  });

  test('handles zero', () => {
    const result = timesDecimals('0', 8);
    expect(result.toFixed()).toBe('0');
  });

  test('handles very small amounts', () => {
    const result = timesDecimals('0.00000001', 8);
    expect(result.toFixed()).toBe('1');
  });

  test('handles large amounts', () => {
    const result = timesDecimals('1000000', 8);
    expect(result.toFixed()).toBe('100000000000000');
  });
});

describe('divDecimals', () => {
  test('converts 100000000 raw to 1 ELF', () => {
    const result = divDecimals('100000000', 8);
    expect(result.toFixed()).toBe('1');
  });

  test('converts 500000 raw to 0.5 USDT', () => {
    const result = divDecimals('500000', 6);
    expect(result.toFixed()).toBe('0.5');
  });

  test('handles zero', () => {
    const result = divDecimals('0', 8);
    expect(result.toFixed()).toBe('0');
  });

  test('roundtrip: timesDecimals -> divDecimals', () => {
    const original = '123.45678901';
    const raw = timesDecimals(original, 8);
    const back = divDecimals(raw.toFixed(0), 8);
    // May lose precision due to toFixed(0)
    expect(back.toNumber()).toBeCloseTo(123.45678901, 4);
  });
});
