#!/usr/bin/env node
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { createHash } = require('node:crypto');
const { spawnSync } = require('node:child_process');

const skillRoot = path.resolve(__dirname, '../..');
const packageScript = path.join(skillRoot, 'scripts/package-pr-evidence.js');
const uploadScript = path.join(skillRoot, 'scripts/upload-pr-evidence.js');
const resolveHarnessScript = path.resolve(skillRoot, '../recipe-cook/scripts/resolve-harness');
const scratch = fs.mkdtempSync(path.join(os.tmpdir(), 'recipe-pretty-pr-test-'));
const fakeHarnessRoot = path.join(scratch, 'harness');

function run(command, args, options = {}) {
  return spawnSync(command, args, {
    cwd: options.cwd || scratch,
    // Published-runtime checks must not override this fixture's recorded harness.
    env: { ...process.env, MM_HARNESS_BIN: '', ...options.env },
    encoding: 'utf8',
  });
}

function mustRun(command, args, options = {}) {
  const result = run(command, args, options);
  assert.equal(result.status, 0, `${command} ${args.join(' ')}\n${result.stdout}\n${result.stderr}`);
  return result;
}

function writeJson(file, value) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`);
}

// The task's mm-harness: validates recipe run packages and renders the PR body.
function installFakeHarness() {
  writeJson(path.join(fakeHarnessRoot, 'package.json'), { name: '@deeeed/metamask-harness', version: '0.92.38', bin: { 'mm-harness': 'bin/mm-harness' } });
  writeJson(path.join(fakeHarnessRoot, 'node_modules/@farmslot/recipe-cli/package.json'), { name: '@farmslot/recipe-cli', version: '0.30.0', type: 'module', main: 'dist/index.js' });
  fs.mkdirSync(path.join(fakeHarnessRoot, 'node_modules/@farmslot/recipe-cli/dist'), { recursive: true });
  fs.writeFileSync(path.join(fakeHarnessRoot, 'node_modules/@farmslot/recipe-cli/dist/index.js'), 'export {};\n');
  const bin = path.join(fakeHarnessRoot, 'bin/mm-harness');
  fs.mkdirSync(path.dirname(bin), { recursive: true });
  fs.writeFileSync(bin, `#!/usr/bin/env node
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const args = process.argv.slice(2);
if (args[0] === 'recipe-validate') {
const recipePath = args[1];
const artifactDir = args[args.indexOf('--artifact-dir') + 1];
assert.deepEqual(args, ['recipe-validate', recipePath, '--artifact-manifest', path.join(artifactDir, 'artifact-manifest.json'), '--artifact-dir', artifactDir, '--json']);
if (process.env.TEST_VALIDATOR_MODE === 'invalid') { console.log(JSON.stringify({ status: 'invalid' })); process.exit(0); }
if (process.env.TEST_VALIDATOR_MODE === 'invalid-json') { console.log('not JSON'); process.exit(0); }
const canonical = (value) => Array.isArray(value)
  ? '[' + value.map(canonical).join(',') + ']'
  : value && typeof value === 'object'
    ? '{' + Object.entries(value).sort(([a], [b]) => a < b ? -1 : a > b ? 1 : 0).map(([key, entry]) => JSON.stringify(key) + ':' + canonical(entry)).join(',') + '}'
    : JSON.stringify(value) ?? 'null';
const digest = (value) => 'sha256:' + crypto.createHash('sha256').update(canonical(value)).digest('hex');
try {
  const recipe = JSON.parse(fs.readFileSync(recipePath, 'utf8'));
  const resolution = JSON.parse(fs.readFileSync(path.join(artifactDir, 'recipe-resolution.json'), 'utf8'));
  if (resolution.schema_version !== 1 || resolution.root.digest !== digest(recipe)) throw new Error('invalid root');
  const docs = new Map();
  for (const dependency of resolution.dependencies) {
    const document = JSON.parse(fs.readFileSync(path.join(artifactDir, dependency.artifact), 'utf8'));
    if (digest(document) !== dependency.digest) throw new Error('invalid dependency');
    docs.set(dependency.ref, document);
  }
  const refs = (document) => Object.values(document.workflow.nodes).filter((node) => node.action === 'call').map((node) => node.ref);
  const actual = [
    ...refs(recipe).map((to) => resolution.root.ref + '>' + to),
    ...[...docs].flatMap(([from, document]) => refs(document).map((to) => from + '>' + to)),
  ].sort();
  const expected = resolution.edges.map((edge) => edge.from + '>' + edge.to).sort();
  if (JSON.stringify(actual) !== JSON.stringify(expected)) throw new Error('invalid edges');
  console.log(JSON.stringify({ status: 'valid', findings: [], summary: { errors: 0, warnings: 0 } }));
} catch (error) {
  console.error(error.message);
  process.exit(1);
}
process.exit(0);
}
if (args[0] === 'pr-body') {
const task = args[2];
const out = path.join(task, 'artifacts/pr-body.md');
assert.deepEqual(args, ['pr-body', 'render', task, '--out', out, '--json']);
const ok = { command: 'pr-body', subcommand: 'render', status: 'ok', taskDir: task, out };
const mode = process.env.TEST_RENDERER_MODE;
if (mode === 'fail') { console.error('retained evidence refused'); process.exit(1); }
if (mode === 'invalid-json') { console.log('not JSON'); process.exit(0); }
if (mode === 'wrong-output') { console.log(JSON.stringify({ ...ok, out: out + '.wrong' })); process.exit(0); }
if (mode === 'not-ok') { console.log(JSON.stringify({ ...ok, status: 'refused' })); process.exit(0); }
if (mode === 'missing-output') fs.rmSync(out, { force: true });
else fs.writeFileSync(out, mode === 'empty' ? '' : fs.readFileSync(path.join(task, 'artifacts/pr-description.md'), 'utf8') + '\\n<!-- PUBLIC_ARTIFACTS_RENDERED -->\\n');
console.log(JSON.stringify(ok));
process.exit(0);
}
console.error('unexpected mm-harness call: ' + args.join(' '));
process.exit(64);
`, { mode: 0o755 });
}

function makeRepo(name, slug) {
  const repo = path.join(scratch, name);
  fs.mkdirSync(repo, { recursive: true });
  mustRun('git', ['init', '-q'], { cwd: repo });
  mustRun('git', ['config', 'user.name', 'Evidence Test'], { cwd: repo });
  mustRun('git', ['config', 'user.email', 'evidence@example.invalid'], { cwd: repo });
  mustRun('git', ['remote', 'add', 'origin', `git@github.com:${slug}.git`], { cwd: repo });
  fs.writeFileSync(path.join(repo, 'package.json'), '{}\n');
  mustRun('git', ['add', 'package.json'], { cwd: repo });
  mustRun('git', ['commit', '-qm', 'fixture'], { cwd: repo });
  const task = path.join(repo, 'temp/tasks/recipe-cook/example');
  fs.mkdirSync(path.join(task, 'artifacts'), { recursive: true });
  fs.mkdirSync(path.join(task, 'inputs'), { recursive: true });
  fs.writeFileSync(path.join(task, 'artifacts/report.md'), 'Task: `TEST-1`\nVerdict: `pass`\n');
  writeJson(path.join(task, 'artifacts/recipe-quality.json'), { schemaVersion: 1, verdict: 'pass', reasons: ['The fixture proof is complete.'] });
  writeJson(path.join(task, 'artifacts/evidence-manifest.json'), { version: 1, summary: 'Fixture evidence.' });
  writeJson(path.join(task, 'inputs/handoff.json'), { schemaVersion: 1, task: { title: 'TEST-1', ticket: 'TEST-1' } });
  mustRun(resolveHarnessScript, [task], {
    env: { MM_HARNESS_BIN: path.join(fakeHarnessRoot, 'bin/mm-harness') },
  });
  return { repo, task };
}

function setOrigin(repo, url) {
  mustRun('git', ['remote', 'set-url', 'origin', url], { cwd: repo });
}

function addUpstream(repo, slug) {
  mustRun('git', ['remote', 'add', 'upstream', `git@github.com:${slug}.git`], { cwd: repo });
}

function canonicalJson(value) {
  if (Array.isArray(value)) return `[${value.map(canonicalJson).join(',')}]`;
  if (value && typeof value === 'object') {
    return `{${Object.entries(value)
      .sort(([left], [right]) => (left < right ? -1 : left > right ? 1 : 0))
      .map(([key, entry]) => `${JSON.stringify(key)}:${canonicalJson(entry)}`)
      .join(',')}}`;
  }
  return JSON.stringify(value) ?? 'null';
}

function recipeDigest(value) {
  return `sha256:${createHash('sha256').update(canonicalJson(value)).digest('hex')}`;
}

function makeRecipeProvenance(runDir, artifacts, withDependency = false) {
  const rootRecipe = {
    $schema: 'https://farmslot.io/schemas/recipe-v1.schema.json',
    description: 'Prove the example behavior.',
    workflow: {
      entry: withDependency ? 'child' : 'done',
      nodes: {
        ...(withDependency
          ? {
              child: {
                action: 'call',
                ref: 'team.example',
                intent: 'Prove the reusable example behavior.',
                next: 'done',
              },
            }
          : {}),
        done: { action: 'end', status: 'pass' },
      },
    },
  };
  const dependencyRecipe = {
    $schema: 'https://farmslot.io/schemas/recipe-v1.schema.json',
    description: 'Reusable example behavior.',
    workflow: {
      entry: 'done',
      nodes: { done: { action: 'end', status: 'pass' } },
    },
  };
  const rootDigest = recipeDigest(rootRecipe);
  const dependencyDigest = recipeDigest(dependencyRecipe);
  const dependencyArtifact = `resolved-recipes/${dependencyDigest.slice('sha256:'.length)}.recipe.json`;
  writeJson(path.join(runDir, 'recipe.json'), rootRecipe);
  writeJson(path.join(runDir, 'recipe-resolution.json'), {
    schema_version: 1,
    root: { ref: '$root:example', digest: rootDigest },
    dependencies: withDependency
      ? [{
          ref: 'team.example',
          source: 'team',
          file: 'example.recipe.json',
          digest: dependencyDigest,
          artifact: dependencyArtifact,
        }]
      : [],
    edges: withDependency ? [{ from: '$root:example', to: 'team.example' }] : [],
  });
  artifacts.push(
    { path: 'recipe.json', type: 'recipe', category: 'system' },
    { path: 'recipe-resolution.json', type: 'json', category: 'system' },
  );
  if (withDependency) {
    writeJson(path.join(runDir, dependencyArtifact), dependencyRecipe);
    artifacts.push({ path: dependencyArtifact, type: 'recipe', category: 'system' });
  }
  return { dependencyArtifact };
}

function makeCoreRun(task) {
  const runDir = path.join(task, 'artifacts/recipe-run');
  writeJson(path.join(runDir, 'summary.json'), { status: 'pass', passed: 2, failed: 0 });
  writeJson(path.join(runDir, 'trace.json'), { entries: [{ nodeId: 'tests', ok: true }] });
  fs.writeFileSync(path.join(runDir, 'report.md'), '# Headless proof\n');
  fs.mkdirSync(path.join(runDir, 'logs'), { recursive: true });
  fs.writeFileSync(path.join(runDir, 'logs/focused-test.log'), 'PASS focused Core tests\n');
  writeJson(path.join(runDir, 'tests/results.json'), { suites: 1, passed: 1 });
  fs.writeFileSync(path.join(runDir, 'UNINDEXED_SECRET_CANARY.txt'), 'must-not-be-packaged\n');
  const artifacts = [
    { path: 'summary.json', type: 'summary', category: 'system' },
    { path: 'trace.json', type: 'trace', category: 'system' },
    { path: 'report.md', type: 'report', category: 'validation' },
    { path: 'logs/focused-test.log', type: 'log', category: 'validation' },
    { path: 'tests/results.json', type: 'test', category: 'validation' },
    { path: 42, type: 'log', category: 'invalid-fixture' },
  ];
  const provenance = makeRecipeProvenance(runDir, artifacts, true);
  writeJson(path.join(runDir, 'artifact-manifest.json'), {
    version: 1,
    runStatus: 'pass',
    artifacts,
  });
  return provenance;
}

function makeVisualRun(task) {
  const runDir = path.join(task, 'artifacts/recipe-run');
  writeJson(path.join(runDir, 'summary.json'), { status: 'pass', passed: 1, failed: 0 });
  writeJson(path.join(runDir, 'trace.json'), { entries: [{ nodeId: 'capture', ok: true }] });
  fs.mkdirSync(path.join(runDir, 'screenshots'), { recursive: true });
  fs.writeFileSync(path.join(runDir, 'screenshots/proof.png'), 'indexed-image');
  fs.writeFileSync(path.join(runDir, 'screenshots/unindexed.png'), 'unindexed-image');
  const artifacts = [
    { path: 'summary.json', type: 'summary', category: 'system' },
    { path: 'trace.json', type: 'trace', category: 'system' },
    { path: 'screenshots/proof.png', type: 'screenshot', category: 'evidence', label: 'Visual proof' },
  ];
  makeRecipeProvenance(runDir, artifacts);
  writeJson(path.join(runDir, 'artifact-manifest.json'), {
    version: 1,
    runStatus: 'pass',
    artifacts,
  });
}

function installFakeGh() {
  const bin = path.join(scratch, 'bin');
  const gh = path.join(bin, 'gh');
  fs.mkdirSync(bin, { recursive: true });
  fs.writeFileSync(gh, `#!/bin/sh
