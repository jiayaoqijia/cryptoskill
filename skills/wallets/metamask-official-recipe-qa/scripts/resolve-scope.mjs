#!/usr/bin/env node
import { writeNewFile } from './write-new-file.mjs';
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { existsSync, mkdirSync, readFileSync } from 'node:fs';
import path from 'node:path';
import { parseArgs } from 'node:util';
import { pathToFileURL } from 'node:url';

const gitEnvironment = () => Object.fromEntries(Object.entries(process.env).filter(([key]) =>
  !['GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE', 'GIT_COMMON_DIR', 'GIT_OBJECT_DIRECTORY', 'GIT_ALTERNATE_OBJECT_DIRECTORIES', 'GIT_PREFIX'].includes(key),
));

function object(value, label) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) throw new Error(`${label} must be an object`);
  return value;
}
function text(value, label) {
  if (typeof value !== 'string' || !value.trim()) throw new Error(`${label} is required`);
  return value.trim();
}
/**
 * Remote-config overrides the run must pin (A/B variants, kill switches). Frozen
 * with the scope and rendered as the harness's `launch --remote-flag` spec, so
 * the same grammar reaches mobile and extension: a bare word is a named variant,
 * true/false a boolean, and an object or array is used as authored JSON.
 */
function remoteFeatureFlags(raw) {
  // An emptied farm field arrives as null: no override, like an omitted one.
  if (raw === undefined || raw === null) return undefined;
  // A farm profile field arrives as text; the JSON it holds is the map.
  let value = raw;
  if (typeof raw === 'string') {
    if (!raw.trim()) return undefined;
    try { value = JSON.parse(raw); } catch { throw new Error('remoteFeatureFlags must be a JSON object, e.g. {"flag":"treatment"}'); }
  }
  const flags = object(value, 'remoteFeatureFlags');
  const keys = Object.keys(flags);
  if (keys.length === 0) throw new Error('remoteFeatureFlags must name at least one flag or be omitted');
  for (const key of keys) {
    if (!/^[A-Za-z_][A-Za-z0-9_.-]*$/.test(key)) throw new Error(`remoteFeatureFlags key is not a flag name: ${key}`);
    const flag = flags[key];
    if (typeof flag === 'string' && !/^[A-Za-z0-9_.-]+$/.test(flag)) throw new Error(`remoteFeatureFlags.${key} must be a variant name, a boolean or JSON, got ${JSON.stringify(flag)}`);
    if (flag === null || !['string', 'boolean', 'object'].includes(typeof flag)) throw new Error(`remoteFeatureFlags.${key} must be a variant name, a boolean or JSON`);
  }
  return flags;
}
function remoteFlagSpec(flags) {
  return Object.entries(flags).map(([key, flag]) => `${key}=${typeof flag === 'object' ? JSON.stringify(flag) : String(flag)}`).join(',');
}
// Official artifacts cannot apply checkout remote-flag pins.
const PROOF_LANES = ['source-dev', 'official-unmodified', 'official-qa-derived'];
function proofLane(value, flags) {
  if (value === undefined) return undefined;
  if (!PROOF_LANES.includes(value)) throw new Error(`proofLane must be one of ${PROOF_LANES.join(', ')}`);
  if (flags && value !== 'source-dev') throw new Error('remoteFeatureFlags need a source build: an official artifact cannot pin them');
  return value;
}
function timestamp(value, label) {
  const input = text(value, label);
  if (!/^\d{4}-\d{2}-\d{2}T.*(?:Z|[+-]\d{2}:\d{2})$/.test(input) || !Number.isFinite(Date.parse(input)))
    throw new Error(`${label} must be an ISO timestamp with a timezone`);
  return new Date(input).toISOString();
}
function parsePR(value) {
  const input = text(value, 'scope.url');
  const short = /^([\w.-]+\/[\w.-]+)#(\d+)$/.exec(input);
  if (short) return { repository: short[1], number: Number(short[2]) };
  const url = new URL(input);
  const match = /^\/([\w.-]+\/[\w.-]+)\/pull\/(\d+)\/?$/.exec(url.pathname);
  if (url.protocol !== 'https:' || url.hostname !== 'github.com' || !match || url.username || url.password)
    throw new Error('scope.url must identify one GitHub PR');
  return { repository: match[1], number: Number(match[2]) };
}
function defaultReadPR(pr) {
  return JSON.parse(execFileSync('gh', ['api', `repos/${pr.repository}/pulls/${pr.number}`, '--method', 'GET'], { encoding: 'utf8', maxBuffer: 8 * 1024 * 1024 }));
}

