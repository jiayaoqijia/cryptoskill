import { afterEach, beforeEach, describe, expect, test } from 'bun:test';
import {
  existsSync,
  mkdirSync,
  readFileSync,
  rmSync,
  statSync,
  utimesSync,
  writeFileSync,
} from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import {
  readWalletContext,
  setActiveWalletProfile,
} from '../../lib/wallet-context.js';

describe('wallet context storage', () => {
  let tempDir = '';
  let contextPath = '';

  const writer = {
    skill: 'unit-test',
    version: '0.0.0',
  };

  beforeEach(() => {
    tempDir = join(tmpdir(), `ca-wallet-context-${Date.now()}-${Math.random()}`);
    contextPath = join(tempDir, 'context.v1.json');
    process.env.PORTKEY_SKILL_WALLET_CONTEXT_PATH = contextPath;
  });

  afterEach(() => {
    delete process.env.PORTKEY_SKILL_WALLET_CONTEXT_PATH;
    if (tempDir && existsSync(tempDir)) {
      rmSync(tempDir, { recursive: true, force: true });
    }
  });

  test('readWalletContext returns null when file is missing', () => {
    expect(readWalletContext()).toBeNull();
  });

  test('readWalletContext returns null when file contains invalid JSON', () => {
    mkdirSync(tempDir, { recursive: true });
    writeFileSync(contextPath, '{bad-json', 'utf8');
    expect(readWalletContext()).toBeNull();
  });

  test('setActiveWalletProfile creates directory and context file', () => {
    const result = setActiveWalletProfile(
      {
        walletType: 'CA',
        source: 'ca-keystore',
        address: 'ELF_manager_tDVV',
        caAddress: 'ELF_ca_tDVV',
        caHash: 'hash_1',
        keystoreFile: '/tmp/mainnet.keystore.json',
      },
      writer,
    );
    expect(result.activeProfileId).toBe('default');
    expect(existsSync(contextPath)).toBeTrue();
    expect(readWalletContext()?.profiles.default?.caHash).toBe('hash_1');
  });

  test('CA keystore profiles with loginEmail use stable per-account profile ids', () => {
    const result = setActiveWalletProfile(
      {
        walletType: 'CA',
        source: 'ca-keystore',
        network: 'mainnet',
        loginEmail: 'User+1@Example.com',
        address: 'ELF_manager_email_tDVV',
        caAddress: 'ELF_ca_email_tDVV',
        caHash: 'hash_email',
        keystoreFile: '/tmp/mainnet/user%40example.com.keystore.json',
      },
      writer,
    );

    expect(result.activeProfileId).toBe('ca:mainnet:user%2B1%40example.com');
    expect(result.profiles['ca:mainnet:user%2B1%40example.com']?.loginEmail).toBe(
      'user+1@example.com',
    );
  });

  test('writes secure file permissions on unix-like platforms', () => {
    setActiveWalletProfile(
      {
        walletType: 'CA',
        source: 'ca-keystore',
        address: 'ELF_perm_tDVV',
        caAddress: 'ELF_perm_ca_tDVV',
        caHash: 'hash_perm',
        keystoreFile: '/tmp/mainnet.keystore.json',
      },
      writer,
    );
    if (process.platform === 'win32') return;

    const dirMode = statSync(tempDir).mode & 0o777;
    const fileMode = statSync(contextPath).mode & 0o777;
    expect(dirMode).toBe(0o700);
    expect(fileMode).toBe(0o600);
  });

  test('throws SIGNER_CONTEXT_LOCK_TIMEOUT when lock is fresh and never released', () => {
    mkdirSync(tempDir, { recursive: true });
    const lockPath = `${contextPath}.lock`;
    writeFileSync(lockPath, 'locked', 'utf8');

    expect(() =>
      setActiveWalletProfile(
        {
          walletType: 'CA',
          source: 'ca-keystore',
          address: 'ELF_lock_tDVV',
          caAddress: 'ELF_ca_tDVV',
          caHash: 'hash_lock',
          keystoreFile: '/tmp/mainnet.keystore.json',
        },
        writer,
      ),
    ).toThrow('SIGNER_CONTEXT_LOCK_TIMEOUT');
  });

  test('cleans stale lock and continues writing', () => {
    mkdirSync(tempDir, { recursive: true });
    const lockPath = `${contextPath}.lock`;
    writeFileSync(lockPath, 'old-lock', 'utf8');
    const staleAt = new Date(Date.now() - 60_000);
    utimesSync(lockPath, staleAt, staleAt);

    const result = setActiveWalletProfile(
      {
        walletType: 'CA',
        source: 'ca-keystore',
        address: 'ELF_stale_tDVV',
        caAddress: 'ELF_ca_tDVV',
        caHash: 'hash_stale',
        keystoreFile: '/tmp/mainnet.keystore.json',
      },
      writer,
    );

    expect(result.profiles.default?.caHash).toBe('hash_stale');
    expect(existsSync(lockPath)).toBeFalse();
  });

  test('context file does not include plaintext private key', () => {
    setActiveWalletProfile(
      {
        walletType: 'CA',
        source: 'ca-keystore',
        address: 'ELF_safe_tDVV',
        caAddress: 'ELF_ca_tDVV',
        caHash: 'hash_safe',
        keystoreFile: '/tmp/mainnet.keystore.json',
      },
      writer,
    );
    const raw = readFileSync(contextPath, 'utf8');
    expect(raw.includes('privateKey')).toBeFalse();
  });

  test('last write wins and lastWriter is updated', () => {
    setActiveWalletProfile(
      {
        walletType: 'CA',
        source: 'ca-keystore',
        address: 'ELF_first_tDVV',
        caAddress: 'ELF_ca_first_tDVV',
        caHash: 'hash_first',
        keystoreFile: '/tmp/first.keystore.json',
      },
      writer,
    );
    const secondWriter = { skill: 'unit-test-2', version: '0.0.1' };
    const second = setActiveWalletProfile(
      {
        walletType: 'CA',
        source: 'ca-keystore',
        address: 'ELF_second_tDVV',
        caAddress: 'ELF_ca_second_tDVV',
        caHash: 'hash_second',
        keystoreFile: '/tmp/second.keystore.json',
      },
      secondWriter,
    );

    expect(second.profiles.default?.caHash).toBe('hash_second');
    expect(second.lastWriter.skill).toBe('unit-test-2');
  });
});
