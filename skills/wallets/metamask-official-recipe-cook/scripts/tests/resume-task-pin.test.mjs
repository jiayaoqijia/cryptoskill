import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import test from 'node:test';
import path from 'node:path';
import { retainedFixture, snapshot } from './resume-task-pin.fixture.mjs';

test('two retained harness resolutions preserve the producer receipt and task files', async (t) => {
  const { task, provider, scripts, env, before } = await retainedFixture(t, 'accepted');
  for (let attempt = 0; attempt < 2; attempt += 1) {
    const result = spawnSync(path.join(scripts, 'resolve-harness'), [task], {
      encoding: 'utf8', env,
    });
    assert.equal(result.status, 0, result.stderr);
    assert.equal(result.stdout.trim(), path.join(provider, 'bin/mm-harness'));
    assert.deepEqual(await snapshot(task), before);
  }
});

for (const scenario of ['existing-runner', 'rejected-pin', 'wrong-provider', 'changed-library']) test(`retained task resume ${scenario}`, async (t) => {
  const { task, scripts, env, before } = await retainedFixture(t, scenario);
  const result = spawnSync(path.join(scripts, 'init-template'), ['--resume-task-dir', task], {
    encoding: 'utf8', env,
  });
  if (scenario === 'existing-runner') {
    assert.equal(result.status, 0, result.stderr);
    assert.deepEqual(await snapshot(task), before, 'Existing runtime command is preserved');
    return;
  }
  if (scenario !== 'accepted') {
    assert.notEqual(result.status, 0);
    assert.match(result.stderr, scenario === 'rejected-pin' ? /TASK_INPUT_CHANGED/ : scenario === 'changed-library' ? /Recorded library source changed/ : /Selected provider is not the MetaMask harness/);
    assert.deepEqual(await snapshot(task), before);
  }
});


for (const scenario of ['pool-update', 'pool-no-registry']) test(`recorded 0.94.1 resolves selected 0.94.6 with a warning: ${scenario}`, async (t) => {
  const { task, poolProvider, retainedProvider, scripts, env, before } = await retainedFixture(t, scenario);
  const pinBefore = await snapshot(retainedProvider);
  const result = spawnSync(path.join(scripts, 'resolve-harness'), [task, '--verify-only'], { encoding: 'utf8', env });
  assert.equal(result.status, 0, result.stderr);
  assert.equal(result.stdout.trim(), path.join(poolProvider, 'bin/mm-harness'));
  assert.match(result.stderr, /0\.94\.1; using configured 0\.94\.6/);
  const launch = spawnSync(result.stdout.trim(), ['help', '--json'], { encoding: 'utf8', env });
  assert.equal(launch.status, 0, launch.stderr);
  assert.equal(JSON.parse(launch.stdout).version, '0.94.6');
  assert.deepEqual(await snapshot(retainedProvider), pinBefore);
  assert.deepEqual(await snapshot(task), before);
});


test('a direct task uses a public fallback outside its pin with an older SDK', async (t) => {
  const { task, provider, retainedProvider, scripts, env, before } = await retainedFixture(t, 'direct-no-pool');
  const pinBefore = await snapshot(retainedProvider);
  const result = spawnSync(path.join(scripts, 'resolve-harness'), [task, '--verify-only'], { encoding: 'utf8', env });
  assert.equal(result.status, 0, result.stderr);
  assert.equal(result.stdout.trim(), path.join(provider, 'bin/mm-harness'));
  assert.match(result.stderr, /0\.94\.1; using configured 0\.94\.6/);
  const launch = spawnSync(result.stdout.trim(), ['help', '--json'], { encoding: 'utf8', env });
  assert.equal(launch.status, 0, launch.stderr);
  assert.deepEqual(await snapshot(retainedProvider), pinBefore);
  assert.deepEqual(await snapshot(task), before);
});

test('a configured launcher inside a retained pin refuses before bootstrap mutation', async (t) => {
  const { task, retainedProvider, scripts, env, before } = await retainedFixture(t, 'unsafe-pool');
  const pinBefore = await snapshot(retainedProvider);
  const result = spawnSync(path.join(scripts, 'resolve-harness'), [task, '--verify-only'], { encoding: 'utf8', env });
  assert.notEqual(result.status, 0);
  assert.match(result.stderr, /launcher is inside the frozen task pin/);
  assert.deepEqual(await snapshot(retainedProvider), pinBefore);
  assert.deepEqual(await snapshot(task), before);
});
