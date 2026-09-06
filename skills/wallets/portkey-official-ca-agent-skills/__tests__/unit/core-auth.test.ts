import { beforeAll, beforeEach, describe, expect, test } from 'bun:test';
import { coreMockState, installCoreModuleMocks, resetCoreMockState } from './core-mock-state';

installCoreModuleMocks();

let auth: typeof import('../../src/core/auth.js');

beforeAll(async () => {
  auth = await import('../../src/core/auth.js');
});

beforeEach(() => {
  resetCoreMockState();
});

const config = {
  apiUrl: 'https://api.portkey',
  eoaApiUrl: 'https://eoa-api.portkey',
  graphqlUrl: 'https://gql.portkey',
  network: 'mainnet' as const,
  eoaFallbackEnabled: true,
  eoaFallbackRetryCount: 2,
  eoaFallbackRetryDelayMs: 200,
};

describe('core/auth', () => {
  test('getVerifierServer returns verifier item', async () => {
    coreMockState.httpPostImpl = async () => ({ id: 'v1', name: 'Verifier-1' });

    const result = await auth.getVerifierServer(config, { chainId: 'AELF' });
    expect(result.id).toBe('v1');
    expect(coreMockState.httpCalls[0]?.path).toBe('/api/app/account/getVerifierServer');
  });

  test('getVerifierServer requires chainId', async () => {
    await expect(auth.getVerifierServer(config, {} as any)).rejects.toThrow('chainId is required');
  });

  test('getVerifierServer throws when verifier not returned', async () => {
    coreMockState.httpPostImpl = async () => ({ id: '' });
    await expect(auth.getVerifierServer(config, { chainId: 'tDVV' })).rejects.toThrow('Failed to get verifier server');
  });

  test('sendVerificationCode validates required params', async () => {
    await expect(
      auth.sendVerificationCode(config, {
        email: '',
        verifierId: 'v1',
        chainId: 'tDVV',
        operationType: 1,
      } as any),
    ).rejects.toThrow('email is required');
  });

  test('sendVerificationCode returns verifierSessionId', async () => {
    coreMockState.httpPostImpl = async () => ({ verifierSessionId: 'session-1' });

    const result = await auth.sendVerificationCode(config, {
      email: 'u@a.com',
      verifierId: 'v1',
      chainId: 'tDVV',
      operationType: 1,
    });

    expect(result.verifierSessionId).toBe('session-1');
  });

  test('verifyCode requires signature + verificationDoc in response', async () => {
    coreMockState.httpPostImpl = async () => ({ signature: '', verificationDoc: '' });

    await expect(
      auth.verifyCode(config, {
        email: 'u@a.com',
        verificationCode: '123456',
        verifierId: 'v1',
        verifierSessionId: 's1',
        chainId: 'tDVV',
        operationType: 1,
      }),
    ).rejects.toThrow('Verification failed');
  });

  test('verifyCode success', async () => {
    coreMockState.httpPostImpl = async () => ({ signature: 'sig', verificationDoc: 'doc' });

    const result = await auth.verifyCode(config, {
      email: 'u@a.com',
      verificationCode: '123456',
      verifierId: 'v1',
      verifierSessionId: 's1',
      chainId: 'tDVV',
      operationType: 1,
    });

    expect(result.signature).toBe('sig');
    expect(result.verificationDoc).toBe('doc');
  });

  test('registerWallet validates params and success/failure branches', async () => {
    await expect(
      auth.registerWallet(config, {
        email: '',
        manager: 'mgr',
        verifierId: 'v1',
        verificationDoc: 'doc',
        signature: 'sig',
        chainId: 'tDVV',
      } as any),
    ).rejects.toThrow('email is required');

    coreMockState.httpPostImpl = async () => ({ sessionId: '' });
    await expect(
      auth.registerWallet(config, {
        email: 'u@a.com',
        manager: 'mgr',
        verifierId: 'v1',
        verificationDoc: 'doc',
        signature: 'sig',
        chainId: 'tDVV',
      }),
    ).rejects.toThrow('Registration request failed');

    coreMockState.httpPostImpl = async () => ({ sessionId: 'reg-1' });
    const ok = await auth.registerWallet(config, {
      email: 'u@a.com',
      manager: 'mgr',
      verifierId: 'v1',
      verificationDoc: 'doc',
      signature: 'sig',
      chainId: 'tDVV',
    });
    expect(ok.sessionId).toBe('reg-1');
  });

  test('recoverWallet validates params and success/failure branches', async () => {
    await expect(
      auth.recoverWallet(config, {
        email: 'u@a.com',
        manager: 'mgr',
        guardiansApproved: [],
        chainId: 'tDVV',
      } as any),
    ).rejects.toThrow('guardiansApproved is required');

    coreMockState.httpPostImpl = async () => ({ sessionId: '' });
    await expect(
      auth.recoverWallet(config, {
        email: 'u@a.com',
        manager: 'mgr',
        chainId: 'tDVV',
        guardiansApproved: [
          {
            type: 0,
            identifier: 'u@a.com',
            verifierId: 'v1',
            verificationDoc: '0,a,b,c,d,2,1866392',
            signature: 'sig',
          },
        ],
      }),
    ).rejects.toThrow('Recovery request failed');

    coreMockState.httpPostImpl = async () => ({ sessionId: 'recover-1' });
    const ok = await auth.recoverWallet(config, {
      email: 'u@a.com',
      manager: 'mgr',
      chainId: 'tDVV',
      guardiansApproved: [
        {
          type: 0,
          identifier: 'u@a.com',
          verifierId: 'v1',
          verificationDoc: '0,a,b,c,d,2,1866392',
          signature: 'sig',
        },
      ],
    });
    expect(ok.sessionId).toBe('recover-1');
  });

  test('recoverWallet rejects malformed guardiansApproved payload', async () => {
    await expect(
      auth.recoverWallet(config, {
        email: 'u@a.com',
        manager: 'mgr',
        chainId: 'tDVV',
        guardiansApproved: [
          {
            type: 0,
            identifier: '',
            verifierId: 'v1',
            verificationDoc: '0,a,b,c,d,2,1866392',
            signature: 'sig',
          },
        ] as any,
      }),
    ).rejects.toThrow('guardiansApproved[0].identifier is required');

    await expect(
      auth.recoverWallet(config, {
        email: 'u@a.com',
        manager: 'mgr',
        chainId: 'AELF',
        guardiansApproved: [
          {
            type: 'Email',
            identifier: 'u@a.com',
            verifierId: 'v1',
            verificationDoc: '0,a,b,c,d,1,1866392',
            signature: 'sig',
          },
        ] as any,
      }),
    ).rejects.toThrow('operation "recovery"');
  });

  test('checkRegisterOrRecoveryStatus handles pending/pass/fail', async () => {
    coreMockState.httpGetImpl = async () => ({ items: [] });
    const pending = await auth.checkRegisterOrRecoveryStatus(config, {
      sessionId: 's1',
      type: 'register',
    });
    expect(pending).toEqual({ status: 'pending' });

    coreMockState.httpGetImpl = async () => ({
      items: [{ registerStatus: 'pass', caAddress: 'ELF_addr_tDVV', caHash: 'hash1' }],
    });
    const pass = await auth.checkRegisterOrRecoveryStatus(config, {
      sessionId: 's2',
      type: 'register',
    });
    expect(pass.status).toBe('pass');
    expect((pass as any).caHash).toBe('hash1');

    coreMockState.httpGetImpl = async () => ({
      items: [{ recoveryStatus: 'fail', recoveryMessage: 'bad code' }],
    });
    const fail = await auth.checkRegisterOrRecoveryStatus(config, {
      sessionId: 's3',
      type: 'recovery',
    });
    expect(fail).toEqual({ status: 'fail', failMessage: 'bad code' });

    coreMockState.httpGetImpl = async () => ({ items: [{ registerStatus: 'pending' }] });
    const pending2 = await auth.checkRegisterOrRecoveryStatus(config, {
      sessionId: 's4',
      type: 'register',
    });
    expect(pending2).toEqual({ status: 'pending' });
  });

  test('checkRegisterOrRecoveryStatus maps known recovery failure hints', async () => {
    coreMockState.httpGetImpl = async () => ({
      items: [
        {
          recoveryStatus: 'fail',
          recoveryMessage: 'Transaction status: NODEVALIDATIONFAILED. Error: AElf.Sdk.CSharp.AssertionException: Please complete the approval of all guardians',
        },
      ],
    });

    const approvalFail = await auth.checkRegisterOrRecoveryStatus(config, {
      sessionId: 's5',
      type: 'recovery',
    });
    expect(approvalFail.status).toBe('fail');
    expect(approvalFail.failMessage).toContain('verify-code --operation recovery');

    coreMockState.httpGetImpl = async () => ({
      items: [
        {
          recoveryStatus: 'fail',
          recoveryMessage: 'Error mapping types.\nDestination Member:\nGuardianApproved\n',
        },
      ],
    });

    const mappingFail = await auth.checkRegisterOrRecoveryStatus(config, {
      sessionId: 's6',
      type: 'recovery',
    });
    expect(mappingFail.status).toBe('fail');
    expect(mappingFail.failMessage).toContain('guardiansApproved must include');
  });
});
