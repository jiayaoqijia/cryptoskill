import { DateTime } from 'luxon';
import { getConfig } from './env.js';
import { BudgetExceededError, RateLimitError } from './errors.js';
import type { BudgetStatus, CallRecord } from './types.js';

// ============================================================================
// Endpoint Cost Table (USD)
// ============================================================================

export const ENDPOINT_COSTS: Record<string, number> = {
  '/api/search_token': 0.001,
  '/api/get_token_price': 0.002,
  '/api/get_balances': 0.005,
  '/api/get_portfolio': 0.01,
  '/api/analyze_wallet': 0.02,
  '/api/get_swap_quote': 0.01,
  '/api/execute_swap': 0.02,
  '/api/get_transaction_status': 0.005,
  '/api/submit_transaction_hash': 0.005,
};

export function getEndpointCost(endpoint: string): number {
  return ENDPOINT_COSTS[endpoint] ?? 0.01; // Default conservative estimate
}

// ============================================================================
// In-Memory Budget Tracker
// ============================================================================

class BudgetTracker {
  private calls: CallRecord[] = [];

  /**
   * Get all calls made today in the configured timezone
   */
  private getCallsToday(): CallRecord[] {
    const config = getConfig();
    const now = DateTime.now().setZone(config.ELSA_TZ);
    const startOfDay = now.startOf('day').toMillis();

    return this.calls.filter((call) => call.timestamp >= startOfDay);
  }

  /**
   * Get calls in the last minute
   */
  private getCallsLastMinute(): CallRecord[] {
    const oneMinuteAgo = Date.now() - 60_000;
    return this.calls.filter((call) => call.timestamp >= oneMinuteAgo);
  }

  /**
   * Clean up old call records (older than 24 hours)
   */
  private cleanup(): void {
    const cutoff = Date.now() - 24 * 60 * 60 * 1000;
    this.calls = this.calls.filter((call) => call.timestamp >= cutoff);
  }

  /**
   * Record a call
   */
  recordCall(endpoint: string, cost_usd: number): void {
    this.calls.push({
      timestamp: Date.now(),
      endpoint,
      cost_usd,
    });
    this.cleanup();
  }

  /**
   * Check if a call can proceed without exceeding budgets
   */
  checkBudget(endpoint: string): void {
    const config = getConfig();
    const estimatedCost = getEndpointCost(endpoint);

    // Check per-call limit
    if (estimatedCost > config.ELSA_MAX_USD_PER_CALL) {
      throw new BudgetExceededError(
        `Estimated cost $${estimatedCost.toFixed(4)} exceeds per-call limit of $${config.ELSA_MAX_USD_PER_CALL.toFixed(2)}`,
        {
          limit: config.ELSA_MAX_USD_PER_CALL,
          requested: estimatedCost,
          spent: 0,
        }
      );
    }

    // Check daily limit
    const spentToday = this.getSpentToday();
    if (spentToday + estimatedCost > config.ELSA_MAX_USD_PER_DAY) {
      throw new BudgetExceededError(
        `Daily budget limit reached. Spent: $${spentToday.toFixed(4)}, Limit: $${config.ELSA_MAX_USD_PER_DAY.toFixed(2)}`,
        {
          limit: config.ELSA_MAX_USD_PER_DAY,
          requested: estimatedCost,
          spent: spentToday,
        }
      );
    }

    // Check rate limit
    const callsLastMinute = this.getCallsLastMinute().length;
    if (callsLastMinute >= config.ELSA_MAX_CALLS_PER_MINUTE) {
      throw new RateLimitError(
        `Rate limit exceeded: ${callsLastMinute}/${config.ELSA_MAX_CALLS_PER_MINUTE} calls in last minute`,
        {
          limit: config.ELSA_MAX_CALLS_PER_MINUTE,
          current: callsLastMinute,
          reset_in_seconds: 60,
        }
      );
    }
  }

  /**
   * Get total spent today
   */
  getSpentToday(): number {
    return this.getCallsToday().reduce((sum, call) => sum + call.cost_usd, 0);
  }

  /**
   * Get current budget status
   */
  getStatus(): BudgetStatus {
    const config = getConfig();
    const callsToday = this.getCallsToday();
    const callsLastMinute = this.getCallsLastMinute();
    const spentToday = callsToday.reduce((sum, call) => sum + call.cost_usd, 0);

    return {
      spent_today_usd: spentToday,
      remaining_today_usd: Math.max(0, config.ELSA_MAX_USD_PER_DAY - spentToday),
      calls_last_minute: callsLastMinute.length,
      last_calls: callsLastMinute.slice(-10), // Last 10 calls
    };
  }

  /**
   * Reset tracker (for testing)
   */
  reset(): void {
    this.calls = [];
  }

  /**
   * Set calls directly (for testing)
   */
  setCalls(calls: CallRecord[]): void {
    this.calls = calls;
  }
}

// Singleton instance
export const budgetTracker = new BudgetTracker();
