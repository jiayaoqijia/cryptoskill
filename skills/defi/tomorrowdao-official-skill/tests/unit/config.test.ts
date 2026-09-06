import { afterEach, beforeEach, describe, expect, test } from 'bun:test';
import {
  CONTRACTS,
  getConfig,
  getContracts,
  getTokenContractAddress,
  resetConfigCache,
} from '../../src/core/config.js';

const OLD_ENV = { ...process.env };

describe('config', () => {
  beforeEach(() => {
    process.env = { ...OLD_ENV };
    resetConfigCache();
  });

  afterEach(() => {
    process.env = { ...OLD_ENV };
    resetConfigCache();
  });

  test('loads defaults', () => {
    const cfg = getConfig();
    expect(cfg.apiBase).toBe('https://api.tmrwdao.com');
    expect(cfg.defaultDaoChain).toBe('tDVV');
    expect(cfg.defaultNetworkChain).toBe('AELF');
    expect(cfg.httpTimeoutMs).toBe(30000);
    expect(cfg.httpRetryMax).toBe(1);
    expect(cfg.httpRetryPost).toBeFalse();
    expect(cfg.rpc.tDVW).toBe('https://tdvw-test-node.aelf.io');
    expect(CONTRACTS.explorer.tDVW).toBe('https://aelfscan.io/tDVW');
  });

  test('loads env overrides', () => {
    process.env.TMRW_API_BASE = 'https://custom.tmrwdao.com/';
    process.env.TMRW_CHAIN_DEFAULT_DAO = 'AELF';
    process.env.TMRW_HTTP_TIMEOUT_MS = '5000';
    process.env.TMRW_HTTP_RETRY_POST = '1';
    resetConfigCache();
    const cfg = getConfig();
    expect(cfg.apiBase).toBe('https://custom.tmrwdao.com');
    expect(cfg.defaultDaoChain).toBe('AELF');
    expect(cfg.httpTimeoutMs).toBe(5000);
    expect(cfg.httpRetryPost).toBeTrue();
  });

  test('supports contracts and explorer json overrides', () => {
    process.env.TMRW_CONTRACTS_JSON = JSON.stringify({
      network: {
        tDVW: {
          token: 'new-tdvw-token-contract',
        },
      },
      explorer: {
        tDVW: 'https://custom-scan.io/tDVW',
      },
    });
    process.env.TMRW_EXPLORER_JSON = JSON.stringify({
      AELF: 'https://custom-scan.io/AELF',
    });
    resetConfigCache();

    const contracts = getContracts();
    expect(contracts.network.tDVW.token).toBe('new-tdvw-token-contract');
    expect(contracts.explorer.tDVW).toBe('https://custom-scan.io/tDVW');
    expect(contracts.explorer.AELF).toBe('https://custom-scan.io/AELF');
    expect(getTokenContractAddress('tDVW')).toBe('new-tdvw-token-contract');
  });

  test('throws on invalid contracts json', () => {
    process.env.TMRW_CONTRACTS_JSON = '{';
    resetConfigCache();
    expect(() => getConfig()).toThrow(/TMRW_CONTRACTS_JSON is invalid JSON object/);
  });

  test('throws on invalid explorer json', () => {
    process.env.TMRW_EXPLORER_JSON = '[]';
    resetConfigCache();
    expect(() => getConfig()).toThrow(/TMRW_EXPLORER_JSON is invalid JSON object/);
  });
});
