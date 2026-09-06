import { afterEach, beforeEach, describe, expect, test } from 'bun:test';
import { clearTokenCache } from '../../src/core/auth.js';
import { resetConfigCache } from '../../src/core/config.js';
import {
  resourceBuy,
  resourceRecords,
  resourceRealtimeRecords,
  resourceSell,
  resourceTurnover,
} from '../../src/domains/resource.js';
import { restoreTestEnv, resetTestEnv } from '../helpers/env.js';
import { installFetchMock, jsonResponse } from '../helpers/mock-fetch.js';

describe('resource domain', () => {
  let restoreFetch: (() => void) | undefined;

  beforeEach(() => {
    resetTestEnv({
      TMRW_API_BASE: 'https://api.tmrwdao.com',
      TMRW_CHAIN_DEFAULT_NETWORK: 'AELF',
    });
    clearTokenCache();
    resetConfigCache();
  });

  afterEach(() => {
    if (restoreFetch) restoreFetch();
    clearTokenCache();
    resetConfigCache();
    restoreTestEnv();
  });

  test('supports simulate buy/sell', async () => {
    const buy = await resourceBuy({ chainId: 'AELF', symbol: 'CPU', amount: 1, mode: 'simulate' });
    const sell = await resourceSell({ chainId: 'AELF', symbol: 'CPU', amount: 1, mode: 'simulate' });

    expect(buy.success).toBeTrue();
    expect(sell.success).toBeTrue();
  });

  test('supports read-only resource APIs', async () => {
    const mocked = installFetchMock((url) => {
      if (url.includes('/resource/realtime-records')) {
        return jsonResponse({ code: '20000', data: { items: [] } });
      }
      if (url.includes('/resource/turnover')) {
        return jsonResponse({ code: '20000', data: { symbol: 'CPU', value: '1' } });
      }
      if (url.includes('/resource/records')) {
        return jsonResponse({ code: '20000', data: { items: [] } });
      }
      return jsonResponse({ code: '20000', data: {} });
    });
    restoreFetch = mocked.restore;

    const realtime = await resourceRealtimeRecords({ chainId: 'AELF', maxResultCount: 5 });
    const turnover = await resourceTurnover({ chainId: 'AELF', symbol: 'CPU' });
    const records = await resourceRecords({ chainId: 'AELF', symbol: 'CPU', maxResultCount: 5 });

    expect(realtime.success).toBeTrue();
    expect(turnover.success).toBeTrue();
    expect(records.success).toBeTrue();
  });

  test('returns fail result on business error and unsupported chain', async () => {
    const mocked = installFetchMock((url) => {
      if (url.includes('/resource/records')) {
        return jsonResponse({
          code: '50001',
          message: 'failed',
        });
      }
      return jsonResponse({ code: '20000', data: {} });
    });
    restoreFetch = mocked.restore;

    const apiFail = await resourceRecords({ chainId: 'AELF' });
    const chainFail = await resourceBuy({ chainId: 'tDVV', symbol: 'CPU', amount: 1, mode: 'simulate' });

    expect(apiFail.success).toBeFalse();
    expect(apiFail.error?.code).toBe('API_BUSINESS_ERROR');
    expect(chainFail.success).toBeFalse();
    expect(chainFail.error?.code).toBe('UNSUPPORTED_CHAIN');
  });

  test('validates symbol and amount', async () => {
    const invalidAmount = await resourceBuy({ chainId: 'AELF', symbol: 'CPU', amount: 0, mode: 'simulate' });
    const invalidSymbol = await resourceSell({ chainId: 'AELF', symbol: '', amount: 1, mode: 'simulate' });

    expect(invalidAmount.success).toBeFalse();
    expect(invalidAmount.error?.code).toBe('INVALID_INPUT');
    expect(invalidSymbol.success).toBeFalse();
    expect(invalidSymbol.error?.code).toBe('INVALID_INPUT');
  });
});
