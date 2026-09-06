import { beforeAll, beforeEach, describe, expect, test } from 'bun:test';
import { coreMockState, installCoreModuleMocks, resetCoreMockState } from './core-mock-state';

installCoreModuleMocks();

let transfer: typeof import('../../src/core/transfer.js');
let account: typeof import('../../src/core/account.js');

beforeAll(async () => {
  account = await import('../../src/core/account.js');
  transfer = await import('../../src/core/transfer.js');
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
  coreMockState.callViewMethodImpl = async (
    _rpc: string,
    contractAddress: string,
    method: string,
    payload: any,
  ) => {
    if (contractAddress === 'CA' && method === 'GetHolderInfo') {
      expect(payload.caHash).toBeTruthy();
      return {
        caHash: payload.caHash,
        caAddress: 'ELF_ca_tDVV',
        managerInfos: [{ address: wallet.address, extraData: '' }],
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

const wallet = { address: 'ELF_wallet', privateKey: 'pk' } as any;

describe('core/transfer', () => {
  test('sameChainTransfer validates params and returns tx info', async () => {
    await expect(
      transfer.sameChainTransfer(config, wallet, {
        caHash: '',
        tokenContractAddress: 'TOKEN',
        symbol: 'ELF',
        to: 'ELF_to',
        amount: '1',
        chainId: 'tDVV',
      } as any),
    ).rejects.toThrow('caHash is required');

    let holderInfoChecks = 0;
    coreMockState.callViewMethodImpl = async (
      _rpc: string,
      contractAddress: string,
      method: string,
      payload: any,
    ) => {
      if (contractAddress === 'CA' && method === 'GetHolderInfo') {
        holderInfoChecks += 1;
        expect(payload.caHash).toBeTruthy();
        return {
          caHash: payload.caHash,
          caAddress: 'ELF_ca_tDVV',
          managerInfos: [{ address: wallet.address, extraData: '' }],
          guardianList: { guardians: [] },
        };
      }
      throw new Error(`Unexpected view call ${contractAddress}.${method}`);
    };
    coreMockState.callSendMethodImpl = async (
      _rpc: string,
      _caContract: string,
      _wallet: any,
      method: string,
      payload: any,
    ) => {
      expect(method).toBe('ManagerForwardCall');
      expect(payload.encodedInput).toBe('0xmock');
      return { transactionId: 'same-tx', data: { Status: 'MINED' } };
    };

    const result = await transfer.sameChainTransfer(config, wallet, {
      caHash: 'hash',
      tokenContractAddress: 'TOKEN',
      symbol: 'ELF',
      to: 'ELF_to',
      amount: '1',
      chainId: 'tDVV',
      memo: 'memo',
    });

    expect(result).toEqual({
      transactionId: 'same-tx',
      status: 'MINED',
      feePreview: {
        transactionFee: { ELF: '1000000' },
        transactionFees: {
          ChargingAddress: 'ELF_fee_payer',
          Fee: { ELF: '1000000' },
        },
        chargingAddress: 'ELF_fee_payer',
        isCaPayingFee: false,
        feeSymbol: 'ELF',
        feeAmount: '1000000',
      },
    });
    expect(holderInfoChecks).toBe(1);
  });

  test('sameChainTransfer forwards guardiansApproved for one-time approval', async () => {
    coreMockState.callSendMethodImpl = async (
      _rpc: string,
      _caContract: string,
      _wallet: any,
      method: string,
      payload: any,
    ) => {
      expect(method).toBe('ManagerForwardCall');
      expect(payload.guardiansApproved).toHaveLength(1);
      expect(payload.guardiansApproved[0].verificationInfo.id).toBe('verifier-1');
      return { transactionId: 'same-guardian', data: { Status: 'MINED' } };
    };

    const result = await transfer.sameChainTransfer(config, wallet, {
      caHash: 'hash',
      tokenContractAddress: 'TOKEN',
      symbol: 'AIBOUNTY',
      to: 'ELF_to',
      amount: '10000000',
      chainId: 'tDVV',
      guardiansApproved: [
        {
          identifier: 'user@example.com',
          type: 0,
          verifierId: 'verifier-1',
          verificationDoc: '0,identifierHashFromDoc,1,2,3,10,1866392',
          signature: 'abcd',
        },
      ],
    });

    expect(result.transactionId).toBe('same-guardian');
    expect(result.status).toBe('MINED');
  });

  test('sameChainTransfer blocks when manager is not synced on target chain', async () => {
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

    await expect(
      transfer.sameChainTransfer(config, wallet, {
        caHash: 'hash',
        tokenContractAddress: 'TOKEN',
        symbol: 'ELF',
        to: 'ELF_to',
        amount: '1',
        chainId: 'tDVV',
      }),
    ).rejects.toThrow('Manager ELF_wallet is not yet synced on tDVV');
  });

  test('crossChainTransfer throws when step1 is not mined', async () => {
    coreMockState.callSendMethodImpl = async (
      _rpc: string,
      _caContract: string,
      _wallet: any,
      method: string,
    ) => {
      if (method === 'ManagerForwardCall') {
        return { transactionId: 'step1', data: { Status: 'FAILED', Error: 'insufficient' } };
      }
      return { transactionId: 'step2', data: { Status: 'MINED' } };
    };

    await expect(
      transfer.crossChainTransfer(config, wallet, {
        caHash: 'hash',
        tokenContractAddress: 'TOKEN',
        symbol: 'ELF',
        to: 'ELF_to',
        amount: '1',
        chainId: 'tDVV',
        toChainId: 'AELF',
      }),
    ).rejects.toThrow('Cross-chain step 1 failed');
  });

  test('crossChainTransfer throws recovery message when step2 fails', async () => {
    coreMockState.callSendMethodImpl = async (
      _rpc: string,
      _caContract: string,
      _wallet: any,
      method: string,
    ) => {
      if (method === 'ManagerForwardCall') {
        return { transactionId: 'step1-success', data: { Status: 'MINED' } };
      }
      throw new Error('rpc timeout');
    };

    await expect(
      transfer.crossChainTransfer(config, wallet, {
        caHash: 'hash',
        tokenContractAddress: 'TOKEN',
        symbol: 'ELF',
        to: 'ELF_to',
        amount: '100',
        chainId: 'tDVV',
        toChainId: 'AELF',
      }),
    ).rejects.toThrow('RECOVERY NEEDED');
  });

  test('crossChainTransfer succeeds', async () => {
    coreMockState.callSendMethodImpl = async (
      _rpc: string,
      _contract: string,
      _wallet: any,
      method: string,
    ) => {
      if (method === 'ManagerForwardCall') {
        return { transactionId: 'step1', data: { Status: 'MINED' } };
      }
      expect(method).toBe('CrossChainTransfer');
      return { transactionId: 'step2', data: { Status: 'MINED' } };
    };

    const result = await transfer.crossChainTransfer(config, wallet, {
      caHash: 'hash',
      tokenContractAddress: 'TOKEN',
      symbol: 'ELF',
      to: 'ELF_to',
      amount: '100',
      chainId: 'tDVV',
      toChainId: 'AELF',
      issueChainId: 1866392,
    });

    expect(result.transactionId).toBe('step2');
    expect(result.feePreview?.isCaPayingFee).toBe(false);
  });

  test('recoverStuckTransfer sends token back to CA', async () => {
    coreMockState.callSendMethodImpl = async (_rpc: string, _contract: string, _wallet: any, method: string, payload: any) => {
      expect(method).toBe('Transfer');
      expect(payload.to).toBe('ELF_ca_tDVV');
      return { transactionId: 'recover-tx', data: { Status: 'MINED' } };
    };

    const result = await transfer.recoverStuckTransfer(config, wallet, {
      tokenContractAddress: 'TOKEN',
      symbol: 'ELF',
      amount: '100',
      caAddress: 'ELF_ca_tDVV',
      chainId: 'tDVV',
    });

    expect(result).toEqual({ transactionId: 'recover-tx', status: 'MINED' });
  });

  test('getTransactionResult validates params and queries tx result', async () => {
    await expect(
      transfer.getTransactionResult(config, { txId: '', chainId: 'tDVV' } as any),
    ).rejects.toThrow('txId is required');

    coreMockState.getTxResultImpl = async (_rpc: string, txId: string) => {
      expect(txId).toBe('abc123');
      return { Status: 'MINED', TransactionId: txId };
    };

    const result = await transfer.getTransactionResult(config, {
      txId: 'abc123',
      chainId: 'tDVV',
    });

    expect((result as any).Status).toBe('MINED');
  });
});
