import { describe, expect, test } from 'bun:test';
import { validateRpcUrl, HttpError } from '../../lib/http';

// ---------------------------------------------------------------------------
// validateRpcUrl — SSRF protection
// ---------------------------------------------------------------------------

describe('validateRpcUrl', () => {
  test('should accept valid https URL', () => {
    expect(() => validateRpcUrl('https://tdvv-public-node.aelf.io')).not.toThrow();
  });

  test('should accept valid http URL (public nodes)', () => {
    expect(() => validateRpcUrl('http://tdvv-public-node.aelf.io')).not.toThrow();
  });

  test('should reject localhost', () => {
    expect(() => validateRpcUrl('http://localhost:8080')).toThrow(/private/i);
  });

  test('should reject 127.0.0.1', () => {
    expect(() => validateRpcUrl('http://127.0.0.1:8080')).toThrow(/private/i);
  });

  test('should reject 10.x private range', () => {
    expect(() => validateRpcUrl('http://10.0.0.1:8080')).toThrow(/private/i);
  });

  test('should reject 192.168.x private range', () => {
    expect(() => validateRpcUrl('http://192.168.1.1:8080')).toThrow(/private/i);
  });

  test('should reject 172.16-31.x private range', () => {
    expect(() => validateRpcUrl('http://172.16.0.1:8080')).toThrow(/private/i);
    expect(() => validateRpcUrl('http://172.31.255.255:8080')).toThrow(/private/i);
  });

  test('should reject non-http protocols', () => {
    expect(() => validateRpcUrl('ftp://example.com')).toThrow(/protocol/i);
    expect(() => validateRpcUrl('file:///etc/passwd')).toThrow(/protocol/i);
  });

  test('should reject invalid URLs', () => {
    expect(() => validateRpcUrl('not-a-url')).toThrow(/Invalid/i);
  });
});

// ---------------------------------------------------------------------------
// HttpError — structured error
// ---------------------------------------------------------------------------

describe('HttpError', () => {
  test('should parse JSON body with code and message', () => {
    const body = JSON.stringify({ code: '3002', message: 'account not exist' });
    const err = new HttpError(404, 'Not Found', body);
    expect(err.statusCode).toBe(404);
    expect(err.errorCode).toBe('3002');
    expect(err.message).toContain('account not exist');
    expect(err instanceof Error).toBe(true);
  });

  test('should handle non-JSON body gracefully', () => {
    const err = new HttpError(500, 'Internal Server Error', 'raw text');
    expect(err.statusCode).toBe(500);
    expect(err.errorCode).toBeNull();
    expect(err.responseBody).toBe('raw text');
  });
});
