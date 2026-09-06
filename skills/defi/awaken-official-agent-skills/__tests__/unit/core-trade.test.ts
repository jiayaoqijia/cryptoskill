// ============================================================
// Unit Test: Core trade functions (import validation)
// ============================================================

import { describe, test, expect } from 'bun:test';
import { executeSwap, addLiquidity, removeLiquidity, approveTokenSpending } from '../../src/core/trade';

describe('Core trade exports', () => {
  test('executeSwap is a function', () => {
    expect(typeof executeSwap).toBe('function');
  });

  test('addLiquidity is a function', () => {
    expect(typeof addLiquidity).toBe('function');
  });

  test('removeLiquidity is a function', () => {
    expect(typeof removeLiquidity).toBe('function');
  });

  test('approveTokenSpending is a function', () => {
    expect(typeof approveTokenSpending).toBe('function');
  });
});
