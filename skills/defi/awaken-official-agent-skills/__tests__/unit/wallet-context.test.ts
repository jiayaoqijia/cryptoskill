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
} from '../../lib/wallet-context';

describe('wallet context storage', () => {
  let tempDir = '';
  let contextPath = '';

  const writer = {
    skill: 'unit-test',
    version: '0.0.0',
  };

  beforeEach(() => {
    tempDir = join(tmpdir(), `awaken-wallet-context-${Date.now()}-${Math.random()}`);
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
        walletType: 'EOA',
        source: 'eoa-local',
        address: 'ELF_awaken_AELF',
        walletFile: '/tmp/wallet.json',
      },
      writer,
    );
    expect(result.activeProfileId).toBe('default');
    expect(existsSync(contextPath)).toBeTrue();
    expect(readWalletContext()?.profiles.default?.address).toBe('ELF_awaken_AELF');
  });

  test('writes secure file permissions on unix-like platforms', () => {
    setActiveWalletProfile(
      {
        walletType: 'EOA',
        source: 'eoa-local',
        address: 'ELF_perm_AELF',
        walletFile: '/tmp/wallet.json',
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
          walletType: 'EOA',
          source: 'eoa-local',
          address: 'ELF_lock_AELF',
          walletFile: '/tmp/wallet.json',
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
        walletType: 'EOA',
        source: 'eoa-local',
        address: 'ELF_stale_AELF',
        walletFile: '/tmp/wallet.json',
      },
      writer,
    );
    expect(result.profiles.default?.address).toBe('ELF_stale_AELF');
    expect(existsSync(lockPath)).toBeFalse();
  });

  test('context file does not include plaintext private key', () => {
    setActiveWalletProfile(
      {
        walletType: 'EOA',
        source: 'eoa-local',
        address: 'ELF_safe_AELF',
        walletFile: '/tmp/wallet.json',
      },
      writer,
    );
    const raw = readFileSync(contextPath, 'utf8');
    expect(raw.includes('privateKey')).toBeFalse();
  });

  test('last write wins and lastWriter is updated', () => {
    setActiveWalletProfile(
      {
        walletType: 'EOA',
        source: 'eoa-local',
        address: 'ELF_first_AELF',
        walletFile: '/tmp/first.json',
      },
      writer,
    );
    const secondWriter = { skill: 'unit-test-2', version: '0.0.1' };
    const second = setActiveWalletProfile(
      {
        walletType: 'EOA',
        source: 'eoa-local',
        address: 'ELF_second_AELF',
        walletFile: '/tmp/second.json',
      },
      secondWriter,
    );
    expect(second.profiles.default?.address).toBe('ELF_second_AELF');
    expect(second.lastWriter.skill).toBe('unit-test-2');
  });
});
