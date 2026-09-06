import { afterEach, beforeEach, describe, expect, test } from 'bun:test';
import { resetConfigCache } from '../../src/core/config.js';
import { callSend, callView, clearAelfCache, packInput } from '../../src/core/chain-client.js';
import { restoreTestEnv, resetTestEnv } from '../helpers/env.js';

describe('chain client', () => {
  beforeEach(() => {
    resetTestEnv({
      TMRW_PRIVATE_KEY: undefined,
      TMRW_RPC_AELF: 'https://aelf-public-node.aelf.io',
      TMRW_RPC_TDVV: 'https://tdvv-public-node.aelf.io',
    });
    resetConfigCache();
  });

  afterEach(() => {
    resetConfigCache();
    restoreTestEnv();
  });

  test('callSend simulate returns encoded request payload', async () => {
    const result = await callSend(
      {
        chainId: 'AELF',
        contractAddress: 'contract-1',
        methodName: 'Vote',
        args: { proposalId: 'p-1' },
      },
      { mode: 'simulate' },
    );

    expect(result.simulated).toBeTrue();
    expect((result.result as any).methodName).toBe('Vote');
  });

  test('callSend send requires signer context or private key', async () => {
    await expect(
      callSend(
        {
          chainId: 'AELF',
          contractAddress: 'contract-1',
          methodName: 'Vote',
          args: { proposalId: 'p-1' },
        },
        { mode: 'send' },
      ),
    ).rejects.toMatchObject({
      code: 'SIGNER_CONTEXT_NOT_FOUND',
    });
  });

  test('callSend send rejects direct contract send for explicit CA signer context', async () => {
    await expect(
      callSend(
        {
          chainId: 'AELF',
          contractAddress: 'contract-1',
          methodName: 'Vote',
          args: { proposalId: 'p-1' },
        },
        {
          mode: 'send',
          privateKey: '1'.repeat(64),
          signerContext: {
            signerMode: 'explicit',
            walletType: 'CA',
            caHash: 'ca_hash_1',
            caAddress: 'ELF_ca_1_AELF',
          },
        },
      ),
    ).rejects.toMatchObject({
      code: 'SIGNER_CA_DIRECT_SEND_FORBIDDEN',
    });
  });

  test('callSend send rejects env fallback when CA identity markers are present', async () => {
    resetTestEnv({
      TMRW_PRIVATE_KEY: '1'.repeat(64),
      PORTKEY_CA_HASH: 'ca_hash_env',
      PORTKEY_CA_ADDRESS: 'ELF_ca_env_AELF',
    });
    resetConfigCache();

    await expect(
      callSend(
        {
          chainId: 'AELF',
          contractAddress: 'contract-1',
          methodName: 'Vote',
          args: { proposalId: 'p-1' },
        },
        { mode: 'send' },
      ),
    ).rejects.toMatchObject({
      code: 'SIGNER_CA_DIRECT_SEND_FORBIDDEN',
    });
  });

  test('callSend simulate still works for CA signer context', async () => {
    const result = await callSend(
      {
        chainId: 'AELF',
        contractAddress: 'contract-1',
        methodName: 'Vote',
        args: { proposalId: 'p-1' },
      },
      {
        mode: 'simulate',
        signerContext: {
          signerMode: 'explicit',
          walletType: 'CA',
          caHash: 'ca_hash_1',
          caAddress: 'ELF_ca_1_AELF',
        },
      },
    );

    expect(result.simulated).toBeTrue();
    expect((result.result as any).methodName).toBe('Vote');
  });

  test('callView rejects unsupported chain before rpc request', async () => {
    await expect(
      callView({
        chainId: 'UNKNOWN' as any,
        contractAddress: 'contract-1',
        methodName: 'View',
        args: {},
      }),
    ).rejects.toMatchObject({
      code: 'UNSUPPORTED_CHAIN',
    });
  });

  test('callSend send rejects unsupported chain when private key exists', async () => {
    resetTestEnv({
      TMRW_PRIVATE_KEY: '1'.repeat(64),
    });
    resetConfigCache();

    await expect(
      callSend(
        {
          chainId: 'UNKNOWN' as any,
          contractAddress: 'contract-1',
          methodName: 'Vote',
          args: {},
        },
        { mode: 'send' },
      ),
    ).rejects.toMatchObject({
      code: 'UNSUPPORTED_CHAIN',
    });
  });

  test('packInput rejects unsupported chain', async () => {
    await expect(packInput('UNKNOWN' as any, 'contract-1', 'Vote', {})).rejects.toMatchObject({
      code: 'UNSUPPORTED_CHAIN',
    });
  });

  test('clearAelfCache is callable for long-lived process cleanup', () => {
    expect(() => clearAelfCache()).not.toThrow();
  });
});
