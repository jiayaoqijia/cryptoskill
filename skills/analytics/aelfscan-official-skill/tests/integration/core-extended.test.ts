import { afterEach, describe, expect, test } from 'bun:test';
import { resetHttpClientState } from '../../lib/http-client.js';
import { getBlockchainOverview } from '../../src/core/blockchain.js';
import { getDailyTransactionInfo, getDailyTransactions, getStatisticsByMetric } from '../../src/core/statistics.js';

const originalFetch = globalThis.fetch;

afterEach(() => {
  globalThis.fetch = originalFetch;
  resetHttpClientState();
});

describe('extended core endpoints', () => {
  test('calls blockchain overview with POST body', async () => {
    let requestUrl = '';
    let requestMethod = '';
    let requestBody = '';

    globalThis.fetch = (async (input: RequestInfo | URL, init?: RequestInit) => {
      requestUrl = String(input);
      requestMethod = String(init?.method || '');
      requestBody = String(init?.body || '');

      return new Response(
        JSON.stringify({
          code: '20000',
          data: { transactions: 100 },
          message: '',
        }),
        { status: 200, headers: { 'Content-Type': 'application/json' } },
      );
    }) as typeof fetch;

    const result = await getBlockchainOverview({ chainId: 'AELF' });

    expect(result.success).toBe(true);
    expect(requestUrl.includes('/api/app/blockchain/blockchainOverview')).toBe(true);
    expect(requestMethod).toBe('POST');
    expect(requestBody.includes('"chainId":"AELF"')).toBe(true);
  });

  test('calls statistics daily transactions with query string', async () => {
    let requestUrl = '';

    globalThis.fetch = (async (input: RequestInfo | URL) => {
      requestUrl = String(input);
      return new Response(
        JSON.stringify({
          code: '20000',
          data: { points: [] },
          message: '',
        }),
        { status: 200, headers: { 'Content-Type': 'application/json' } },
      );
    }) as typeof fetch;

    const result = await getDailyTransactions({ chainId: 'AELF' });

    expect(result.success).toBe(true);
    expect(requestUrl.includes('/api/app/statistics/dailyTransactions')).toBe(true);
    expect(requestUrl.includes('chainId=AELF')).toBe(true);
  });

  test('returns input error when date range is missing', async () => {
    const result = await getDailyTransactionInfo({
      chainId: 'AELF',
      startDate: '',
      endDate: '',
    });

    expect(result.success).toBe(false);
    expect(result.error?.code).toBe('INVALID_INPUT');
  });

  test('routes statistics by metric', async () => {
    let requestUrl = '';

    globalThis.fetch = (async (input: RequestInfo | URL) => {
      requestUrl = String(input);
      return new Response(
        JSON.stringify({
          code: '20000',
          data: { list: [] },
          message: '',
        }),
        { status: 200, headers: { 'Content-Type': 'application/json' } },
      );
    }) as typeof fetch;

    const result = await getStatisticsByMetric({
      metric: 'dailyTransactions',
      chainId: 'AELF',
    });

    expect(result.success).toBe(true);
    expect(requestUrl.includes('/api/app/statistics/dailyTransactions')).toBe(true);
  });
});
