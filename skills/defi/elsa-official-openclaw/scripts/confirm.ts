import { getConfig, getConfirmationTtlMs, isConfirmationRequired } from './env.js';
import { ConfirmationInvalidError, ConfirmationRequiredError } from './errors.js';
import { generateToken, hashParams, normalizeSwapParams, nowMs } from './util.js';
import type { ConfirmationTokenData, NormalizedSwapParams } from './types.js';

// ============================================================================
// In-Memory Confirmation Token Store
// ============================================================================

class ConfirmationStore {
  private tokens: Map<string, ConfirmationTokenData> = new Map();

  /**
   * Issue a new confirmation token for swap parameters
   */
  issueToken(params: {
    from_chain: string;
    from_token: string;
    from_amount: string;
    to_chain: string;
    to_token: string;
    wallet_address: string;
    slippage: number;
  }): string {
    // Cleanup expired tokens first
    this.cleanup();

    const normalized = normalizeSwapParams(params);
    const token = generateToken();
    const now = nowMs();
    const ttl = getConfirmationTtlMs();

    this.tokens.set(token, {
      createdAt: now,
      expiresAt: now + ttl,
      normalizedParamsHash: hashParams(normalized),
    });

    return token;
  }

  /**
   * Validate and consume a confirmation token
   * Returns true if valid, throws if invalid
   */
  validateAndConsume(
    token: string,
    params: {
      from_chain: string;
      from_token: string;
      from_amount: string;
      to_chain: string;
      to_token: string;
      wallet_address: string;
      slippage: number;
    }
  ): boolean {
    const data = this.tokens.get(token);

    if (!data) {
      throw new ConfirmationInvalidError(
        'Confirmation token not found. Run elsa_execute_swap_dry_run first.',
        { reason: 'not_found' }
      );
    }

    // Check expiry
    if (nowMs() > data.expiresAt) {
      this.tokens.delete(token);
      throw new ConfirmationInvalidError(
        'Confirmation token has expired. Run elsa_execute_swap_dry_run again.',
        { reason: 'expired' }
      );
    }

    // Check params match
    const normalized = normalizeSwapParams(params);
    const expectedHash = hashParams(normalized);

    if (data.normalizedParamsHash !== expectedHash) {
      throw new ConfirmationInvalidError(
        'Swap parameters do not match the dry-run. Run elsa_execute_swap_dry_run with the same parameters.',
        { reason: 'params_mismatch' }
      );
    }

    // One-time use: delete after successful validation
    this.tokens.delete(token);

    return true;
  }

  /**
   * Check if confirmation is required and token is present
   */
  requireConfirmation(token: string | undefined, params: {
    from_chain: string;
    from_token: string;
    from_amount: string;
    to_chain: string;
    to_token: string;
    wallet_address: string;
    slippage: number;
  }): void {
    if (!isConfirmationRequired()) {
      return;
    }

    if (!token) {
      throw new ConfirmationRequiredError();
    }

    this.validateAndConsume(token, params);
  }

  /**
   * Remove expired tokens
   */
  private cleanup(): void {
    const now = nowMs();
    for (const [token, data] of this.tokens.entries()) {
      if (now > data.expiresAt) {
        this.tokens.delete(token);
      }
    }
  }

  /**
   * Reset store (for testing)
   */
  reset(): void {
    this.tokens.clear();
  }

  /**
   * Get token count (for testing)
   */
  size(): number {
    return this.tokens.size;
  }

  /**
   * Check if token exists (for testing)
   */
  has(token: string): boolean {
    return this.tokens.has(token);
  }
}

// Singleton instance
export const confirmationStore = new ConfirmationStore();
