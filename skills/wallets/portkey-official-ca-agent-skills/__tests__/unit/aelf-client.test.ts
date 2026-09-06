import { describe, expect, it } from 'bun:test';
import { spawnSync } from 'node:child_process';
import * as path from 'node:path';
import { fileURLToPath } from 'node:url';

type AelfClientCheckResult = {
  walletAddress: string;
  walletPrivateKeyLength: number;
  mnemonicWordCount: number;
  uniqueAddresses: boolean;
  uniquePrivateKeys: boolean;
  restoredMatches: boolean;
  shortKeyAddressDefined: boolean;
  clearCachesOk: boolean;
};

function runAelfClientCheck(): AelfClientCheckResult {
  const testDir = path.dirname(fileURLToPath(import.meta.url));
  const helperPath = path.join(testDir, 'helpers', 'aelf-client-real-check.ts');
  const repoRoot = path.resolve(testDir, '..', '..');
  const result = spawnSync(process.execPath, [helperPath], {
    cwd: repoRoot,
    env: process.env,
    encoding: 'utf8',
  });

  if (result.status !== 0) {
    throw new Error(
      [
        `Isolated aelf-client check failed with exit code ${result.status ?? 'unknown'}.`,
        result.stderr?.trim(),
        result.stdout?.trim(),
      ]
        .filter(Boolean)
        .join('\n'),
    );
  }

  const lines = (result.stdout ?? '')
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean);
  const payload = lines.at(-1);

  if (!payload) {
    throw new Error('Isolated aelf-client check did not emit JSON output.');
  }

  return JSON.parse(payload) as AelfClientCheckResult;
}

describe('lib/aelf-client', () => {
  // Run in a subprocess because Bun module mocks leak across the full unit suite.
  it('validates wallet helpers with the real module implementation', () => {
    const result = runAelfClientCheck();

    expect(result.walletAddress).toBeDefined();
    expect(result.walletPrivateKeyLength).toBe(64);
    expect(result.mnemonicWordCount).toBe(12);
    expect(result.uniqueAddresses).toBe(true);
    expect(result.uniquePrivateKeys).toBe(true);
    expect(result.restoredMatches).toBe(true);
    expect(result.shortKeyAddressDefined).toBe(true);
    expect(result.clearCachesOk).toBe(true);
  });
});
