import { beforeAll, beforeEach, describe, expect, test, mock } from 'bun:test';
import BigNumber from 'bignumber.js';

type MockState = {
  axiosCalls: Array<{ url: string; params?: any }>;
  axiosGetImpl: (url: string, options?: any) => Promise<any>;
  getTokenInfoImpl: (rpcUrl: string, tokenContract: string, symbol: string) => Promise<any>;
  getBalanceImpl: (...args: any[]) => Promise<string>;
  getAllowanceImpl: (...args: any[]) => Promise<string>;
  callViewMethodImpl: (...args: any[]) => Promise<any>;
};

const defaultState = (): MockState => ({
  axiosCalls: [],
  axiosGetImpl: async () => ({ data: { data: {} } }),
  getTokenInfoImpl: async (_rpcUrl: string, _tokenContract: string, symbol: string) => ({
    symbol,
    decimals: symbol === 'USDT' ? 6 : 8,
  }),
  getBalanceImpl: async () => '0',
  getAllowanceImpl: async () => '0',
  callViewMethodImpl: async () => ({ amount: '0' }),
});

const g = globalThis as any;
const state: MockState = g.__AWAKEN_QUERY_MOCK_STATE || (g.__AWAKEN_QUERY_MOCK_STATE = defaultState());

function resetState() {
  const d = defaultState();
  state.axiosCalls = d.axiosCalls;
  state.axiosGetImpl = d.axiosGetImpl;
  state.getTokenInfoImpl = d.getTokenInfoImpl;
  state.getBalanceImpl = d.getBalanceImpl;
  state.getAllowanceImpl = d.getAllowanceImpl;
  state.callViewMethodImpl = d.callViewMethodImpl;
}

mock.module('axios', () => ({
  default: {
    get: async (url: string, options?: any) => {
      state.axiosCalls.push({ url, params: options?.params });
      return state.axiosGetImpl(url, options);
    },
  },
  get: async (url: string, options?: any) => {
    state.axiosCalls.push({ url, params: options?.params });
    return state.axiosGetImpl(url, options);
  },
}));

mock.module('../../lib/aelf-client', () => ({
  callViewMethod: (...args: any[]) => (state.callViewMethodImpl as any)(...args),
  getBalance: (...args: any[]) => (state.getBalanceImpl as any)(...args),
  getAllowance: (...args: any[]) => (state.getAllowanceImpl as any)(...args),
  getTokenInfo: (...args: any[]) => (state.getTokenInfoImpl as any)(...args),
  divDecimals: (value: string | number, decimals: number) =>
    new BigNumber(value).div(new BigNumber(10).pow(decimals)),
}));

let queryCore: typeof import('../../src/core/query');

const config = {
  chainId: 'tDVV',
  rpcUrl: 'https://rpc.mock',
  apiBaseUrl: 'https://api.mock',
  socketUrl: 'https://socket.mock',
  explorerUrl: 'https://explorer.mock',
  tokenContract: 'TOKEN_CONTRACT',
  swapHookContract: 'SWAP_HOOK',
  router: { '0.3': 'ROUTER_03' },
  factory: { '0.3': 'FACTORY_03' },
} as any;

beforeAll(async () => {
  queryCore = await import('../../src/core/query');
});

beforeEach(() => {
  resetState();
});

