import { afterEach, describe, expect, test } from 'bun:test';
import { getBlocks } from '../../src/core/blockchain.js';

const originalFetch = globalThis.fetch;

afterEach(() => {
  globalThis.fetch = originalFetch;
});

describe('tool result shape', () => {
  test('returns traceId/success/raw on success', async () => {
    globalThis.fetch = (async () => {
      return new Response(
        JSON.stringify({
          code: '20000',
          data: {
            total: 0,
            blocks: [],
          },
          message: '',
        }),
        { status: 200, headers: { 'Content-Type': 'application/json' } },
      );
    }) as unknown as typeof fetch;

    const result = await getBlocks({ chainId: 'AELF', maxResultCount: 1, skipCount: 0 });
    expect(result.success).toBe(true);
    expect(typeof result.traceId).toBe('string');
    expect(result.traceId.length > 5).toBe(true);
    expect(result.raw).toBeDefined();
  });

  test('returns normalized failure shape', async () => {
    globalThis.fetch = (async () => {
      return new Response('bad request', { status: 400 });
    }) as unknown as typeof fetch;

    const result = await getBlocks({ chainId: 'AELF' });
    expect(result.success).toBe(false);
    expect(result.error?.code).toBe('HTTP_ERROR');
    expect(typeof result.traceId).toBe('string');
  });

  test('propagates traceId to request header', async () => {
    let traceHeader = '';

    globalThis.fetch = (async (_input: RequestInfo | URL, init?: RequestInit) => {
      const headers = new Headers(init?.headers);
      traceHeader = headers.get('X-Trace-Id') || '';

      return new Response(
        JSON.stringify({
          code: '20000',
          data: {
            total: 0,
            blocks: [],
          },
          message: '',
        }),
        { status: 200, headers: { 'Content-Type': 'application/json' } },
      );
    }) as unknown as typeof fetch;

    const result = await getBlocks({ chainId: 'AELF', maxResultCount: 1, skipCount: 0 });

    expect(result.success).toBe(true);
    expect(traceHeader).toBe(result.traceId);
  });
});
