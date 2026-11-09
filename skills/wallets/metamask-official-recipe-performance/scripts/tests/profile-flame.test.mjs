import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';

const script = fileURLToPath(new URL('../profile-flame.py', import.meta.url));
test('CPU view weights the caller tree, escapes labels and rejects empty profiles', t => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'profile-flame-'));
  t.after(() => fs.rmSync(dir, { recursive: true }));
  const input = path.join(dir, 'sample.cpuprofile');
  const output = path.join(dir, 'flame.html');
  const profile = {
    nodes: [
      { id: 1, callFrame: { functionName: '(root)' }, children: [2, 3] },
      { id: 2, callFrame: { functionName: '<mount>', url: 'http://local/a.js?token=private', lineNumber: 9 } },
      { id: 3, callFrame: { functionName: 'layout' } },
    ],
    samples: [2, 2, 3], timeDeltas: [1000, 2000, 1000], startTime: 0, endTime: 4000,
  };
  fs.writeFileSync(input, JSON.stringify(profile));
  const run = () => spawnSync('python3', [script, input, output], { encoding: 'utf8' });
  assert.equal(run().status, 0);
  const html = fs.readFileSync(output, 'utf8');
  assert.match(html, /width="900.000"/);
  assert.match(html, /&lt;mount&gt; a.js:10: inclusive 3.000 ms; self 3.000 ms/);
  assert.doesNotMatch(html, /token|private|<mount>/);
  assert.notEqual(run().status, 0, 'must not overwrite evidence');
  fs.unlinkSync(output);
  fs.writeFileSync(input, JSON.stringify({ ...profile, samples: [], timeDeltas: [] }));
  const empty = run();
  assert.notEqual(empty.status, 0);
  assert.match(empty.stderr, /CPU samples and matching timeDeltas are required/);
  assert.equal(fs.existsSync(output), false);
});


test('deep sampled stacks render without changing the interpreter recursion limit', t => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'profile-flame-deep-'));
  t.after(() => fs.rmSync(dir, { recursive: true }));
  const count = 1500;
  const profile = {
    nodes: Array.from({ length: count }, (_, id) => ({
      id, callFrame: { functionName: `frame${id}` },
      children: id + 1 < count ? [id + 1] : [],
    })),
    samples: [count - 1], timeDeltas: [1000], startTime: 0, endTime: 1000,
  };
  const input = path.join(dir, 'deep.cpuprofile');
  const output = path.join(dir, 'deep.html');
  fs.writeFileSync(input, JSON.stringify(profile));
  const result = spawnSync('python3', [script, input, output], { encoding: 'utf8' });
  assert.equal(result.status, 0, result.stderr);
  const html = fs.readFileSync(output, 'utf8');
  assert.equal((html.match(/<rect /g) || []).length, count);
  assert.match(html, /viewBox="0 0 1200 33000"/);
  assert.match(html, /frame1499 :0: inclusive 1.000 ms; self 1.000 ms/);
});
