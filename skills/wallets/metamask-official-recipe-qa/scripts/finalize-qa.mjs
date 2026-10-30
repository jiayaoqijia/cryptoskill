#!/usr/bin/env node
import assert from 'node:assert/strict';
import { access, mkdir, readFile, realpath, writeFile } from 'node:fs/promises';
import { createRequire } from 'node:module';
import path from 'node:path';
import { parseArgs } from 'node:util';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { reselectQa } from './reselect-qa.mjs';

const json = async (file) => JSON.parse(await readFile(file, 'utf8'));
const record = (value) => value && typeof value === 'object' && !Array.isArray(value);
async function contained(root, relative) {
  assert(typeof relative === 'string' && relative && !path.isAbsolute(relative));
  assert(!relative.split(/[\\/]/).some((part) => !part || part === '..' || part === '.'));
  const resolved = await realpath(path.join(root, relative));
  assert(resolved.startsWith(await realpath(root) + path.sep), 'QA evidence escapes the task');
  return resolved;
}

/** Assemble the standard suite and task index from actual retained run packages. */
export async function finalizeQa(task, index, suitePath = 'qa-suite', checkOnly = false, reselection) {
  task = await realpath(task);
  const artifacts = path.join(task, 'artifacts');
  const resultPath = path.join(artifacts, 'qa-proof.json');
  if (!checkOnly && !reselection) await assert.rejects(access(resultPath), { code: 'ENOENT' }, 'QA result already exists');
  const skillRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
  const ownName = path.basename(path.dirname(path.dirname(fileURLToPath(import.meta.url))));
  const { verifyHarness } = await import(pathToFileURL(path.join(skillRoot, ownName.replace(/recipe-qa$/, 'recipe-cook'), 'scripts/verify-harness.mjs')).href);
  const lock = await verifyHarness(task);
  const require = createRequire(path.join(lock.source.packageRoot, 'package.json'));
  const { freezeRecipeSuiteScope, finalizeRecipeSuite } = await import(pathToFileURL(require.resolve('@farmslot/recipe-runner')).href);
  const { digestRecipeDocument, RECIPE_SUITE_SCOPE_SCHEMA_URL } = await import(pathToFileURL(require.resolve('@farmslot/protocol')).href);
  const { validateRuntimeProof } = await import(pathToFileURL(require.resolve('@farmslot/recipe-cli/harness')).href);
  assert.equal(typeof validateRuntimeProof, 'function', 'The locked harness must provide portable runtime proof validation');
  const source = await json(path.join(artifacts, 'qa-scope.json'));
  assert(record(index.packages) && record(index.smoke), 'Expected packages and smoke index');
  const suiteDir = path.join(artifacts, suitePath);
  const suiteScopePath = path.join(suiteDir, 'suite-scope.json');
  // A smoke check validates a partial index without freezing the final suite.
  let scopeDocument;
  if (checkOnly) {
    scopeDocument = { $schema: RECIPE_SUITE_SCOPE_SCHEMA_URL, suite_id: `qa-${path.basename(task)}`, cases: Object.keys(index.packages).sort().map((id) => ({ id })) };
  } else if (reselection) {
    scopeDocument = await json(await contained(artifacts, `${reselection.previous.suitePath}/suite-scope.json`));
  } else {
    await access(suiteScopePath).catch(async (error) => {
      if (error.code !== 'ENOENT') throw error;
      await mkdir(suiteDir, { recursive: true });
      const cases = Object.keys(index.packages).sort().map((id) => ({ id }));
      await writeFile(suiteScopePath, JSON.stringify({ $schema: RECIPE_SUITE_SCOPE_SCHEMA_URL, suite_id: `qa-${path.basename(task)}`, cases }, null, 2) + '\n', { flag: 'wx' });
    });
    await contained(artifacts, suitePath);
    scopeDocument = await json(suiteScopePath);
  }
  const scope = freezeRecipeSuiteScope(scopeDocument);
  assert.deepEqual(Object.keys(index.packages).sort(), scope.scope.cases.map((item) => item.id).sort());
  assert(Object.hasOwn(index.packages, index.smoke.caseId) && index.smoke.proofTarget, 'Smoke must name a declared case and proof target');
  if (reselection) {
    assert.deepEqual(reselection.previous.source, { baseSha: source.baseSha, headSha: source.headSha }, 'QA source changed');
    assert.equal(reselection.previous.scope.path, 'qa-scope.json', 'QA scope path changed');
    assert.equal(reselection.previous.scope.digest, digestRecipeDocument(source), 'Frozen QA scope changed');
    assert.equal(reselection.previous.scope.suiteDigest, digestRecipeDocument(scope.scope), 'Frozen QA cases changed');
    assert.deepEqual(index.smoke, reselection.previous.smoke, 'QA smoke selection changed');
    assert.deepEqual(Object.keys(index.packages).sort(), Object.keys(reselection.previous.packages).sort(), 'QA case selection changed');
  }
  const resolutions = [];
  for (const [id, relative] of Object.entries(index.packages)) {
    const directory = await contained(artifacts, relative);
    const [recipe, summary, trace, manifest, recipeResolution] = await Promise.all(
      ['recipe.json', 'summary.json', 'trace.json', 'artifact-manifest.json', 'recipe-resolution.json'].map((file) => json(path.join(directory, file))),
    );
    const resolvedRecipes = {};
    const artifactPaths = ['recipe.json', 'summary.json', 'trace.json', 'artifact-manifest.json', 'recipe-resolution.json'];
    for (const dependency of recipeResolution.dependencies) {
      resolvedRecipes[dependency.digest] = await json(await contained(directory, dependency.artifact));
      artifactPaths.push(dependency.artifact);
    }
    for (const artifact of manifest.artifacts) {
      await contained(directory, artifact.path);
      artifactPaths.push(artifact.path);
    }
    validateRuntimeProof({ recipe, summary, trace, manifest, recipeResolution, resolvedRecipes, artifactPaths }, id === index.smoke.caseId ? index.smoke.proofTarget : undefined);
    if (reselection) assert.equal(summary.status, 'pass', `QA case ${id} has no passing attempt`);
    resolutions.push({ id, kind: 'verdict', result: { status: summary.status, summaryPath: path.join(directory, 'summary.json') } });
  }
  if (checkOnly) return { status: 'pass', packages: Object.keys(index.packages), smoke: index.smoke };
  if (reselection) {
    await mkdir(suiteDir);
    await writeFile(suiteScopePath, JSON.stringify(scope.scope, null, 2) + '\n', { flag: 'wx' });
  }
  await finalizeRecipeSuite({ scope, resolutions, outputDir: suiteDir });
  const result = { version: 1, source: { baseSha: source.baseSha, headSha: source.headSha }, suitePath, scope: { path: 'qa-scope.json', digest: digestRecipeDocument(source), suiteDigest: digestRecipeDocument(scope.scope) }, packages: index.packages, smoke: index.smoke };
  if (reselection) return result;
  await writeFile(resultPath, JSON.stringify(result, null, 2) + '\n', { flag: 'wx' });
  // A farm-dispatched task also needs the gateway's result binding: the same
  // proof, bound to the run id and the admitted profile and inputs copied
  // verbatim from inputs/qa.json. Written here so a worker never hand-authors
  // (or invents digests for) the document the gateway compares byte for byte.
  const farmInputPath = path.join(task, 'inputs', 'qa.json');
  const farmInput = await access(farmInputPath).then(() => json(farmInputPath), (error) => { if (error.code === 'ENOENT') return null; throw error; });
  if (farmInput) {
    assert(typeof farmInput.runId === 'string' && record(farmInput.profile) && record(farmInput.inputs), 'inputs/qa.json must carry runId, profile and inputs');
    const farmResultPath = path.join(artifacts, 'qa-result.json');
    await writeFile(farmResultPath, JSON.stringify({ version: 1, runId: farmInput.runId, qa: { profile: farmInput.profile, inputs: farmInput.inputs }, ...result }, null, 2) + '\n', { flag: 'wx' });
  }
  return resultPath;
}

