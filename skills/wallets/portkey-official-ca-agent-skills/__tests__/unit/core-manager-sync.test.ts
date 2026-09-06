import { beforeAll, beforeEach, describe, expect, test } from 'bun:test';
import { coreMockState, installCoreModuleMocks, resetCoreMockState } from './core-mock-state';

installCoreModuleMocks();

let managerSync: typeof import('../../src/core/manager-sync.js');
let account: typeof import('../../src/core/account.js');

beforeAll(async () => {
  account = await import('../../src/core/account.js');
  managerSync = await import('../../src/core/manager-sync.js');
});

beforeEach(() => {
  resetCoreMockState();
  account.clearChainInfoCache();
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

describe('core/manager-sync', () => {
  test('checkManagerSyncState returns synced manager info', async () => {
    coreMockState.callViewMethodImpl = async (
      _rpc: string,
      contractAddress: string,
      method: string,
      payload: any,
    ) => {
      if (contractAddress === 'CA' && method === 'GetHolderInfo') {
        expect(payload.caHash).toBe('hash');
        return {
          caHash: 'hash',
          caAddress: 'ELF_ca_tDVV',
          managerInfos: [{ address: 'ELF_manager', extraData: '' }],
          guardianList: { guardians: [] },
        };
      }
      throw new Error(`Unexpected view call ${contractAddress}.${method}`);
    };

    const result = await managerSync.checkManagerSyncState(config, {
      caHash: 'hash',
      chainId: 'tDVV',
      managerAddress: 'ELF_manager',
    });

    expect(result.isManagerSynced).toBe(true);
    expect(result.caAddress).toBe('ELF_ca_tDVV');
  });

  test('checkManagerSyncState returns unsynced manager info and formats blocking error', async () => {
    coreMockState.callViewMethodImpl = async (
      _rpc: string,
      contractAddress: string,
      method: string,
    ) => {
      if (contractAddress === 'CA' && method === 'GetHolderInfo') {
        return {
          caHash: 'hash',
          caAddress: 'ELF_ca_tDVV',
          managerInfos: [{ address: 'ELF_other_manager', extraData: '' }],
          guardianList: { guardians: [] },
        };
      }
      throw new Error(`Unexpected view call ${contractAddress}.${method}`);
    };

    const result = await managerSync.checkManagerSyncState(config, {
      caHash: 'hash',
      chainId: 'tDVV',
      managerAddress: 'ELF_manager',
    });

    expect(result.isManagerSynced).toBe(false);
    expect(managerSync.formatManagerSyncError(result)).toContain('Manager ELF_manager is not yet synced on tDVV');
    expect(managerSync.formatManagerSyncError(result)).toContain('Current on-chain managers: ELF_other_manager');
    expect(managerSync.formatManagerSyncError(result)).toContain('verify the selected loginEmail/keystoreFile or re-login / recover');
  });
});