// Overlay same-kind preset defaults; bind source SHAs only to PR scope.
// Ranges use their own baseline, not the release PR's target-branch tip.
export function scopeRequestFromFarmInput(raw) {
  const farm = object(raw, 'inputs/qa.json');
  const preset = farm.profile?.inputs?.scope ?? {};
  const admitted = object(farm.inputs?.scope, 'inputs.scope');
  const sameKind = admitted.kind === undefined || admitted.kind === preset.kind;
  const scope = sameKind ? { ...preset, ...admitted } : { ...admitted };
  if (farm.inputs?.proof_lane !== undefined) scope.proofLane = farm.inputs.proof_lane;
  if (scope.kind !== 'pr') return scope;
  const source = farm.source ?? {};
  return {
    ...scope,
    url: scope.url ?? text(farm.sourceRef, 'sourceRef'),
    ...(source.baseSha && !scope.expectedBaseSha ? { expectedBaseSha: source.baseSha } : {}),
    ...(source.headSha && !scope.expectedHeadSha ? { expectedHeadSha: source.headSha } : {}),
  };
}

/** Resolve data only. Never check out a branch, install packages or launch an app. */
export function resolveScope(raw, { repo = process.cwd(), now = new Date(), readPR = defaultReadPR } = {}) {
  const input = object(raw, 'scope');
  const kind = input.kind;
  const allowed = {
    pr: ['kind', 'url'],
    range: ['kind', 'base', 'head'],
    window: ['kind', 'ref', 'hours', 'since', 'until'],
    ref: ['kind', 'ref'],
  }[kind];
  if (!allowed) throw new Error('scope.kind must be pr, range, window or ref');
  for (const key of Object.keys(input)) if (![...allowed, 'expectedHeadSha', 'expectedBaseSha', 'remoteFeatureFlags', 'proofLane', 'mainnetOptIn'].includes(key)) throw new Error(`Unknown ${kind} scope input: ${key}`);
  const flags = remoteFeatureFlags(input.remoteFeatureFlags);
  const lane = proofLane(input.proofLane, flags);
  if (input.mainnetOptIn !== undefined && typeof input.mainnetOptIn !== 'boolean') throw new Error('mainnetOptIn must be true or false');
  const git = (...args) => execFileSync('git', ['-C', repo, ...args], { env: gitEnvironment(), encoding: 'utf8', maxBuffer: 32 * 1024 * 1024 });
  const commit = (ref) => git('rev-parse', '--verify', '--end-of-options', `${text(ref, 'commit reference')}^{commit}`).trim();
  const hashes = (output) => output.trim() ? output.trim().split('\n') : [];
  const changes = (args) => {
    const fields = git(...args).split('\0');
    if (fields.at(-1) === '') fields.pop();
    if (fields.length % 2) throw new Error('Git returned an invalid change list');
    const result = [];
    for (let index = 0; index < fields.length; index += 2) result.push({ status: fields[index], path: fields[index + 1] });
    return result;
  };
  let baseSha, headSha, comparisonBaseSha, commits, files, source;
  if (kind === 'pr') {
    const pr = parsePR(input.url);
    const facts = readPR(pr);
    if (facts.number !== pr.number || facts.base?.repo?.full_name?.toLowerCase() !== pr.repository.toLowerCase())
      throw new Error('PR metadata belongs to another source');
    const fullSha = /^(?:[a-f0-9]{40}|[a-f0-9]{64})$/;
    if (!fullSha.test(facts.base.sha) || !fullSha.test(facts.head?.sha ?? ''))
      throw new Error('PR metadata must contain exact commits');
    baseSha = commit(facts.base.sha); headSha = commit(facts.head.sha);
    if (baseSha !== facts.base.sha || headSha !== facts.head.sha) throw new Error('Local objects do not match the PR commits');
    const bases = hashes(git('merge-base', '--all', baseSha, headSha));
    if (bases.length !== 1) throw new Error('PR has no unique merge base; resolve its comparison explicitly');
    comparisonBaseSha = bases[0];
    source = { ...pr, url: `https://github.com/${pr.repository}/pull/${pr.number}`, headRepository: facts.head.repo?.full_name ?? null, trust: facts.head.repo?.full_name?.toLowerCase() === pr.repository.toLowerCase() ? 'same-repository' : 'fork' };
  } else if (kind === 'range') {
    baseSha = commit(input.base); headSha = commit(input.head);
    comparisonBaseSha = baseSha;
    source = { base: input.base, head: input.head };
  } else if (kind === 'ref') {
    // One commit and no diff: the criteria come from a domain plan or the caller.
    headSha = commit(input.ref); baseSha = headSha; comparisonBaseSha = headSha;
    source = { ref: input.ref };
  } else {
    const until = timestamp(input.until ?? now.toISOString(), 'scope.until');
    const hours = input.hours ?? 24;
    if (!input.since && (typeof hours !== 'number' || !Number.isFinite(hours) || hours <= 0))
      throw new Error('scope.hours must be a positive number');
    const since = timestamp(input.since ?? new Date(Date.parse(until) - hours * 3_600_000).toISOString(), 'scope.since');
    if (Date.parse(since) >= Date.parse(until)) throw new Error('scope.since must precede scope.until');
    const requestedHeadSha = commit(input.ref ?? 'HEAD');
    headSha = git('rev-list', '--first-parent', '-1', `--before=${until}`, requestedHeadSha).trim();
    if (!headSha) throw new Error('No commit exists at the requested cutoff');
    commits = hashes(git('rev-list', '--first-parent', '--reverse', `--since-as-filter=${since}`, `--until=${until}`, headSha));
    const selected = new Map();
    for (const sha of commits) {
      const parent = git('show', '-s', '--format=%P', sha).trim().split(' ')[0];
      const entries = parent
        ? changes(['diff', '--name-status', '--no-renames', '-z', parent, sha, '--'])
        : changes(['diff-tree', '--root', '--no-commit-id', '--name-status', '--no-renames', '-r', '-z', sha, '--']);
      for (const entry of entries) selected.set(entry.path, entry);
    }
    const firstParent = commits.length ? git('show', '-s', '--format=%P', commits[0]).trim().split(' ')[0] : headSha;
    baseSha = firstParent || null;
    comparisonBaseSha = baseSha;
    files = [...selected.values()].sort((a, b) => a.path.localeCompare(b.path));
    source = { ref: input.ref ?? 'HEAD', requestedHeadSha, since, until, selection: 'first-parent commits by committer timestamp; files are the union of their changes' };
  }
  if (input.expectedHeadSha && input.expectedHeadSha !== headSha) throw new Error('Resolved head differs from the requested revision; do not prepare or execute this target');
  if (input.expectedBaseSha && input.expectedBaseSha !== baseSha) throw new Error('Resolved baseline differs from the requested revision; do not prepare or execute this target');
  if (kind !== 'window') {
    commits = hashes(git('rev-list', '--reverse', `${comparisonBaseSha}..${headSha}`));
    files = changes(['diff', '--name-status', '--no-renames', '-z', comparisonBaseSha, headSha, '--']);
  }
  const scope = { schemaVersion: 1, kind, source, baseSha, comparisonBaseSha, headSha, commits, files, empty: files.length === 0 };
  if (flags) Object.assign(scope, { remoteFeatureFlags: flags, remoteFlagSpec: remoteFlagSpec(flags) });
  if (lane) scope.proofLane = lane;
  if (input.mainnetOptIn) scope.mainnetOptIn = true;
  return { ...scope, sha256: createHash('sha256').update(JSON.stringify(scope)).digest('hex') };
}

