import { afterEach, beforeEach, describe, expect, test } from 'bun:test';
import { mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import AElf from 'aelf-sdk';
import { getKeystore } from 'aelf-sdk/src/util/keyStore.js';
import { SkillError } from '../../src/core/errors.js';
import { resolvePrivateKeyContext } from '../../src/core/signer-context.js';
import { setActiveWalletProfile } from '../../src/core/wallet-context.js';

describe('signer context', () => {
  let tempDir: string | null = null;

  const clearSignerEnv = () => {
    delete process.env.PORTKEY_SKILL_WALLET_CONTEXT_PATH;
    delete process.env.PORTKEY_WALLET_PASSWORD;
    delete process.env.TMRW_PRIVATE_KEY;
    delete process.env.PORTKEY_PRIVATE_KEY;
    delete process.env.AELF_PRIVATE_KEY;
    delete process.env.EFOREST_PRIVATE_KEY;
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
      expect(error).toBeInstanceOf(SkillError);
      expect((error as SkillError).code).toBe(expectedCode);
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

  test('resolves private key from explicit input', () => {
    const wallet = AElf.wallet.createNewWallet();
    const resolved = resolvePrivateKeyContext({
      signerMode: 'explicit',
      privateKey: wallet.privateKey,
    });
    expect(resolved.provider).toBe('explicit');
    expect(resolved.privateKey).toBe(wallet.privateKey);
  });

  test('resolves private key from active EOA context', () => {
    tempDir = mkdtempSync(join(tmpdir(), 'tomorrow-signer-context-'));
    const contextPath = join(tempDir, 'context.v1.json');
    const walletFile = join(tempDir, 'wallet.json');
    process.env.PORTKEY_SKILL_WALLET_CONTEXT_PATH = contextPath;

    const password = 'secret-pass';
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
    const resolved = resolvePrivateKeyContext({ signerMode: 'context' });
    expect(resolved.provider).toBe('context');
    expect(resolved.privateKey).toBe(wallet.privateKey);
  });

  test('auto mode falls back to env when context missing', () => {
    const wallet = AElf.wallet.createNewWallet();
    process.env.TMRW_PRIVATE_KEY = wallet.privateKey;
    const resolved = resolvePrivateKeyContext({ signerMode: 'auto' });
    expect(resolved.provider).toBe('env');
    expect(resolved.privateKey).toBe(wallet.privateKey);
  });

  test('context mode throws invalid when active wallet file is missing', () => {
    tempDir = mkdtempSync(join(tmpdir(), 'tomorrow-signer-context-invalid-'));
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
    process.env.PORTKEY_WALLET_PASSWORD = 'secret';
    expectSignerErrorCode(
      () => resolvePrivateKeyContext({ signerMode: 'context' }),
      'SIGNER_CONTEXT_INVALID',
    );
  });

  test('resolves private key from active CA context with password env', () => {
    tempDir = mkdtempSync(join(tmpdir(), 'tomorrow-signer-context-ca-'));
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
    const resolved = resolvePrivateKeyContext({ signerMode: 'context' });
    expect(resolved.provider).toBe('context');
    expect(resolved.identity.walletType).toBe('CA');
  });

  test('daemon mode reports not implemented', () => {
    expectSignerErrorCode(
      () => resolvePrivateKeyContext({ signerMode: 'daemon' }),
      'SIGNER_DAEMON_NOT_IMPLEMENTED',
    );
  });

  test('returns SIGNER_CONTEXT_NOT_FOUND when explicit/context/env all unavailable', () => {
    tempDir = mkdtempSync(join(tmpdir(), 'tomorrow-signer-context-empty-'));
    process.env.PORTKEY_SKILL_WALLET_CONTEXT_PATH = join(tempDir, 'context.v1.json');
    expectSignerErrorCode(
      () => resolvePrivateKeyContext({ signerMode: 'auto' }),
      'SIGNER_CONTEXT_NOT_FOUND',
    );
  });
});