printf '%s\\n' "$*" >> "$GH_CALL_LOG"
if [ "$1 $2" = "api user" ]; then echo test-owner; exit 0; fi
if [ "$1 $2 $3" = "api -X PATCH" ] || [ "$1 $2 $3" = "api -X POST" ]; then echo https://example.invalid/comment/77; exit 0; fi
if [ "$1 $2" = "pr create" ]; then echo https://example.invalid/pr/1; exit 0; fi
if [ "$1 $2" = "pr view" ]; then exit 1; fi
if [ "$1 $2" = "repo view" ]; then exit 1; fi
exit 0
`);
  fs.chmodSync(gh, 0o755);
  return bin;
}

function resetLog(log) {
  fs.rmSync(log, { force: true });
}

try {
  installFakeHarness();
  const core = makeRepo('core', 'MetaMask/core');
  fs.mkdirSync(path.join(core.repo, '.github'), { recursive: true });
  fs.writeFileSync(path.join(core.repo, '.github/pull-request-template.md'), [
    '## **Description**',
    '',
    '<!-- CORE_TEMPLATE_SENTINEL -->',
    '',
    '## **Manual testing steps**',
    '',
    '## **Pre-merge author checklist**',
    '',
    '- [ ] Template preserved',
    '',
  ].join('\n'));
  const coreProvenance = makeCoreRun(core.task);
  mustRun(process.execPath, [packageScript, '--task', core.task]);

  const corePackage = path.join(core.task, 'pr-package');
  const runPackage = path.join(corePackage, 'runs/artifacts-recipe-run');
  for (const relative of [
    'artifact-manifest.json',
    'recipe.json',
    'recipe-resolution.json',
    coreProvenance.dependencyArtifact,
    'summary.json',
    'trace.json',
    'report.md',
    'logs/focused-test.log',
    'tests/results.json',
  ]) assert.equal(fs.existsSync(path.join(runPackage, relative)), true, `missing packaged ${relative}`);
  assert.equal(fs.existsSync(path.join(runPackage, 'UNINDEXED_SECRET_CANARY.txt')), false);
  const corePrDesc = fs.readFileSync(path.join(corePackage, 'pr-desc.md'), 'utf8');
  assert.match(corePrDesc, /CORE_TEMPLATE_SENTINEL/);
  assert.match(corePrDesc, /Screenshots: N\/A — this repository is headless/);
  assert.match(corePrDesc, /Recipe evidence: `pass`/);
  assert.equal(fs.existsSync(path.join(corePackage, 'evidence.md')), true);
  assert.equal(fs.existsSync(path.join(corePackage, 'evidence-manifest.json')), true);
  assert.equal(fs.existsSync(path.join(corePackage, 'recipe-quality.json')), true);
  const packageManifest = JSON.parse(fs.readFileSync(path.join(corePackage, 'package-manifest.json'), 'utf8'));
  assert.deepEqual(packageManifest.repository, {
    canonicalSlug: 'MetaMask/core',
    targetSlug: 'MetaMask/core',
    adapter: 'core',
    visualEvidence: false,
    familySource: 'canonical-origin',
  });
  assert.equal(packageManifest.runs.length, 1);
  assert.equal(JSON.stringify(packageManifest).includes('UNINDEXED_SECRET_CANARY'), false);

  for (const [name, mutate, gap] of [
    ['missing-report', (task) => fs.rmSync(path.join(task, 'artifacts/report.md')), 'EVIDENCE_REPORT_MISSING'],
    ['empty-report', (task) => fs.writeFileSync(path.join(task, 'artifacts/report.md'), ' \n'), 'EVIDENCE_REPORT_MISSING'],
    ['missing-quality', (task) => fs.rmSync(path.join(task, 'artifacts/recipe-quality.json')), 'EVIDENCE_QUALITY_MISSING'],
    ['invalid-quality', (task) => writeJson(path.join(task, 'artifacts/recipe-quality.json'), {}), 'EVIDENCE_QUALITY_MISSING'],
    ['failed-quality', (task) => writeJson(path.join(task, 'artifacts/recipe-quality.json'), { verdict: 'fail' }), 'EVIDENCE_QUALITY_FAILED'],
    ['missing-run', (task) => fs.rmSync(path.join(task, 'artifacts/recipe-run'), { recursive: true }), 'EVIDENCE_RUN_MISSING'],
    ['incomplete-run', (task) => fs.rmSync(path.join(task, 'artifacts/recipe-run/trace.json')), 'EVIDENCE_RUN_MISSING'],
  ]) {
    const fixture = makeRepo(name, 'MetaMask/core');
    makeCoreRun(fixture.task);
    const output = path.join(fixture.task, 'pr-package');
    fs.mkdirSync(output);
    fs.writeFileSync(path.join(output, 'pr-desc.md'), 'Stale PR draft');
    mutate(fixture.task);
    const result = run(process.execPath, [packageScript, '--task', fixture.task]);
    assert.equal(result.status, 1, name);
    assert.ok(result.stderr.includes(gap), `${name}: ${result.stderr}`);
    assert.equal(fs.existsSync(output), false, `${name} left a partial package directory`);
    assert.equal(fs.existsSync(path.join(output, 'pr-desc.md')), false, `${name} retained a publishable draft`);
    assert.equal(fs.existsSync(path.join(output, 'package-manifest.json')), false, `${name} emitted a package manifest`);
  }

  writeJson(path.join(core.task, 'artifacts/recipe-quality.json'), { verdict: 'warn', reasons: ['Non-blocking limitation.'] });
  mustRun(process.execPath, [packageScript, '--task', core.task]);
  assert.match(fs.readFileSync(path.join(corePackage, 'pr-desc.md'), 'utf8'), /Recipe evidence: `warn`/);
  writeJson(path.join(core.task, 'artifacts/recipe-quality.json'), { verdict: 'pass', reasons: ['The fixture proof is complete.'] });

  // A worker-authored artifacts/pr-description.md that already follows the repo PR
  // template is the base of pr-desc.md: its text survives and packaging only adds the
  // evidence and artifact blocks. It is also the outcome file dev/fix-bug tasks write.
  const authored = makeRepo('authored-pr-description', 'MetaMask/core');
  makeCoreRun(authored.task);
  const authoredTemplate = fs.readFileSync(path.join(core.repo, '.github/pull-request-template.md'), 'utf8');
  fs.mkdirSync(path.join(authored.repo, '.github'), { recursive: true });
  fs.writeFileSync(path.join(authored.repo, '.github/pull-request-template.md'), authoredTemplate);
  fs.writeFileSync(
    path.join(authored.task, 'artifacts/pr-description.md'),
    authoredTemplate.replace(/^## \*\*Description\*\*\s*$/m, '## **Description**\n\nAUTHORED_BODY_SENTINEL: cancel-all now submits every order.'),
  );
  mustRun(process.execPath, [packageScript, '--task', authored.task]);
  const authoredPrDesc = fs.readFileSync(path.join(authored.task, 'pr-package/pr-desc.md'), 'utf8');
  assert.match(authoredPrDesc, /AUTHORED_BODY_SENTINEL/);
  assert.match(authoredPrDesc, /PUBLIC_ARTIFACTS_RENDERED/);
  assert.match(authoredPrDesc, /## \*\*Recipe artifact package\*\*/);
  assert.match(authoredPrDesc, /Screenshots: N\/A — this repository is headless/);
  assert.doesNotMatch(authoredPrDesc, /recipe-pretty-pr suggestion: edit as needed/);
  assert.equal(fs.readFileSync(path.join(authored.task, 'pr-package/evidence.md'), 'utf8').includes('AUTHORED_BODY_SENTINEL'), true);

  const frozenFiles = ['artifacts/harness-provenance.json', 'inputs/handoff.json'];
  const frozenBytes = frozenFiles.map((file) => fs.readFileSync(path.join(authored.task, file)));
  for (const mode of ['fail', 'invalid-json', 'wrong-output', 'not-ok', 'missing-output', 'empty']) {
    const refusal = run(process.execPath, [packageScript, '--task', authored.task], { env: { TEST_RENDERER_MODE: mode } });
    assert.equal(refusal.status, 1, `${mode} substituted authored prose`);
    assert.match(refusal.stderr, /EVIDENCE_PR_BODY_INVALID/);
    assert.equal(fs.existsSync(path.join(authored.task, 'pr-package/pr-desc.md')), false);
  }
  const pathBin = path.join(scratch, 'path-bin');
  fs.mkdirSync(pathBin);
  fs.writeFileSync(path.join(pathBin, 'mm-harness'), '#!/bin/sh\necho PATH_HARNESS_MUST_NOT_RUN >&2\nexit 99\n', { mode: 0o755 });
  const selected = mustRun(process.execPath, [packageScript, '--task', authored.task], { env: { PATH: `${pathBin}${path.delimiter}${process.env.PATH}` } });
  assert.doesNotMatch(selected.stderr, /PATH_HARNESS_MUST_NOT_RUN/);
  assert.match(fs.readFileSync(path.join(authored.task, 'pr-package/pr-desc.md'), 'utf8'), /PUBLIC_ARTIFACTS_RENDERED/);
  frozenFiles.forEach((file, index) => assert.deepEqual(fs.readFileSync(path.join(authored.task, file)), frozenBytes[index]));

  for (const mode of ['invalid', 'invalid-json']) {
    const refused = run(process.execPath, [packageScript, '--task', core.task], { env: { TEST_VALIDATOR_MODE: mode } });
    assert.equal(refused.status, 1);
    assert.match(refused.stderr, /Invalid Recipe v1 artifact package/);
    assert.equal(fs.existsSync(path.join(corePackage, 'pr-desc.md')), false);
  }
  mustRun(process.execPath, [packageScript, '--task', core.task]);

  const staleHarness = makeRepo('stale-harness', 'MetaMask/core');
  makeCoreRun(staleHarness.task);
  const harnessExecutable = path.join(fakeHarnessRoot, 'bin/mm-harness');
  const originalExecutable = fs.readFileSync(harnessExecutable);
  fs.appendFileSync(harnessExecutable, '# provenance drift\n');
  const staleHarnessResult = run(process.execPath, [packageScript, '--task', staleHarness.task]);
  assert.equal(staleHarnessResult.status, 1);
  assert.match(staleHarnessResult.stderr, /Harness provenance no longer matches its recorded executable and package hashes/);
  fs.writeFileSync(harnessExecutable, originalExecutable);
  fs.chmodSync(harnessExecutable, 0o755);

  const staleHarnessAuthored = makeRepo('stale-harness-authored', 'MetaMask/core');
  makeCoreRun(staleHarnessAuthored.task);
  fs.mkdirSync(path.join(staleHarnessAuthored.repo, '.github'), { recursive: true });
  fs.writeFileSync(path.join(staleHarnessAuthored.repo, '.github/pull-request-template.md'), authoredTemplate);
  fs.writeFileSync(
    path.join(staleHarnessAuthored.task, 'artifacts/pr-description.md'),
    authoredTemplate.replace(/^## \*\*Description\*\*\s*$/m, '## **Description**\n\nAUTHORED_BEFORE_VERIFY.'),
  );
  fs.appendFileSync(harnessExecutable, '# provenance drift before artifacts render\n');
  const staleAuthoredResult = run(process.execPath, [packageScript, '--task', staleHarnessAuthored.task]);
  assert.equal(staleAuthoredResult.status, 1);
  assert.match(staleAuthoredResult.stderr, /Harness provenance no longer matches its recorded executable and package hashes/);
  fs.writeFileSync(harnessExecutable, originalExecutable);
  fs.chmodSync(harnessExecutable, 0o755);

  const staleValidator = makeRepo('stale-validator', 'MetaMask/core');
  makeCoreRun(staleValidator.task);
  const validatorModule = path.join(fakeHarnessRoot, 'node_modules/@farmslot/recipe-cli/dist/index.js');
  const originalValidator = fs.readFileSync(validatorModule);
  fs.appendFileSync(validatorModule, '// provenance drift\n');
  const staleValidatorResult = run(process.execPath, [packageScript, '--task', staleValidator.task]);
  assert.equal(staleValidatorResult.status, 1);
  assert.match(staleValidatorResult.stderr, /Harness provenance no longer matches its recorded executable and package hashes/);
  fs.writeFileSync(validatorModule, originalValidator);

  const tampered = makeRepo('tampered', 'MetaMask/core');
  const tamperedProvenance = makeCoreRun(tampered.task);
  writeJson(path.join(tampered.task, 'artifacts/recipe-run', tamperedProvenance.dependencyArtifact), { tampered: true });
  const tamperedResult = run(process.execPath, [packageScript, '--task', tampered.task]);
  assert.equal(tamperedResult.status, 1);
  assert.match(tamperedResult.stderr, /Invalid Recipe v1 artifact package/);
  assert.equal(fs.existsSync(path.join(tampered.task, 'pr-package')), false);

  const partialPackage = makeRepo('partial-package', 'MetaMask/core');
  makeCoreRun(partialPackage.task);
  const invalidRun = path.join(partialPackage.task, 'artifacts/zz-invalid-run');
  fs.cpSync(path.join(partialPackage.task, 'artifacts/recipe-run'), invalidRun, { recursive: true });
  writeJson(path.join(invalidRun, 'recipe-resolution.json'), { dependencies: [] });
  const partialResult = run(process.execPath, [packageScript, '--task', partialPackage.task]);
  assert.equal(partialResult.status, 1);
  assert.match(partialResult.stderr, /Invalid Recipe v1 artifact package/);
  assert.equal(fs.existsSync(path.join(partialPackage.task, 'pr-package')), false, 'later invalid run left copied evidence behind');

  const fakeBin = installFakeGh();
  const ghLog = path.join(scratch, 'gh-calls.log');
  const env = { PATH: `${fakeBin}:${process.env.PATH}`, GH_CALL_LOG: ghLog };

  fs.rmSync(path.join(corePackage, 'pr-desc.md'));
  resetLog(ghLog);
  const missingTemplateBody = run(process.execPath, [uploadScript, '--task', core.task, '--create-pr'], { env });
  assert.equal(missingTemplateBody.status, 1);
  assert.match(missingTemplateBody.stderr, /PR creation requires .*pr-desc\.md/);
  assert.equal(fs.existsSync(ghLog), false, 'missing packaged PR body still called gh');
  mustRun(process.execPath, [packageScript, '--task', core.task]);

  resetLog(ghLog);
  const dryRun = mustRun(process.execPath, [uploadScript, '--task', core.task, '--dry-run'], { env });
  assert.equal(fs.existsSync(ghLog), false, 'headless dry-run called gh');
  assert.equal(fs.existsSync(path.join(corePackage, 'pr-body.uploaded.md')), false, 'dry-run wrote a PR body');
  const dryPlan = JSON.parse(dryRun.stdout);
  assert.equal(dryPlan.adapter, 'core');
  assert.equal(dryPlan.visualEvidence, false);
  assert.equal(dryPlan.artifactsRepo, null);
  assert.equal(dryPlan.productRepo, 'MetaMask/core');
  assert.equal(dryPlan.canonicalProductRepo, 'MetaMask/core');
  assert.equal(dryPlan.familySource, 'canonical-origin');

  resetLog(ghLog);
  mustRun(process.execPath, [uploadScript, '--task', core.task], { env });
  assert.equal(fs.existsSync(ghLog), false, 'text-only local packaging called gh without --create-pr');

  resetLog(ghLog);
  const created = mustRun(process.execPath, [uploadScript, '--task', core.task, '--create-pr'], { env });
  const createCalls = fs.readFileSync(ghLog, 'utf8');
  assert.match(createCalls, /^pr view /m);
  assert.match(createCalls, /^pr create /m);
  assert.equal(createCalls.includes('repo create'), false);
  assert.equal(createCalls.includes('api -X PUT'), false);
  assert.equal(JSON.parse(created.stdout).prUrl, 'https://example.invalid/pr/1');

  const help = mustRun(process.execPath, [uploadScript, '--help']);
  assert.match(help.stderr, /--adapter extension\|mobile\|core/);

  const unsupportedTask = makeRepo('unsupported-task', 'Other/widget');
  resetLog(ghLog);
  const crossRepo = run(process.execPath, [uploadScript, '--task', unsupportedTask.task, '--dry-run'], {
    cwd: core.repo,
    env,
  });
  assert.equal(crossRepo.status, 1);
  assert.match(crossRepo.stderr, /Could not derive a canonical MetaMask product family/);
  assert.equal(fs.existsSync(ghLog), false, 'unsupported task repo fell through to supported cwd');

  const mismatchedTask = makeRepo('mismatched-task', 'MetaMask/metamask-mobile');
  resetLog(ghLog);
  const crossRepoMismatch = run(process.execPath, [uploadScript, '--task', mismatchedTask.task, '--adapter', 'core', '--dry-run'], {
    cwd: core.repo,
    env,
  });
  assert.equal(crossRepoMismatch.status, 1);
  assert.match(crossRepoMismatch.stderr, /does not match canonical repository family mobile/);
  assert.equal(fs.existsSync(ghLog), false, 'mismatched task policy fell through to supported cwd');

  const families = [
    ['core', 'MetaMask/core', 'core'],
    ['extension', 'MetaMask/metamask-extension', 'extension'],
    ['mobile', 'MetaMask/metamask-mobile', 'mobile'],
  ];

  for (const [name, canonicalSlug, adapter] of families) {
    const repoName = canonicalSlug.split('/')[1];

    const hostile = makeRepo(`hostile-${name}`, canonicalSlug);
    setOrigin(hostile.repo, `git@github.com.evil.example:MetaMask/${repoName}.git`);
    const hostileResult = run(process.execPath, [uploadScript, '--task', hostile.task, '--adapter', adapter, '--dry-run'], { env });
    assert.equal(hostileResult.status, 1);
    assert.match(hostileResult.stderr, /approved github\.com SSH\/HTTPS remote/);

    const local = makeRepo(`local-${name}`, canonicalSlug);
    setOrigin(local.repo, `/tmp/MetaMask/${repoName}.git`);
    const localResult = run(process.execPath, [uploadScript, '--task', local.task, '--adapter', adapter, '--dry-run'], { env });
    assert.equal(localResult.status, 1);
    assert.match(localResult.stderr, /refusing local path or non-GitHub identity/);

    const fork = makeRepo(`fork-${name}`, `engineer/${repoName}`);
    addUpstream(fork.repo, canonicalSlug);
    makeCoreRun(fork.task);
    mustRun(process.execPath, [packageScript, '--task', fork.task]);
    resetLog(ghLog);
    const forkPreview = mustRun(process.execPath, [uploadScript, '--task', fork.task, '--dry-run'], { env });
    const forkPlan = JSON.parse(forkPreview.stdout);
    assert.equal(forkPlan.productRepo, `engineer/${repoName}`);
    assert.equal(forkPlan.canonicalProductRepo, canonicalSlug);
    assert.equal(forkPlan.familySource, 'canonical-upstream');
    assert.equal(fs.existsSync(ghLog), false, 'zero-image fork dry-run called gh');

    resetLog(ghLog);
    mustRun(process.execPath, [uploadScript, '--task', fork.task, '--create-pr'], { env });
    const forkCreateCalls = fs.readFileSync(ghLog, 'utf8');
    assert.match(forkCreateCalls, new RegExp(`^pr create --repo engineer/${repoName} `, 'm'));
    assert.equal(forkCreateCalls.includes(`--repo ${canonicalSlug}`), false);

    for (const [target, selector, method, suffix] of [
      ['comment', ['--comment', '77'], 'PATCH', 'issues/comments/77'],
      ['new-comment', ['--pr', '5'], 'POST', 'issues/5/comments'],
    ]) {
      resetLog(ghLog);
      const preview = mustRun(process.execPath, [uploadScript, '--task', fork.task, '--target', target, ...selector, '--dry-run'], { env });
      assert.equal(JSON.parse(preview.stdout).productRepo, canonicalSlug);
      assert.ok(preview.stderr.includes(`${method} repos/${canonicalSlug}/${suffix}`));
      assert.equal(fs.existsSync(ghLog), false, 'zero-image comment dry-run called gh');

      const uploaded = mustRun(process.execPath, [uploadScript, '--task', fork.task, '--target', target, ...selector], { env });
      const commentCalls = fs.readFileSync(ghLog, 'utf8');
      assert.match(commentCalls, new RegExp(`^api -X ${method} repos/${canonicalSlug}/${suffix} `, 'm'));
      assert.equal(commentCalls.includes(`repos/engineer/${repoName}/`), false);
      assert.equal(commentCalls.includes('pr create'), false);
      assert.equal(commentCalls.includes('pr edit'), false);
      assert.equal(JSON.parse(uploaded.stdout).productRepo, canonicalSlug);
    }

    const explicitFork = makeRepo(`explicit-${name}`, `engineer/${repoName}`);
    makeCoreRun(explicitFork.task);
    mustRun(process.execPath, [packageScript, '--task', explicitFork.task, '--adapter', adapter]);
    const explicitPreview = mustRun(process.execPath, [uploadScript, '--task', explicitFork.task, '--adapter', adapter, '--dry-run'], { env });
    const explicitPlan = JSON.parse(explicitPreview.stdout);
    assert.equal(explicitPlan.productRepo, `engineer/${repoName}`);
    assert.equal(explicitPlan.canonicalProductRepo, canonicalSlug);
    assert.equal(explicitPlan.familySource, 'explicit-adapter');
  }

  for (const [name, slug, adapter] of families.filter(([family]) => family !== 'core')) {
    const fixture = makeRepo(name, slug);
    makeVisualRun(fixture.task);
    mustRun(process.execPath, [packageScript, '--task', fixture.task]);
    const images = path.join(fixture.task, 'pr-package/images');
    const packagedImages = fs.readdirSync(images).filter((file) => file.endsWith('.png'));
    assert.deepEqual(packagedImages, ['01-visual-proof.png']);
    assert.equal(fs.readFileSync(path.join(images, packagedImages[0]), 'utf8'), 'indexed-image');

    const visualPackage = path.join(fixture.task, 'pr-package');
    fs.rmSync(path.join(visualPackage, 'pr-desc.md'));
    resetLog(ghLog);
    const missingVisualTemplate = run(process.execPath, [
      uploadScript,
      '--task', fixture.task,
      '--create-pr',
      '--confirm-public-upload',
      '--ensure-repo',
    ], { env });
    assert.equal(missingVisualTemplate.status, 1);
    assert.match(missingVisualTemplate.stderr, /PR creation requires .*pr-desc\.md/);
    assert.equal(fs.existsSync(ghLog), false, `${adapter} missing packaged PR body still called gh`);
    assert.equal(fs.existsSync(path.join(visualPackage, 'pr-body.uploaded.md')), false, `${adapter} missing packaged PR body wrote a local upload body`);
    assert.deepEqual(fs.readdirSync(images).filter((file) => file.endsWith('.png')), packagedImages);
    mustRun(process.execPath, [packageScript, '--task', fixture.task]);

    resetLog(ghLog);
    const denied = run(process.execPath, [uploadScript, '--task', fixture.task], { env });
    assert.equal(denied.status, 1);
    assert.match(denied.stderr, /--confirm-public-upload/);
    assert.match(denied.stderr, new RegExp(`mm-${adapter}-artifacts`));
    const calls = fs.readFileSync(ghLog, 'utf8');
    assert.match(calls, /^api user /m);
    assert.equal(calls.includes('repo create'), false);
    assert.equal(calls.includes('api -X PUT'), false);

    // Evidence comment: the task report, hosted images injected, written to one
    // comment in place; never the PR body, never without the report.
    const reportPath = path.join(fixture.task, 'artifacts/report.md');
    fs.renameSync(reportPath, `${reportPath}.aside`);
    resetLog(ghLog);
    const noReport = run(process.execPath, [uploadScript, '--task', fixture.task, '--target', 'comment', '--comment', '77', '--confirm-public-upload'], { env });
    assert.equal(noReport.status, 1);
    assert.match(noReport.stderr, /needs the comment text/);
    fs.writeFileSync(reportPath, '## QA review\n\nVerdict: FAIL\n\n| AC | Result |\n|---|---|\n| AC1 | PASS |\n');
    resetLog(ghLog);
    const commentDry = mustRun(process.execPath, [uploadScript, '--task', fixture.task, '--target', 'comment', '--comment', '77', '--dry-run'], { env });
    assert.equal(JSON.parse(commentDry.stdout).target, 'comment');
    assert.equal(fs.readFileSync(ghLog, 'utf8').includes('api -X PATCH'), false, `${adapter} comment dry-run wrote a comment`);
    resetLog(ghLog);
    const commented = mustRun(process.execPath, [uploadScript, '--task', fixture.task, '--target', 'comment', '--comment', '77', '--confirm-public-upload', '--ensure-repo'], { env });
    const commentCalls = fs.readFileSync(ghLog, 'utf8');
    assert.match(commentCalls, /^api -X PUT /m);
    assert.match(commentCalls, new RegExp(`^api -X PATCH repos/${slug}/issues/comments/77 `, 'm'));
    assert.equal(commentCalls.includes('pr create'), false);
    assert.equal(commentCalls.includes('pr edit'), false);
    assert.equal(JSON.parse(commented.stdout).commentUrl, 'https://example.invalid/comment/77');
    const commentBody = fs.readFileSync(path.join(visualPackage, 'comment-body.uploaded.md'), 'utf8');
    assert.match(commentBody, /Verdict: FAIL/);
    assert.match(commentBody, new RegExp(`<img src="https://raw\\.githubusercontent\\.com/test-owner/mm-${adapter}-artifacts/`));
    resetLog(ghLog);
    const posted = mustRun(process.execPath, [uploadScript, '--task', fixture.task, '--target', 'new-comment', '--pr', '5', '--confirm-public-upload', '--ensure-repo'], { env });
    assert.match(fs.readFileSync(ghLog, 'utf8'), new RegExp(`^api -X POST repos/${slug}/issues/5/comments `, 'm'));
    assert.equal(JSON.parse(posted.stdout).commentUrl, 'https://example.invalid/comment/77');
    const badTarget = run(process.execPath, [uploadScript, '--task', fixture.task, '--target', 'comment'], { env });
    assert.equal(badTarget.status, 1);
    assert.match(badTarget.stderr, /--comment <id>/);
    // Cook's evidence-manifest selection restricts and captions the hosted set.
    const selectionPath = path.join(fixture.task, 'artifacts/evidence-manifest.json');
    writeJson(selectionPath, { version: 1, preferred_mode: 'screenshots', standalone: [{ label: 'AC1 proof', covers: ['AC1'], file: 'proof.png' }] });
    fs.writeFileSync(path.join(fixture.task, 'artifacts/recipe-run/screenshots/other.png'), 'other-image');
    const manifestPath = path.join(fixture.task, 'artifacts/recipe-run/artifact-manifest.json');
    const manifestBefore = fs.readFileSync(manifestPath, 'utf8');
    const manifestDoc = JSON.parse(manifestBefore);
    manifestDoc.artifacts.push({ path: 'screenshots/other.png', type: 'screenshot', category: 'evidence', label: 'Other' });
    writeJson(manifestPath, manifestDoc);
    makeRecipeProvenance(path.join(fixture.task, 'artifacts/recipe-run'), manifestDoc.artifacts);
    mustRun(process.execPath, [packageScript, '--task', fixture.task]);
    assert.deepEqual(fs.readdirSync(images).filter((file) => file.endsWith('.png')), ['01-ac1-proof.png']);
    fs.rmSync(selectionPath);
    mustRun(process.execPath, [packageScript, '--task', fixture.task]);
    assert.deepEqual(fs.readdirSync(images).filter((file) => file.endsWith('.png')), ['01-other.png', '02-visual-proof.png']);
    fs.rmSync(path.join(fixture.task, 'artifacts/recipe-run/screenshots/other.png'));
    fs.writeFileSync(manifestPath, manifestBefore);
    makeRecipeProvenance(path.join(fixture.task, 'artifacts/recipe-run'), JSON.parse(manifestBefore).artifacts);
    mustRun(process.execPath, [packageScript, '--task', fixture.task]);

    // A failed quality verdict is refused for a PR body and carried for a comment.
    const qualityPath = path.join(fixture.task, 'artifacts/recipe-quality.json');
    const qualityBefore = fs.readFileSync(qualityPath, 'utf8');
    fs.writeFileSync(qualityPath, JSON.stringify({ ...JSON.parse(qualityBefore), verdict: 'fail' }));
    const failedPackage = run(process.execPath, [packageScript, '--task', fixture.task]);
    assert.equal(failedPackage.status, 1);
    assert.match(failedPackage.stderr, /EVIDENCE_QUALITY_FAILED/);
    mustRun(process.execPath, [packageScript, '--task', fixture.task, '--allow-fail']);
    fs.writeFileSync(qualityPath, qualityBefore);
    mustRun(process.execPath, [packageScript, '--task', fixture.task]);

    resetLog(ghLog);
    const preview = mustRun(process.execPath, [uploadScript, '--task', fixture.task, '--dry-run'], { env });
    const previewPlan = JSON.parse(preview.stdout);
    assert.equal(previewPlan.adapter, adapter);
    assert.equal(previewPlan.productRepo, slug);
    assert.equal(previewPlan.canonicalProductRepo, slug);
    assert.equal(previewPlan.familySource, 'canonical-origin');
    const previewCalls = fs.readFileSync(ghLog, 'utf8');
    assert.match(previewCalls, /^api user /m);
    assert.match(previewCalls, /^repo view /m);
    assert.equal(previewCalls.includes('repo create'), false);
    assert.equal(previewCalls.includes('api -X PUT'), false);
  }

  // HTML-only QA tasks must package and publish without an authored Markdown
  // duplicate. The same consent applies when there are no standalone images.
  for (const adapter of ['core', 'extension', 'mobile']) {
    const slug = adapter === 'core' ? 'MetaMask/core' : `MetaMask/metamask-${adapter}`;
    const fixture = makeRepo(`html-qa-${adapter}`, slug);
    if (adapter === 'core') makeCoreRun(fixture.task);
    else makeVisualRun(fixture.task);
    const artifacts = path.join(fixture.task, 'artifacts');
    const html = '<!doctype html><html><body><h1>QA finding</h1><p>FAIL: warning absent.</p></body></html>';
    const data = { title: 'QA <finding>', verdict: 'FAIL', summary: 'Warning absent; other criteria remain unproved.' };
    fs.rmSync(path.join(artifacts, 'report.md'));
    fs.writeFileSync(path.join(artifacts, 'report.html'), html);
    writeJson(path.join(artifacts, 'report-data.json'), data);
    writeJson(path.join(artifacts, 'recipe-quality.json'), { verdict: 'fail', reasons: ['Incomplete proof remains explicit.'] });
    const refused = run(process.execPath, [packageScript, '--task', fixture.task]);
    assert.match(refused.stderr, /EVIDENCE_QUALITY_FAILED/);
    mustRun(process.execPath, [packageScript, '--task', fixture.task, '--allow-fail']);
    const packaged = path.join(fixture.task, 'pr-package');
    assert.equal(fs.readFileSync(path.join(packaged, 'report.html'), 'utf8'), html);
    assert.equal(fs.existsSync(path.join(packaged, 'evidence.md')), false);
    assert.equal(fs.existsSync(path.join(artifacts, 'report.md')), false);
    assert.match(fs.readFileSync(path.join(packaged, 'pr-desc.md'), 'utf8'), /pr-package\/report\.html/);
    assert.equal(JSON.parse(fs.readFileSync(path.join(packaged, 'package-manifest.json'))).files.evidence, path.join(packaged, 'report.html'));

    resetLog(ghLog);
    const preview = mustRun(process.execPath, [uploadScript, '--task', fixture.task, '--target', 'new-comment', '--pr', '5', '--dry-run'], { env });
    const plan = JSON.parse(preview.stdout);
    assert.equal(plan.report, 'report.html');
    assert.match(plan.reportUrl, /\/report\.html$/);
    assert.doesNotMatch(fs.readFileSync(ghLog, 'utf8'), /api -X|repo create/);
    assert.equal(fs.existsSync(path.join(packaged, 'comment-body.uploaded.md')), false);

    resetLog(ghLog);
    const denied = run(process.execPath, [uploadScript, '--task', fixture.task, '--target', 'new-comment', '--pr', '5'], { env });
    assert.equal(denied.status, 1);
    assert.match(denied.stderr, /HTML report.*explicit consent/);
    assert.doesNotMatch(fs.readFileSync(ghLog, 'utf8'), /api -X|repo create/);

    // A stale legacy report must not override the current HTML report's FAIL.
    fs.writeFileSync(path.join(artifacts, 'report.md'), 'Stale legacy verdict: PASS');
    for (const [target, idArgs, method] of [['new-comment', ['--pr', '5'], 'POST'], ['comment', ['--comment', '77'], 'PATCH']]) {
      resetLog(ghLog);
      mustRun(process.execPath, [uploadScript, '--task', fixture.task, '--target', target, ...idArgs, '--confirm-public-upload', '--ensure-repo'], { env });
      const calls = fs.readFileSync(ghLog, 'utf8');
      assert.match(calls, /^api -X PUT .*\/report\.html /m);
      assert.match(calls, new RegExp(`^api -X ${method} repos/${slug}/issues/`, 'm'));
      assert.doesNotMatch(calls, /pr create|pr edit/);
      const body = fs.readFileSync(path.join(packaged, 'comment-body.uploaded.md'), 'utf8');
      assert.match(body, /QA &lt;finding&gt;/);
      assert.match(body, /Verdict: FAIL/);
      assert.match(body, /Warning absent; other criteria remain unproved/);
      assert.match(body, /\[Full HTML report\]\(https:\/\/github\.com\//);
      assert.doesNotMatch(body, /Stale legacy|<!doctype|<html>/);
    }

    fs.rmSync(path.join(artifacts, 'report-data.json'));
    resetLog(ghLog);
    const missingData = run(process.execPath, [uploadScript, '--task', fixture.task, '--target', 'new-comment', '--pr', '5', '--dry-run'], { env });
    assert.equal(missingData.status, 1);
    assert.match(missingData.stderr, /report-data\.json/);
    assert.equal(fs.existsSync(ghLog), false, 'invalid HTML report reached GitHub');
  }

  console.log('recipe-pretty-pr Core headless packaging, consent, and platform regressions: PASS');
} finally {
  fs.rmSync(scratch, { recursive: true, force: true });
}
