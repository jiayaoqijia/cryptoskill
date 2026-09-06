import { describe, expect, it } from 'bun:test';
import { spawnSync } from 'node:child_process';
import * as path from 'node:path';
import { fileURLToPath } from 'node:url';

type EncodeCheckResult = {
  resolvedRequestTypeSet: boolean;
  encodedArgs: number[];
};

function runEncodeCheck(): EncodeCheckResult {
  const testDir = path.dirname(fileURLToPath(import.meta.url));
  const helperPath = path.join(testDir, 'helpers', 'aelf-client-encode-check.ts');
  const repoRoot = path.resolve(testDir, '..', '..');
  const result = spawnSync(process.execPath, [helperPath], {
    cwd: repoRoot,
    env: process.env,
    encoding: 'utf8',
  });

  if (result.status !== 0) {
    throw new Error(
      [
        `Isolated aelf-client encode check failed with exit code ${result.status ?? 'unknown'}.`,
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
    throw new Error('Isolated aelf-client encode check did not emit JSON output.');
  }

  return JSON.parse(payload) as EncodeCheckResult;
}

describe('lib/aelf-client encodeManagerForwardCallParams', () => {
  // Run in a subprocess because Bun module mocks leak across the full unit suite.
  it('resolves descriptor methods before reading resolvedRequestType', () => {
    const result = runEncodeCheck();

    expect(result.resolvedRequestTypeSet).toBe(true);
    expect(result.encodedArgs).toEqual([1, 2, 3]);
  });
});
