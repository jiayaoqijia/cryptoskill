import { afterAll, beforeAll, beforeEach, describe, expect, test } from 'bun:test';
import * as fs from 'node:fs';
import * as os from 'node:os';
import * as path from 'node:path';
import {
  MockHttpError,
  coreMockState,
  installCoreModuleMocks,
  resetCoreMockState,
} from './core-mock-state';
import { createWallet } from '../../lib/aelf-client.js';

installCoreModuleMocks();

const originalHome = process.env.HOME;
const originalContextPath = process.env.PORTKEY_SKILL_WALLET_CONTEXT_PATH;
const testHome = fs.mkdtempSync(path.join(os.tmpdir(), 'ca-account-home-'));
process.env.HOME = testHome;
process.env.PORTKEY_SKILL_WALLET_CONTEXT_PATH = path.join(
  testHome,
  '.portkey',
  'skill-wallet',
  'context.v1.json',
);

let account: typeof import('../../src/core/account.js');
let keystore: typeof import('../../src/core/keystore.js');

beforeAll(async () => {
  account = await import('../../src/core/account.js');
  keystore = await import('../../src/core/keystore.js');
});

beforeEach(() => {
  resetCoreMockState();
  account.clearChainInfoCache();
  keystore.clearKeystoreState();
  const portkeyDir = path.join(testHome, '.portkey');
  if (fs.existsSync(portkeyDir)) {
    fs.rmSync(portkeyDir, { recursive: true, force: true });
  }
});

afterAll(() => {
  if (originalHome !== undefined) {
    process.env.HOME = originalHome;
  } else {
    delete process.env.HOME;
  }
  if (originalContextPath !== undefined) {
    process.env.PORTKEY_SKILL_WALLET_CONTEXT_PATH = originalContextPath;
  } else {
    delete process.env.PORTKEY_SKILL_WALLET_CONTEXT_PATH;
  }
  fs.rmSync(testHome, { recursive: true, force: true });
});

const TEST_CONFIG = {
  apiUrl: 'https://api',
  eoaApiUrl: 'https://eoa-api',
  graphqlUrl: 'https://gql',
  network: 'mainnet' as const,
  eoaFallbackEnabled: true,
  eoaFallbackRetryCount: 2,
  eoaFallbackRetryDelayMs: 200,
};

