import { afterEach, describe, expect, test } from 'bun:test';
import { request } from '../../lib/http-client.js';

const originalFetch = globalThis.fetch;

afterEach(() => {
  globalThis.fetch = originalFetch;
});

describe('http client', () => {
  test('parses envelope response', async () => {
    globalThis.fetch = (async () => {
      return new Response(
        JSON.stringify({
          code: '20000',
          data: { ok: true },
          message: '',
        }),
        { status: 200, headers: { 'Content-Type': 'application/json' } },
      );
    }) as unknown as typeof fetch;

    const result = await request<{ ok: boolean }>({
      path: '/api/app/blockchain/filters',
    });

    expect(result.data.ok).toBe(true);
    expect(result.raw).toBeDefined();
  });

  test('throws for business error', async () => {
    globalThis.fetch = (async () => {
      return new Response(
        JSON.stringify({
          code: '50000',
          data: null,
          message: 'business failure',
        }),
        { status: 200, headers: { 'Content-Type': 'application/json' } },
      );
    }) as unknown as typeof fetch;

    await expect(
      request({
        path: '/api/app/blockchain/filters',
      }),
    ).rejects.toThrow('business failure');
  });
});
