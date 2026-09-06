import { afterEach, beforeEach, describe, expect, test } from 'bun:test';
import { resetConfigCache } from '../../lib/config.js';
import { getBlocks } from '../../src/core/blockchain.js';

const originalFetch = globalThis.fetch;
const originalMaxResultCountEnv = process.env.AELFSCAN_MAX_RESULT_COUNT;

beforeEach(() => {
  resetConfigCache();
});

afterEach(() => {
  globalThis.fetch = originalFetch;
  if (originalMaxResultCountEnv === undefined) {
    delete process.env.AELFSCAN_MAX_RESULT_COUNT;
  } else {
    process.env.AELFSCAN_MAX_RESULT_COUNT = originalMaxResultCountEnv;
  }
  resetConfigCache();
});

describe('pagination guard', () => {
  test('clamps maxResultCount to configured upper limit', async () => {
    process.env.AELFSCAN_MAX_RESULT_COUNT = '200';
    resetConfigCache();

    let requestUrl = '';
    globalThis.fetch = (async (input: RequestInfo | URL) => {
      requestUrl = String(input);
      return new Response(JSON.stringify({ code: '20000', data: { list: [] }, message: '' }), {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
      });
    }) as unknown as typeof fetch;

    const result = await getBlocks({ chainId: 'AELF', maxResultCount: 999, skipCount: 0 });

    expect(result.success).toBe(true);
    expect(requestUrl.includes('maxResultCount=200')).toBe(true);
  });

  test('returns INVALID_INPUT for invalid pagination values', async () => {
    const result = await getBlocks({ chainId: 'AELF', maxResultCount: -1 });

    expect(result.success).toBe(false);
    expect(result.error?.code).toBe('INVALID_INPUT');
  });
});
