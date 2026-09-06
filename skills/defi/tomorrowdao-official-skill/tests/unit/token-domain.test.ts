import { afterEach, beforeEach, describe, expect, test } from 'bun:test';
import { clearTokenCache } from '../../src/core/auth.js';
import { resetConfigCache } from '../../src/core/config.js';
import {
  daoTokenAllowanceView,
  daoTokenBalanceView,
} from '../../src/domains/dao.js';
import {
  tokenApprove,
  tokenAllowanceView,
  tokenBalanceView,
} from '../../src/domains/token.js';
import { restoreTestEnv, resetTestEnv } from '../helpers/env.js';

describe('token domain', () => {
  beforeEach(() => {
    resetTestEnv({
      TMRW_PRIVATE_KEY: '1'.repeat(64),
      TMRW_CHAIN_DEFAULT_DAO: 'tDVV',
    });
    clearTokenCache();
    resetConfigCache();
  });

  afterEach(() => {
    clearTokenCache();
    resetConfigCache();
    restoreTestEnv();
  });

  test('returns fail result for generic token allowance on unsupported chain', async () => {
    const result = await tokenAllowanceView({
      chainId: 'UNKNOWN' as any,
      symbol: 'ELF',
      owner: 'owner',
      spender: 'spender',
    });

    expect(result.success).toBeFalse();
    expect(result.error?.code).toBe('UNSUPPORTED_CHAIN');
  });

  test('returns fail result for generic token balance on unsupported chain', async () => {
    const result = await tokenBalanceView({
      chainId: 'UNKNOWN' as any,
      symbol: 'ELF',
      owner: 'owner',
    });

    expect(result.success).toBeFalse();
    expect(result.error?.code).toBe('UNSUPPORTED_CHAIN');
  });

  test('supports token approve simulate payload', async () => {
    const result = await tokenApprove({
      chainId: 'tDVV',
      args: {
        spender: 'spender-1',
        symbol: 'AIBOUNTY',
        amount: 200000000,
      },
      mode: 'simulate',
    });

    expect(result.success).toBeTrue();
    expect((result.data as any).contractAddress).toBe('7RzVGiuVWkvL4VfVHdZfQF2Tri3sgLe9U991bohHFfSRZXuGX');
    expect((result.data as any).methodName).toBe('Approve');
    expect((result.data as any).args).toEqual({
      spender: 'spender-1',
      symbol: 'AIBOUNTY',
      amount: 200000000,
    });
  });

  test('returns fail result when token approve send resolves to CA signer', async () => {
    resetTestEnv({
      TMRW_PRIVATE_KEY: '1'.repeat(64),
      PORTKEY_CA_HASH: 'ca_hash_1',
      PORTKEY_CA_ADDRESS: 'ELF_ca_1_AELF',
      TMRW_CHAIN_DEFAULT_DAO: 'tDVV',
    });
    clearTokenCache();
    resetConfigCache();

    const result = await tokenApprove({
      chainId: 'tDVV',
      args: {
        spender: 'spender-1',
        symbol: 'AIBOUNTY',
        amount: 200000000,
      },
      mode: 'send',
    });

    expect(result.success).toBeFalse();
    expect(result.error?.code).toBe('SIGNER_CA_DIRECT_SEND_FORBIDDEN');
  });

  test('dao token aliases keep generic token helper behavior', async () => {
    const genericBalance = await tokenBalanceView({
      chainId: 'UNKNOWN' as any,
      symbol: 'ELF',
      owner: 'owner',
    });
    const daoBalance = await daoTokenBalanceView({
      chainId: 'UNKNOWN' as any,
      symbol: 'ELF',
      owner: 'owner',
    });
    const genericAllowance = await tokenAllowanceView({
      chainId: 'UNKNOWN' as any,
      symbol: 'ELF',
      owner: 'owner',
      spender: 'spender',
    });
    const daoAllowance = await daoTokenAllowanceView({
      chainId: 'UNKNOWN' as any,
      symbol: 'ELF',
      owner: 'owner',
      spender: 'spender',
    });

    expect(daoBalance).toEqual(genericBalance);
    expect(daoAllowance).toEqual(genericAllowance);
  });
});
