import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { spawnSync } from 'node:child_process';
import { chmod, mkdtemp, mkdir, readFile, readdir, realpath, rm, symlink, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const init = fileURLToPath(new URL('../init-template', import.meta.url));
export async function snapshot(root) {
  const files = {};
  for (const name of await readdir(root, { recursive: true, withFileTypes: true })) {
    if (name.isFile()) {
      const file = path.join(name.parentPath, name.name);
      files[path.relative(root, file)] = await readFile(file, 'utf8');
    }
  }
  return files;
}

export async function retainedFixture(t, scenario) {
  const root = await realpath(await mkdtemp(path.join(os.tmpdir(), 'cook-resume-pin-')));
  t.after(() => rm(root, { recursive: true, force: true }));
  const task = path.join(root, 'task');
  const provider = path.join(root, 'installed');
  const originalProvider = path.join(root, 'original-provider');
  const poolProvider = path.join(root, 'pool-provider');
  const canonicalLibrary = path.join(root, 'canonical-library');
  const packRoot = path.join(root, 'project-pack');
  const retainedPack = path.join(root, 'pin/project-pack');
  const upgraded = ['pool-update', 'pool-no-registry', 'direct-no-pool'].includes(scenario);
  const recordedVersion = upgraded ? '0.94.1' : '0.94.3';
  const retainedProvider = path.join(root, 'pin/provider');
  const retainedCli = path.join(root, 'pin/farmslot');
  const sdk = path.join(provider, 'node_modules/@farmslot/recipe-cli');
  await mkdir(path.join(task, 'artifacts'), { recursive: true });
  await mkdir(path.join(task, 'inputs'), { recursive: true });
  await mkdir(path.join(retainedProvider, 'bin'), { recursive: true });
  await mkdir(path.join(originalProvider, 'bin'), { recursive: true });
  await mkdir(sdk, { recursive: true });
  await mkdir(canonicalLibrary);
  await mkdir(retainedPack);
  await writeFile(path.join(retainedPack, 'project.json'), JSON.stringify({ name: 'fixture', paths: { runtime_dir: 'temp/recipe/runtime', artifact_dir: 'temp/artifacts' } }));
  await writeFile(path.join(canonicalLibrary, 'source'), 'library-v1');
  const libraryFingerprint = createHash('sha256').update('library-v1').digest('hex');
  for (const installation of [originalProvider, retainedProvider, provider, poolProvider]) {
    await mkdir(path.join(installation, 'bin'), { recursive: true });
    const version = upgraded && (installation === poolProvider || (installation === provider && scenario === 'direct-no-pool')) ? '0.94.6' : recordedVersion;
    await writeFile(path.join(installation, 'package.json'), JSON.stringify({ name: scenario === 'wrong-provider' ? '@farmslot/cli' : '@deeeed/metamask-harness', version, bin: { 'mm-harness': 'bin/mm-harness' } }));
    await writeFile(path.join(installation, 'bin/mm-harness'), '#!/bin/sh\nROOT="$(cd "$(dirname "$0")/.." && pwd)"\nmkdir -p "$ROOT/node_modules/@deeeed"\n[ -e "$ROOT/node_modules/@deeeed/metamask-harness" ] || ln -s "$ROOT" "$ROOT/node_modules/@deeeed/metamask-harness"\nprintf \'{"package":"@deeeed/metamask-harness","version":"0.94.3"}\\n\'\n'.replace('0.94.3', version));
    await chmod(path.join(installation, 'bin/mm-harness'), 0o755);
  }
  await writeFile(retainedCli, '#!/bin/sh\nprintf \'%s\\n\' "$@"\n');
  await chmod(retainedCli, 0o755);
  for (const [name, contents] of Object.entries({
    'TASK.md': '# Original task\n', 'CHECKLIST.md': '- [x] Original step\n',
    mark: '#!/bin/sh\nexit 73\n',
    'artifacts/harness-provenance.json': JSON.stringify({ package: { name: '@farmslot/cli', version: '0.3.0' }, source: { kind: 'task-retained', packageRoot: '/unused' }, resolvedExecutable: retainedCli, retainedInputs: [{ source: originalProvider, path: retainedProvider }, { source: packRoot, path: retainedPack }], bindingIdentity: { project: 'fixture', adapter: 'extension', provider: { sourceFingerprint: 'provider-proof' }, libraries: [{ name: 'perps', path: canonicalLibrary, sourceFingerprint: libraryFingerprint }] } }),
    'inputs/recipe-binding.json': JSON.stringify({ checkoutRoot: root, packRoot, provider: { root: originalProvider, module: path.join(originalProvider, 'dist/provider.js'), version: recordedVersion } }),
  })) await writeFile(path.join(task, name), contents);
  await writeFile(path.join(sdk, 'package.json'), JSON.stringify({ name: '@farmslot/recipe-cli', type: 'module', exports: { './harness': './index.mjs' } }));
  await writeFile(path.join(sdk, 'index.mjs'), `import { readFileSync } from 'node:fs';
    import { createHash } from 'node:crypto';
    import path from 'node:path';
    export function verifySelectedTask(task) {
      ${scenario === 'rejected-pin' ? "throw new Error('TASK_INPUT_CHANGED');" : "return JSON.parse(readFileSync(path.join(task, 'artifacts/harness-provenance.json')));"}
    }
    export function sourceSnapshot(directory) {
      return { sourceFingerprint: createHash('sha256').update(readFileSync(path.join(directory, 'source'))).digest('hex') };
    }
    export async function resolveHarnessContext() {
      return { slot: ${JSON.stringify(['pool-update', 'pool-no-registry', 'unsafe-pool'].includes(scenario) ? { value: 'one', poolFile: 'fixture-pool' } : { value: null })} };
    }
    export async function resolveProjectContext(options) {
      if (Object.keys(options.load.env).length) throw new Error('Stale ambient provider reached pool selection');
      if (!options.projectsDir) throw new Error('PROJECT_NOT_FOUND');
      if (options.projectsDir === ${JSON.stringify(path.dirname(retainedPack))}) {
        const pack = JSON.parse(readFileSync(path.join(options.projectsDir, 'project-pack/project.json')));
        if (pack.name !== 'fixture' || !pack.paths.runtime_dir || !pack.paths.artifact_dir) throw new Error('Wrong retained project');
      }
      return { project: { provider: { root: ${JSON.stringify(scenario === 'unsafe-pool' ? retainedProvider : poolProvider)} } } };
    }
    export async function withTaskProjectHost(_options, _task, invoke) {
      return invoke({ context: { project: { provider: { root: ${JSON.stringify(retainedProvider)} } } } });
    }`);
  const scripts = path.join(root, 'installed-scripts');
  await symlink(path.dirname(init), scripts);
  if (scenario === 'existing-runner') await writeFile(path.join(task, 'mm-harness'), '#!/bin/sh\nexit 71\n');
  if (scenario === 'changed-library') await writeFile(path.join(canonicalLibrary, 'source'), 'library-v2');
  const before = await snapshot(task);
  const env = { ...process.env, MM_HARNESS_PACKAGE_ROOT: provider };
  if (scenario === 'pool-no-registry') delete env.FARMSLOT_PROJECTS_DIR;
  return { task, provider, poolProvider, originalProvider, retainedProvider, retainedCli, scripts, env, before };
}
