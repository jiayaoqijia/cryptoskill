import { beforeAll, beforeEach, describe, expect, test } from 'bun:test';
import { coreMockState, installCoreModuleMocks, resetCoreMockState } from './core-mock-state';

installCoreModuleMocks();

let account: typeof import('../../src/core/account.js');
let security: typeof import('../../src/core/security.js');

beforeAll(async () => {
  account = await import('../../src/core/account.js');
  security = await import('../../src/core/security.js');
});

beforeEach(() => {
  resetCoreMockState();
  account.clearChainInfoCache();
  coreMockState.httpGetImpl = async (path: string, options?: any) => {
    if (path === '/api/app/search/chainsinfoindex') {
      return {
        items: [
          {
            chainId: 'tDVV',
            endPoint: 'https://rpc',
            caContractAddress: 'CA_CONTRACT',
            defaultToken: {
              name: 'ELF',
              symbol: 'ELF',
              address: 'TOKEN_CONTRACT',
              imageUrl: 'https://example.com/elf.png',
              decimals: 8,
            },
          },
        ],
      };
    }

    if (path === '/api/app/user/security/balanceCheck') {
      expect(options?.params?.caHash).toBe('ca_hash');
      expect(options?.params?.checkTransferSafeChainId).toBe('tDVV');
      return {
        isTransferSafe: true,
        isSynchronizing: false,
        isOriginChainSafe: true,
        accelerateGuardians: [],
      };
    }

    return {};
  };
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

type SecurityFixture = {
  symbol: string;
  tokenBalance: string;
  tokenDecimals?: number;
  feeSymbol?: string;
  feeBalance?: string;
  feeDecimals?: number;
  singleLimit?: string;
  dailyLimit?: string;
  dailyTransferredAmount?: string;
};

function installTransferViewMocks({
  symbol,
  tokenBalance,
  tokenDecimals = 8,
  feeSymbol = 'ELF',
  feeBalance,
  feeDecimals = 8,
  singleLimit = '100000000',
  dailyLimit = '1000000000',
  dailyTransferredAmount = '0',
}: SecurityFixture): void {
  coreMockState.callViewMethodImpl = async (
    _rpc: string,
    contractAddress: string,
    method: string,
    payload: any,
  ) => {
    if (contractAddress === 'TOKEN_CONTRACT' && method === 'GetBalance') {
      expect(payload.owner).toBe('ELF_ca_tDVV');
      if (payload.symbol === symbol) {
        return { symbol, balance: tokenBalance };
      }
      if (payload.symbol === feeSymbol) {
        return { symbol: feeSymbol, balance: feeBalance ?? tokenBalance };
      }
    }

    if (contractAddress === 'TOKEN_CONTRACT' && method === 'GetTokenInfo') {
      if (payload.symbol === symbol) {
        return { symbol, decimals: tokenDecimals };
      }
      if (payload.symbol === feeSymbol) {
        return { symbol: feeSymbol, decimals: feeDecimals };
      }
    }

    if (contractAddress === 'CA_CONTRACT' && method === 'GetTransferLimit') {
      return {
        singleLimit,
        dailyLimit,
        dailyTransferredAmount,
      };
    }

    if (contractAddress === 'CA_CONTRACT' && method === 'GetDefaultTokenTransferLimit') {
      return {
        transferLimit: {
          dayLimit: dailyLimit,
          singleLimit,
        },
      };
    }

    throw new Error(`Unexpected view call ${contractAddress}.${method}`);
  };
}

describe('core/security', () => {
  test('transferPreflight returns needs_add_guardian when wallet security is unsafe', async () => {
    coreMockState.httpGetImpl = async (path: string) => {
      if (path === '/api/app/search/chainsinfoindex') {
        return {
          items: [
            {
              chainId: 'tDVV',
              endPoint: 'https://rpc',
              caContractAddress: 'CA_CONTRACT',
              defaultToken: {
                name: 'ELF',
                symbol: 'ELF',
                address: 'TOKEN_CONTRACT',
                imageUrl: 'https://example.com/elf.png',
                decimals: 8,
              },
            },
          ],
        };
      }

      if (path === '/api/app/user/security/balanceCheck') {
        return {
          isTransferSafe: false,
          isSynchronizing: false,
          isOriginChainSafe: false,
          accelerateGuardians: [],
        };
      }

      return {};
    };

    const result = await security.transferPreflight(config, {
      caHash: 'ca_hash',
      caAddress: 'ELF_ca_tDVV',
      chainId: 'tDVV',
      symbol: 'ELF',
      amount: '100000000',
    });

    expect(result.decision).toBe('needs_add_guardian');
    expect(result.transferLimit).toBeUndefined();
  });

  test('transferPreflight returns needs_security_sync when wallet upgrade is still synchronizing', async () => {
    coreMockState.httpGetImpl = async (path: string) => {
      if (path === '/api/app/search/chainsinfoindex') {
        return {
          items: [
            {
              chainId: 'tDVV',
              endPoint: 'https://rpc',
              caContractAddress: 'CA_CONTRACT',
              defaultToken: {
                name: 'ELF',
                symbol: 'ELF',
                address: 'TOKEN_CONTRACT',
                imageUrl: 'https://example.com/elf.png',
                decimals: 8,
              },
            },
          ],
        };
      }

      if (path === '/api/app/user/security/balanceCheck') {
        return {
          isTransferSafe: false,
          isSynchronizing: true,
          isOriginChainSafe: true,
          accelerateGuardians: [],
        };
      }

      return {};
    };

    const result = await security.transferPreflight(config, {
      caHash: 'ca_hash',
      caAddress: 'ELF_ca_tDVV',
      chainId: 'tDVV',
      symbol: 'ELF',
      amount: '100000000',
    });

    expect(result.decision).toBe('needs_security_sync');
    expect(result.transferLimit).toBeUndefined();
  });

  test('transferPreflight returns direct_transfer when wallet is safe and transfer is within limits', async () => {
    installTransferViewMocks({
      symbol: 'ELF',
      tokenBalance: '200000000',
      singleLimit: '500000000',
      dailyLimit: '1000000000',
    });

    const result = await security.transferPreflight(config, {
      caHash: 'ca_hash',
      caAddress: 'ELF_ca_tDVV',
      chainId: 'tDVV',
      symbol: 'ELF',
      amount: '100000000',
    });

    expect(result.decision).toBe('direct_transfer');
    expect(result.transferLimit?.isSingleLimited).toBe(false);
    expect(result.transferLimit?.isDailyLimited).toBe(false);
  });

  test('transferPreflight keeps ELF one-time approval semantics on the fee token path', async () => {
    installTransferViewMocks({
      symbol: 'ELF',
      tokenBalance: '200000000',
      singleLimit: '100000000',
      dailyLimit: '1000000000',
    });

    const result = await security.transferPreflight(config, {
      caHash: 'ca_hash',
      caAddress: 'ELF_ca_tDVV',
      chainId: 'tDVV',
      symbol: 'ELF',
      amount: '150000000',
    });

    expect(result.decision).toBe('needs_one_time_approval');
    expect(result.transferLimit?.isSingleLimited).toBe(true);
    expect(result.transferLimit?.canApprove).toBe(true);
    expect(result.transferLimit?.feeSymbol).toBe('ELF');
    expect(result.transferLimit?.feeBalance).toBe('200000000');
    expect(result.transferLimit?.feeBuffer).toBe('10000000');
  });

  test('transferPreflight allows one-time approval when ELF balance exactly equals amount plus fee buffer', async () => {
    installTransferViewMocks({
      symbol: 'ELF',
      tokenBalance: '160000000',
      singleLimit: '100000000',
      dailyLimit: '1000000000',
    });

    const result = await security.transferPreflight(config, {
      caHash: 'ca_hash',
      caAddress: 'ELF_ca_tDVV',
      chainId: 'tDVV',
      symbol: 'ELF',
      amount: '150000000',
    });

    expect(result.decision).toBe('needs_one_time_approval');
    expect(result.transferLimit?.canApprove).toBe(true);
    expect(result.transferLimit?.feeBuffer).toBe('10000000');
  });

  test('transferPreflight returns needs_one_time_approval for non-native token when transfer and fee balances both fit', async () => {
    installTransferViewMocks({
      symbol: 'AIBOUNTY',
      tokenBalance: '200000000',
      feeBalance: '15000000',
      singleLimit: '100000000',
      dailyLimit: '1000000000',
    });

    const result = await security.transferPreflight(config, {
      caHash: 'ca_hash',
      caAddress: 'ELF_ca_tDVV',
      chainId: 'tDVV',
      symbol: 'AIBOUNTY',
      amount: '150000000',
    });

    expect(result.decision).toBe('needs_one_time_approval');
    expect(result.transferLimit?.canApprove).toBe(true);
    expect(result.transferLimit?.balance).toBe('200000000');
    expect(result.transferLimit?.feeSymbol).toBe('ELF');
    expect(result.transferLimit?.feeBalance).toBe('15000000');
    expect(result.transferLimit?.feeDecimals).toBe(8);
  });

  test('transferPreflight allows one-time approval for non-native token when transfer and fee balances exactly fit', async () => {
    installTransferViewMocks({
      symbol: 'AIBOUNTY',
      tokenBalance: '150000000',
      feeBalance: '10000000',
      singleLimit: '100000000',
      dailyLimit: '1000000000',
    });

    const result = await security.transferPreflight(config, {
      caHash: 'ca_hash',
      caAddress: 'ELF_ca_tDVV',
      chainId: 'tDVV',
      symbol: 'AIBOUNTY',
      amount: '150000000',
    });

    expect(result.decision).toBe('needs_one_time_approval');
    expect(result.transferLimit?.canApprove).toBe(true);
    expect(result.transferLimit?.balance).toBe('150000000');
    expect(result.transferLimit?.feeBalance).toBe('10000000');
  });

  test('transferPreflight returns needs_limit_modification for non-native token when fee balance does not fit', async () => {
    installTransferViewMocks({
      symbol: 'AIBOUNTY',
      tokenBalance: '200000000',
      feeBalance: '9000000',
      singleLimit: '100000000',
      dailyLimit: '1000000000',
    });

    const result = await security.transferPreflight(config, {
      caHash: 'ca_hash',
      caAddress: 'ELF_ca_tDVV',
      chainId: 'tDVV',
      symbol: 'AIBOUNTY',
      amount: '150000000',
    });

    expect(result.decision).toBe('needs_limit_modification');
    expect(result.transferLimit?.canApprove).toBe(false);
    expect(result.transferLimit?.feeBalance).toBe('9000000');
  });

  test('transferPreflight returns needs_limit_modification when ELF amount plus fee buffer does not fit', async () => {
    installTransferViewMocks({
      symbol: 'ELF',
      tokenBalance: '155000000',
      singleLimit: '100000000',
      dailyLimit: '1000000000',
    });

    const result = await security.transferPreflight(config, {
      caHash: 'ca_hash',
      caAddress: 'ELF_ca_tDVV',
      chainId: 'tDVV',
      symbol: 'ELF',
      amount: '150000000',
    });

    expect(result.decision).toBe('needs_limit_modification');
    expect(result.transferLimit?.canApprove).toBe(false);
  });
});
