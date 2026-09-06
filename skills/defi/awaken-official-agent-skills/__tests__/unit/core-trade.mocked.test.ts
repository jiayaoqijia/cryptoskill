import { beforeAll, beforeEach, describe, expect, mock, test } from 'bun:test';
import BigNumber from 'bignumber.js';

type TradeMockState = {
  axiosCalls: Array<{ url: string; params?: any }>;
  sendCalls: Array<{ rpcUrl: string; contractAddress: string; method: string; args: any }>;
  approveCalls: Array<{ symbol: string; spender: string; amount: string }>;
  axiosGetImpl: (url: string, options?: any) => Promise<any>;
  getTokenInfoImpl: (rpcUrl: string, tokenContract: string, symbol: string) => Promise<any>;
  getAllowanceImpl: (...args: any[]) => Promise<string>;
  approveTokenImpl: (...args: any[]) => Promise<any>;
  callViewMethodImpl: (...args: any[]) => Promise<any>;
};

const defaultState = (): TradeMockState => ({
  axiosCalls: [],
  sendCalls: [],
  approveCalls: [],
  axiosGetImpl: async () => ({ data: { data: {} } }),
  getTokenInfoImpl: async (_rpcUrl: string, _tokenContract: string, symbol: string) => ({
    symbol,
    decimals: symbol === 'USDT' ? 6 : 8,
  }),
  getAllowanceImpl: async () => '0',
  approveTokenImpl: async (_config: any, _signer: any, symbol: string, spender: string, amount: string) => ({
    transactionId: `approve-${symbol}`,
    status: 'mined',
    symbol,
    spender,
    amount,
  }),
  callViewMethodImpl: async () => ({ allowance: '0' }),
});

const g = globalThis as any;
const state: TradeMockState = g.__AWAKEN_TRADE_MOCK_STATE || (g.__AWAKEN_TRADE_MOCK_STATE = defaultState());

function resetState() {
  const d = defaultState();
  state.axiosCalls = d.axiosCalls;
  state.sendCalls = d.sendCalls;
  state.approveCalls = d.approveCalls;
  state.axiosGetImpl = d.axiosGetImpl;
  state.getTokenInfoImpl = d.getTokenInfoImpl;
  state.getAllowanceImpl = d.getAllowanceImpl;
  state.approveTokenImpl = d.approveTokenImpl;
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
  getTokenInfo: (...args: any[]) => (state.getTokenInfoImpl as any)(...args),
  getAllowance: (...args: any[]) => (state.getAllowanceImpl as any)(...args),
  approveToken: async (...args: any[]) => {
    const [, , symbol, spender, amount] = args;
    state.approveCalls.push({ symbol, spender, amount });
    return (state.approveTokenImpl as any)(...args);
  },
  timesDecimals: (value: string | number, decimals: number) =>
    new BigNumber(value).times(new BigNumber(10).pow(decimals)),
  divDecimals: (value: string | number, decimals: number) =>
    new BigNumber(value).div(new BigNumber(10).pow(decimals)),
}));

let tradeCore: typeof import('../../src/core/trade');

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

const signer = {
  address: 'ELF_signer',
  sendContractCall: async (rpcUrl: string, contractAddress: string, method: string, args: any) => {
    state.sendCalls.push({ rpcUrl, contractAddress, method, args });
    return {
      transactionId: `tx-${method}`,
      txResult: { Status: 'Mined' },
    };
  },
} as any;

beforeAll(async () => {
  tradeCore = await import('../../src/core/trade');
});

beforeEach(() => {
  resetState();
});

