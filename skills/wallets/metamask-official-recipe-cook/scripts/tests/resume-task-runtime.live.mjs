import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import test from 'node:test';
import path from 'node:path';
import { realpath } from 'node:fs/promises';
import { init, retainedFixture, snapshot } from './resume-task-pin.fixture.mjs';

// Manual runtime integration: run this .live.mjs at release; it starts several CLIs.
test('retained resume provides runtime without mutating its pin', async (t) => {
  const { task, originalProvider, retainedProvider, env, before } = await retainedFixture(t, 'accepted');
  const result = spawnSync(init, ['--resume-task-dir', task], { encoding: 'utf8', env });
  assert.equal(result.status, 0, result.stderr);
  assert.equal(result.stdout.trim(), path.join(task, 'CHECKLIST.md'));
  const after = await snapshot(task);
  assert.ok(after['mm-harness']);
  delete after['mm-harness'];
  assert.deepEqual(after, before, 'Only the missing runtime command may be added');
  const help = spawnSync(path.join(task, 'mm-harness'), ['help', '--json'], { encoding: 'utf8', env });
  assert.equal(help.status, 0, help.stderr);
  assert.equal(JSON.parse(help.stdout).version, '0.94.3');
  assert.equal(await realpath(path.join(originalProvider, 'node_modules/@deeeed/metamask-harness')), originalProvider);
  await assert.rejects(realpath(path.join(retainedProvider, 'node_modules/@deeeed/metamask-harness')), { code: 'ENOENT' });
});
