import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { mkdtemp, mkdir, readFile, realpath, rm, writeFile, copyFile, cp } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { pathToFileURL } from 'node:url';
import { reselectQa } from './reselect-qa.mjs';

const json = (value) => JSON.stringify(value, null, 2) + '\n';
async function setup() {
  const root = await realpath(await mkdtemp(path.join(os.tmpdir(), 'qa-reselection-')));
  const task = path.join(root, 'task');
  const artifacts = path.join(task, 'artifacts');
  const scripts = path.join(root, 'skills/recipe-qa/scripts');
  const cook = path.join(root, 'skills/recipe-cook/scripts');
  await Promise.all([scripts, cook, artifacts, path.join(task, 'inputs')].map((dir) => mkdir(dir, { recursive: true })));
  for (const name of ['finalize-qa.mjs', 'reselect-qa.mjs']) await copyFile(new URL(name, import.meta.url), path.join(scripts, name));
  await copyFile(new URL('../../recipe-cook/scripts/verify-harness.mjs', import.meta.url), path.join(cook, 'verify-harness.mjs'));
  // Only external harness IO is doubled. The real CLI, scope guards and selection writer run.
  await writeFile(path.join(cook, 'resolve-harness'), '#!/bin/sh\nexit 0\n', { mode: 0o755 });
  const provider = path.join(root, 'provider');
  await mkdir(provider);
  await writeFile(path.join(provider, 'package.json'), '{}');
  const modules = {
    '@farmslot/protocol': `import { createHash } from 'node:crypto';
      export const RECIPE_SUITE_SCOPE_SCHEMA_URL = 'https://example.test/suite';
      export const digestRecipeDocument = value => 'sha256:' + createHash('sha256').update(JSON.stringify(value)).digest('hex');`,
    '@farmslot/recipe-runner': `import { readFile, writeFile } from 'node:fs/promises'; import path from 'node:path';
      export const freezeRecipeSuiteScope = scope => ({ scope });
      export async function finalizeRecipeSuite({ scope, resolutions, outputDir }) {
        const rows = [];
        for (const row of resolutions) {
          const summary_path = row.id + '.summary.json';
          await writeFile(path.join(outputDir, summary_path), await readFile(row.result.summaryPath));
          rows.push({ id: row.id, kind: 'verdict', status: row.result.status, summary_path });
        }
        await writeFile(path.join(outputDir, 'suite-result.json'), JSON.stringify({ resolutions: rows }));
      }`,
    '@farmslot/recipe-cli': `import assert from 'node:assert/strict';
      export function validateRuntimeProof({ summary }) { assert.equal(summary.status, 'pass', 'Package failed'); }`,
  };
  for (const [name, source] of Object.entries(modules)) {
    const dir = path.join(provider, 'node_modules', name);
    await mkdir(dir, { recursive: true });
    const exports = name === '@farmslot/recipe-cli' ? { './harness': './index.mjs' } : './index.mjs';
    await writeFile(path.join(dir, 'package.json'), json({ name, type: 'module', exports }));
    await writeFile(path.join(dir, 'index.mjs'), source);
  }
  const input = { runId: 'recorded-run', profile: { id: 'qa' }, inputs: { target: 'pinned' } };
  const source = { baseSha: 'a'.repeat(40), headSha: 'b'.repeat(40), cases: ['visible', 'conformance'] };
  await writeFile(path.join(task, 'inputs/qa.json'), json(input));
  await writeFile(path.join(artifacts, 'qa-scope.json'), json(source));
  await writeFile(path.join(artifacts, 'harness-provenance.json'), json({ source: { packageRoot: provider } }));
  for (const [name, status] of [['earlier', 'pass'], ['corrected', 'pass'], ['later', 'pass'], ['conformance', 'pass'], ['failed', 'fail']]) {
    const dir = path.join(artifacts, name);
    await mkdir(dir);
    for (const [file, value] of Object.entries({
      'recipe.json': { name }, 'summary.json': { status, recipeRunId: name }, 'trace.json': [],
      'artifact-manifest.json': { artifacts: [] }, 'recipe-resolution.json': { dependencies: [] },
    })) await writeFile(path.join(dir, file), json(value));
  }
  const initial = { packages: { visible: 'earlier', conformance: 'conformance' }, smoke: { caseId: 'visible', proofTarget: 'rows' } };
  const corrected = { ...initial, packages: { ...initial.packages, visible: 'corrected' } };
  const { finalizeQa } = await import(pathToFileURL(path.join(scripts, 'finalize-qa.mjs')).href);
  const invokeCli = async (index, ...flags) => {
    const indexPath = path.join(root, 'requested-index.json');
    await writeFile(indexPath, json(index));
    return spawnSync(process.execPath, [path.join(scripts, 'finalize-qa.mjs'), '--task', task, '--index', indexPath, ...flags], { encoding: 'utf8' });
  };
  await finalizeQa(task, initial);
  const select = (index) => reselectQa(task, index, finalizeQa);
  const selected = () => readFile(path.join(artifacts, 'qa-result.json'), 'utf8');
  return { root, scripts, task, artifacts, input, source, initial, corrected, invokeCli, selected, select, finalizeQa };
}

