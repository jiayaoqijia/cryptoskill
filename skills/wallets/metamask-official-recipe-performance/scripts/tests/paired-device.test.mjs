import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';

const scripts = fileURLToPath(new URL('..', import.meta.url));
function fixture(t) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'mobile-perf-'));
  t.after(() => fs.rmSync(dir, { recursive: true }));
  return dir;
}
function python(script, args) {
  return spawnSync('python3', [path.join(scripts, script), ...args], { encoding: 'utf8' });
}

test('blocks alternate and a failed capture stops without overwriting its evidence', (t) => {
  const dir = fixture(t);
  const adapter = path.join(dir, 'capture');
  fs.writeFileSync(adapter, '#!/usr/bin/env python3\nimport sys\nfrom pathlib import Path\np=Path(sys.argv[3]); (p/"observed.txt").write_text(" ".join(sys.argv[1:]))\nsys.exit(7 if sys.argv[1]=="broken" else 0)\n', { mode: 0o755 });
  const out = path.join(dir, 'ok');
  const result = python('paired-blocks.py', [out, '5', '2', 'base:abc', 'head:def', adapter]);
  assert.equal(result.status, 0, result.stderr);
  const manifest = JSON.parse(fs.readFileSync(path.join(out, 'blocks.json')));
  assert.deepEqual(manifest.blocks.map(x => [x.block, x.state, x.requestedRef]),
    [['a1', 'base', 'abc'], ['b1', 'head', 'def'], ['a2', 'base', 'abc'], ['b2', 'head', 'def']]);
  assert.equal(python('paired-blocks.py', [out, '5', '2', 'base:abc', 'head:def', adapter]).status, 1);
  const failed = path.join(dir, 'failed');
  assert.equal(python('paired-blocks.py', [failed, '5', '2', 'base:abc', 'broken:def', adapter]).status, 7);
  const partial = JSON.parse(fs.readFileSync(path.join(failed, 'blocks.json')));
  assert.deepEqual(partial.blocks.map(x => x.status), ['pass', 'failed']);
  assert.ok(fs.existsSync(path.join(failed, 'b1/observed.txt')));
});

function captures(dir, baseGaps, headGaps) {
  const blocks = [];
  for (const [index, state, gap] of [[1, 'base', baseGaps[0]], [1, 'head', headGaps[0]],
    [2, 'base', baseGaps[1]], [2, 'head', headGaps[1]]]) {
    const block = `${state === 'base' ? 'a' : 'b'}${index}`;
    const data = path.join(dir, block, 'data'); fs.mkdirSync(data, { recursive: true });
    for (const [n, value] of gap.entries()) {
      const raw = { marks: [{ n: 'press', t: 1000 }, { n: 'open-complete', t: 2000 }],
        frames: [900, 1000 + value, 2050] };
      fs.writeFileSync(path.join(data, `timed-${n}.json`), JSON.stringify(JSON.stringify(raw)));
    }
    blocks.push({ block, state, status: 'pass' });
  }
  fs.writeFileSync(path.join(dir, 'blocks.json'), JSON.stringify({ rounds: 2, repeats: 2,
    states: [['base', 'abc'], ['head', 'def']], blocks }));
}

test('interpolated percentiles retain a pooled gain that is not separated by blocks', (t) => {
  const dir = fixture(t);
  captures(dir, [[100, 200], [110, 210]], [[50, 100], [120, 220]]);
  const output = path.join(dir, 'metrics.json');
  const result = python('report.py', [dir, 'base', 'head', '--json', output]);
  assert.equal(result.status, 0, result.stderr);
  const metric = JSON.parse(fs.readFileSync(output)).open.metrics['next JS frame ms'];
  assert.equal(metric.states.base.p50, 155);
  assert.equal(metric.states.base.p75, 202.5);
  assert.equal(metric.states.head.p50, 110);
  assert.equal(metric.blockSeparation, 'not-separated');
  const file = path.join(dir, 'a1/data/timed-0.json');
  const raw = JSON.parse(JSON.parse(fs.readFileSync(file)));
  raw.marks.pop(); fs.writeFileSync(file, JSON.stringify(raw));
  const invalid = python('report.py', [dir, 'base', 'head']);
  assert.notEqual(invalid.status, 0);
  assert.match(invalid.stderr, /missing or invalid press\/open-complete/);
});

test('whole overlapping frame gaps and a higher-FPS direction are preserved', (t) => {
  const dir = fixture(t);
  captures(dir, [[100, 100], [100, 100]], [[50, 50], [50, 50]]);
  const raw = { marks: [{ n: 'press', t: 1000 }, { n: 'open-complete', t: 2000 }],
    frames: [900, 1100, 1150, 2200] };
  for (const block of ['a1', 'b1', 'a2', 'b2']) {
    for (const n of [0, 1]) {
      const sample = block.startsWith('b') ? { ...raw, frames: [900, 1100, 1150, 1500, 2200] } : raw;
      fs.writeFileSync(path.join(dir, block, `data/timed-${n}.json`), JSON.stringify(sample));
    }
  }
  const output = path.join(dir, 'metrics.json');
  assert.equal(python('report.py', [dir, 'base', 'head', '--json', output]).status, 0);
  const metrics = JSON.parse(fs.readFileSync(output)).open.metrics;
  assert.equal(metrics.fps.states.base.p50, 2);
  assert.equal(metrics.fps.states.head.p50, 3);
  assert.equal(metrics.fps.blockSeparation, 'better-separated');
  assert.equal(metrics['>100 ms frames'].states.base.p50, 2);
  assert.equal(metrics['longest frame'].states.base.p50, 1050);
  assert.equal(metrics['blocked ms'].states.base.p50, 1150);
  assert.equal(metrics['next JS frame ms'].states.base.p50, 100);
});

test('completion waits for both slide and first content layout, excluding later relayouts', (t) => {
  const dir = fixture(t);
  captures(dir, [[100, 100], [100, 100]], [[50, 50], [50, 50]]);
  for (const block of ['a1', 'b1', 'a2', 'b2']) {
    for (const n of [0, 1]) {
      const file = path.join(dir, block, `data/timed-${n}.json`);
      const raw = JSON.parse(JSON.parse(fs.readFileSync(file)));
      raw.marks.push({ n: 'content-layout', t: 2100 }, { n: 'content-layout', t: 3500 });
      raw.frames.push(2250);
      fs.writeFileSync(file, JSON.stringify(raw));
    }
  }
  const output = path.join(dir, 'metrics.json');
  const result = python('report.py', [dir, 'base', 'head', '--end-mark', 'open-complete,content-layout', '--json', output]);
  assert.equal(result.status, 0, result.stderr);
  assert.equal(JSON.parse(fs.readFileSync(output)).open.metrics['window ms'].states.base.p50, 1100);
});

test('captures must bracket both boundaries so a collection cutoff cannot hide a long gap', (t) => {
  const dir = fixture(t);
  captures(dir, [[100, 100], [100, 100]], [[50, 50], [50, 50]]);
  const file = path.join(dir, 'a1/data/timed-0.json');
  const raw = JSON.parse(JSON.parse(fs.readFileSync(file)));
  for (const frames of [[1100, 1500, 2200], [900, 1100, 1500, 1900]]) {
    fs.writeFileSync(file, JSON.stringify({ ...raw, frames }));
    const result = python('report.py', [dir, 'base', 'head']);
    assert.notEqual(result.status, 0);
    assert.match(result.stderr, /frame probe did not cover the open/);
  }
});
