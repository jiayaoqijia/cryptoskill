import { describe, it, expect, beforeEach, vi } from 'vitest';
import { ConfirmationInvalidError, ConfirmationRequiredError } from '../errors.js';

// Track mock time
let mockTime = Date.now();

// Mock the env module
vi.mock('../env.js', () => ({
  getConfig: () => ({
    ELSA_CONFIRMATION_TTL_SECONDS: 600,
    ELSA_REQUIRE_CONFIRMATION_TOKEN: true,
  }),
  isConfirmationRequired: () => true,
  getConfirmationTtlMs: () => 600_000,
}));

// Mock util module
vi.mock('../util.js', () => ({
  nowMs: () => mockTime,
  generateToken: () => `test-token-${Math.random().toString(36).slice(2)}`,
  normalizeSwapParams: (params: any) => ({
    from_chain: params.from_chain.trim().toLowerCase(),
    from_token: params.from_token.trim().toLowerCase(),
    from_amount: params.from_amount.trim(),
    to_chain: params.to_chain.trim().toLowerCase(),
    to_token: params.to_token.trim().toLowerCase(),
    wallet_address: params.wallet_address.trim().toLowerCase(),
    slippage: params.slippage,
  }),
  hashParams: (params: any) => {
    const json = JSON.stringify(params);
    // Simple hash for testing
    let hash = 0;
    for (let i = 0; i < json.length; i++) {
      const char = json.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash;
    }
    return hash.toString(16);
  },
}));

// Import after mocks
import { confirmationStore } from '../confirm.js';

describe('confirmationStore', () => {
  const validParams = {
    from_chain: 'base',
    from_token: '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
    from_amount: '100',
    to_chain: 'base',
    to_token: '0x4200000000000000000000000000000000000006',
    wallet_address: '0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045',
    slippage: 0.5,
  };

  beforeEach(() => {
    confirmationStore.reset();
    mockTime = Date.now();
  });

  describe('issueToken', () => {
    it('should issue a token for valid params', () => {
      const token = confirmationStore.issueToken(validParams);
      expect(token).toBeTruthy();
      expect(typeof token).toBe('string');
      expect(token.length).toBeGreaterThan(10);
    });

    it('should store the token', () => {
      const token = confirmationStore.issueToken(validParams);
      expect(confirmationStore.has(token)).toBe(true);
      expect(confirmationStore.size()).toBe(1);
    });

    it('should issue unique tokens for each call', () => {
      const token1 = confirmationStore.issueToken(validParams);
      const token2 = confirmationStore.issueToken(validParams);
      expect(token1).not.toBe(token2);
      expect(confirmationStore.size()).toBe(2);
    });
  });

  describe('validateAndConsume', () => {
    it('should validate and consume a valid token', () => {
      const token = confirmationStore.issueToken(validParams);

      const result = confirmationStore.validateAndConsume(token, validParams);

      expect(result).toBe(true);
      expect(confirmationStore.has(token)).toBe(false);
    });

    it('should throw for non-existent token', () => {
      expect(() =>
        confirmationStore.validateAndConsume('non-existent-token', validParams)
      ).toThrow(ConfirmationInvalidError);
    });

    it('should throw for expired token', () => {
      const token = confirmationStore.issueToken(validParams);

      // Advance time past TTL (600 seconds = 600000 ms)
      mockTime = mockTime + 601_000;

      expect(() =>
        confirmationStore.validateAndConsume(token, validParams)
      ).toThrow(ConfirmationInvalidError);
    });

    it('should throw for params mismatch', () => {
      const token = confirmationStore.issueToken(validParams);

      const differentParams = {
        ...validParams,
        from_amount: '200', // Different amount
      };

      expect(() =>
        confirmationStore.validateAndConsume(token, differentParams)
      ).toThrow(ConfirmationInvalidError);
    });

    it('should be one-time use (second use fails)', () => {
      const token = confirmationStore.issueToken(validParams);

      // First use succeeds
      confirmationStore.validateAndConsume(token, validParams);

      // Second use fails
      expect(() =>
        confirmationStore.validateAndConsume(token, validParams)
      ).toThrow(ConfirmationInvalidError);
    });

    it('should normalize params for comparison', () => {
      const token = confirmationStore.issueToken(validParams);

      // Params with different casing/whitespace should still match
      const normalizedEquivalent = {
        from_chain: '  BASE  ',
        from_token: '0x833589FCD6EDB6E08F4C7C32D4F71B54BDA02913',
        from_amount: '100',
        to_chain: 'BASE',
        to_token: '0x4200000000000000000000000000000000000006',
        wallet_address: '0xD8DA6BF26964AF9D7EED9E03E53415D37AA96045',
        slippage: 0.5,
      };

      const result = confirmationStore.validateAndConsume(token, normalizedEquivalent);
      expect(result).toBe(true);
    });
  });

  describe('requireConfirmation', () => {
    it('should pass when token is valid', () => {
      const token = confirmationStore.issueToken(validParams);

      expect(() =>
        confirmationStore.requireConfirmation(token, validParams)
      ).not.toThrow();
    });

    it('should throw ConfirmationRequiredError when token is undefined', () => {
      expect(() =>
        confirmationStore.requireConfirmation(undefined, validParams)
      ).toThrow(ConfirmationRequiredError);
    });

    it('should throw ConfirmationInvalidError for invalid token', () => {
      expect(() =>
        confirmationStore.requireConfirmation('invalid-token', validParams)
      ).toThrow(ConfirmationInvalidError);
    });
  });

  describe('cleanup', () => {
    it('should clean up expired tokens when issuing new ones', () => {
      // Issue first token
      const token1 = confirmationStore.issueToken(validParams);
      expect(confirmationStore.size()).toBe(1);

      // Advance time past TTL
      mockTime = mockTime + 601_000;

      // Issue second token (should trigger cleanup)
      const token2 = confirmationStore.issueToken(validParams);

      // First token should be cleaned up, only second remains
      expect(confirmationStore.has(token1)).toBe(false);
      expect(confirmationStore.has(token2)).toBe(true);
      expect(confirmationStore.size()).toBe(1);
    });
  });
});
