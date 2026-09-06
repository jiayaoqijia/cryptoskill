import { afterEach, beforeEach, describe, expect, test } from 'bun:test';
import { mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import AElf from 'aelf-sdk';
import { getKeystore } from 'aelf-sdk/src/util/keyStore.js';
import { resolveSignerContext, SignerContextError } from '../../lib/signer-context';
import { setActiveWalletProfile } from '../../lib/wallet-context';

describe('signer context resolver', () => {
  let tempDir: string | null = null;

  const clearSignerEnv = () => {
    delete process.env.PORTKEY_SKILL_WALLET_CONTEXT_PATH;
    delete process.env.PORTKEY_WALLET_PASSWORD;
    delete process.env.PORTKEY_PRIVATE_KEY;
    delete process.env.AELF_PRIVATE_KEY;
    delete process.env.EFOREST_PRIVATE_KEY;
    delete process.env.TMRW_PRIVATE_KEY;
    delete process.env.PORTKEY_CA_HASH;
    delete process.env.PORTKEY_CA_ADDRESS;
    delete process.env.PORTKEY_CA_KEYSTORE_PASSWORD;
  };

  const expectSignerErrorCode = (
    action: () => unknown,
    expectedCode: string,
  ) => {
    try {
      action();
      throw new Error('Expected signer context action to throw');
    } catch (error) {
      expect(error).toBeInstanceOf(SignerContextError);
      expect((error as SignerContextError).code).toBe(expectedCode);
    }
  };

  beforeEach(() => {
    clearSignerEnv();
  });

  afterEach(() => {
    clearSignerEnv();
    if (tempDir) {
      rmSync(tempDir, { recursive: true, force: true });
      tempDir = null;
    }
  });

  test('resolves explicit signer from private key', () => {
    const wallet = AElf.wallet.createNewWallet();
    const result = resolveSignerContext({
      signerMode: 'explicit',
      privateKey: wallet.privateKey,
    });
    expect(result.provider).toBe('explicit');
    expect(result.identity.walletType).toBe('EOA');
  });

  test('resolves active EOA wallet context with password env', () => {
    tempDir = mkdtempSync(join(tmpdir(), 'awaken-signer-context-'));
    const contextPath = join(tempDir, 'context.v1.json');
    const walletFile = join(tempDir, 'wallet.json');
    process.env.PORTKEY_SKILL_WALLET_CONTEXT_PATH = contextPath;

    const password = 'test-pass';
    const wallet = AElf.wallet.createNewWallet();
    writeFileSync(
      walletFile,
      JSON.stringify(
        {
          address: wallet.address,
          AESEncryptPrivateKey: AElf.wallet.AESEncrypt(wallet.privateKey, password),
        },
        null,
        2,
      ),
    );

    setActiveWalletProfile(
      {
        walletType: 'EOA',
        source: 'eoa-local',
        address: wallet.address,
        walletFile,
      },
      { skill: 'test', version: '0.0.0' },
    );

    process.env.PORTKEY_WALLET_PASSWORD = password;
    const resolved = resolveSignerContext({ signerMode: 'context' });
    expect(resolved.provider).toBe('context');
    expect(resolved.identity.walletType).toBe('EOA');
  });

  test('daemon mode reports not implemented', () => {
    expect(() => resolveSignerContext({ signerMode: 'daemon' })).toThrow(
      SignerContextError,
    );
  });

  test('auto mode falls back to env when context is invalid', () => {
    tempDir = mkdtempSync(join(tmpdir(), 'awaken-signer-context-invalid-'));
    process.env.PORTKEY_SKILL_WALLET_CONTEXT_PATH = join(tempDir, 'context.v1.json');
    setActiveWalletProfile(
      {
        walletType: 'EOA',
        source: 'eoa-local',
        address: 'ELF_missing_AELF',
        walletFile: join(tempDir, 'missing-wallet.json'),
      },
      { skill: 'test', version: '0.0.0' },
    );
    const envWallet = AElf.wallet.createNewWallet();
    process.env.PORTKEY_PRIVATE_KEY = envWallet.privateKey;

    const resolved = resolveSignerContext({ signerMode: 'auto' });
    expect(resolved.provider).toBe('env');
    expect(resolved.identity.walletType).toBe('EOA');
  });

  test('context mode throws SIGNER_CONTEXT_INVALID for broken wallet file', () => {
    tempDir = mkdtempSync(join(tmpdir(), 'awaken-signer-context-broken-'));
    process.env.PORTKEY_SKILL_WALLET_CONTEXT_PATH = join(tempDir, 'context.v1.json');
    setActiveWalletProfile(
      {
        walletType: 'EOA',
        source: 'eoa-local',
        address: 'ELF_missing_AELF',
        walletFile: join(tempDir, 'missing-wallet.json'),
      },
      { skill: 'test', version: '0.0.0' },
    );
    process.env.PORTKEY_WALLET_PASSWORD = 'any';
    expectSignerErrorCode(
      () => resolveSignerContext({ signerMode: 'context' }),
      'SIGNER_CONTEXT_INVALID',
    );
  });

  test('resolves active CA keystore context with password env', () => {
    tempDir = mkdtempSync(join(tmpdir(), 'awaken-signer-context-ca-'));
    const contextPath = join(tempDir, 'context.v1.json');
    const keystoreFile = join(tempDir, 'ca.keystore.json');
    process.env.PORTKEY_SKILL_WALLET_CONTEXT_PATH = contextPath;

    const password = 'ca-secret';
    const managerWallet = AElf.wallet.createNewWallet();
    const keystore = getKeystore(
      {
        privateKey: managerWallet.privateKey,
        mnemonic: managerWallet.mnemonic,
        address: managerWallet.address,
      },
      password,
    ) as Record<string, unknown>;
    writeFileSync(
      keystoreFile,
      JSON.stringify(
        {
          caHash: 'ca_hash_1',
          caAddress: 'ELF_ca_1_AELF',
          keystore,
        },
        null,
        2,
      ),
    );

    setActiveWalletProfile(
      {
        walletType: 'CA',
        source: 'ca-keystore',
        network: 'mainnet',
        address: managerWallet.address,
        caAddress: 'ELF_ca_1_AELF',
        caHash: 'ca_hash_1',
        keystoreFile,
      },
      { skill: 'test', version: '0.0.0' },
    );

    process.env.PORTKEY_CA_KEYSTORE_PASSWORD = password;
    const resolved = resolveSignerContext({ signerMode: 'context' });
    expect(resolved.provider).toBe('context');
    expect(resolved.identity.walletType).toBe('CA');
    expect(resolved.identity.caAddress).toBe('ELF_ca_1_AELF');
  });

  test('returns SIGNER_CONTEXT_NOT_FOUND when explicit/context/env all unavailable', () => {
    expectSignerErrorCode(
      () => resolveSignerContext({ signerMode: 'auto' }),
      'SIGNER_CONTEXT_NOT_FOUND',
    );
  });
});
