import assert from 'node:assert/strict';
import { execFileSync, spawnSync } from 'node:child_process';
import { mkdtempSync, readFileSync, writeFileSync, rmSync, renameSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';
import { resolveScope, scopeRequestFromFarmInput } from './resolve-scope.mjs';

function fixture(t) {
  const repo = mkdtempSync(path.join(os.tmpdir(), 'qa-scope-'));
  t.after(() => rmSync(repo, { recursive: true, force: true }));
  const environment = Object.fromEntries(Object.entries(process.env).filter(([key]) => !key.startsWith('GIT_')));
  const git = (...args) => execFileSync('git', ['-C', repo, ...args], { env: environment, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }).trim();
  git('init', '-q'); git('config', 'user.name', 'Fixture'); git('config', 'user.email', 'fixture@example.test');
  const commit = (file, content, date) => {
    writeFileSync(path.join(repo, file), content); git('add', '.');
    execFileSync('git', ['-C', repo, 'commit', '-qm', 'test: scope fixture'], { env: { ...environment, GIT_AUTHOR_DATE: date, GIT_COMMITTER_DATE: date } });
    return git('rev-parse', 'HEAD');
  };
  const base = commit('initial.txt', 'initial', '2026-09-10T12:00:00Z');
  const first = commit('first.txt', 'first', '2026-09-14T12:00:00Z');
  const head = commit('latest.txt', 'latest', '2026-09-15T06:00:00Z');
  return { repo, git, commit, base, first, head, environment };
}

test('daily scope includes an old topic change when its merge lands inside the window', (t) => {
  const f = fixture(t);
  const branch = f.git('branch', '--show-current');
  f.git('checkout', '-qb', 'topic', f.base);
  const topic = f.commit('topic.txt', 'landed later', '2026-09-11T12:00:00Z');
  f.git('checkout', '-q', branch);
  execFileSync('git', ['-C', f.repo, 'merge', '--no-ff', '-qm', 'test: land topic', 'topic'], {
    env: { ...f.environment, GIT_AUTHOR_DATE: '2026-09-15T07:00:00Z', GIT_COMMITTER_DATE: '2026-09-15T07:00:00Z' },
  });
  const result = resolveScope({ kind: 'window', hours: 24 }, { repo: f.repo, now: new Date('2026-09-15T08:00:00Z') });
  assert.deepEqual(result.commits, [f.first, f.head, f.git('rev-parse', 'HEAD')]);
  assert(!result.commits.includes(topic));
  assert(result.files.some((file) => file.path === 'topic.txt'));
});

test('CLI refuses to replace frozen scope after the requested ref advances', (t) => {
  const f = fixture(t);
  const input = path.join(f.repo, 'scope-input.json');
  const out = path.join(f.repo, 'scope-output.json');
  writeFileSync(input, JSON.stringify({ kind: 'range', base: f.base, head: 'HEAD' }));
  const args = [fileURLToPath(new URL('./resolve-scope.mjs', import.meta.url)), '--input', input, '--out', out, '--repo', f.repo];
  execFileSync(process.execPath, args, { env: f.environment });
  const frozen = readFileSync(out, 'utf8');
  f.commit('later.txt', 'later', '2026-09-15T09:00:00Z');
  const retry = spawnSync(process.execPath, args, { env: f.environment, encoding: 'utf8' });
  assert.notEqual(retry.status, 0);
  assert.match(retry.stderr, /Scope output already exists/);
  assert.equal(readFileSync(out, 'utf8'), frozen);
});

test('release ranges freeze both refs and include renamed/deleted paths without mutating checkout', (t) => {
  const f = fixture(t);
  renameSync(path.join(f.repo, 'first.txt'), path.join(f.repo, 'renamed.txt'));
  const head = f.commit('latest.txt', 'updated', '2026-09-15T07:00:00Z');
  const result = resolveScope({ kind: 'range', base: f.first, head }, { repo: f.repo });
  assert.equal(result.baseSha, f.first); assert.equal(result.headSha, head);
  assert.deepEqual(result.files.map((x) => [x.status, x.path]), [['D', 'first.txt'], ['A', 'latest.txt'], ['A', 'renamed.txt']]);
  assert.equal(f.git('status', '--porcelain'), '');
});

test('a window freezes its cutoff and retains only selected landed changes', (t) => {
  const f = fixture(t);
  const result = resolveScope({ kind: 'window', hours: 24 }, { repo: f.repo, now: new Date('2026-09-15T08:00:00Z') });
  assert.deepEqual(result.commits, [f.first, f.head]);
  assert.deepEqual(result.files.map((x) => x.path), ['first.txt', 'latest.txt']);
  const historical = resolveScope({ kind: 'window', hours: 24, until: '2026-09-14T18:00:00Z' }, { repo: f.repo });
  assert.equal(historical.headSha, f.first);
  assert.deepEqual(historical.commits, [f.first]);
});

test('an empty window is explicit and cannot masquerade as recipe coverage', (t) => {
  const f = fixture(t);
  const result = resolveScope({ kind: 'window', hours: 1, until: '2026-09-15T08:00:00Z' }, { repo: f.repo });
  assert.equal(result.empty, true); assert.deepEqual(result.files, []); assert.deepEqual(result.commits, []);
  assert.equal(result.headSha, f.head);
});

test('PR comparison uses its merge base and records fork trust without executing it', (t) => {
  const f = fixture(t);
  const facts = { number: 42, base: { sha: f.base, repo: { full_name: 'example/app' } }, head: { sha: f.head, repo: { full_name: 'contributor/app' } } };
  const result = resolveScope({ kind: 'pr', url: 'https://github.com/example/app/pull/42' }, { repo: f.repo, readPR: () => facts });
  assert.equal(result.comparisonBaseSha, f.base); assert.equal(result.source.trust, 'fork');
  assert.throws(() => resolveScope({ kind: 'pr', url: 'example/app#43' }, { repo: f.repo, readPR: () => facts }), /another source/);
  assert.throws(() => resolveScope({ kind: 'window', since: 'yesterday' }, { repo: f.repo }), /ISO timestamp/);
  assert.throws(() => resolveScope({ kind: 'window', hours: -1 }, { repo: f.repo }), /positive/);
});

test('explicit expected revisions reject moving PRs before producing runtime input', t => {
  const f = fixture(t);
  const facts = { number: 42, base: { sha: f.base, repo: { full_name: 'example/app' } }, head: { sha: f.head, repo: { full_name: 'example/app' } } };
  const input = { kind: 'pr', url: 'https://github.com/example/app/pull/42', expectedHeadSha: f.head, expectedBaseSha: f.base };
  const scope = resolveScope(input, { repo: f.repo, readPR: () => facts });
  assert.equal(scope.kind, 'pr');
  assert.equal(scope.source.number, 42);
  assert.throws(() => resolveScope({ ...input, expectedHeadSha: f.first }, { repo: f.repo, readPR: () => facts }), /do not prepare or execute/);
  assert.throws(() => resolveScope({ ...input, expectedBaseSha: f.first }, { repo: f.repo, readPR: () => facts }), /do not prepare or execute/);
});

test('remote feature flags freeze with the scope as the harness launch spec, on every kind', (t) => {
  const f = fixture(t);
  const remoteFeatureFlags = { perpsTAT3938AbtestScreenVsBottomSheet: 'treatment', perpsEnabled: true, perpsConfig: { tier: 2 } };
  const scope = resolveScope({ kind: 'ref', ref: f.head, remoteFeatureFlags }, { repo: f.repo });
  assert.deepEqual(scope.remoteFeatureFlags, remoteFeatureFlags);
  assert.equal(scope.remoteFlagSpec, 'perpsTAT3938AbtestScreenVsBottomSheet=treatment,perpsEnabled=true,perpsConfig={"tier":2}');
  const facts = { number: 42, base: { sha: f.base, repo: { full_name: 'example/app' } }, head: { sha: f.head, repo: { full_name: 'example/app' } } };
  const pr = resolveScope({ kind: 'pr', url: 'https://github.com/example/app/pull/42', remoteFeatureFlags }, { repo: f.repo, readPR: () => facts });
  assert.equal(pr.remoteFlagSpec, scope.remoteFlagSpec);
  assert.notEqual(pr.sha256, resolveScope({ kind: 'pr', url: 'https://github.com/example/app/pull/42' }, { repo: f.repo, readPR: () => facts }).sha256, 'the variant is part of the frozen scope');
  assert.equal('remoteFlagSpec' in resolveScope({ kind: 'ref', ref: f.head }, { repo: f.repo }), false);
  // A farm profile delivers the map as text; blank text means no override.
  assert.equal(resolveScope({ kind: 'ref', ref: f.head, remoteFeatureFlags: JSON.stringify(remoteFeatureFlags) }, { repo: f.repo }).remoteFlagSpec, scope.remoteFlagSpec);
  assert.equal('remoteFlagSpec' in resolveScope({ kind: 'ref', ref: f.head, remoteFeatureFlags: '  ' }, { repo: f.repo }), false);
  // A farm field the operator typed in and then emptied is stored as null: no override either.
  const cleared = resolveScope({ kind: 'ref', ref: f.head, remoteFeatureFlags: null }, { repo: f.repo });
  assert.equal('remoteFlagSpec' in cleared, false);
  assert.equal(cleared.sha256, resolveScope({ kind: 'ref', ref: f.head }, { repo: f.repo }).sha256);
  const farm = { profile: { inputs: { scope: { kind: 'ref' } } }, inputs: { scope: { ref: f.head, remoteFeatureFlags: null } } };
  assert.equal('remoteFlagSpec' in resolveScope(scopeRequestFromFarmInput(farm), { repo: f.repo }), false);
  assert.throws(() => resolveScope({ kind: 'ref', ref: f.head, remoteFeatureFlags: '{nope' }, { repo: f.repo }), /JSON object/);
  for (const bad of [{}, [], 'treatment', { 'bad key': true }, { flag: null }, { flag: 'has,comma' }, { flag: 3 }]) {
    assert.throws(() => resolveScope({ kind: 'ref', ref: f.head, remoteFeatureFlags: bad }, { repo: f.repo }), /remoteFeatureFlags/);
  }
});

test('the proof lane and mainnet opt-in freeze with the scope; an official lane refuses remote-flag pins', (t) => {
  const f = fixture(t);
  const plain = resolveScope({ kind: 'ref', ref: f.head }, { repo: f.repo });
  assert.equal('proofLane' in plain || 'mainnetOptIn' in plain, false, 'absent means source-dev on testnet');
  const official = resolveScope({ kind: 'ref', ref: f.head, proofLane: 'official-unmodified', mainnetOptIn: true }, { repo: f.repo });
  assert.equal(official.proofLane, 'official-unmodified');
  assert.equal(official.mainnetOptIn, true);
  assert.notEqual(official.sha256, plain.sha256);
  assert.equal('mainnetOptIn' in resolveScope({ kind: 'ref', ref: f.head, mainnetOptIn: false }, { repo: f.repo }), false);
  assert.throws(() => resolveScope({ kind: 'ref', ref: f.head, proofLane: 'runway' }, { repo: f.repo }), /proofLane must be one of/);
  assert.throws(() => resolveScope({ kind: 'ref', ref: f.head, mainnetOptIn: 'yes' }, { repo: f.repo }), /mainnetOptIn/);
  assert.throws(() => resolveScope({ kind: 'ref', ref: f.head, proofLane: 'official-unmodified', remoteFeatureFlags: { perpsEnabled: true } }, { repo: f.repo }), /need a source build/);
  assert.equal(resolveScope({ kind: 'ref', ref: f.head, proofLane: 'source-dev', remoteFeatureFlags: { perpsEnabled: true } }, { repo: f.repo }).proofLane, 'source-dev');
  // The farm release profile's proof_lane input joins the request; mainnetOptIn arrives inside the scope.
  const farm = { profile: { inputs: { scope: { kind: 'range' } } }, inputs: { scope: { base: 'v1.0.0', head: 'release/1.1.0', mainnetOptIn: true }, proof_lane: 'official-unmodified' } };
  assert.deepEqual(scopeRequestFromFarmInput(farm), { kind: 'range', base: 'v1.0.0', head: 'release/1.1.0', mainnetOptIn: true, proofLane: 'official-unmodified' });
});

test('a farm PR source binds only a PR scope: a release range keeps its annotated base tag', (t) => {
  const f = fixture(t);
  f.git('tag', '-a', 'v1.0.0', '-m', 'release 1.0.0', f.first);
  const tagObject = f.git('rev-parse', 'v1.0.0');
  assert.notEqual(tagObject, f.first, 'the base tag is annotated');
  // The release PR targets a stable branch whose tip merged the previous release.
  const stableTip = f.git('commit-tree', '-p', f.base, '-p', f.first, '-m', 'test: merge release 1.0.0', `${f.first}^{tree}`);
  const farm = {
    sourceRef: 'example/app#42',
    source: { baseSha: stableTip, headSha: f.head },
    profile: { inputs: { scope: { kind: 'range' } } },
    inputs: { scope: { base: 'v1.0.0', head: f.head } },
  };

  const request = scopeRequestFromFarmInput(farm);
  assert.deepEqual(request, { kind: 'range', base: 'v1.0.0', head: f.head });
  const range = resolveScope(request, { repo: f.repo });
  assert.equal(range.baseSha, f.first, 'the tag resolves to its commit, not its tag object');
  assert.deepEqual(range.commits, [f.head]);
  // Binding the PR base to the range is what refused release QA.
  assert.throws(() => resolveScope({ ...request, expectedBaseSha: stableTip }, { repo: f.repo }), /Resolved baseline differs/);

  const facts = { number: 42, base: { sha: stableTip, repo: { full_name: 'example/app' } }, head: { sha: f.head, repo: { full_name: 'example/app' } } };
  const prFarm = { ...farm, profile: { inputs: { scope: { kind: 'pr' } } }, inputs: { scope: {} } };
  const prRequest = scopeRequestFromFarmInput(prFarm);
  assert.deepEqual(prRequest, { kind: 'pr', url: 'example/app#42', expectedBaseSha: stableTip, expectedHeadSha: f.head });
  assert.equal(resolveScope(prRequest, { repo: f.repo, readPR: () => facts }).baseSha, stableTip);
  const moved = { ...facts, base: { ...facts.base, sha: f.base } };
  assert.throws(() => resolveScope(prRequest, { repo: f.repo, readPR: () => moved }), /Resolved baseline differs/);
});

test('a farm scope request keeps preset fields only for the same kind and lets explicit SHAs win', () => {
  const daily = { sourceRef: 'example/app#42', source: { baseSha: 'b'.repeat(40), headSha: 'h'.repeat(40) }, profile: { inputs: { scope: { kind: 'window', hours: 24 } } } };
  // The farm's shallow merge drops `kind`; the preset restores it for the same scope.
  assert.deepEqual(scopeRequestFromFarmInput({ ...daily, inputs: { scope: { ref: 'main', hours: 48 } } }), { kind: 'window', hours: 48, ref: 'main' });
  // A Daily preset launched as a ref keeps none of the window's fields.
  assert.deepEqual(scopeRequestFromFarmInput({ ...daily, inputs: { scope: { kind: 'ref', ref: 'abc123' } } }), { kind: 'ref', ref: 'abc123' });
  // An explicit expected SHA in a PR scope wins over the farm source.
  const pr = { ...daily, profile: { inputs: { scope: { kind: 'pr' } } }, inputs: { scope: { expectedHeadSha: 'e'.repeat(40) } } };
  assert.deepEqual(scopeRequestFromFarmInput(pr), { kind: 'pr', url: 'example/app#42', expectedHeadSha: 'e'.repeat(40), expectedBaseSha: 'b'.repeat(40) });
});

test('CLI freezes the farm scope request once and refuses a different one on resume', (t) => {
  const f = fixture(t);
  const farmInput = path.join(f.repo, 'qa.json');
  const out = path.join(f.repo, 'inputs', 'qa-scope-request.json');
  const farm = { sourceRef: 'example/app#42', source: { baseSha: f.base, headSha: f.head }, profile: { inputs: { scope: { kind: 'range' } } }, inputs: { scope: { base: f.first, head: f.head } } };
  writeFileSync(farmInput, JSON.stringify(farm));
  const args = [fileURLToPath(new URL('./resolve-scope.mjs', import.meta.url)), '--farm-input', farmInput, '--out', out];
  execFileSync(process.execPath, args, { env: f.environment });
  assert.deepEqual(JSON.parse(readFileSync(out, 'utf8')), { kind: 'range', base: f.first, head: f.head });
  execFileSync(process.execPath, args, { env: f.environment });
  writeFileSync(farmInput, JSON.stringify({ ...farm, inputs: { scope: { base: f.base, head: f.head } } }));
  const changed = spawnSync(process.execPath, args, { env: f.environment, encoding: 'utf8' });
  assert.notEqual(changed.status, 0);
  assert.match(changed.stderr, /new task, not a resume/);
});
