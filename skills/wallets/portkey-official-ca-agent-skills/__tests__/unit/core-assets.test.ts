import { beforeAll, beforeEach, describe, expect, test } from 'bun:test';
import {
  MockHttpError,
  coreMockState,
  installCoreModuleMocks,
  resetCoreMockState,
} from './core-mock-state';

installCoreModuleMocks();

let assets: typeof import('../../src/core/assets.js');
let account: typeof import('../../src/core/account.js');

beforeAll(async () => {
  account = await import('../../src/core/account.js');
  assets = await import('../../src/core/assets.js');
});

beforeEach(() => {
  resetCoreMockState();
  account.clearChainInfoCache();
});

const config = {
  apiUrl: 'https://api',
  eoaApiUrl: 'https://eoa-api',
  graphqlUrl: 'https://gql',
  network: 'mainnet' as const,
  eoaFallbackEnabled: true,
  eoaFallbackRetryCount: 2,
  eoaFallbackRetryDelayMs: 200,
};

describe('core/assets', () => {
  test('getTokenBalance validates required params', async () => {
    await expect(
      assets.getTokenBalance(config, {
        caAddress: '',
        chainId: 'tDVV',
        symbol: 'ELF',
      } as any),
    ).rejects.toThrow('caAddress is required');
  });

  test('getTokenBalance returns decimals from GetTokenInfo and fallback to default decimals', async () => {
    coreMockState.httpGetImpl = async (path: string) => {
      if (path === '/api/app/search/chainsinfoindex') {
        return {
          items: [
            {
              chainId: 'tDVV',
              endPoint: 'https://rpc',
              caContractAddress: 'CA',
              defaultToken: { address: 'TOKEN', decimals: 8 },
            },
          ],
        };
      }
      return {};
    };

    let tokenInfoFailed = false;
    coreMockState.callViewMethodImpl = async (_rpcUrl: string, _contract: string, method: string) => {
      if (method === 'GetBalance') return { symbol: 'ELF', balance: '1000' };
      if (method === 'GetTokenInfo') {
        if (tokenInfoFailed) throw new Error('token info unavailable');
        return { symbol: 'ELF', decimals: 6 };
      }
      return {};
    };

    const withTokenInfo = await assets.getTokenBalance(config, {
      caAddress: 'ELF_addr_tDVV',
      chainId: 'tDVV',
      symbol: 'ELF',
    });
    expect(withTokenInfo.decimals).toBe(6);

    tokenInfoFailed = true;
    const fallback = await assets.getTokenBalance(config, {
      caAddress: 'ELF_addr_tDVV',
      chainId: 'tDVV',
      symbol: 'USDT',
    });
    expect(fallback.decimals).toBe(8);
    expect(fallback.balance).toBe('1000');
  });

  test('getTokenList maps request payload', async () => {
    coreMockState.httpPostImpl = async () => ({ data: [{ symbol: 'ELF' }] });

    const result = await assets.getTokenList(config, {
      caAddressInfos: [{ chainId: 'tDVV', caAddress: 'ELF_addr_tDVV' }],
      skipCount: 1,
      maxResultCount: 2,
    });

    expect(result.data.length).toBe(1);
    expect(result.dataSource).toBe('aa');
    expect(coreMockState.httpCalls[0]?.path).toBe('/api/app/user/assets/token');
  });

  test('getTokenList falls back to EOA on AA 401 when strategy=auto', async () => {
    let tokenPostCount = 0;
    coreMockState.httpPostImpl = async (path: string) => {
      if (path === '/api/app/user/assets/token') {
        tokenPostCount += 1;
        if (tokenPostCount === 1) {
          throw new MockHttpError(401, 'Unauthorized', '');
        }
        return { data: [{ symbol: 'ELF', balance: '1' }], totalRecordCount: 1 };
      }
      return {};
    };
    coreMockState.httpGetImpl = async (path: string) => {
      if (path === '/api/app/search/chainsinfoindex') {
        return { items: [{ chainId: 'AELF' }, { chainId: 'tDVV' }] };
      }
      return {};
    };

    const result = await assets.getTokenList(config, {
      caAddressInfos: [{ chainId: 'tDVV', caAddress: 'ELF_addr_tDVV' }],
      strategy: 'auto',
    });

    expect(result.dataSource).toBe('eoa-fallback');
    expect(tokenPostCount).toBe(2);
    const tokenCalls = coreMockState.httpCalls.filter((call) => call.path === '/api/app/user/assets/token');
    expect(tokenCalls.length).toBe(2);
    expect(tokenCalls[0]?.options?.data?.caAddressInfos?.length).toBe(1);
    expect(tokenCalls[1]?.options?.data?.addressInfos?.length).toBe(2);
    expect(tokenCalls[1]?.options?.data?.addressInfos?.[0]?.address).toBe('ELF_addr_tDVV');
  });

  test('getTokenList supports strategy=eoa and validates strategy', async () => {
    coreMockState.httpGetImpl = async () => ({ items: [{ chainId: 'tDVV' }] });
    coreMockState.httpPostImpl = async () => ({ data: [{ symbol: 'ELF' }], totalRecordCount: 1 });

    const result = await assets.getTokenList(config, {
      caAddressInfos: [{ chainId: 'tDVV', caAddress: 'ELF_addr_tDVV' }],
      strategy: 'eoa',
    });

    expect(result.dataSource).toBe('eoa-direct');
    expect(coreMockState.httpCalls[1]?.options?.data?.addressInfos?.[0]?.address).toBe('ELF_addr_tDVV');

    await expect(
      assets.getTokenList(config, {
        caAddressInfos: [{ chainId: 'tDVV', caAddress: 'ELF_addr_tDVV' }],
        strategy: 'bad' as any,
      }),
    ).rejects.toThrow('strategy must be one of');
  });

  test('getTokenList does not fallback when eoaFallbackEnabled=false', async () => {
    coreMockState.httpPostImpl = async () => {
      throw new MockHttpError(401, 'Unauthorized', '');
    };

    const params = {
      caAddressInfos: [{ chainId: 'tDVV' as const, caAddress: 'ELF_addr_tDVV' }],
      strategy: 'auto' as const,
    };

    await expect(
      assets.getTokenList(
        { ...config, eoaFallbackEnabled: false },
        params,
      ),
    ).rejects.toThrow('EOA fallback is disabled');
    await expect(
      assets.getTokenList(
        { ...config, eoaFallbackEnabled: false },
        params,
      ),
    ).rejects.toThrow('PORTKEY_EOA_FALLBACK_ENABLED=true');
    await expect(
      assets.getTokenList(
        { ...config, eoaFallbackEnabled: false },
        params,
      ),
    ).rejects.toThrow("strategy='eoa'");
  });

  test('getTokenList retries EOA request on transient upstream errors', async () => {
    let tokenPostCount = 0;
    coreMockState.httpPostImpl = async (path: string) => {
      if (path === '/api/app/user/assets/token') {
        tokenPostCount += 1;
        if (tokenPostCount === 1) {
          throw new MockHttpError(401, 'Unauthorized', '');
        }
        if (tokenPostCount === 2) {
          throw new MockHttpError(500, 'Server Error', '');
        }
        return { data: [{ symbol: 'ELF' }], totalRecordCount: 1 };
      }
      return {};
    };
    coreMockState.httpGetImpl = async () => ({ items: [{ chainId: 'tDVV' }] });

    const result = await assets.getTokenList(config, {
      caAddressInfos: [{ chainId: 'tDVV', caAddress: 'ELF_addr_tDVV' }],
      strategy: 'auto',
    });

    expect(result.dataSource).toBe('eoa-fallback');
    expect(tokenPostCount).toBe(3);
  });

  test('getNftCollections and getNftItems validate params and return data', async () => {
    await expect(
      assets.getNftCollections(config, { caAddressInfos: [] as any[] }),
    ).rejects.toThrow('caAddressInfos is required');

    coreMockState.httpPostImpl = async () => ({ data: [{ symbol: 'COLL' }] });
    const coll = await assets.getNftCollections(config, {
      caAddressInfos: [{ chainId: 'tDVV', caAddress: 'ELF_addr_tDVV' }],
    });
    expect(coll.data.length).toBe(1);

    await expect(
      assets.getNftItems(config, {
        caAddressInfos: [{ chainId: 'tDVV', caAddress: 'ELF_addr_tDVV' }],
        symbol: '',
      } as any),
    ).rejects.toThrow('symbol is required');

    coreMockState.httpPostImpl = async () => ({ data: [{ tokenId: '1' }] });
    const items = await assets.getNftItems(config, {
      caAddressInfos: [{ chainId: 'tDVV', caAddress: 'ELF_addr_tDVV' }],
      symbol: 'COLL',
    });
    expect(items.data[0]?.tokenId).toBe('1');
  });

  test('getTokenPrice validates symbols and returns items or empty array', async () => {
    await expect(
      assets.getTokenPrice(config, { symbols: [] }),
    ).rejects.toThrow('symbols is required');

    coreMockState.httpGetImpl = async () => ({ items: [{ symbol: 'ELF', usd: 1 }] });
    const prices = await assets.getTokenPrice(config, { symbols: ['ELF'] });
    expect(prices.length).toBe(1);

    coreMockState.httpGetImpl = async () => ({ items: undefined });
    const empty = await assets.getTokenPrice(config, { symbols: ['USDT'] });
    expect(empty).toEqual([]);
  });
});