function main() {
  const { values } = parseArgs({ options: { input: { type: 'string' }, out: { type: 'string' }, repo: { type: 'string' }, 'farm-input': { type: 'string' }, help: { type: 'boolean' } } });
  if (values.help) {
    console.log('resolve-scope --input <scope-request.json> --out <new-qa-scope.json> [--repo <checkout>]');
    console.log('resolve-scope --farm-input <task>/inputs/qa.json --out <task>/inputs/qa-scope-request.json');
    return;
  }
  if (values['farm-input']) {
    if (!values.out) throw new Error('--farm-input requires --out');
    const request = JSON.stringify(scopeRequestFromFarmInput(JSON.parse(readFileSync(values['farm-input'], 'utf8'))), null, 2) + '\n';
    if (existsSync(values.out)) {
      if (readFileSync(values.out, 'utf8') !== request) throw new Error('Scope request differs from the frozen one: this is a new task, not a resume.');
    } else {
      mkdirSync(path.dirname(path.resolve(values.out)), { recursive: true });
      writeNewFile(values.out, request);
    }
    console.log(request.trim());
    return;
  }
  if (!values.input || !values.out) throw new Error('--input and --out are required');
  if (existsSync(values.out)) throw new Error('Scope output already exists. Reuse the frozen artifact or create a new task.');
  const input = JSON.parse(readFileSync(values.input, 'utf8'));
  const result = resolveScope(input, { repo: values.repo });
  mkdirSync(path.dirname(path.resolve(values.out)), { recursive: true });
  writeNewFile(values.out, JSON.stringify(result, null, 2) + '\n');
  console.log(JSON.stringify({ path: path.resolve(values.out), sha256: result.sha256, headSha: result.headSha, files: result.files.length, empty: result.empty }));
}
if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) main();
