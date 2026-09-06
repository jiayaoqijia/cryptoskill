import { beforeAll, beforeEach, describe, expect, test } from 'bun:test';
import { coreMockState, installCoreModuleMocks, resetCoreMockState } from './core-mock-state';

installCoreModuleMocks();

let contract: typeof import('../../src/core/contract.js');
let account: typeof import('../../src/core/account.js');

beforeAll(async () => {
  account = await import('../../src/core/account.js');
  contract = await import('../../src/core/contract.js');
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
            caContractAddress: 'CA_CONTRACT',
            defaultToken: { address: 'TOKEN', decimals: 8 },
          },
        ],
      };
      }
      return {};
    };
    coreMockState.callViewMethodImpl = async (
      _rpc: string,
      contractAddress: string,
      method: string,
      payload: any,
    ) => {
      if (contractAddress === 'CA_CONTRACT' && method === 'GetHolderInfo') {
        expect(payload.caHash).toBeTruthy();
        return {
          caHash: payload.caHash,
          caAddress: 'ELF_ca_tDVV',
          managerInfos: [
            { address: 'ELF_wallet', extraData: '' },
            { address: 'ELF_wallet_2', extraData: '' },
          ],
          guardianList: { guardians: [] },
        };
      }
      throw new Error(`Unexpected view call ${contractAddress}.${method}`);
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

describe('core/contract', () => {
  test('callContractViewMethod validates required params', async () => {
    await expect(
      contract.callContractViewMethod(config, {
        rpcUrl: '',
        contractAddress: 'c',
        methodName: 'Get',
      } as any),
    ).rejects.toThrow('rpcUrl is required');

    await expect(
      contract.callContractViewMethod(config, {
        rpcUrl: 'https://rpc',
        contractAddress: '',
        methodName: 'Get',
      } as any),
    ).rejects.toThrow('contractAddress is required');

    await expect(
      contract.callContractViewMethod(config, {
        rpcUrl: 'https://rpc',
        contractAddress: 'c',
        methodName: '',
      } as any),
    ).rejects.toThrow('methodName is required');
  });

  test('callContractViewMethod delegates to aelf client', async () => {
    coreMockState.callViewMethodImpl = async (rpcUrl: string, address: string, method: string, payload: any) => {
      expect(rpcUrl).toBe('https://rpc');
      expect(address).toBe('TOKEN');
      expect(method).toBe('GetBalance');
      expect(payload.symbol).toBe('ELF');
      return { balance: '100' };
    };

    const result = await contract.callContractViewMethod(config, {
      rpcUrl: 'https://rpc',
      contractAddress: 'TOKEN',
      methodName: 'GetBalance',
      params: { symbol: 'ELF' },
    });

    expect((result as any).balance).toBe('100');
  });

  test('callCaViewMethod resolves chain info automatically', async () => {
    coreMockState.callViewMethodImpl = async (rpcUrl: string, address: string, method: string) => {
      expect(rpcUrl).toBe('https://rpc');
      expect(address).toBe('CA_CONTRACT');
      expect(method).toBe('GetHolderInfo');
      return { caHash: 'hash' };
    };

    const result = await contract.callCaViewMethod(config, 'tDVV', 'GetHolderInfo', {
      caHash: 'hash',
    });

    expect((result as any).caHash).toBe('hash');
  });

  test('managerForwardCall encodes params then calls CA contract', async () => {
    const wallet = { address: 'ELF_wallet', privateKey: 'pk' } as any;

    coreMockState.encodeManagerForwardCallParamsImpl = async (rpcUrl: string, payload: any) => {
      expect(rpcUrl).toBe('https://rpc');
      expect(payload.methodName).toBe('Transfer');
      return { encodedInput: '0xencoded' };
    };

    coreMockState.callSendMethodImpl = async (
      rpcUrl: string,
      caContractAddress: string,
      _wallet: any,
      method: string,
      encoded: any,
    ) => {
      expect(rpcUrl).toBe('https://rpc');
      expect(caContractAddress).toBe('CA_CONTRACT');
      expect(method).toBe('ManagerForwardCall');
      expect(encoded.encodedInput).toBe('0xencoded');
      return { transactionId: 'tx-forward', data: { Status: 'MINED' } };
    };
    coreMockState.calculateTransactionFeeImpl = async (
      rpcUrl: string,
      caContractAddress: string,
      _wallet: any,
      method: string,
      payload: any,
    ) => {
      expect(rpcUrl).toBe('https://rpc');
      expect(caContractAddress).toBe('CA_CONTRACT');
      expect(method).toBe('ManagerForwardCall');
      expect(payload.encodedInput).toBe('0xencoded');
      return {
        transactionFee: { ELF: '1000000' },
        transactionFees: {
          ChargingAddress: 'ELF_fee_payer',
          Fee: { ELF: '1000000' },
        },
        chargingAddress: 'ELF_fee_payer',
        isCaPayingFee: null,
        feeSymbol: 'ELF',
        feeAmount: '1000000',
      };
    };

    const result = await contract.managerForwardCall(config, wallet, {
      caHash: 'hash',
      contractAddress: 'TOKEN',
      methodName: 'Transfer',
      args: { to: 'ELF_to', symbol: 'ELF', amount: '1' },
      chainId: 'tDVV',
    });

    expect(result.transactionId).toBe('tx-forward');
    expect(result.feePreview?.feeAmount).toBe('1000000');
    expect(result.feePreview?.chargingAddress).toBe('ELF_fee_payer');
    expect(result.caAddress).toBe('ELF_ca_tDVV');
  });

  test('managerForwardCall forwards one-time approval guardians for transfer calls', async () => {
    const wallet = { address: 'ELF_wallet', privateKey: 'pk' } as any;

    coreMockState.encodeManagerForwardCallParamsImpl = async () => ({ encodedInput: '0xencoded' });
    coreMockState.callSendMethodImpl = async (
      _rpc: string,
      _caContractAddress: string,
      _wallet: any,
      method: string,
      payload: any,
    ) => {
      expect(method).toBe('ManagerForwardCall');
      expect(payload.guardiansApproved).toHaveLength(1);
      expect(payload.guardiansApproved[0].identifierHash).toBe('identifierHashFromDoc');
      expect(payload.guardiansApproved[0].verificationInfo.id).toBe('v-transfer');
      expect(Buffer.isBuffer(payload.guardiansApproved[0].verificationInfo.signature)).toBe(true);
      return { transactionId: 'tx-guardian', data: { Status: 'MINED' } };
    };

    const result = await contract.managerForwardCall(config, wallet, {
      caHash: 'hash',
      contractAddress: 'TOKEN',
      methodName: 'Transfer',
      args: { to: 'ELF_to', symbol: 'ELF', amount: '1' },
      chainId: 'tDVV',
      guardiansApproved: [
        {
          identifier: 'proof@example.com',
          type: 0,
          verifierId: 'v-transfer',
          verificationDoc: '0,identifierHashFromDoc,1,2,3,10,1866392',
          signature: 'abcd',
        },
      ],
    });

    expect(result.transactionId).toBe('tx-guardian');
  });

  test('managerForwardCall blocks before fee preview and send when manager is not synced', async () => {
    const wallet = { address: 'ELF_wallet', privateKey: 'pk' } as any;
    let feePreviewCalled = false;
    let sendCalled = false;

    coreMockState.callViewMethodImpl = async (
      _rpc: string,
      contractAddress: string,
      method: string,
    ) => {
      if (contractAddress === 'CA_CONTRACT' && method === 'GetHolderInfo') {
        return {
          caHash: 'hash',
          caAddress: 'ELF_ca_tDVV',
          managerInfos: [{ address: 'ELF_other_manager', extraData: '' }],
          guardianList: { guardians: [] },
        };
      }
      throw new Error(`Unexpected view call ${contractAddress}.${method}`);
    };
    coreMockState.calculateTransactionFeeImpl = async () => {
      feePreviewCalled = true;
      return {
        transactionFee: null,
        transactionFees: null,
        chargingAddress: null,
        isCaPayingFee: null,
        feeSymbol: null,
        feeAmount: null,
      };
    };
    coreMockState.callSendMethodImpl = async () => {
      sendCalled = true;
      return { transactionId: 'tx-forward', data: { Status: 'MINED' } };
    };

    await expect(
      contract.managerForwardCall(config, wallet, {
        caHash: 'hash',
        contractAddress: 'TOKEN',
        methodName: 'ClaimByPortkeyToCa',
        args: { value: Buffer.from('1234', 'hex') },
        chainId: 'tDVV',
      }),
    ).rejects.toThrow('Manager ELF_wallet is not yet synced on tDVV');

    expect(feePreviewCalled).toBe(false);
    expect(sendCalled).toBe(false);
  });

  test('managerForwardCallWithKey builds wallet and forwards call', async () => {
    coreMockState.getWalletByPrivateKeyImpl = (privateKey: string) => {
      expect(privateKey).toBe('raw-pk');
      return { address: 'ELF_wallet_2', privateKey };
    };

    coreMockState.callSendMethodImpl = async () => ({
      transactionId: 'tx-key',
      data: { Status: 'MINED' },
    });

    const result = await contract.managerForwardCallWithKey(config, 'raw-pk', {
      caHash: 'hash',
      contractAddress: 'TOKEN',
      methodName: 'Transfer',
      args: { to: 'ELF_to', symbol: 'ELF', amount: '1' },
      chainId: 'tDVV',
    });

    expect(result.transactionId).toBe('tx-key');
  });

  test('managerForwardCall throws for missing required params', async () => {
    const wallet = { address: 'ELF_wallet', privateKey: 'pk' } as any;

    await expect(
      contract.managerForwardCall(config, wallet, {
        caHash: '',
        contractAddress: 'TOKEN',
        methodName: 'Transfer',
        args: {},
        chainId: 'tDVV',
      } as any),
    ).rejects.toThrow('caHash is required');
  });
});
