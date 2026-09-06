import { afterAll, beforeAll, beforeEach, describe, expect, test } from 'bun:test';
import * as fs from 'node:fs';
import * as os from 'node:os';
import * as path from 'node:path';
import { createWallet } from '../../lib/aelf-client.js';

const originalHome = process.env.HOME;
const originalContextPath = process.env.PORTKEY_SKILL_WALLET_CONTEXT_PATH;
const testHome = fs.mkdtempSync(path.join(os.tmpdir(), 'ca-require-wallet-home-'));
process.env.HOME = testHome;
process.env.PORTKEY_SKILL_WALLET_CONTEXT_PATH = path.join(
  testHome,
  '.portkey',
  'skill-wallet',
  'context.v1.json',
);

let keystore: typeof import('../../src/core/keystore.js');
let requireWallet: typeof import('../../src/mcp/require-wallet.js')['requireWallet'];

beforeAll(async () => {
  keystore = await import('../../src/core/keystore.js');
  ({ requireWallet } = await import('../../src/mcp/require-wallet.js'));
});

beforeEach(() => {
  keystore.clearKeystoreState();
  const portkeyDir = path.join(testHome, '.portkey');
  if (fs.existsSync(portkeyDir)) {
    fs.rmSync(portkeyDir, { recursive: true, force: true });
  }
  delete process.env.PORTKEY_PRIVATE_KEY;
  delete process.env.PORTKEY_CA_HASH;
  delete process.env.PORTKEY_CA_ADDRESS;
  delete process.env.PORTKEY_CA_KEYSTORE_PASSWORD;
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

describe('mcp requireWallet', () => {
  test('prioritizes unlocked in-memory wallet', () => {
    const manager = createWallet();
    keystore.saveKeystore({
      password: 'secret',
      privateKey: manager.privateKey,
      mnemonic: manager.mnemonic!,
      caHash: 'hash_unlock',
      caAddress: 'ELF_ca_unlock_tDVV',
      originChainId: 'tDVV',
      network: 'mainnet',
    });

    const wallet = requireWallet();
    expect(wallet.address).toBe(manager.address);
  });

  test('falls back to PORTKEY_PRIVATE_KEY env when no unlocked wallet', () => {
    const envWallet = createWallet();
    process.env.PORTKEY_PRIVATE_KEY = envWallet.privateKey;
    const wallet = requireWallet();
    expect(wallet.address).toBe(envWallet.address);
  });

  test('uses active context + password env to auto unlock keystore', () => {
    const manager = createWallet();
    keystore.saveKeystore({
      password: 'secret',
      privateKey: manager.privateKey,
      mnemonic: manager.mnemonic!,
      caHash: 'hash_ctx',
      caAddress: 'ELF_ca_ctx_tDVV',
      loginEmail: 'ctx@example.com',
      originChainId: 'tDVV',
      network: 'mainnet',
    });
    keystore.lockWallet();

    process.env.PORTKEY_CA_KEYSTORE_PASSWORD = 'secret';
    const wallet = requireWallet();
    expect(wallet.address).toBe(manager.address);
  });

  test('uses active keystoreFile when loginEmail is absent', () => {
    const manager = createWallet();
    const saved = keystore.saveKeystore({
      password: 'secret',
      privateKey: manager.privateKey,
      mnemonic: manager.mnemonic!,
      caHash: 'hash_ctx_file',
      caAddress: 'ELF_ca_ctx_file_tDVV',
      loginEmail: 'file@example.com',
      originChainId: 'tDVV',
      network: 'mainnet',
    });
    keystore.lockWallet();
    keystore.setActiveWallet({
      walletType: 'CA',
      source: 'ca-keystore',
      network: 'mainnet',
      address: manager.address,
      caAddress: 'ELF_ca_ctx_file_tDVV',
      caHash: 'hash_ctx_file',
      keystoreFile: saved.keystorePath,
    });

    process.env.PORTKEY_CA_KEYSTORE_PASSWORD = 'secret';
    const wallet = requireWallet();
    expect(wallet.address).toBe(manager.address);
  });

  test('accepts loginEmail + password input for direct keystore resolution', () => {
    const manager = createWallet();
    keystore.saveKeystore({
      password: 'secret',
      privateKey: manager.privateKey,
      mnemonic: manager.mnemonic!,
      caHash: 'hash_direct_input',
      caAddress: 'ELF_direct_input_tDVV',
      loginEmail: 'direct@example.com',
      originChainId: 'AELF',
      network: 'mainnet',
    });
    keystore.lockWallet();

    const wallet = requireWallet({
      network: 'mainnet',
      loginEmail: 'direct@example.com',
      password: 'secret',
    });
    expect(wallet.address).toBe(manager.address);
  });

  test('throws SIGNER_PASSWORD_REQUIRED when active context exists without password', () => {
    const manager = createWallet();
    keystore.saveKeystore({
      password: 'secret',
      privateKey: manager.privateKey,
      mnemonic: manager.mnemonic!,
      caHash: 'hash_need_password',
      caAddress: 'ELF_ca_need_password_tDVV',
      originChainId: 'tDVV',
      network: 'mainnet',
    });
    keystore.lockWallet();

    expect(() => requireWallet()).toThrow('SIGNER_PASSWORD_REQUIRED');
  });

  test('throws SIGNER_CONTEXT_NOT_FOUND when all sources are unavailable', () => {
    expect(() => requireWallet()).toThrow('SIGNER_CONTEXT_NOT_FOUND');
  });
});