describe('core/trade mocked', () => {
  test('executeSwap approves when allowance is insufficient', async () => {
    state.getAllowanceImpl = async () => '0';
    state.axiosGetImpl = async (url: string) => {
      if (url.endsWith('/api/app/route/best-swap-routes')) {
        return {
          data: {
            data: {
              routes: [
                {
                  amountIn: '100000000',
                  amountOut: '2500000',
                  distributions: [
                    {
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
        };
      }
      throw new Error(`unexpected url: ${url}`);
    };

    const result = await tradeCore.executeSwap(config, signer, {
      symbolIn: 'ELF',
      symbolOut: 'USDT',
      amountIn: '1',
      slippage: '0.01',
    });

    expect(state.approveCalls.length).toBe(1);
    expect(state.approveCalls[0]?.spender).toBe('SWAP_HOOK');
    expect(state.sendCalls.some((call) => call.contractAddress === 'SWAP_HOOK')).toBe(true);
    expect(result.transactionId).toBe('tx-SwapExactTokensForTokens');
    expect(result.estimatedAmountOut).toBe('2.5');
  });

  test('executeSwap skips approve when allowance is enough', async () => {
    state.getAllowanceImpl = async () => '999999999999';
    state.axiosGetImpl = async () => ({
      data: {
        data: {
          routes: [
            {
              amountIn: '100000000',
              amountOut: '1200000',
              distributions: [
                {
                  amountIn: '100000000',
                  amountOut: '1200000',
                  tokens: [{ symbol: 'ELF' }, { symbol: 'USDT' }],
                  feeRates: [0.3],
                },
              ],
            },
          ],
        },
      },
    });

    const result = await tradeCore.executeSwap(config, signer, {
      symbolIn: 'ELF',
      symbolOut: 'USDT',
      amountIn: '1',
    });

    expect(state.approveCalls.length).toBe(0);
    expect(result.transactionId).toBe('tx-SwapExactTokensForTokens');
  });

  test('addLiquidity approves both tokens and sends AddLiquidity', async () => {
    state.getAllowanceImpl = async () => '0';

    const result = await tradeCore.addLiquidity(config, signer, {
      tokenA: 'ELF',
      tokenB: 'USDT',
      amountA: '1',
      amountB: '2',
      feeRate: '0.3',
    });

    expect(state.approveCalls.length).toBe(2);
    expect(state.approveCalls[0]?.spender).toBe('ROUTER_03');
    expect(state.sendCalls.some((call) => call.method === 'AddLiquidity')).toBe(true);
    expect(result.transactionId).toBe('tx-AddLiquidity');
  });

  test('removeLiquidity approves LP token on factory and sends RemoveLiquidity', async () => {
    state.callViewMethodImpl = async () => ({ allowance: '0' });

    const result = await tradeCore.removeLiquidity(config, signer, {
      tokenA: 'ELF',
      tokenB: 'USDT',
      lpAmount: '1',
      feeRate: '0.3',
    });

    expect(state.sendCalls.some((call) => call.contractAddress === 'FACTORY_03' && call.method === 'Approve')).toBe(true);
    expect(state.sendCalls.some((call) => call.contractAddress === 'ROUTER_03' && call.method === 'RemoveLiquidity')).toBe(true);
    expect(result.transactionId).toBe('tx-RemoveLiquidity');
  });

  test('removeLiquidity throws when factory is missing for feeRate', async () => {
    const configWithoutFactory = {
      ...config,
      router: { ...config.router, '0.1': 'ROUTER_01' },
      factory: { ...config.factory },
    } as any;

    await expect(
      tradeCore.removeLiquidity(configWithoutFactory, signer, {
        tokenA: 'ELF',
        tokenB: 'USDT',
        lpAmount: '1',
        feeRate: '0.1',
      }),
    ).rejects.toThrow('No factory for feeRate=0.1');
  });

  test('approveTokenSpending delegates to approveToken and formats result', async () => {
    const result = await tradeCore.approveTokenSpending(config, signer, {
      symbol: 'ELF',
      spender: 'ROUTER_03',
      amount: '1.5',
    });

    expect(state.approveCalls.length).toBe(1);
    expect(result.symbol).toBe('ELF');
    expect(result.transactionId).toBe('approve-ELF');
  });
});
