import { afterEach, describe, expect, test } from 'bun:test';
import { search } from '../../src/core/search.js';

const originalFetch = globalThis.fetch;

afterEach(() => {
  globalThis.fetch = originalFetch;
});

describe('search core', () => {
  test('calls search endpoint with expected query fields', async () => {
    let requestUrl = '';

    globalThis.fetch = (async (input: RequestInfo | URL) => {
      requestUrl = String(input);
      return new Response(
        JSON.stringify({
          code: '20000',
          data: {
            tokens: [],
            nfts: [],
            accounts: [],
            contracts: [],
            blocks: [],
            block: {},
            transaction: null,
          },
          message: '',
        }),
        { status: 200, headers: { 'Content-Type': 'application/json' } },
      );
    }) as typeof fetch;

    const result = await search({
      chainId: 'AELF',
      keyword: 'ELF',
      filterType: 0,
      searchType: 0,
    });

    expect(result.success).toBe(true);
    expect(requestUrl.includes('/api/app/blockchain/search')).toBe(true);
    expect(requestUrl.includes('chainId=AELF')).toBe(true);
    expect(requestUrl.includes('keyword=ELF')).toBe(true);
  });

  test('returns input error when keyword is missing', async () => {
    const result = await search({
      chainId: 'AELF',
      keyword: '',
    });

    expect(result.success).toBe(false);
    expect(result.error?.code).toBe('INVALID_INPUT');
  });
});
