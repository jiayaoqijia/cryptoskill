import { describe, it, expect, beforeEach, afterEach } from 'bun:test';
import { getConfig, NETWORK_DEFAULTS } from '../../lib/config';

describe('lib/config', () => {
  const originalEnv = { ...process.env };

  afterEach(() => {
    // Restore env
    process.env = { ...originalEnv };
  });

  it('should return mainnet config by default', () => {
    delete process.env.PORTKEY_NETWORK;
    delete process.env.PORTKEY_API_URL;
    delete process.env.PORTKEY_EOA_API_URL;
    delete process.env.PORTKEY_EOA_FALLBACK_ENABLED;
    delete process.env.PORTKEY_EOA_FALLBACK_RETRY_COUNT;
    delete process.env.PORTKEY_EOA_FALLBACK_RETRY_DELAY_MS;

    const config = getConfig();
    expect(config.network).toBe('mainnet');
    expect(config.apiUrl).toBe(NETWORK_DEFAULTS.mainnet.apiUrl);
    expect(config.eoaApiUrl).toBe(NETWORK_DEFAULTS.mainnet.eoaApiUrl);
    expect(config.graphqlUrl).toBe(NETWORK_DEFAULTS.mainnet.graphqlUrl);
    expect(config.eoaFallbackEnabled).toBe(true);
    expect(config.eoaFallbackRetryCount).toBe(2);
    expect(config.eoaFallbackRetryDelayMs).toBe(200);
  });

  it('should reject testnet network override', () => {
    expect(() => getConfig({ network: 'testnet' })).toThrow('decommissioned');
  });

  it('should reject PORTKEY_NETWORK=testnet', () => {
    process.env.PORTKEY_NETWORK = 'testnet';
    expect(() => getConfig()).toThrow('decommissioned');
  });

  it('should prioritize function params over env variables', () => {
    process.env.PORTKEY_NETWORK = 'testnet';
    const config = getConfig({ network: 'mainnet' });
    expect(config.network).toBe('mainnet');
  });

  it('should allow apiUrl override via env', () => {
    process.env.PORTKEY_API_URL = 'https://custom-api.example.com';
    const config = getConfig();
    expect(config.apiUrl).toBe('https://custom-api.example.com');
  });

  it('should allow apiUrl override via params', () => {
    const config = getConfig({ apiUrl: 'https://param-api.example.com' });
    expect(config.apiUrl).toBe('https://param-api.example.com');
  });

  it('should allow EOA api override via env and params', () => {
    process.env.PORTKEY_EOA_API_URL = 'https://env-eoa.example.com';
    const fromEnv = getConfig();
    expect(fromEnv.eoaApiUrl).toBe('https://env-eoa.example.com');

    const fromParam = getConfig({ eoaApiUrl: 'https://param-eoa.example.com' });
    expect(fromParam.eoaApiUrl).toBe('https://param-eoa.example.com');
  });

  it('should parse EOA fallback flags and retry env values', () => {
    process.env.PORTKEY_EOA_FALLBACK_ENABLED = 'false';
    process.env.PORTKEY_EOA_FALLBACK_RETRY_COUNT = '3';
    process.env.PORTKEY_EOA_FALLBACK_RETRY_DELAY_MS = '450';

    const config = getConfig();
    expect(config.eoaFallbackEnabled).toBe(false);
    expect(config.eoaFallbackRetryCount).toBe(3);
    expect(config.eoaFallbackRetryDelayMs).toBe(450);
  });

  it('should throw for invalid EOA fallback env values', () => {
    process.env.PORTKEY_EOA_FALLBACK_ENABLED = 'maybe';
    expect(() => getConfig()).toThrow('Invalid boolean value');

    process.env.PORTKEY_EOA_FALLBACK_ENABLED = 'true';
    process.env.PORTKEY_EOA_FALLBACK_RETRY_COUNT = '0';
    expect(() => getConfig()).toThrow('PORTKEY_EOA_FALLBACK_RETRY_COUNT must be an integer >= 1');
  });

  it('should throw on unknown network', () => {
    expect(() => getConfig({ network: 'unknown' as any })).toThrow('Unknown network');
  });

  it('should have correct mainnet defaults', () => {
    expect(NETWORK_DEFAULTS.mainnet.apiUrl).toBe('https://aa-portkey.portkey.finance');
    expect(NETWORK_DEFAULTS.mainnet.eoaApiUrl).toBe('https://eoa-portkey.portkey.finance');
  });
});
