import { describe, expect, it } from 'bun:test';
import { spawnSync } from 'node:child_process';
import * as path from 'node:path';
import { fileURLToPath } from 'node:url';

type ViewCallCheckResult = {
  walletAddress: string;
  walletHasKeyPair: boolean;
  paramsEcho: string;
  balance: string;
  emptyCallArgCount: number;
  configValue: string;
};

function runViewCallCheck(): ViewCallCheckResult {
  const testDir = path.dirname(fileURLToPath(import.meta.url));
  const helperPath = path.join(testDir, 'helpers', 'aelf-client-view-call-check.ts');
  const repoRoot = path.resolve(testDir, '..', '..');
  const result = spawnSync(process.execPath, [helperPath], {
    cwd: repoRoot,
    env: process.env,
    encoding: 'utf8',
  });

  if (result.status !== 0) {
    throw new Error(
      [
        `Isolated aelf-client view-call check failed with exit code ${result.status ?? 'unknown'}.`,
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
    throw new Error('Isolated aelf-client view-call check did not emit JSON output.');
  }

  return JSON.parse(payload) as ViewCallCheckResult;
}

describe('lib/aelf-client callViewMethod', () => {
  // Run in a subprocess because Bun module mocks leak across the full unit suite.
  it('rehydrates the ephemeral wallet before binding a read-only contract', () => {
    const result = runViewCallCheck();

    expect(result.walletAddress).toBe('ELF_rehydrated_wallet');
    expect(result.walletHasKeyPair).toBe(true);
    expect(result.paramsEcho).toBe('ELF');
    expect(result.balance).toBe('123');
    expect(result.emptyCallArgCount).toBe(0);
    expect(result.configValue).toBe('config-ok');
  });
});
