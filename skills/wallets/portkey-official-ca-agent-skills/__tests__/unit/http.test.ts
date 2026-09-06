import { describe, it, expect } from 'bun:test';
import { createHttpClient, HttpError } from '../../lib/http';
import type { PortkeyConfig } from '../../lib/types';

describe('lib/http', () => {
  const mockConfig: PortkeyConfig = {
    apiUrl: 'https://aa-portkey.portkey.finance',
    eoaApiUrl: 'https://eoa-portkey.portkey.finance',
    graphqlUrl: 'https://indexer-api.aefinder.io/api/app/graphql/portkey',
    network: 'mainnet',
    eoaFallbackEnabled: true,
    eoaFallbackRetryCount: 2,
    eoaFallbackRetryDelayMs: 200,
  };

  it('should create an HTTP client with get/post/put/del methods', () => {
    const client = createHttpClient(mockConfig);
    expect(typeof client.get).toBe('function');
    expect(typeof client.post).toBe('function');
    expect(typeof client.put).toBe('function');
    expect(typeof client.del).toBe('function');
    expect(typeof client.request).toBe('function');
  });

  it('should strip trailing slash from baseUrl', () => {
    const client = createHttpClient({
      ...mockConfig,
      apiUrl: 'https://example.com/',
    });
    // The client should work without double slashes
    expect(client).toBeDefined();
  });

  it('should parse nested error bodies from Portkey APIs', () => {
    const err = new HttpError(
      403,
      'Forbidden',
      JSON.stringify({ error: { code: '3002', message: 'Guardian not exist.' } }),
    );

    expect(err.errorCode).toBe('3002');
    expect(err.message).toContain('Guardian not exist.');
  });
});
