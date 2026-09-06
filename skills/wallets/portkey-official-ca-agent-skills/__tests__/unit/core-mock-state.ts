import { mock } from 'bun:test';

export class MockHttpError extends Error {
  statusCode: number;
  errorCode: string | null;
  responseBody: string;

  constructor(statusCode: number, statusText: string, body = '') {
    let errorCode: string | null = null;
    let apiMessage = '';
    try {
      const parsed = JSON.parse(body);
      const nested = parsed?.error && typeof parsed.error === 'object' ? parsed.error : null;
      errorCode = nested?.code ?? nested?.Code ?? parsed?.code ?? parsed?.Code ?? null;
      apiMessage = nested?.message ?? nested?.Message ?? parsed?.message ?? parsed?.Message ?? '';
    } catch {
      apiMessage = body;
    }

    super(`HTTP ${statusCode} ${statusText}: ${apiMessage || body}`);
    this.name = 'HttpError';
    this.statusCode = statusCode;
    this.responseBody = body;
    this.errorCode = errorCode;
  }
}

const PRIVATE_IP_PATTERNS = [
  /^localhost$/i,
  /^127\./,
  /^10\./,
  /^172\.(1[6-9]|2\d|3[01])\./,
  /^192\.168\./,
  /^0\./,
  /^\[::1\]/,
  /^\[fd/i,
  /^\[fe80:/i,
];

function mockValidateRpcUrl(url: string): void {
  let parsed: URL;
  try {
    parsed = new URL(url);
  } catch {
    throw new Error(`Invalid RPC URL: ${url}`);
  }

  if (parsed.protocol !== 'https:' && parsed.protocol !== 'http:') {
    throw new Error(`RPC URL must use http(s) protocol, got: ${parsed.protocol}`);
  }

  const hostname = parsed.hostname;
  for (const pattern of PRIVATE_IP_PATTERNS) {
    if (pattern.test(hostname)) {
      throw new Error(`RPC URL must not point to a private/internal address: ${hostname}`);
    }
  }
}

type CoreMockState = {
  httpCalls: Array<{ method: string; path: string; options?: any }>;
  httpGetImpl: (path: string, options?: any) => Promise<any>;
  httpPostImpl: (path: string, options?: any) => Promise<any>;
  httpPutImpl: (path: string, options?: any) => Promise<any>;
  httpDelImpl: (path: string, options?: any) => Promise<any>;

  createWalletImpl: (...args: any[]) => any;
  getWalletByPrivateKeyImpl: (...args: any[]) => any;
  getAelfInstanceImpl: (...args: any[]) => any;
  getContractInstanceImpl: (...args: any[]) => Promise<any>;
  callViewMethodImpl: (...args: any[]) => Promise<any>;
  callSendMethodImpl: (...args: any[]) => Promise<any>;
  calculateTransactionFeeImpl: (...args: any[]) => Promise<any>;
  encodeManagerForwardCallParamsImpl: (...args: any[]) => Promise<any>;
  getTxResultImpl: (...args: any[]) => Promise<any>;
};

const defaultState = (): CoreMockState => ({
  httpCalls: [],
  httpGetImpl: async () => ({}),
  httpPostImpl: async () => ({}),
  httpPutImpl: async () => ({}),
  httpDelImpl: async () => ({}),

  createWalletImpl: () => ({
    address: 'ELF_mock_wallet',
    privateKey: 'a'.repeat(64),
    mnemonic: 'm1 m2 m3 m4 m5 m6 m7 m8 m9 m10 m11 m12',
  }),
  getWalletByPrivateKeyImpl: (privateKey: string) => ({ address: 'ELF_mock_wallet', privateKey }),
  getAelfInstanceImpl: () => ({}),
  getContractInstanceImpl: async () => ({}),
  callViewMethodImpl: async () => ({}),
  callSendMethodImpl: async () => ({ transactionId: 'tx-mock', data: { Status: 'MINED' } }),
  calculateTransactionFeeImpl: async () => ({
    transactionFee: { ELF: '1000000' },
    transactionFees: {
      ChargingAddress: 'ELF_fee_payer',
      Fee: { ELF: '1000000' },
    },
    chargingAddress: 'ELF_fee_payer',
    isCaPayingFee: null,
    feeSymbol: 'ELF',
    feeAmount: '1000000',
  }),
  encodeManagerForwardCallParamsImpl: async () => ({ encodedInput: '0xmock' }),
  getTxResultImpl: async () => ({ Status: 'MINED' }),
});

const g = globalThis as any;
export const coreMockState: CoreMockState =
  g.__CA_CORE_MOCK_STATE || (g.__CA_CORE_MOCK_STATE = defaultState());

export function resetCoreMockState(): void {
  const d = defaultState();
  coreMockState.httpCalls = d.httpCalls;
  coreMockState.httpGetImpl = d.httpGetImpl;
  coreMockState.httpPostImpl = d.httpPostImpl;
  coreMockState.httpPutImpl = d.httpPutImpl;
  coreMockState.httpDelImpl = d.httpDelImpl;
  coreMockState.createWalletImpl = d.createWalletImpl;
  coreMockState.getWalletByPrivateKeyImpl = d.getWalletByPrivateKeyImpl;
  coreMockState.getAelfInstanceImpl = d.getAelfInstanceImpl;
  coreMockState.getContractInstanceImpl = d.getContractInstanceImpl;
  coreMockState.callViewMethodImpl = d.callViewMethodImpl;
  coreMockState.callSendMethodImpl = d.callSendMethodImpl;
  coreMockState.calculateTransactionFeeImpl = d.calculateTransactionFeeImpl;
  coreMockState.encodeManagerForwardCallParamsImpl = d.encodeManagerForwardCallParamsImpl;
  coreMockState.getTxResultImpl = d.getTxResultImpl;
}

export function installCoreModuleMocks(): void {
  if (g.__CA_CORE_MOCKS_INSTALLED) return;
  g.__CA_CORE_MOCKS_INSTALLED = true;

  mock.module('../../lib/http.js', () => ({
    createHttpClient: () => ({
      request: async (method: string, path: string, options?: any) => {
        coreMockState.httpCalls.push({ method, path, options });
        const m = method.toUpperCase();
        if (m === 'GET') return coreMockState.httpGetImpl(path, options);
        if (m === 'POST') return coreMockState.httpPostImpl(path, options);
        if (m === 'PUT') return coreMockState.httpPutImpl(path, options);
        if (m === 'DELETE') return coreMockState.httpDelImpl(path, options);
        return {};
      },
      get: async (path: string, options?: any) => {
        coreMockState.httpCalls.push({ method: 'GET', path, options });
        return coreMockState.httpGetImpl(path, options);
      },
      post: async (path: string, options?: any) => {
        coreMockState.httpCalls.push({ method: 'POST', path, options });
        return coreMockState.httpPostImpl(path, options);
      },
      put: async (path: string, options?: any) => {
        coreMockState.httpCalls.push({ method: 'PUT', path, options });
        return coreMockState.httpPutImpl(path, options);
      },
      del: async (path: string, options?: any) => {
        coreMockState.httpCalls.push({ method: 'DELETE', path, options });
        return coreMockState.httpDelImpl(path, options);
      },
    }),
    HttpError: MockHttpError,
    validateRpcUrl: mockValidateRpcUrl,
  }));

  mock.module('../../lib/aelf-client.js', () => ({
    createWallet: (...args: any[]) => coreMockState.createWalletImpl(...args),
    getWalletByPrivateKey: (...args: any[]) => coreMockState.getWalletByPrivateKeyImpl(...args),
    getAelfInstance: (...args: any[]) => coreMockState.getAelfInstanceImpl(...args),
    getContractInstance: (...args: any[]) => coreMockState.getContractInstanceImpl(...args),
    callViewMethod: (...args: any[]) => coreMockState.callViewMethodImpl(...args),
    callSendMethod: (...args: any[]) => coreMockState.callSendMethodImpl(...args),
    calculateTransactionFee: (...args: any[]) => coreMockState.calculateTransactionFeeImpl(...args),
    encodeManagerForwardCallParams: (...args: any[]) =>
      coreMockState.encodeManagerForwardCallParamsImpl(...args),
    getTxResult: (...args: any[]) => coreMockState.getTxResultImpl(...args),
    clearCaches: () => {},
  }));
}