const USAGE = 'Usage: finalize-qa --task <task-dir> --index <packages-and-smoke.json> [--suite qa-suite] [--check-only | --reselect]';

if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  let values;
  try {
    ({ values } = parseArgs({ options: { task: { type: 'string' }, index: { type: 'string' }, suite: { type: 'string' }, 'check-only': { type: 'boolean' }, reselect: { type: 'boolean' }, help: { type: 'boolean' } } }));
  } catch (error) {
    if (error.code !== 'ERR_PARSE_ARGS_UNKNOWN_OPTION' && error.code !== 'ERR_PARSE_ARGS_INVALID_OPTION_VALUE') throw error;
    console.error(`${error.message}\n${USAGE}`);
    process.exit(2);
  }
  if (values.help) {
    console.log(USAGE);
  } else if (!values.task || !values.index) {
    console.error(USAGE);
    process.exit(2);
  } else {
    assert(!values.reselect || (!values['check-only'] && !values.suite), '--reselect cannot be combined with --check-only or --suite');
    const index = await json(values.index);
    const result = values.reselect
      ? await reselectQa(values.task, index, finalizeQa)
      : await finalizeQa(values.task, index, values.suite, values['check-only'] === true);
    console.log(typeof result === 'string' ? result : JSON.stringify(result, null, 2));
  }
}