const baseline = await setup();
test.after(() => rm(baseline.root, { recursive: true, force: true }));
async function fixture(t) {
  const root = await realpath(await mkdtemp(path.join(os.tmpdir(), 'qa-selection-case-')));
  t.after(() => rm(root, { recursive: true, force: true }));
  const task = path.join(root, 'task');
  await cp(baseline.task, task, { recursive: true });
  const artifacts = path.join(task, 'artifacts');
  const selected = () => readFile(path.join(artifacts, 'qa-result.json'), 'utf8');
  const select = (index) => reselectQa(task, index, baseline.finalizeQa);
  const invokeCli = async (index, ...flags) => {
    const indexPath = path.join(root, 'requested-index.json');
    await writeFile(indexPath, json(index));
    return spawnSync(process.execPath, [path.join(baseline.scripts, 'finalize-qa.mjs'), '--task', task, '--index', indexPath, ...flags], { encoding: 'utf8' });
  };
  return { ...baseline, root, task, artifacts, selected, select, invokeCli };
}

test('reselection advances the same farm binding and retains every earlier registration and attempt', async (t) => {
  const f = await fixture(t);
  const oldResult = await f.selected();
  const oldProof = await readFile(path.join(f.artifacts, 'qa-proof.json'), 'utf8');
  const oldSuite = await readFile(path.join(f.artifacts, 'qa-suite/suite-result.json'), 'utf8');
  const oldPackage = await readFile(path.join(f.artifacts, 'earlier/summary.json'), 'utf8');
  const selected = await f.invokeCli(f.corrected, '--reselect');
  assert.equal(selected.status, 0, selected.stderr);
  const current = JSON.parse(await f.selected());
  assert.deepEqual(current.packages, f.corrected.packages);
  assert.equal(current.runId, f.input.runId);
  assert.deepEqual(current.qa, { profile: f.input.profile, inputs: f.input.inputs });
  assert.deepEqual(current.source, JSON.parse(oldResult).source);
  assert.deepEqual(current.scope, JSON.parse(oldResult).scope);
  assert.equal(await readFile(path.join(f.artifacts, 'qa-proof.json'), 'utf8'), oldProof);
  assert.equal(await readFile(path.join(f.artifacts, 'qa-suite/suite-result.json'), 'utf8'), oldSuite);
  assert.equal(await readFile(path.join(f.artifacts, 'earlier/summary.json'), 'utf8'), oldPackage);
  const revisionDir = path.dirname(selected.stdout.trim());
  const receipt = JSON.parse(await readFile(path.join(revisionDir, 'reselection.json'), 'utf8'));
  assert.equal(await readFile(path.join(f.artifacts, receipt.previous.path), 'utf8'), oldResult);
  assert.equal(await readFile(path.join(f.artifacts, receipt.selected.path), 'utf8'), await f.selected());
  const summary = JSON.parse(await readFile(path.join(f.artifacts, current.suitePath, 'visible.summary.json'), 'utf8'));
  assert.equal(summary.recipeRunId, 'corrected');
});

test('a later reselection keeps the previous successor and its lineage', async (t) => {
  const f = await fixture(t);
  const revisionDir = path.dirname(await f.select(f.corrected));
  const secondResult = await f.selected();
  const later = await f.select({ ...f.corrected, packages: { ...f.corrected.packages, visible: 'later' } });
  const laterReceipt = JSON.parse(await readFile(path.join(path.dirname(later), 'reselection.json'), 'utf8'));
  assert.equal(await readFile(path.join(f.artifacts, laterReceipt.previous.path), 'utf8'), secondResult);
  assert.equal(await readFile(path.join(revisionDir, 'qa-result.json'), 'utf8'), secondResult);
});

test('normal finalization remains write-once and check-only cannot advance a frozen binding', async (t) => {
  const f = await fixture(t);
  const before = await f.selected();
  await assert.rejects(f.finalizeQa(f.task, f.corrected), /QA result already exists/);
  assert.equal((await f.finalizeQa(f.task, f.corrected, undefined, true)).status, 'pass');
  assert.notEqual((await f.invokeCli(f.corrected, '--reselect', '--check-only')).status, 0);
  assert.notEqual((await f.invokeCli(f.corrected, '--reselect', '--suite', 'qa-suite')).status, 0);
  assert.equal(await f.selected(), before);
});

