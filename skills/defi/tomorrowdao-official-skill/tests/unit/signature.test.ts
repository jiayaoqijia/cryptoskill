import { describe, expect, test } from 'bun:test';
import { buildLegacyTimestampSignature, buildSignaturePayload } from '../../src/core/signature.js';

describe('signature', () => {
  const privateKey = '1'.repeat(64);

  test('builds auth signature payload', () => {
    const payload = buildSignaturePayload(privateKey, 1700000000000);
    expect(payload.address.length).toBeGreaterThan(10);
    expect(payload.publicKey.length).toBeGreaterThan(60);
    expect(payload.signature.length).toBe(130);
  });

  test('builds legacy timestamp signature', () => {
    const payload = buildLegacyTimestampSignature(privateKey, 1700000000000);
    expect(payload.signature.length).toBe(130);
  });
});