describe('core/account', () => {
  test('checkAccount returns registered when originChainId exists', async () => {
    coreMockState.httpGetImpl = async () => ({ originChainId: 'tDVV' });

    const result = await account.checkAccount(
      TEST_CONFIG,
      { email: 'a@b.com' },
    );

    expect(result).toEqual({ isRegistered: true, originChainId: 'tDVV' });
    expect(coreMockState.httpCalls[0]?.path).toBe('/api/app/account/registerInfo');
  });

  test('checkAccount returns not registered on empty payload', async () => {
    coreMockState.httpGetImpl = async () => ({ originChainId: null });

    const result = await account.checkAccount(
      TEST_CONFIG,
      { email: 'a@b.com' },
    );

    expect(result).toEqual({ isRegistered: false, originChainId: null });
  });

  test('checkAccount handles HttpError 404/3002 as not registered', async () => {
    coreMockState.httpGetImpl = async () => {
      throw new MockHttpError(404, 'Not Found', JSON.stringify({ code: '3002' }));
    };

    const result = await account.checkAccount(
      TEST_CONFIG,
      { email: 'x@y.com' },
    );

    expect(result).toEqual({ isRegistered: false, originChainId: null });
  });

  test('checkAccount handles nested 403 error.code=3002 as not registered', async () => {
    coreMockState.httpGetImpl = async () => {
      throw new MockHttpError(
        403,
        'Forbidden',
        JSON.stringify({ error: { code: '3002', message: 'Guardian not exist.' } }),
      );
    };

    const result = await account.checkAccount(
      TEST_CONFIG,
      { email: 'nested@example.com' },
    );

    expect(result).toEqual({ isRegistered: false, originChainId: null });
  });

  test('checkAccount handles legacy message fallback', async () => {
    coreMockState.httpGetImpl = async () => {
      throw new Error('account not exist 3002');
    };

    const result = await account.checkAccount(
      TEST_CONFIG,
      { email: 'x@y.com' },
    );

    expect(result).toEqual({ isRegistered: false, originChainId: null });
  });

  test('checkAccount throws for unknown errors', async () => {
    coreMockState.httpGetImpl = async () => {
      throw new Error('boom');
    };

    await expect(
      account.checkAccount(
        TEST_CONFIG,
        { email: 'x@y.com' },
      ),
    ).rejects.toThrow('boom');
  });

  test('getGuardianList normalizes guardianList.guardians response', async () => {
    coreMockState.httpGetImpl = async () => ({
      guardianList: { guardians: [{ guardianIdentifier: 'a@b.com', type: 'Email' }] },
      caHash: 'hash',
      caAddress: 'ELF_abc_tDVV',
      createChainId: 'tDVV',
    });

    const result = await account.getGuardianList(
      TEST_CONFIG,
      { identifier: 'a@b.com', chainId: 'tDVV' },
    );

    expect(result.guardians.length).toBe(1);
    expect(result.caHash).toBe('hash');
    expect(result.createChainId).toBe('tDVV');
    expect(coreMockState.httpCalls[0]?.options?.params?.chainId).toBe('tDVV');
  });

  test('getGuardianList requires chainId', async () => {
    await expect(
      account.getGuardianList(TEST_CONFIG, { identifier: 'missing-chain' } as any),
    ).rejects.toThrow('chainId is required');
  });

  test('getGuardianList supports guardianAccounts legacy format', async () => {
    coreMockState.httpGetImpl = async () => ({
      guardianAccounts: [{ guardianIdentifier: 'legacy@b.com', type: 'Email' }],
    });

    const result = await account.getGuardianList(
      TEST_CONFIG,
      { identifier: 'legacy@b.com', chainId: 'AELF' },
    );

    expect(result.guardians[0]?.guardianIdentifier).toBe('legacy@b.com');
  });

  test('getChainInfo caches by apiUrl and clearChainInfoCache resets cache', async () => {
    let times = 0;
    coreMockState.httpGetImpl = async (path: string) => {
      if (path === '/api/app/search/chainsinfoindex') {
        times += 1;
        return {
          items: [
            {
              chainId: 'AELF',
              endPoint: 'https://rpc',
              caContractAddress: 'CA',
              defaultToken: { address: 'TOKEN', decimals: 8 },
            },
          ],
        };
      }
      return {};
    };

    await account.getChainInfo(TEST_CONFIG);
    await account.getChainInfo(TEST_CONFIG);
    expect(times).toBe(1);

    account.clearChainInfoCache();
    await account.getChainInfo(TEST_CONFIG);
    expect(times).toBe(2);
  });

  test('getChainInfoByChainId throws when not found', async () => {
    coreMockState.httpGetImpl = async () => ({
      items: [
        {
          chainId: 'AELF',
          endPoint: 'https://rpc',
          caContractAddress: 'CA',
          defaultToken: { address: 'TOKEN', decimals: 8 },
        },
      ],
    });

    await expect(
      account.getChainInfoByChainId(
        TEST_CONFIG,
        'tDVV',
      ),
    ).rejects.toThrow('not found');
  });

  test('getHolderInfo resolves chain and returns on-chain holder info', async () => {
    coreMockState.httpGetImpl = async () => ({
      items: [
        {
          chainId: 'AELF',
          endPoint: 'https://rpc.aelf',
          caContractAddress: 'CA_CONTRACT',
          defaultToken: { address: 'TOKEN', decimals: 8 },
        },
      ],
    });

    coreMockState.callViewMethodImpl = async (
      rpcUrl: string,
      contractAddress: string,
      method: string,
      payload: any,
    ) => {
      expect(rpcUrl).toBe('https://rpc.aelf');
      expect(contractAddress).toBe('CA_CONTRACT');
      expect(method).toBe('GetHolderInfo');
      expect(payload.caHash).toBe('CA_HASH');
      return { caHash: 'CA_HASH', caAddress: 'ELF_addr_AELF' };
    };

    const result = await account.getHolderInfo(
      TEST_CONFIG,
      { chainId: 'AELF', caHash: 'CA_HASH' },
    );

    expect(result.caHash).toBe('CA_HASH');
  });

  test('getHolderInfo throws when holder does not exist', async () => {
    coreMockState.httpGetImpl = async () => ({
      items: [
        {
          chainId: 'AELF',
          endPoint: 'https://rpc.aelf',
          caContractAddress: 'CA_CONTRACT',
          defaultToken: { address: 'TOKEN', decimals: 8 },
        },
      ],
    });
    coreMockState.callViewMethodImpl = async () => ({ caHash: '' });

    await expect(
      account.getHolderInfo(
        TEST_CONFIG,
        { chainId: 'AELF', caHash: 'MISSING_HASH' },
      ),
    ).rejects.toThrow('Holder not found');
  });

  test('prepareAuthFlow recommends register for unregistered emails', async () => {
    coreMockState.httpGetImpl = async (requestPath: string) => {
      if (requestPath === '/api/app/account/registerInfo') {
        throw new MockHttpError(404, 'Not Found', JSON.stringify({ code: '3002' }));
      }
      return {};
    };

    const result = await account.prepareAuthFlow(
      TEST_CONFIG,
      { email: 'new@example.com', network: 'mainnet' },
    );

    expect(result.isRegistered).toBe(false);
    expect(result.recommendedFlow).toBe('register');
    expect(result.resolvedChainId).toBe('tDVV');
    expect(result.guardians).toBeUndefined();
    expect(result.matchedLocalProfile).toBeNull();
  });

  test('prepareAuthFlow recommends recovery and includes guardian + local profile data', async () => {
    const wallet = createWallet();
    keystore.saveKeystore({
      password: 'secret',
      privateKey: wallet.privateKey,
      mnemonic: wallet.mnemonic!,
      caHash: 'local_hash',
      caAddress: 'ELF_local_tDVV',
      loginEmail: 'known@example.com',
      originChainId: 'tDVV',
      network: 'mainnet',
    });
    keystore.lockWallet();

    coreMockState.httpGetImpl = async (requestPath: string) => {
      if (requestPath === '/api/app/account/registerInfo') {
        return { originChainId: 'tDVV' };
      }
      if (requestPath === '/api/app/account/guardianIdentifiers') {
        return {
          guardianList: {
            guardians: [{ guardianIdentifier: 'known@example.com', type: 'Email' }],
          },
          caHash: 'chain_hash',
          caAddress: 'ELF_chain_tDVV',
          createChainId: 'tDVV',
        };
      }
      return {};
    };

    const result = await account.prepareAuthFlow(
      TEST_CONFIG,
      { email: 'known@example.com', network: 'mainnet' },
    );

    expect(result.isRegistered).toBe(true);
    expect(result.recommendedFlow).toBe('recovery');
    expect(result.resolvedChainId).toBe('tDVV');
    expect(result.caHash).toBe('chain_hash');
    expect(result.caAddress).toBe('ELF_chain_tDVV');
    expect(result.guardians?.length).toBe(1);
    expect(result.matchedLocalProfile?.loginEmail).toBe('known@example.com');
    expect(result.matchedLocalProfile?.caHash).toBe('local_hash');
  });

  test('prepareAuthFlow uses originChainId when chainId override is omitted', async () => {
    const httpCalls: string[] = [];
    coreMockState.httpGetImpl = async (requestPath: string, options?: any) => {
      httpCalls.push(`${requestPath}:${options?.params?.chainId || ''}`);
      if (requestPath === '/api/app/account/registerInfo') {
        return { originChainId: 'tDVV' };
      }
      if (requestPath === '/api/app/account/guardianIdentifiers') {
        expect(options?.params?.chainId).toBe('tDVV');
        return {
          guardianList: {
            guardians: [{ guardianIdentifier: 'tdvv@example.com', type: 'Email' }],
          },
          caHash: 'tdvv_hash',
          caAddress: 'ELF_tdvv_tDVV',
          createChainId: 'tDVV',
        };
      }
      return {};
    };

    const result = await account.prepareAuthFlow(
      TEST_CONFIG,
      { email: 'tdvv@example.com', network: 'mainnet' },
    );

    expect(result.recommendedFlow).toBe('recovery');
    expect(result.originChainId).toBe('tDVV');
    expect(result.resolvedChainId).toBe('tDVV');
    expect(httpCalls).toContain('/api/app/account/guardianIdentifiers:tDVV');
  });

  test('prepareAuthFlow keeps explicit registration override for new accounts', async () => {
    coreMockState.httpGetImpl = async () => {
      throw new MockHttpError(404, 'Not Found', JSON.stringify({ code: '3002' }));
    };

    const result = await account.prepareAuthFlow(
      TEST_CONFIG,
      { email: 'new-aelf@example.com', network: 'mainnet', chainId: 'AELF' },
    );

    expect(result.isRegistered).toBe(false);
    expect(result.recommendedFlow).toBe('register');
    expect(result.resolvedChainId).toBe('AELF');
  });
});
