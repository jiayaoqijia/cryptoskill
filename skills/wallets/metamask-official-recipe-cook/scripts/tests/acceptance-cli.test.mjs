import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { copyFileSync, mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { createRequire } from 'node:module';
import test from 'node:test';
import { fileURLToPath } from 'node:url';

function fixture(t) {
  const root = mkdtempSync(path.join(os.tmpdir(), 'cook-acceptance-'));
  t.after(() => rmSync(root, { recursive: true, force: true }));
  const scripts = path.join(root, 'scripts');
  const task = path.join(root, 'task with spaces');
  const harness = path.join(root, 'locked harness', 'bin', 'mm-harness');
  const runtime = path.join(root, 'locked harness', 'node_modules', '@farmslot', 'agent-runtime');
  for (const dir of [scripts, task, path.dirname(harness), path.join(runtime, 'scripts')]) mkdirSync(dir, { recursive: true });
  copyFileSync(fileURLToPath(new URL('../acceptance-cli', import.meta.url)), path.join(scripts, 'acceptance-cli'));
  writeFileSync(harness, 'locked executable');
  writeFileSync(path.join(scripts, 'resolve-harness'), '#!/usr/bin/env bash\n[ "$1" = "$EXPECTED_TASK" ] && [ "$2" = "--verify-only" ] && [ -z "${3:-}" ] || exit 42\n[ -z "${REFUSE_LOCK:-}" ] || exit 17\nprintf "%s" "$LOCKED_HARNESS"\n', { mode: 0o755 });
  writeFileSync(path.join(runtime, 'package.json'), JSON.stringify({ name: '@farmslot/agent-runtime' }));
  writeFileSync(path.join(runtime, 'scripts', 'acceptance-cli.cjs'), 'if (process.argv[2] === "set") { console.error("Verdicts are engine-owned."); process.exit(1); } console.log(JSON.stringify(process.argv.slice(2))); process.exit(Number(process.env.CLI_EXIT || 0));\n');
  const run = (args, extra = {}) => spawnSync('bash', [path.join(scripts, 'acceptance-cli'), task, ...args], {
    encoding: 'utf8', env: { ...process.env, EXPECTED_TASK: task, LOCKED_HARNESS: harness, ...extra },
  });
  return { task, run };
}

test('resolves from the verified task lock and forwards read commands intact', (t) => {
  const { task, run } = fixture(t);
  for (const args of [['list'], ['render']]) {
    const result = run(args);
    assert.equal(result.status, 0, result.stderr);
    assert.deepEqual(JSON.parse(result.stdout), [...args, '--task-dir', task]);
  }
});

test('the wrapper preserves the verdict-write refusal', (t) => {
  const { run } = fixture(t);
  for (const verdict of ['proven', 'untestable']) {
    const result = run(['set', 'AC-1', verdict]);
    assert.equal(result.status, 1);
    assert.match(result.stderr, /Verdicts are engine-owned/);
    assert.equal(result.stdout, '');
  }
});

test('the published runtime exposes reads and refuses verdict writes', {
  skip: !process.env.MM_HARNESS_BIN && 'Set MM_HARNESS_BIN to the published harness executable.',
}, () => {
  const require = createRequire(path.resolve(process.env.MM_HARNESS_BIN));
  const cli = require.resolve('@farmslot/agent-runtime/scripts/acceptance-cli.cjs');
  const help = spawnSync(process.execPath, [cli, '--help'], { encoding: 'utf8' });
  assert.equal(help.status, 0, help.stderr);
  assert.match(help.stdout, /ac list/);
  assert.match(help.stdout, /ac render/);
  assert.doesNotMatch(help.stdout, /ac set/);
  for (const verdict of ['proven', 'untestable']) {
    const result = spawnSync(process.execPath, [cli, 'set', 'AC-1', verdict], { encoding: 'utf8' });
    assert.notEqual(result.status, 0);
    assert.match(result.stderr, /Verdicts are engine-owned/);
  }
});

test('a refused lock stops execution and the ledger exit code reaches the caller', (t) => {
  const { run } = fixture(t);
  const refused = run(['list'], { REFUSE_LOCK: '1' });
  assert.equal(refused.status, 17);
  assert.equal(refused.stdout, '');
  const failed = run(['list'], { CLI_EXIT: '9' });
  assert.equal(failed.status, 9);
  assert.deepEqual(JSON.parse(failed.stdout).slice(0, 1), ['list']);
});
