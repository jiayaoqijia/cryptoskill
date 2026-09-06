import { afterEach, beforeEach, describe, expect, test } from 'bun:test';
import { clearTokenCache, getAccessToken } from '../../src/core/auth.js';
import { resetConfigCache } from '../../src/core/config.js';
import { restoreTestEnv, resetTestEnv } from '../helpers/env.js';
import { installFetchMock, jsonResponse, textResponse } from '../helpers/mock-fetch.js';

describe('auth', () => {
  let restoreFetch: (() => void) | undefined;

  beforeEach(() => {
    resetTestEnv({
      TMRW_PRIVATE_KEY: undefined,
      TMRW_CA_HASH: undefined,
      TMRW_AUTH_BASE: 'https://api.tmrwdao.com',
      TMRW_AUTH_CHAIN_ID: 'AELF',
      TMRW_SOURCE: 'nightElf',
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

  test('requires private key', async () => {
    await expect(getAccessToken()).rejects.toMatchObject({
      code: 'AUTH_PRIVATE_KEY_REQUIRED',
    });
  });

  test('gets access token and hits cache', async () => {
    resetTestEnv({
      TMRW_PRIVATE_KEY: '1'.repeat(64),
      TMRW_AUTH_BASE: 'https://api.tmrwdao.com',
    });
    resetConfigCache();

    const mocked = installFetchMock(() => {
      return jsonResponse({
        access_token: 'token-1',
        token_type: 'Bearer',
        expires_in: 120,
      });
    });
    restoreFetch = mocked.restore;

    const first = await getAccessToken();
    const second = await getAccessToken();

    expect(first.accessToken).toBe('token-1');
    expect(second.accessToken).toBe('token-1');
    expect(mocked.calls.length).toBe(1);
  });

  test('force refresh bypasses cache', async () => {
    resetTestEnv({ TMRW_PRIVATE_KEY: '1'.repeat(64) });
    resetConfigCache();

    let count = 0;
    const mocked = installFetchMock(() => {
      count += 1;
      return jsonResponse({
        access_token: `token-${count}`,
        token_type: 'Bearer',
        expires_in: 120,
      });
    });
    restoreFetch = mocked.restore;

    const first = await getAccessToken();
    const second = await getAccessToken(true);

    expect(first.accessToken).toBe('token-1');
    expect(second.accessToken).toBe('token-2');
    expect(mocked.calls.length).toBe(2);
  });

  test('force refresh failure clears stale cache', async () => {
    resetTestEnv({ TMRW_PRIVATE_KEY: '1'.repeat(64) });
    resetConfigCache();

    let call = 0;
    const mocked = installFetchMock(() => {
      call += 1;
      if (call === 1) {
        return jsonResponse({
          access_token: 'token-ok',
          token_type: 'Bearer',
          expires_in: 120,
        });
      }
      return textResponse('upstream failed', 500);
    });
    restoreFetch = mocked.restore;

    const first = await getAccessToken();
    expect(first.accessToken).toBe('token-ok');

    await expect(getAccessToken(true)).rejects.toMatchObject({
      code: 'AUTH_HTTP_ERROR',
    });

    // After failed refresh, next call should fetch again instead of using stale cache.
    await expect(getAccessToken()).rejects.toMatchObject({
      code: 'AUTH_HTTP_ERROR',
    });
    expect(call).toBe(3);
  });

  test('returns AUTH_HTTP_ERROR on non-2xx response', async () => {
    resetTestEnv({ TMRW_PRIVATE_KEY: '1'.repeat(64) });
    resetConfigCache();

    const mocked = installFetchMock(() => textResponse('bad request', 500));
    restoreFetch = mocked.restore;

    await expect(getAccessToken()).rejects.toMatchObject({
      code: 'AUTH_HTTP_ERROR',
    });
  });

  test('returns AUTH_RESPONSE_INVALID when fields are missing', async () => {
    resetTestEnv({ TMRW_PRIVATE_KEY: '1'.repeat(64) });
    resetConfigCache();

    const mocked = installFetchMock(() =>
      jsonResponse({
        token_type: 'Bearer',
      }),
    );
    restoreFetch = mocked.restore;

    await expect(getAccessToken()).rejects.toMatchObject({
      code: 'AUTH_RESPONSE_INVALID',
    });
  });

  test('includes ca_hash when configured', async () => {
    resetTestEnv({
      TMRW_PRIVATE_KEY: '1'.repeat(64),
      TMRW_CA_HASH: 'ca-hash-1',
    });
    resetConfigCache();

    let requestBody = '';
    const mocked = installFetchMock((_url, init) => {
      requestBody = String(init?.body || '');
      return jsonResponse({
        access_token: 'token-ca',
        token_type: 'Bearer',
        expires_in: 120,
      });
    });
    restoreFetch = mocked.restore;

    const token = await getAccessToken();

    expect(token.accessToken).toBe('token-ca');
    expect(requestBody.includes('ca_hash=ca-hash-1')).toBeTrue();
  });
});
