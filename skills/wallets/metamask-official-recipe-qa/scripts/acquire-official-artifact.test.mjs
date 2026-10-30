import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { copyFileSync, existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { acquireOfficialArtifact } from './acquire-official-artifact.mjs';

const HEAD = 'a'.repeat(40);
const digestOf = (file) => `sha256:${createHash('sha256').update(readFileSync(file)).digest('hex')}`;

/** A fake GitHub holding one CI run whose artifact zip holds `member`. */
function fixture(t, { repository, workflow, artifact, member }) {
  const root = mkdtempSync(path.join(os.tmpdir(), 'qa-official-'));
  t.after(() => rmSync(root, { recursive: true, force: true }));
  const staging = path.join(root, 'staging');
  mkdirSync(path.dirname(path.join(staging, member)), { recursive: true });
  writeFileSync(path.join(staging, member), `build ${member}`);
  const zip = path.join(root, 'artifact.zip');
  execFileSync('zip', ['-q', '-r', zip, '.'], { cwd: staging });
  const run = { id: 7, event: 'push', html_url: 'https://github.com/run/7', conclusion: 'success', head_sha: HEAD, head_branch: 'release/8.16.0', head_repository: { full_name: repository }, path: `.github/workflows/${workflow}` };
  const routes = [];
  const github = {
    api(route) {
      routes.push(route);
      if (route.includes('/workflows/')) return { workflow_runs: [...github.newer, run] };
      if (route.endsWith('/runs/7')) return run;
      return { artifacts: [{ id: 99, name: artifact, expired: false, digest: github.digest }] };
    },
    download(route, file) { routes.push(route); copyFileSync(zip, file); },
    digest: digestOf(zip),
    newer: [],
  };
  return { root, out: path.join(root, 'out'), run, github, routes, member };
}

const scope = { proofLane: 'official-unmodified', headSha: HEAD, source: { base: 'v8.15.0', head: 'origin/release/8.16.0' } };
const mobile = { repository: 'MetaMask/metamask-mobile', workflow: 'build-rc-auto.yml', artifact: 'android-apk-main-rc', member: 'metamask-rc-main-8.16.0-7206.apk' };

test('the Android RC of the frozen head becomes verified runtime-launch arguments', (t) => {
  const f = fixture(t, mobile);
  const record = acquireOfficialArtifact({ scope, platform: 'android', out: f.out, github: f.github });
  assert.match(f.routes[0], /workflows\/build-rc-auto\.yml\/runs\?branch=release%2F8\.16\.0&head_sha=a{40}&status=completed/);
  assert.equal(path.relative(f.out, record.file).split(path.sep).slice(1).join('/'), f.member);
  assert.equal(record.sha256, createHash('sha256').update(`build ${f.member}`).digest('hex'));
  assert.deepEqual([record.version, record.buildId, record.packageId, record.run.id, record.artifact.id], ['8.16.0', '7206', 'io.metamask', 7, 99]);
  assert.deepEqual(record.launch, ['--adapter', 'mobile', '--platform', 'android', '--artifact-file', record.file, '--artifact-version', '8.16.0', '--artifact-build-id', '7206', '--artifact-package-id', 'io.metamask', '--artifact-sha256', record.sha256]);
});

test('the Extension RC is the Chrome zip inside the release Main run artifact, whatever the tests concluded', (t) => {
  const f = fixture(t, { repository: 'MetaMask/metamask-extension', workflow: 'main.yml', artifact: 'build-dist-webpack', member: 'builds/metamask-chrome-8.16.0.zip' });
  f.run.conclusion = 'failure';
  const record = acquireOfficialArtifact({ scope, platform: 'extension', out: f.out, github: f.github });
  assert.equal(record.run.conclusion, 'failure');
  assert.deepEqual(record.launch, ['--adapter', 'extension', '--artifact-file', record.file, '--artifact-version', '8.16.0', '--artifact-sha256', record.sha256]);
  assert.equal('buildId' in record, false);
});

test('acquisition fails closed: source lane, wrong head, missing or tampered artifact, other version', (t) => {
  const f = fixture(t, mobile);
  const acquire = (overrides = {}) => acquireOfficialArtifact({ scope, platform: 'android', out: f.out, github: f.github, ...overrides });
  assert.throws(() => acquire({ scope: { ...scope, proofLane: 'source-dev' } }), /not an official proof lane/);
  assert.throws(() => acquire({ platform: 'ios' }), /downloaded iOS is unsupported/);
  assert.throws(() => acquire({ scope: { ...scope, source: { ref: HEAD } } }), /Pass --version/);
  f.run.head_sha = 'b'.repeat(40);
  assert.throws(() => acquire({ runId: '7' }), /not build-rc-auto\.yml on release\/8\.16\.0 at the frozen head/);
  f.run.head_sha = HEAD;
  f.run.event = 'pull_request';
  assert.throws(() => acquire({ runId: '7' }), /is a pull_request run, not a push or workflow_dispatch build/);
  f.run.event = 'push';
  const api = f.github.api;
  f.github.api = (route) => route.includes('/artifacts?') ? { artifacts: [{ id: 99, expired: true }] } : api(route);
  assert.throws(() => acquire(), /official build of this head is unavailable/);
  f.github.api = api;
  const digest = f.github.digest;
  f.github.digest = `sha256:${'0'.repeat(64)}`;
  assert.throws(() => acquire(), /does not match its GitHub digest/);
  f.github.digest = digest;
  f.run.head_branch = 'release/8.17.0';
  assert.throws(() => acquire({ version: '8.17.0' }), /metamask-rc-main-8\.16\.0-7206\.apk is not version 8\.17\.0/);
});

test('a dispatched Mobile RC counts; a newer release PR run is skipped, not fatal', (t) => {
  const m = fixture(t, mobile);
  m.run.event = 'workflow_dispatch';
  assert.equal(acquireOfficialArtifact({ scope, platform: 'android', out: m.out, github: m.github, runId: '7' }).run.id, 7);
  const e = fixture(t, { repository: 'MetaMask/metamask-extension', workflow: 'main.yml', artifact: 'build-dist-webpack', member: 'builds/metamask-chrome-8.16.0.zip' });
  e.github.newer.push({ ...e.run, id: 8, event: 'pull_request' });
  assert.equal(acquireOfficialArtifact({ scope, platform: 'extension', out: e.out, github: e.github }).run.id, 7);
  e.run.event = 'workflow_dispatch';
  assert.throws(() => acquireOfficialArtifact({ scope, platform: 'extension', out: e.out, github: e.github }), /official build of this head is unavailable/);
});

test('a digest mismatch deletes the archive so the next attempt downloads again', (t) => {
  const f = fixture(t, mobile);
  const download = f.github.download;
  let downloads = 0;
  f.github.download = (route, file) => {
    downloads += 1;
    if (downloads === 1) writeFileSync(file, 'bad transfer');
    else download(route, file);
  };
  const acquire = () => acquireOfficialArtifact({ scope, platform: 'android', out: f.out, github: f.github });
  const archive = path.join(f.out, `${mobile.artifact}-99.zip`);
  assert.throws(acquire, /does not match its GitHub digest/);
  assert.equal(existsSync(archive), false);
  const record = acquire();
  assert.equal(downloads, 2);
  assert.equal(digestOf(archive), f.github.digest);
  assert.equal(record.artifact.id, 99);
});
