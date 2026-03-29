import { describe, it, expect, beforeEach, vi, afterEach } from 'vitest';
import { BudgetExceededError, RateLimitError } from '../errors.js';

// Mock luxon DateTime
vi.mock('luxon', () => {
  let mockNow = Date.now();
  return {
    DateTime: {
      now: () => ({
        setZone: () => ({
          startOf: () => ({
            toMillis: () => {
              // Return start of the current mock day
              const d = new Date(mockNow);
              d.setHours(0, 0, 0, 0);
              return d.getTime();
            },
          }),
        }),
      }),
      _setMockTime: (time: number) => {
        mockNow = time;
      },
      _getMockTime: () => mockNow,
    },
  };
});

// Mock the env module
vi.mock('../env.js', () => ({
  getConfig: () => ({
    ELSA_MAX_USD_PER_CALL: 0.05,
    ELSA_MAX_USD_PER_DAY: 2.00,
    ELSA_MAX_CALLS_PER_MINUTE: 30,
    ELSA_TZ: 'UTC',
  }),
}));

// Import after mocks are set up
import { budgetTracker, getEndpointCost, ENDPOINT_COSTS } from '../budgets.js';
import { DateTime } from 'luxon';

describe('budgets', () => {
  beforeEach(() => {
    budgetTracker.reset();
    vi.useFakeTimers();
    const now = new Date('2024-01-15T12:00:00Z').getTime();
    vi.setSystemTime(now);
    (DateTime as any)._setMockTime(now);
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  describe('ENDPOINT_COSTS', () => {
    it('should have costs for all documented endpoints', () => {
      expect(ENDPOINT_COSTS['/api/search_token']).toBe(0.001);
      expect(ENDPOINT_COSTS['/api/get_token_price']).toBe(0.002);
      expect(ENDPOINT_COSTS['/api/get_balances']).toBe(0.005);
      expect(ENDPOINT_COSTS['/api/get_portfolio']).toBe(0.01);
      expect(ENDPOINT_COSTS['/api/analyze_wallet']).toBe(0.02);
      expect(ENDPOINT_COSTS['/api/get_swap_quote']).toBe(0.01);
      expect(ENDPOINT_COSTS['/api/execute_swap']).toBe(0.02);
      expect(ENDPOINT_COSTS['/api/get_transaction_status']).toBe(0.005);
      expect(ENDPOINT_COSTS['/api/submit_transaction_hash']).toBe(0.005);
    });

    it('should return default cost for unknown endpoints', () => {
      expect(getEndpointCost('/api/unknown')).toBe(0.01);
    });
  });

  describe('per-call budget', () => {
    it('should allow calls within per-call limit', () => {
      expect(() => budgetTracker.checkBudget('/api/search_token')).not.toThrow();
    });
  });

  describe('daily budget', () => {
    it('should track spending across calls', () => {
      budgetTracker.recordCall('/api/get_portfolio', 0.01);
      budgetTracker.recordCall('/api/analyze_wallet', 0.02);

      const status = budgetTracker.getStatus();
      expect(status.spent_today_usd).toBeCloseTo(0.03, 4);
      expect(status.remaining_today_usd).toBeCloseTo(1.97, 4);
    });

    it('should reject calls that would exceed daily limit', () => {
      // Record spending close to limit
      budgetTracker.recordCall('/api/test', 1.99);

      // This 0.02 call would push total over 2.00
      expect(() => budgetTracker.checkBudget('/api/execute_swap')).toThrow(BudgetExceededError);
    });
  });

  describe('rate limiting', () => {
    it('should allow calls within rate limit', () => {
      // Make 29 calls (under limit of 30)
      for (let i = 0; i < 29; i++) {
        budgetTracker.recordCall('/api/search_token', 0.001);
      }

      expect(() => budgetTracker.checkBudget('/api/search_token')).not.toThrow();
    });

    it('should reject calls exceeding rate limit', () => {
      // Make 30 calls (at limit)
      for (let i = 0; i < 30; i++) {
        budgetTracker.recordCall('/api/search_token', 0.001);
      }

      expect(() => budgetTracker.checkBudget('/api/search_token')).toThrow(RateLimitError);
    });

    it('should reset rate limit after 1 minute', () => {
      // Make 30 calls
      for (let i = 0; i < 30; i++) {
        budgetTracker.recordCall('/api/search_token', 0.001);
      }

      // Move forward 61 seconds
      vi.advanceTimersByTime(61_000);

      // Should be allowed now
      expect(() => budgetTracker.checkBudget('/api/search_token')).not.toThrow();
    });
  });

  describe('getStatus', () => {
    it('should return correct budget status', () => {
      budgetTracker.recordCall('/api/search_token', 0.001);
      budgetTracker.recordCall('/api/get_portfolio', 0.01);

      const status = budgetTracker.getStatus();

      expect(status.spent_today_usd).toBeCloseTo(0.011, 4);
      expect(status.remaining_today_usd).toBeCloseTo(1.989, 4);
      expect(status.calls_last_minute).toBe(2);
      expect(status.last_calls).toHaveLength(2);
    });

    it('should only include last 10 calls in last_calls', () => {
      // Make 15 calls
      for (let i = 0; i < 15; i++) {
        budgetTracker.recordCall('/api/search_token', 0.001);
      }

      const status = budgetTracker.getStatus();
      expect(status.last_calls).toHaveLength(10);
      expect(status.calls_last_minute).toBe(15);
    });
  });
});