test('retained tasks use the installed pin verifier before loading their locked runtime', async (t) => {
  const f = await fixture(t);
  for (const name of ['qa-proof.json', 'qa-result.json', 'qa-suite']) {
    await rm(path.join(f.artifacts, name), { recursive: true, force: true });
  }
  const receipt = path.join(f.artifacts, 'harness-provenance.json');
  const lock = JSON.parse(await readFile(receipt, 'utf8'));
  await writeFile(receipt, json({ ...lock, source: { ...lock.source, kind: 'task-retained' } }));
  // Cook deliberately refuses this format. Only the installed SDK can verify its authority.
  const cook = path.join(f.root, 'skills/recipe-cook/scripts');
  await mkdir(cook, { recursive: true });
  await writeFile(path.join(cook, 'resolve-harness'), '#!/bin/sh\nexit 1\n', { mode: 0o755 });
  await copyFile(new URL('../../recipe-cook/scripts/verify-harness.mjs', import.meta.url), path.join(cook, 'verify-harness.mjs'));
  const scripts = path.join(f.root, 'skills/recipe-qa/scripts');
  await cp(baseline.scripts, scripts, { recursive: true });
  const trusted = path.join(f.root, 'installed');
  const sdk = path.join(trusted, 'node_modules/@farmslot/recipe-cli');
  await mkdir(sdk, { recursive: true });
  await writeFile(path.join(sdk, 'package.json'), json({ name: '@farmslot/recipe-cli', type: 'module', exports: { './harness': './index.mjs' } }));
  await writeFile(path.join(sdk, 'index.mjs'), `import { readFileSync, writeFileSync } from 'node:fs';
    import path from 'node:path';
    export function verifySelectedTask(task) {
      if (process.env.REJECT_TEST_PIN) throw new Error('TASK_INPUT_CHANGED');
      writeFileSync(path.join(task, 'verified'), 'yes');
      return JSON.parse(readFileSync(path.join(task, 'artifacts/harness-provenance.json')));
    }`);
  const index = path.join(f.root, 'index.json');
  await writeFile(index, json(f.initial));
  const invoke = (extra = {}) => spawnSync(process.execPath, [
    path.join(scripts, 'finalize-qa.mjs'), '--task', f.task, '--index', index,
  ], { encoding: 'utf8', env: { ...process.env, MM_HARNESS_PACKAGE_ROOT: trusted, ...extra } });
  const before = await readFile(receipt, 'utf8');
  const rejected = invoke({ REJECT_TEST_PIN: '1' });
  assert.notEqual(rejected.status, 0);
  assert.match(rejected.stderr, /TASK_INPUT_CHANGED/);
  await assert.rejects(readFile(path.join(f.artifacts, 'qa-proof.json')), { code: 'ENOENT' });
  await assert.rejects(readFile(path.join(f.artifacts, 'qa-result.json')), { code: 'ENOENT' });
  const accepted = invoke();
  assert.equal(accepted.status, 0, accepted.stderr);
  assert.equal(await readFile(path.join(f.task, 'verified'), 'utf8'), 'yes');
  assert.equal(JSON.parse(await readFile(path.join(f.artifacts, 'qa-result.json'))).runId, f.input.runId);
  assert.deepEqual(JSON.parse(await readFile(path.join(f.artifacts, 'qa-proof.json'))).packages, f.initial.packages);
  assert.equal(await readFile(receipt, 'utf8'), before);
});

for (const [name, change] of [
  ['failed package', (index) => ({ ...index, packages: { ...index.packages, visible: 'failed' } })],
  ['missing case', (index) => ({ ...index, packages: { visible: 'corrected' } })],
  ['changed smoke', (index) => ({ ...index, smoke: { caseId: 'conformance', proofTarget: 'different' } })],
  ['escaped package', (index) => ({ ...index, packages: { ...index.packages, visible: '../escape' } })],
]) test(`${name} cannot replace the frozen QA selection`, async (t) => {
  const f = await fixture(t);
  const before = await f.selected();
  await assert.rejects(f.select(change(f.corrected)));
  assert.equal(await f.selected(), before);
});

test('changed source or QA input cannot replace the frozen selection', async (t) => {
  const f = await fixture(t);
  const before = await f.selected();
  await writeFile(path.join(f.artifacts, 'qa-scope.json'), json({ ...f.source, headSha: 'c'.repeat(40) }));
  await assert.rejects(f.select(f.corrected), /QA source changed/);
  await writeFile(path.join(f.artifacts, 'qa-scope.json'), json(f.source));
  await writeFile(path.join(f.task, 'inputs/qa.json'), json({ ...f.input, runId: 'another-run' }));
  await assert.rejects(f.select(f.corrected), /QA run identity changed/);
  assert.equal(await f.selected(), before);
});

test('concurrent reselection refuses and a changed binding is never overwritten', async (t) => {
  const f = await fixture(t);
  const before = await f.selected();
  let enter;
  const entered = new Promise((resolve) => { enter = resolve; });
  let release;
  const released = new Promise((resolve) => { release = resolve; });
  const first = reselectQa(f.task, f.corrected, async (_, index, suitePath) => {
    enter();
    await released;
    return { ...JSON.parse(before), suitePath, packages: index.packages };
  });
  await entered;
  await assert.rejects(reselectQa(f.task, f.corrected, () => assert.fail('second writer ran')), { code: 'EEXIST' });
  const changed = json({ ...JSON.parse(before), packages: { visible: 'another-owner' } });
  await writeFile(path.join(f.artifacts, 'qa-result.json'), changed);
  release();
  await assert.rejects(first, /QA selection changed during reselection/);
  assert.equal(await f.selected(), changed);
});