describe('core/query mocked', () => {
  test('getQuote routeType=0 with amountIn branch', async () => {
    state.axiosGetImpl = async () => ({
      data: {
        data: {
          routes: [
            {
              amountIn: '100000000',
              amountOut: '2500000',
              splits: 1,
              distributions: [
                {
                  percent: 100,
                  amountIn: '100000000',
                  amountOut: '2500000',
                  tokens: [{ symbol: 'ELF' }, { symbol: 'USDT' }],
                  feeRates: [0.3],
                },
              ],
            },
          ],
        },
      },
    });

    const result = await queryCore.getQuote(config, {
      symbolIn: 'ELF',
      symbolOut: 'USDT',
      amountIn: '1',
    });

    expect(state.axiosCalls[0]?.params?.routeType).toBe(0);
    expect(state.axiosCalls[0]?.params?.amountIn).toBe('100000000');
    expect(result).toMatchObject({
      amountIn: '1',
      amountOut: '2.5',
      splits: 1,
    });
    expect(result.distributions[0]).toMatchObject({
      amountIn: '1',
      amountOut: '2.5',
    });
  });

  test('getQuote routeType=1 with amountOut branch and throws on no route', async () => {
    state.axiosGetImpl = async () => ({
      data: {
        data: {
          routes: [
            {
              amountIn: '300000000',
              amountOut: '5000000',
              splits: 1,
              distributions: [
                {
                  percent: 100,
                  amountIn: '300000000',
                  amountOut: '5000000',
                  tokens: [{ symbol: 'ELF' }, { symbol: 'USDT' }],
                  feeRates: [0.3],
                },
              ],
            },
          ],
        },
      },
    });

    const ok = await queryCore.getQuote(config, {
      symbolIn: 'ELF',
      symbolOut: 'USDT',
      amountOut: '5',
    });
    expect(state.axiosCalls[0]?.params?.routeType).toBe(1);
    expect(state.axiosCalls[0]?.params?.amountOut).toBe('5000000');
    expect(ok.amountOut).toBe('5');

    state.axiosGetImpl = async () => ({ data: { data: { routes: [] } } });
    await expect(
      queryCore.getQuote(config, {
        symbolIn: 'ELF',
        symbolOut: 'USDT',
        amountIn: '1',
      }),
    ).rejects.toThrow('No swap route found');
  });

  test('getPair throws when no pair found', async () => {
    state.axiosGetImpl = async () => ({ data: { data: { items: [] } } });

    await expect(
      queryCore.getPair(config, {
        token0: 'ELF',
        token1: 'USDT',
        feeRate: '0.3',
      }),
    ).rejects.toThrow('No trade pair found');
  });

  test('getPair returns first pair when list exists', async () => {
    state.axiosGetImpl = async () => ({
      data: {
        data: {
          items: [
            { id: 'pair-1', price: 2.35 },
            { id: 'pair-2', price: 2.5 },
          ],
        },
      },
    });

    const pair = await queryCore.getPair(config, {
      token0: 'ELF',
      token1: 'USDT',
      feeRate: '0.3',
    });

    expect(pair.id).toBe('pair-1');
    expect(state.axiosCalls[0]?.params?.FeeRate).toBe('0.003');
  });

  test('getTokenBalance and getTokenAllowance normalize decimals', async () => {
    state.getTokenInfoImpl = async (_rpcUrl: string, _tokenContract: string, symbol: string) => ({
      symbol,
      decimals: symbol === 'USDT' ? 6 : 8,
    });
    state.getBalanceImpl = async () => '1234500';
    state.getAllowanceImpl = async () => '4200000';

    const balance = await queryCore.getTokenBalance(config, {
      address: 'ELF_user',
      symbol: 'USDT',
    });
    const allowance = await queryCore.getTokenAllowance(config, {
      owner: 'ELF_owner',
      spender: 'ELF_spender',
      symbol: 'USDT',
    });

    expect(balance.balance).toBe('1.2345');
    expect(allowance.allowance).toBe('4.2');
  });

  test('getLiquidityPositions supports filters and portfolio fallback', async () => {
    state.axiosGetImpl = async (url: string, options?: any) => {
      if (url.endsWith('/api/app/liquidity/user-liquidity')) {
        return {
          data: {
            data: {
              items: [
                {
                  lpTokenAmount: '100',
                  token0Amount: '10',
                  token1Amount: '20',
                  assetUSD: 30,
                  tradePair: {
                    id: 'pair-1',
                    feeRate: '0.003',
                    token0: { symbol: 'ELF', decimals: 8 },
                    token1: { symbol: 'USDT', decimals: 6 },
                  },
                },
                {
                  lpTokenAmount: '50',
                  token0Amount: '5',
                  token1Amount: '5',
                  assetUSD: 10,
                  tradePair: {
                    id: 'pair-2',
                    feeRate: '0.003',
                    token0: { symbol: 'BTC', decimals: 8 },
                    token1: { symbol: 'USDT', decimals: 6 },
                  },
                },
              ],
            },
          },
        };
      }

      if (url.endsWith('/api/app/trade-pairs')) {
        return {
          data: {
            data: {
              items: [{ price: 2.5 }],
            },
          },
        };
      }

      if (url.endsWith('/api/app/liquidity/user-positions')) {
        throw new Error('portfolio endpoint unavailable');
      }

      throw new Error(`unexpected url: ${url} params=${JSON.stringify(options?.params)}`);
    };

    state.callViewMethodImpl = async () => ({ amount: '1234' });

    const result = await queryCore.getLiquidityPositions(config, {
      address: 'ELF_user',
      token0: 'ELF',
    });

    expect(result.totalPositions).toBe(1);
    expect(result.positions[0]).toMatchObject({
      pairId: 'pair-1',
      lpTokenAmountOnChain: '1234',
      pairPrice: 2.5,
    });
    expect(result.portfolioDetail).toBeUndefined();
  });

  test('getLiquidityPositions keeps portfolio detail and skips on-chain call without factory', async () => {
    let callViewCount = 0;
    state.callViewMethodImpl = async () => {
      callViewCount += 1;
      return { amount: '999' };
    };
    state.axiosGetImpl = async (url: string) => {
      if (url.endsWith('/api/app/liquidity/user-liquidity')) {
        return {
          data: {
            data: {
              items: [
                {
                  lpTokenAmount: '88',
                  token0Amount: '1',
                  token1Amount: '2',
                  assetUSD: 3,
                  tradePair: {
                    id: 'pair-unknown-factory',
                    feeRate: '0.001', // 0.1%, not in factory map
                    token0: { symbol: 'BTC', decimals: 8 },
                    token1: { symbol: 'USDT', decimals: 6 },
                  },
                },
              ],
            },
          },
        };
      }
      if (url.endsWith('/api/app/trade-pairs')) {
        return { data: { data: { items: [{ price: 10.5 }] } } };
      }
      if (url.endsWith('/api/app/liquidity/user-positions')) {
        return {
          data: {
            data: {
              items: [
                {
                  lpTokenAmount: '88',
                  lpTokenPercent: '0.2',
                  estimatedAPR: 12.5,
                  dynamicAPR: 13.1,
                  impermanentLossInUSD: 1.2,
                  tradePairInfo: {
                    id: 'pair-unknown-factory',
                    feeRate: '0.001',
                    token0: { symbol: 'BTC' },
                    token1: { symbol: 'USDT' },
                  },
                  position: {
                    valueInUsd: 3,
                    token0Amount: '1',
                    token0AmountInUsd: 1.5,
                    token1Amount: '2',
                    token1AmountInUsd: 1.5,
                  },
                  fee: { valueInUsd: 0.1 },
                },
              ],
            },
          },
        };
      }
      throw new Error(`unexpected url: ${url}`);
    };

    const result = await queryCore.getLiquidityPositions(config, {
      address: 'ELF_user',
    });

    expect(result.totalPositions).toBe(1);
    expect(result.positions[0]?.lpTokenAmountOnChain).toBe('0');
    expect(result.portfolioDetail?.length).toBe(1);
    expect(callViewCount).toBe(0);
  });
});
