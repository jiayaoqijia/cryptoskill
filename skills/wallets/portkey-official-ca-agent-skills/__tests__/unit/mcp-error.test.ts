import { describe, expect, test } from 'bun:test';
import { fail, toMcpError } from '../../src/mcp/error.js';

describe('mcp error helpers', () => {
  test('uses explicit string code when present', () => {
    const parsed = toMcpError({
      code: 'EXTERNAL_SERVICE_ERROR',
      message: 'service unavailable',
      details: { retryable: true },
      traceId: 'trace-1',
    });
    expect(parsed.code).toBe('EXTERNAL_SERVICE_ERROR');
    expect(parsed.message).toBe('service unavailable');
    expect(parsed.traceId).toBe('trace-1');
  });

  test('extracts prefixed code only when in allowlist', () => {
    const parsed = toMcpError(
      new Error('SIGNER_CONTEXT_NOT_FOUND: no signer available'),
    );
    expect(parsed.code).toBe('SIGNER_CONTEXT_NOT_FOUND');
    expect(parsed.message).toBe('no signer available');
  });

  test('does not extract non-whitelisted prefix from message', () => {
    const parsed = toMcpError(new Error('HTTP: connection refused'));
    expect(parsed.code).toBe('UNKNOWN_ERROR');
    expect(parsed.message).toBe('HTTP: connection refused');
  });

  test('handles primitive and nullish values', () => {
    expect(toMcpError('boom').message).toBe('boom');
    expect(toMcpError(null).code).toBe('UNKNOWN_ERROR');
  });

  test('fail returns legacy + structured payload', () => {
    const result = fail(
      new Error('SIGNER_PASSWORD_REQUIRED: active CA context found'),
    );
    expect(result.isError).toBeTrue();
    expect(result.content[0]?.text).toBe(
      '[ERROR] SIGNER_PASSWORD_REQUIRED: active CA context found',
    );
    const parsed = JSON.parse(result.content[1]?.text || '{}');
    expect(parsed.error.code).toBe('SIGNER_PASSWORD_REQUIRED');
    expect(parsed.error.message).toBe('active CA context found');
  });
});
