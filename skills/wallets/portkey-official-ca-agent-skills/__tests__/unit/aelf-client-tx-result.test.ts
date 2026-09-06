import { describe, expect, it } from 'bun:test';
import { spawnSync } from 'node:child_process';
import * as path from 'node:path';
import { fileURLToPath } from 'node:url';

type TxResultCheck = {
  terminalError: string;
  pendingError: string;
  longTailMinedStatus: string;
  notExistedError: string;
};

function runTxResultCheck(): TxResultCheck {
  const testDir = path.dirname(fileURLToPath(import.meta.url));
  const helperPath = path.join(testDir, 'helpers', 'aelf-client-tx-result-check.ts');
  const repoRoot = path.resolve(testDir, '..', '..');
  const result = spawnSync(process.execPath, [helperPath], {
    cwd: repoRoot,
    env: process.env,
    encoding: 'utf8',
  });

  if (result.status !== 0) {
    throw new Error(
      [
        `Isolated aelf-client tx-result check failed with exit code ${result.status ?? 'unknown'}.`,
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
    throw new Error('Isolated aelf-client tx-result check did not emit JSON output.');
  }

  return JSON.parse(payload) as TxResultCheck;
}

describe('lib/aelf-client getTxResult', () => {
  it('surfaces original terminal errors and preserves long-tail polling states in isolated execution', () => {
    const result = runTxResultCheck();

    expect(result.terminalError).toContain('Transaction tx-validation NODEVALIDATIONFAILED');
    expect(result.terminalError).toContain('Low transfer security level.');
    expect(result.pendingError).toContain('Transaction tx-pending PENDING_VALIDATION');
    expect(result.longTailMinedStatus).toBe('MINED');
    expect(result.notExistedError).toContain('Transaction tx-not-existed NOTEXISTED');
  });
});
