import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { access, readFile, realpath } from 'node:fs/promises';
import { constants } from 'node:fs';
import { createRequire } from 'node:module';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

async function installedSdk() {
  assert(process.env.MM_HARNESS_PACKAGE_ROOT, 'Retained task verification requires MM_HARNESS_PACKAGE_ROOT');
  const installed = createRequire(path.join(process.env.MM_HARNESS_PACKAGE_ROOT, 'package.json'));
  return import(pathToFileURL(installed.resolve('@farmslot/recipe-cli/harness')).href);
}

/** Verify each task through its producer's receipt contract without replacing its tooling. */
export async function verifyHarness(task) {
  const lock = JSON.parse(await readFile(path.join(task, 'artifacts/harness-provenance.json'), 'utf8'));
  if (lock.source?.kind === 'task-retained') {
    // Trust the installed SDK before loading anything from the task's retained pin.
    const { verifySelectedTask } = await installedSdk();
    return verifySelectedTask(task);
  }
  execFileSync(fileURLToPath(new URL('resolve-harness', import.meta.url)), [task, '--verify-only'], { stdio: 'pipe' });
  return JSON.parse(await readFile(path.join(task, 'artifacts/harness-provenance.json'), 'utf8'));
}

/** Resolve a public launcher through the SDK metadata API, never inside a task pin. */
export async function recordedHarnessExecutable(task, lock) {
  lock ??= await verifyHarness(task);
  const selected = JSON.parse(await readFile(path.join(task, 'inputs/recipe-binding.json'), 'utf8'));
  const sdk = await installedSdk();
  for (const library of lock.bindingIdentity.libraries) {
    if (library.path === selected.provider.root || library.path.startsWith(`${selected.provider.root}${path.sep}`)) continue;
    assert.equal(sdk.sourceSnapshot(library.path).sourceFingerprint, library.sourceFingerprint,
      `Recorded library source changed: ${library.name}`);
  }
  const options = {
    tokens: ['--target', selected.checkoutRoot, '--project', lock.bindingIdentity.project,
      '--adapter', lock.bindingIdentity.adapter, ...(lock.bindingIdentity.app ? ['--app', lock.bindingIdentity.app] : [])],
    projectsDir: process.env.FARMSLOT_PROJECTS_DIR,
    slotPoolDir: process.env.FARMSLOT_POOL_DIR,
  };
  const location = await sdk.resolveHarnessContext({ ...options, adapter: false });
  let root = process.env.MM_HARNESS_PACKAGE_ROOT;
  if (location.slot?.value && location.slot.poolFile) {
    if (!options.projectsDir) {
      const packInput = lock.retainedInputs.find(entry => selected.packRoot === entry.source
        || selected.packRoot.startsWith(`${entry.source}${path.sep}`));
      assert(packInput, 'Task project configuration was not retained');
      const packRoot = path.join(packInput.path, path.relative(packInput.source, selected.packRoot));
      options.projectsDir = path.dirname(packRoot);
    }
    root = (await sdk.resolveProjectContext({ ...options, load: { env: {} } })).project.provider.root;
  }
  const manifest = JSON.parse(await readFile(path.join(root, 'package.json'), 'utf8'));
  assert.equal(manifest.name, '@deeeed/metamask-harness', 'Selected provider is not the MetaMask harness');
  const bin = typeof manifest.bin === 'string' ? manifest.bin : manifest.bin?.['mm-harness'];
  assert(typeof bin === 'string' && bin, 'Selected provider has no mm-harness executable');
  const executable = await realpath(path.resolve(root, bin));
  assert(executable.startsWith(`${await realpath(root)}${path.sep}`), 'Harness executable is outside its selected package');
  assert(!lock.retainedInputs.some(entry => executable.startsWith(`${entry.path}${path.sep}`)),
    'Selected harness launcher is inside the frozen task pin');
  if (selected.provider.version !== manifest.version) {
    console.warn(`Task recorded harness ${selected.provider.version ?? 'unknown'}; using configured ${manifest.version} (${root}).`);
  }
  await access(executable, constants.X_OK);
  return executable;
}

if (process.argv[1] && fileURLToPath(import.meta.url) === await realpath(process.argv[1])) {
  assert(process.argv[2], 'Usage: verify-harness.mjs <task-dir>');
  const task = path.resolve(process.argv[2]);
  const mode = process.argv[3];
  assert(mode === undefined || mode === '--runtime', 'Unknown verification mode');
  const lock = await verifyHarness(task);
  if (mode === '--runtime') console.log(lock.source.kind === 'task-retained'
    ? await recordedHarnessExecutable(task, lock)
    : execFileSync(fileURLToPath(new URL('resolve-harness', import.meta.url)), [task, '--verify-only'], { encoding: 'utf8' }).trim());
  else console.log(lock.source.kind);
}
