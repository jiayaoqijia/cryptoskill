#!/usr/bin/env node
import { writeNewFile } from './write-new-file.mjs';
import { execFileSync, spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { closeSync, existsSync, mkdirSync, mkdtempSync, openSync, readFileSync, renameSync, rmSync } from 'node:fs';
import path from 'node:path';
import { parseArgs } from 'node:util';
import { pathToFileURL } from 'node:url';

// Release-head CI builds only; PR events build a synthetic merge.
const SOURCES = {
  android: {
    repository: 'MetaMask/metamask-mobile',
    workflow: 'build-rc-auto.yml',
    artifact: 'android-apk-main-rc',
    events: ['push', 'workflow_dispatch'],
    packageId: 'io.metamask',
    member: /^metamask-rc-main-(\d+\.\d+\.\d+)-(\d+)\.apk$/,
  },
  extension: {
    repository: 'MetaMask/metamask-extension',
    workflow: 'main.yml',
    artifact: 'build-dist-webpack',
    events: ['push'],
    member: /^builds\/metamask-chrome-(\d+\.\d+\.\d+)\.zip$/,
  },
};

const sha256 = (file) => createHash('sha256').update(readFileSync(file)).digest('hex');

function defaultGitHub() {
  return {
    api: (route) => JSON.parse(execFileSync('gh', ['api', route, '--method', 'GET'], { encoding: 'utf8', maxBuffer: 8 * 1024 * 1024 })),
    download(route, file) {
      const fd = openSync(file, 'wx');
      try {
        const result = spawnSync('gh', ['api', route], { stdio: ['ignore', fd, 'pipe'], encoding: 'utf8' });
        if (result.status !== 0) throw new Error(`gh api ${route} failed: ${result.stderr.trim()}`);
      } finally { closeSync(fd); }
    },
  };
}

/** Download and verify the frozen release artifact; runtime-launch rechecks its identity. */
export function acquireOfficialArtifact({ scope, platform, out, runId, version, github = defaultGitHub() }) {
  const source = SOURCES[platform];
  if (!source) throw new Error('--platform must be android or extension (downloaded iOS is unsupported)');
  if (!scope.proofLane?.startsWith('official-')) throw new Error('The frozen scope is not an official proof lane: build it from source instead');
  if (!/^[a-f0-9]{40}$/.test(scope.headSha ?? '')) throw new Error('qa-scope.json must hold the frozen headSha');
  const head = scope.source?.head ?? scope.source?.ref;
  version ??= /(?:^|\/)release\/(\d+\.\d+\.\d+)$/.exec(head ?? '')?.[1];
  if (!/^\d+\.\d+\.\d+$/.test(version ?? '')) throw new Error('Pass --version X.Y.Z: the frozen scope does not name a release/X.Y.Z head');
  const branch = `release/${version}`;

  const runs = runId
    ? [github.api(`repos/${source.repository}/actions/runs/${runId}`)]
    : github.api(`repos/${source.repository}/actions/workflows/${source.workflow}/runs?branch=${encodeURIComponent(branch)}&head_sha=${scope.headSha}&status=completed&per_page=20`).workflow_runs;
  let run, artifact;
  for (const candidate of runs) {
    if (!source.events.includes(candidate.event)) {
      if (runId) throw new Error(`Run ${runId} is a ${candidate.event} run, not a ${source.events.join(' or ')} build of ${branch}`);
      continue;
    }
    if (candidate.head_sha !== scope.headSha || candidate.head_branch !== branch || candidate.head_repository?.full_name !== source.repository || !candidate.path?.endsWith(`/${source.workflow}`))
      throw new Error(`Run ${candidate.id} is not ${source.workflow} on ${branch} at the frozen head ${scope.headSha}`);
    artifact = github.api(`repos/${source.repository}/actions/runs/${candidate.id}/artifacts?name=${source.artifact}`).artifacts.find((entry) => !entry.expired);
    if (artifact) { run = candidate; break; }
  }
  if (!run) throw new Error(`No ${source.workflow} run on ${branch} at ${scope.headSha} holds an unexpired ${source.artifact}: the official build of this head is unavailable`);
  const digest = /^sha256:([a-f0-9]{64})$/.exec(artifact.digest ?? '')?.[1];
  if (!digest) throw new Error(`Artifact ${artifact.id} has no SHA-256 digest to verify the download against`);

  mkdirSync(out, { recursive: true });
  const archive = path.join(out, `${source.artifact}-${artifact.id}.zip`);
  if (!existsSync(archive)) {
    // Download beside the archive and rename, so an interrupted transfer never looks complete.
    const partial = `${archive}.partial`;
    rmSync(partial, { force: true });
    github.download(`repos/${source.repository}/actions/artifacts/${artifact.id}/zip`, partial);
    renameSync(partial, archive);
  }
  if (sha256(archive) !== digest) {
    rmSync(archive);
    throw new Error(`Downloaded ${source.artifact} does not match its GitHub digest ${digest}`);
  }

  const members = execFileSync('unzip', ['-Z1', archive], { encoding: 'utf8' }).split('\n').filter((name) => source.member.test(name));
  if (members.length !== 1) throw new Error(`Expected one ${source.member} in ${source.artifact}, found ${members.length}`);
  const [, memberVersion, buildId] = source.member.exec(members[0]);
  if (memberVersion !== version) throw new Error(`${members[0]} is not version ${version}`);
  // A fresh directory per extraction: nothing earlier in `out` can redirect the member.
  const extracted = mkdtempSync(path.join(out, 'extract-'));
  execFileSync('unzip', ['-q', archive, members[0], '-d', extracted]);
  const file = path.join(extracted, members[0]);
  const fileSha256 = sha256(file);

  const launch = platform === 'android'
    ? ['--adapter', 'mobile', '--platform', 'android', '--artifact-file', file, '--artifact-version', version, '--artifact-build-id', buildId, '--artifact-package-id', source.packageId, '--artifact-sha256', fileSha256]
    : ['--adapter', 'extension', '--artifact-file', file, '--artifact-version', version, '--artifact-sha256', fileSha256];
  return {
    schemaVersion: 1,
    proofLane: scope.proofLane,
    platform,
    repository: source.repository,
    branch,
    headSha: scope.headSha,
    run: { id: run.id, url: run.html_url, workflow: source.workflow, conclusion: run.conclusion },
    artifact: { id: artifact.id, name: source.artifact, digest: artifact.digest },
    file,
    sha256: fileSha256,
    version,
    ...(platform === 'android' ? { buildId, packageId: source.packageId } : {}),
    launch,
  };
}

function main() {
  const { values } = parseArgs({ options: { scope: { type: 'string' }, platform: { type: 'string' }, out: { type: 'string' }, record: { type: 'string' }, 'run-id': { type: 'string' }, version: { type: 'string' }, help: { type: 'boolean' } } });
  if (values.help) {
    console.log('acquire-official-artifact --scope <task>/artifacts/qa-scope.json --platform <android|extension> --out <scratch dir> --record <task>/artifacts/runtime-artifact.json [--run-id <id>] [--version X.Y.Z]');
    return;
  }
  if (!values.scope || !values.platform || !values.out || !values.record) throw new Error('--scope, --platform, --out and --record are required');
  if (existsSync(values.record)) throw new Error('Runtime artifact record already exists. Reuse it or create a new task.');
  const record = acquireOfficialArtifact({ scope: JSON.parse(readFileSync(values.scope, 'utf8')), platform: values.platform, out: path.resolve(values.out), runId: values['run-id'], version: values.version });
  mkdirSync(path.dirname(path.resolve(values.record)), { recursive: true });
  writeNewFile(values.record, JSON.stringify(record, null, 2) + '\n');
  console.log(JSON.stringify(record));
}
if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) main();
