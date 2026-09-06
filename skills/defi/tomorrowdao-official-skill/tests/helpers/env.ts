import { rmSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const ORIGINAL_ENV = { ...process.env };
const ISOLATED_CONTEXT_PATH = path.join(os.tmpdir(), 'tomorrowdao-skill-wallet-context.test.json');
const CLEARED_ENV_KEYS = [
  'PORTKEY_WALLET_PASSWORD',
  'PORTKEY_PRIVATE_KEY',
  'AELF_PRIVATE_KEY',
  'EFOREST_PRIVATE_KEY',
  'PORTKEY_CA_HASH',
  'PORTKEY_CA_ADDRESS',
  'PORTKEY_CA_KEYSTORE_PASSWORD',
];

export function resetTestEnv(overrides: Record<string, string | undefined> = {}): void {
  process.env = { ...ORIGINAL_ENV };
  rmSync(ISOLATED_CONTEXT_PATH, { force: true });

  for (const key of CLEARED_ENV_KEYS) {
    delete process.env[key];
  }

  process.env.PORTKEY_SKILL_WALLET_CONTEXT_PATH = ISOLATED_CONTEXT_PATH;

  Object.entries(overrides).forEach(([key, value]) => {
    if (value === undefined) {
      delete process.env[key];
      return;
    }
    process.env[key] = value;
  });
}

export function restoreTestEnv(): void {
  rmSync(ISOLATED_CONTEXT_PATH, { force: true });
  process.env = { ...ORIGINAL_ENV };
}
