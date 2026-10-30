import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import test from 'node:test';
import { fileURLToPath } from 'node:url';

for (const name of ['find-package-symbol', 'review-route']) {
  test(`recipe-cook ${name}`, () => {
    const result = spawnSync('bash', [fileURLToPath(new URL(`${name}.test.sh`, import.meta.url))], { encoding: 'utf8' });
    assert.equal(result.status, 0, `${result.stdout}\n${result.stderr}`);
  });
}
